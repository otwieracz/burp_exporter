from prometheus_client import start_http_server, Gauge, Enum
from burp_exporter.burp import BurpSpool
import argparse
import time
import logging

burp_clients_gauge = Gauge('burp_clients', 'Number of clients with backups')
burp_backup_age_gauge = Gauge('burp_backup_age', 'Age of burp backups per client in seconds', ['client_name'])
burp_clients_status_enum = Enum('burp_clients_status', 'Status of burp clients', labelnames=['client_name'], states=['in-progress', 'healthly', 'no-backups'])


def burp_clients(spool):
    clients = spool.clients()
    burp_clients_gauge.set(len(clients))

def _update_client_gauge(client):
    current_backup = client.current_backup()
    if current_backup:
        return burp_backup_age_gauge.labels(client.client_name).set(current_backup.age().total_seconds())
    else:
        return None

def burp_backup_age(spool):
    [_update_client_gauge(client) for client in spool.clients()]

def burp_clients_status(spool):
    # disable py-lint in this line as it does not like it by some reason
    [burp_clients_status_enum.labels(client.client_name).state(client.status()) for client in spool.clients()] # pylint: disable=no-member


parser = argparse.ArgumentParser(description='Prometheus exporter for Burp backup program working on top of Burp\' spool directory')
parser.add_argument('spool', help='Path to Burp\'s spool directory')
parser.add_argument('-t', '--time', type=int, default=60, help='Time interval between data collections in seconds')
parser.add_argument('-p', '--port', type=int, default=8000, help='Port on which to expose metrics')

def start_exporter():
    args = parser.parse_args()
    spool = BurpSpool(args.spool)
    start_http_server(args.port)
    logging.basicConfig(format='%(asctime)s burp_exporter %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    logging.info(f"burp_exporter started on port {args.port}, refresh interval is {args.time}")
    while True:
        burp_clients(spool)
        burp_clients_status(spool)
        burp_backup_age(spool)
        time.sleep(args.time)
