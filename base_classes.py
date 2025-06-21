# base_classes.py
# Abstract Base Classes for Vaccine Tracker
# COP5230 Assignment 2 M4 - Enhanced OOP Version
# 06/14/2025
# Hamza Kurdi

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class DataEntity(ABC):
    """
    Abstract base class for all data entities in the system.
    Enforces common interface for data validation and display.
    """
    
    def __init__(self, entity_id: int):
        self._id = entity_id  # thsi is a explicit private variable
        self._created_timestamp = None
        self._modified_timestamp = None
    
    @property
    def id(self) -> int:
        """Getter for entity ID"""
        return self._id
    
    @abstractmethod
    def validate_data(self) -> bool:
        """
        Abstract method - each entity must implement its own validation logic
        Returns: bool indicating if data is valid
        """
        pass
    
    @abstractmethod
    def get_display_info(self) -> str:
        """
        Abstract method - each entity must define how it displays info
        Returns: formatted string for display
        """
        pass
    
    def reset_entity(self):
        """Base reset functionality - can be overridden"""
        self._modified_timestamp = None


class ReportGenerator(ABC):
    """
    Abstract base class for different types of reports.
    Implements polymorphism through different report types.
    """
    
    def __init__(self, data_source):
        self._data_source = data_source
        self._report_title = ""
    
    @abstractmethod
    def generate_content(self) -> str:
        """Abstract method - each report type implements different content generation"""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Abstract method - each report provides different statistics"""
        pass
    
    def format_report(self, title: str = None, **kwargs) -> str:
        """
        Common report formatting with keyword arguments
        Uses keyword args for flexible formatting options
        """
        # keyword argument handling
        include_header = kwargs.get('include_header', True)
        include_stats = kwargs.get('include_stats', True)
        separator = kwargs.get('separator', '\n')
        
        report_parts = []
        
        if include_header and (title or self._report_title):
            report_parts.append(f"=== {title or self._report_title} ===")
            report_parts.append("")  # blank line
        
        # get the main content
        content = self.generate_content()
        report_parts.append(content)
        
        if include_stats:
            stats = self.get_statistics()
            if stats:
                report_parts.append("")
                report_parts.append("SUMMARY STATISTICS:")
                for key, value in stats.items():
                    report_parts.append(f"  {key}: {value}")
        
        return separator.join(report_parts)


class DialogHandler(ABC):
    """
    Abstract base class for different dialog types.
    Demonstrates polymorphism through different dialog behaviors.
    """
    
    def __init__(self, title: str, message: str):
        self._title = title
        self._message = message
        self._result = None
        self._callback = None
    
    @property
    def title(self) -> str:
        """Getter for dialog title"""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """Setter for dialog title"""
        self._title = value
    
    @property
    def message(self) -> str:
        """Getter for dialog message"""
        return self._message
    
    @message.setter
    def message(self, value: str):
        """Setter for dialog message"""
        self._message = value
    
    @abstractmethod
    def create_widgets(self, window, dialog_rect):
        """Abstract method - each dialog type creates different widgets"""
        pass
    
    @abstractmethod
    def handle_response(self, response):
        """Abstract method - each dialog handles responses differently"""
        pass
    
    def set_callback(self, callback):
        """Setter for callback function"""
        self._callback = callback
    
    def get_result(self):
        """Getter for dialog result"""
        return self._result


class DataValidator:
    """
    Utility class for common validation operations.
    Supports the modularity requirement.
    """
    
    @staticmethod
    def validate_id(entity_id: int, existing_ids: List[int] = None) -> bool:
        """
        Validates entity ID with optional duplicate checking
        Uses positional and keyword arguments
        """
        # basic validation
        if not isinstance(entity_id, int) or entity_id <= 0:
            return False
        
        # check for duplicates if list provided
        if existing_ids and entity_id in existing_ids:
            return False
        
        return True
    
    @staticmethod
    def validate_name(name: str, min_length: int = 1, max_length: int = 50) -> bool:
        """
        Validates name fields with keyword arguments for flexibility
        """
        if not isinstance(name, str):
            return False
        
        name = name.strip()
        return min_length <= len(name) <= max_length
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Basic phone validation - allows empty or valid formats"""
        if not phone or not phone.strip():
            return True  # optional field
        
        # remove common separators for validation
        cleaned = ''.join(c for c in phone if c.isdigit())
        return 10 <= len(cleaned) <= 15  # reasonable phone length range