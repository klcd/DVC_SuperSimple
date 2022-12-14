#!/bin/bash

dvc exp run -S train.param.alpha=2
dvc exp run -S train.param.alpha=3
dvc exp run -S train.param.alpha=4

