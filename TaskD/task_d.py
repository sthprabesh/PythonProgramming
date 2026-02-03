# Copyright (c) 2026 Prabesh Shrestha 
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by nnn according to given task


from datetime import datetime, date
import csv

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",    
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

def convert_data(line: list) -> list:
    """
    Convert data types to meet program requirements.

    Parameters:
        line (list): Unconverted line -> 7 columns

    Returns:
        converted (list): Converted data types
    """
    converted = []

    # 1. timestamp
    converted.append(datetime.fromisoformat(line[0]))

    # 2–7. six numeric values (Wh)
    converted.append(int(line[1]))  # consumption phase 1
    converted.append(int(line[2]))  # consumption phase 2
    converted.append(int(line[3]))  # consumption phase 3
    converted.append(int(line[4]))  # production phase 1
    converted.append(int(line[5]))  # production phase 2
    converted.append(int(line[6]))  # production phase 3

    return converted



def read_data(filename: str) -> list:
    """
    Reads the CSV file and returns the rows in a suitable structure.

    Parameters:
        filename (str): Name of the file containing the electricity data

    Returns:
        list: Parsed consumption and production rows
    """
    consumption_and_production = []

    with open(filename, "r", encoding="utf-8") as f:
        next(f)
        for line in f:
            line = line.strip()
            fields = line.split(";")
            consumption_and_production.append(convert_data(fields))

    return consumption_and_production


def day_information(day: date, database: list) -> str:
    """
    Create printable string for a given day.
s
    Parameters:
        day (date): Reportable day
        database (list): Consumption and production data + dates

    Returns:
        Printable string
    """
    consumption_phase1 = 0
    consumption_phase2 = 0
    consumption_phase3 = 0
    production_phase1 = 0
    production_phase2 = 0
    production_phase3 = 0
    for per_hour in database:
        if per_hour[0].date() == day:
            consumption_phase1 += per_hour[1]/1000
            consumption_phase2 += per_hour[2]/1000
            consumption_phase3 += per_hour[3]/1000
            production_phase1 += per_hour[4]/1000
            production_phase2 += per_hour[5]/1000
            production_phase3 += per_hour[6]/1000
            
            
    cp1 =f"{consumption_phase1:.2f}".replace(".", ",")
    cp2 =f"{consumption_phase2:.2f}".replace(".", ",")
    cp3 =f"{consumption_phase3:.2f}".replace(".", ",")  
    pp1 =f"{production_phase1:.2f}".replace(".", ",")
    pp2 =f"{production_phase2:.2f}".replace(".", ",")
    pp3 =f"{production_phase3:.2f}".replace(".", ",")

    return f'{day.strftime("%d.%m.%Y"):<15}'+ f"{cp1:<8}" + f"{cp2:<8}" + f"{cp3:<13}" + f"{pp1:<8}" + f"{pp2:<8}" + f"{pp3:<8}"


def main() -> None:
    """
    Main function: reads data, computes daily totals, and prints the report.
    """
    db = read_data("week42.csv")

    print("Week 42 electricity consumption and production (kWh, by phase)", end="\n\n")
    print("Day         Date            Consumption [kWh]             Production [kWh]")
    print("          (dd.mm.yyyy)     v1     v2     v3              v1      v2     v3")
    print("-----------------------------------------------------------------------------")

    print(f"{DAYS[0]:<10}", day_information(date(2025, 10, 13), db))
    print(f"{DAYS[1]:<10}", day_information(date(2025, 10, 14), db))
    print(f"{DAYS[2]:<10}", day_information(date(2025, 10, 15), db))
    print(f"{DAYS[3]:<10}", day_information(date(2025, 10, 16), db))
    print(f"{DAYS[4]:<10}", day_information(date(2025, 10, 17), db))
    print(f"{DAYS[5]:<10}", day_information(date(2025, 10, 18), db))
    print(f"{DAYS[6]:<10}", day_information(date(2025, 10, 19), db))


if __name__ == "__main__":
    main()
