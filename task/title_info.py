from task.base import Task
from pymediainfo import MediaInfo
import requests


class TitleInfoTask(Task):

    def __init__(self, url, task_content):
        super().__init__(url, task_content)

    def execute(self):

        self.start()

        try:
            title = dict()

            mi = MediaInfo.parse(self.source_path)

            for track in mi.tracks:
                if track.track_type == 'General':
                    title['file_size'] = track.file_size
                    title['writing_application'] = track.writing_application
                    if track.duration is not None:
                        title['duration'] = int(float(track.duration))
                elif track.track_type == 'Video':
                    title['height'] = track.height
                    title['width'] = track.width
                    title['video_codec'] = track.codec
                    title['video_encoding_settings'] = track.encoding_settings

            resp = requests.put('{}/titles/{}'.format(self.url, self.content['title']['id']),
                                json=title)

            if resp.status_code == 201:
                print('Updated Successfully: {}'.format(self.source_path))
                self.complete()
            else:
                print('Update Failed: {}'.format(self.source_path))
                self.error()

        except RuntimeError as e:
            print(e)
