# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by nnn according to given task

"""
A program that reads reservation data from a file
and prints them to the console using functions:

Reservation number: 123
Booker: Anna Virtanen
Date: 31.10.2025
Start time: 10.00
Number of hours: 2
Hourly rate: 19,95 €
Total price: 39,90 €
Paid: Yes
Venue: Meeting Room A
Phone: 0401234567
Email: anna.virtanen@example.com

"""
from datetime import datetime

def print_reservation_number(reservation: list) -> None: 
    print(f"Reservation number: {reservation[0]}")

def print_booker(reservation: list) -> None:
    """
    Prints the reservation number

    Parameters:
     reservation (lst): reservation -> columns separated by |
    """
    booker = reservation[1]
    print(f"Booker: {booker}")
    

def print_date(reservation: list) -> None:
    date_str = reservation[2]
    day = datetime.strptime(date_str, "%Y-%m-%d").date()
    print(f"Date: {day.strftime('%d.%m.%Y')}")

def print_start_time(reservation: list) -> None:
    time_str = reservation[3]
    t = datetime.strptime(time_str, "%H:%M").time()
    print(f"Start time: {t.strftime('%H.%M')}")

def print_hours(reservation: list) -> None:
    print(f"Number of hours: {reservation[4]}")

def print_hourly_rate(reservation: list) -> None:
    rate = float(reservation[5])
    print(f"Hourly rate: {rate:.2f}".replace('.', ',') + " €")

def print_total_price(reservation: list) -> None:
    hours = int(reservation[4])
    rate = float(reservation[5])
    total = hours * rate
    print(f"Total price: {total:.2f}".replace('.', ',') + " €")

def print_paid(reservation: list) -> None:
    paid = reservation[6] == "True"
    print(f"Paid: {'Yes' if paid else 'No'}")

def print_venue(reservation: list) -> None:
    print(f"Venue: {reservation[7]}")

def print_phone(reservation: list) -> None:
    print(f"Phone: {reservation[8]}")

def print_email(reservation: list) -> None:
    print(f"Email: {reservation[9]}")


def main():
    """
    Reads reservation data from a file and
    prints them to the console using functions
    """
    # Define the file name directly in the code
    reservations = "reservations.txt"

    # Open the file, read it, and split the contents
    with open(reservations, "r", encoding="utf-8") as f:
        reservation = f.read().strip()
        reservation = reservation.split('|')

    # Implement the remaining parts following
    # the function print_booker(reservation)
    
    # The functions to be created should perform type conversions
    # and print according to the sample output

    print_reservation_number(reservation)
    print_booker(reservation)
    print_date(reservation)
    print_start_time(reservation)
    print_hours(reservation)
    print_hourly_rate(reservation)
    print_total_price(reservation)
    print_paid(reservation)
    print_venue(reservation)
    print_phone(reservation)
    print_email(reservation)

if __name__ == "__main__":
    main()