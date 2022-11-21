from settings import base_ya_link as ya_link
from settings import base_vk_link as vk_link
from settings import access_token
import datetime
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
    def __init__(self, token):
        self.token = token

    def upload_fotos(self):
        pass
    def create_ya_folder(self):
        pass


def upload_from_vk_to_ya(vk_json, ya_obj, fotos_count):
    upload_fotos_list = []
    upload_fotos_dict = {}
    for item in vk_json['response']['items']:
        upload_fotos_dict['file name'] = str(item['likes']['count']) + '.jpeg'
        for foto in item['sizes']:
            if foto['type'] == 'w':
                upload_fotos_dict['upload_link'] = foto['url']
                upload_fotos_dict['size'] = foto['type']
                upload_fotos_list.append(upload_fotos_dict)




if __name__ == '__main__':
    # vk_id = input('Введите id пользователя VK:')
    # ya_token = input('Введите ключ, полученный с полигона Yandex:')
    # access_token = 'access_token'
    # user_id = 'id29252022'
    nic_name = 'glumovav' # my account
    foto_count = 5 #
    vk = VK(access_token, nic_name)
    ya = Yandex()
    pp(vk.users_info())
    vk_user = vk.users_info()
    vk_user_id = vk_user['response'][0]['id']
    res_fotos = vk.fotos_get(foto_count, vk_user_id)

    result = upload_from_vk_to_ya(res_fotos, ya, foto_count)


