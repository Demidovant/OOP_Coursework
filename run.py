import requests
import datetime
import time

with open('ya_token.txt') as file1, open('vk_token.txt') as file2, open('vk_user_id.txt') as file3:
    ya_token = file1.read()
    vk_token = file2.read()
    vk_user_id = file3.read()


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

    def is_file_exist(self, filename):
        """Метод проверяет существует ли указанный файл"""
        url = self.baseurl + 'v1/disk/resources'
        params = {'path': filename}
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            print(f'Файл {filename} существует')
            return True
        else:
            return False

    def create_folder(self, folder):
        """Метод создает папку на яндекс диске"""
        url = self.baseurl + 'v1/disk/resources'
        params = {'path': folder}
        resp = requests.put(url, headers=self.headers, params=params)
        if resp.status_code == 201:
            print(f'Папка {folder} успешно создана')
        else:
            print(f'Ошибка при создании папки {folder}')
            print(resp.json())

    def upload(self, path, link_to_img):
        """Метод загружает файл на яндекс диск"""
        url = self.baseurl + 'v1/disk/resources/upload'
        params = {'path': path, 'url': link_to_img}
        resp = requests.post(url, headers=self.headers, params=params)
        if resp.status_code == 202:
            print(f'Файл {path} успешно загружен')
        else:
            print('Ошибка при загрузке файла')
            print(resp.json())


vk = VK(vk_token, vk_user_id)
ya = YA(ya_token)

# print(vk.user_info())
# print(ya.disk_info())

photos = vk.get_photos()

folder_to_save_photos = vk_user_id
ya.create_folder(folder_to_save_photos)

for photo in photos['response']['items']:
    # max_size = max([size['type'] for size in photo['sizes']])
    flag = False
    for type_ in 'wzyrqpoxms':
        if flag:
            break
        for size in photo['sizes']:
            if size['type'] == type_:
                filename = f"{folder_to_save_photos}/{photo['likes']['count']}.jpg"
                if ya.is_file_exist(filename):
                    now = datetime.datetime.now()
                    filename = f"{folder_to_save_photos}/{photo['likes']['count']}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
                ya.upload(filename, size['url'])
                time.sleep(1)
                flag = True
