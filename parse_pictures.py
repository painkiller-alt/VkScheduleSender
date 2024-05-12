import requests
from pymongo.mongo_client import MongoClient
from pymongo import collection

courses = {
    '1kurs': '1 курс',
    '2kurs': '2 курс',
    '3kurs': '3 курс',
    '4kurs': '4-5 курс',
}


db_name = "oltry"
db_pass = "goforwhat"

mongodb_uri = f"mongodb+srv://{db_name}:{db_pass}@cluster0.lgoyzdw.mongodb.net/?retryWrites=true&w=majority"

acces_token = '319e4fed319e4fed319e4fed62328804603319e319e4fed54cd383c178437745c845ee7'
version_of_vkapi = '5.154'

colleges_ids = {
    'КТС': '-145391943'
}

def get_ids():
    result = {}

    url = f'https://api.vk.com/method/wall.get?' \
          f'access_token={acces_token}&' \
          f'v={version_of_vkapi}&' \
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

def get_photos(post_ids):
    result = {}
    url = f'https://api.vk.com/method/wall.getById?access_token={acces_token}&v={version_of_vkapi}&posts={",".join(post_ids)}'

    resp = requests.get(url)
    print(resp.json())
    posts = resp.json()['response']['items']
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


# CONFIGURE
search_count = 10
urls_parse = True
settings = {
    '1kurs': {
        0: True,
        1: True,
        2: True,
        3: False,
        4: True,
        5: True,
    },
    '2kurs': {
        0: True,
        1: True,
        2: True,
        3: False,
        4: True,
        5: True,
    },
    '3kurs': {
        0: True,
        1: True,
        2: True,
        3: False,
        4: True,
        5: True,
    },
    '4kurs': {
        0: True,
        1: True,
        2: True,
        3: False,
        4: True,
        5: True,
    }
}


if urls_parse:
    urls = get_ids()
else:
    urls = {
        '1kurs': 'https://vk.com/ktskursk?w=wall-145391943_19895',
        '2kurs': 'https://vk.com/ktskursk?w=wall-145391943_19896',
        '3kurs': 'https://vk.com/ktskursk?w=wall-145391943_19897',
        '4kurs': 'https://vk.com/ktskursk?w=wall-145391943_19898'
    }

def get_attacments():
    posts_ids = []
    for course, post_url in urls.items():
        posts_ids.append(post_url.split('wall')[-1])

    if posts_ids:
        pics = get_photos(posts_ids)
    else:
        raise ValueError("New pictures not found")

    to_save = {}
    for course, days in settings.items():
        to_save[course] = {}
        day_n = 0
        for i, setting in days.items():
            to_save[course][str(i)] = None
            if len(pics[course])-1 < day_n or setting == False:
                to_save[course][str(i)] = None
            else:
                to_save[course][str(i)] = pics[course][day_n]['url']
                day_n += 1

    return to_save

def parse(test=True):
    client = MongoClient(mongodb_uri)

    if test:
        db = client.KTCbot_data_test
    else:
        db = client.KTCbot_data

    colleges: collection.Collection = db.colleges

    coll = colleges.find_one("КТС")

    coll["attachments"] = get_attacments()

    colleges.update_one(
        {"_id": f"КТС"},
        {"$set": coll}
    )

if __name__ == '__main__':
    parse(test=True)
