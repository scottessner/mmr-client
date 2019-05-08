from task.base import Task
import requests
import os
import re
import json


class ScanTask(Task):

    def __init__(self, url, task_content):
        super().__init__(url, task_content)

    def execute(self):

        self.start()

        matches = self.search_files('/data/tvshows', r'\.mkv|\.mp4|\.ts\Z', r'\.grab')

        for match in matches:
            self.add_file(match)

        matches = self.search_files('/data/movies', r'\.mkv|\.mp4|\.ts\Z', r'\.grab')

        for match in matches:
            self.add_file(match)

        self.complete()

    def add_file(self, path):

        folder, file = os.path.split(path)

        resp = requests.get('{}/titles/search'.format(self.url),
                            params={'path': path})

        if resp.status_code == 200:
            titles = json.loads(resp.text)
            for title in titles:

                if title['path'] == path:
                    # print('Already in system: {}'.format(path))
                    return

        resp = requests.post('{}/titles'.format(self.url),
                             json={'path': path})

        if resp.status_code == 201:
            print('Added: {}'.format(file))
        elif resp.status_code == 400:
            print('Not added: {}'.format(file))

    def search_files(self, search_folder, include_regex, exclude_regex):

        results = list()

        for root, dirs, files in os.walk(search_folder):

            for file in files:

                path = os.path.join(root, file).encode('utf-8', 'surrogateescape').decode('utf-8')

                if re.search(include_regex, path):

                    if not re.search(exclude_regex, path):

                        results.append(path)

        return results
