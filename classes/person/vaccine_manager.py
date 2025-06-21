# vaccine_manager.py
# Final Vax Project - VaccineManager class implementation
# COP5230 Assignment M5 
# 06/21/2025
# Hamza Kurdi

from typing import Optional, Dict, List
from person import Person

class VaccineManager:
    """
    This class manages a bunch of Person objects for the vaccine program.
    Basically stores people and lets you do stuff with them like add/remove etc.
    Made it more efficient by using a dictionary to find people faster.
    
    ===== ENCAPSULATION DEMONSTRATED THROUGHOUT THIS CLASS =====
    This class encapsulates the management of Person objects and provides
    a clean interface for vaccine management operations.
    """
    
    def __init__(self, max_capacity: int = 15):
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Private attributes hide the internal data structures from external access
        # External code cannot directly manipulate the people list or lookup dictionary
        self.__people = []  # Private list of Person objects
        self.__max_capacity = max_capacity  # Private capacity limit
        self.__id_lookup = {}  # Private dictionary to make finding people faster hopefully
    
    # ===== ENCAPSULATION DEMONSTRATED HERE =====
    # Public getter methods provide controlled read-only access to private data
    # External code can query the state but cannot directly modify private attributes
    def get_person_count(self) -> int:
        """returns how many people we currently have"""
        return len(self.__people)
    
    def get_max_capacity(self) -> int:
        """returns the max number of people allowed"""
        return self.__max_capacity
    
    def add_person(self, person: Person) -> bool:
        """tries to add a person to the system, returns True if it worked"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # This method encapsulates complex validation logic and data management
        # External code just calls add_person() - all the internal complexity is hidden
        if (len(self.__people) >= self.__max_capacity or 
            person.id in self.__id_lookup or 
            not person.validate_data()):
            return False
        
        # Private data structures are modified through controlled internal logic
        self.__people.append(person)
        self.__id_lookup[person.id] = person
        return True
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """find someone by their ID number - should be faster with the dictionary"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # The internal lookup dictionary is hidden from external code
        # This method provides the interface to access private data safely
        return self.__id_lookup.get(person_id)
    
    def get_person_by_index(self, index: int) -> Optional[Person]:
        """get person by their position in the list, checks bounds so we dont crash"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Encapsulates bounds checking and safe access to private list
        # External code doesn't need to worry about array bounds - it's handled internally
        return self.__people[index] if 0 <= index < len(self.__people) else None
    
    def get_people(self) -> List[Person]:
        """returns a copy of all the people so you cant mess with the original list"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Returns a copy instead of direct access to private data
        # This prevents external code from accidentally modifying the internal list
        return self.__people.copy()
    
    def clear_all_people(self) -> int:
        """removes everyone from the system and tells you how many got removed"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Encapsulates the complex operation of clearing both data structures
        # External code gets a simple interface, internal consistency is maintained
        count = len(self.__people)
        self.__people.clear()
        self.__id_lookup.clear()
        return count
    
    def reset_all_medical_data(self) -> int:
        """clears all the medical info for everyone, keeps the people tho"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Encapsulates iteration over private data and coordination with Person objects
        for person in self.__people:
            person.reset_data()  # Uses Person's encapsulated reset method
        return len(self.__people)
    
    def get_vaccination_stats(self) -> Dict[str, int]:
        """calculates vaccination stats for reporting - counts each vaccine type"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Complex statistical calculation is encapsulated in a clean method interface
        # Internal iteration over private data is hidden from external code
        if not self.__people:
            return {'covid19': 0, 'influenza': 0, 'ebola': 0, 'fully_vaccinated': 0, 'total_people': 0}
        
        stats = {'total_people': len(self.__people), 'covid19': 0, 'influenza': 0, 'ebola': 0, 'fully_vaccinated': 0}
        
        # Private data access is encapsulated within this method
        for person in self.__people:
            if person.get_covid19_vaccine():  # Using Person's encapsulated getter methods
                stats['covid19'] += 1
            if person.get_influenza_vaccine():
                stats['influenza'] += 1
            if person.get_ebola_vaccine():
                stats['ebola'] += 1
            if person.is_cleared_for_entry():  # Using Person's encapsulated business logic
                stats['fully_vaccinated'] += 1
        
        return stats
    
    def get_symptom_stats(self) -> Dict[str, int]:
        """counts up all the different symptoms people have - for the health reports"""
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Another example of encapsulating complex data processing
        # External code gets clean statistics without knowing internal implementation
        if not self.__people:
            return {'fever': 0, 'fatigue': 0, 'headache': 0, 'any_symptoms': 0, 'cleared_for_entry': 0}
        
        stats = {'fever': 0, 'fatigue': 0, 'headache': 0, 'any_symptoms': 0, 'cleared_for_entry': 0}
        
        # Iteration over private data is encapsulated within this method
        for person in self.__people:
            # Uses Person's encapsulated getter methods instead of direct attribute access
            if person.get_fever():
                stats['fever'] += 1
            if person.get_fatigue():
                stats['fatigue'] += 1
            if person.get_headache():
                stats['headache'] += 1
            if person.get_symptom_count() > 0:  # Uses Person's encapsulated calculation
                stats['any_symptoms'] += 1
            if person.is_cleared_for_entry():  # Uses Person's encapsulated business logic
                stats['cleared_for_entry'] += 1
        
        return stats