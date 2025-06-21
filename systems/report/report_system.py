# report_system.py
# Final Vax Project Report System
# COP5230 Assignment M5
# 06/21/2025
# Hamza Kurdi

from typing import Dict, Any, List
from datetime import datetime
from classes.base_classes import ReportGenerator
from classes.person.vaccine_manager import VaccineManager

# ===== INHERITANCE DEMONSTRATED HERE =====
# IndividualReport inherits from ReportGenerator abstract base class
# This demonstrates inheritance - gets structure and behavior from ReportGenerator
class IndividualReport(ReportGenerator):
    """
    Concrete implementation of ReportGenerator for individual patient reports.
    Demonstrates polymorphism through different report generation.
    """
    
    def __init__(self, manager: VaccineManager, patient_id: int):
        # ===== INHERITANCE DEMONSTRATED HERE =====
        # Calling parent class constructor using super()
        super().__init__(manager)
        
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Private/protected attributes encapsulate report state
        self._patient_id = patient_id
        self._report_title = "Individual Patient Report"
        self._target_person = None
        
        # find the person during initialization
        self._target_person = self._data_source.get_person_by_id(patient_id)
    
    def generate_content(self) -> str:
        """
        Implementation of abstract method for individual report content.
        ===== INHERITANCE & POLYMORPHISM DEMONSTRATED HERE =====
        This method implements the abstract method from ReportGenerator
        Each report type implements this method differently (polymorphism)
        """
        if not self._target_person:
            return f"ERROR: No patient found with ID {self._patient_id}"
        
        person = self._target_person
        
        content = f"DETAILED PATIENT REPORT\n\n"
        content += f"Patient ID: {person.id}\n"
        content += f"Name: {person.get_first_name()} {person.get_last_name()}\n"
        content += f"Phone: {person.get_phone() or 'Not provided'}\n"
        content += f"Address: {person.get_address() or 'Not provided'}\n\n"
        
        content += f"VACCINATION RECORD:\n"
        content += f"   COVID-19: {'Vaccinated' if person.get_covid19_vaccine() else 'Not Vaccinated'}\n"
        content += f"   Influenza: {'Vaccinated' if person.get_influenza_vaccine() else 'Not Vaccinated'}\n"
        content += f"   Ebola: {'Vaccinated' if person.get_ebola_vaccine() else 'Not Vaccinated'}\n\n"
        
        content += f"SYMPTOM CHECK:\n"
        content += f"   Fever: {'Present' if person.get_fever() else 'None'}\n"
        content += f"   Fatigue: {'Present' if person.get_fatigue() else 'None'}\n"
        content += f"   Headache: {'Present' if person.get_headache() else 'None'}\n\n"
        
        if person.is_cleared_for_entry():
            content += "FINAL STATUS: CLEARED FOR ENTRY\nPatient meets all requirements."
        else:
            content += "FINAL STATUS: NOT CLEARED\nPatient does not meet entry requirements."
        
        return content
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Implementation of abstract method for individual report statistics.
        ===== INHERITANCE & POLYMORPHISM DEMONSTRATED HERE =====
        Another polymorphic method - each report type calculates different statistics
        """
        if not self._target_person:
            return {}
        
        person = self._target_person
        
        return {
            "Vaccines Received": person.get_vaccine_count(),
            "Current Symptoms": person.get_symptom_count(),
            "Entry Status": "CLEARED" if person.is_cleared_for_entry() else "NOT CLEARED"
        }


# ===== INHERITANCE DEMONSTRATED HERE =====
# VaccinationStatsReport also inherits from ReportGenerator
# Multiple classes inherit from the same base class showing inheritance hierarchy
class VaccinationStatsReport(ReportGenerator):
    """
    Concrete implementation for vaccination statistics report.
    Shows polymorphism with different content generation logic.
    """
    
    def __init__(self, manager: VaccineManager):
        # ===== INHERITANCE DEMONSTRATED HERE =====
        # Another example of calling parent constructor
        super().__init__(manager)
        # ===== ENCAPSULATION DEMONSTRATED HERE =====
        # Protected attribute encapsulates report configuration
        self._report_title = "Vaccination Statistics Report"
    
    def generate_content(self) -> str:
        """
        Implementation of abstract method for vaccination stats content.
        ===== POLYMORPHISM DEMONSTRATED HERE =====
        Same method name as IndividualReport but completely different implementation
        This is polymorphism - same interface, different behavior
        """
        if self._data_source.get_person_count() == 0:
            return "No patients in the system.\n\nAdd patients to view vaccination statistics."
        
        stats = self._data_source.get_vaccination_stats()
        total = stats['total_people']
        
        content = f"VACCINATION STATISTICS\n\n"
        content += f"Total Patients: {total}\n\n"
        content += f"Vaccination Coverage:\n"
        content += f"   COVID-19: {stats['covid19']} patients ({stats['covid19']/total*100:.1f}%)\n"
        content += f"   Influenza: {stats['influenza']} patients ({stats['influenza']/total*100:.1f}%)\n"
        content += f"   Ebola: {stats['ebola']} patients ({stats['ebola']/total*100:.1f}%)\n\n"
        content += f"Fully Vaccinated: {stats['fully_vaccinated']} patients ({stats['fully_vaccinated']/total*100:.1f}%)"
        
        return content
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Implementation of abstract method for vaccination statistics.
        ===== POLYMORPHISM DEMONSTRATED HERE =====
        Different statistical calculations than IndividualReport - polymorphic behavior
        """
        stats = self._data_source.get_vaccination_stats()
        
        return {
            "Total Patients": stats['total_people'],
            "COVID-19 Coverage": f"{stats['covid19']/stats['total_people']*100:.1f}%" if stats['total_people'] > 0 else "0%",
            "Influenza Coverage": f"{stats['influenza']/stats['total_people']*100:.1f}%" if stats['total_people'] > 0 else "0%",
            "Ebola Coverage": f"{stats['ebola']/stats['total_people']*100:.1f}%" if stats['total_people'] > 0 else "0%",
            "Fully Vaccinated": f"{stats['fully_vaccinated']/stats['total_people']*100:.1f}%" if stats['total_people'] > 0 else "0%"
        }


