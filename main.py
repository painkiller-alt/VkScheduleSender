from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
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

def get_photos_upload_server(group_id):
    resp = requests.get(
        f"https://api.vk.com/method/photos.getWallUploadServer?access_token={admin_profile_token}&group_id={group_id}&v=5.199"
    )

    return resp.json()["response"]["upload_url"]

def save_wall_photo(group_id, server, photo, h):
    resp = requests.get(
        f"https://api.vk.com/method/photos.saveWallPhoto?access_token={admin_profile_token}&v=5.199&group_id={group_id}&server={server}&photo={photo}&hash={h}"
    )

    return resp.json()["response"]

def post(owner_id, message, attachments):
    requests.get(
        f"https://api.vk.com/method/wall.post?access_token={admin_profile_token}&v=5.199&owner_id={owner_id}&message={message}&attachments={attachments}"
    )

def check_posts():
    log("Проверено")
    parse_urls = get_ids(service_token)

    for user_course, url in parse_urls.items():
        if url not in db.parsed:
            log(url)
            db.parsed[url] = user_course
            db.save()
            for peer_id, data in db.data.items():
                if course(data.get('group'))[0] == user_course and data.get("timetable"):
                    subject = url.split('=')[1]
                    repost(vk, int(peer_id), subject)
sched.add_job(check_posts, trigger="interval", **check_interval)

def check_repls():
    repl_groups, img = get_repls()

    if not repl_groups:
        return

    log(f"Замены получены > {img} / {repl_groups}")

    ### Постим пост в группу с картинкой
    upload_url = get_photos_upload_server(groupid)
    resp = requests.post(upload_url, files={'file': open(img, 'rb')}).json()
    s = save_wall_photo(groupid, resp["server"], resp["photo"], resp["hash"])
    post(-groupid, "", f"photo{s[0]['owner_id']}_{s[0]['id']}")
    ###

    log("Пост создан")

    last_post_url = get_last_post(groupid)

    # Делаем рассылку с заменами
    for peer_id, data in db.data.items():
        if data.get('group') in repl_groups and data.get("repls"):
            repost(vk, int(peer_id), last_post_url.split("=")[1])

    log("Рассылка завершена")

    remove_repls()
    log("Файлы удалены")

sched.add_job(check_repls, trigger="interval", **repls_check_interval)

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
                # Если написали команду /group
                if message.text.startswith('/group'):
                    sp = message.text.strip().split(" ", maxsplit=1)
                    if len(sp) > 1:
                        group = sp[1]

                        found_group = find_group(group)
                        if not found_group:
                            db.data[peer_id] = {}
                            vk.messages.send(
                                peer_id=peer_id,
                                random_id=generate_random(),
                                message=f"Кажется такой группы нет, проверьте чтобы название точно совпадало с названием в расписании (регистр букв не важен), Если вы уверены в правильности ввода, напишите @oltry. \nСписок групп:\n\n{all_groups_send()}"
                            )
                        else:
                            if not db.data.get(peer_id):
                                db.data[peer_id] = {}

                            if not db.data[peer_id].get("repls"): db.data[peer_id].update({"repls": True})
                            if not db.data[peer_id].get("timetable"): db.data[peer_id].update({"timetable": True})

                            db.data[peer_id].update({"group": found_group})
                            db.save()

                            if int(peer_id) >= 2000000000:
                                msg = f"Ваша группа - {found_group}. Если все верно, можете снять права администратора - я не смогу читать вашу беседу. Когда выйдет новое официальное расписание, я перешлю его сюда. \n\nПересылать:"
                            else:
                                msg = f"Ваша группа - {found_group}. Когда выйдет новое официальное расписание, я перешлю его сюда. \n\nПересылать:"

                            msg_id = generate_random()
                            vk.messages.send(
                                peer_id=peer_id,
                                random_id=msg_id,
                                message=msg,
                                keyboard=kboards.menu
                            )
                    else:
                        vk.messages.send(peer_id=peer_id, random_id=generate_random(),
                                         message=invalid_syntax_message)

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
            vk_session = VkApi(token=admin_token, api_version="5.199")
            longpoll = VkBotLongPoll(vk=vk_session, group_id=groupid)
            vk = vk_session.get_api()

            servicevk_session = VkApi(app_id=51792781, token=service_token, client_secret="WglFxfGsYCVDcswQYTqB", api_version="5.199")
            servicevk = vk_session.get_api()

            main()
        except Exception as e:
            log(tr.format_exc())
            time.sleep(10)
