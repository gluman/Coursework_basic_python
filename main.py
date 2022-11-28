from settings import base_ya_link as ya_link
from settings import Y_TOKEN as ya_token
from settings import base_vk_link as vk_link
from settings import VK_TOKEN as vk_token
import datetime as d
import requests
from pprint import pprint as pp
from progressbar import ProgressBar

import time


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

    def fotos_get(self, f_count, user_id, album='profile'):
        url = vk_link + 'photos.get'
        params = {'owner_id': user_id,
                  'album_id': album,
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

    def get_ya_folder(self):
        uri = 'v1/disk/resources/'
        request_url = self.base_host + uri
        path = str(vk_user_id) + '_' + str(d.date.today())
        params = {'path': path}
        response = requests.put(request_url, params=params, headers=self.get_headers())
        if response.status_code == 201 or response.status_code == 409:
            return path
        else:
            pp(response.json())

    def check_exist_file(self, path_name, file_name):  # fix it
        uri = 'v1/disk/resources/'
        request_url = self.base_host + uri
        params = {'path': path_name + '/' + file_name}
        response = requests.get(request_url, params=params, headers=self.get_headers())
        res = response.json()
        if response.status_code == 200:
            f_name = res['name'].split('.')
            if len(f_name[0].split('_')) > 2:
                p1_name = f_name[0].split('_')  # f_name[1] is .jpeg
                if len(p1_name) > 2:
                    p1_name[2] = '_' + str(int(p1_name[2]) + 1)
                    self.check_exist_file(path_name, p1_name.join())
                else:
                    self.check_exist_file(path_name, p1_name.join() + '_1' + '.' + f_name[1])
            else:
                self.check_exist_file(path_name, f_name[0] + '_' + str(d.date.today()) + '.' + f_name[1])  # fix it. возвращает значение сюдаже, а нужно где вызывается. нужно поменять всю конструкцию на while
        else:
            return file_name

    def upload_to_ya(self, url, file_name):
        uri = 'v1/disk/resources/upload/'
        request_url = self.base_host + uri
        ya_path = self.get_ya_folder() + '/' + file_name
        if type(ya_path) is str:
            params = {'url': url, 'path': ya_path}
            response = requests.post(request_url, params=params, headers=self.get_headers())
            return response.status_code


def json_file(dic):  # fix it
    pass


def upload_from_vk_to_ya(vk_json, fotos_count=5):
    count = 1  # счетчик количества фото
    upload_fotos_list = []
    upload_fotos_dict = {}
    l = len(vk_json['response']['items'])
    if l < fotos_count:
        cnt_foto = l
    else:
        cnt_foto = fotos_count
    progress_foto = round(100 / l, 0)
    print('Starting copy files from VK to YA...')
    pbar = ProgressBar().start()

    for item in vk_json['response']['items']:
        if count <= cnt_foto:
            ya_path = ya.get_ya_folder()
            upload_fotos_dict['file name'] = ya.check_exist_file(ya_path, str(item['likes']['count']) + '.jpeg')
            link = ''
            size_type = ''
            sizing = [y['type'] for y in item['sizes']]
            sizing.sort()
            for size in item['sizes']:
                if size['type'] == sizing[-1]:
                    link = size['url']
                    size_type = size['type']
                    break
            upload_fotos_dict['upload_link'] = link
            upload_fotos_dict['size'] = size_type
            ya.upload_to_ya(upload_fotos_dict['upload_link'], upload_fotos_dict['file name'])
            upload_fotos_dict.pop('upload_link')
            upload_fotos_list.append(upload_fotos_dict)
            pbar.update(progress_foto * count)
            time.sleep(3)
            count += 1
    json_file(upload_fotos_list)
    pbar.finish()
    print('Complete.')


if __name__ == '__main__':
    print('Before you start you must read README.md file!!!')
    # vk_name = input('Input id for VK user:')
    vk_name = 'id29252022'
    if vk_name.startswith('id'):
        vk_user_id = vk_name[2:]
    foto_count = input('Input foto count for copy (Enter to default = 5): ')

    while type(foto_count) != int or foto_count <= 0:
        try:
            foto_count = int(foto_count)
        except ValueError:
            if foto_count == '':
                print('count = 5')
                foto_count = 5
            else:
                print('You must input integer count > 0')
                foto_count = input('Input foto count for copy (Enter to default = 5): ')
        else:
            if foto_count > 0:
                break
            else:
                print('You must input integer count > 0')
                foto_count = input('Input foto count for copy (Enter to default = 5): ')

    ya = Yandex(ya_token)
    vk = VK(vk_token, vk_user_id)
    res_fotos = vk.fotos_get(foto_count, vk_user_id)
    upload_from_vk_to_ya(res_fotos, foto_count)
