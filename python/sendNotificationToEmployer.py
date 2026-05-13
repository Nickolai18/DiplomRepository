# import smtplib

# # help(smtplib)

# smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

# smtpObj.starttls()

# smtpObj.login('uitlgtu10@gmail.com','distribution')

# smtpObj.sendmail("uitlgtu10@gmail.com","nick.rotari.42@gmail.com","go to your pc and writing diplom, bitch!")
from datetime import datetime

# Две даты
date1 = datetime(2025, 3, 13, 10, 0, 0)
date2 = datetime(2025, 3, 15, 3, 30, 0)

# Разница (timedelta)
diff = date2 - date1

# 1. Получение часов (только часть часов, без дней)
print(diff.total_seconds())  # Выведет 4 (часы между 10:00 и 14:30)

# 2. Получение общего количества часов (дни * 24 + часы)
total_hours = diff.total_seconds() / 3600
print(total_hours)  # Выведет 52.5 (2 дня * 24 + 4.5 часа)

