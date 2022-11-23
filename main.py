from settings import base_ya_link as ya_link
from settings import TOKEN as ya_token
from settings import base_vk_link as vk_link
from settings import access_token
import datetime as d
import requests
from pprint import pprint as pp


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = vk_link + 'users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def fotos_get(self, f_count, user_id):
        url = vk_link + 'photos.get'
        params = {'owner_id': user_id,
                  'album_id': 'profile',
                  'extended': '1',
                  'photo_sizes': '1',
                  'count': f_count
                  }
        response = requests.get(url, params={**self.params, **params})
        return response.json()


class Yandex:
    """
    class for yandex objects and methods
    """
    base_host = ya_link

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload_fotos(self):
        pass

    def _get_upload_link(self, path):
        uri = 'v1/disk/resources/upload/'
        request_url = self.base_host + uri
        params = {'path': path,
                  'overwrite': True}
        response = requests.get(request_url, params=params, headers=self.get_headers())
        pp(response.json())
        return response.json()['href']

    def create_ya_folder(self):
        uri = 'v1/disk/resources/'
        request_url = self.base_host + uri
        path = str(vk_user_id) + '_' + str(d.date.today())
        params = {'path': path}
        response = requests.put(request_url, params=params, headers=self.get_headers())
        if response.status_code == 201 or response.status_code == 409:
            return path
        else:
            pp(response.json())

    def check_exist_file(self, file_name):
        pass

    def upload_to_ya(self, url, file_name):
        uri = 'v1/disk/resources/upload/'
        request_url = self.base_host + uri
        ya_path = self.create_ya_folder() + '/' + file_name
        if type(ya_path) is str:
            params = {'url': url, 'path': ya_path}
            response = requests.post(request_url, params=params, headers=self.get_headers())
            pp(response.json())
            return


def upload_from_vk_to_ya(vk_json, fotos_count=5):
    count = 1  # счетчик количества фото
    upload_fotos_list = []
    upload_fotos_dict = {}
    for item in vk_json['response']['items']:
        if count <= fotos_count:
            upload_fotos_dict['file name'] = str(item['likes']['count']) + '.jpeg'
            for size in item['sizes']:
                if size['type'] == 'w':
                    upload_fotos_dict['upload_link'] = size['url']
                    upload_fotos_dict['size'] = size['type']
                    upload_fotos_list.append(upload_fotos_dict)
                elif size['type'] == 'z':
                    upload_fotos_dict['upload_link'] = size['url']
                    upload_fotos_dict['size'] = size['type']
                    upload_fotos_list.append(upload_fotos_dict)
                else
                    size = dict(sorted(item['size']))
            count += 1
            ya.upload_to_ya(upload_fotos_dict['upload_link'], upload_fotos_dict['file name'])


if __name__ == '__main__':
    # vk_id = input('Введите id пользователя VK:')
    # ya_token = input('Введите ключ, полученный с полигона Yandex:')
    # access_token = 'access_token'
    # user_id = 'id29252022'
    nic_name = 'glumovav'  # my account
    foto_count = 4  #
    vk = VK(access_token, nic_name)
    ya = Yandex(ya_token)
    pp(vk.users_info())
    vk_user = vk.users_info()
    vk_user_id = vk_user['response'][0]['id']
    res_fotos = vk.fotos_get(foto_count, vk_user_id)
    upload_from_vk_to_ya(res_fotos, foto_count)
