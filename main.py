from task.client import TaskClient
import os
import time

print(os.environ['API_URL'])

client = TaskClient(os.environ['API_URL'])

while True:
    task = client.take()

    if task is not None:
        try:
            task.execute()
        except Exception:
            task.error()

    else:
        print("No new tasks.  Sleeping for 60 seconds")
        time.sleep(60)