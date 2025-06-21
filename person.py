# person.py
# Enhanced Person and VaccineManager classes with OOP principles
# COP5230 Assignment 2 M4 - Enhanced OOP Version
# 06/14/2025
# Hamza Kurdi

from typing import List, Optional, Dict, Any
from base_classes import DataEntity, DataValidator


class Person(DataEntity):
    """
    Enhanced Person class inheriting from DataEntity ABC.
    Implements encapsulation with private variables and getters/setters.
    """
    
    def __init__(self, person_id: int, first_name: str, last_name: str, 
                 phone: str = "", address: str = ""):
        """
        Initialize person with positional and keyword arguments
        """
        super().__init__(person_id)
        
        # private instance variables with explicit declaration
        self.__first_name = ""
        self.__last_name = ""
        self.__phone = ""
        self.__address = ""
        
        # private vaccine status variables
        self.__covid19_vaccine = False
        self.__influenza_vaccine = False
        self.__ebola_vaccine = False
        
        # private symptom variables  
        self.__fever = False
        self.__fatigue = False
        self.__headache = False
        
        # use setters for validation during initialization
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_phone(phone)
        self.set_address(address)
    
    # getter and setter methods for encapsulation
    def get_first_name(self) -> str:
        """Getter for first name"""
        return self.__first_name
    
    def set_first_name(self, name: str):
        """Setter for first name with validation"""
        if DataValidator.validate_name(name):
            self.__first_name = name.strip()
        else:
            raise ValueError("Invalid first name")
    
    def get_last_name(self) -> str:
        """Getter for last name"""
        return self.__last_name
    
    def set_last_name(self, name: str):
        """Setter for last name with validation"""
        if DataValidator.validate_name(name):
            self.__last_name = name.strip()
        else:
            raise ValueError("Invalid last name")
    
    def get_phone(self) -> str:
        """Getter for phone number"""
        return self.__phone
    
    def set_phone(self, phone: str):
        """Setter for phone with validation"""
        if DataValidator.validate_phone(phone):
            self.__phone = phone.strip()
        else:
            raise ValueError("Invalid phone number format")
    
    def get_address(self) -> str:
        """Getter for address"""
        return self.__address
    
    def set_address(self, address: str):
        """Setter for address"""
        self.__address = address.strip()
    
    # vaccine status getters and setters
    def get_covid19_vaccine(self) -> bool:
        """Getter for COVID-19 vaccine status"""
        return self.__covid19_vaccine
    
    def set_covid19_vaccine(self, status: bool):
        """Setter for COVID-19 vaccine status"""
        self.__covid19_vaccine = bool(status)
    
    def get_influenza_vaccine(self) -> bool:
        """Getter for influenza vaccine status"""
        return self.__influenza_vaccine
    
    def set_influenza_vaccine(self, status: bool):
        """Setter for influenza vaccine status"""
        self.__influenza_vaccine = bool(status)
    
    def get_ebola_vaccine(self) -> bool:
        """Getter for ebola vaccine status"""
        return self.__ebola_vaccine
    
    def set_ebola_vaccine(self, status: bool):
        """Setter for ebola vaccine status"""
        self.__ebola_vaccine = bool(status)
    
    # symptom getters and setters
    def get_fever(self) -> bool:
        """Getter for fever symptom"""
        return self.__fever
    
    def set_fever(self, status: bool):
        """Setter for fever symptom"""
        self.__fever = bool(status)
    
    def get_fatigue(self) -> bool:
        """Getter for fatigue symptom"""
        return self.__fatigue
    
    def set_fatigue(self, status: bool):
        """Setter for fatigue symptom"""
        self.__fatigue = bool(status)
    
    def get_headache(self) -> bool:
        """Getter for headache symptom"""
        return self.__headache
    
    def set_headache(self, status: bool):
        """Setter for headache symptom"""
        self.__headache = bool(status)
    
    # properties for backward compatibility with existing code
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
        """
        Enhanced reset method - clears vaccine and symptom data.
        Calls parent reset for timestamp handling.
        """
        super().reset_entity()
        
        # reset vaccine status
        self.__covid19_vaccine = False
        self.__influenza_vaccine = False
        self.__ebola_vaccine = False
        
        # reset symptoms
        self.__fever = False
        self.__fatigue = False
        self.__headache = False
    
    def get_vaccine_count(self) -> int:
        """Helper method to count how many vaccines person has"""
        count = 0
        if self.__covid19_vaccine:
            count += 1
        if self.__influenza_vaccine:
            count += 1
        if self.__ebola_vaccine:
            count += 1
        return count
    
    def get_symptom_count(self) -> int:
        """Helper method to count current symptoms"""
        count = 0
        if self.__fever:
            count += 1
        if self.__fatigue:
            count += 1
        if self.__headache:
            count += 1
        return count
    
    def update_medical_data(self, vaccines: Dict[str, bool] = None, 
                           symptoms: Dict[str, bool] = None):
        """
        Bulk update method using keyword arguments for flexibility.
        Allows updating multiple medical fields at once.
        """
        if vaccines:
            # update vaccine status if provided
            if 'covid19' in vaccines:
                self.set_covid19_vaccine(vaccines['covid19'])
            if 'influenza' in vaccines:
                self.set_influenza_vaccine(vaccines['influenza'])
            if 'ebola' in vaccines:
                self.set_ebola_vaccine(vaccines['ebola'])
        
        if symptoms:
            # update symptom status if provided
            if 'fever' in symptoms:
                self.set_fever(symptoms['fever'])
            if 'fatigue' in symptoms:
                self.set_fatigue(symptoms['fatigue'])
            if 'headache' in symptoms:
                self.set_headache(symptoms['headache'])


