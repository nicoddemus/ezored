import os
from unittest import TestCase

from ezored.models.util.download_util import DownloadUtil
from testfixtures import tempdir


class TestDownloadUtil(TestCase):
    def test_get_filename_from_url(self):
        download_url = 'https://raw.githubusercontent.com/ezored/ezored/python-version/extras/images/jetbrains-logo.png'
        download_filename = DownloadUtil.get_filename_from_url(download_url)

        self.assertEqual(download_filename, 'jetbrains-logo.png')

    @tempdir()
    def test_download_file(self, d):
        os.chdir(d.path)

        download_url = 'https://raw.githubusercontent.com/ezored/ezored/python-version/extras/images/jetbrains-logo.png'
        download_filename = DownloadUtil.get_filename_from_url(download_url)

        DownloadUtil.download_file(download_url)

        self.assertTrue(os.path.isfile(download_filename))
        self.assertEqual(os.path.getsize(download_filename), 5627)

    @tempdir()
    def test_download_file_with_custom_destination(self, d):
        os.chdir(d.path)

        download_url = 'https://raw.githubusercontent.com/ezored/ezored/python-version/extras/images/jetbrains-logo.png'
        download_dest = 'download'
        download_filename = DownloadUtil.get_filename_from_url(download_url)

        os.mkdir(download_dest)

        DownloadUtil.download_file(download_url, download_dest)

        self.assertTrue(os.path.isfile(os.path.join(download_dest, download_filename)))
        self.assertEqual(os.path.getsize(os.path.join(download_dest, download_filename)), 5627)

    @tempdir()
    def test_download_file_with_custom_filename(self, d):
        os.chdir(d.path)

        download_url = 'https://raw.githubusercontent.com/ezored/ezored/python-version/extras/images/jetbrains-logo.png'
        download_filename = 'file.png'

        DownloadUtil.download_file(download_url, filename=download_filename)

        self.assertTrue(os.path.isfile(download_filename))
        self.assertEqual(os.path.getsize(download_filename), 5627)

    @tempdir()
    def test_download_file_with_custom_dest_and_filename(self, d):
        os.chdir(d.path)

        download_url = 'https://raw.githubusercontent.com/ezored/ezored/python-version/extras/images/jetbrains-logo.png'
        download_dest = 'download'
        download_filename = 'file.png'

        os.mkdir(download_dest)

        DownloadUtil.download_file(download_url, download_dest, download_filename)

        self.assertTrue(os.path.isfile(os.path.join(download_dest, download_filename)))
        self.assertEqual(os.path.getsize(os.path.join(download_dest, download_filename)), 5627)
