import numpy as np
import yaml
import json
import argparse
import pandas as pd


from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from joblib import load


def evaluate_model(model, test_data, train_data):

    metric = {}

    y_pred_test = model.predict(test_data[:,0].reshape(-1,1))
    metric['mae_test'] = mean_absolute_error(y_pred= y_pred_test, y_true=test_data[:,1])
    metric['mape_test'] = mean_absolute_percentage_error(y_pred=y_pred_test, y_true=test_data[:,1])

    y_pred_train = model.predict(train_data[:,0].reshape(-1,1))
    metric['mae_train'] = mean_absolute_error(y_pred=y_pred_train, y_true=train_data[:,1])
    metric['mape_train'] = mean_absolute_percentage_error(y_pred=y_pred_train,y_true=train_data[:,1])

    return metric, y_pred_test, y_pred_train


def evaluate_model_from_config(config_path):

    #Load config
    with open(config_path, "r") as fid:
        config = yaml.safe_load(fid)

    #Load data from inputs
    test_data = np.genfromtxt(config['evaluate']['inputs']['test_data'])
    train_data = np.genfromtxt(config['evaluate']['inputs']['train_data'])

    model = load(config['evaluate']['inputs']['model'])

    #Evaluate and save to outputs
    metric, y_pred_test, y_pred_train = evaluate_model(model, test_data, train_data)
    metrics_json = json.dumps(metric)

    with open(config['evaluate']['outputs']['metric'], 'w') as fid:
        fid.write(metrics_json)

    df = pd.DataFrame(np.concatenate([np.concatenate([test_data, train_data], axis=0),
                                      np.concatenate([y_pred_test, y_pred_train], axis=0),
                                      np.concatenate([np.zeros(y_pred_test.size), np.ones(y_pred_train.size)], axis=0).reshape(-1,1)
                                      ],
                                    axis=1)
                    )
    df.columns = ['x', 'y', 'y_pred', 'train']
    df.to_csv(config['evaluate']['outputs']['result'], index=False)


if __name__ == "__main__":
    print("Started evaluate stage")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', dest='config_path', required=True)
    args = arg_parser.parse_args()

    evaluate_model_from_config(args.config_path)

    print("Finished evaluate stage")
