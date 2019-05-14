#!/bin/bash
set -e
# collect inputs / conifgs
TARGET=$1
TARGET_DIR="../result-archive/$TARGET/"
GIT_HASH=$(git rev-parse --short HEAD)

echo "Archiving results/ to $TARGET_DIR ..."

# 0. make output dir
mkdir $TARGET_DIR

# 1. copy *.csv and YAML files
cp results/*.csv $TARGET_DIR
cp results/*.yml $TARGET_DIR

# 2. tar all raw results to target dir
tar -zcf $TARGET_DIR/raw_results.tar.gz results/

# 3.
tar -zcf $TARGET_DIR/prometheus-data.tar.gz ~/tng-sdk-benchmark/prometheus/prometheus-data/

# 4. store git hash
echo $GIT_HASH > $TARGET_DIR/githash.txt

# finally print the outputs
tree -h $TARGET_DIR
echo "----------------------------------"
echo "Git hash for logbook: $GIT_HASH"
echo "----------------------------------"
echo "Done."
