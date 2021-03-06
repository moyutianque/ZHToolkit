#!/bin/sh
work_path=$(dirname $0)
current_folder=$(basename "$work_path")

echo "Working with $current_folder"
echo "Using config $work_path/config.yaml"
echo "Tensorboard events were saved in: "
echo "$work_path/events"
echo ""
echo "================= START =================="

rm -rf arun-log/$current_folder-$1/*

spring.submit arun -s \
--gpu -n $1 --gres=gpu:8 --ntasks-per-node=8 --cpus-per-task=5 \
--job-name "zh_task" -o "arun-log/$current_folder-$1" \
"python -u main.py --config_path $work_path/config.yaml" 
