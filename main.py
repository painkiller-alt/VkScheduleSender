import time

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent, VkBotEventType
#from vk_api.exceptions import ApiError

from apscheduler.schedulers.background import BackgroundScheduler  # Таймер
from db import DataBase
from lib import *
from log import log

from config import *
from data.constant import *

import traceback as tr

primal_path = getcd()
db_path = f'{primal_path}/data'
db = DataBase(db_path)
sched = BackgroundScheduler()  # Таймер
vk_session = VkApi(token=admin_token)
longpoll = VkBotLongPoll(vk=vk_session, group_id=groupid)
vk = vk_session.get_api()

servicevk_session = VkApi(app_id=51792781, token=service_token, client_secret="WglFxfGsYCVDcswQYTqB")
servicevk = vk_session.get_api()

if urls_parse:
    urls = get_ids(service_token)
else:
    urls = {
        '1': 'https://vk.com/ktskursk?w=wall-145391943_19672',
        '2': 'https://vk.com/ktskursk?w=wall-145391943_19673',
        '3': 'https://vk.com/ktskursk?w=wall-145391943_19674',
        '4': 'https://vk.com/ktskursk?w=wall-145391943_19675'
    }

def check_posts():
    for course, url in urls.items():
        if url not in db.parsed:
            log(url)
            db.parsed[url] = course
            db.save()
            for peer_id, group in db.data.items():
                if group.get('course') == course:
                    subject = url.split('=')[1]
                    repost(vk, int(peer_id), subject)

sched.add_job(check_posts, trigger="interval", **check_interval)

sched.start()

def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            action = event.message.get('action')
            peer_id = event.message.get('peer_id')
            message = event.message
            if action:
                if action.get('type') == "chat_invite_user" and on_add_message:
                    db.data[peer_id] = {}
                    db.save()
                    vk.messages.send(peer_id=peer_id, random_id=generate_random(), message=on_add_message)
            else:
                if message.text.startswith('/course'):
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
                            vk.messages.send(peer_id=peer_id, random_id=generate_random(),
                                             message=f"Ваш курс - {course}. Если все верно, можете снять права администратора - я не смогу читать вашу беседу. Когда выйдет новое официальное расписание, я перешлю его сюда.")

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            log(tr.format_exc())
            time.sleep(10)
