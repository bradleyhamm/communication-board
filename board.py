import os
import urllib
import urllib3
import requests
import string
import random
import concurrent.futures
from werkzeug.utils import secure_filename

IMAGE_API_URL = 'https://openclipart.org/search/json/?query=%s'


class ImageFinder(object):

    def __init__(self, search_term):
        self.download_session = urllib3.PoolManager()
        self.search_term = search_term
        self.image_urls = self.get_image_urls()

    def get_image_urls(self):
        url = IMAGE_API_URL % urllib.parse.quote(self.search_term)
        res = requests.get(url)
        res.raise_for_status()
        try:
            json = res.json()
        except ValueError:
            raise Exception('Image API returned unexpected response data')
        else:
            return [image['svg']['png_thumb'] for image in json['payload']]

    def get_image(self, url):
        from views import UPLOAD_FOLDER
        filename = self._get_filename()
        r = self.download_session.request('GET', url)
        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
            f.write(r.data)
        return filename

    def _get_filename(self):
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        filename = secure_filename('%s-%s.png' % (self.search_term, random_string))
        return filename

    def __iter__(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for url in self.image_urls:
                futures.append(executor.submit(self.get_image, url))
            for future in concurrent.futures.as_completed(futures):
                yield future.result()
