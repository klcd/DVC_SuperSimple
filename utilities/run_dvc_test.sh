#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR

dvc init

/bin/bash ${SCRIPT_DIR}/create_pipelines.sh


dvc dag
dvc repro

/bin/bash ${SCRIPT_DIR}/run_couple_exp.sh

dvc plots modify -x x -y y_train --title "Example" reports/result.csv
dvc destroy
