# dialog_system.py
# Final Vax Project Dialog System
# COP5230 Assignment M5
# 06/21/2025
# Hamza Kurdi

import pygame
import pygwidgets
from typing import Any, Callable
from base_classes import DialogHandler


class InfoDialog(DialogHandler):
    """
    Concrete implementation of DialogHandler for information dialogs.
    Demonstrates polymorphism through different dialog behaviors.
    """
    
    def __init__(self, title: str, message: str):
        super().__init__(title, message)
        self.__widgets = []  # this is a private widget list
        self.__ok_button = None
    
    def create_widgets(self, window, dialog_rect):
        """
        Implementation of abstract method for info dialog widgets.
        Creates simple OK dialog.
        """
        self.__widgets.clear()
        
        # title widget
        title_widget = pygwidgets.DisplayText(
            window, (dialog_rect.x + 25, dialog_rect.y + 25), self._title,
            fontSize=18, textColor=(17, 24, 39)
        )
        self.__widgets.append(title_widget)
        
        # message widget
        message_widget = pygwidgets.DisplayText(
            window, (dialog_rect.x + 25, dialog_rect.y + 60), self._message,
            fontSize=12, textColor=(17, 24, 39), width=450
        )
        self.__widgets.append(message_widget)
        
        # OK button
        self.__ok_button = pygwidgets.TextButton(
            window, (dialog_rect.x + dialog_rect.width - 100, 
                    dialog_rect.y + dialog_rect.height - 50), "OK"
        )
        self.__widgets.append(self.__ok_button)
        
        return self.__widgets
    
    def handle_response(self, clicked_widget):
        """
        Implementation of abstract method for info dialog response.
        """
        if clicked_widget == self.__ok_button:
            self._result = True
            return True  # dialog should close
        return False
    
    def get_widgets(self):
        """Getter for dialog widgets"""
        return self.__widgets


class ErrorDialog(DialogHandler):
    """
    Concrete implementation for error dialogs.
    Shows polymorphism with different styling/behavior.
    """
    
    def __init__(self, title: str, message: str):
        super().__init__(title, message)
        self.__widgets = []
        self.__ok_button = None
    
    def create_widgets(self, window, dialog_rect):
        """
        Implementation of abstract method for error dialog widgets.
        Similar to info but with error styling.
        """
        self.__widgets.clear()
        
        # error title with different color
        title_widget = pygwidgets.DisplayText(
            window, (dialog_rect.x + 25, dialog_rect.y + 25), f"⚠ {self._title}",
            fontSize=18, textColor=(239, 68, 68)  # red color for errors
        )
        self.__widgets.append(title_widget)
        
        # error message
        message_widget = pygwidgets.DisplayText(
            window, (dialog_rect.x + 25, dialog_rect.y + 60), self._message,
            fontSize=12, textColor=(17, 24, 39), width=450
        )
        self.__widgets.append(message_widget)
        
        # OK button
        self.__ok_button = pygwidgets.TextButton(
            window, (dialog_rect.x + dialog_rect.width - 100, 
                    dialog_rect.y + dialog_rect.height - 50), "OK"
        )
        self.__widgets.append(self.__ok_button)
        
        return self.__widgets
    
    def handle_response(self, clicked_widget):
        """
        Implementation of abstract method for error dialog response.
        """
        if clicked_widget == self.__ok_button:
            self._result = True
            return True
        return False
    
    def get_widgets(self):
        """Getter for dialog widgets"""
        return self.__widgets


