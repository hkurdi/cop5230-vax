# person.py
# Final Vax Project Person classes
# COP5230 Assignment M5
# 06/21/2025
# Hamza Kurdi

from typing import Dict
from base_classes import DataEntity


class Person(DataEntity):
    """
    Person class that extends DataEntity base class.
    Uses private attributes with getter/setter properties for data encapsulation.
    Handles patient info, vaccination records, and symptom tracking.
    """
    
    def __init__(self, person_id: int, first_name: str, last_name: str, 
                 phone: str = "", address: str = ""):
        """Create new person object with required ID and name, optional contact info"""
        super().__init__(person_id)
        
        # store personal info as private attributes
        self.__first_name = first_name.strip()
        self.__last_name = last_name.strip()
        self.__phone = phone.strip()
        self.__address = address.strip()
        
        # initialize vaccination status - all start as False
        self.__covid19_vaccine = False
        self.__influenza_vaccine = False
        self.__ebola_vaccine = False
        
        # symptom tracking variables
        self.__fever = False
        self.__fatigue = False
        self.__headache = False
    
    # Property accessors for private data
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
        Overrides the abstract validate_data method from parent class.
        Makes sure person has required fields filled out properly.
        """
        # need at least first and last name
        if not self.__first_name or not self.__last_name:
            return False
        
        # check that ID is valid (inherited from DataEntity)
        if self._id <= 0:
            return False
        
        return True
    
    def get_display_info(self) -> str:
        """
        Overrides abstract method to show formatted person information.
        Returns a nice formatted string with all the patient details.
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
        Determines if person can enter the facility based on vaccination and symptoms.
        Need all 3 vaccines AND no symptoms to be cleared for entry.
        """
        fully_vaccinated = (self.__covid19_vaccine and 
                          self.__influenza_vaccine and 
                          self.__ebola_vaccine)
        
        has_symptoms = (self.__fever or self.__fatigue or self.__headache)
        
        return fully_vaccinated and not has_symptoms
    
    def reset_data(self):
        """Clears all vaccination and symptom data back to default values."""
        # reset all vaccine flags
        self.__covid19_vaccine = False
        self.__influenza_vaccine = False
        self.__ebola_vaccine = False
        
        # clear symptom flags
        self.__fever = False
        self.__fatigue = False
        self.__headache = False
    
    def update_medical_data(self, vaccines: Dict[str, bool] = None, 
                           symptoms: Dict[str, bool] = None):
        """
        Convenient method to update multiple medical fields at once.
        Pass dictionaries with the fields you want to update.
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