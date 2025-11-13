# Table of Calculating Easter Date

## Table of Paschal Full Moon

|Epact|PFM     |DL|Julian|1900-2199|1700-1899|1583-1699|2200-2299|
|-----|--------|--|------|---------|---------|---------|---------|
|   23|21 March|C |16    |––       |14       | 3       | 6       |
|   22|22      |D | 5    |14       | 3       |––       |––       |
|   21|23      |E |––    | 3       |––       |11       |14       |
|   20|24      |F |13    |––       |11       |––       | 3       |
|   19|25      |G | 2    |11       |––       |19       |––       |
|   18|26      |A |––    |––       |19       | 8       |11       |
|   17|27      |B |10    |19       | 8       |––       |––       |
|   16|28      |C |––    | 8       |––       |16       |19       |
|   15|29      |D |18    |––       |16       | 5       | 8       |
|   14|30      |E | 7    |16       | 5       |––       |––       |
|   13|31      |F |––    | 5       |––       |13       |16       |
|   12| 1 April|G |15    |––       |13       | 2       | 5       |
|   11| 2      |A | 4    |13       | 2       |––       |––       |
|   10| 3      |B |––    | 2       |––       |10       |13       |
|    9| 4      |C |12    |––       |10       |––       | 2       |
|    8| 5      |D | 1    |10       |––       |18       |––       |
|    7| 6      |E |––    |––       |18       | 7       |10       |
|    6| 7      |F | 9    |18       | 7       |––       |––       |
|    5| 8      |G |––    | 7       |––       |15       |18       |
|    4| 9      |A |17    |––       |15       | 4       | 7       |
|    3|10      |B | 6    |15       | 4       |––       |––       |
|    2|11      |C |––    | 4       |––       |12       |15       |
|    1|12      |D |14    |––       |12       | 1       | 4       |
|   \*|13      |E | 3    |12       | 1       |––       |––       |
|   29|14      |F |––    | 1       |––       | 9       |12       |
|   28|15      |G |11    |––       | 9       |––       | 1       |
|   27|16      |A |––    | 9       |––       |17       |––       |
|25 26|17      |B |19    |17       |17       | 6       | 9       |
|24 25|18      |C | 8    | 6       | 6       |14       |17       |

**Note:**

- For epact 25, the Paschal Full Moon date in case of Golden Numbers 1\~11 is 18 April, else 17 April for the last 8 Golden Numbers (12\~19).
- The Golden Number is calculated as `y % 19 + 1`.
- Easter is the Sunday after the Paschal Full Moon!

|Year DL  |A |B |C |D |E |F |G |Doomsday     |
|---------|--|--|--|--|--|--|--|-------------|
|A        |+7|+6|+5|+4|+3|+2|+1|Tuesday (2)  |
|B        |+1|+7|+6|+5|+4|+3|+2|Monday (1)   |
|C        |+2|+1|+7|+6|+5|+4|+3|Sunday (0)   |
|D        |+3|+2|+1|+7|+6|+5|+4|Saturday (6) |
|E        |+4|+3|+2|+1|+7|+6|+5|Friday (5)   |
|F        |+5|+4|+3|+2|+1|+7|+6|Thursday (4) |
|G        |+6|+5|+4|+3|+2|+1|+7|Wednesday (3)|

### HOW TO CALCULATE DOOMSDAY

```python
def doomsday(y):
	k = y // 100 # Century
	d = (5 * (k % 4) + 2) % 7 if y > 1582 else 6 * k % 7 # Century correction
	t = y % 100 # Last 2 digits
	a = t // 12 # How many 12s
	b = t % 12 # Left over after 12s
	c = b // 4 # How many 4s in the left over
	return (a + b + c + d) % 7 # Weekday of doomsday
	# Sunday (0), Monday (1), Tuesday (2), Wednesday (3), Thursday (4), Friday (5), Saturday (6)

def weekday_doomsday(y):
	return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][doomsday(y)]
```

The doomsday value is found on the rightmost column of the above table.

## Gaussian Algorithm to find Easter

This algorithm (by Carl Friedrich Gauss) works for both Julian and Gregorian calendar (Gregorian Easter from 1583 on, but Julian one is before 1583, since Gregorian Calendar was introduced on 15 October 1582).

```python
def gauss(y):
	a = y % 19 # Golden Number
	b = y % 4 # Leap Year
	c = y % 7 
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
	if march <= 31: return f"{march} March"
	else: return f"{april} April"
```

## Traditional algorithms to find Easter

### Clavian Easter algorithm (1581)

Based on Christopher Clavius' Easter tables. Works for Gregorian calendar for finding Easter after 1582.

