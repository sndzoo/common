# prom2csv

## Installation

First, install my custom fork of `parides` using branch `dev`:

```sh
git clone git@github.com:mpeuster/parides.git
cd parides/
python setup.py develop
```

Second, install `prom2csv` itself:

```sh
python setup.py develop
```

## Usage

```sh
# fetch all metrics given in local metrics.yml for given time frame
prom2csvy -s 2019-04-15T12:00:00 -e 2019-04-15T13:00:00

# custom metrics file
prom2csv -s 2019-04-15T12:00:00 -e 2019-04-15T13:00:00 -m metricy.yml

# fetch all metrics for experiments given by experiment csv (-t) but limit to 2 intervals
prom2csv -m metrics.yml -t ../../result-archive/2019-04-15-tango_suricata_cpubw_1_tango5/result_ec_metrics.csv --limit 2

# fetch all metrics for all intervals
prom2csv -m metrics.yml -t ../../result-archive/2019-04-15-tango_suricata_cpubw_1_tango5/result_ec_metrics.csv 
```