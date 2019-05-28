#!/bin/bash

set -e

# collect inputs / conifgs
SOURCE_DIR=$1
TARGET_DIR=$2

echo "Input: " $SOURCE_DIR
echo "Output: " $TARGET_DIR

set -x
set +e
mkdir $TARGET_DIR/meta
mkdir $TARGET_DIR/data

# top level
cp -n templates/LICENSE $TARGET_DIR/LICENSE
cp -n templates/README.md $TARGET_DIR/README.md
cp -n templates/.gitignore $TARGET_DIR/.gitignore

# meta (static)
cp -n templates/platform_hw_info.xml $TARGET_DIR/meta/platform_hw_info.xml
cp -n templates/platform_sw_info_os.txt $TARGET_DIR/meta/platform_sw_info_os.txt
cp -n templates/platform_sw_info_pkg.txt $TARGET_DIR/meta/platform_sw_info_pkg.txt
set -e

# meta (experiment)
cp $SOURCE_DIR/original_ped.yml $TARGET_DIR/meta/ped.yml
cp $SOURCE_DIR/ts_metrics.yml $TARGET_DIR/meta/ts_metrics.yml

# meta (data)
cp $SOURCE_DIR/result_ec_metrics.csv $TARGET_DIR/data/csv_experiments.csv
cp $SOURCE_DIR/timeseries.tar.gz $TARGET_DIR/data/csv_timeseries.tar.gz
cp $SOURCE_DIR/raw_results.tar.gz $TARGET_DIR/data/raw_records.tar.gz
cp $SOURCE_DIR/prometheus-data.tar.gz $TARGET_DIR/data/raw_prometheus_data.tar.gz

set +x
tree -h $TARGET_DIR
echo "DONE"
