#!/bin/sh

dvc run --name split \
 --deps data/data.csv \
 --outs data/test_data.csv \
 --outs data/train_data.csv \
 --params split.param \
 python stages/split.py --config params.yaml

dvc run --name train \
--deps data/train_data.csv \
--outs models/model.joblib \
--params train.param \
python stages/train.py --config params.yaml

dvc run --name evaluate \
--deps data/test_data.csv \
--deps data/train_data.csv \
--deps models/model.joblib \
--outs reports/result.csv \
--metrics reports/metrics.json \
python stages/evaluate.py --config params.yaml

