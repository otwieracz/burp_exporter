# burp_exporter

Prometheus exporter for BURP backup program (https://burp.grke.org/) written in Python.

`burp_exporter` operates directly on BURP spool directory thus has to be running on the same machine as server, but does not require complex configuration as a client of monitor protocol.

## Usage

```
usage: burp_exporter [-h] [-t TIME] [-p PORT] spool
```

## Installation

```
# pip3 install burp_exporter
# cp burp_exporter.service /etc/systemd/system/
```

Create `/etc/default/burp_exporter`:
```
ARGS="/path/to/my_spool"
```

## Exposed metrics

* `burp_clients` - Number of clients with backups
* `burp_backup_age` - Age of burp backups per client in seconds
* `burp_clients_status` - Status of burp clients

```
# HELP burp_clients Number of clients with backups
# TYPE burp_clients gauge
burp_clients 4.0
# HELP burp_backup_age Age of burp backups per client in seconds
# TYPE burp_backup_age gauge
burp_backup_age{client_name="foo.bar.com"} 6.554384881348e+06
burp_backup_age{client_name="single.car.com"} 7.018920881891e+06
burp_backup_age{client_name="zar.car.com"} 6.603584882319e+06
# HELP burp_clients_status Status of burp clients
# TYPE burp_clients_status gauge
burp_clients_status{burp_clients_status="in-progress",client_name="empty.car.com"} 0.0
burp_clients_status{burp_clients_status="healthly",client_name="empty.car.com"} 0.0
burp_clients_status{burp_clients_status="no-backups",client_name="empty.car.com"} 1.0
burp_clients_status{burp_clients_status="in-progress",client_name="foo.bar.com"} 0.0
burp_clients_status{burp_clients_status="healthly",client_name="foo.bar.com"} 1.0
burp_clients_status{burp_clients_status="no-backups",client_name="foo.bar.com"} 0.0
burp_clients_status{burp_clients_status="in-progress",client_name="single.car.com"} 0.0
burp_clients_status{burp_clients_status="healthly",client_name="single.car.com"} 1.0
burp_clients_status{burp_clients_status="no-backups",client_name="single.car.com"} 0.0
burp_clients_status{burp_clients_status="in-progress",client_name="zar.car.com"} 1.0
burp_clients_status{burp_clients_status="healthly",client_name="zar.car.com"} 0.0
burp_clients_status{burp_clients_status="no-backups",client_name="zar.car.com"} 0.0
```
