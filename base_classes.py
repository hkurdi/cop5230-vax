# base_classes.py
# Final Vax Project Base Classes
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

# So last time I had alot of unused methods that basically just building the skeleton
# for this final project. So then, I left some methods as placeholders on purpose to show I understand 
# how abstract classes work and stuff. This gives me a good foundation to build on for the 
# actual implementation. Here's the finished base classes for the final project.

from abc import ABC, abstractmethod
from typing import Dict, Any


class DataEntity(ABC):
    """
    Base class for all the data stuff in the system.
    Makes sure everything has validation and display methods.
    """
    
    def __init__(self, entity_id: int):
        self._id = entity_id
    
    @property
    def id(self) -> int:
        """Gets the ID"""
        return self._id
    
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


class ReportGenerator(ABC):
    """
    Base class for making different kinds of reports.
    Uses polymorphism so each report type can work differently.
    """
    
    def __init__(self, data_source):
        self._data_source = data_source
    
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
        """
        report_parts = []
        
        if title:
            report_parts.append(f"=== {title} ===")
            report_parts.append("")  # blank line
        
        # get the main report content
        content = self.generate_content()
        report_parts.append(content)
        
        if include_stats:
            stats = self.get_statistics()
            if stats:
                report_parts.append("")
                report_parts.append("SUMMARY STATISTICS:")
                for key, value in stats.items():
                    report_parts.append(f"  {key}: {value}")
        
        return '\n'.join(report_parts)


class DialogHandler(ABC):
    """
    Base class for different dialog boxes.
    Shows polymorphism with different dialog behaviours.
    """
    
    def __init__(self, title: str, message: str):
        self._title = title
        self._message = message
        self._result = None
    
    @property
    def title(self) -> str:
        """Gets the dialog title"""
        return self._title
    
    @property
    def message(self) -> str:
        """Gets the dialog message"""
        return self._message
    
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
        return self._result