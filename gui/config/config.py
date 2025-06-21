# config.py
# GUI Configuration Module
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

from typing import Dict

class GUIConfiguration:
    """
    Config class to keep all the GUI settings in one place.
    Makes it easier to change colors and sizes later.
    """
    
    def __init__(self):
        # window settings
        self.__window_width = 800
        self.__window_height = 750
        self.__window_title = "Vaccine Tracker"
        
        # color scheme - keeping these private w/ getters
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
    
    # getter methods for the config values
    def get_window_size(self) -> tuple:
        """Returns window width and height"""
        return (self.__window_width, self.__window_height)
    
    def get_window_title(self) -> str:
        """Returns the window title"""
        return self.__window_title
    
    def get_colors(self) -> Dict[str, tuple]:
        """Returns copy of colors dict"""
        return self.__colors.copy()  # return copy so nothing gets messed up
    
    def get_card_margin(self) -> int:
        """Returns the card margin value"""
        return self.__card_margin
    
    def set_window_title(self, title: str):
        """Changes the window title"""
        self.__window_title = title
    
    def update_color(self, color_name: str, color_value: tuple):
        """Updates a specific color if it exists"""
        if color_name in self.__colors:
            self.__colors[color_name] = color_value