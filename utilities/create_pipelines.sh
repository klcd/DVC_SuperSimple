#!/bin/sh

dvc run --name split \
 --deps data/data.txt \
 --outs data/test_data.txt \
 --outs data/train_data.txt \
 --params split.param \
 python stages/split.py --config params.yaml

dvc run --name train \
--deps data/train_data.txt \
--outs models/model.joblib \
--params train.param \
python stages/train.py --config params.yaml

dvc run --name evaluate \
--deps data/test_data.txt \
--deps data/train_data.txt \
--deps models/model.joblib \
--outs reports/result.csv \
--metrics reports/metrics.json \
python stages/evaluate.py --config params.yaml

