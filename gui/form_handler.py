# form_handler.py
# Patient Form Handler Module
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

import pygwidgets
from typing import Dict, Any
from config import GUIConfiguration


class PatientFormHandler:
    """
    This class handles all the patient form functionality.
    Easier to manage when its separated into its own class like this.
    """
    
    def __init__(self, window, config: GUIConfiguration):
        self.__window = window
        self.__config = config
        self.__colors = config.get_colors()
        
        # form widgets - keeping track of everything we create
        self.__form_widgets = []
        self.__input_fields = {}
        self.__checkboxes = {}
        
        self.__setup_form_widgets()
    
    def __setup_form_widgets(self):
        """
        Set up all the form widgets and input fields.
        Had to make this private to keep things organized properly.
        """
        # clear existing widgets first
        self.__form_widgets.clear()
        self.__input_fields.clear()
        self.__checkboxes.clear()
        
        form_start_y = 110
        col1_x = 70
        col2_x = 420
        entry_width = 180
        
        # form header text
        header = pygwidgets.DisplayText(
            self.__window, (50, form_start_y), "Add New Patient",
            fontSize=16, textColor=self.__colors['text_dark']
        )
        self.__form_widgets.append(header)
        
        # create input fields with their labels
        self.__create_input_field("id", "Patient ID *", col1_x, form_start_y + 35, entry_width)
        self.__create_input_field("fname", "First Name *", col1_x, form_start_y + 80, entry_width)
        self.__create_input_field("lname", "Last Name *", col1_x, form_start_y + 125, entry_width)
        self.__create_input_field("phone", "Phone Number", col2_x, form_start_y + 35, entry_width)
        self.__create_input_field("addr", "Address", col2_x, form_start_y + 80, int(entry_width * 1.2))
        
        # vaccine checkboxes section
        vaccine_y = 290
        self.__create_section_header("Vaccination Status", 70, vaccine_y)
        self.__create_checkbox("covid", "COVID-19 Vaccine", 85, vaccine_y + 25)
        self.__create_checkbox("influenza", "Influenza Vaccine", 85, vaccine_y + 50)
        self.__create_checkbox("ebola", "Ebola Vaccine", 85, vaccine_y + 75)
        
        # symptom checkboxes section
        self.__create_section_header("Current Symptoms", 420, vaccine_y)
        self.__create_checkbox("fever", "Fever", 435, vaccine_y + 25)
        self.__create_checkbox("fatigue", "Fatigue", 435, vaccine_y + 50)
        self.__create_checkbox("headache", "Headache", 435, vaccine_y + 75)
    
    def __create_input_field(self, field_id: str, label: str, x: int, y: int, width: int):
        """
        Helper method to create input fields with their labels.
        Takes position and size parameters to make positioning easier.
        """
        # create the label widget
        label_widget = pygwidgets.DisplayText(
            self.__window, (x, y), label, fontSize=11, textColor=self.__colors['text_dark']
        )
        self.__form_widgets.append(label_widget)
        
        # create the input field widget
        input_widget = pygwidgets.InputText(
            self.__window, (x, y + 15), width=width
        )
        self.__form_widgets.append(input_widget)
        self.__input_fields[field_id] = input_widget
    
    def __create_checkbox(self, checkbox_id: str, label: str, x: int, y: int):
        """Helper method to create checkboxes with labels"""
        checkbox = pygwidgets.TextCheckBox(
            self.__window, (x, y), label, value=False
        )
        self.__form_widgets.append(checkbox)
        self.__checkboxes[checkbox_id] = checkbox
    
    def __create_section_header(self, text: str, x: int, y: int):
        """Creates section headers for different parts of the form"""
        header = pygwidgets.DisplayText(
            self.__window, (x, y), text, fontSize=14, textColor=self.__colors['text_dark']
        )
        self.__form_widgets.append(header)
    
    def get_form_widgets(self) -> list:
        """Returns list of all form widgets for drawing"""
        return self.__form_widgets
    
    def get_form_data(self) -> Dict[str, Any]:
        """
        Gets all the data from the form fields and returns it as a dictionary.
        Returns a dict with all the values or raises an error if something goes wrong.
        """
        try:
            # get the basic patient info
            data = {
                'id': int(self.__input_fields['id'].getValue().strip()),
                'first_name': self.__input_fields['fname'].getValue().strip(),
                'last_name': self.__input_fields['lname'].getValue().strip(),
                'phone': self.__input_fields['phone'].getValue().strip(),
                'address': self.__input_fields['addr'].getValue().strip(),
            }
            
            # get vaccine status from checkboxes
            data['vaccines'] = {
                'covid19': self.__checkboxes['covid'].getValue(),
                'influenza': self.__checkboxes['influenza'].getValue(),
                'ebola': self.__checkboxes['ebola'].getValue()
            }
            
            # get current symptoms from checkboxes
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
        """Clear all form fields back to their default values"""
        # clear all input fields
        for field in self.__input_fields.values():
            field.setValue("")
        
        # uncheck all checkboxes
        for checkbox in self.__checkboxes.values():
            checkbox.setValue(False)
    
    def validate_required_fields(self) -> tuple:
        """
        Validates the required fields and makes sure everything looks good.
        Returns tuple with (is_valid, error_message) for easy checking.
        """
        # check the required fields first
        if not self.__input_fields['id'].getValue().strip():
            return (False, "Patient ID is required to continue.")
        
        if not self.__input_fields['fname'].getValue().strip():
            return (False, "First name is required to continue.")
        
        if not self.__input_fields['lname'].getValue().strip():
            return (False, "Last name is required to continue.")
        
        # validate the ID is a proper number
        try:
            patient_id = int(self.__input_fields['id'].getValue().strip())
            if patient_id <= 0:
                return (False, "Patient ID must be a positive number.")
            if patient_id > 999:  # reasonable upper limit for this project
                return (False, "Patient ID must be 999 or less.")
        except ValueError:
            return (False, "Patient ID must be a valid number.")
        
        # check name lengths so they don't get too long
        fname = self.__input_fields['fname'].getValue().strip()
        lname = self.__input_fields['lname'].getValue().strip()
        
        if len(fname) > 30:
            return (False, "First name must be 30 characters or less.")
        if len(lname) > 30:
            return (False, "Last name must be 30 characters or less.")
        
        # address length validation
        address = self.__input_fields['addr'].getValue().strip()
        if len(address) > 100:
            return (False, "Address must be 100 characters or less.")
        
        # phone number validation (only if they entered something)
        phone = self.__input_fields['phone'].getValue().strip()
        if phone:  # only validate if not empty
            # remove common separators to count digits
            clean_phone = ''.join(c for c in phone if c.isdigit())
            if len(clean_phone) < 10:
                return (False, "Phone number must have at least 10 digits.")
            if len(phone) > 20:  # original length including formatting chars
                return (False, "Phone number must be 20 characters or less.")
        
        return (True, "")