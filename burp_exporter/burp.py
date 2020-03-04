import os
from dateutil.parser import isoparse
from datetime import datetime, timezone
from functools import reduce


def _parse_backup_identifier(backup_identifier):
    """Parse string like '0000001 2019-12-14 10:13:45 +0100' into tuple (backup_number, datetime)"""
    assert isinstance(backup_identifier, str), f"`{backup_identifier}' is not a string"

    split = backup_identifier.split(' ')
    assert (len(split) == 4 or len(split) == 3), "Invalid backup identifier"

    if(len(split) == 4):
        raw_number, date, time, timezone = split
    elif(len(split) == 3):
        raw_number, date, time = split
        timezone = "+0000"

    number = int(raw_number)
    dt = isoparse(f"{date} {time}{timezone}")
    
    assert isinstance(number, int), "Invalid backup number"
    assert isinstance(dt, datetime), "Invalid backup date"

    return (number, dt)

def _filter_special_backup_dirs(backup_dirs):
    special_names = ['current', 'working']
    filtered = filter(lambda x: x not in special_names, backup_dirs)
    return filtered


class Backup:
    client_name = None
    number = None
    datetime = None

    def __init__(self, client_name, backup_identifier):
        self.client_name = client_name
        self.number, self.datetime = _parse_backup_identifier(backup_identifier)

    def age(self):
        """Get age of specified backup"""
        # timezone.utc to generate tz-aware time
        backup_age = datetime.now(timezone.utc) - self.datetime
        return backup_age


class BurpClient:
    client_dir = None
    client_name = None

    def __init__(self, spool_directory, client_name):
        self.client_name = client_name
        self.client_dir = os.path.join(str(spool_directory), str(client_name))
        assert os.path.exists(self.client_dir), f"Client {client_name} does not exist"

    def backups(self):
        """List all backups for client"""
        backup_identifiers = _filter_special_backup_dirs(os.listdir(self.client_dir))
        return [Backup(self.client_name, backup_identifier) for backup_identifier in backup_identifiers]

    def current_backup(self):
        """Get most recent backup of specific client"""
        current_backup_real_dir = os.path.realpath(os.path.join(self.client_dir, "current"))
        if os.path.exists(current_backup_real_dir):
            return Backup(self.client_name, os.path.basename(current_backup_real_dir))
        else:
            return None

    def status(self):
        directory_really_exists = lambda p: os.path.isdir(os.path.realpath(os.path.join(self.client_dir, p)))
        if directory_really_exists("working"):
            return "in-progress"
        elif directory_really_exists("current"):
            return "healthly"
        else:
            return "no-backups"


class BurpSpool:
    spool_directory = None

    def __init__(self, spool_directory):
        """Initialize BurpSpool instance pointing to `spool_directory`"""
        self.spool_directory = spool_directory

    def client(self, client_name):
        """Get specific client from spool directory"""
        return BurpClient(self.spool_directory, client_name)

    def clients(self):
        """Get all clients from spool directory"""
        return [BurpClient(self.spool_directory, client) for client in os.listdir(self.spool_directory)]

    def backups(self):
        """List backups for all clients"""
        per_client_backups = [client.backups() for client in self.clients()]
        return reduce(lambda a,b : a + b, per_client_backups)
