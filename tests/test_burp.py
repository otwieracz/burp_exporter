import unittest
import datetime
from dateutil.tz import tzoffset
from burp_exporter.burp import BurpSpool, BurpClient, Backup

class TestBurpSpool(unittest.TestCase):
    spool = None

    def setUp(self):
        self.spool = BurpSpool("spool")

    def test_clients(self):
        clients = self.spool.clients()
        for client in clients:
            self.assertIsInstance(client, BurpClient)

    def test_client_backups(self):
        client = self.spool.client('single.car.com')
        client_backups = client.backups()
        for backup in client_backups:
            self.assertIsInstance(backup, Backup)
            
    def test_client_status(self):
        self.assertEqual(self.spool.client('single.car.com').status(), "healthly")
        self.assertEqual(self.spool.client('empty.car.com').status(), "no-backups")
        self.assertEqual(self.spool.client('foo.bar.com').status(), "healthly")
        self.assertEqual(self.spool.client('zar.car.com').status(), "in-progress")
            
    def test_client_current_backup(self):
        client = self.spool.client('foo.bar.com')
        current_backup = client.current_backup()
        self.assertEqual(current_backup.number, 10)

    def test_backups(self):
        backups = self.spool.backups()
        for backup in backups:
            self.assertIsInstance(backup, Backup)

    def test_backup_age(self):
        backups = self.spool.backups()
        for backup in backups:
            backup_age = backup.age()
            self.assertIsInstance(backup_age, datetime.timedelta)
            self.assertGreaterEqual(backup_age.total_seconds(), 0)

