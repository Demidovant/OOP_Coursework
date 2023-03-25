import requests

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
        self.params = {'access_token': self.token, 'v': self.version}

    def user_info(self):
        """Метод возвращает информацию о пользователе с ID=user_id"""
        url = self.baseurl + 'users.get'
        params = {'user_ids': self.id}
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


vk = VK(vk_token, vk_user_id)
ya = YA(ya_token)

print(vk.user_info())
print()
print(ya.disk_info())
