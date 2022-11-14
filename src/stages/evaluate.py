import numpy as np
import yaml
import json
import argparse
import pandas as pd

def evaluate_model(train_data, test_data):
    return np.mean(train_data), np.mean(test_data)

def evaluate_model_from_config(config_path):

    #Load config
    with open(config_path, "r") as fid:
        config = yaml.safe_load(fid)

    #Load data from inputs
    test_data = np.genfromtxt(config['evaluate']['inputs']['test_data'])
    train_data = np.genfromtxt(config['evaluate']['inputs']['train_data'])

    #Evaluate
    train_res, test_res = evaluate_model(test_data, train_data)


    #Save the data to outputs

    metric = {}
    metric['test'] = test_res
    metric['train'] = train_res
    metrics_json = json.dumps(metric)

    with open(config['evaluate']['outputs']['metric'], 'w') as fid:
        fid.write(metrics_json)


    df = pd.DataFrame()
    df['x'] = np.arange(0,100)
    df['y_train'] = np.sin(train_res*df['x'])
    df['y_test']  = np.sin(test_res*df['x'])
    df.to_csv(config['evaluate']['outputs']['result'], index=False)


if __name__ == "__main__":
    print("Started evaluate stage")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', dest='config_path', required=True)
    args = arg_parser.parse_args()

    evaluate_model_from_config(args.config_path)

    print("Finished evaluate stage")
