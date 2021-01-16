import yaml
from schema import Schema, Optional, And, Use

Device = {'id': str, 
          Optional('name'): str, 
          'type': str, 
          'address': str,
          object: object}  # allow extra keys

def validate_config(config_string):
  config_schema = Schema(And(Use(yaml.safe_load),  # first convert from YAML
                         [Device]))
  return config_schema.validate(config_string)
  
def load_config(config_path='config.yml'):
  with open(config_path, 'r') as config_file:
    return validate_config(config_file)
    
if __name__ == '__main__':
  print(load_config())
  