#  Copyright (c) 2019 Manuel Peuster, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).
import logging
import dateutil
import argparse
import yaml
import os
import requests
import datetime as dt
import pandas as pd
from parides.converter import data_from_prom


logging.basicConfig(level=logging.WARNING)
LOG = logging.getLogger("prom2csv")


def setup_logging(args):
    LOG.setLevel(logging.INFO)
    if args.verbose:
        LOG.setLevel(logging.DEBUG)


def parse_args(manual_args=None):
    parser = argparse.ArgumentParser(
        description="prom2csv")

    parser.add_argument(
        "-v",
        "--verbose",
        help="Increases logging level to debug",
        required=False,
        default=False,
        dest="verbose",
        action="store_true")

    parser.add_argument(
        "-m",
        "--metrics",
        help="File with metric queries",
        required=False,
        default="metrics.yml",
        dest="metrics")

    parser.add_argument(
        "--no-wildcard-metrics",
        help="Skip automated metric discovery",
        required=False,
        default=False,
        dest="no_wildcard_metrics",
        action="store_true")

    parser.add_argument(
        "-t",
        "--timestamps",
        help="File with experiment times. e.g. result_ec_metrics.csv",
        required=False,
        default=None,
        dest="timestamps")

    parser.add_argument(
        "--limit",
        help="Limit number of intervals used. INT.",
        required=False,
        default=None,
        dest="limit")

    parser.add_argument(
        "-o",
        "--output",
        help="Folder to put results. Default: out",
        required=False,
        default="out",
        dest="output")

    parser.add_argument(
        "-s",
        "--start",
        help="Start time",
        required=False,
        default=str(dt.datetime.now() - dt.timedelta(minutes=15)),
        dest="start")

    parser.add_argument(
        "-e",
        "--end",
        help="End time",
        required=False,
        default=str(dt.datetime.now()),
        dest="end")

    parser.add_argument(
        "--prometheus_url",
        help="URL of Prometheus API",
        required=False,
        default="http://127.0.0.1:9090",
        dest="prom_url")

    if manual_args is not None:
        return parser.parse_args(manual_args)
    return parser.parse_args()


def query(args, query, start, end, resolution="1s", slice_size="10min"):
    """
    Get data from Prometheus.
    Uses: https://goettl79.github.io/parides/
    """
    dfs = data_from_prom(url=args.prom_url,
                         query=query,
                         start_time=dateutil.parser.parse(start),
                         end_time=dateutil.parser.parse(end),
                         resolution=resolution,
                         freq=slice_size)
    LOG.debug("Prometheus returned {} data frames".format(len(dfs)))
    # cocatinate to a single DF
    rdf = pd.concat(dfs)
    LOG.debug("Created result data frame with size {} (row, col)"
              .format(rdf.shape))
    return rdf


def discover_metrics(args, wc_metrics):
    LOG.info("Runnin automated metric discovery ...")
    result = list()
    try:
        # translate wc_metrics
        pattern = [wm.get("metric_starts_with")
                   for wm in wc_metrics
                   if wm.get("metric_starts_with") is not None]
        # do request to Prometheus
        r = requests.get("{}/api/v1/label/__name__/values"
                         .format(args.prom_url))
        # get list of metric names
        metrics_found = r.json().get("data", list())
        LOG.info("Found {} metrics in Prometheus".format(len(metrics_found)))
        # filte metrics based on wc_metrics
        for mf in metrics_found:
            for p in pattern:
                if p in mf:
                    # found! add to result
                    result.append({"name": mf, "query": mf})
        LOG.info("Using {} metrics after filtering".format(len(result)))
    except BaseException as ex:
        LOG.error("Metric dicovery failed: {}".format(ex))
    return result


def read_yaml(path):
    yml = None
    with open(path, "r") as f:
        try:
            yml = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as ex:
            LOG.exception("YAML error while reading %r." % path)
            LOG.debug(ex)
    return yml


def write_yaml(path, data):
    with open(path, "w") as f:
        try:
            yaml.dump(data, f, default_flow_style=False)
        except yaml.YAMLError as ex:
            LOG.exception("YAML error while writing %r" % path)
            LOG.debug(ex)


def get_time_intervals(args):
    """
    Returns list(touple(run_id, start, end))
    """
    df = pd.read_csv(args.timestamps)
    # select the subset of columns we need
    df = df[["run_id", "experiment_start", "experiment_stop"]]
    # print(df.head())
    # convert to list of touples
    return list(df.itertuples(index=False, name=None))


def store_dataframe(args, m, ti, df, ftype="csv"):
    """
    Write dataframe to disk.
    """
    filename = "ts_{0:04d}_{1}.{2}".format(ti[0], m.get("name"), ftype)
    path = os.path.join(args.output, filename)
    LOG.debug("Writing data frame to: {}".format(path))
    if ftype == "csv":
        df.to_csv(path)


def prom2csv(args, metrics, time_intervals):
    """
    Fetch data for all given metrics and time intervals.
    """
    assert(len(metrics) > 0)
    assert(len(time_intervals) > 0)
    total_steps = len(metrics) * len(time_intervals)
    step = 0
    LOG.info("Fetching data for {} metrics and {} intervals ..."
             .format(len(metrics), len(time_intervals)))
    for m in metrics:
        for ti in time_intervals:
            LOG.info("--- Step {}/{}".format(step, total_steps))
            step += 1
            LOG.debug("PROM GET interval={} / metric={}"
                      .format(ti, m.get("name")))
            LOG.debug("PROM QUERY={}".format(m.get("query")))
            try:
                df = query(args, m.get("query"), ti[1], ti[2])
                # print(df.head())
                store_dataframe(args, m, ti, df)
            except BaseException as ex:
                LOG.error("Error in processing step. Skipping: {} for {}"
                          .format(ti, m.get("name")))
                LOG.error(ex)
                exit(1)  # remove later


def main():
    args = parse_args()
    setup_logging(args)
    if not os.path.exists(args.output):
        LOG.error("Output path '{}' does not exist. Abort."
                  .format(args.output))
        exit(1)
    LOG.info("Collecting metrics from {}".format(args.metrics))
    if not os.path.exists(args.metrics):
        LOG.warning("Couldn't find metric file: {}. Using default!"
                    .format(args.metrics))
        args.metrics = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "metrics.yml")
    metrics = read_yaml(args.metrics).get("metrics")
    if not args.no_wildcard_metrics:
        # do automated metric discovery
        wc_metrics = read_yaml(args.metrics).get("wildcard_metrics")
        metrics.extend(discover_metrics(args, wc_metrics))
    # write `ts_metrics.yml` into current folder
    write_yaml("ts_metrics.yml", metrics)
    # format: list(touple(run_id, start, end))
    if args.timestamps is not None:
        # get time intervals from experiment file
        time_intervals = get_time_intervals(args)
        if args.limit:
            time_intervals = time_intervals[0:int(args.limit)]
        LOG.info("Loaded {} time intervals".format(len(time_intervals)))
    else:
        # default: use --start/--end values as single interval
        time_intervals = [(0, args.start, args.end)]
        LOG.info("Start: {} / End: {}".format(args.start, args.end))
    # run the export
    prom2csv(args, metrics, time_intervals)
    LOG.info("DONE")


if __name__ == "__main__":
    main()