class VaccineManager:
    """
    Enhanced manager class for Person collection.
    Implements better encapsulation and scalability.
    """
    
    def __init__(self, max_capacity: int = 15):
        self.__people = []  # private list 
        self.__max_capacity = max_capacity
        self.__id_tracker = set()  # track used IDs for efficiency
    
    def get_people(self) -> List[Person]:
        """Getter for people list (returns copy for encapsulation)"""
        return self.__people.copy()
    
    def get_person_count(self) -> int:
        """Getter for current person count"""
        return len(self.__people)
    
    def get_max_capacity(self) -> int:
        """Getter for maximum capacity"""
        return self.__max_capacity
    
    def set_max_capacity(self, capacity: int):
        """Setter for maximum capacity with validation"""
        if capacity < len(self.__people):
            raise ValueError("Cannot set capacity lower than current person count")
        self.__max_capacity = capacity
    
    def add_person(self, person: Person) -> bool:
        """
        Enhanced add person method with better validation.
        Returns bool indicating success.
        """
        # check capacity
        if len(self.__people) >= self.__max_capacity:
            # print(f"Cannot add person - at capacity limit of {self.__max_capacity}")
            return False
        
        # check for duplicate ID
        if person.id in self.__id_tracker:
            # print(f"Cannot add person - ID {person.id} already exists")
            return False
        
        # validate person data
        if not person.validate_data():
            # print("Cannot add person - invalid data")
            return False
        
        # add person and track ID
        self.__people.append(person)
        self.__id_tracker.add(person.id)
        # print(f"Successfully added person {person.get_first_name()} {person.get_last_name()}")
        return True
    
    def remove_person(self, person_id: int) -> bool:
        """
        Remove person by ID.
        Returns bool indicating success.
        """
        for i, person in enumerate(self.__people):
            if person.id == person_id:
                removed_person = self.__people.pop(i)
                self.__id_tracker.remove(person_id)
                # print(f"Removed person {removed_person.get_first_name()} {removed_person.get_last_name()}")
                return True
        
        # print(f"Person with ID {person_id} not found")
        return False
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """
        Enhanced find method with better efficiency using ID tracker.
        """
        # quick check if ID exists
        if person_id not in self.__id_tracker:
            return None
        
        # find and return person
        for person in self.__people:
            if person.id == person_id:
                return person
        
        return None
    
    def get_person_by_index(self, index: int) -> Optional[Person]:
        """
        Get person by list index with bounds checking.
        """
        if 0 <= index < len(self.__people):
            return self.__people[index]
        return None
    
    def clear_all_people(self):
        """Clear all people from manager"""
        count = len(self.__people)
        self.__people.clear()
        self.__id_tracker.clear()
        print(f"DEBUG: Cleared {count} people from manager")
        return count
    
    def reset_all_medical_data(self):
        """Reset vaccine and symptom data for all people"""
        count = 0
        for person in self.__people:
            person.reset_data()
            count += 1
        print(f"DEBUG: Reset medical data for {count} people")
        return count
    
    def get_available_ids(self) -> List[int]:
        """Get list of all currently used IDs"""
        return list(self.__id_tracker)
    
    def is_id_available(self, person_id: int) -> bool:
        """Check if ID is available for use"""
        return person_id not in self.__id_tracker
    
    def get_vaccination_stats(self) -> Dict[str, int]:
        """
        Get vaccination statistics for all people.
        Returns dict with vaccine counts.
        """
        stats = {
            'covid19': 0,
            'influenza': 0, 
            'ebola': 0,
            'fully_vaccinated': 0,
            'total_people': len(self.__people)
        }
        
        for person in self.__people:
            if person.get_covid19_vaccine():
                stats['covid19'] += 1
            if person.get_influenza_vaccine():
                stats['influenza'] += 1
            if person.get_ebola_vaccine():
                stats['ebola'] += 1
            if person.is_cleared_for_entry():
                stats['fully_vaccinated'] += 1
        
        return stats
    
    def get_symptom_stats(self) -> Dict[str, int]:
        """
        Get symptom statistics for all people.
        Returns dict with symptom counts.
        """
        stats = {
            'fever': 0,
            'fatigue': 0,
            'headache': 0,
            'any_symptoms': 0,
            'cleared_for_entry': 0
        }
        
        for person in self.__people:
            if person.get_fever():
                stats['fever'] += 1
            if person.get_fatigue():
                stats['fatigue'] += 1
            if person.get_headache():
                stats['headache'] += 1
            
            if person.get_fever() or person.get_fatigue() or person.get_headache():
                stats['any_symptoms'] += 1
            
            if person.is_cleared_for_entry():
                stats['cleared_for_entry'] += 1
        
        return stats
    
    # backward compatibility property
    @property
    def people(self) -> List[Person]:
        """Property for backward compatibility with existing GUI code"""
        return self.__people