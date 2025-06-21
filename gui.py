# gui.py
# Enhanced GUI using OOP principles with modularity and scalability
# COP5230 Assignment 2 M4 - Enhanced OOP Version
# 06/14/2025
# Hamza Kurdi

import pygame
import pygwidgets
import sys
from typing import Optional, Dict, Any

# import our enhanced modular classes
from person import Person, VaccineManager
from report_system import ReportManager
from dialog_system import DialogManager


class GUIConfiguration:
    """
    Configuration class for GUI settings and constants.
    Improves maintainability by centralizing configuration.
    """
    
    def __init__(self):
        # window settings
        self.__window_width = 800
        self.__window_height = 750
        self.__window_title = "Vaccine Tracker"
        
        # color scheme - private variables with getters
        self.__colors = {
            'bg': (245, 247, 250),
            'card': (255, 255, 255),
            'form_bg': (240, 240, 240),
            'primary': (59, 130, 246),
            'success': (34, 197, 94),
            'danger': (239, 68, 68),
            'warning': (245, 158, 11),
            'text_dark': (17, 24, 39),
            'text_light': (107, 114, 128),
            'border': (229, 231, 235),
            'hover': (243, 244, 246)
        }
        
        # layout constants
        self.__card_margin = 20
        self.__form_columns = 2
        self.__button_spacing = 10
    
    # getters for configuration values
    def get_window_size(self) -> tuple:
        """Getter for window dimensions"""
        return (self.__window_width, self.__window_height)
    
    def get_window_title(self) -> str:
        """Getter for window title"""
        return self.__window_title
    
    def get_colors(self) -> Dict[str, tuple]:
        """Getter for color scheme"""
        return self.__colors.copy()  # return copy for encapsulation
    
    def get_card_margin(self) -> int:
        """Getter for card margin"""
        return self.__card_margin
    
    def set_window_title(self, title: str):
        """Setter for window title"""
        self.__window_title = title
    
    def update_color(self, color_name: str, color_value: tuple):
        """Setter for individual colors"""
        if color_name in self.__colors:
            self.__colors[color_name] = color_value


