# task_g_class.py
# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.
#
# Modified by nnn according to given task
#
# Class-based refactor of the original list-based program.
# Behavior and output are preserved.

from __future__ import annotations
from datetime import datetime, date, time
from typing import List


INPUT_FILE = "reservations.txt"


class Reservation:
    def __init__(
        self,
        reservation_id: int,
        name: str,
        email: str,
        phone: str,
        date: date,
        time: time,
        duration: int,
        price: float,
        confirmed: bool,
        resource: str,
        created: datetime,
    ):
        self.reservation_id = reservation_id
        self.name = name
        self.email = email
        self.phone = phone
        self.date = date
        self.time = time
        self.duration = duration
        self.price = price
        self.confirmed = confirmed
        self.resource = resource
        self.created = created

    def is_confirmed(self) -> bool:
        return self.confirmed

    def is_long(self) -> bool:
        return self.duration > 3  # keep original behavior (> 3)

    def total_price(self) -> float:
        return self.duration * self.price


def parse_bool(value: str) -> bool:
    v = value.strip()
    return v == "True" or v.lower() in ("1", "true", "yes", "y", "t")


def parse_date(value: str) -> date:
    return datetime.strptime(value.strip(), "%Y-%m-%d").date()


def parse_time(value: str) -> time:
    return datetime.strptime(value.strip(), "%H:%M").time()


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S")


def convert_reservation_data_to_object(fields: List[str]) -> Reservation:
    return Reservation(
        reservation_id=int(fields[0].strip()),
        name=fields[1].strip(),
        email=fields[2].strip(),
        phone=fields[3].strip(),
        date=parse_date(fields[4]),
        time=parse_time(fields[5]),
        duration=int(fields[6].strip()),
        price=float(fields[7].strip()),
        confirmed=parse_bool(fields[8]),
        resource=fields[9].strip(),
        created=parse_datetime(fields[10]),
    )


def fetch_reservations(path: str = INPUT_FILE) -> List[Reservation]:
    reservations: List[Reservation] = []
    # keep header placeholder to preserve indexing logic parity with original program
    # header will be a dummy Reservation with string fields where appropriate
    reservations.append(
        Reservation(
            reservation_id=0,
            name="name",
            email="email",
            phone="phone",
            date=parse_date("1970-01-01"),
            time=parse_time("00:00"),
            duration=0,
            price=0.0,
            confirmed=False,
            resource="reservedResource",
            created=parse_datetime("1970-01-01 00:00:00"),
        )
    )
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if len(line) > 1:
                parts = line.split("|")
                reservations.append(convert_reservation_data_to_object(parts))
    return reservations


def confirmed_reservations(reservations: List[Reservation]) -> None:
    for r in reservations[1:]:
        if r.is_confirmed():
            print(f'- {r.name}, {r.resource}, {r.date.strftime("%d.%m.%Y")} at {r.time.strftime("%H.%M")}')


def long_reservations(reservations: List[Reservation]) -> None:
    for r in reservations[1:]:
        if r.is_long():
            print(f'- {r.name}, {r.date.strftime("%d.%m.%Y")} at {r.time.strftime("%H.%M")}, duration {r.duration} h, {r.resource}')


def confirmation_statuses(reservations: List[Reservation]) -> None:
    for r in reservations[1:]:
        name: str = r.name
        confirmed: bool = r.confirmed
        print(f'{name} → {"Confirmed" if confirmed else "NOT Confirmed"}')


def confirmation_summary(reservations: List[Reservation]) -> None:
    confirmed_count: int = len([x for x in reservations[1:] if x.confirmed])
    print(f'- Confirmed reservations: {confirmed_count} pcs\n- Not confirmed reservations: {len(reservations) - confirmed_count} pcs')


def total_revenue(reservations: List[Reservation]) -> None:
    revenue: float = sum(x.total_price() for x in reservations[1:] if x.confirmed)
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
