import numpy as np
import yaml
import argparse

def transform_data(data, transform_function=lambda x : x**2):
    return transform_function(data)


def transform_data_from_config(config_path):

    #Load config
    with open(config_path, "r") as fid:
        config = yaml.safe_load(fid)

    #Load data from inputs
    data = np.genfromtxt(config['transform']['inputs']['raw_data'])

    #Split data

    func = lambda x: config['transform']['param2']*x**2 +config['transform']['param1']*x + config['transform']['param0']

    trans_data = transform_data(data, func)

    #Save the data to outputs
    np.savetxt(config['transform']['outputs']['trans_data'], trans_data)


if __name__ == "__main__":
    print("Started transform stage")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', dest='config_path', required=True)
    args = arg_parser.parse_args()

    transform_data_from_config(args.config_path)

    print("Finished transform stage")
