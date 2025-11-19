from datetime import date, timedelta

def Gauss(y): 
  """
  Thuật toán Gauss, thuật toán tính Lễ Phục Sinh theo lịch Grégorien.
  Nếu trước 1582, sử dụng lịch Julien.
  Còn gọi là "Osternformel" (công thức Lễ Phục Sinh), tìm ra vào 1800 (sửa đổi lần cuối vào 1816)
  """
  a = y % 19 # Chỉ số vàng
  b = y % 4 # Bao nhiêu phần dư sau khi chia 4
  c = y % 7 # Bao nhiêu phần dư sau khi chia 7
  k = y // 100 # The kỷ
  p = (13 + 8 * k) // 25 # Phương trình mặt trăng
  q = k // 4 # Bao nhiêu 400?
  m = (15 - p + k - q) % 30 if y > 1582 else 15 # Hằng cải chính âm lịch the kỷ
  n = (4 + k - q) % 7 if y > 1582 else 6 # Hằng cải chính dương lịch thế kỷ
  d = (19 * a + m) % 30 # Epact
  if d == 29 or (d == 28 and a > 10): d -= 1 # Xử lý ngoại lệ
  e = (2 * b + 4 * c + 6 * d + n) % 7 # Số ngày trước Lễ Phục Sinh 
  march_date = d + e + 22
  april_date = d + e - 9
  return (april_date, 4) if march_date > 31 else (march_date, 3)

