import numpy as np
import yaml
from sklearn.linear_model import Ridge
import argparse
from joblib import dump


def setup_train_model(alpha, data_train, **kwargs):

    model = Ridge(alpha=alpha, fit_intercept=True)
    model.fit(data_train[:, 0].reshape(-1, 1), data_train[:, 1].reshape(-1, 1))

    return model


def setup_train_model_from_config(config_path):

    #1. Load config
    with open(config_path, "r") as fid:
        config = yaml.safe_load(fid)

    #2. Load data dependencies
    data = np.genfromtxt(config['train']['inputs']['train_data'])

    #3. Setup & Train Model
    model = setup_train_model(config['train']['param']['alpha'], data)

    #4. Save model
    dump(model, config['train']['outputs']['model'])

if __name__ == "__main__":
    print("Started train stage")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', dest='config_path', required=True)
    args = arg_parser.parse_args()
    setup_train_model_from_config(args.config_path)

    print("Finished train stage")
