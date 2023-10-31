"""
Test custom Django management commands
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, pathed_check):
        """Test waiting for database if database ready"""
        pathed_check.return_value = True

        call_command('wait_for_db')

        pathed_check.assert_called_once_with(database=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, pathed_check):
        """Test waiting for database when getting OperationalError"""
        pathed_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(pathed_check.call_count, 6)
        pathed_check.assert_called_with(database=['default'])
