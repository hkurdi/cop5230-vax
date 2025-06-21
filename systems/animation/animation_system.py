# animation_system.py
# Timer and Animation System for Vaccine Tracker
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

import pygame
from typing import Callable
from classes.base_classes import DataEntity

# ===== INHERITANCE DEMONSTRATED HERE =====
# AnimatedElement inherits from DataEntity to show we can extend our base classes
# This gives us consistent validation and display methods across all system elements
class AnimatedElement(DataEntity):
    """
    Base class for anything that needs animation in the system.
    Extends DataEntity to keep things consistent with our existing architecture.
    """
    
    def __init__(self, element_id: int, animation_speed: float = 1.0):
        # ===== INHERITANCE DEMONSTRATED HERE =====
        # Calling parent constructor from DataEntity
        super().__init__(element_id)
        
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Private attributes to hide animation state from external code
        self.__animation_speed = animation_speed
        self.__is_animating = False
        self.__current_frame = 0
    
    # ===== ENCAPSULATION DEMONSTRATED HERE =====
    # Getter methods provide controlled access to private animation data
    def get_animation_speed(self) -> float:
        """Gets the animation speed"""
        return self.__animation_speed
    
    def set_animation_speed(self, speed: float):
        """Sets the animation speed"""
        self.__animation_speed = speed
    
    def is_animating(self) -> bool:
        """Checks if currently animating"""
        return self.__is_animating
    
    def start_animation(self):
        """Starts the animation"""
        self.__is_animating = True
        self.__current_frame = 0
    
    def stop_animation(self):
        """Stops the animation"""
        self.__is_animating = False
    
    # ===== INHERITANCE & POLYMORPHISM DEMONSTRATED HERE =====
    # Implementation of abstract methods from DataEntity base class
    def validate_data(self) -> bool:
        """Basic validation for animated elements"""
        return self._id > 0 and self.__animation_speed > 0
    
    def get_display_info(self) -> str:
        """Display info for animated elements"""
        return f"AnimatedElement ID: {self._id}, Speed: {self.__animation_speed}, Active: {self.__is_animating}"


class SimpleTimer:
    """
    Basic timer class for handling timed events.
    Keeping this straightforward - just need start/stop and checking if time's up.
    """
    
    def __init__(self, duration_seconds: float, callback_function: Callable = None):
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Private attributes encapsulate timer implementation details
        self.__duration_ms = int(duration_seconds * 1000)  # convret to ms
        self.__callback = callback_function
        self.__start_time = 0
        self.__is_running = False
    
    def start(self):
        """Start the timer"""
        self.__start_time = pygame.time.get_ticks()
        self.__is_running = True
    
    def stop(self):
        """Stop the timer"""
        self.__is_running = False
    
    def update(self) -> bool:
        """
        Check if timer finished and call callback if needed.
        Returns True if timer completed this frame.
        """
        if not self.__is_running:
            return False
        
        current_time = pygame.time.get_ticks()
        if current_time - self.__start_time >= self.__duration_ms:
            self.__is_running = False
            
            # call the callback function if we have one
            if self.__callback:
                self.__callback()
            
            return True
        
        return False
    
    def get_time_left(self) -> float:
        """Get remaining time in seconds"""
        if not self.__is_running:
            return 0.0
        
        elapsed = pygame.time.get_ticks() - self.__start_time
        remaining_ms = max(0, self.__duration_ms - elapsed)
        return remaining_ms / 1000.0


# ===== INHERITANCE DEMONSTRATED HERE =====
# StatusAnimation inherits from AnimatedElement 
# This shows inheritance hierarchy - AnimatedElement -> DataEntity
class StatusAnimation(AnimatedElement):
    """
    Animation for the status indicator circle.
    Makes it pulse when someone gets added or when there's an error.
    ===== INHERITANCE DEMONSTRATED HERE =====
    Inherits from AnimatedElement which inherits from DataEntity
    This shows multi-level inheritance in action
    """
    
    def __init__(self, center_position: tuple, base_radius: int = 20):
        # ===== INHERITANCE DEMONSTRATED HERE =====
        # Call parent constructor with animation speed
        super().__init__(1, 2.0)  # ID=1, medium animation speed
        
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Private attributes hide internal animation calculations
        self.__center_pos = center_position
        self.__base_radius = base_radius
        self.__pulse_amount = 0.0
        self.__pulse_direction = 1  # 1 for growing, -1 for shrinking
    
    def update_animation(self):
        """Update the pulsing animation"""
        if not self.is_animating():
            return
        
        # simple pulse calculation - grows and shrinks
        self.__pulse_amount += self.get_animation_speed() * self.__pulse_direction * 0.02
        
        # reverse direction when we hit the limits
        if self.__pulse_amount >= 0.3:
            self.__pulse_direction = -1
        elif self.__pulse_amount <= 0.0:
            self.__pulse_direction = 1
            self.__pulse_amount = 0.0
    
    def draw_animated_circle(self, window, color: tuple, status_text: str = ""):
        """Draw the animated status circle"""
        # calculate current radius with pulse effect
        current_radius = int(self.__base_radius * (1.0 + self.__pulse_amount))
        
        # draw the pulsing circle
        pygame.draw.circle(window, color, self.__center_pos, current_radius)
        pygame.draw.circle(window, (255, 255, 255), self.__center_pos, current_radius, 3)
        
        # draw status text if provided
        if status_text:
            font = pygame.font.Font(None, 24)
            text_surface = font.render(status_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.__center_pos)
            window.blit(text_surface, text_rect)
    
    # ===== INHERITANCE & POLYMORPHISM DEMONSTRATED HERE =====
    # Override parent's display method with animation-specific info
    def get_display_info(self) -> str:
        """Override to show status animation specific info"""
        base_info = super().get_display_info()
        return f"{base_info}, Pulse: {self.__pulse_amount:.2f}, Radius: {self.__base_radius}"


