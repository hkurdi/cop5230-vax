# display_handler.py
# Patient Display Handler Module
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

import pygame
import pygwidgets
from typing import Optional, Dict, Any
from config import GUIConfiguration
from classes.person.person import Person


class PatientDisplayHandler:
    """
    This class handles showing patient information on the screen.
    Keeps the display code seperate from the form handling stuff.
    """
    
    def __init__(self, window, config: GUIConfiguration):
        self.__window = window
        self.__config = config
        self.__colors = config.get_colors()
        
        # display widgets - need to keep track of these
        self.__display_widgets = []
        self.__patient_text = None
        self.__counter_label = None
        self.__nav_buttons = {}
        
        # status indicator circle stuff
        self.__indicator_pos = (720, 530)
        self.__indicator_color = self.__colors['text_light']
        
        self.__setup_display_widgets()
    
    def __setup_display_widgets(self):
        """Sets up all the widgets for displaying patient info"""
        self.__display_widgets.clear()
        self.__nav_buttons.clear()
        
        # patient overview section label
        overview_label = pygwidgets.DisplayText(
            self.__window, (50, 440), "Patient Overview",
            fontSize=16, textColor=self.__colors['text_dark']
        )
        self.__display_widgets.append(overview_label)
        
        # main patient text display area
        self.__patient_text = pygwidgets.DisplayText(
            self.__window, (50, 465),
            "No patients registered in the system.\n\nUse the form above to add your first patient.",
            fontSize=11, textColor=self.__colors['text_dark'], width=600, height=130
        )
        self.__display_widgets.append(self.__patient_text)
        
        # counter label to show which patient we're viewing
        self.__counter_label = pygwidgets.DisplayText(
            self.__window, (20, 75), "No patients registered",
            fontSize=12, textColor=self.__colors['text_dark'], justified='center', width=760
        )
        self.__display_widgets.append(self.__counter_label)
        
        # navigation buttons for going through patients
        self.__nav_buttons['prev'] = pygwidgets.TextButton(
            self.__window, (280, 605), "Previous"
        )
        self.__nav_buttons['next'] = pygwidgets.TextButton(
            self.__window, (380, 605), "Next"
        )
        
        self.__display_widgets.extend(self.__nav_buttons.values())
    
    def get_display_widgets(self) -> list:
        """Returns the list of display widgets"""
        return self.__display_widgets
    
    def get_nav_buttons(self) -> Dict[str, Any]:
        """Returns the navigation button dictionary"""
        return self.__nav_buttons
    
    def __truncate_text(self, text: str, max_length: int = 40) -> str:
        """Cuts off long text so it fits better on screen"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def update_patient_display(self, person: Optional[Person], current_index: int, total_count: int):
        """
        Updates the patient display area with current patient info.
        Handles text overflow and formatting for better readability.
        """
        if not person or total_count == 0:
            self.__patient_text.setValue(
                "No patients registered in the system.\n\nUse the form above to add your first patient."
            )
            self.__indicator_color = self.__colors['text_light']
            self.__counter_label.setValue("No patients registered")
            self.__update_nav_button_states(-1, 0)
            return
        
        try:
            # Get display info with overflow protection to prevent text cutoff
            info = f"PATIENT INFORMATION\n"
            info += f"ID: {person.id}  |  Name: {self.__truncate_text(person.get_first_name(), 15)} {self.__truncate_text(person.get_last_name(), 15)}\n"
            info += f"Phone: {self.__truncate_text(person.get_phone() or 'Not provided', 20)}\n"
            info += f"Address: {self.__truncate_text(person.get_address() or 'Not provided', 35)}\n\n"
            
            info += f"VACCINATION STATUS\n"
            info += f"{'[YES]' if person.get_covid19_vaccine() else '[NO]'} COVID-19 Vaccine\n"
            info += f"{'[YES]' if person.get_influenza_vaccine() else '[NO]'} Influenza Vaccine\n"
            info += f"{'[YES]' if person.get_ebola_vaccine() else '[NO]'} Ebola Vaccine\n\n"
            
            info += f"CURRENT SYMPTOMS\n"
            info += f"{'[YES]' if person.get_fever() else '[NO]'} Fever\n"
            info += f"{'[YES]' if person.get_fatigue() else '[NO]'} Fatigue\n"
            info += f"{'[YES]' if person.get_headache() else '[NO]'} Headache\n\n"
            
            # Add status information with appropriate colors
            if person.is_cleared_for_entry():
                info += "STATUS: ✅ CLEARED FOR ENTRY\n(Fully vaccinated with no symptoms)"
                self.__indicator_color = self.__colors['success']
            else:
                info += "STATUS: ❌ NOT CLEARED\n(Missing vaccines or has symptoms)"
                self.__indicator_color = self.__colors['danger']
            
            self.__patient_text.setValue(info)
            self.__counter_label.setValue(
                f"Viewing Patient {current_index + 1} of {total_count}"
            )
            self.__update_nav_button_states(current_index, total_count)
            
        except Exception as e:
            print(f"DEBUG: Error updating patient display: {str(e)}")
            self.__patient_text.setValue(f"Error displaying patient information")
            self.__indicator_color = self.__colors['danger']
        
    def __update_nav_button_states(self, current_index: int, total_count: int):
        """
        Updates the prev/next buttons based on current position.
        Disables buttons when you can't go any further in that direction.
        """
        if total_count == 0:
            self.__nav_buttons['prev'].disable()
            self.__nav_buttons['next'].disable()
        else:
            # previous button logic
            if current_index > 0:
                self.__nav_buttons['prev'].enable()
            else:
                self.__nav_buttons['prev'].disable()
            
            # next button logic
            if current_index < total_count - 1:
                self.__nav_buttons['next'].enable()
            else:
                self.__nav_buttons['next'].disable()
    
    def draw_status_indicator(self):
        """Draw the status indicator circle with appropriate symbol"""
        pygame.draw.circle(self.__window, self.__indicator_color, self.__indicator_pos, 20)
        pygame.draw.circle(self.__window, self.__colors['card'], self.__indicator_pos, 20, 3)
        
        # add the status symbol inside the circle
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