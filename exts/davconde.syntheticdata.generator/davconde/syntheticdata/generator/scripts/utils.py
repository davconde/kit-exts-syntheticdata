import os
import json
from pathlib import Path
import omni.ui as ui
import carb


def dict_primitives_to_models(d):
    for key, value in d.items():
        if isinstance(value, float):
            d[key] = ui.SimpleFloatModel(value)
        elif isinstance(value, int):
            d[key] = ui.SimpleIntModel(value)
        elif isinstance(value, str):
            d[key] = ui.SimpleStringModel(value)
        elif isinstance(value, bool):
            d[key] = ui.SimpleBoolModel(value)
        elif isinstance(value, dict):
            dict_primitives_to_models(value)


def dict_models_to_primitives(d):
    for key, value in d.items():
        if isinstance(value, ui.SimpleFloatModel):
            d[key] = value.get_value_as_float()
        elif isinstance(value, ui.SimpleIntModel):
            d[key] = value.get_value_as_int()
        elif isinstance(value, ui.SimpleStringModel):
            d[key] = value.get_value_as_string()
        elif isinstance(value, ui.SimpleBoolModel):
            d[key] = value.get_value_as_bool()
        elif isinstance(value, dict):
            dict_models_to_primitives(value)


def load_models_dict(model='default'):
    d_s = os.path.sep
    model_file = f'{os.path.dirname(os.path.abspath(__file__))}{d_s}..{d_s}settings{d_s}{model}.json'
    models = json.load(open(model_file))
    return models


def save_models_dict(d, model='default'):
    if model == 'default':
        return
    d_s = os.path.sep
    model_file = f'{os.path.dirname(os.path.abspath(__file__))}{d_s}..{d_s}settings{d_s}{model}.json'
    d_c = d.copy()
    d_c.pop('config_file', None)
    dict_models_to_primitives(d_c)
    json.dump(d_c, open(model_file, 'w+'), indent=4)
