import datetime

arrTicket = [{'id': 1, 'title': 'Сломался принтер', 'description': 'не печатает принтер', 'employee': 'pf', 'critical': 0, 'create_date': datetime.datetime(2026, 5, 9, 11, 9), 'confirm_date': datetime.datetime(2026, 5, 11, 12, 40, 20)},
{'id': 2, 'title': 'Интернетjjnjn', 'description': 'Интернет Не работает', 'employee': 'pf', 'critical': 1, 'create_date': datetime.datetime(2026, 5, 9, 11, 10, 38), 'confirm_date': datetime.datetime(2026, 5, 11, 12, 40, 20)},
{'id': 3, 'title': 'Интернет', 'description': 'Не загружается сайт', 'employee': 'hr', 'critical': 0, 'create_date': datetime.datetime(2026, 5, 9, 11, 18, 9), 'confirm_date': datetime.datetime(2026, 5, 11, 16, 47, 21)},
{'id': 4, 'title': 'ЭЦП', 'description': 'Установить ЭЦП', 'employee': 'hr', 'critical': 2, 'create_date': datetime.datetime(2026, 5, 9, 11, 25, 38), 'confirm_date': datetime.datetime(2026, 5, 11, 16, 47, 19)}]

arrUsers = [{'name': 'Николай', 'surname': 'Ротарь', 'code': 'hr', 'number_of_calls': 27},{'name': 'Николай', 'surname': 'Ротарь', 'code': 'pf', 'number_of_calls': 27}]

numOfUsers = []
# print(coding.get('hr'))
def countTicket(arrayUsers, numberOfUsers, arrayTicket = 0):
    for user in arrayUsers:
        codeUser = user["code"]
        numberOfUsers.append({codeUser:0})
    def addTicketInCount(code, numberOfUsers):
            for codeUserInf in numberOfUsers:
                if codeUserInf.get(code) != None:
                    codeUserInf[code] += 1
                    break
                else:
                    continue
    for ticket in arrayTicket:
        arrayTicket 
    
countTicket(arrUsers, numOfUsers)
print(numOfUsers)
