import numpy as np
import yaml
import argparse

def split_data(data, test_fraction):

    max_ind = int(np.floor(data.size*test_fraction))
    train_data = data[:max_ind]
    test_data = data[max_ind:]

    return train_data, test_data


def split_data_from_config(config_path):

    #Load config
    with open(config_path, "r") as fid:
        config = yaml.safe_load(fid)

    #Load data from inputs
    data = np.genfromtxt(config['split']['inputs']['raw_data'])

    #Split data
    train_data, test_data = split_data(data,
                                       config['split']['test_fraction'])

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
