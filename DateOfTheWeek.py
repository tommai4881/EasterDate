def is_leap_year(year):
    """
    Determines if a year is a leap year.
    Uses Julian rules for years <= 1582 and Gregorian rules for years > 1582.
    """
    if year <= 1582:
        return year % 4 == 0
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_days_in_month(month, year):
    """Return the number of days in a specific month/year."""
    if month == 2:
        return 29 if is_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def date_of_the_week(day, month, year):
    """
    Calculates the day of the week for a given date.
    Handles the transition from Julian to Gregorian calendar in Oct 1582.
    """
    
    # --- 1. VALIDATION ---
    # Check basic ranges
    if not (1 <= month <= 12):
        raise ValueError(f"Month {month} is invalid.")
    
    max_days = get_days_in_month(month, year)
    if not (1 <= day <= max_days):
        raise ValueError(f"Day {day} is not valid for month {month}.")

    # Check for the specific 10 days skipped in history (Oct 5 - Oct 14, 1582)
    if year == 1582 and month == 10 and (5 <= day <= 14):
        raise ValueError("This date does not exist due to the Gregorian calendar switch.")

    # --- 2. CALCULATION TERMS ---
    
    # Term A: Year Component
    year_part = year % 100
    year_term = (year_part + year_part // 4) % 7
    
    # Term B: Month Component (Lookup Table)
    # Jan=0, Feb=3, Mar=3, Apr=6, May=1, Jun=4, Jul=6, Aug=2, Sep=5, Oct=0, Nov=3, Dec=5
    month_offsets = [0, 3, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5]
    month_term = month_offsets[month - 1]

    # Term C: Century/History Component
    # Post-1582 (Gregorian)
    if year > 1582 or (year == 1582 and (month > 10 or (month == 10 and day >= 15))):
        century_term = [6, 4, 2, 0][(year // 100) % 4]
        
    # Pre-1582 (Julian)
    elif year < 1582 or (year == 1582 and (month < 10 or (month == 10 and day <= 4))):
        century_term = (18 - year // 100) % 7
        
    # This else should theoretically never be reached because of the validation above,
    # but kept for logic parity.
    else:
        raise ValueError("This day is not valid!")

    # Term L: Leap Year Adjustment
    # If it's a leap year and we are in Jan or Feb, we must subtract 1
    leap_adjustment = 1 if is_leap_year(year) and month < 3 else 0

    # --- 3. FINAL RESULT ---
    total = year_term + month_term + century_term + day - leap_adjustment
    weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    return weekdays[total % 7]

if __name__ == "__main__":
    d = int(input("Enter the day: "))
    m = int(input("Enter the month: "))
    y = int(input("Enter the year: "))
    print(f"Date: {["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][m-1]} {d}, {y}")
    print(f"Date of the week: {date_of_the_week(d, m, y)}")