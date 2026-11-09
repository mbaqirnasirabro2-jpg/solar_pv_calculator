"""
Title: Ultimate Solar PV, Inverter, Battery Bank, and MPPT String Sizing Calculator
Author: Muhammad Baqir (GitHub: @mbaqirnasirabro2-jpg)
Description: Comprehensive Python engineering tool for sizing solar PV arrays, selecting inverters,
             calculating off-grid battery banks, computing DC cable voltage drop, and determining 
             optimal series/parallel PV string configurations for inverter MPPT matching.
"""

import math

class UltimateSolarSystemCalculator:
    def __init__(self, load_kwh_per_day, peak_sun_hours, system_voltage, max_continuous_load_kw=None):
        """
        Initializes the ultimate solar system calculation parameters.
        """
        self.load_kwh = load_kwh_per_day
        self.psh = peak_sun_hours
        self.system_voltage = system_voltage
        self.max_load_kw = max_continuous_load_kw if max_continuous_load_kw else (load_kwh_per_day / 5.0)

    def estimate_pv_sizing(self, system_efficiency=0.75):
        """Calculates required Solar PV Array capacity in kW."""
        required_generation_kwh = self.load_kwh / system_efficiency
        pv_capacity_kw = required_generation_kwh / self.psh
        
        print("--- 1. Solar PV Array Sizing ---")
        print(f"Target Daily Load: {self.load_kwh} kWh/day")
        print(f"Required PV System Capacity: {pv_capacity_kw:.2f} kW ({pv_capacity_kw * 1000:.2f} W)\n")
        return pv_capacity_kw

    def select_inverter_rating(self, surge_safety_factor=1.25):
        """Selects the recommended inverter rating in kW/kVA considering surge loads."""
        recommended_inverter_kw = self.max_load_kw * surge_safety_factor
        
        print("--- 2. Inverter Rating Selection ---")
        print(f"Max Continuous Load: {self.max_load_kw:.2f} kW")
        print(f"Recommended Inverter Capacity: {recommended_inverter_kw:.2f} kW (kVA)\n")
        return recommended_inverter_kw

    def calculate_battery_bank(self, days_of_autonomy=2, depth_of_discharge=0.80, battery_efficiency=0.90):
        """Calculates off-grid battery bank capacity in Ah and kWh with days of autonomy."""
        total_energy_wh = (self.load_kwh * 1000) * days_of_autonomy
        usable_capacity_wh = total_energy_wh / (depth_of_discharge * battery_efficiency)
        total_battery_ah = usable_capacity_wh / self.system_voltage
        battery_bank_kwh = usable_capacity_wh / 1000.0
        
        print("--- 3. Off-Grid Battery Bank Sizing ---")
        print(f"Days of Autonomy: {days_of_autonomy} days | DoD: {depth_of_discharge * 100}%")
        print(f"Required Battery Bank Energy: {battery_bank_kwh:.2f} kWh")
        print(f"Required Total Amp-Hours (at {self.system_voltage}V): {total_battery_ah:.2f} Ah\n")
        return total_battery_ah, battery_bank_kwh

    def calculate_mppt_string_configuration(self, 
                                          panel_wp, 
                                          panel_vmp, 
                                          panel_voc, 
                                          panel_imp, 
                                          panel_isc, 
                                          mppt_v_min, 
                                          mppt_v_max, 
                                          inverter_max_v_dc, 
                                          target_total_pv_kw):
        """
        Calculates optimal series panels per string and parallel strings count 
        matching inverter MPPT voltage and current windows.
        """
        print("--- 4. MPPT String Configuration & Panel Layout ---")
        
        max_panels_series_voc = int(inverter_max_v_dc / panel_voc)
        target_mppt_voltage = (mppt_v_min + mppt_v_max) / 2.0
        panels_in_series = round(target_mppt_voltage / panel_vmp)
        
        total_string_vmp = panels_in_series * panel_vmp
        total_string_voc = panels_in_series * panel_voc
        
        if total_string_voc > inverter_max_v_dc:
            panels_in_series = max_panels_series_voc
            total_string_vmp = panels_in_series * panel_vmp
            total_string_voc = panels_in_series * panel_voc

        total_panels_needed = math.ceil((target_total_pv_kw * 1000) / panel_wp)
        parallel_strings = math.ceil(total_panels_needed / panels_in_series)
        
        actual_total_panels = panels_in_series * parallel_strings
        actual_total_kw = (actual_total_panels * panel_wp) / 1000.0
        
        print(f"Selected Panel Rating: {panel_wp}W (Vmp: {panel_vmp}V, Voc: {panel_voc}V)")
        print(f"Inverter MPPT Range: {mppt_v_min}V - {mppt_v_max}V (Max DC: {inverter_max_v_dc}V)")
        print(f"Panels in Series per String: {panels_in_series}")
        print(f"Number of Parallel Strings: {parallel_strings}")
        print(f"Total Installed Panels: {actual_total_panels}")
        print(f"Actual Array Peak Power: {actual_total_kw:.2f} kW\n")
        
        return panels_in_series, parallel_strings, actual_total_kw

    def calculate_cable_size(self, length_m, current_amps, conductor_material="copper", allowable_voltage_drop_pct=3.0):
        """Calculates minimum cross-sectional area of a DC cable based on voltage drop."""
        rho = 0.0225 if conductor_material.lower() == "copper" else 0.0360
        max_v_drop = self.system_voltage * (allowable_voltage_drop_pct / 100.0)
        min_area_mm2 = (2 * length_m * current_amps * rho) / max_v_drop
        
        print("--- 5. DC Cable Sizing & Voltage Drop ---")
        print(f"Conductor: {conductor_material.capitalize()} | Length: {length_m}m | Current: {current_amps}A")
        print(f"Minimum Cable Cross-Section: {min_area_mm2:.2f} mm²\n")
        return min_area_mm2


# --- Execution Example ---
if __name__ == "__main__":
    print("=== ULTIMATE SOLAR SYSTEM & MPPT DESIGN TOOL ===\n")
    
    solar_tool = UltimateSolarSystemCalculator(
        load_kwh_per_day=25.0,       # 25 kWh daily load
        peak_sun_hours=5.2,          # 5.2 PSH
        system_voltage=48.0,         # 48V DC battery system
        max_continuous_load_kw=5.0   # 5 kW peak load
    )
    
    # 1. System Sizing & Storage
    pv_cap = solar_tool.estimate_pv_sizing(system_efficiency=0.80)
    inverter_cap = solar_tool.select_inverter_rating(surge_safety_factor=1.25)
    solar_tool.calculate_battery_bank(days_of_autonomy=2, depth_of_discharge=0.80)
    
    # 2. MPPT String Matching (e.g., Jinko 660W N-Type panels)
    solar_tool.calculate_mppt_string_configuration(
        panel_wp=660.0,              
        panel_vmp=38.5,              
        panel_voc=46.2,              
        panel_imp=17.15,             
        panel_isc=18.30,             
        mppt_v_min=120.0,            
        mppt_v_max=500.0,            
        inverter_max_v_dc=550.0,     
        target_total_pv_kw=pv_cap    
    )
    
    # 3. Cable Sizing
    solar_tool.calculate_cable_size(length_m=30.0, current_amps=35.0, conductor_material="copper")
