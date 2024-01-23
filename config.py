token = "vk1.a.4fv422Iap7FeZshEIzYernP9u-lpjfWC1mNeon6Kyry53oiRVDSBI8iRfVpQYWP1QQejUIMCLmK-iOVQmZNHNoHURVBlJwNPFhihobfTiVcqJjPkjY5f3yD7LrjONAtlrcK1iVM--idXqTMBmMU3mxsKevBoOH3RNYx2GWSp2rbEEpbWy4xk79RTSqlwDLm7-TQDDnqXHf_aS91xWrxX1Q"
admin_token = "vk1.a.ORPdVASZJKBrBUHgyj0_Dg6rWs1QtGqP_ZqxdY2aB4tHEqsrTqkjLSO58wBEHMEq6Ek-fI3bU5Xl8CzGYiGOA8ykvgICjvR1zMDZflzLOqrK8HyikMswHvyJLIJflGWW5Aslhewk1koc50-qaGtE4CIq5Dj3pLHluHI0ageym4ucXA9zB0apcwQ32tk1HKa5zuRnL2oVNBdlnSb975bK1w"
groupid = 219068570
def_peerid = 2000000000
search_count = 10
urls_parse = True

root_name = "VkSender"

on_add_message = """
Привет!
Я бот, который будет автоматически пересылать посты с расписанием из группы КТС сюда.
Чтобы настроить курс:
1) Выдайте права администратора (или доступ к командам), чтобы я мог получать команды (после установки можете их снять)
2) Введите /course (Ваш курс - цифра от 1 до 5)
* Без скобочек

Если все будет нормально, бот повторит ваш курс, и вы можете убрать права администратора (или доступ к командам).
"""
invalid_syntax_message = "Неверный синтаксис, используйте '/course x', где вместо x - номер вашего курса от 1 до 5"
ads_message = "Поддерживается https://t.me/ktctimetablebot"

check_interval = {
    "seconds": 3
}

courses = {
    '1': '1 курс',
    '2': '2 курс',
    '3': '3 курс',
    '4': '4-5 курс',
}

colleges_ids = {
    'КТС': '-145391943'
}

settings = {
    '1kurs': {
        0: True,
        1: True,
        2: True,
        3: True,
        4: True,
        5: True,
    },
    '2kurs': {
        0: True,
        1: True,
        2: True,
        3: True,
        4: True,
        5: True,
    },
    '3kurs': {
        0: True,
        1: True,
        2: True,
        3: True,
        4: True,
        5: True,
    },
    '4kurs': {
        0: True,
        1: True,
        2: True,
        3: True,
        4: True,
        5: True,
    }
}