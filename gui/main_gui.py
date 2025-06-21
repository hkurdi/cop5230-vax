# main_gui.py
# Main GUI Application Module
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

import pygame
import pygwidgets
import sys

# import our modular classes
from config import GUIConfiguration
from form_handler import PatientFormHandler
from display_handler import PatientDisplayHandler
from classes.person.person import Person
from classes.person.vaccine_manager import VaccineManager
from systems.report_system import ReportManager
from systems.dialog_system import DialogManager


class VaccineTrackerGUI:
    """
    Main GUI class that handles the whole application.
    I split things up into different classes to make it easier to work with.
    """
    
    def __init__(self):
        # using seperate classes to handle different parts of the GUI
        self.__config = GUIConfiguration()
        self.__manager = VaccineManager()
        self.__report_manager = ReportManager(self.__manager)
        
        # keeping track of what patient we're looking at
        self.__current_index = -1
        self.__running = True
        
        # initialize pygame stuff
        pygame.init()
        
        # setup the window using our config class
        window_size = self.__config.get_window_size()
        self.__window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(self.__config.get_window_title())
        self.__clock = pygame.time.Clock()
        
        # get the colors we'll be using
        self.__colors = self.__config.get_colors()
        
        # create the different handler classes
        self.__form_handler = PatientFormHandler(self.__window, self.__config)
        self.__display_handler = PatientDisplayHandler(self.__window, self.__config)
        self.__dialog_manager = DialogManager(self.__window, self.__colors)
        
        # setup the main GUI widgets
        self.__setup_main_widgets()
        
        # update the display to show current state
        self.__update_patient_display()
        
        # start running the app
        self.__run()
    
    def __setup_main_widgets(self):
        """
        Sets up the main widgets for the GUI.
        I separated this from __init__ to keep things cleaner.
        """
        self.__main_widgets = []
        
        card_left = self.__config.get_card_margin()
        card_width = 760
        
        # main title at the top
        header = pygwidgets.DisplayText(
            self.__window, (card_left, 25), "Vaccine Tracker",
            fontSize=28, textColor=self.__colors['primary'], justified='center', width=card_width
        )
        self.__main_widgets.append(header)
        
        # subtitle with my name and course info
        subtitle = pygwidgets.DisplayText(
            self.__window, (card_left, 55), "COP5230 Hamza Kurdi - Enhanced OOP Version",
            fontSize=14, textColor=self.__colors['text_light'], justified='center', width=card_width
        )
        self.__main_widgets.append(subtitle)
        
        # button to add new patient
        self.__add_button = pygwidgets.TextButton(
            self.__window, (320, 395), "Add Patient to System"
        )
        self.__main_widgets.append(self.__add_button)
        
        # setup the action buttons at the bottom
        self.__setup_action_buttons()
    
    def __setup_action_buttons(self):
        """
        Creates all the action buttons at the bottom of the screen.
        Using a dictionary to make it easier to manage the button positions.
        """
        button_config = {
            'width': 120,
            'height': 30,
            'start_y': 650,
            'margin': 10,
            'total_buttons': 6
        }
        
        # calculate where to put each button
        window_width = self.__config.get_window_size()[0]
        usable_width = window_width - 2 * button_config['margin']
        total_spacing = usable_width - (button_config['width'] * button_config['total_buttons'])
        spacing = total_spacing // (button_config['total_buttons'] - 1)
        
        # button definitions with their callback functions
        button_defs = [
            ("Individual Report", self.__handle_individual_report),
            ("Vaccine Statistics", self.__handle_vaccine_stats),
            ("Symptom Analysis", self.__handle_symptom_analysis),
            ("Reset Data", self.__handle_reset_data),
            ("Delete All Patients", self.__handle_delete_all),
            ("Exit Application", self.__handle_exit)
        ]
        
        self.__action_buttons = {}
        
        # create each button in a loop to avoid repetition
        for i, (label, callback) in enumerate(button_defs):
            x_pos = button_config['margin'] + i * (button_config['width'] + spacing)
            
            button = pygwidgets.TextButton(
                self.__window, (x_pos, button_config['start_y']), label,
                width=button_config['width'], height=button_config['height']
            )
            
            # store the button with its callback for later use
            self.__action_buttons[button] = callback
            self.__main_widgets.append(button)
    
    def __handle_events(self, event):
        """
        Handles all the pygame events like mouse clicks and keyboard stuff.
        Checks dialogs first, then form widgets, then main buttons.
        """
        # dialog events get priority over everything else
        if self.__dialog_manager.handle_dialog_events(event):
            return
        
        # handle form widget events
        for widget in self.__form_handler.get_form_widgets():
            if hasattr(widget, 'handleEvent') and widget.handleEvent(event):
                return
        
        # handle display widget events (the prev/next buttons)
        nav_buttons = self.__display_handler.get_nav_buttons()
        if nav_buttons['prev'].handleEvent(event):
            self.__navigate_previous()
            return
        elif nav_buttons['next'].handleEvent(event):
            self.__navigate_next()
            return
        
        # handle main widget events
        for widget in self.__main_widgets:
            if hasattr(widget, 'handleEvent') and widget.handleEvent(event):
                if widget == self.__add_button:
                    self.__handle_add_patient()
                    return
                
                # check if it's one of our action buttons
                if widget in self.__action_buttons:
                    callback = self.__action_buttons[widget]
                    callback()  # call the function we stored
                    return
    
    def __handle_add_patient(self):
        """
        Adds a new patient to the system after validating the form data.
        Fixed a bug where navigation wasn't working properly after adding.
        """
        try:
            # first check if all required fields are filled out
            is_valid, error_msg = self.__form_handler.validate_required_fields()
            if not is_valid:
                self.__dialog_manager.show_error_dialog("Validation Error", error_msg)
                return
            
            # get the data from the form
            form_data = self.__form_handler.get_form_data()
            
            # make sure we don't have duplicate IDs
            if self.__manager.get_person_by_id(form_data['id']):
                self.__dialog_manager.show_error_dialog(
                    "Duplicate ID", "A patient with this ID already exists in the system."
                )
                return
            
            # check if we're at the capacity limit
            if self.__manager.get_person_count() >= self.__manager.get_max_capacity():
                self.__dialog_manager.show_error_dialog(
                    "System Limit", f"Maximum of {self.__manager.get_max_capacity()} patients allowed."
                )
                return
            
            # create new person object
            person = Person(
                form_data['id'], form_data['first_name'], form_data['last_name'],
                form_data['phone'], form_data['address']
            )
            
            # set the medical data using the bulk update method
            person.update_medical_data(
                vaccines=form_data['vaccines'],
                symptoms=form_data['symptoms']
            )
            
            # try to add to the manager
            if self.__manager.add_person(person):
                # FIXED: Set current index properly for new patient
                was_empty = self.__manager.get_person_count() == 1
                if was_empty:
                    self.__current_index = 0  # show first patient immediately
                else:
                    self.__current_index = self.__manager.get_person_count() - 1  # show the new patient
                
                self.__update_patient_display()
                
                success_msg = f"Patient {form_data['first_name']} {form_data['last_name']} has been successfully added to the system."
                self.__dialog_manager.show_info_dialog("Success!", success_msg)
                self.__form_handler.clear_form()
            else:
                self.__dialog_manager.show_error_dialog(
                    "Add Failed", "Unable to add patient to system."
                )
        
        except Exception as e:
            self.__dialog_manager.show_error_dialog("System Error", f"An unexpected error occurred: {str(e)}")
            
    def __navigate_previous(self):
        """Go to the previous patient in the list"""
        if self.__current_index > 0:
            self.__current_index -= 1
            self.__update_patient_display()
    
    def __navigate_next(self):
        """Go to the next patient in the list"""
        if self.__current_index < self.__manager.get_person_count() - 1:
            self.__current_index += 1
            self.__update_patient_display()
    
    def __update_patient_display(self):
        """
        Updates the patient display area with the current patient info.
        Uses the display handler class to keep the code organized.
        """
        current_person = None
        total_count = self.__manager.get_person_count()
        
        # make sure we have a valid index
        if total_count > 0:
            if self.__current_index < 0:
                self.__current_index = 0
            elif self.__current_index >= total_count:
                self.__current_index = total_count - 1
            
            current_person = self.__manager.get_person_by_index(self.__current_index)
        
        # let the display handler update the display
        self.__display_handler.update_patient_display(current_person, self.__current_index, total_count)
    
    # Action button handlers for generating reports
    def __handle_individual_report(self):
        """Handles generating a report for a specific patient by ID"""
        if self.__manager.get_person_count() == 0:
            self.__dialog_manager.show_info_dialog(
                "No Patients", "No patients in the system.\n\nAdd patients first to generate individual reports."
            )
            return
        
        # show user what patient IDs are available
        available_ids = [str(p.id) for p in self.__manager.get_people()]
        ids_text = ", ".join(available_ids)
        prompt = f"Enter the patient ID to generate report:\n\nAvailable Patient IDs: {ids_text}"
        
        self.__dialog_manager.show_input_dialog(
            "Individual Patient Report", prompt, self.__process_individual_report
        )
    
    def __process_individual_report(self, id_input: str):
        """
        Processes the patient ID input and generates the report.
        This gets called back from the input dialog.
        """
        if id_input is None:  # user cancelled the dialog
            return
        
        try:
            if not id_input.strip():
                self.__dialog_manager.show_error_dialog("Invalid Input", "Please enter a patient ID.")
                return
            
            patient_id = int(id_input.strip())
            
            # generate the report using our report manager
            report_content = self.__report_manager.generate_individual_report(
                patient_id, include_header=True, include_stats=True
            )
            
            if "Error" in report_content:
                # show which IDs are actually available
                available_ids = [str(p.id) for p in self.__manager.get_people()]
                ids_text = ", ".join(available_ids)
                error_msg = f"No patient with ID {patient_id} found.\n\nAvailable IDs: {ids_text}"
                self.__dialog_manager.show_error_dialog("Patient Not Found", error_msg)
            else:
                self.__dialog_manager.show_info_dialog("Patient Report Generated", report_content)
                
        except ValueError:
            self.__dialog_manager.show_error_dialog(
                "Invalid Input", "Patient ID must be a valid number.\n\nPlease enter only numeric values."
            )
        except Exception as e:
            self.__dialog_manager.show_error_dialog("Report Error", f"Unable to generate report: {str(e)}")
    
    def __handle_vaccine_stats(self):
        """Shows vaccination statistics for all patients in the system"""
        report_content = self.__report_manager.generate_vaccination_stats(
            include_header=True, include_stats=False
        )
        self.__dialog_manager.show_info_dialog("Vaccination Statistics", report_content)
    
    def __handle_symptom_analysis(self):
        """Shows symptom analysis for all patients in the system"""
        report_content = self.__report_manager.generate_symptom_analysis(
            include_header=True, include_stats=False
        )
        self.__dialog_manager.show_info_dialog("Symptom Analysis", report_content)
        
    def __handle_reset_data(self):
        """Handle resetting all medical data with confirmation dialog"""
        # prevent multiple dialogs from opening
        if self.__dialog_manager.get_is_active():
            return
            
        if self.__manager.get_person_count() == 0:
            self.__dialog_manager.show_info_dialog(
                "Reset Data", "No patient data to reset.\n\nThe system is already empty."
            )
            return
        
        patient_count = self.__manager.get_person_count()
        confirm_msg = (
            f"Are you sure you want to reset ALL vaccination and symptom data?\n\n"
            f"This will affect {patient_count} patient(s):\n"
            f"• All vaccination records will be cleared\n"
            f"• All symptom data will be removed\n"
            f"• Patient information (names, IDs) will be kept\n\n"
            f"This action cannot be undone."
        )
        
        self.__dialog_manager.show_confirmation_dialog(
            "Confirm Data Reset", confirm_msg, self.__process_reset_confirmation
        )
    
    def __process_reset_confirmation(self, confirmed: bool):
        """Process the reset confirmation callback"""
        if confirmed:
            self.__manager.reset_all_medical_data()
            self.__dialog_manager.show_info_dialog(
                "Reset Complete",
                f"All vaccination and symptom data has been cleared for {self.__manager.get_person_count()} patient(s).\n\nPatient information has been preserved."
            )
            self.__update_patient_display()
            self.__form_handler.clear_form()
            
    def __handle_delete_all(self):
        """Handle deleting all patients with confirmation dialog"""
        # prevent multiple dialogs from opening accidentally
        if self.__dialog_manager.get_is_active():
            return
            
        if self.__manager.get_person_count() == 0:
            self.__dialog_manager.show_info_dialog(
                "Delete All Patients", "No patients to delete.\n\nThe system is already empty."
            )
            return
        
        patient_count = self.__manager.get_person_count()
        warning_msg = (
            f"⚠️ WARNING: This will permanently delete ALL {patient_count} patient(s)!\n\n"
            f"This includes:\n"
            f"• All patient information\n"
            f"• All vaccination records\n"
            f"• All symptom data\n\n"
            f"This action is PERMANENT and cannot be undone!\n\n"
            f"Are you absolutely sure?"
        )
        
        self.__dialog_manager.show_confirmation_dialog(
            "⚠️ DANGER: Confirm Complete Deletion", warning_msg, self.__process_delete_confirmation
        )

    def __process_delete_confirmation(self, confirmed: bool):
        """Process the delete confirmation callback"""
        if confirmed:
            patient_count = self.__manager.get_person_count()
            self.__manager.clear_all_people()
            self.__current_index = -1
            self.__update_patient_display()
            self.__form_handler.clear_form()
            
            self.__dialog_manager.show_info_dialog(
                "Deletion Complete",
                f"All {patient_count} patient record(s) have been permanently deleted from the system."
            )
    
    def __handle_exit(self):
        """Handle application exit with a confirmation dialog"""
        self.__dialog_manager.show_confirmation_dialog(
            "Exit Application",
            "Are you sure you want to close the Vaccine Tracker?\n\nAny unsaved work will be lost.",
            self.__process_exit_confirmation
        )
    
    def __process_exit_confirmation(self, confirmed: bool):
        """Process the exit confirmation callback"""
        if confirmed:
            self.__running = False
            pygame.quit()
            sys.exit()
    
    def __draw_modern_card(self, x: int, y: int, width: int, height: int, color: tuple = None):
        """
        Draws nice looking cards with shadow effects.
        You can specify a custom color or it'll use the default card color.
        """
        if color is None:
            color = self.__colors['card']
        
        # draw shadow first
        shadow_rect = pygame.Rect(x + 3, y + 3, width, height)
        pygame.draw.rect(self.__window, (0, 0, 0, 30), shadow_rect, border_radius=12)
        
        # draw the main card
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.__window, color, card_rect, border_radius=12)
        pygame.draw.rect(self.__window, self.__colors['border'], card_rect, 2, border_radius=12)
    
    def __draw(self):
        """
        Draws everything on the screen each frame.
        Calls the different handler classes to draw their parts.
        """
        # clear the screen
        self.__window.fill(self.__colors['bg'])
        
        # draw the modern card backgrounds
        margin = self.__config.get_card_margin()
        self.__draw_modern_card(margin, 10, 760, 85)  # header card
        self.__draw_modern_card(margin, 105, 760, 320, self.__colors['form_bg'])  # form card
        self.__draw_modern_card(margin, 435, 680, 170)  # display card
        self.__draw_modern_card(710, 490, 70, 70)  # status indicator card
        
        # draw all the widgets
        for widget in self.__main_widgets:
            widget.draw()
        
        for widget in self.__form_handler.get_form_widgets():
            widget.draw()
        
        for widget in self.__display_handler.get_display_widgets():
            widget.draw()
        
        # draw the status indicator circle
        self.__display_handler.draw_status_indicator()
        
        # draw any active dialog
        self.__dialog_manager.draw_dialog()
        
        # update the display
        pygame.display.flip()
    
    def __run(self):
        """
        Main application loop that keeps everything running.
        Handles events and redraws the screen at 60 FPS.
        """
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                else:
                    self.__handle_events(event)
            
            self.__draw()
            self.__clock.tick(60)
        
        pygame.quit()
        sys.exit()


# Entry point for the application
if __name__ == "__main__":
    # create and run the GUI application
    app = VaccineTrackerGUI()