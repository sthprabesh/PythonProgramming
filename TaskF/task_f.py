import csv
from datetime import datetime, timedelta
from typing import List, Dict, Any

CSV_FILE = "2025.csv"
REPORT_FILE = "report.txt"

def format_number(value: float) -> str:
    """Two decimals, comma as decimal separator."""
    return f"{value:.2f}".replace(".", ",")

def parse_timestamp(s: str) -> datetime:
    """Parse ISO timestamps (ms + offset) or common formats; return naive datetime."""
    s = s.strip()
    # try direct ISO (handles 2025-01-01T00:00:00.000+02:00)
    try:
        ts = datetime.fromisoformat(s)
    except Exception:
        ts = None

    if ts is None:
        s2 = s.replace("T", " ")
        formats = [
            "%Y-%m-%d %H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%d.%m.%Y %H:%M:%S",
            "%d.%m.%Y"
        ]
        for fmt in formats:
            try:
                ts = datetime.strptime(s2, fmt)
                break
            except Exception:
                continue

    if ts is None:
        raise ValueError(f"Unknown date format: {s}")

    # If timestamp has tzinfo, convert to local time and drop tzinfo (make naive)
    if ts.tzinfo is not None:
        ts = ts.astimezone().replace(tzinfo=None)

    return ts

def detect_delimiter(sample: str) -> str:
    """Return ';' if present, else ','. """
    if ";" in sample and sample.count(";") >= sample.count(","):
        return ";"
    return ","

def read_data(filename: str) -> List[Dict[str, Any]]:
    """Reads CSV, convert comma decimals, return list of rows."""
    rows: List[Dict[str, Any]] = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            header = f.readline()
            if not header:
                return rows
            delim = detect_delimiter(header)
            f.seek(0)
            reader = csv.reader(f, delimiter=delim)
            next(reader, None)  # skip header if present
            for r in reader:
                if not r or len(r) < 4:
                    continue
                try:
                    ts = parse_timestamp(r[0])
                    # numbers use comma as decimal separator -> replace before float
                    cons = float(r[1].replace(",", "."))
                    prod = float(r[2].replace(",", "."))
                    temp = float(r[3].replace(",", "."))
                    rows.append({"ts": ts, "cons": cons, "prod": prod, "temp": temp})
                except Exception:
                    continue
    except FileNotFoundError:
        return rows
    return rows

def calc_range(data: List[Dict[str, Any]], start: datetime, end: datetime) -> Dict[str, float]:
    """Sums consumption, production and average temperature for inclusive range."""
    end = end.replace(hour=23, minute=59, second=59)
    total_cons = 0.0
    total_prod = 0.0
    temp_sum = 0.0
    count = 0
    for row in data:
        ts = row["ts"]
        if start <= ts <= end:
            total_cons += row["cons"]
            total_prod += row["prod"]
            temp_sum += row["temp"]
            count += 1
    avg_temp = (temp_sum / count) if count else 0.0
    return {"cons": total_cons, "prod": total_prod, "avg_temp": avg_temp}

def create_daily_report(data: List[Dict[str, Any]]) -> List[str]:
    """Builds daily report for a date range (input dd.mm.yyyy)."""
    s = input("Enter start date (dd.mm.yyyy): ").strip()
    e = input("Enter end date (dd.mm.yyyy): ").strip()
    try:
        start = datetime.strptime(s, "%d.%m.%Y")
        end = datetime.strptime(e, "%d.%m.%Y")
    except ValueError:
        print("Invalid date format. Use dd.mm.yyyy.")
        return []
    stats = calc_range(data, start, end)
    lines: List[str] = []
    lines.append("-----------------------------------------------------")
    lines.append(f"Report for the period {start.strftime('%d.%m.%Y')}–{end.strftime('%d.%m.%Y')}")
    lines.append(f"- Total consumption: {format_number(stats['cons'])} kWh")
    lines.append(f"- Total production: {format_number(stats['prod'])} kWh")
    lines.append(f"- Average temperature: {format_number(stats['avg_temp'])} °C")
    return lines

def create_monthly_report(data: List[Dict[str, Any]]) -> List[str]:
    """Builds monthly summary for chosen month (1-12)."""
    m = input("Enter month number (1–12): ").strip()
    try:
        month = int(m)
        if month < 1 or month > 12:
            print("Invalid month number.")
            return []
    except ValueError:
        print("Invalid input.")
        return []
    year = 2025
    start = datetime(year, month, 1)
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    end = next_month - timedelta(days=1)
    stats = calc_range(data, start, end)
    month_name = start.strftime("%B")
    lines: List[str] = []
    lines.append("-----------------------------------------------------")
    lines.append(f"Report for the month: {month_name}")
    lines.append(f"- Total consumption: {format_number(stats['cons'])} kWh")
    lines.append(f"- Total production: {format_number(stats['prod'])} kWh")
    lines.append(f"- Average temperature: {format_number(stats['avg_temp'])} °C")
    return lines

def create_yearly_report(data: List[Dict[str, Any]]) -> List[str]:
    """Builds full-year 2025 summary."""
    start = datetime(2025, 1, 1)
    end = datetime(2025, 12, 31)
    stats = calc_range(data, start, end)
    lines: List[str] = []
    lines.append("-----------------------------------------------------")
    lines.append("Report for the year: 2025")
    lines.append(f"- Total consumption: {format_number(stats['cons'])} kWh")
    lines.append(f"- Total production: {format_number(stats['prod'])} kWh")
    lines.append(f"- Average temperature: {format_number(stats['avg_temp'])} °C")
    return lines

def print_report_to_console(lines: List[str]) -> None:
    """Prints report lines to console."""
    if not lines:
        return
    for line in lines:
        print(line)

def write_report_to_file(lines: List[str]) -> None:
    """Writes report to report.txt (overwrite)."""
    if not lines:
        print("No report content to save.")
        return
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"Report written to {REPORT_FILE}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def show_main_menu() -> str:
    """Shows main menu and return choice."""
    print("\n--- Energy Report Menu ---")
    print("1) Daily summary for a date range")
    print("2) Monthly summary for one month")
    print("3) Full year 2025 summary")
    print("4) Exit the program")
    return input("Select an option (1-4): ").strip()

def post_report_menu() -> str:
    """Shows post-report menu and return choice."""
    print("\nWhat would you like to do next?")
    print("1) Write the report to the file report.txt")
    print("2) Create a new report")
    print("3) Exit")
    return input("Select an option (1-3): ").strip()

def main() -> None:
    """Main: read data, loop menus, generate and save reports."""
    print(f"Reading data from {CSV_FILE}...")
    data = read_data(CSV_FILE)
    if not data:
        print("No data loaded. Check 2025.csv.")
    else:
        print(f"Loaded {len(data)} rows.")
    while True:
        choice = show_main_menu()
        report_lines: List[str] = []
        if choice == "1":
            report_lines = create_daily_report(data)
        elif choice == "2":
            report_lines = create_monthly_report(data)
        elif choice == "3":
            report_lines = create_yearly_report(data)
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid selection.")
            continue

        if not report_lines:
            continue

        print_report_to_console(report_lines)

        while True:
            action = post_report_menu()
            if action == "1":
                write_report_to_file(report_lines)
                continue
            elif action == "2":
                break
            elif action == "3":
                print("Exiting program.")
                return
            else:
                print("Invalid selection.")

if __name__ == "__main__":
    main()
