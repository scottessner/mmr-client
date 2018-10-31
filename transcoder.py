import os
import re
import subprocess
import time
from mmr_client import MmrClient

progress_regex = re.compile('Encoding:.*, (?P<progress>\d{0,2}).* \((?P<fps>.{0,6}) fps, avg (?P<fps_avg>.{0,6}) fps.*(?P<hours>\d{2})h(?P<minutes>\d{2})m(?P<seconds>\d{2})s\)')


def find_transcode_progress(line):
    result = progress_regex.match(line)
    progress = dict()
    if result is not None:
        progress['progress'] = result.groupdict().get('progress', None)
        progress['hours'] = result.groupdict().get('hours', None)
        progress['minutes'] = result.groupdict().get('minutes', None)
        progress['seconds'] = result.groupdict().get('seconds', None)
        progress['eta'] = '{}:{}:{}'.format(progress['hours'], progress['minutes'], progress['seconds'])
    return progress


def transcode(client):

    client.start_file()
    input_path = client.source_path
    output_path = client.dest_path

    folder = os.path.split(output_path)[0]
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(client.log_path, 'w+') as logfile:

        command = ['HandBrakeCLI',
                   '-i',
                   input_path,
                   '-o',
                   output_path,
                   '--preset=HQ 1080p30 Surround',
                   '--subtitle',
                   'scan',
                   '-F']

        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=logfile)

        progress = dict()
        while True:
            line = ''
            while line[-1:] != '\r' and process.poll() is None:
                line = line + bytes.decode(process.stdout.read(1))

            latest_progress = find_transcode_progress(line)
            if progress.get('progress', None) != latest_progress.get('progress', None):
                progress = latest_progress
                # print(line)
                if progress.get('progress', None):
                    client.set_progress(progress['progress'])
                    print('Transcoding: {}% Complete ETA: {}'.format(progress['progress'], progress['eta']))
                # TODO: Send progress update to api

            if process.poll() is not None:
                if process.poll() == 0:
                    # print('Status Matched: {}'.format(status))
                    os.remove(input_path)
                    client.complete_file()
                else:
                    client.error_file()
                logfile.write('HandBrakeCLI completed with return code {}'.format(process.poll()))

                # TODO: Send completion status to api
                return process.poll()


if __name__ == '__main__':
    # url = 'http://127.0.0.1:5000/mmr-api/v1'
    url = 'http://ssessner.com/mmr-api/v1'

    client = MmrClient(url, '/data/media')

    while True:
        client.take_file()

        if client.task:
            print('Compressing: {}'.format(client.task['source_path']))
            status = transcode(client)
        else:
            time.sleep(60)
