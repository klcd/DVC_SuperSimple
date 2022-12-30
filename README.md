# Why DVC

In MlOps it becomes important that we do not only have a good control on

- Code
- Environment/Infrastructure
- Configuration

but we also need to keep track on

- Data
- Experiments
- Parameters

DVC is an open-source tool that allows to do just that. In my opinion its main advantages are

- Code agnostic
- Cloud independent
- Open source
- Well documented

It very much helps you to separate your experiment parameters from your code, which allows you to see your changes quickly. This together with the its data tracking capabilities allows you to experiment efficiently and create reproducible work.

# Introduction

In this tutorial we are going to create a dvc pipeline that can be fully controlled from the command line.

## Environment
In the folder ```environment``` you can find a conda/pip environment that includes all the necessary packages.

## Data

In the folder ```data``` we have a file called ```data.csv``` it that contains the x and y coordinates generated
with the script ```create_data.py``` in the utilities folder.

## Stages and Parameters
In the folder ```stages``` you can find multiple python files.

- split.py: In this script we load the data and split it into test and train data
- train.py: Now we setup a Ridge model and train it with the train data.
- evaluate.py: Here we use the trained model for predictions.

All the stages scripts contain three parts

- A function ```<name>``` that does the actual task
- A function ```<name>_from_config``` that loads the necesary inputs
- A Main section where command line arguments are parsed

This ensures that the first function can be reused in another context. In larger projects
it might even be externalized.

All parameters to run the stages are found in the ```params.yaml```. With this it is
ensured that the code and the configuration is separated and you can easily modify
parameters without accidentially changing the code.

The stages can be called from the command line as follows

```
python <path to script> --config <path to params.yaml>
```

but now we will let ```dvc``` handle this for us and build a pipeline.


# DVC Pipeline Tutorial


## 1. Initializing DVC

In your project directory, lets start a new branch

```
git checkout -b <my_branch>
```
and run

```dvc init```

to initialise dvc. Then create a init commit

```
git commit -m "dvc init"
```

## 2. Adding stages

In order to use dvc efficiently we need to create a pipeline.
Therefore we have created scripts that perform minimal task such that our pipeline runs very fast.

Each script corresponds to a stage in the pipeline and in the following we will add these stages together to create our pipeline.

For each stage we need to define

- a name (--name, -n)
- its inputs (--deps, -d)
- its outputs (--outs, -o)
- parameters used (--params, p)

using the ```dvc run``` or ```dvc stage``` command to add it to the ```dvc.yaml``` file. The difference ist that the former directly runs your stage an there directly tests if your script works.

We can now add our split stage.

```
dvc run --name split \
 --deps stages/split.py \
 --deps initial_data/data.csv \
 --outs data/test_data.csv \
 --outs data/train_data.csv \
 --params split.param \
 python stages/split.py --config params.yaml
```

the train stage

```
dvc run --name train \
 --deps stages/train.py \
--deps data/train_data.csv \
--outs models/model.joblib \
--params train.param \
python stages/train.py --config params.yaml
```

and the final evaluation stage

```
dvc run --name evaluate \
--deps stages/evaluate.py \
--deps data/test_data.csv \
--deps data/train_data.csv \
--deps models/model.joblib \
--outs reports/result.csv \
--metrics reports/metrics.json \
python stages/evaluate.py --config params.yaml

```

The created pipeline can now be visualized with

```dvc dag```

Lets have a look at the files that were created when me build the pipeline

- dvc.yaml: Contains all inputs, outputs, parameters etc
- dvc.lock: Similar information but also md5 hashes. So it save the current status of the pipeline.

Lets add this two files to git

```
git add dvc.lock dvc.yaml
git commit -m "First pipeline run"
```


From now on we can run our pipeline using

```dvc repro```

Nothing should happen. To convince yourself that dvc is doing a great job. Go to the data/data.csv file and change an number and run ```dvc repro``` again and commit the ```dvc.lock``` again

```
git commit -a -m "I changed a numer"
```

If you want you can apply a simple change to the scripts as well and rerun the pipeline.

## 3. Experiments and metrics

In the process of experimenting we want to track our metrics. Therefore define what these are and where they are saved. This happened at the stage definition using the (--metrics, -m) tag. But here we could do it also direclty in the  ```dvc.yaml``` file.


So lets to some experiments. Each experiment is tracked by dvc and dvc creates a "vertical" history to the "horizontal" git history.

```
dvc exp run -S train.param.alpha=0.2
dvc exp run -S train.param.alpha=0.3
dvc exp run -S train.param.alpha=0.4
```

we can now check how the metrics changed with ```dvc exp show --only-changed``` and use ```dvc exp apply exp-...``` to apply the changes of a specific experiment to the current workspace (or create a git branch using  ```dvc exp branch exp-...```).

If we are happy with the result of the experiment in the workspace we commit it to git. Note that the experiments runned are not lost but remain at the corresponding git commit.

Note for pipelines that are running longer. There is also a possibility to create a queue of experiment and run them in one go.

Now after we run a new experiment with ```dvc exp run -S train.param.alpha=1.0```. We can use ```dvc metrics diff`` to compare the metrics with the last commit. If the experiment yields better results we can commit it again.

## 4. Plots

Now we want to add plots to look a experiments and especially to compare them.

To have a quick look we can use ```dvc plots show <path_to_output>``` and point to an output of a stage

We can use the following command to create a plot
```
dvc plots modify -x x -y y --title "Example" reports/result.csv
```

In the ```dvc.yaml``` the output is moved from the outs section into a plots section that can be further modified.

E.g. we can use
- Different output data
- Specify data to use
- Use different plot templates
- Define our own templates

How to do this can be found [here](https://dvc.org/doc/command-reference/plots)

After a dvc repro the plots can be generated using the ```dvc plots show ``` command and are stored in a folder with the name ```dvc_plots``` as html . Using ```dvc plots diff``` we can compare different revisions (git commits). By default we compare the current workspace state (uncommited changes) to the last commit.

More:
    - [Different examples](https://dvc.org/doc/command-reference/plots/show)
    - [Custom plots with vega templates]



Finally, to restart the tutorial from the beginning we can use

```
dvc destroy
```

to remove everything related to dvc

This is the end of the introduction but there is a lot more. For example,

- we can track the training of a model using [DVCLive](https://dvc.org/doc/dvclive)
- use remote storage for our data
- take remote machines to train our model using CML
- there is a [VSCode extension](https://marketplace.visualstudio.com/items?itemName=Iterative.dvc)
- define [data](https://dvc.org/doc/use-cases/data-registry)/[model](https://dvc.org/doc/use-cases/model-registry) registries to collaborate

