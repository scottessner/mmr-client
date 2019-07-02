from task.client import TaskClient
import os
import time

print(os.environ['API_URL'])

client = TaskClient(os.environ['API_URL'])

# while True:
task = client.take()

if task is not None:
    try:
        task.execute()
    except Exception:
        task.error()
    # else:
    #     break;
else:
    print('No tasks available.  Waiting 60 seconds to check again.')
    time.sleep(60)