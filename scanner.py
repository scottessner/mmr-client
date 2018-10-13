from mmr_client import MmrClient
from multiprocessing import Pool

# url = 'http://127.0.0.1:5000/v1'
url = 'http://ssessner.com/v1'

c = MmrClient(url, '/data/media')
matches = c.search_files('tvshows', r'\.ts\Z', r'\.grab')

with Pool(4) as p:
    result = p.map(c.add_file, matches)
