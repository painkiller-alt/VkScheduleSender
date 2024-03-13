groupid = 219068570
admin_id = 451418349
def_peerid = 2000000000
search_count = 10

on_add_message = """
Привет!
Я бот, который будет автоматически пересылать посты с расписанием из группы КТС и лично ваши замены сюда.
Чтобы настроить группу:
1) Выдайте права администратора (или доступ к командам), чтобы я мог получать команды (после установки можете их снять)
2) Введите /group <ваша группа> (Название как в расписании)
* Без <>

Если все будет нормально, бот повторит вашу группу, и вы можете убрать права администратора (или доступ к командам).
"""
invalid_syntax_message = "Неверный синтаксис, используйте '/group x', где вместо x - название вашей группы (как в расписании)\n\nПример:\n/group исп-1.2 \n или \n/group Р-1 и тд."
ads_message = "Поддерживается https://t.me/ktctimetablebot"

groups = {
  "1kurs": [
    "12 Группа",
    "13 Группа",
    "ССА-1",
    "ИСП-1.1",
    "ИСП-1.2",
    "ИСП-1.3",
    "ИСП-1.1К",
    "ИСП-1.2К",
    "ИКС-1.1",
    "ИКС-1.2",
    "ИБ-1",
    "Р-1",
    "ПС-1"
  ],
  "2kurs": [
    "22 Группа",
    "23 Группа",
    "ССА-2",
    "ИСП-2.1",
    "ИСП-2.2",
    "ИСП-2К",
    "ИКС-2.1",
    "ИКС-2.2",
    "Р-2"
  ],
  "3kurs": [
    "32 Группа",
    "33 Группа",
    "ССА-3.1",
    "ССА-3.2",
    "ИСП-3.1",
    "ИСП-3.2",
    "ИСП-3К",
    "ИКС-3",
    "Р-3",
    "ПС-3"
  ],
  "4kurs": [
    "ССА-4.1",
    "ССА-4.2",
    "ПКС-4.1",
    "ПКС-4.2",
    "ПКС-4К",
    "ИКС-4",
    "ИКС-5",
    "Р-4"
  ]
}

calls = ("timetable", "repls")

check_interval = {"seconds": 60}
repls_check_interval = {"seconds": 3}

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