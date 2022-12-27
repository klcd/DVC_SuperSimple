import numpy as np
import yaml
from sklearn.linear_model import Ridge
import argparse
from joblib import dump


def setup_train_model(alpha, data_train, **kwargs):

    model = Ridge(alpha=alpha, fit_intercept=True)
    model.fit(data_train[:, 0].reshape(-1, 1), data_train[:, 1].reshape(-1, 1))

    return model


def setup_train_model_from_config(config):

    #2. Load data dependencies
    data = np.genfromtxt(config.train.inputs.train_data)

    #3. Setup & Train Model
    model = setup_train_model(config.train.param.alpha, data)

    #4. Save model
    dump(model, config.train.outputs.model)

if __name__ == "__main__":
    print("Started train stage")

    from helpers.load_config import default_config_parser, load_config_from_command_line
    args = default_config_parser()
    config = load_config_from_command_line(args.config_path)
    setup_train_model_from_config(config)

    print("Finished train stage")
