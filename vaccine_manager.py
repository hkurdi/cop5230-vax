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
    """
    
    def __init__(self, max_capacity: int = 15):
        self.__people = []
        self.__max_capacity = max_capacity
        self.__id_lookup = {}  # dictionary to make finding people faster hopefully
    
    def get_person_count(self) -> int:
        """returns how many people we currently have"""
        return len(self.__people)
    
    def get_max_capacity(self) -> int:
        """returns the max number of people allowed"""
        return self.__max_capacity
    
    def add_person(self, person: Person) -> bool:
        """tries to add a person to the system, returns True if it worked"""
        if (len(self.__people) >= self.__max_capacity or 
            person.id in self.__id_lookup or 
            not person.validate_data()):
            return False
        
        self.__people.append(person)
        self.__id_lookup[person.id] = person
        return True
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """find someone by their ID number - should be faster with the dictionary"""
        return self.__id_lookup.get(person_id)
    
    def get_person_by_index(self, index: int) -> Optional[Person]:
        """get person by their position in the list, checks bounds so we dont crash"""
        return self.__people[index] if 0 <= index < len(self.__people) else None
    
    def get_people(self) -> List[Person]:
        """returns a copy of all the people so you cant mess with the original list"""
        return self.__people.copy()
    
    def clear_all_people(self) -> int:
        """removes everyone from the system and tells you how many got removed"""
        count = len(self.__people)
        self.__people.clear()
        self.__id_lookup.clear()
        return count
    
    def reset_all_medical_data(self) -> int:
        """clears all the medical info for everyone, keeps the people tho"""
        for person in self.__people:
            person.reset_data()
        return len(self.__people)
    
    def get_vaccination_stats(self) -> Dict[str, int]:
        """calculates vaccination stats for reporting - counts each vaccine type"""
        if not self.__people:
            return {'covid19': 0, 'influenza': 0, 'ebola': 0, 'fully_vaccinated': 0, 'total_people': 0}
        
        stats = {'total_people': len(self.__people), 'covid19': 0, 'influenza': 0, 'ebola': 0, 'fully_vaccinated': 0}
        
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
        """counts up all the different symptoms people have - for the health reports"""
        if not self.__people:
            return {'fever': 0, 'fatigue': 0, 'headache': 0, 'any_symptoms': 0, 'cleared_for_entry': 0}
        
        stats = {'fever': 0, 'fatigue': 0, 'headache': 0, 'any_symptoms': 0, 'cleared_for_entry': 0}
        
        for person in self.__people:
            if person.get_fever():
                stats['fever'] += 1
            if person.get_fatigue():
                stats['fatigue'] += 1
            if person.get_headache():
                stats['headache'] += 1
            if person.get_symptom_count() > 0:
                stats['any_symptoms'] += 1
            if person.is_cleared_for_entry():
                stats['cleared_for_entry'] += 1
        
        return stats