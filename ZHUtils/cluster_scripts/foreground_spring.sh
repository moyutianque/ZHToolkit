#!/bin/sh
work_path=$(dirname $0)
current_folder=$(basename "$work_path")

echo "Working with $current_folder"
echo "Using config $work_path/config.yaml"
echo "Tensorboard events were saved in: "
echo "$work_path/events"
echo ""
echo "================= START =================="

spring.submit run \
--gpu -n 2 --gres=gpu:2 --ntasks-per-node=2 --cpus-per-task=5 \
--job-name "clip-yfcc_resnet" \
"python -u main.py --config_path $work_path/config.yaml" 