class ConfirmationDialog(DialogHandler):
    """
    Concrete implementation for yes/no confirmation dialogs.
    Demonstrates different widget creation and response handling.
    """
    
    def __init__(self, title: str, message: str):
        super().__init__(title, message)
        self.__widgets = []
        self.__yes_button = None
        self.__no_button = None
    
    def create_widgets(self, window, dialog_rect):
        """
        Implementation of abstract method for confirmation dialog widgets.
        Creates Yes/No buttons.
        """
        self.__widgets.clear()
        
        # title widget
        title_widget = pygwidgets.DisplayText(
            window, (dialog_rect.x + 25, dialog_rect.y + 25), self._title,
            fontSize=18, textColor=(17, 24, 39)
        )
        self.__widgets.append(title_widget)
        
        # message widget
        message_widget = pygwidgets.DisplayText(
            window, (dialog_rect.x + 25, dialog_rect.y + 60), self._message,
            fontSize=12, textColor=(17, 24, 39), width=450
        )
        self.__widgets.append(message_widget)
        
        # Yes and No buttons
        self.__yes_button = pygwidgets.TextButton(
            window, (dialog_rect.x + dialog_rect.width - 180, 
                    dialog_rect.y + dialog_rect.height - 50), "Yes"
        )
        self.__no_button = pygwidgets.TextButton(
            window, (dialog_rect.x + dialog_rect.width - 90, 
                    dialog_rect.y + dialog_rect.height - 50), "No"
        )
        
        self.__widgets.append(self.__yes_button)
        self.__widgets.append(self.__no_button)
        
        return self.__widgets
    
    def handle_response(self, clicked_widget):
        """
        Implementation of abstract method for confirmation dialog response.
        Returns different results based on button clicked.
        """
        if clicked_widget == self.__yes_button:
            self._result = True
            return True
        elif clicked_widget == self.__no_button:
            self._result = False
            return True
        return False
    
    def get_widgets(self):
        """Getter for dialog widgets"""
        return self.__widgets


class InputDialog(DialogHandler):
    """
    Concrete implementation for text input dialogs.
    Shows polymorphism with input field handling.
    """
    
    def __init__(self, title: str, message: str, default_value: str = ""):
        super().__init__(title, message)
        self.__widgets = []
        self.__input_field = None
        self.__ok_button = None
        self.__cancel_button = None
        self.__default_value = default_value
    
    def create_widgets(self, window, dialog_rect):
        """
        Implementation of abstract method for input dialog widgets.
        Creates input field with OK/Cancel buttons.
        """
        self.__widgets.clear()
        
        # title widget
        title_widget = pygwidgets.DisplayText(
            window, (dialog_rect.x + 25, dialog_rect.y + 25), self._title,
            fontSize=18, textColor=(17, 24, 39)
        )
        self.__widgets.append(title_widget)
        
        # message widget
        message_widget = pygwidgets.DisplayText(
            window, (dialog_rect.x + 25, dialog_rect.y + 60), self._message,
            fontSize=12, textColor=(17, 24, 39), width=450
        )
        self.__widgets.append(message_widget)
        
        # input field
        self.__input_field = pygwidgets.InputText(
            window, (dialog_rect.x + 25, dialog_rect.y + 160), width=300
        )
        if self.__default_value:
            self.__input_field.setValue(self.__default_value)
        self.__widgets.append(self.__input_field)
        
        # OK and Cancel buttons
        self.__ok_button = pygwidgets.TextButton(
            window, (dialog_rect.x + dialog_rect.width - 180, 
                    dialog_rect.y + dialog_rect.height - 50), "OK"
        )
        self.__cancel_button = pygwidgets.TextButton(
            window, (dialog_rect.x + dialog_rect.width - 90, 
                    dialog_rect.y + dialog_rect.height - 50), "Cancel"
        )
        
        self.__widgets.append(self.__ok_button)
        self.__widgets.append(self.__cancel_button)
        
        return self.__widgets
    
    def handle_response(self, clicked_widget):
        """
        Implementation of abstract method for input dialog response.
        Returns input value or None for cancel.
        """
        if clicked_widget == self.__ok_button:
            self._result = self.__input_field.getValue()
            return True
        elif clicked_widget == self.__cancel_button:
            self._result = None
            return True
        return False
    
    def get_widgets(self):
        """Getter for dialog widgets"""
        return self.__widgets
    
    def get_input_value(self) -> str:
        """Get current input field value"""
        return self.__input_field.getValue() if self.__input_field else ""