```python
def clavian(y):
	g = y % 19 + 1 # Golden Number
	f = 11 * g % 30 # Foundation
	k = y // 100
	s = 3 * (k - 15) // 4 # Solar Correction
	l = 8 * (k - 14) // 25 # Lunar Correction
	e = (f - 10 - s + k) % 30 # Epact
	# Paschal Full Moon
	if e not in [24, 25]:	
		m = 44 - e if e < 24 else 74 - e
	# The 24th and 25th epacts have special cases
	elif e == 24: m = 49 # Epact 24 is 18 April
	elif e == 25: m = 48 if g > 11 else 49
	# Epact 25 is 18 April for Golden Numbers 1~11, else 17 April for the last 8 Golden Numbers (12~19)
	c = k - k //4 - 2 # Century Correction
	w = (y + y // 4 - c + m) % 7 # Weekday of Paschal Full Moon
	march = m + 7 - w
	april = m - 24 - w
	if march <= 31: return f"{march} March"
	else: return f"{april} April"
```

### Typikon Julian algorithm (325)

Based on the algorithm from the *Typikon*, an Orthodox Christian liturgical book. Works for Julian calendar for finding Easter before 1583, as well as Orthodox Julian Easter after 1582.

```python
def typikon(y):
	l = (y + 16) % 19 + 1 # Lunar Cycle
	s = (y + 19) % 28 + 1 # Solar Cycle
	f = (11 * l + (3 if l < 17 else 4)) % 30 # Foundation
	m = 47 - f if f < 47 else 77 - f # Paschal Full Moon
	c = (s + s // 4 - 1) % 7 + 1 # Concurrent (weekday of March 24)
	# Sunday (1), Monday (2), Tuesday (3), Wednesday (4), Thursday (5), Friday (6), Saturday (7)
	w = (m + c + 3) % 7 # Weekday of Paschal Full Moon
	# Sunday (0), Monday (1), Tuesday (2), Wednesday (3), Thursday (4), Friday (5), Saturday (6)
	march = m + 7 - w
	april = m - 24 - w
	if march <= 31: return f"{march} March"
	else: return f"{april} April"
```

## Russian Boundary Key for Dates of Easter

|Easter Sunday|DL|Boundary Key|Letter name|
|-------------|--|------------|-----------|
|22 March     |D |А           |Az (A) |
|23           |E |Б           |Buky (Be)|
|24           |F |В           |Vedi (Ve)|
|25           |G |Г           |Glagol (Ge)|
|26           |A |Д           |Dobro (De)|
|27           |B |Е           |Jest' (Je)|
|28           |C |Ж           |Živete (Že)|
|29           |D |Ѕ           |Dzelo  (Dze)|
|30           |E |З           |Zemlja (Ze)|
|31           |F |И           |Iže (I)|
| 1 April     |G |І           |I Desjateričnoje|
| 2           |A |К           |Kako (Ka)|
| 3           |B |Л           |Ljudi (El)|
| 4           |C |М           |Myslete (Em)|
| 5           |D |Н           |Naš (En)|
| 6           |E |О           |On (O)|
| 7           |F |П           |Pokoj (Pe)|
| 8           |G |Р           |Rcy (Er)|
| 9           |A |С           |Slovo (Es)|
|10           |B |Т           |Tverdo (Te)|
|11           |C |У           |Uk (U)|
|12           |D |Ф           |Fert (Ef)|
|13           |E |Х           |Her (Ha)|
|14           |F |Ѿ           |Ot|
|15           |G |Ц           |Cy (Ce)|
|16           |A |Ч           |Červ' (Če)|
|17           |B |Ш           |Ša|
|18           |C |Щ           |Šča|
|19           |D |Ъ           |Jer (Tvjordyj Znak)|
|20           |E |Ы           |Jery (Y)|
|21           |F |Ь           |Jer' (Mjagkij Znak)|
|22           |G |Ѣ           |Jat|
|23           |A |Ю           |Ju|
|24           |B |Ѫ           |Jus Bol'šoj|
|25           |C |Ѧ           |Ja (Jus Malyj)|

## Easter dates for 2015 - 2029

|Year|Easter Sunday|Julian (Julian Calendar)|Julian in Gregorian (Gregorian Calendar)|
|----|-------------|------------------------|----------------------------------------|
|2015|5 April      |30 March                |12 April                                |
|2016|27 March     |18 April                |1 May                                   |
|2017|16 April     |3 April                 |16 April                                |
|2018|1 April      |26 March                |8 April                                 |
|2019|21 April     |15 April                |28 April                                |
|2020|12 April     |6 April                 |19 April                                |
|2021|4 April      |19 April                |2 May                                   |
|2022|17 April     |11 April                |24 April                                |
|2023|9 April      |3 April                 |16 April                                |
|2024|31 March     |22 April                |5 May                                   |
|2025|20 April     |7 April                 |20 April                                |
|2026|5 April      |30 March                |12 April                                |
|2027|28 March     |19 April                |2 May                                   |
|2028|16 April     |3 April                 |16 April                                |
|2029|1 April      |26 March                |8 April                                 |