# task_g_dict.py
# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.
#
# Modified by Prabesh Shrestha Bata according to given task
#
# Dictionary-based refactor of the original list-based program.
# Behavior and output are preserved.

from __future__ import annotations
from datetime import datetime, date, time
from typing import List, Dict


INPUT_FILE = "reservations.txt"


def parse_bool(value: str) -> bool:
    v = value.strip()
    return v == "True" or v.lower() in ("1", "true", "yes", "y", "t")


def parse_date(value: str) -> date:
    return datetime.strptime(value.strip(), "%Y-%m-%d").date()


def parse_time(value: str) -> time:
    return datetime.strptime(value.strip(), "%H:%M").time()


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S")


def convert_reservation_data_to_dict(fields: List[str]) -> Dict:
    """
    Convert a list of 11 string fields into a dictionary with proper types.
    Field order expected:
    0: reservationId, 1: name, 2: email, 3: phone,
    4: reservationDate (YYYY-MM-DD), 5: reservationTime (HH:MM),
    6: durationHours, 7: price, 8: confirmed, 9: reservedResource, 10: createdAt (YYYY-MM-DD HH:MM:SS)
    """
    return {
        "id": int(fields[0].strip()),
        "name": fields[1].strip(),
        "email": fields[2].strip(),
        "phone": fields[3].strip(),
        "date": parse_date(fields[4]),
        "time": parse_time(fields[5]),
        "duration": int(fields[6].strip()),
        "price": float(fields[7].strip()),
        "confirmed": parse_bool(fields[8]),
        "resource": fields[9].strip(),
        "created": parse_datetime(fields[10]),
    }


def fetch_reservations(path: str = INPUT_FILE) -> List[Dict]:
    """
    Read reservations.txt and return a list of reservation dictionaries.
    The first line in the file is treated as header and skipped.
    """
    reservations: List[Dict] = []
    # Add header as in original program (kept for parity with original fetch_reservations)
    reservations.append(
        {
            "id": "reservationId",
            "name": "name",
            "email": "email",
            "phone": "phone",
            "date": "reservationDate",
            "time": "reservationTime",
            "duration": "durationHours",
            "price": "price",
            "confirmed": "confirmed",
            "resource": "reservedResource",
            "created": "createdAt",
        }
    )
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if len(line) > 1:
                parts = line.split("|")
                # convert and append
                reservations.append(convert_reservation_data_to_dict(parts))
    return reservations


def confirmed_reservations(reservations: List[Dict]) -> None:
    for r in reservations[1:]:
        if r["confirmed"]:
            print(f'- {r["name"]}, {r["resource"]}, {r["date"].strftime("%d.%m.%Y")} at {r["time"].strftime("%H.%M")}')


def long_reservations(reservations: List[Dict]) -> None:
    for r in reservations[1:]:
        # original used > 3
        if r["duration"] > 3:
            print(f'- {r["name"]}, {r["date"].strftime("%d.%m.%Y")} at {r["time"].strftime("%H.%M")}, duration {r["duration"]} h, {r["resource"]}')


def confirmation_statuses(reservations: List[Dict]) -> None:
    for r in reservations[1:]:
        name: str = r["name"]
        confirmed: bool = r["confirmed"]
        print(f'{name} → {"Confirmed" if confirmed else "NOT Confirmed"}')


def confirmation_summary(reservations: List[Dict]) -> None:
    confirmed_count: int = len([x for x in reservations[1:] if x["confirmed"]])
    print(f'- Confirmed reservations: {confirmed_count} pcs\n- Not confirmed reservations: {len(reservations) - confirmed_count} pcs')


def total_revenue(reservations: List[Dict]) -> None:
    revenue: float = sum(x["duration"] * x["price"] for x in reservations[1:] if x["confirmed"])
    # keep the same formatting as original (comma as decimal separator)
    print(f'Total revenue from confirmed reservations: {revenue:.2f} €'.replace('.', ','))


def main() -> None:
    reservations = fetch_reservations(INPUT_FILE)
    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)
    print("2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)
    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print("4) Confirmation Summary")
    confirmation_summary(reservations)
    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)


if __name__ == "__main__":
    main()
