from task.client import TaskClient
import os
import time

print(os.environ['API_URL'])

client = TaskClient(os.environ['API_URL'])

task = client.take()

if task is not None:
    print('Took task {}'.format(task.content['title']['path']))
    task.execute()
else:
    print('No tasks available.  Waiting 60 seconds to check again.')
    time.sleep(60)