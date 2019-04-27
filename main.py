from task.client import TaskClient
import os

print(os.environ['API_URL'])

client = TaskClient(os.environ['API_URL'], '/data/media')

task = client.take()

if task is not None:
    print('Took task {}'.format(task.content['title']['path']))
    task.execute()