class MessageNotification:
    """
    Simple notification system for showing temporary messages.
    Nothing too fancy - just slide in, show for a bit, then fade out.
    """
    
    def __init__(self, message: str, duration_seconds: float = 2.5, **position_options):
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Private attributes manage notification state
        self.__message = message
        self.__duration_timer = SimpleTimer(duration_seconds, self.__on_expired)
        self.__alpha = 255
        self.__slide_offset = 200  # start off-screen
        self.__is_active = False
        self.__position = position_options.get('position', (550, 80))
        self.__background_color = position_options.get('bg_color', (59, 130, 246))
    
    def show(self):
        """Show the notification"""
        self.__is_active = True
        self.__duration_timer.start()
    
    def __on_expired(self):
        """Private callback when timer expires"""
        self.__is_active = False
    
    def update(self):
        """Update notification animation and timer"""
        if not self.__is_active:
            return
        
        # update the timer
        self.__duration_timer.update()
        
        # animate slide-in effect
        if self.__slide_offset > 0:
            self.__slide_offset -= 6  # slide speed
            if self.__slide_offset < 0:
                self.__slide_offset = 0
        
        # fade out in the last half second
        time_left = self.__duration_timer.get_time_left()
        if time_left < 0.5:
            self.__alpha = int(255 * (time_left / 0.5))
    
    def draw(self, window):
        """Draw the notification if active"""
        if not self.__is_active:
            return
        
        # calculate final position with slide animation
        final_x = self.__position[0] - self.__slide_offset
        final_pos = (final_x, self.__position[1])
        
        # create notification surface
        notification_rect = pygame.Rect(final_pos[0], final_pos[1], 160, 40)
        
        # draw background with current alpha
        temp_surface = pygame.Surface((160, 40))
        temp_surface.set_alpha(self.__alpha)
        temp_surface.fill(self.__background_color)
        pygame.draw.rect(temp_surface, self.__background_color, (0, 0, 160, 40), border_radius=8)
        
        # draw text
        font = pygame.font.Font(None, 20)
        text_surface = font.render(self.__message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(80, 20))
        temp_surface.blit(text_surface, text_rect)
        
        # blit to main window
        window.blit(temp_surface, final_pos)
    
    def is_active(self) -> bool:
        """Check if notification is currently active"""
        return self.__is_active


class AnimationManager:
    """
    Manages all the animations and timers for the GUI.
    Keeps everything organized in one place so the main GUI doesn't get cluttered.
    """
    
    def __init__(self, window, colors: dict):
        self.__window = window
        self.__colors = colors
        
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Private collections to manage animation components
        self.__status_animation = StatusAnimation((720, 530))
        self.__active_notifications = []
        self.__auto_pulse_timer = SimpleTimer(30.0, self.__trigger_auto_pulse)
        
        # start the auto-pulse timer to occasionally animate the status indicator
        self.__auto_pulse_timer.start()
    
    def __trigger_auto_pulse(self):
        """Private method to trigger periodic status pulse"""
        # make the status indicator pulse every 30 seconds just for visual interest
        if not self.__status_animation.is_animating():
            self.__pulse_status_briefly()
        
        # restart the timer for next pulse
        self.__auto_pulse_timer.start()
    
    def pulse_status_briefly(self):
        """Public method to pulse status indicator (for success/error feedback)"""
        self.__pulse_status_briefly()
    
    def __pulse_status_briefly(self):
        """Private implementation of status pulsing"""
        self.__status_animation.start_animation()
        
        # set a timer to stop the animation after 2 seconds
        stop_timer = SimpleTimer(2.0, self.__status_animation.stop_animation)
        stop_timer.start()
    
    def show_notification(self, message: str, notification_type: str = "info"):
        """
        Show a notification with automatic cleanup.
        """
        # determine colors based on type
        if notification_type == "success":
            bg_color = self.__colors.get('success', (34, 197, 94))
        elif notification_type == "error":
            bg_color = self.__colors.get('danger', (239, 68, 68))
        else:
            bg_color = self.__colors.get('primary', (59, 130, 246))
        
        # create notification with keyword arguments
        notification = MessageNotification(
            message, 
            duration_seconds=2.5,
            position=(550, 80 + len(self.__active_notifications) * 50),
            bg_color=bg_color
        )
        
        notification.show()
        self.__active_notifications.append(notification)
    
    def update_all_animations(self):
        """Update all active animations and timers"""
        # update status animation
        self.__status_animation.update_animation()
        
        # update auto-pulse timer
        self.__auto_pulse_timer.update()
        
        # update notifications and remove expired ones
        self.__active_notifications = [
            notification for notification in self.__active_notifications
            if self.__update_and_check_notification(notification)
        ]
    
    def __update_and_check_notification(self, notification: MessageNotification) -> bool:
        """Private helper to update notification and check if still active"""
        notification.update()
        return notification.is_active()
    
    def draw_all_animations(self, status_color: tuple, status_text: str = ""):
        """
        Draw all active animations.
        """
        # draw animated status indicator
        self.__status_animation.draw_animated_circle(self.__window, status_color, status_text)
        
        # draw all active notifications
        for notification in self.__active_notifications:
            notification.draw(self.__window)
    
    def cleanup_all(self):
        """Clean up all animations and timers"""
        self.__status_animation.stop_animation()
        self.__auto_pulse_timer.stop()
        self.__active_notifications.clear()
