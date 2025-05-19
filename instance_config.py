import os
import json

def load_instance_config(filename="instance_config.json"):
    path = os.path.join(os.path.dirname(__file__), 'config', filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
