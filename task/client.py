import os
import requests
import re
import json
import time
import platform
from urllib3.exceptions import NewConnectionError
from task.transcoder import TranscodeTask


class TaskClient(object):

    def __init__(self, url, base_path):
        self.url = url
        self.base_path = base_path

    def take(self):
        task = None

        try:
            print('Trying to get a task')
            resp = requests.post('{}/tasks/next'.format(self.url),
                                 json={'host': platform.node()})

            print('Status: {}'.format(resp.status_code))
            if resp.status_code == 201:
                task_content = json.loads(resp.text)
                print('Got a task')

                if task_content['type'] == 'compress':
                    task = TranscodeTask(self.url, self.base_path, task_content)
                # elif task_content['type'] == 'remux':
                #     task = RemuxTask(self.url, self.base_path, task_content)

        except requests.exceptions.RequestException:
            print('Cannot connect to server')

        return task



    # def add_file(self, relative_path):
    #
    #     folder, file = os.path.split(relative_path)
    #
    #     resp = requests.post('{}/task'.format(self.url),
    #                          json={'source_path': relative_path})
    #
    #     if resp.status_code == 201:
    #         print('Added: {}'.format(file))
    #     elif resp.status_code == 400:
    #         print('Not added: {}'.format(file))
    #
    #
    # def search_files(self, search_folder, include_regex, exclude_regex):
    #
    #     results = list()
    #
    #     for root, dirs, files in os.walk(os.path.join(self.base_path, search_folder)):
    #
    #         for file in files:
    #
    #             folder = os.path.relpath(root, self.base_path)
    #
    #             relative_path = os.path.join(folder, file)
    #
    #             if re.search(include_regex, relative_path):
    #
    #                 if not re.search(exclude_regex, relative_path):
    #
    #                     results.append(relative_path)
    #
    #     return results