import os, json, logging, threading
import pandas as pd

###############################################################################
# Constants
###############################################################################
_here = os.path.dirname(os.path.abspath(__file__))
_cwd = os.path.dirname(_here)
_const = os.path.join(_cwd, 'user', 'constant.json')
_flog = os.path.join(_cwd, 'user', 'file.log')

###############################################################################
# Logging
###############################################################################
LOG_FORMAT = '%(asctime)s - %(levelname)-8s - %(message)s'
LOG_FORMAT = logging.Formatter(LOG_FORMAT)

log = logging.getLogger('term')
log.setLevel(logging.INFO)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(LOG_FORMAT)
log.addHandler(c_handler)

flog = logging.getLogger('to_file')
flog.setLevel(logging.INFO)
f_handler = logging.FileHandler(_flog)
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(LOG_FORMAT)
flog.addHandler(f_handler)

###############################################################################
# Basic functions
###############################################################################
def get_const(item:str=''):
    if not os.path.isfile(_const): return None
    with open(_const) as f: const = json.load(f)
    for i in item.split('.'):
        if not i: break
        const = const.get(i, {})
    return const

def up_const(const:dict):
    with open(_const, 'w') as f: json.dump(const, f, indent=2)

def set_const(mapping:dict):
    const = get_const()
    for k, v in mapping.items():
        keys = k.split('.')
        tmp = const
        for k in keys[:-1]:
            tmp = tmp.setdefault(k, {})
        tmp[keys[-1]] = v
    up_const(const)

def pretty_df(df:pd.DataFrame):
    res = []
    for l in df.to_dict('records'):
        txt = f'{df.columns[0]} : {l[df.columns[0]]}'
        for c in df.columns[1:]:
            if l[c] > 0:
                txt += f'\n{c} : {l[c]:.2f}'
        res.append(txt)
    return res
