# vaccine_manager.py
# Final Vax Project VaccineManager class
# COP5230 Assignment M5
# 06/21/2025
# Hamza Kurdi

from typing import Optional, Dict, List
from person import Person

class VaccineManager:
    """
    Enhanced manager class for Person collection.
    Implements better encapsulation and scalability.
    """
    
    def __init__(self, max_capacity: int = 15):
        self.__people = []  # private list 
        self.__max_capacity = max_capacity
    
    def get_person_count(self) -> int:
        """Getter for current person count"""
        return len(self.__people)
    
    def get_max_capacity(self) -> int:
        """Getter for maximum capacity"""
        return self.__max_capacity
    
    def add_person(self, person: Person) -> bool:
        """
        Enhanced add person method with better validation.
        Returns bool indicating success.
        """
        # check capacity
        if len(self.__people) >= self.__max_capacity:
            return False
        
        # check for duplicate ID
        if self.get_person_by_id(person.id):
            return False
        
        # validate person data
        if not person.validate_data():
            return False
        
        # add person
        self.__people.append(person)
        return True
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """Find person by ID"""
        for person in self.__people:
            if person.id == person_id:
                return person
        return None
    
    def get_person_by_index(self, index: int) -> Optional[Person]:
        """Get person by list index with bounds checking"""
        if 0 <= index < len(self.__people):
            return self.__people[index]
        return None
    
    def clear_all_people(self):
        """Clear all people from manager"""
        count = len(self.__people)
        self.__people.clear()
        return count
    
    def reset_all_medical_data(self):
        """Reset vaccine and symptom data for all people"""
        count = 0
        for person in self.__people:
            person.reset_data()
            count += 1
        return count
    
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
            if person.fever:
                stats['fever'] += 1
            if person.fatigue:
                stats['fatigue'] += 1
            if person.headache:
                stats['headache'] += 1
            
            if person.fever or person.fatigue or person.headache:
                stats['any_symptoms'] += 1
            
            if person.is_cleared_for_entry():
                stats['cleared_for_entry'] += 1
        
        return stats
    
    # backward compatibility property
    @property
    def people(self) -> List[Person]:
        """Property for backward compatibility with existing GUI code"""
        return self.__people