import os
import re
import subprocess
from task.client import TaskClient

progress_regex = re.compile('frame=*(?P<frame>\d{0,6})\sfps=\s(?P<fps>\d{0,6}).*time=(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2}).(?P<ms>\d{2})\sbitrate=(?P<bitrate>.*(?=kbits/s)).*speed=(?P<speed>.*(?=x))')


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


def remux(client):

    client.start()

    folder = os.path.split(client.tmp_path)[0]
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(client.log_path, 'w+') as logfile:

        command = ['ffmpeg',
                   '-y',
                   '-i',
                   client.source_path,
                   '-c',
                   'copy',
                   client.tmp_path]

        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        progress = dict()
        while True:
            line = ''
            while line[-1:] != '\r' and process.poll() is None:
                line = line + bytes.decode(process.stderr.read(1))
            # line = bytes.decode(process.stderr.readline())

            latest_progress = find_transcode_progress(line)
            if progress.get('progress', None) != latest_progress.get('progress', None):
                progress = latest_progress
            # print(line)
            #     if progress.get('progress', None):
            #         client.set_progress(progress['progress'])
            #         # print('Transcoding: {}% Complete ETA: {}'.format(progress['progress'], progress['eta']))

            if process.poll() is not None:
                if process.poll() == 0:
                    print('Remuxed Successfully.')
                    os.rename(client.tmp_path, client.dest_path)
                    os.remove(client.source_path)
                    client.complete()
                else:
                    client.error()
                logfile.write('ffmpeg completed with return code {}'.format(process.poll()))

                return process.poll()


if __name__ == '__main__':
    url = 'http://192.168.20.168:5000/mmr-api/v1'
    # url = 'http://ssessner.com/mmr-api/v1'

    client = TaskClient(url, '/data/media')

    client.task = {"source_path": "movies/Grown Ups (2010)/Grown Ups (2010).mkv",
                   "dest_path": "movies/Grown Ups (2010)/Grown Ups (2010).mp4",
                   "id": 99999}

    status = remux(client)

    # while True:
    #     client.take_file()
    #
    #     if client.task:
    #         print('Compressing: {}'.format(client.task['source_path']))
    #         status = remux(client)
    #     else:
    #         time.sleep(60)
