from unittest import TestCase

import pytest
from ezored.commands import Base


class TestBase(TestCase):
    def test_run_error(self):
        with pytest.raises(NotImplementedError) as error:
            command = Base(None, None, None)
            command.run()

        self.assertEqual(error.type, NotImplementedError)
