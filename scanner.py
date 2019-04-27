from task.client import TaskClient
from multiprocessing import Pool

# url = 'http://127.0.0.1:5000/mmr-api/v1'
url = 'http://ssessner.com/mmr-api/v1'

# c = TaskClient(url, '/data/media')
# matches = c.search_files('tvshows', r'\.ts\Z', r'\.grab')
#
# with Pool(4) as p:
#     result = p.map(c.add_file, matches)
#
# c = TaskClient(url, '/data/media')
# matches = c.search_files('movies', r'\.ts\Z', r'\.grab')
#
# with Pool(4) as p:
#     result = p.map(c.add_file, matches)

c = TaskClient(url, '/data/media')
matches = c.search_files('tvshows/The Big Bang Theory/Season 08', r'\.mkv\Z', r'\.grab')

with Pool(4) as p:
    result = p.map(c.add_file, matches)