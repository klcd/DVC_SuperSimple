import numpy as np
import yaml
import argparse

from sklearn.model_selection import train_test_split

def split_data(data, test_fraction, **kwargs):

    train_data, test_data = train_test_split(data, test_size=test_fraction, shuffle=True)

    return train_data, test_data


def split_data_from_config(config_path):

    #Load config
    with open(config_path, "r") as fid:
        config = yaml.safe_load(fid)

    #Load data from inputs
    data = np.genfromtxt(config['split']['inputs']['trans_data'])

    #Split data
    train_data, test_data = split_data(data,
                                       **config['split']['param'])

    #Save the data to outputs
    np.savetxt(config['split']['outputs']['test_data'], test_data)
    np.savetxt(config['split']['outputs']['train_data'], train_data)


if __name__ == "__main__":
    print("Started split stage")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', dest='config_path', required=True)
    args = arg_parser.parse_args()

    split_data_from_config(args.config_path)

    print("Finished split stage")
