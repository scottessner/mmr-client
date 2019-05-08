import requests
import json
import platform
from task.transcoder import TranscodeTask
from task.title_info import TitleInfoTask
from task.scanner import ScanTask


class TaskClient(object):

    def __init__(self, url):
        self.url = url

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
                    task = TranscodeTask(self.url, task_content)
                if task_content['type'] == 'title_info':
                    task = TitleInfoTask(self.url, task_content)
                if task_content['type'] == 'preview':
                    task = ScanTask(self.url, task_content)
                # elif task_content['type'] == 'remux':
                #     task = RemuxTask(self.url, self.base_path, task_content)

        except requests.exceptions.RequestException:
            print('Cannot connect to server')

        return task
