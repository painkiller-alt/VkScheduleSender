import time

import requests
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
#from vk_api.exceptions import ApiError
from keyboards import kboards
import json

from apscheduler.schedulers.background import BackgroundScheduler  # Таймер
from db import DataBase
from lib import *
from log import log, logging

from config import *
from data.constant import *

import traceback as tr

logging.getLogger('apscheduler.executors.default').propagate = False  # Отключение логгинга scheduler-а
primal_path = getcd()
db_path = f'{primal_path}/data'
db = DataBase(db_path)
sched = BackgroundScheduler()  # Таймер

urls = get_ids(service_token)

def check_posts():
    log("Проверено")
    parse_urls = get_ids(service_token)

    for course, url in parse_urls.items():
        if url not in db.parsed:
            log(url)
            db.parsed[url] = course
            db.save()
            for peer_id, data in db.data.items():
                if data.get('course') == course and data.get("timetable"):
                    subject = url.split('=')[1]
                    repost(vk, int(peer_id), subject)

sched.add_job(check_posts, trigger="interval", **check_interval)

sched.start()

def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            peer_id = str(event.message.get('peer_id'))
            action = event.message.get('action')
            message = event.message
            if action:
                if action.get('type') == "chat_invite_user" and on_add_message:
                    db.data[peer_id] = {}
                    db.save()
                    vk.messages.send(peer_id=peer_id, random_id=generate_random(), message=on_add_message)
            else:
                # Если написали команду /course
                if message.text.startswith('/course'):
                    if not db.data[peer_id].get("repls"): db.data[peer_id].update({"repls": True})
                    if not db.data[peer_id].get("timetable"): db.data[peer_id].update({"timetable": True})
                    sp = message.text.split(" ", maxsplit=1)
                    if len(sp) > 1:
                        course = sp[1]

                        if course not in ["1", "2", "3", "4", "5"]:
                            vk.messages.send(peer_id=peer_id, random_id=generate_random(),
                                             message=invalid_syntax_message)
                        else:
                            if not db.data.get(peer_id):
                                db.data[peer_id] = {}

                            to_add = "4" if course == "5" else course
                            db.data[peer_id].update({"course": to_add})
                            db.save()

                            if int(peer_id) >= 2000000000:
                                msg = f"Ваш курс - {course}. Если все верно, можете снять права администратора - я не смогу читать вашу беседу. Когда выйдет новое официальное расписание, я перешлю его сюда. \n\nПересылать:"
                            else:
                                msg = f"Ваш курс - {course}. Когда выйдет новое официальное расписание, я перешлю его сюда. \n\nПересылать:"

                            msg_id = generate_random()
                            vk.messages.send(
                                peer_id=peer_id,
                                random_id=msg_id,
                                message=msg,
                                keyboard=kboards.menu
                            )
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            vk.messages.sendMessageEventAnswer(
                      event_id=event.object.event_id,
                      user_id=event.object.user_id,
                      peer_id=event.object.peer_id,
                      event_data=json.dumps({"type": "show_snackbar", "text": "Настройки применены"}))

            peer_id = str(event.object.get('peer_id'))
            call = event.object.payload.get('type')
            # Отвечаем на callback
            if call in calls:
                setting = call

                db.data[peer_id][setting] = not db.data[peer_id][setting]
                db.save()

                if setting == "timetable":
                    rus_setting = "Расписание"
                else:
                    rus_setting = "Замены"

                vk.messages.send(
                    peer_id=peer_id,
                    random_id=generate_random(),
                    message=f"{rus_setting}: {'Вкл.' if db.data[peer_id][setting] else 'Выкл.'}"
                )



if __name__ == "__main__":
    while True:
        try:
            log("Запуск")
            vk_session = VkApi(token=admin_token)
            longpoll = VkBotLongPoll(vk=vk_session, group_id=groupid)
            vk = vk_session.get_api()

            servicevk_session = VkApi(app_id=51792781, token=service_token, client_secret="WglFxfGsYCVDcswQYTqB")
            servicevk = vk_session.get_api()
            main()
        except Exception as e:
            log(tr.format_exc())
            time.sleep(10)
