# Copyright (c) 2026 Prabesh Shrestha 
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by nnn according to given task

"""
A program that prints reservation information according to task requirements

The data structure and example data record:

reservationId | name | email | phone | reservationDate | reservationTime | durationHours | price | confirmed | reservedResource | createdAt
------------------------------------------------------------------------
201 | Moomin Valley | moomin@whitevalley.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Forest Area 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime

"""

from datetime import datetime

HEADERS = [
    "reservationId",
    "name",
    "email",
    "phone",
    "reservationDate",
    "reservationTime",
    "durationHours",
    "price",
    "confirmed",
    "reservedResource",
    "createdAt",
]


def convert_reservation_data(reservation: list) -> list:
    """
    Convert data types to meet program requirements

    Parameters:
     reservation (list): Unconverted reservation -> 11 columns

    Returns:
     converted (list): Converted data types
    """
    converted = []
    # Convert the first element = reservation[0]
    converted.append(int(reservation[0]))  # reservationId (str -> int)
    # And continue from here
    converted.append(reservation[1])  # name (str)
    
    converted.append(reservation[2])  # email (str)
    
    converted.append(reservation[3])  # phone (str)
    
    reservation_date = datetime.strptime(reservation[4], "%Y-%m-%d").date()
    converted.append(reservation_date)  # reservationDate (date)
    
    time_str = reservation[5].strip() 
    if len(time_str) == 5: # HH:MM 
        reservation_time = datetime.strptime(time_str, "%H:%M").time() 
    else: # HH:MM:SS 
         reservation_time = datetime.strptime(time_str, "%H:%M:%S").time() 
    converted.append(reservation_time) # reservationTime (time)
         
    converted.append(int(reservation[6]))  # durationHours (int)
    
    converted.append(float(reservation[7]))  # price (float)
    
    converted.append(reservation[8].strip() == "True")# confirmed (bool)
    
    converted.append(reservation[9])  # reservedResource (str)
    
    created_at = datetime.strptime(reservation[10].strip(), "%Y-%m-%d %H:%M:%S") 
    converted.append(created_at)# createdAt (datetime)
    
    return converted


def fetch_reservations(reservation_file: str) -> list:
    """
    Reads reservations from a file and returns the reservations converted
    You don't need to modify this function!

    Parameters:
     reservation_file (str): Name of the file containing the reservations

    Returns:
     reservations (list): Read and converted reservations
    """
    reservations = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            fields = line.split("|")
            reservations.append(convert_reservation_data(fields))
    return reservations


def confirmed_reservations(reservations: list[list]) -> None:
    for r in reservations:
        if r[8]:  # confirmed
            date_str = r[4].strftime("%d.%m.%Y")
            time_str = r[5].strftime("%H.%M")
            print(f"- {r[1]}, {r[9]}, {date_str} at {time_str}")


def long_reservations(reservations: list[list]) -> None:
    """
    Print long reservations

    Parameters:
     reservations (list): Reservations
    """
    for r in reservations:
        if r[6] >= 3:
            date_str = r[4].strftime("%d.%m.%Y")
            time_str = r[5].strftime("%H.%M")
            print(f"- {r[1]}, {date_str} at {time_str}, duration {r[6]} h, {r[9]}")



def confirmation_statuses(reservations: list[list]) -> None:
    """
    Print confirmation statuses

    Parameters:
     reservations (list): Reservations
    """
    for r in reservations: 
        print(r[1], "->", "Confirmed"
              if r[8] 
              else "NOT confirmed")


def confirmation_summary(reservations: list[list]) -> None:
    """
    Print confirmation summary

    Parameters:
     reservations (list): Reservations
    """
    confirmed = sum(1 for r in reservations if r[8])
    unconfirmed = len(reservations) - confirmed
    print("Confirmed:", confirmed)
    print("Not confirmed:", unconfirmed)


def total_revenue(reservations: list[list]) -> None:
    """
    Print total revenue

    Parameters:
     reservations (list): Reservations
    """
    total = sum(r[6] * r[7] for r in reservations if r[8])
    print("Total revenue:", total)


def main(): 
    reservations = fetch_reservations("reservations.txt")

    """
    Prints reservation information according to requirements
    Reservation-specific printing is done in functions
    
    # PART A -> Before continuing to part B, make sure that the following lines
    # print all the reservation data and the correct data types to the console. 
    # After that, you can remove this section or comment it out up to part B.
    print(" | ".join(HEADERS))
    print("------------------------------------------------------------------------")
    for reservation in reservations:
        print(" | ".join(str(x) for x in reservation))
        data_types = [type(x).__name__ for x in reservation]
        print(" | ".join(data_types))
        print(
            "------------------------------------------------------------------------"
        )
    """

    # PART B -> Build the output required in part B from this using
    # the predefined functions and the necessary print statements.

    print("1) Confirmed Reservations") 
    confirmed_reservations(reservations)
    print()
    
    print("2) Long Reservations")
    long_reservations(reservations)
    print()
    
    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print()
    
    print("4) Confirmation Summary")
    confirmation_summary(reservations)
    print()
    
    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)
    print()


if __name__ == "__main__":
    main()
