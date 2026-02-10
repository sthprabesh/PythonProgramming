# Copyright (c) 2026 Prabesh Shrestha 
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
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
    """Convert one CSV row into correct data types."""
    converted = []
    converted.append(datetime.fromisoformat(line[0]))  # timestamp
    converted.append(int(line[1]))
    converted.append(int(line[2]))
    converted.append(int(line[3]))
    converted.append(int(line[4]))
    converted.append(int(line[5]))
    converted.append(int(line[6]))
    return converted


def read_data(filename: str) -> list:
    """Read CSV file and return converted rows."""
    rows = []
    with open(filename, "r", encoding="utf-8") as f:
        next(f)
        for line in f:
            fields = line.strip().split(";")
            rows.append(convert_data(fields))
    return rows


def day_information(day: date, database: list) -> str:
    """Return formatted daily totals for one date."""
    c1 = c2 = c3 = 0
    p1 = p2 = p3 = 0

    for per_hour in database:
        if per_hour[0].date() == day:
            c1 += per_hour[1] / 1000
            c2 += per_hour[2] / 1000
            c3 += per_hour[3] / 1000
            p1 += per_hour[4] / 1000
            p2 += per_hour[5] / 1000
            p3 += per_hour[6] / 1000

    # format numbers
    f1 = f"{c1:.2f}".replace(".", ",")
    f2 = f"{c2:.2f}".replace(".", ",")
    f3 = f"{c3:.2f}".replace(".", ",")
    g1 = f"{p1:.2f}".replace(".", ",")
    g2 = f"{p2:.2f}".replace(".", ",")
    g3 = f"{p3:.2f}".replace(".", ",")

    return f'{day.strftime("%d.%m.%Y"):<15}{f1:<8}{f2:<8}{f3:<13}{g1:<8}{g2:<8}{g3:<8}'


def write_week(week_number: int, database: list, file):
    """Write one week's report section."""
    file.write(f"Week {week_number} electricity consumption and production (kWh, by phase)\n\n")
    file.write("Day         Date            Consumption [kWh]             Production [kWh]\n")
    file.write("          (dd.mm.yyyy)     v1     v2     v3              v1      v2     v3\n")
    file.write("-----------------------------------------------------------------------------\n")

    # all dates in this week
    all_dates = sorted({row[0].date() for row in database})

    for d in all_dates:
        weekday = DAYS[d.weekday()]
        file.write(f"{weekday:<10} {day_information(d, database)}\n")

    file.write("\n\n")

def total_summary(week41: list, week42: list, week43: list) -> str:
    """Return total consumption and production for all weeks."""
    c1 = c2 = c3 = 0
    p1 = p2 = p3 = 0

    for db in (week41, week42, week43):
        for row in db:
            c1 += row[1] / 1000
            c2 += row[2] / 1000
            c3 += row[3] / 1000
            p1 += row[4] / 1000
            p2 += row[5] / 1000
            p3 += row[6] / 1000

    # format
    f = lambda x: f"{x:.2f}".replace(".", ",")

    return (
        f"Total consumption and production (Weeks 41–43)\n"
        f"Consumption:  v1 {f(c1)}  v2 {f(c2)}  v3 {f(c3)}\n"
        f"Production:   v1 {f(p1)}  v2 {f(p2)}  v3 {f(p3)}\n"
    )


def main() -> None:
    """Read 3 weeks and write summary.txt."""
    week41 = read_data("week41.csv")
    week42 = read_data("week42.csv")
    week43 = read_data("week43.csv")

    with open("summary.txt", "w", encoding="utf-8") as f:
        write_week(41, week41, f)
        write_week(42, week42, f)
        write_week(43, week43, f)
        
        #combined totals for all weeks
        f.write(total_summary(week41, week42, week43))


if __name__ == "__main__":
    main()
