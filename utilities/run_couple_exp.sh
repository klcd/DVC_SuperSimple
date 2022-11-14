#!/bin/bash

dvc exp run -S transform.param.param2=2
dvc exp run -S transform.param.param2=3
dvc exp run -S transform.param.param2=4