class PatientFormHandler:
    """
    Separate class for handling patient form operations.
    Improves modularity and single responsibility principle.
    """
    
    def __init__(self, window, config: GUIConfiguration):
        self.__window = window
        self.__config = config
        self.__colors = config.get_colors()
        
        # form widgets - private variables
        self.__form_widgets = []
        self.__input_fields = {}
        self.__checkboxes = {}
        
        self.__setup_form_widgets()
    
    def __setup_form_widgets(self):
        """
        Private method to setup form widgets.
        Demonstrates encapsulation.
        """
        # clear existing widgets
        self.__form_widgets.clear()
        self.__input_fields.clear()
        self.__checkboxes.clear()
        
        form_start_y = 110
        col1_x = 70
        col2_x = 420
        entry_width = 180
        
        # form header
        header = pygwidgets.DisplayText(
            self.__window, (50, form_start_y), "Add New Patient",
            fontSize=16, textColor=self.__colors['text_dark']
        )
        self.__form_widgets.append(header)
        
        # create input fields with labels
        self.__create_input_field("id", "Patient ID *", col1_x, form_start_y + 35, entry_width)
        self.__create_input_field("fname", "First Name *", col1_x, form_start_y + 80, entry_width)
        self.__create_input_field("lname", "Last Name *", col1_x, form_start_y + 125, entry_width)
        self.__create_input_field("phone", "Phone Number", col2_x, form_start_y + 35, entry_width)
        self.__create_input_field("addr", "Address", col2_x, form_start_y + 80, int(entry_width * 1.2))
        
        # vaccine checkboxes
        vaccine_y = 290
        self.__create_section_header("Vaccination Status", 70, vaccine_y)
        self.__create_checkbox("covid", "COVID-19 Vaccine", 85, vaccine_y + 25)
        self.__create_checkbox("influenza", "Influenza Vaccine", 85, vaccine_y + 50)
        self.__create_checkbox("ebola", "Ebola Vaccine", 85, vaccine_y + 75)
        
        # symptom checkboxes
        self.__create_section_header("Current Symptoms", 420, vaccine_y)
        self.__create_checkbox("fever", "Fever", 435, vaccine_y + 25)
        self.__create_checkbox("fatigue", "Fatigue", 435, vaccine_y + 50)
        self.__create_checkbox("headache", "Headache", 435, vaccine_y + 75)
    
    def __create_input_field(self, field_id: str, label: str, x: int, y: int, width: int):
        """
        Private helper method to create input field with label.
        Uses positional arguments for layout.
        """
        # create label
        label_widget = pygwidgets.DisplayText(
            self.__window, (x, y), label, fontSize=11, textColor=self.__colors['text_dark']
        )
        self.__form_widgets.append(label_widget)
        
        # create input field
        input_widget = pygwidgets.InputText(
            self.__window, (x, y + 15), width=width
        )
        self.__form_widgets.append(input_widget)
        self.__input_fields[field_id] = input_widget
    
    def __create_checkbox(self, checkbox_id: str, label: str, x: int, y: int):
        """Private helper method to create checkbox"""
        checkbox = pygwidgets.TextCheckBox(
            self.__window, (x, y), label, value=False
        )
        self.__form_widgets.append(checkbox)
        self.__checkboxes[checkbox_id] = checkbox
    
    def __create_section_header(self, text: str, x: int, y: int):
        """Private helper method to create section headers"""
        header = pygwidgets.DisplayText(
            self.__window, (x, y), text, fontSize=14, textColor=self.__colors['text_dark']
        )
        self.__form_widgets.append(header)
    
    def get_form_widgets(self) -> list:
        """Getter for form widgets list"""
        return self.__form_widgets
    
    def get_form_data(self) -> Dict[str, Any]:
        """
        Extract and validate form data.
        Returns dict with form values or raises exception for invalid data.
        """
        try:
            # get basic info
            data = {
                'id': int(self.__input_fields['id'].getValue().strip()),
                'first_name': self.__input_fields['fname'].getValue().strip(),
                'last_name': self.__input_fields['lname'].getValue().strip(),
                'phone': self.__input_fields['phone'].getValue().strip(),
                'address': self.__input_fields['addr'].getValue().strip(),
            }
            
            # get vaccine status
            data['vaccines'] = {
                'covid19': self.__checkboxes['covid'].getValue(),
                'influenza': self.__checkboxes['influenza'].getValue(),
                'ebola': self.__checkboxes['ebola'].getValue()
            }
            
            # get symptoms
            data['symptoms'] = {
                'fever': self.__checkboxes['fever'].getValue(),
                'fatigue': self.__checkboxes['fatigue'].getValue(),
                'headache': self.__checkboxes['headache'].getValue()
            }
            
            return data
            
        except ValueError as e:
            raise ValueError("Patient ID must be a valid number")
        except Exception as e:
            raise Exception(f"Error reading form data: {str(e)}")
    
    def clear_form(self):
        """Clear all form fields"""
        # clear input fields
        for field in self.__input_fields.values():
            field.setValue("")
        
        # clear checkboxes
        for checkbox in self.__checkboxes.values():
            checkbox.setValue(False)
    
    def validate_required_fields(self) -> tuple:
        """
        Validate required form fields.
        Returns (is_valid, error_message) tuple.
        """
        # check required fields
        if not self.__input_fields['id'].getValue().strip():
            return (False, "Patient ID is required to continue.")
        
        if not self.__input_fields['fname'].getValue().strip():
            return (False, "First name is required to continue.")
        
        if not self.__input_fields['lname'].getValue().strip():
            return (False, "Last name is required to continue.")
        
        # check if ID is numeric
        try:
            int(self.__input_fields['id'].getValue().strip())
        except ValueError:
            return (False, "Patient ID must be a valid number.")
        
        return (True, "")


