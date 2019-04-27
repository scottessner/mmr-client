import os
import requests
import time


class Task(object):

    def __init__(self, url, base_path, content):
        self.url = url
        self.base_path = base_path
        self.content = content

    @property
    def source_path(self):
        if self.content:
            return os.path.join(self.base_path, self.content['title']['path'])
        return None

    @property
    def dest_path(self):
        if self.content:
            # os
            return os.path.join(self.base_path, self.content['title']['path'])
        return None

    @property
    def tmp_path(self):
        if self.content:
            folder, file = os.path.split(self.dest_path)
            return os.path.join(self.base_path, 'tmp', 'mmr', file)
        return None

    @property
    def log_path(self):
        if self.content:
            return os.path.join(self.base_path, 'tmp', 'logs', '{}.log'.format(self.content['id']))

    def start(self):
        self.content['state'] = 'active'
        try:
            self.update_status()
        except requests.exceptions.RequestException as e:
            print(e)

    def set_progress(self, progress):
        self.content['progress'] = progress
        try:
            self.update_status()
        except requests.exceptions.RequestException as e:
            print(e)

    def complete(self):
        self.content['state'] = 'complete'
        self.content['progress'] = 100
        while True:
            try:
                self.update_status()
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(30)
            break

        self.content = None

    def error(self):
        self.content['state'] = 'error'
        while True:
            try:
                self.update_status()
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(30)
            break
        self.content = None

    def update_status(self):
        resp = requests.put('{}/tasks/{}'.format(self.url, self.content['id']),
                            data=self.content)

        if resp.status_code == 200:
            pass
