#!/bin/bash

dvc init

dvc run --name transform \
 --deps data/data.txt \
 --outs data/transformed_data.txt \
 --params transform.param \
 python src/stages/transform.py --config params.yaml

 dvc run --name split \
--deps data/transformed_data.txt \
--outs data/test_data.txt \
--outs data/train_data.txt \
--params split.param \
python src/stages/split.py --config params.yaml

dvc run --name evaluate \
--deps data/test_data.txt \
--deps data/train_data.txt \
--outs reports/result.csv \
--metrics reports/metrics.json \
python src/stages/evaluate.py --config params.yaml

dvc dag

dvc repro


dvc exp run -S transform.param.param2=2
dvc exp run -S transform.param.param2=3
dvc exp run -S transform.param.param2=4

dvc plots modify -x x -y y_train --title "Example" reports/result.csv

dvc destroy
