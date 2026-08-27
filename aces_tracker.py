import json
import math
import random
import os

SAVE_FILE = "aces_save.json"

class MercCompany:
    def __init__(self):
        self.sp = 100
        self.unit_a = []
        self.unit_b = []
        self.load_state()

    def load_state(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    data = json.load(f)
                    self.sp = data.get('sp', 100)
                    self.unit_a = data.get('unit_a', [])
                    self.unit_b = data.get('unit_b', [])
            except Exception as e:
                print(f"Error loading save file: {e}")

    def save_state(self):
        data = {
            'sp': self.sp,
            'unit_a': self.unit_a,
            'unit_b': self.unit_b
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def print_roster(self, unit_name, roster):
        print(f"\n--- {unit_name} (Target: 200 PV) ---")
        pv_total = 0
        if not roster:
            print("No pilots assigned.")
        for idx, pilot in enumerate(roster):
            pv = pilot.get('pv', 0)
            pv_total += pv
            print(f"[{idx}] {pilot.get('pilot', 'Unknown')} | Mech: {pilot.get('mech', 'Unknown')} | "
                  f"PV: {pv} | Skill: {pilot.get('skill', 4)} | XP: {pilot.get('xp', 0)} | Status: {pilot.get('status', 'OK')}")
        print(f"Total PV: {pv_total}/200")

    def buy_unit(self, name, pv, unit_choice):
        cost = pv * 40
        if self.sp >= cost:
            self.sp -= cost
            new_unit = {
                "pilot": "Recruit", "mech": name, "pv": pv, 
                "skill": 4, "gunnery": 4, "piloting": 5, 
                "edgeMax": 1, "edgeCurrent": 1, "xp": 0, 
                "abilities": "None", "status": "OK"
            }
            if unit_choice == 'A':
                self.unit_a.append(new_unit)
            else:
                self.unit_b.append(new_unit)
            self.save_state()
            print(f"\nSuccess! Requisitioned {name} for {cost} SP.")
        else:
            print(f"\nInsufficient SP! Cost is {cost}, but you only have {self.sp}.")

    def settle_sortie(self, base_sp, bonus_sp, kills, payout_scale, repair_cost):
        gross_income = math.floor((base_sp + bonus_sp) * payout_scale) + (kills * 5)
        net_sp = gross_income - repair_cost
        self.sp += net_sp
        self.save_state()
        print(f"\n--- Sortie Complete ---")
        print(f"Gross Income: +{gross_income} SP")
        print(f"Repairs/Logistics: -{repair_cost} SP")
        print(f"Net Treasury Change: {net_sp} SP. New Balance: {self.sp} SP")

    def roll_2d6(self):
        return random.randint(1, 6) + random.randint(1, 6)

def main():
    company = MercCompany()
    
    while True:
        print(f"\n=== BATTLETECH ACES TRACKER ===")
        print(f"Current Support Points (SP): {company.sp}")
        print("1. View Company Roster")
        print("2. Requisition New Unit")
        print("3. Settle Post-Sortie Upkeep")
        print("4. Roll Survival / Salvage (2D6)")
        print("5. Quit")
        
        choice = input("Select an option (1-5): ")
        
        if choice == '1':
            company.print_roster("Unit Alpha", company.unit_a)
            company.print_roster("Unit Beta", company.unit_b)
            
        elif choice == '2':
            mech_name = input("Enter Mech/Chassis Name: ")
            try:
                pv = int(input("Enter PV: "))
                unit_choice = input("Assign to Unit A or B? (A/B): ").strip().upper()
                if unit_choice in ['A', 'B']:
                    company.buy_unit(mech_name, pv, unit_choice)
                else:
                    print("Invalid unit choice.")
            except ValueError:
                print("Invalid PV entered. Must be a number.")
                
        elif choice == '3':
            try:
                base = int(input("Base Scenario Reward (e.g., 50 for Decisive Victory): "))
                bonus = int(input("Bonus/Objective SP: "))
                kills = int(input("Enemies Fully Destroyed (Scrap): "))
                scale = float(input("Deployment Payout Scale (1.0 for Full, 0.5 for Co-Op): "))
                repairs = int(input("Total Repair & Medical Costs (in SP): "))
                company.settle_sortie(base, bonus, kills, scale, repairs)
            except ValueError:
                print("Invalid input. Please enter numerical values.")
                
        elif choice == '4':
            roll = company.roll_2d6()
            print(f"\n2D6 Roll Result: {roll}")
            print("Mech Salvage needs 4+ | Vehicle Salvage needs 6+ | Crew Survival: 2-3 (KIA), 4-6 (Wounded), 7+ (OK)")
            
        elif choice == '5':
            print("Shutting down tracker. Data saved.")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
