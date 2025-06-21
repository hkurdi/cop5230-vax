# main_gui.py
# Main GUI Application Module
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

import pygame
import pygwidgets
import sys

# import our modular classes
from .config.config import GUIConfiguration
from .handlers.form_handler import PatientFormHandler
from .handlers.display_handler import PatientDisplayHandler
from classes.person.person import Person
from classes.person.vaccine_manager import VaccineManager
from systems.report.report_system import ReportManager
from systems.dialog.dialog_system import DialogManager
from systems.animation.animation_system import AnimationManager


class VaccineTrackerGUI:
    """
    Main GUI class that handles the whole application.
    I split things up into different classes to make it easier to work with.
    """
    
    def __init__(self):
        # using seperate classes for different parts - makes debugging easier
        self.__config = GUIConfiguration()
        self.__manager = VaccineManager()
        self.__report_manager = ReportManager(self.__manager)
        
        # track current patient index
        self.__current_index = -1
        self.__running = True
        
        # setup pygame
        pygame.init()
        
        # create the main window
        window_size = self.__config.get_window_size()
        self.__window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(self.__config.get_window_title())
        self.__clock = pygame.time.Clock()
        
        # load colors from config
        self.__colors = self.__config.get_colors()
        
        # initialize all the handlers
        self.__form_handler = PatientFormHandler(self.__window, self.__config)
        self.__display_handler = PatientDisplayHandler(self.__window, self.__config)
        self.__dialog_manager = DialogManager(self.__window, self.__colors)
        self.__animation_manager = AnimationManager(self.__window, self.__colors)
        
        # setup widgets
        self.__setup_main_widgets()
        
        # update display
        self.__update_patient_display()
        
        # start main loop
        self.__run()
    
    def __setup_main_widgets(self):
        """
        Creates main widgets for the interface.
        Moved this out of __init__ so it's not so cluttered.
        """
        self.__main_widgets = []
        
        card_left = self.__config.get_card_margin()
        card_width = 760
        
        # title text at top
        header = pygwidgets.DisplayText(
            self.__window, (card_left, 25), "Vaccine Tracker",
            fontSize=28, textColor=self.__colors['primary'], justified='center', width=card_width
        )
        self.__main_widgets.append(header)
        
        # subtitle w/ course info
        subtitle = pygwidgets.DisplayText(
            self.__window, (card_left, 55), "COP5230 Hamza Kurdi - Enhanced OOP Version",
            fontSize=14, textColor=self.__colors['text_light'], justified='center', width=card_width
        )
        self.__main_widgets.append(subtitle)
        
        # add patient button
        self.__add_button = pygwidgets.TextButton(
            self.__window, (320, 395), "Add Patient to System"
        )
        self.__main_widgets.append(self.__add_button)
        
        # create action buttons
        self.__setup_action_buttons()
    
    def __setup_action_buttons(self):
        """
        Sets up the bottom action buttons.
        Used a dict to handle positioning - easier than calculating manually each time.
        """
        button_config = {
            'width': 120,
            'height': 30,
            'start_y': 650,
            'margin': 10,
            'total_buttons': 6
        }
        
        # figure out button spacing
        window_width = self.__config.get_window_size()[0]
        usable_width = window_width - 2 * button_config['margin']
        total_spacing = usable_width - (button_config['width'] * button_config['total_buttons'])
        spacing = total_spacing // (button_config['total_buttons'] - 1)
        
        # button labels and functions
        button_defs = [
            ("Individual Report", self.__handle_individual_report),
            ("Vaccine Statistics", self.__handle_vaccine_stats),
            ("Symptom Analysis", self.__handle_symptom_analysis),
            ("Reset Data", self.__handle_reset_data),
            ("Delete All Patients", self.__handle_delete_all),
            ("Exit Application", self.__handle_exit)
        ]
        
        self.__action_buttons = {}
        
        # create buttons in loop
        for i, (label, callback) in enumerate(button_defs):
            x_pos = button_config['margin'] + i * (button_config['width'] + spacing)
            
            button = pygwidgets.TextButton(
                self.__window, (x_pos, button_config['start_y']), label,
                width=button_config['width'], height=button_config['height']
            )
            
            # store button w/ callback
            self.__action_buttons[button] = callback
            self.__main_widgets.append(button)
    
    def __handle_events(self, event):
        """
        Handles pygame events - mouse clicks, keyboard, etc.
        Prioritizes dialogs first, then forms, then main buttons.
        """
        # dialog events first - most important
        if self.__dialog_manager.handle_dialog_events(event):
            return
        
        # check form widgets
        for widget in self.__form_handler.get_form_widgets():
            if hasattr(widget, 'handleEvent') and widget.handleEvent(event):
                return
        
        # navigation buttons (prev/next)
        nav_buttons = self.__display_handler.get_nav_buttons()
        if nav_buttons['prev'].handleEvent(event):
            self.__navigate_previous()
            return
        elif nav_buttons['next'].handleEvent(event):
            self.__navigate_next()
            return
        
        # main widgets
        for widget in self.__main_widgets:
            if hasattr(widget, 'handleEvent') and widget.handleEvent(event):
                if widget == self.__add_button:
                    self.__handle_add_patient()
                    return
                
                # check action buttons
                if widget in self.__action_buttons:
                    callback = self.__action_buttons[widget]
                    callback()  # run the function
                    return
    
    def __handle_add_patient(self):
        """
        Adds new patient after validating form.
        Had to fix navigation bug - wasn't showing new patient correctly.
        """
        try:
            # validate required fields first
            is_valid, error_msg = self.__form_handler.validate_required_fields()
            if not is_valid:
                self.__animation_manager.show_notification("Please fill required fields", "error")
                self.__dialog_manager.show_error_dialog("Validation Error", error_msg)
                return
            
            # get form data
            form_data = self.__form_handler.get_form_data()
            
            # check for duplicate IDs
            if self.__manager.get_person_by_id(form_data['id']):
                self.__animation_manager.show_notification("Duplicate ID detected", "error")
                self.__dialog_manager.show_error_dialog(
                    "Duplicate ID", "A patient with this ID already exists in the system."
                )
                return
            
            # check capacity limit
            if self.__manager.get_person_count() >= self.__manager.get_max_capacity():
                self.__dialog_manager.show_error_dialog(
                    "System Limit", f"Maximum of {self.__manager.get_max_capacity()} patients allowed."
                )
                return
            
            # create person object
            person = Person(
                form_data['id'], form_data['first_name'], form_data['last_name'],
                form_data['phone'], form_data['address']
            )
            
            # add medical data
            person.update_medical_data(
                vaccines=form_data['vaccines'],
                symptoms=form_data['symptoms']
            )
            
            # add to manager
            if self.__manager.add_person(person):
                # BUGFIX: navigation index wasn't updating right
                was_empty = self.__manager.get_person_count() == 1
                if was_empty:
                    self.__current_index = 0  # first patient
                else:
                    self.__current_index = self.__manager.get_person_count() - 1  # newest patient
                
                self.__update_patient_display()
                
                # show success animations
                self.__animation_manager.pulse_status_briefly()
                self.__animation_manager.show_notification(f"Patient {form_data['first_name']} added successfully!", "success")
                
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
        """Previous patient"""
        if self.__current_index > 0:
            self.__current_index -= 1
            self.__update_patient_display()
            # show nav notification
            current_person = self.__manager.get_person_by_index(self.__current_index)
            self.__animation_manager.show_notification(f"← {current_person.get_first_name()}", "info")
    
    def __navigate_next(self):
        """Next patient"""
        if self.__current_index < self.__manager.get_person_count() - 1:
            self.__current_index += 1
            self.__update_patient_display()
            # show nav notification
            current_person = self.__manager.get_person_by_index(self.__current_index)
            self.__animation_manager.show_notification(f"{current_person.get_first_name()} →", "info")
    
    def __update_patient_display(self):
        """
        Updates patient display area.
        Using display handler to keep things organized.
        """
        current_person = None
        total_count = self.__manager.get_person_count()
        
        # validate index bounds
        if total_count > 0:
            if self.__current_index < 0:
                self.__current_index = 0
            elif self.__current_index >= total_count:
                self.__current_index = total_count - 1
            
            current_person = self.__manager.get_person_by_index(self.__current_index)
        
        # update display
        self.__display_handler.update_patient_display(current_person, self.__current_index, total_count)
    
    # Report button handlers
    def __handle_individual_report(self):
        """Generate report for specific patient"""
        if self.__manager.get_person_count() == 0:
            self.__dialog_manager.show_info_dialog(
                "No Patients", "No patients in the system.\n\nAdd patients first to generate individual reports."
            )
            return
        
        # show available IDs to user
        available_ids = [str(p.id) for p in self.__manager.get_people()]
        ids_text = ", ".join(available_ids)
        prompt = f"Enter the patient ID to generate report:\n\nAvailable Patient IDs: {ids_text}"
        
        self.__dialog_manager.show_input_dialog(
            "Individual Patient Report", prompt, self.__process_individual_report
        )
    
    def __process_individual_report(self, id_input: str):
        """
        Process patient ID input and generate report.
        Callback from input dialog.
        """
        if id_input is None:  # user cancelled
            return
        
        try:
            if not id_input.strip():
                self.__dialog_manager.show_error_dialog("Invalid Input", "Please enter a patient ID.")
                return
            
            patient_id = int(id_input.strip())
            
            # generate report
            report_content = self.__report_manager.generate_individual_report(
                patient_id, include_header=True, include_stats=True
            )
            
            if "Error" in report_content:
                # show available IDs
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
        """Show vaccination stats for all patients"""
        report_content = self.__report_manager.generate_vaccination_stats(
            include_header=True, include_stats=False
        )
        self.__dialog_manager.show_info_dialog("Vaccination Statistics", report_content)
    
    def __handle_symptom_analysis(self):
        """Show symptom analysis for all patients"""
        report_content = self.__report_manager.generate_symptom_analysis(
            include_header=True, include_stats=False
        )
        self.__dialog_manager.show_info_dialog("Symptom Analysis", report_content)
        
    def __handle_reset_data(self):
        """Reset all medical data w/ confirmation"""
        # dont allow multiple dialogs
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
        """Process reset confirmation"""
        if confirmed:
            patient_count = self.__manager.get_person_count()
            self.__manager.reset_all_medical_data()
            
            # show reset animation
            self.__animation_manager.pulse_status_briefly()
            self.__animation_manager.show_notification(f"Reset complete - {patient_count} patients affected", "info")
            
            self.__dialog_manager.show_info_dialog(
                "Reset Complete",
                f"All vaccination and symptom data has been cleared for {patient_count} patient(s).\n\nPatient information has been preserved."
            )
            self.__update_patient_display()
            self.__form_handler.clear_form()
            
    def __handle_delete_all(self):
        """Delete all patients w/ confirmation"""
        # prevent multiple dialogs opening
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
        """Process delete confirmation"""
        if confirmed:
            patient_count = self.__manager.get_person_count()
            self.__manager.clear_all_people()
            self.__current_index = -1
            
            # show delete animation
            self.__animation_manager.pulse_status_briefly()
            self.__animation_manager.show_notification(f"Deleted {patient_count} patients", "error")
            
            self.__update_patient_display()
            self.__form_handler.clear_form()
            
            self.__dialog_manager.show_info_dialog(
                "Deletion Complete",
                f"All {patient_count} patient record(s) have been permanently deleted from the system."
            )
    
    def __handle_exit(self):
        """Exit app w/ confirmation"""
        self.__dialog_manager.show_confirmation_dialog(
            "Exit Application",
            "Are you sure you want to close the Vaccine Tracker?\n\nAny unsaved work will be lost.",
            self.__process_exit_confirmation
        )
    
    def __process_exit_confirmation(self, confirmed: bool):
        """Process exit confirmation"""
        if confirmed:
            # cleanup before exit
            self.__animation_manager.cleanup_all()
            self.__running = False
            pygame.quit()
            sys.exit()
    
    def __get_current_status_info(self) -> tuple:
        """
        Get status color/text for animated indicator.
        Returns (color, text) tuple.
        """
        if self.__manager.get_person_count() == 0:
            return (self.__colors['text_light'], "?")
        
        if self.__current_index >= 0:
            current_person = self.__manager.get_people()[self.__current_index]
            if current_person.is_cleared_for_entry():
                return (self.__colors['success'], "+")
            else:
                return (self.__colors['danger'], "-")
        
        return (self.__colors['text_light'], "?")

    def __draw_modern_card(self, x: int, y: int, width: int, height: int, color: tuple = None):
        """
        Draw card with shadow effects.
        Custom color optional - uses default if not specified.
        """
        if color is None:
            color = self.__colors['card']
        
        # shadow first
        shadow_rect = pygame.Rect(x + 3, y + 3, width, height)
        pygame.draw.rect(self.__window, (0, 0, 0, 30), shadow_rect, border_radius=12)
        
        # main card
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.__window, color, card_rect, border_radius=12)
        pygame.draw.rect(self.__window, self.__colors['border'], card_rect, 2, border_radius=12)
    
    def __draw(self):
        """
        Draw everything each frame.
        Calls handler classes for their parts.
        """
        # clear screen
        self.__window.fill(self.__colors['bg'])
        
        # draw card backgrounds
        margin = self.__config.get_card_margin()
        self.__draw_modern_card(margin, 10, 760, 85)  # header
        self.__draw_modern_card(margin, 105, 760, 320, self.__colors['form_bg'])  # form
        self.__draw_modern_card(margin, 435, 680, 170)  # display
        self.__draw_modern_card(710, 490, 70, 70)  # status indicator
        
        # draw widgets
        for widget in self.__main_widgets:
            widget.draw()
        
        for widget in self.__form_handler.get_form_widgets():
            widget.draw()
        
        for widget in self.__display_handler.get_display_widgets():
            widget.draw()
        
        # draw animations and status
        status_color, status_text = self.__get_current_status_info()
        self.__animation_manager.draw_all_animations(status_color, status_text)
        
        # draw dialogs
        self.__dialog_manager.draw_dialog()
        
        # update display
        pygame.display.flip()
    
    def __run(self):
        """
        Main app loop - keeps everything running.
        Handles events and redraws.
        """
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                else:
                    self.__handle_events(event)
            
            # update animations first
            self.__animation_manager.update_all_animations()
            
            self.__draw()
            self.__clock.tick(60)
        
        pygame.quit()
        sys.exit()
        
# create and run GUI
if __name__ == "__main__":
    app = VaccineTrackerGUI()