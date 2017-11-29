import os
import sys

from ezored.models.logger import Logger
from tqdm import tqdm

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse


class DownloadUtil(object):
    @staticmethod
    def download_file(url, dest=None, filename=None):
        """
        Download and save a file specified by url to dest directory,
        """
        Logger.d('New download request')

        u = urllib2.urlopen(url)

        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)

        if not filename:
            filename = DownloadUtil.get_filename_from_url(path)

        if dest:
            filename = os.path.join(dest, filename)

        Logger.d('Getting file metadata...')

        with open(filename, 'wb') as f:
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func('Content-Length')
            file_size = None
            pbar = None

            if meta_length:
                file_size = int(meta_length[0])

            if file_size:
                Logger.d('File size in bytes: {0}'.format(file_size))
                Logger.clean('')
                pbar = tqdm(total=file_size)

            file_size_dl = 0
            block_sz = 8192

            if not pbar:
                Logger.d('Downloading, please wait...')

            while True:
                dbuffer = u.read(block_sz)

                if not dbuffer:
                    break

                dbuffer_len = len(dbuffer)
                file_size_dl += dbuffer_len
                f.write(dbuffer)

                if pbar:
                    pbar.update(dbuffer_len)

            if pbar:
                pbar.close()
                Logger.clean('')

            return filename

    @staticmethod
    def get_filename_from_url(url):
        Logger.d('Parsing URL to get filename...')

        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        filename = os.path.basename(path)

        if not filename:
            filename = 'downloaded.file'

        Logger.d('Filename from download URL: {0}'.format(filename))

        return filename
