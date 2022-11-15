import numpy as np
import yaml
import argparse

def transform_data(data, transform_function=lambda x : x**2):
    return transform_function(data)

def create_func(param0, param1, param2, **kwargs):
    return lambda x: param0+param1*x+param2*x**2

def transform_data_from_config(config_path):

    #1. Load config
    with open(config_path, "r") as fid:
        config = yaml.safe_load(fid)

    #2. Load data dependencies
    data = np.genfromtxt(config['transform']['inputs']['raw_data'])

    #3. Split data
    func = create_func(**config['transform']['param'])
    trans_data = transform_data(data, func)

    #4. Save the data to outputs
    np.savetxt(config['transform']['outputs']['trans_data'], trans_data)


if __name__ == "__main__":
    print("Started transform stage")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', dest='config_path', required=True)
    args = arg_parser.parse_args()

    transform_data_from_config(args.config_path)

    print("Finished transform stage")
