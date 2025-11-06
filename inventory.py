import yaml
import argparse
import logging
import json
import csv
from pathlib import Path
from logging.handlers import RotatingFileHandler


parser = argparse.ArgumentParser(prog='ansible-inventory-file',  description="Generate a dynamic Ansible inventory file.")
parser.add_argument(
        "--output",
        type=str,
        default="inventory.yaml",
        help="Output filename for the generated inventory file."
    )
parser.add_argument("--no-playbook", action="store_true", help="Skip creating the playbook file.")
parser.add_argument(
    "--input",
    type=str,
    help="Optional path to a JSON or CSV file containing server information."
)


# Logging Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler

# keeps log files from being overloaded
file_handler = RotatingFileHandler(
   'inventory.log',
   maxBytes=10000000,
   backupCount=50
)

file_formatter = logging.Formatter(
  '%(asctime)s - %(levelname)s - %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S'  
)

file_handler.setFormatter(file_formatter)

# Console handler – clean and readable output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(console_formatter)


# Add both handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# takes server input
def load_server_data(input_file):
   # Load default server data when no  JSON or CSV file is found.
   if not input_file:
      logger.warning("No input file provided. Using default static server")
      return [ {"ip": "10.0.1.5", "hostname": "serverA.example.com", "group": "web_servers"},
        {"ip": "10.0.1.6", "hostname": "serverC.example.com", "group": "web_servers"},
        {"ip": "10.0.1.20", "hostname": "serverB.example.com", "group": "db_servers"},
        {"ip": "10.0.1.30", "hostname": "serverD.example.com", "group": "monitoring_servers"}]
   
   input_path = Path(input_file)
   if not input_path.exists():
      logger.error(f"Input file '{input_file}' not found.")
      raise FileNotFoundError(f"File '{input_file}' not found.")
   
   # Loads server data from a JSON or CSV file.
   try:
      if input_file.endswith(".json"):
         with open(input_file, 'r') as f:
            data = json.load(f)
      elif input_file.endswith(".csv"):
         with open(input_file, newline='') as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
      else:
         raise ValueError("Unsupported file format. Use .json or .csv")
      
      logger.info(f"Loaded {len(data)} server entries from {input_file}")
      return data
   except Exception:
      logger.exception("Failed to load input data.")
      raise


# Inventory Creation
def create_inventory(output_file, raw_server_data):
    # gets group from server data file.
    unique_groups = {server['group'] for server in raw_server_data}

    children_structure = {}
    for group_name in unique_groups:
        children_structure[group_name] = {'hosts': {}}

    # ansible yaml format
    inventory = {
      'all': {
        'children': children_structure
      }
    }


    for server in raw_server_data:
      group_name = server['group']
      host_name = server['hostname']
      ip = server['ip']

      inventory['all']['children'][group_name]['hosts'][host_name] = {
         'ansible_host': ip
      }

    try:
      with open(output_file, 'w') as f:
        yaml.dump(inventory, f, sort_keys=False, default_flow_style=False)
        logger.info(f"Inventory file '{output_file}' created successfully!")
    except Exception:
      logger.exception("Failed to create inventory file")



def create_playbook():
    playbook_content = """
- name: Install and start NGINX
  hosts: web_servers
  become: yes
  tasks:
    - name: Install NGINX
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start NGINX service
      service:
        name: nginx
        state: started
        enabled: yes

"""
    try:
      with open('install_nginx.yml', 'w') as f:
        f.write(playbook_content)
        logger.info("Playbook 'install_nginx.yml' created successfully.")
    except Exception:
        logger.exception("Failed to create playbook file.")

# Main execution
if __name__ == '__main__':
  args = parser.parse_args()
  try:
    server_data = load_server_data(args.input)
    create_inventory(args.output, server_data)

    if not args.no_playbook:
      create_playbook()
    else:
      logger.info("Playbook creation skipped as requested.")
    
    logger.info("All operations completed successfully.")
  except Exception:
     logger.error("Process terminated due to errors.")
  