def Clavian(y):
  """
  Thuật toán của Christopher Clavius, dựa theo các bảng tính phức tạp của ông trong sách "Romani Calendarii ab Gregorio XIII Pontifice Maximo Restituti Explicatio Sanctissimi Domini Nostri Clementis VIII Pontificis Maximi Jussu Edita" của Christopher Clavius, xuất bản năm 1603.
  """
  g = y % 19 + 1 # Chỉ số vàng
  f = 11 * g % 30 # Nen móng
  k = y // 100 # The kỷ
  s = 3 * (k - 15) // 4 # Phương trình mặt trời
  l = 8 * (k - 14) // 25 # Phương trình mặt trăng
  e = (f - 10 - s + l) % 30 # Epact
  # Rằm Vượt Qua
  if e < 24: m = 44 - e
  elif e == 24: m = 49 # 18 avril
  elif e == 25: m = 49 if g < 12 else 48
  elif e > 25: m = 74 - e
  elif y <= 1582: m = 47 - f if f < 27 else 77 - f # Julian trước 15/10/1582
  d = k - k // 4 - 2 if y > 1582 else 0 # Khoảng cách ngày
  h = (y + y // 4 - d + m) % 7 # Thứ của ngày rằm
  march_date = m + 7 - h
  april_date = m - 24 - h
  return (april_date, 4) if march_date > 31 else (march_date, 3)

def Typikon(y):
  """
  Thuật toán Typikon Chính Thống Giáo, theo sách "Typikon" của Giáo hội Chính Thống Giáo. Dùng để tính Lễ Phục Sinh trong lịch Julien (đặc biệt đối với Lễ Phục Sinh Công Giáo trước năm 1583, các nước Tin Lành tiền-Grégorien trước 14/9/1752, Phổ trước 2/9/1610, etc cũng như các nước Chính Thống Giáo dùng lịch Julien cải chánh (dùng lịch Grégorien cho các ngày lễ cố định, nhưng lễ Phục Sinh theo lịch Julien cổ truyền) và cổ truyền (dùng lịch Julien cho các ngày lễ cố định và di động)). Công thức này được sử dụng trong các nghi thức của Giáo hội Chính Thống Giáo.
  
  Returns:
    Ngày lễ Phục Sinh theo lịch Julien
  """
  l = (y + 16) % 19 + 1 # Chu kỳ mặt trăng
  s = (y + 19) % 28 + 1 # Chu kỳ mặt trời
  f = (11 * l + (3 if l < 17 else 4)) % 30 # Nền móng (Themelion)
  m = 47 - f if f < 27 else 77 - f # Rằm Vượt Qua
  c = (s + s // 4 - 1) % 7 + 1 # Đồng dạng (Concurrent)
  h = (m + c + 3) % 7 # Thứ của rằm
  march_date = m + 7 - h
  april_date   = m - 24 - h
  return (april_date, 4) if march_date > 31 else (march_date, 3)

def Meeus(y):
  """
  Thuật toán Meeus Chính Thống Giáo, theo sách "Astronomical Algorithms" của Jean Meeus.
  
  Returns:
    Ngày lễ Phục Sinh theo lịch Julien
  """
  a = y % 4
  b = y % 7
  c = y % 19
  d = (19 * c + 15) % 30
  e = (2 * a + 4 * b - d + 34) % 7
  month = (d + e + 114) // 31
  day = (d + e + 114) % 31 + 1
  return (day, month)

def juliantoGregorian(y):
  """
  Chuyển đổi từ lịch Julien sang lịch Grégorien.
  """
  julianeaster = Meeus(y)
  julian_date = date(y, julianeaster[1], julianeaster[0])
  correction = y // 100 - y // 400 - 2
  gregorian_date = julian_date + timedelta(days=correction) # Đó là vì module timedate chỉ hỗ trợ lịch Grégorien kể cả lịch tính trước 1582
  return (gregorian_date.day, gregorian_date.month)

def Bradley(y):
  """
  Thuật toán của James Bradley, dựa theo các bảng tính của ông trong The Book of Common Prayer và trong Luật Lịch pháp của Quốc hội Anh năm 1750.
  """
  g = y % 19 + 1 # Chỉ số vàng
  s = (y - 1600) // 100 - (y - 1600) // 400 # Phương trình Mặt Trời
  l = 8 * (y // 100 - 14) // 25 # Phương trình Mặt Trăng
  c = s - l # Mã cypher
  p = (3 - 11 * g + c) % 30 if y > 1582 else (26 - 11 * g) % 30 # Rằm Vượt Qua
  if p == 29 or (p == 28 and g > 11): p -= 1
  d = (y + y // 4 - y // 100 + y // 400) % 7 if y > 1582 else (y + y // 4 + 5) % 7 # Chữ Chúa Nhật
  march_date = p + 22 + (4 - d - p) % 7 
  april_date = p - 9 + (4 - d - p) % 7
  return (april_date, 4) if march_date > 31 else (march_date, 3)

def Carter(y):
  """
  Thuật toán của Carter, dựa theo công thức in trên Tờ Thông Tin số 57: "Ngày Lễ Phục Sinh" của Đài Thiên văn Hoàng gia Greenwich năm 1996.
  """
  a = y % 19
  k = y // 100
  s = k - k // 4 - 12
  m = 8 * (k - 14) // 25
  b = 202 + s - m - 11 * a if y > 1582 else 225 - 11 * a
  d = b % 30 + 21
  if (d == 49 and a > 10) or d == 50: d -= 1
  e = (y + y // 4 + d - 10 - s) % 7 if y > 1582 else (y + y // 4 + d) % 7
  q_3 = d + 7 - e # Mars
  q_4 = d - 24 - e # April
  return (q_4, 4) if q_3 > 31 else (q_3, 3)

def AnonymousNY(y):
  """
  Thuật toán Nature năm 1876 (tối ưu hoá 1961)
  """
  if y < 1583: return Meeus(y) # Phương pháp này chỉ áp dụng cho năm >= 1583
  a = y % 19
  b = y // 100
  c = y % 100
  d = b // 4
  e = b % 4
  g = (8 * b + 13) // 25
  h = (19 * a + b - d - g + 15) % 30
  i = c // 4
  k = c % 4
  l = (32 + 2 * e + 2 * i - h - k) % 7
  m = (a + 11 * h + 19 * l) // 433
  n = (h + l - 7 * m + 90) // 25 # Tháng
  o = (h + l - 7 * m + 33 * n + 19) % 32 # Ngày
  return (o, n)

def Knuth(x):
  """
  Thuật toán Knuth, từ quyển "The Art of Computer Programming" của Donald E. Knuth
  """
  b = (x % 19) + 1 # Chỉ số vàng
  c = x // 100 + 1 # Thế kỷ
  d = 3 * c // 4 - 12 if x > 1582 else 0 # Phương trình Mặt Trời
  e = (8 * c + 5) // 25 - 5 if x > 1582 else 7 # Phương trình Mặt Trăng
  f = 5 * x // 4 - d - 10 if x > 1582 else 5 * x // 4 - 7 # Chúa Nhật
  h = (11 * b + 20 + e - d) % 30 # Epact
  if (h == 25 and b > 11) or (h == 24): h += 1
  i = 44 - h # Rằm Vượt Qua
  if i < 21: i += 30
  j = (f + i) % 7 # Thứ của rằm
  k3 = i + 7 - j
  k4 = i - 24 - j
  return (k4, 4) if k3 > 31 else (k3, 3)

def Oudin(m):
  """
  Thuật toán của Jean-Marc Oudin, từ bài viết "Étude sur la date de Pâques" (Nghiên cứu về ngày Lễ Phục Sinh) của ông (1940).
  """
  c = m // 100
  k = c - 17 // 25
  r = (c - c // 4 - (c - k) // 3 + 19 * (m % 19) + 15) % 30 if m > 1582 else (19 * (m % 19) + 15) % 30 # Rằm Vượt Qua
  if r == 29 or (r == 28 and m % 19 > 10): r -= 1
  j = (m + m // 4 + r + 2 - c + c // 4) % 7 if m > 1582 else (m + m // 4 + r) % 7
  p3 = 28 + r - j
  p4 = r - j - 3
  return (p4, 4) if p3 > 31 else (p3, 3)

if __name__ == "__main__":
  # Thử nghiệm các thuật toán
  y = int(input("Nhập năm cần nhập: "))
  # Lưu ý, năm sau 1582 mới áp dụng lịch Grégorien, còn trước đó sử dụng lịch Julien.
  
  print(f"Gauss: {Gauss(y)[0]} tháng {Gauss(y)[1]}") # Lịch Grégorien
  print(f"Clavius: {Clavian(y)[0]} tháng {Clavian(y)[1]}") # Lịch Grégorien
  print(f"Bradley: {Bradley(y)[0]} tháng {Bradley(y)[1]}") # Lịch Grégorien
  print(f"Carter: {Carter(y)[0]} tháng {Carter(y)[1]}") # Lịch Grégorien
  print(f"AnonymousNY: {AnonymousNY(y)[0]} tháng {AnonymousNY(y)[1]}") # Lịch Grégorien
  print(f"Knuth: {Knuth(y)[0]} tháng {Knuth(y)[1]}") # Lịch Grégorien
  print(f"Oudin: {Oudin(y)[0]} tháng {Oudin(y)[1]}") # Lịch Grégorien
  print(f"--------------------------------")  
  print(f"Typikon: {Typikon(y)[0]} tháng {Typikon(y)[1]} {"(Julien)" if y > 1582 else ""}") # Lịch Julien
  print(f"Meeus: {Meeus(y)[0]} tháng {Meeus(y)[1]} {"(Julien)" if y > 1582 else ""}") # Lịch Julien
  print(f"(Lịch Grégorien {"tính trước" if y <= 1582 else "cho Lễ Phục Sinh Chính Thống Giáo"}: {juliantoGregorian(y)[0]} tháng {juliantoGregorian(y)[1]})")