from vk_api.exceptions import ApiError
from random import randint
from config import *
from data.constant import *
import requests
import os

def getcd():
    path_here = os.getcwd()
    path_here = path_here.replace('\\', '/')
    path_list = path_here.split('/')

    path_result = ''
    for path_dir in path_list:
        path_result += f'{path_dir}'
        if root_name in path_dir:
            break
        path_result += '/'

    return path_result

def generate_random():
    return randint(0, 1000000)

def check_admin(vk, groupid):
    for peerid in range(1, 1000):

        try:
            members = vk.messages.getConversationMembers(peer_id=def_peerid + peerid)
        except ApiError:
            break

        for i in members["items"]:
            print(i["member_id"])
            if i["member_id"] == -groupid:
                admin = i.get('is_admin', False)
                if admin:
                    print('admined')

def get_ids(service_token):
    result = {}

    url = f'https://api.vk.com/method/wall.get?' \
          f'access_token={service_token}&' \
          f'v=5.199&' \
          f'owner_id={colleges_ids["КТС"]}&' \
          f'count={search_count}'

    resp = requests.get(url)
    posts = resp.json()['response']['items']

    for post in posts:
        text = post['text']

        if "#РасписаниеКТС" in text:
            for course, course_rus in courses.items():
                if course_rus in text:
                    result[course] = f"https://vk.com/ktskursk?w=wall{colleges_ids['КТС']}_{post['id']}"

        if set(result) == {"1kurs", "2kurs", "3kurs", "4kurs"}:
            break

    return result

def get_subject(post_url):
    return post_url.split('wall')[-1]

def get_photos(vk, urls):
    result = {}

    posts_ids = []
    for course, post_url in urls.items():
        posts_ids.append(get_subject(post_url))

    posts = vk.wall.getById(posts=",".join(posts_ids))["items"]

    for post_n, post in enumerate(posts):
        for attachment in post['attachments']:
            last_edit = 0
            maxheight = 0
            for size_n, size in enumerate(attachment['photo']['sizes']):
                if size['height'] > maxheight:
                    maxheight = size['height']
                    last_edit = size_n

            course = list(urls.keys())[post_n]
            if course in result:
                result[list(urls.keys())[post_n]].append(attachment['photo']['sizes'][last_edit])
            else:
                result[list(urls.keys())[post_n]] = [attachment['photo']['sizes'][last_edit]]

    return result

def repost(vk, peerid, attachid):
    try:
        vk.messages.send(peer_id=peerid, random_id=generate_random(), message=ads_message, attachment=f"{attachid}")
    except ApiError:
        pass