class PatientDisplayHandler:
    """
    Separate class for handling patient display operations.
    Demonstrates single responsibility principle and modularity.
    """
    
    def __init__(self, window, config: GUIConfiguration):
        self.__window = window
        self.__config = config
        self.__colors = config.get_colors()
        
        # display widgets - private variables
        self.__display_widgets = []
        self.__patient_text = None
        self.__counter_label = None
        self.__nav_buttons = {}
        
        # status indicator properties
        self.__indicator_pos = (720, 530)
        self.__indicator_color = self.__colors['text_light']
        
        self.__setup_display_widgets()
    
    def __setup_display_widgets(self):
        """Private method to setup patient display widgets"""
        self.__display_widgets.clear()
        self.__nav_buttons.clear()
        
        # patient overview label
        overview_label = pygwidgets.DisplayText(
            self.__window, (50, 440), "Patient Overview",
            fontSize=16, textColor=self.__colors['text_dark']
        )
        self.__display_widgets.append(overview_label)
        
        # main patient text display
        self.__patient_text = pygwidgets.DisplayText(
            self.__window, (50, 465),
            "No patients registered in the system.\n\nUse the form above to add your first patient.",
            fontSize=11, textColor=self.__colors['text_dark'], width=600, height=130
        )
        self.__display_widgets.append(self.__patient_text)
        
        # counter label
        self.__counter_label = pygwidgets.DisplayText(
            self.__window, (20, 75), "No patients registered",
            fontSize=12, textColor=self.__colors['text_dark'], justified='center', width=760
        )
        self.__display_widgets.append(self.__counter_label)
        
        # navigation buttons
        self.__nav_buttons['prev'] = pygwidgets.TextButton(
            self.__window, (280, 605), "Previous"
        )
        self.__nav_buttons['next'] = pygwidgets.TextButton(
            self.__window, (380, 605), "Next"
        )
        
        self.__display_widgets.extend(self.__nav_buttons.values())
    
    def get_display_widgets(self) -> list:
        """Getter for display widgets"""
        return self.__display_widgets
    
    def get_nav_buttons(self) -> Dict[str, Any]:
        """Getter for navigation buttons"""
        return self.__nav_buttons
    
    def update_patient_display(self, person: Optional[Person], current_index: int, total_count: int):
        """
        Update patient display with current person info.
        Uses optional type annotation for better type safety.
        """
        if not person or total_count == 0:
            self.__patient_text.setValue(
                "No patients registered in the system.\n\nUse the form above to add your first patient."
            )
            self.__indicator_color = self.__colors['text_light']
            self.__counter_label.setValue("No patients registered")
            self.__update_nav_button_states(current_index, total_count)
            return
        
        # use the person's display method (polymorphic behavior)
        info = person.get_display_info()
        
        # add status information
        if person.is_cleared_for_entry():
            info += "STATUS: CLEARED FOR ENTRY\n(Fully vaccinated with no symptoms)"
            self.__indicator_color = self.__colors['success']
        else:
            info += "STATUS: NOT CLEARED\n(Missing vaccines or has symptoms)"
            self.__indicator_color = self.__colors['danger']
        
        self.__patient_text.setValue(info)
        self.__counter_label.setValue(
            f"Viewing Patient {current_index + 1} of {total_count}"
        )
        self.__update_nav_button_states(current_index, total_count)
    
    def __update_nav_button_states(self, current_index: int, total_count: int):
        """
        Update navigation button states with better handling
        """
        if total_count <= 0:
            self.__nav_buttons['prev'].disable()
            self.__nav_buttons['next'].disable()
        else:
            # previous button
            if current_index > 0:
                self.__nav_buttons['prev'].enable()
            else:
                self.__nav_buttons['prev'].disable()
            
            # next button  
            if current_index < total_count - 1:
                self.__nav_buttons['next'].enable()
            else:
                self.__nav_buttons['next'].disable()
    def draw_status_indicator(self):
        """Draw the status indicator circle"""
        pygame.draw.circle(self.__window, self.__indicator_color, self.__indicator_pos, 20)
        pygame.draw.circle(self.__window, self.__colors['card'], self.__indicator_pos, 20, 3)
        
        # add status symbol
        status_font = pygame.font.Font(None, 24)
        if self.__indicator_color == self.__colors['success']:
            status_text = "✓"
        elif self.__indicator_color == self.__colors['danger']:
            status_text = "✗"
        else:
            status_text = "?"
        
        text_surface = status_font.render(status_text, True, self.__colors['card'])
        text_rect = text_surface.get_rect(center=self.__indicator_pos)
        self.__window.blit(text_surface, text_rect)