class DialogManager:
    """
    Manager class for handling dialog lifecycle and polymorphic behavior.
    Demonstrates composition and encapsulation.
    """
    
    def __init__(self, window, colors: dict):
        self.__window = window
        self.__colors = colors
        self.__current_dialog = None  # private current dialog
        self.__dialog_rect = None
        self.__is_dialog_active = False
        
        # dialog dimensions
        self.__dialog_width = 500
        self.__dialog_height = 280
    
    def get_is_active(self) -> bool:
        """Getter for dialog active status"""
        return self.__is_dialog_active
    
    def set_dialog_dimensions(self, width: int, height: int):
        """Setter for dialog dimensions"""
        self.__dialog_width = width
        self.__dialog_height = height
    
    def show_info_dialog(self, title: str, message: str, callback: Callable = None):
        """
        Show information dialog using polymorphism.
        Uses positional and keyword arguments.
        """
        self.__show_dialog(InfoDialog(title, message), callback)
    
    def show_error_dialog(self, title: str, message: str, callback: Callable = None):
        """Show error dialog using polymorphism"""
        self.__show_dialog(ErrorDialog(title, message), callback)
    
    def show_confirmation_dialog(self, title: str, message: str, callback: Callable = None):
        """Show confirmation dialog using polymorphism"""
        self.__show_dialog(ConfirmationDialog(title, message), callback)
    
    def show_input_dialog(self, title: str, message: str, callback: Callable = None, 
                         default_value: str = ""):
        """
        Show input dialog using polymorphism and keyword arguments.
        Demonstrates keyword argument usage.
        """
        dialog = InputDialog(title, message, default_value)
        self.__show_dialog(dialog, callback)
    
    def __show_dialog(self, dialog: DialogHandler, callback: Callable = None):
        """
        Private method to show any dialog type (polymorphic behavior).
        """
        if self.__is_dialog_active:
            # print("Dialog already active, ignoring new dialog request")
            return
        
        self.__current_dialog = dialog
        self.__is_dialog_active = True
        
        # calculate dialog position (centered)
        window_width = 800  # hardcoded for this app
        window_height = 750
        dialog_x = (window_width - self.__dialog_width) // 2
        dialog_y = (window_height - self.__dialog_height) // 2
        
        self.__dialog_rect = pygame.Rect(dialog_x, dialog_y, 
                                       self.__dialog_width, self.__dialog_height)
        
        # create widgets using polymorphic method
        self.__current_dialog.create_widgets(self.__window, self.__dialog_rect)
        self.__current_dialog.set_callback(callback)
    
    def handle_dialog_events(self, event) -> bool:
        """
        Handle events for active dialog using polymorphic response handling.
        Returns True if event was handled by dialog.
        """
        if not self.__is_dialog_active or not self.__current_dialog:
            return False
        
        # get widgets from current dialog (polymorphic)
        widgets = self.__current_dialog.get_widgets()
        
        for widget in widgets:
            if hasattr(widget, 'handleEvent') and widget.handleEvent(event):
                # use polymorphic response handling
                should_close = self.__current_dialog.handle_response(widget)
                
                if should_close:
                    result = self.__current_dialog.get_result()
                    callback = self.__current_dialog._callback
                    
                    # close dialog first
                    self.__close_dialog()
                    
                    # then call callback with result
                    if callback:
                        callback(result)
                
                return True
        
        return False
    
    def draw_dialog(self):
        """
        Draw active dialog with modern styling.
        Uses polymorphic widget drawing.
        """
        if not self.__is_dialog_active or not self.__current_dialog:
            return
        
        # draw semi-transparent overlay
        overlay = pygame.Surface((800, 750))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.__window.blit(overlay, (0, 0))
        
        # draw dialog shadow
        shadow_rect = pygame.Rect(self.__dialog_rect.x + 5, self.__dialog_rect.y + 5,
                                 self.__dialog_rect.width, self.__dialog_rect.height)
        pygame.draw.rect(self.__window, (0, 0, 0, 50), shadow_rect, border_radius=15)
        
        # draw main dialog
        pygame.draw.rect(self.__window, self.__colors['form_bg'], self.__dialog_rect, border_radius=15)
        pygame.draw.rect(self.__window, self.__colors['border'], self.__dialog_rect, 3, border_radius=15)
        
        # draw widgets using polymorphic behavior
        widgets = self.__current_dialog.get_widgets()
        for widget in widgets:
            widget.draw()
    
    def __close_dialog(self):
        """Private method to close current dialog"""
        self.__current_dialog = None
        self.__is_dialog_active = False
        self.__dialog_rect = None
    
    def force_close_dialog(self):
        """Public method to force close dialog (for cleanup)"""
        self.__close_dialog()
    
    def get_current_dialog_type(self) -> str:
        """Get type of current dialog for debugging"""
        if not self.__current_dialog:
            return "None"
        return type(self.__current_dialog).__name__