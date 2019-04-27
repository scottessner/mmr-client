from daemons.utils import search_files
import os
import config
import requests
import json


class DiscWatcher:

    def __init__(self):
        self.watch_folder = '/data/media/tmp/media'

    def scan(self):

        folder_state = list()

        for disc in os.scandir(self.watch_folder):

            if disc.is_dir():

                disc_state = dict()
                disc_state['name'] = disc.name
                disc_state['path'] = disc.path
                disc_state['titles'] = list()

                for title in os.scandir(disc.path):

                    if title.is_file():

                        stat = title.stat()

                        title_state = dict()
                        title_state['name'] = title.name
                        title_state['path'] = title.path
                        title_state['size'] = stat.st_size
                        title_state['mtime'] = stat.st_mtime

                        disc_state['titles'].append(title_state)

                folder_state.append(disc_state)

        folder_state_json = json.dumps(folder_state)

        resp = requests.post('http://localhost:5000/mmr-api/v1/discs/scan', json=folder_state_json)

        resp.status_code