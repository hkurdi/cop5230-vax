# base_classes.py
# Vax Project Base Classes
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

# So last time I had alot of unused methods that basically just building the skeleton
# for m5. So then, I left some methods as placeholders on purpose to show I understand 
# how abstract classes work and stuff. This gives me a good foundation to build on for the 
# actual implementation. Here's the finished base classes for M5 and hopefully the final project.

from abc import ABC, abstractmethod
from typing import Dict, Any

# ===== INHERITANCE DEMONSTRATED HERE =====
# DataEntity is an abstract base class that will be inherited by concrete classes like Person
# This demonstrates INHERITANCE - subclasses inherit structure and behavior from this base class
class DataEntity(ABC):
    """
    Base class for all the data stuff in the system.
    Makes sure everything has validation and display methods.
    """
    
    def __init__(self, entity_id: int):
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Using protected attribute (_id) to hide internal implementation details
        # Subclasses can access this, but external code should use the property
        self._id = entity_id
    
    @property
    def id(self) -> int:
        """Gets the ID"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Property provides controlled access to private data
        # This encapsulates the internal _id attribute behind a clean interface
        return self._id
    
    # ===== POLYMORPHISM DEMONSTRATED HERE =====
    # These abstract methods will be implemented differently by each subclass
    # This enables polymorphism - same method names, different behaviors
    @abstractmethod
    def validate_data(self) -> bool:
        """
        Each subclass needs to implement thier own validation
        Returns: True if data is good, False if not
        """
        pass
    
    @abstractmethod
    def get_display_info(self) -> str:
        """
        Each class defines how to display it's info
        Returns: string formatted for showing to user
        """
        pass

# ===== INHERITANCE DEMONSTRATED HERE =====
# ReportGenerator is another abstract base class for inheritance hierarchy
# Different report types will inherit from this base class
class ReportGenerator(ABC):
    """
    Base class for making different kinds of reports.
    Uses polymorphism so each report type can work differently.
    """
    
    def __init__(self, data_source):
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Protected attribute encapsulates the data source from external access
        self._data_source = data_source
    
    # ===== POLYMORPHISM DEMONSTRATED HERE =====
    # Abstract methods that will have different implementations in subclasses
    # This is the foundation for polymorphic behavior in report generation
    @abstractmethod
    def generate_content(self) -> str:
        """Each report type generates content differently"""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Each report calculates it's own stats"""
        pass
    
    def format_report(self, title: str = None, include_stats: bool = True) -> str:
        """
        Formats the report nicely for all report types
        ===== POLYMORPHISM DEMONSTRATED HERE =====
        This method calls the abstract methods (generate_content, get_statistics)
        The actual behavior depends on which subclass implements these methods
        This is runtime polymorphism in action!
        """
        report_parts = []
        
        if title:
            report_parts.append(f"=== {title} ===")
            report_parts.append("")  # blank line
        
        # get the main report content - POLYMORPHIC CALL
        # The actual implementation depends on the specific subclass
        content = self.generate_content()
        report_parts.append(content)
        
        if include_stats:
            # Another POLYMORPHIC CALL - behavior varies by subclass
            stats = self.get_statistics()
            if stats:
                report_parts.append("")
                report_parts.append("SUMMARY STATISTICS:")
                for key, value in stats.items():
                    report_parts.append(f"  {key}: {value}")
        
        return '\n'.join(report_parts)

# ===== INHERITANCE DEMONSTRATED HERE =====
# DialogHandler is an abstract base class for different dialog types
# Shows inheritance hierarchy for UI component management
class DialogHandler(ABC):
    """
    Base class for different dialog boxes.
    Shows polymorphism with different dialog behaviours.
    """
    
    def __init__(self, title: str, message: str):
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Protected attributes hide internal dialog state from external code
        # Subclasses can access these, but external code uses properties/methods
        self._title = title
        self._message = message
        self._result = None
        self._callback = None
        
    def set_callback(self, callback):
        """Sets the callback function for this dialog"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Provides controlled way to set the callback while maintaining encapsulation
        self._callback = callback
    
    # ===== ENCAPSULATION DEMONSTRATED HERE =====
    # Properties provide controlled access to encapsulated data
    # External code can read these values but cannot directly modify the private state
    @property
    def title(self) -> str:
        """Gets the dialog title"""
        return self._title
    
    @property
    def message(self) -> str:
        """Gets the dialog message"""
        return self._message
    
    # ===== POLYMORPHISM DEMONSTRATED HERE =====
    # Abstract methods that enable polymorphic behavior in dialog handling
    # Each dialog type (Info, Error, Confirmation, Input) implements these differently
    @abstractmethod
    def create_widgets(self, window, dialog_rect):
        """Each dialog type creates it's own widgets"""
        pass
    
    @abstractmethod
    def handle_response(self, response):
        """Each dialog handles user responses diferently"""
        pass
    
    def get_result(self):
        """Gets the result from the dialog"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Provides controlled access to the internal result state
        return self._result