class EnhancedVaccineGUI:
    """
    Main enhanced GUI class implementing OOP principles.
    Uses composition, encapsulation, and polymorphism.
    """
    
    def __init__(self):
        # composition - use other classes for specific responsibilities
        self.__config = GUIConfiguration()
        self.__manager = VaccineManager()
        self.__report_manager = ReportManager(self.__manager)
        
        # current state - private variables
        self.__current_index = -1
        self.__running = True
        
        # initialize pygame
        pygame.init()
        
        # setup window using configuration
        window_size = self.__config.get_window_size()
        self.__window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(self.__config.get_window_title())
        self.__clock = pygame.time.Clock()
        
        # get colors from configuration
        self.__colors = self.__config.get_colors()
        
        # initialize handler classes (composition)
        self.__form_handler = PatientFormHandler(self.__window, self.__config)
        self.__display_handler = PatientDisplayHandler(self.__window, self.__config)
        self.__dialog_manager = DialogManager(self.__window, self.__colors)
        
        # setup GUI widgets
        self.__setup_main_widgets()
        
        # initial display update
        self.__update_patient_display()
        
        # start the application
        self.__run()
    
    def __setup_main_widgets(self):
        """
        Private method to setup main GUI widgets.
        Separates widget creation from initialization.
        """
        self.__main_widgets = []
        
        card_left = self.__config.get_card_margin()
        card_width = 760
        
        # main header
        header = pygwidgets.DisplayText(
            self.__window, (card_left, 25), "Vaccine Tracker",
            fontSize=28, textColor=self.__colors['primary'], justified='center', width=card_width
        )
        self.__main_widgets.append(header)
        
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
        
        # create action buttons with better layout
        self.__setup_action_buttons()
    
    def __setup_action_buttons(self):
        """
        Private method to setup action buttons.
        Uses keyword arguments for flexible button configuration.
        """
        button_config = {
            'width': 120,
            'height': 30,
            'start_y': 650,
            'margin': 10,
            'total_buttons': 6
        }
        
        # calculate button positions
        window_width = self.__config.get_window_size()[0]
        usable_width = window_width - 2 * button_config['margin']
        total_spacing = usable_width - (button_config['width'] * button_config['total_buttons'])
        spacing = total_spacing // (button_config['total_buttons'] - 1)
        
        # button definitions with their callbacks
        button_defs = [
            ("Individual Report", self.__handle_individual_report),
            ("Vaccine Statistics", self.__handle_vaccine_stats),
            ("Symptom Analysis", self.__handle_symptom_analysis),
            ("Reset Data", self.__handle_reset_data),
            ("Delete All Patients", self.__handle_delete_all),
            ("Exit Application", self.__handle_exit)
        ]
        
        self.__action_buttons = {}
        
        # create buttons using loop for scalability
        for i, (label, callback) in enumerate(button_defs):
            x_pos = button_config['margin'] + i * (button_config['width'] + spacing)
            
            button = pygwidgets.TextButton(
                self.__window, (x_pos, button_config['start_y']), label,
                width=button_config['width'], height=button_config['height']
            )
            
            # store button with callback for event handling
            self.__action_buttons[button] = callback
            self.__main_widgets.append(button)
    
    def __handle_events(self, event):
        """
        Private method for event handling using polymorphic behavior.
        Demonstrates encapsulation of event logic.
        """
        # dialog events take priority
        if self.__dialog_manager.handle_dialog_events(event):
            return
        
        # handle form widget events
        for widget in self.__form_handler.get_form_widgets():
            if hasattr(widget, 'handleEvent') and widget.handleEvent(event):
                return
        
        # handle display widget events (navigation)
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
                
                # check action buttons
                if widget in self.__action_buttons:
                    callback = self.__action_buttons[widget]
                    callback()  # call the associated callback
                    return
    
    def __handle_add_patient(self):
        """
        Private method to handle adding new patient.
        Uses form handler for validation and data extraction.
        """
        try:
            # validate required fields first
            is_valid, error_msg = self.__form_handler.validate_required_fields()
            if not is_valid:
                self.__dialog_manager.show_error_dialog("Validation Error", error_msg)
                return
            
            # get form data
            form_data = self.__form_handler.get_form_data()
            
            # check for duplicate ID
            if self.__manager.get_person_by_id(form_data['id']):
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
            
            # create new person using enhanced class
            person = Person(
                form_data['id'], form_data['first_name'], form_data['last_name'],
                form_data['phone'], form_data['address']
            )
            
            # set medical data using bulk update method (keyword arguments)
            person.update_medical_data(
                vaccines=form_data['vaccines'],
                symptoms=form_data['symptoms']
            )
            
            # add to manager
            if self.__manager.add_person(person):
                self.__current_index = self.__manager.get_person_count() - 1
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
        """Private method to navigate to previous patient"""
        if self.__current_index > 0:
            self.__current_index -= 1
            self.__update_patient_display()
    
    def __navigate_next(self):
        """Private method to navigate to next patient"""
        if self.__current_index < self.__manager.get_person_count() - 1:
            self.__current_index += 1
            self.__update_patient_display()
    
    def __update_patient_display(self):
        """
        Update patient display with better index handling
        """
        current_person = None
        total_count = self.__manager.get_person_count()
        
        # Handle empty system
        if total_count == 0:
            self.__current_index = -1
            self.__display_handler.update_patient_display(None, -1, 0)
            return
        
        # Ensure valid index for non-empty system
        if self.__current_index < 0:
            self.__current_index = 0
        elif self.__current_index >= total_count:
            self.__current_index = total_count - 1
        
        current_person = self.__manager.get_person_by_index(self.__current_index)
        self.__display_handler.update_patient_display(current_person, self.__current_index, total_count)
    
    # Action button handlers using polymorphic report generation
    def __handle_individual_report(self):
        """Handle individual report generation using polymorphism"""
        if self.__manager.get_person_count() == 0:
            self.__dialog_manager.show_info_dialog(
                "No Patients", "No patients in the system.\n\nAdd patients first to generate individual reports."
            )
            return
        
        # get available patient IDs for user reference
        available_ids = [str(p.id) for p in self.__manager.get_people()]
        ids_text = ", ".join(available_ids)
        prompt = f"Enter the patient ID to generate report:\n\nAvailable Patient IDs: {ids_text}"
        
        self.__dialog_manager.show_input_dialog(
            "Individual Patient Report", prompt, self.__process_individual_report
        )
    
    def __process_individual_report(self, id_input: str):
        """
        Process individual report input using polymorphic report generation.
        Callback method for input dialog.
        """
        if id_input is None:  # user cancelled
            return
        
        try:
            if not id_input.strip():
                self.__dialog_manager.show_error_dialog("Invalid Input", "Please enter a patient ID.")
                return
            
            patient_id = int(id_input.strip())
            
            # use polymorphic report generation
            report_content = self.__report_manager.generate_individual_report(
                patient_id, include_header=True, include_stats=True
            )
            
            if "Error" in report_content:
                # extract available IDs for error message
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
        """Handle vaccination statistics using polymorphic report generation"""
        report_content = self.__report_manager.generate_vaccination_stats(
            include_header=True, include_stats=False
        )
        self.__dialog_manager.show_info_dialog("Vaccination Statistics", report_content)
    
    def __handle_symptom_analysis(self):
        """Handle symptom analysis using polymorphic report generation"""
        report_content = self.__report_manager.generate_symptom_analysis(
            include_header=True, include_stats=False
        )
        self.__dialog_manager.show_info_dialog("Symptom Analysis", report_content)
    
    def __handle_reset_data(self):
        """Handle data reset with confirmation dialog"""
        if self.__manager.get_person_count() == 0:
            self.__dialog_manager.show_info_dialog(
                "Reset Data", "No patient data to reset.\n\nThe system is already empty."
            )
            return
        
        confirm_msg = (
            f"Are you sure you want to reset ALL vaccination and symptom data?\n\n"
            f"This will affect {self.__manager.get_person_count()} patient(s):\n"
            f"- All vaccination records will be cleared\n"
            f"- All symptom data will be removed\n"
            f"- Patient information (names, IDs) will be kept\n\n"
            f"This action cannot be undone."
        )
        
        self.__dialog_manager.show_confirmation_dialog(
            "Confirm Data Reset", confirm_msg, self.__process_reset_confirmation
        )
    
    def __process_reset_confirmation(self, confirmed: bool):
        """Process reset confirmation callback"""
        print(f"DEBUG: Reset confirmation received: {confirmed}")
        
        if confirmed:
            try:
                count = self.__manager.reset_all_medical_data()
                self.__update_patient_display()
                self.__form_handler.clear_form()
                
                success_msg = f"All vaccination and symptom data has been cleared for {count} patient(s).\n\nPatient information has been preserved."
                self.__dialog_manager.show_info_dialog("Reset Complete", success_msg)
                
            except Exception as e:
                print(f"DEBUG: Error during reset: {str(e)}")
                self.__dialog_manager.show_error_dialog("Reset Failed", f"Error: {str(e)}")
    
    def __handle_delete_all(self):
        """Handle delete all patients with confirmation"""
        if self.__manager.get_person_count() == 0:
            self.__dialog_manager.show_info_dialog(
                "Delete All Patients", "No patients to delete.\n\nThe system is already empty."
            )
            return
        
        warning_msg = (
            f"WARNING: This will permanently delete ALL {self.__manager.get_person_count()} patient(s)!\n\n"
            f"This includes:\n"
            f"- All patient information\n"
            f"- All vaccination records\n"
            f"- All symptom data\n\n"
            f"This action is PERMANENT and cannot be undone!\n\n"
            f"Are you absolutely sure?"
        )
        
        self.__dialog_manager.show_confirmation_dialog(
            "DANGER: Confirm Complete Deletion", warning_msg, self.__process_delete_confirmation
        )
    
    def __process_delete_confirmation(self, confirmed: bool):
        """Process delete confirmation callback"""
        print(f"DEBUG: Delete confirmation received: {confirmed}")
        
        if confirmed:
            try:
                patient_count = self.__manager.get_person_count()
                self.__manager.clear_all_people()
                self.__current_index = -1
                self.__update_patient_display()
                self.__form_handler.clear_form()
                
                success_msg = f"All {patient_count} patient record(s) have been permanently deleted from the system."
                self.__dialog_manager.show_info_dialog("Deletion Complete", success_msg)
                
            except Exception as e:
                print(f"DEBUG: Error during deletion: {str(e)}")
                self.__dialog_manager.show_error_dialog("Deletion Failed", f"Error: {str(e)}")
    
    def __handle_exit(self):
        """Handle application exit with confirmation"""
        self.__dialog_manager.show_confirmation_dialog(
            "Exit Application",
            "Are you sure you want to close the Vaccine Tracker?\n\nAny unsaved work will be lost.",
            self.__process_exit_confirmation
        )
    
    def __process_exit_confirmation(self, confirmed: bool):
        """Process exit confirmation callback"""
        if confirmed:
            self.__running = False
            pygame.quit()
            sys.exit()
    
    def __draw_modern_card(self, x: int, y: int, width: int, height: int, color: tuple = None):
        """
        Private method to draw modern cards with shadows.
        Uses positional and keyword arguments.
        """
        if color is None:
            color = self.__colors['card']
        
        # shadow effect
        shadow_rect = pygame.Rect(x + 3, y + 3, width, height)
        pygame.draw.rect(self.__window, (0, 0, 0, 30), shadow_rect, border_radius=12)
        
        # main card
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.__window, color, card_rect, border_radius=12)
        pygame.draw.rect(self.__window, self.__colors['border'], card_rect, 2, border_radius=12)
    
    def __draw(self):
        """
        Private method to draw all GUI elements.
        Uses composition to delegate drawing to handlers.
        """
        # clear screen
        self.__window.fill(self.__colors['bg'])
        
        # draw modern cards
        margin = self.__config.get_card_margin()
        self.__draw_modern_card(margin, 10, 760, 85)  # header card
        self.__draw_modern_card(margin, 105, 760, 320, self.__colors['form_bg'])  # form card
        self.__draw_modern_card(margin, 435, 680, 170)  # display card
        self.__draw_modern_card(710, 490, 70, 70)  # status indicator card
        
        # draw all widgets
        for widget in self.__main_widgets:
            widget.draw()
        
        for widget in self.__form_handler.get_form_widgets():
            widget.draw()
        
        for widget in self.__display_handler.get_display_widgets():
            widget.draw()
        
        # draw status indicator using display handler
        self.__display_handler.draw_status_indicator()
        
        # draw dialog if active (polymorphic behavior)
        self.__dialog_manager.draw_dialog()
        
        # update display
        pygame.display.flip()
    
    def __run(self):
        """
        Private method for main application loop.
        Encapsulates the main game loop logic.
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


# Application entry point
if __name__ == "__main__":
    # create and run the enhanced GUI application
    app = EnhancedVaccineGUI()