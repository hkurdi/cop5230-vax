# vaccine_manager.py
# Final Vax Project VaccineManager class
# COP5230 Assignment M5
# 06/21/2025
# Hamza Kurdi

from typing import Optional, Dict, List
from person import Person

class VaccineManager:
    """
    Manager class for handling Person collection.
    This class encapsulates the person data and provides scalable operations.
    I tried to follow good OOP principles here.
    """
    
    def __init__(self, max_capacity: int = 15):
        self.__people = []  # private list to store people
        self.__max_capacity = max_capacity
    
    def get_person_count(self) -> int:
        """Returns the current number of people in the system"""
        return len(self.__people)
    
    def get_max_capacity(self) -> int:
        """Returns the maximum capacity allowed"""
        return self.__max_capacity
    
    def add_person(self, person: Person) -> bool:
        """
        Adds a new person to the manager with validation.
        Returns True if successful, False otherwise.
        Had to add lots of checks to make sure we don't get duplicate data.
        """
        # first check if we have room
        if len(self.__people) >= self.__max_capacity:
            return False
        
        # make sure we don't have duplicate IDs
        if self.get_person_by_id(person.id):
            return False
        
        # validate the person's data before adding
        if not person.validate_data():
            return False
        
        # everything looks good, add the person
        self.__people.append(person)
        return True
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """Finds and returns a person by their ID, or None if not found"""
        for person in self.__people:
            if person.id == person_id:
                return person
        return None
    
    def get_person_by_index(self, index: int) -> Optional[Person]:
        """Gets person by their position in the list, with safety checks"""
        if 0 <= index < len(self.__people):
            return self.__people[index]
        return None
    
    def clear_all_people(self):
        """Removes all people from the manager and returns how many were removed"""
        count = len(self.__people)
        self.__people.clear()
        return count
    
    def reset_all_medical_data(self):
        """Clears vaccine and symptom data for everyone and returns count"""
        count = 0
        for person in self.__people:
            person.reset_data()
            count += 1
        return count
    
    def get_vaccination_stats(self) -> Dict[str, int]:
        """
        Calculates vaccination statistics for all people in the system.
        Returns a dictionary with counts for each vaccine type.
        This method is pretty useful for generating reports.
        """
        stats = {
            'covid19': 0,
            'influenza': 0, 
            'ebola': 0,
            'fully_vaccinated': 0,
            'total_people': len(self.__people)
        }
        
        for person in self.__people:
            if person.covid19_vaccine:
                stats['covid19'] += 1
            if person.influenza_vaccine:
                stats['influenza'] += 1
            if person.ebola_vaccine:
                stats['ebola'] += 1
            if person.is_cleared_for_entry():
                stats['fully_vaccinated'] += 1
        
        return stats
    
    def get_symptom_stats(self) -> Dict[str, int]:
        """
        Gathers symptom statistics for all people.
        Returns dictionary with symptom counts and clearance info.
        Took me a while to get this logic right.
        """
        stats = {
            'fever': 0,
            'fatigue': 0,
            'headache': 0,
            'any_symptoms': 0,
            'cleared_for_entry': 0
        }
        
        for person in self.__people:
            if person.fever:
                stats['fever'] += 1
            if person.fatigue:
                stats['fatigue'] += 1
            if person.headache:
                stats['headache'] += 1
            
            # check if person has any symptoms at all
            if person.fever or person.fatigue or person.headache:
                stats['any_symptoms'] += 1
            
            if person.is_cleared_for_entry():
                stats['cleared_for_entry'] += 1
        
        return stats
    
    # keeping this for backwards compatibility with the GUI
    @property
    def people(self) -> List[Person]:
        """Property to access the people list - needed for existing GUI code"""
        return self.__people