# ===== INHERITANCE DEMONSTRATED HERE =====
# Third class inheriting from ReportGenerator - shows inheritance hierarchy
class SymptomAnalysisReport(ReportGenerator):
    """
    Concrete implementation for symptom analysis report.
    Another example of polymorphism in report generation.
    """
    
    def __init__(self, manager: VaccineManager):
        super().__init__(manager)
        self._report_title = "Symptom Analysis Report"
    
    def generate_content(self) -> str:
        """
        Implementation of abstract method for symptom analysis content.
        ===== POLYMORPHISM DEMONSTRATED HERE =====
        Third different implementation of generate_content - pure polymorphism
        """
        if self._data_source.get_person_count() == 0:
            return "No patients in the system.\n\nAdd patients to view symptom analysis."
        
        # get vaccinated people with symptoms
        covid_with_symptoms = 0
        flu_with_symptoms = 0
        ebola_with_symptoms = 0
        
        for person in self._data_source.get_people():
            has_symptoms = (person.get_fever() or person.get_fatigue() or person.get_headache())
            
            if person.get_covid19_vaccine() and has_symptoms:
                covid_with_symptoms += 1
            if person.get_influenza_vaccine() and has_symptoms:
                flu_with_symptoms += 1
            if person.get_ebola_vaccine() and has_symptoms:
                ebola_with_symptoms += 1
        
        symptom_stats = self._data_source.get_symptom_stats()
        
        content = f"SYMPTOM ANALYSIS REPORT\n\n"
        content += f"Vaccinated patients currently experiencing symptoms:\n\n"
        content += f"COVID-19 vaccinated with symptoms: {covid_with_symptoms}\n"
        content += f"Influenza vaccinated with symptoms: {flu_with_symptoms}\n"
        content += f"Ebola vaccinated with symptoms: {ebola_with_symptoms}\n\n"
        content += f"Total patients with any symptoms: {symptom_stats['any_symptoms']}\n"
        content += f"Patients cleared for entry: {symptom_stats['cleared_for_entry']}"
        
        return content
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Implementation of abstract method for symptom statistics.
        ===== POLYMORPHISM DEMONSTRATED HERE =====
        Third different implementation of get_statistics - polymorphic method behavior
        """
        symptom_stats = self._data_source.get_symptom_stats()
        total = self._data_source.get_person_count()
        
        return {
            "Patients with Fever": symptom_stats['fever'],
            "Patients with Fatigue": symptom_stats['fatigue'], 
            "Patients with Headache": symptom_stats['headache'],
            "Patients with Any Symptoms": symptom_stats['any_symptoms'],
            "Symptom Rate": f"{symptom_stats['any_symptoms']/total*100:.1f}%" if total > 0 else "0%",
            "Entry Clearance Rate": f"{symptom_stats['cleared_for_entry']/total*100:.1f}%" if total > 0 else "0%"
        }


class ReportFactory:
    """
    Factory class for creating different types of reports.
    Supports scalability by centralizing report creation logic.
    """
    
    @staticmethod
    def create_individual_report(manager: VaccineManager, patient_id: int) -> IndividualReport:
        """Factory method for individual reports"""
        return IndividualReport(manager, patient_id)
    
    @staticmethod
    def create_vaccination_report(manager: VaccineManager) -> VaccinationStatsReport:
        """Factory method for vaccination statistics reports"""
        return VaccinationStatsReport(manager)
    
    @staticmethod
    def create_symptom_report(manager: VaccineManager) -> SymptomAnalysisReport:
        """Factory method for symptom analysis reports"""
        return SymptomAnalysisReport(manager)
    
    @staticmethod
    def get_available_report_types() -> List[str]:
        """Get list of available report types for UI"""
        return ["individual", "vaccination", "symptom"]
    
    @staticmethod
    def create_report_by_type(report_type: str, manager: VaccineManager, **kwargs) -> ReportGenerator:
        """
        Create report by type string with keyword arguments.
        Demonstrates keyword argument usage.
        """
        if report_type.lower() == "individual":
            patient_id = kwargs.get('patient_id')
            if patient_id is None:
                raise ValueError("patient_id required for individual reports")
            return ReportFactory.create_individual_report(manager, patient_id)
        
        elif report_type.lower() == "vaccination":
            return ReportFactory.create_vaccination_report(manager)
        
        elif report_type.lower() == "symptom":
            return ReportFactory.create_symptom_report(manager)
        
        else:
            raise ValueError(f"Unknown report type: {report_type}")


class ReportManager:
    """
    Manager class for handling multiple reports and batch operations.
    Demonstrates composition and better encapsulation.
    """
    
    def __init__(self, vaccine_manager: VaccineManager):
        self.__vaccine_manager = vaccine_manager
        self.__report_history = []  # private list to store generated reports
        self.__factory = ReportFactory()
    
    def generate_individual_report(self, patient_id: int, **format_options) -> str:
        """
        Generate individual patient report with formatting options.
        Uses keyword arguments for flexible formatting.
        """
        try:
            report = self.__factory.create_individual_report(self.__vaccine_manager, patient_id)
            
            valid_options = {}
            if 'title' in format_options:
                valid_options['title'] = format_options['title']
            if 'include_stats' in format_options:
                valid_options['include_stats'] = format_options['include_stats']
            
            formatted_report = report.format_report(**valid_options)
            
            self.__report_history.append({
                'type': 'individual',
                'patient_id': patient_id,
                'content': formatted_report,
                'timestamp': datetime.now().strftime("%m-%d-%Y")
            })
            
            return formatted_report
            
        except Exception as e:
            # print(f"Error generating individual report: {str(e)}")
            return f"Error generating individual report"
    
    def generate_vaccination_stats(self, **format_options) -> str:
        """Generate vaccination statistics report"""
        try:
            report = self.__factory.create_vaccination_report(self.__vaccine_manager)
            
            valid_options = {}
            if 'title' in format_options:
                valid_options['title'] = format_options['title']
            if 'include_stats' in format_options:
                valid_options['include_stats'] = format_options['include_stats']
            
            formatted_report = report.format_report(**valid_options)
            
            self.__report_history.append({
                'type': 'vaccination',
                'content': formatted_report,
                'timestamp': datetime.now().strftime("%m-%d-%Y")
            })
            
            return formatted_report
            
        except Exception as e:
            # print(f"Error generating vaccination report: {str(e)}")
            return f"Error generating vaccination report"
    
    def generate_symptom_analysis(self, **format_options) -> str:
        """Generate symptom analysis report"""
        try:
            report = self.__factory.create_symptom_report(self.__vaccine_manager)
            
            valid_options = {}
            if 'title' in format_options:
                valid_options['title'] = format_options['title']
            if 'include_stats' in format_options:
                valid_options['include_stats'] = format_options['include_stats']
            
            formatted_report = report.format_report(**valid_options)
            
            self.__report_history.append({
                'type': 'symptom',
                'content': formatted_report,
                'timestamp': datetime.now().strftime("%m-%d-%Y")
            })
            
            return formatted_report
            
        except Exception as e:
            # print(f"Error generating symptom analysis: {str(e)}")
            return f"Error generating symptom report"
    
    def get_report_history_count(self) -> int:
        """Get number of reports generated"""
        return len(self.__report_history)
    
    def clear_report_history(self):
        """Clear report history"""
        self.__report_history.clear()
    
    def batch_generate_all_reports(self, **format_options) -> Dict[str, str]:
        """
        Generate all available reports in batch operation.
        Returns dict with report type as key and content as value.
        """
        results = {}
        
        # vaccination stats report
        results['vaccination'] = self.generate_vaccination_stats(**format_options)
        
        # symptom analysis report  
        results['symptom'] = self.generate_symptom_analysis(**format_options)
        
        # individual reports for all patients
        individual_reports = {}
        for person in self.__vaccine_manager.get_people():
            report_content = self.generate_individual_report(person.id, **format_options)
            individual_reports[f"patient_{person.id}"] = report_content
        
        results['individual_reports'] = individual_reports
        
        return results