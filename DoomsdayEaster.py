from datetime import datetime, timedelta

def doomsday(y): # Doomsday Algorithm
	k = y // 100 # Century
	d = (5 * (k % 4) + 2) % 7 if y > 1582 else 6 * k % 7 # Century correction
	t = y % 100 # Last 2 digits
	a = t // 12 # How many 12s
	b = t % 12 # Left over after 12s
	c = b // 4 # How many 4s in the left over
	return ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][(a + b + c + d) % 7] # Weekday of doomsday

def gauss(y): # Improved Gaussian Algorithm
	a = y % 19 # Golden Number
	b = y % 4 # Leap Year
	c = y % 7 # Weekday of the year
	k = y // 100 # Century
	p = (13 + 8 * k) // 25 # Lunar correction
	q = k // 4 # Century leap years
	m = (15 + k - p - q) % 30 if y > 1582 else 15 # Lunar constant
	n = (4 + k - q) % 7 if y > 1582 else 6 # Weekday constant
	d = (19 * a + m) % 30 # Paschal Full Moon
	if d == 29 or (d == 28 and a > 10): d -= 1 # Edge cases
	e = (2 * b + 4 * c + 6 * d + n) % 7 # Sunday after that
	march = d + e + 22
	april = d + e - 9
	if march <= 31: return (march, 3)
	else: return (april, 4)
	
def gauss_date(y): # Format Easter date
    day, month = gauss(y)
    if month == 3: return f"{day} March" # March date
    else: return f"{day} April" # April date
 
def Typikon(y): # Typikon Algorithm for finding Julian Easter
	l = (y + 16) % 19 + 1 # Lunar Cycle
	s = (y + 19) % 28 + 1 # Solar Cycle
	f = (11 * l + (3 if l < 17 else 4)) % 30 # Foundation
	m = 47 - f if f < 47 else 77 - f # Paschal Full Moon
	c = (s + s // 4 - 1) % 7 + 1 # Concurrent (weekday of March 24)
	w = (m + c + 3) % 7 # Weekday of Paschal Full Moon
	march = m + 7 - w
	april = m - 24 - w
	if march <= 31: return (march, 3)
	else: return (april, 4)
 
def Typikon_date(y): # Format Julian Easter date, converted into Gregorian calendar
    day, month = Typikon(y)
    date = datetime(y, month, day) + timedelta(days= y//100 - y//400 - 2)
    monthname = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][date.month - 1] # Month name, since January has index 0
    return f"{date.day} {monthname}"     

if __name__ == "__main__": # Testing function
	year = int(input("Enter a year: ")) # Get year from user
	print("Easter date:", gauss_date(year), year) # Print Easter date and year
	if year > 1582: # Gregorian calendar only adopted in 1582
		print("Julian Easter date:", Typikon_date(year), year) # Print Julian Easter date and year
	print("Doomsday:", doomsday(year)) # Print Doomsday