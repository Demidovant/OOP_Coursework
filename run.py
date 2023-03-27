import json
import requests
import datetime
import time
from tqdm import tqdm


class VK:
    def __init__(self, token, user_id, version='5.131'):
        self.baseurl = 'https://api.vk.com/method/'
        self.token = token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version, 'user_ids': self.id}

    def user_info(self):
        """Метод возвращает информацию о пользователе с ID=user_id"""
        url = self.baseurl + 'users.get'
        response = requests.get(url, params=self.params)
        return response.json()

    def get_photos(self, count=5):
        """Метод возвращает список фотографий в профиле"""
        url = self.baseurl + 'photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1, 'count': count}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


class YA:
    def __init__(self, token):
        self.baseurl = 'https://cloud-api.yandex.net/'
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def disk_info(self):
        """Метод возвращает информацию о диске пользователя"""
        url = self.baseurl + 'v1/disk'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def is_file_exist(self, folder, filename):
        """Метод проверяет существует ли указанный файл"""
        url = self.baseurl + 'v1/disk/resources'
        path = folder + '/' + filename
        params = {'path': path}
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            # print(f'Файл {filename} уже существует в папке {folder}')
            return True
        else:
            return False

    def create_folder(self, folder):
        """Метод создает папку на яндекс диске"""
        url = self.baseurl + 'v1/disk/resources'
        params = {'path': folder}
        resp = requests.put(url, headers=self.headers, params=params)
        # if resp.status_code == 201:
        #     print(f'Папка {folder} успешно создана')
        # else:
        #     print(f'Ошибка при создании папки {folder}')
        #     print(resp.json())

    def upload(self, folder, filename, link_to_img):
        """Метод загружает файл на яндекс диск"""
        url = self.baseurl + 'v1/disk/resources/upload'
        path = folder + '/' + filename
        params = {'path': path, 'url': link_to_img}
        resp = requests.post(url, headers=self.headers, params=params)
        # if resp.status_code == 202:
        #     print(f'Файл {filename} успешно загружен в папку {folder}')
        # else:
        #     print(f'Ошибка при загрузке файла {filename} в папку {folder}')
        #     print(resp.json())


if __name__ == '__main__':

    with open('config.json') as input_file:
        config = json.load(input_file)
    ya_token = config['ya_token']
    vk_token = config['vk_token']
    vk_user_id = config['vk_user_id']

    vk = VK(vk_token, vk_user_id)
    ya = YA(ya_token)

    # print(vk.user_info())
    # print(ya.disk_info())

    photos = vk.get_photos()

    folder = vk_user_id
    ya.create_folder(folder)

    stat = []

    for photo in tqdm(photos['response']['items']):
        max_size = max(photo['sizes'], key=lambda x: x['type'])
        filename = f"{photo['likes']['count']}.jpg"
        if ya.is_file_exist(folder, filename):
            now = datetime.datetime.now()
            filename = f"{photo['likes']['count']}_{now.strftime('%Y-%m-%d_%H-%M-%S_%f')}.jpg"
        stat.append({'file_name': filename, 'size': max_size['type'], 'folder': folder})
        ya.upload(folder, filename, max_size['url'])
        time.sleep(0.2)

    with open('stat.json', 'w', encoding='utf-8') as out_file:
        json.dump(stat, out_file)
