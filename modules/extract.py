import numpy as np
import pandas as pd
from modules.instant import CanHo

def standardize(ch: CanHo):
    if ch.real_estate_type:
        ch.real_estate_type = ch.real_estate_type.lower()
    if ch.project_name:
        ch.project_name = ch.project_name.lower()
    if ch.street:
        ch.street = ch.street.lower()
    if ch.ward:
        ch.ward = ch.ward.lower()
    if ch.district:
        ch.district = ch.district.lower()
    if ch.city:
        ch.city = ch.city.lower()
    if ch.direction:
        ch.direction = ch.direction.lower()
    if ch.corner:
        ch.corner = ch.corner.lower()

    if ch.area:
        ch.area = float(ch.area)
    if ch.n_bedroom:
        ch.n_bedroom = int(ch.n_bedroom)
    if ch.floor:
        ch.floor = int(ch.floor)
    if ch.rate_direction:
        ch.rate_direction = float(ch.rate_direction)
    if ch.rate_corner:
        ch.rate_corner = float(ch.rate_corner)

    ch.street = None
    ch.ward = None
    return ch

def json_to_input(json: CanHo):
    json = standardize(json)
    json = json.dict()
    # list_features = ['real_estate_type', 'project_name', 'street', 'ward', 'district',
    #                 'city', 'n_bedroom', 'area']
    list_features = ['real_estate_type', 'project_name', 'district',
                    'city', 'n_bedroom', 'area']
    input = dict.fromkeys(list_features)
    for ft in list_features:
        if ft in json.keys():
            input[ft] = json[ft]
        else:
            input[ft] = np.nan
    input = pd.Series(input).values
    res = pd.DataFrame(input.reshape(1,-1), columns=list_features).fillna(value=np.nan)
    res[list_features[:-2]] = res[list_features[:-2]].astype(object)
    return res


def consider_floor(ch: CanHo):

    if not ch.floor:
        return 0
    else:
        floor = np.concatenate([np.linspace(start=0, stop=0.1, num=20), np.linspace(start=0.1, stop=0, num=10)])
        return floor[ch.floor - 2]


def consider_direction(ch: CanHo):

    if not ch.direction:
        return 0
    else:
        if not ch.rate_direction:
            return 0.04 if ('đông' in ch.direction) else 0.02
        else:
            return ch.rate_direction if ('đông' in ch.direction) else ch.rate_direction


def consider_corner(ch: CanHo):

    if not ch.corner:
        return 0
    else:
        if not ch.rate_corner:
            return 0.06 if ('góc' in ch.corner) else 0
        else:
            return ch.rate_corner if ('góc' in ch.corner) else 0

