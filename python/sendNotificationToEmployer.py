import smtplib

# help(smtplib)

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

smtpObj.starttls()

smtpObj.login('uitlgtu10@gmail.com','distribution')

smtpObj.sendmail("uitlgtu10@gmail.com","nick.rotari.42@gmail.com","go to your pc and writing diplom, bitch!")
