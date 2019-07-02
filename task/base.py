import os
import requests
import time
import json


class Task(object):

    def __init__(self, url, content):
        self.url = url
        self.content = content

    @property
    def source_path(self):
        if self.content:
            return os.path.join(self.content['title']['path'])
        return None

    @property
    def dest_path(self):
        if self.content:
            # os
            return os.path.join(self.content['title']['path'])
        return None

    @property
    def tmp_path(self):
        if self.content:
            folder, file = os.path.split(self.dest_path)
            return os.path.join('/data', 'tmp', 'mmr', file)
        return None

    @property
    def log_path(self):
        if self.content:
            return os.path.join('/data', 'tmp', 'logs', '{}.log'.format(self.content['id']))

    def update_title_path(self, title_path):
        payload = {'path': title_path}
        resp = requests.put('{}/titles/{}'.format(self.url, self.content['title']['id']),
                            json=payload)

    def start(self):
        payload = {'state': 'active'}
        try:
            self.update_status(payload)
        except requests.exceptions.RequestException as e:
            print(e)

    def set_progress(self, progress):
        payload = {'progress': progress}
        try:
            self.update_status(payload)
        except requests.exceptions.RequestException as e:
            print(e)

    def complete(self):
        payload = {'state': 'complete', 'progress': 100}
        while True:
            try:
                self.update_status(payload)
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(30)
            break

        self.content = None

    def error(self):
        payload = {'state': 'error'}
        while True:
            try:
                self.update_status(payload)
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(30)
            break
        self.content = None

    def update_status(self, payload):
        resp = requests.put('{}/tasks/{}'.format(self.url, self.content['id']),
                            json=payload)

        if resp.status_code == 200 or resp.status_code == 201:
            self.content = json.loads(resp.text)
