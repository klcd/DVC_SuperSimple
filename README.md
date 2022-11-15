# Why DVC

# Initializing DVC

# Adding stages

In order to use dvc efficiently we need to create a pipeline.
Therefore we have created scripts that perform minimal task such that our pipeline runs very fast.

Each script corresponds to a stage in the pipeline and in the following we will add these stages together to create our pipeline.

For each stage we need to define

- a name (--name, -n)
- its inputs (--deps, -d)
- its outputs (--outs, -o)
- parameters used (--params, p)

using the ```dvc run``` or ```dvc stage``` command to add it to the ```dvc.yaml``` file. The difference ist that the former directly runs your stage an there directly tests if your script works.

We can now add our first stage.

```
dvc run --name transform \
 --deps data/data.txt \
 --outs data/transformed_data.txt \
 --params transform.param0 \
 --params transform.param1 \
 --params transform.param2 \
 python src/stages/transform.py --config params.yaml
```

the second stage

```
dvc run --name split \
--deps data/transformed_data.txt \
--outs data/test_data.txt \
--outs data/train_data.txt \
--params split.test_fraction \
python src/stages/split.py --config params.yaml
```

and the final stage

```
dvc run --name evaluate \
--deps data/test_data.txt \
--deps data/train_data.txt \
--outs data/result.csv \
--metrics reports/metrics.json \
python src/stages/evaluate.py --config params.yaml

```

The created pipeline can now be visualized with

```dvc dag```

Also we can run our pipeline using

```dvc repro```

if you used the  ```run``` command above nothing should happen because the current status of the pipeline is saved in a file called ```dvc.lock``` that tracks all our inputs, outputs and parameters. Make sure to have a look at it.

To convince yourself that dvc is doing a great job. Go to the data/data.txt file and change an number and run ```dvc repro``` again.


# Experiments and metrics

In the process of experimenting we want to track our metrics. Therefore define what these are and where they are saved. This can happen at the stage definition using the (--metrics, -m) tag. But here we do it direclty in the  ```dvc.yaml``` file.

Therefore we only need to define a metrics section in the
stage where our metrics.json is created.

```
    metrics:
      - reports/metrics.json:
          cache:False
```

As we added the metrics now lets run a couple experiments. Each experiment is tracked by dvc and dvc creates a "vertical" history to the "horizontal" git history.

```
dvc exp run -S transform.param2=2
dvc exp run -S transform.param2=3
dvc exp run -S transform.param2=4
```

we can now check how the metrics changed with ```dvc exp show --only-changed``` and use ```dvc exp apply exp-...``` to apply the changes of a specific experiment to the current workspace or create a git branch using  ```dvc exp branch exp-...```.

If we are happy with the result of the experiment in the workspace we commit it to git. Note that the experiments runned are not lost but remain at the corresponding git commit.

Now after we run a new experiment with ```dvc exp run -S transform.param2=1.75```. We can use ```dvc metrics diff`` to compare the metrics with the last commit.

# Plots

Now we want to add plots to look a experiments and especially to compare them.

To have a quick look we can use ```dvc plots show <path_to_output>``` and point to an output of a stage

Using ```dvc plots modify <path_to_output>``` the output is moved from the outs section into a plots section in the ```dvc.yaml``` that can be further modified.

E.g. we can use
- Different output data
- Specify data to use
- Use different plot templates
- Define our own templates

How to do this can be found [here](https://dvc.org/doc/command-reference/plots)

Now we add plots in the ```dvc.yaml``` file. Therefore we use the evaluate stage where the csv file is generated and move the file from the ```outs``` section into a new section called ```plots``` or we can use the ```dvc plots modify <path_to_file>``` command to indirectly modify the ```dvc.yaml```.

After a dvc repro the plots can be found as an html in      ```dvc_plots``` and be generated using the ```dvc plots show ``` command. Using ```dvc plots diff``` we can compare different revisions (git commits). By default we compare the current workspace state (uncommited changes) to the last commit.

More:
    - [Different examples](https://dvc.org/doc/command-reference/plots/show)
    - [Custom plots with vega templates]


This is the end of the introduction but there is a lot more. For example,

- we can track the training of a model using [DVCLive](https://dvc.org/doc/dvclive)
- use remote storage for our data
- take remote machines to train our model using CML
- there is a [VSCode extension](https://marketplace.visualstudio.com/items?itemName=Iterative.dvc)
- define [data](https://dvc.org/doc/use-cases/data-registry)/[model](https://dvc.org/doc/use-cases/model-registry) registries to collaborate
