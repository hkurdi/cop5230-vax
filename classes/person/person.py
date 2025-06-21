# person.py
# Final Vax Project Person classes - CLEANED VERSION
# COP5230 Assignment M5
# 06/21/2025
# Hamza Kurdi

from typing import Dict
from classes.base_classes import DataEntity

# ===== INHERITANCE DEMONSTRATED HERE =====
# Person class inherits from DataEntity abstract base class
# This demonstrates inheritance - Person gets all the structure and behavior from DataEntity
# and must implement the abstract methods (validate_data, get_display_info)
class Person(DataEntity):
    """
    Person class extending DataEntity with vaccination and symptom tracking.
    Uses private attributes with standardized getter methods for better encapsulation.
    """
    
    def __init__(self, person_id: int, first_name: str, last_name: str, 
                 phone: str = "", address: str = ""):
        # ===== INHERITANCE DEMONSTRATED HERE =====
        # Calling parent class constructor using super()
        # This inherits the initialization behavior from DataEntity
        super().__init__(person_id)
        
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Using private attributes (double underscore prefix) to hide internal data
        # This is data hiding - external code cannot directly access these attributes
        # Personal info (private with validation) - strip whitespace just in case
        self.__first_name = first_name.strip()
        self.__last_name = last_name.strip()
        self.__phone = phone.strip()
        self.__address = address.strip()
        
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Medical data stored as private attributes - completely hidden from outside access
        # External code must use getter/setter methods to access this data
        # Medical data - all start False by default
        self.__covid19_vaccine = False
        self.__influenza_vaccine = False
        self.__ebola_vaccine = False
        self.__fever = False
        self.__fatigue = False
        self.__headache = False
    
    # ===== ENCAPSULATION DEMONSTRATED HERE =====
    # Getter methods provide controlled read-only access to private data
    # This encapsulates the internal state and prevents direct manipulation
    # Standardized getter methods (removing redundant properties)
    def get_first_name(self) -> str:
        return self.__first_name
    
    def get_last_name(self) -> str:
        return self.__last_name
    
    def get_phone(self) -> str:
        return self.__phone
    
    def get_address(self) -> str:
        return self.__address
    
    # ===== ENCAPSULATION DEMONSTRATED HERE =====
    # Getter/setter pairs provide controlled access to private medical data
    # This encapsulates the vaccine status while allowing controlled modification
    # Vaccine getters/setters - pretty straightforward
    def get_covid19_vaccine(self) -> bool:
        return self.__covid19_vaccine
    
    def set_covid19_vaccine(self, value: bool):
        self.__covid19_vaccine = value
    
    def get_influenza_vaccine(self) -> bool:
        return self.__influenza_vaccine
    
    def set_influenza_vaccine(self, value: bool):
        self.__influenza_vaccine = value
    
    def get_ebola_vaccine(self) -> bool:
        return self.__ebola_vaccine
    
    def set_ebola_vaccine(self, value: bool):
        self.__ebola_vaccine = value
    
    # ===== ENCAPSULATION DEMONSTRATED HERE =====
    # More getter/setter pairs for symptom data encapsulation
    # Symptom getters/setters - same pattern as vaccines
    def get_fever(self) -> bool:
        return self.__fever
    
    def set_fever(self, value: bool):
        self.__fever = value
    
    def get_fatigue(self) -> bool:
        return self.__fatigue
    
    def set_fatigue(self, value: bool):
        self.__fatigue = value
    
    def get_headache(self) -> bool:
        return self.__headache
    
    def set_headache(self, value: bool):
        self.__headache = value
    
    # ===== ENCAPSULATION DEMONSTRATED HERE =====
    # Public methods that operate on private data provide a clean interface
    # The internal implementation is hidden, only the functionality is exposed
    # Utility methods - helpful for statistics
    def get_vaccine_count(self) -> int:
        """Count of vaccines recieved"""
        return sum([self.__covid19_vaccine, self.__influenza_vaccine, self.__ebola_vaccine])
    
    def get_symptom_count(self) -> int:
        """Count of current symptoms - usefull for triage"""
        return sum([self.__fever, self.__fatigue, self.__headache])
    
    # ===== INHERITANCE & POLYMORPHISM DEMONSTRATED HERE =====
    # Implementation of abstract method from DataEntity base class
    # This is polymorphism - different classes implement validate_data differently
    def validate_data(self) -> bool:
        """Validate required fields are present - basic data integrity check"""
        return bool(self.__first_name and self.__last_name and self._id > 0)
    
    # ===== INHERITANCE & POLYMORPHISM DEMONSTRATED HERE =====
    # Implementation of abstract method from DataEntity base class
    # This is polymorphism - each DataEntity subclass displays info differently
    def get_display_info(self) -> str:
        """Formatted display string for patient information - makes nice output"""
        info_parts = [
            f"PATIENT INFORMATION",
            f"ID: {self._id}  |  Name: {self.__first_name} {self.__last_name}",
            f"Phone: {self.__phone or 'Not provided'}",
            f"Address: {self.__address or 'Not provided'}",
            "",
            f"VACCINATION STATUS",
            f"{'[YES]' if self.__covid19_vaccine else '[NO]'} COVID-19 Vaccine",
            f"{'[YES]' if self.__influenza_vaccine else '[NO]'} Influenza Vaccine", 
            f"{'[YES]' if self.__ebola_vaccine else '[NO]'} Ebola Vaccine",
            "",
            f"CURRENT SYMPTOMS",
            f"{'[YES]' if self.__fever else '[NO]'} Fever",
            f"{'[YES]' if self.__fatigue else '[NO]'} Fatigue",
            f"{'[YES]' if self.__headache else '[NO]'} Headache",
            ""
        ]
        return '\n'.join(info_parts)
    
    def is_cleared_for_entry(self) -> bool:
        """Check if person meets entry requirements (all vaccines, no symptoms) - main buisness logic"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # This method accesses private attributes to perform business logic
        # The complex logic is encapsulated in a simple method interface
        fully_vaccinated = all([self.__covid19_vaccine, self.__influenza_vaccine, self.__ebola_vaccine])
        has_symptoms = any([self.__fever, self.__fatigue, self.__headache])
        return fully_vaccinated and not has_symptoms
    
    def reset_data(self):
        """Reset all medical data to defaults - good for testing"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Internal method that modifies private data in a controlled way
        self.__covid19_vaccine = self.__influenza_vaccine = self.__ebola_vaccine = False
        self.__fever = self.__fatigue = self.__headache = False
    
    def update_medical_data(self, vaccines: Dict[str, bool] = None, symptoms: Dict[str, bool] = None):
        """Bulk update medical data from dictionaries - convienent for batch operations"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Provides a controlled interface for bulk updates of private data
        # External code can't directly modify private attributes, must use this method
        if vaccines:
            self.__covid19_vaccine = vaccines.get('covid19', self.__covid19_vaccine)
            self.__influenza_vaccine = vaccines.get('influenza', self.__influenza_vaccine)
            self.__ebola_vaccine = vaccines.get('ebola', self.__ebola_vaccine)
        
        if symptoms:
            self.__fever = symptoms.get('fever', self.__fever)
            self.__fatigue = symptoms.get('fatigue', self.__fatigue)
            self.__headache = symptoms.get('headache', self.__headache)