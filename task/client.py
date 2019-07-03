import requests
import json
import os
from task.transcoder import TranscodeTask
from task.title_info import TitleInfoTask
from task.scanner import ScanTask
from task.remux import RemuxTask


class TaskClient(object):

    def __init__(self, url):
        self.url = url

    def take(self):
        task = None

        try:
            print('Trying to get a task')
            resp = requests.post('{}/tasks/next'.format(self.url),
                                 json={'host': os.environ['NAME']})

            print('Status: {}'.format(resp.status_code))
            if resp.status_code == 201:
                task_content = json.loads(resp.text)
                task_title = task_content['title']
                if task_title:
                    task_path = task_title.get('path')
                else:
                    task_path = ''

                print('Got task: \n  ID: {} \n  Title: {} \n  Type: {}'
                      .format(task_content['id'],
                              task_path,
                              task_content['type']))

                if task_content['type'] == 'compress':
                    task = TranscodeTask(self.url, task_content)
                elif task_content['type'] == 'title_info':
                    task = TitleInfoTask(self.url, task_content)
                elif task_content['type'] == 'scan':
                    task = ScanTask(self.url, task_content)
                elif task_content['type'] == 'remux':
                    task = RemuxTask(self.url, task_content)
                else:
                    print('Unknown Task Type: {}. Skipping'.format(task_content['type']))

        except requests.exceptions.RequestException:
            print('Cannot connect to server')
            task.error()

        return task
