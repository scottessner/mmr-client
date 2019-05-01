from pymediainfo import MediaInfo
from task.client import TaskClient
import requests
import os

# url = 'http://127.0.0.1:5000/mmr-api/v1'
url = 'http://ssessner.com/mmr-api/v1'

c = TaskClient(url, '/data/media')
matches = c.search_files('tvshows', r'\.*\Z', r'\.grab')

# def add_file(self, relative_path):
#
#     folder, file = os.path.split(relative_path)
#
#     resp = requests.post('{}/task'.format(self.url),
#                          json={'source_path': relative_path})
#
#     if resp.status_code == 201:
#         print('Added: {}'.format(file))
#     elif resp.status_code == 400:
#         print('Not added: {}'.format(file))
#
#
# def search_files(self, search_folder, include_regex, exclude_regex):
#
#     results = list()
#
#     for root, dirs, files in os.walk(os.path.join(self.base_path, search_folder)):
#
#         for file in files:
#
#             folder = os.path.relpath(root, self.base_path)
#
#             relative_path = os.path.join(folder, file)
#
#             if re.search(include_regex, relative_path):
#
#                 if not re.search(exclude_regex, relative_path):
#
#                     results.append(relative_path)
#
#     return results

for path in matches:

    try:
        title = dict()

        mi = MediaInfo.parse(os.path.join('/data/media', path))

        title['path'] = path

        for track in mi.tracks:
            if track.track_type == 'General':
                title['file_size'] = track.file_size
                title['duration'] = track.duration
                title['writing_application'] = track.writing_application
            elif track.track_type == 'Video':
                title['height'] = track.height
                title['width'] = track.width
                title['video_codec'] = track.codec
                title['video_encoding_settings'] = track.encoding_settings

        resp = requests.post('{}/titles'.format(url),
                             json=title)

        if resp.status_code == 201:
            print('Added: {}'.format(path))
        elif resp.status_code == 400:
            print('Not added: {}'.format(path))

    except RuntimeError as e:
        print(e)
