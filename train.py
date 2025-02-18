from model.initialization import initialization
from config import conf
import argparse
import torch

def boolean_string(s):
    if s.upper() not in {'FALSE', 'TRUE'}:
        raise ValueError('Not a valid boolean string')
    return s.upper() == 'TRUE'


# add test``k
parser = argparse.ArgumentParser(description='Train')
parser.add_argument('--cache', default=True, type=boolean_string,
                    help='cache: if set as TRUE all the training data will be loaded at once'
                         ' before the training start. Default: TRUE')
opt = parser.parse_args()

m = initialization(conf, train=opt.cache)[0]
print(conf)
#move to cuda
print("cuda is available:",torch.cuda.is_available())
m.fit()
