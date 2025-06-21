# person.py
# Final Vax Project Person and VaccineManager classes
# COP5230 Assignment M5
# 06/21/2025
# Hamza Kurdi

from typing import List, Optional, Dict, Any
from base_classes import DataEntity


class Person(DataEntity):
    """
    Enhanced Person class inheriting from DataEntity ABC.
    Implements encapsulation with private variables and properties.
    """
    
    def __init__(self, person_id: int, first_name: str, last_name: str, 
                 phone: str = "", address: str = ""):
        """Initialize person with positional and keyword arguments"""
        super().__init__(person_id)
        
        # private instance variables
        self.__first_name = first_name.strip()
        self.__last_name = last_name.strip()
        self.__phone = phone.strip()
        self.__address = address.strip()
        
        # private vaccine status variables
        self.__covid19_vaccine = False
        self.__influenza_vaccine = False
        self.__ebola_vaccine = False
        
        # private symptom variables  
        self.__fever = False
        self.__fatigue = False
        self.__headache = False
    
    # Properties for accessing private variables
    @property
    def first(self) -> str:
        return self.__first_name
    
    @property
    def last(self) -> str:
        return self.__last_name
    
    @property
    def phone(self) -> str:
        return self.__phone
    
    @property
    def addr(self) -> str:
        return self.__address
    
    @property
    def covid19_vaccine(self) -> bool:
        return self.__covid19_vaccine
    
    @covid19_vaccine.setter
    def covid19_vaccine(self, value: bool):
        self.__covid19_vaccine = value
    
    @property
    def influenza_vaccine(self) -> bool:
        return self.__influenza_vaccine
    
    @influenza_vaccine.setter
    def influenza_vaccine(self, value: bool):
        self.__influenza_vaccine = value
    
    @property
    def ebola_vaccine(self) -> bool:
        return self.__ebola_vaccine
    
    @ebola_vaccine.setter
    def ebola_vaccine(self, value: bool):
        self.__ebola_vaccine = value
    
    @property
    def fever(self) -> bool:
        return self.__fever
    
    @fever.setter
    def fever(self, value: bool):
        self.__fever = value
    
    @property
    def fatigue(self) -> bool:
        return self.__fatigue
    
    @fatigue.setter
    def fatigue(self, value: bool):
        self.__fatigue = value
    
    @property
    def headache(self) -> bool:
        return self.__headache
    
    @headache.setter
    def headache(self, value: bool):
        self.__headache = value
    
    def validate_data(self) -> bool:
        """
        Implementation of abstract method from DataEntity.
        Validates person data completeness.
        """
        # required fields validation
        if not self.__first_name or not self.__last_name:
            return False
        
        # id validation (inherited from parent)
        if self._id <= 0:
            return False
        
        return True
    
    def get_display_info(self) -> str:
        """
        Implementation of abstract method from DataEntity.
        Returns formatted display string for person.
        """
        info = f"PATIENT INFORMATION\n"
        info += f"ID: {self._id}  |  Name: {self.__first_name} {self.__last_name}\n"
        info += f"Phone: {self.__phone or 'Not provided'}\n"
        info += f"Address: {self.__address or 'Not provided'}\n\n"
        
        info += f"VACCINATION STATUS\n"
        info += f"{'[YES]' if self.__covid19_vaccine else '[NO]'} COVID-19 Vaccine\n"
        info += f"{'[YES]' if self.__influenza_vaccine else '[NO]'} Influenza Vaccine\n"
        info += f"{'[YES]' if self.__ebola_vaccine else '[NO]'} Ebola Vaccine\n\n"
        
        info += f"CURRENT SYMPTOMS\n"
        info += f"{'[YES]' if self.__fever else '[NO]'} Fever\n"
        info += f"{'[YES]' if self.__fatigue else '[NO]'} Fatigue\n"
        info += f"{'[YES]' if self.__headache else '[NO]'} Headache\n\n"
        
        return info
    
    def is_cleared_for_entry(self) -> bool:
        """
        Checks if person meets all requirements for entry.
        Person is cleared if fully vaccinated and has no symptoms.
        """
        fully_vaccinated = (self.__covid19_vaccine and 
                          self.__influenza_vaccine and 
                          self.__ebola_vaccine)
        
        has_symptoms = (self.__fever or self.__fatigue or self.__headache)
        
        return fully_vaccinated and not has_symptoms
    
    def reset_data(self):
        """Reset vaccine and symptom data."""
        # reset vaccine status
        self.__covid19_vaccine = False
        self.__influenza_vaccine = False
        self.__ebola_vaccine = False
        
        # reset symptoms
        self.__fever = False
        self.__fatigue = False
        self.__headache = False
    
    def update_medical_data(self, vaccines: Dict[str, bool] = None, 
                           symptoms: Dict[str, bool] = None):
        """
        Bulk update method using keyword arguments for flexibility.
        Allows updating multiple medical fields at once.
        """
        if vaccines:
            if 'covid19' in vaccines:
                self.__covid19_vaccine = vaccines['covid19']
            if 'influenza' in vaccines:
                self.__influenza_vaccine = vaccines['influenza']
            if 'ebola' in vaccines:
                self.__ebola_vaccine = vaccines['ebola']
        
        if symptoms:
            if 'fever' in symptoms:
                self.__fever = symptoms['fever']
            if 'fatigue' in symptoms:
                self.__fatigue = symptoms['fatigue']
            if 'headache' in symptoms:
                self.__headache = symptoms['headache']