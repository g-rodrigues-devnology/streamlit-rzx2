import json
import os

assets_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')

def get_asset_path(name: str)-> str:
    return os.path.join(assets_path, name)

names_map = {}

with open(get_asset_path('countries-pt.json')) as f:
    data = json.load(f)

    for item in data:
        names_map[item['alpha2'].lower()] = item['name']

def get_country_name(code: str) -> str:
    code = code.lower()

    if code in names_map:
        return names_map[code]
    
    return code