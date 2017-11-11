from unittest import TestCase

import pytest
from ezored.models.constants import Constants
from ezored.models.logger import Logger


class TestLogger(TestCase):
    def test_clean(self):
        Logger.clean("test_clean")
        self.assertTrue(True)

    def test_debug_with_debug_turned_on(self):
        Constants.DEBUG = True
        Logger.d("test_debug_with_debug_turned_on")
        self.assertTrue(True)

    def test_debug_with_debug_turned_off(self):
        Constants.DEBUG = False
        Logger.d("test_debug_with_debug_turned_off")
        self.assertTrue(True)

    def test_warning(self):
        Logger.w("test_warning")
        self.assertTrue(True)

    def test_information(self):
        Logger.i("test_information")
        self.assertTrue(True)

    def test_error(self):
        Logger.e("test_error")
        self.assertTrue(True)

    def test_fatal(self):
        with pytest.raises(SystemExit) as error:
            Logger.f("test_fatal")

        self.assertTrue(error.type == SystemExit)
        self.assertTrue(error.value.code == 1)

    def test_show(self):
        Logger.show("test", "test_show")
        self.assertTrue(True)
