#!/bin/bash
set -e
# collect inputs / configs / results
SOURCE=$1
SOURCE_DIR="$SOURCE"
TARGET=$2
TARGET_DIR="$HOME/nfv-benchmarking-result-archive/$TARGET"


echo "Archiving tng-bench results..."
echo "SOURCE_DIR=$SOURCE_DIR"
echo "TARGET_DIR=$TARGET_DIR"

# 0. make output dir
mkdir $TARGET_DIR

# 1. copy *.csv and YAML files
cp $SOURCE_DIR/*.csv $TARGET_DIR
cp $SOURCE_DIR/*.yml $TARGET_DIR

# 2. tar all raw results to target dir
tar -zcf $TARGET_DIR/raw_results.tar.gz $SOURCE_DIR

# 3.
tar -zcf $TARGET_DIR/prometheus-data.tar.gz $HOME/tng-sdk-benchmark/prometheus/prometheus-data/

# finally print the outputs
echo "----------------------------------"
tree -h $TARGET_DIR
echo "----------------------------------"
echo "Done."
