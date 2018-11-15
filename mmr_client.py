import os
import requests
import re
import json
import time
import platform
from urllib3.exceptions import NewConnectionError


class MmrClient(object):

    def __init__(self, url, base_path):
        self.url = url
        self.base_path = base_path
        self.task = None

    @property
    def source_path(self):
        if self.task:
            return os.path.join(self.base_path, self.task['source_path'])
        return None

    @property
    def dest_path(self):
        if self.task:
            return os.path.join(self.base_path, self.task['dest_path'])
        return None

    @property
    def tmp_path(self):
        if self.task:
            folder, file = os.path.split(self.dest_path)
            return os.path.join(self.base_path, 'tmp', 'mmr', file)
        return None

    @property
    def log_path(self):
        if self.task:
            return os.path.join(self.base_path, 'tmp', 'logs', '{}.log'.format(self.task['id']))

    def add_file(self, relative_path):

        folder, file = os.path.split(relative_path)

        resp = requests.post('{}/tasks'.format(self.url),
                             json={'source_path': relative_path})

        if resp.status_code == 201:
            print('Added: {}'.format(file))
        elif resp.status_code == 400:
            print('Not added: {}'.format(file))

    def search_files(self, search_folder, include_regex, exclude_regex):

        results = list()

        for root, dirs, files in os.walk(os.path.join(self.base_path, search_folder)):

            for file in files:

                folder = os.path.relpath(root, self.base_path)

                relative_path = os.path.join(folder, file)

                if re.search(include_regex, relative_path):

                    if not re.search(exclude_regex, relative_path):

                        results.append(relative_path)

        return results

    def take_file(self):
        try:
            resp = requests.post('{}/tasks/next'.format(self.url),
                                 json={'host': platform.node()})

            if resp.status_code == 201:
                self.task = json.loads(resp.text)
        except requests.exceptions.RequestException:
            print('Cannot connect to server')

    def start_file(self):
        self.task['state'] = 'active'
        try:
            self.update_status()
        except requests.exceptions.RequestException:
            pass

    def set_progress(self, progress):
        self.task['progress'] = progress
        try:
            self.update_status()
        except requests.exceptions.RequestException:
            pass

    def complete_file(self):
        self.task['state'] = 'complete'
        self.task['progress'] = 100
        while True:
            try:
                self.update_status()
            except requests.exceptions.RequestException:
                time.sleep(30)
            break

        self.task = None

    def error_file(self):
        self.task['state'] = 'error'
        while True:
            try:
                self.update_status()
            except requests.exceptions.RequestException:
                time.sleep(30)
            break
        self.task = None

    def update_status(self):
        resp = requests.put('{}/tasks/{}'.format(self.url, self.task['id']),
                            data=self.task)

        if resp.status_code == 200:
            pass
