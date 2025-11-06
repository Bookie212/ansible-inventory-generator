# 🧩 Ansible Inventory File Generator

A Python-based utility that dynamically generates **Ansible inventory files** in YAML format and optionally creates a **playbook** for automated NGINX installation.  
It supports both **default static data** and **user-provided server lists** in JSON or CSV format.

---

## 🚀 Features

✅ Generate an `inventory.yaml` file automatically  
✅ Accept server input from **JSON** or **CSV** files  
✅ Create a ready-to-use **Ansible playbook** (`install_nginx.yml`)  
✅ Built-in **logging system** (console + rotating log file)  
✅ Fully configurable through **command-line arguments**  
✅ Graceful error handling with helpful log messages  

---

## 📦 Requirements

- Python 3.7 or later  
- [PyYAML](https://pyyaml.org/)
  
Install dependencies:

pip install pyyaml

## 🧰 Usage
### 🏗️ 1. Run with default static data

If you don’t provide an input file, the script will generate a default inventory using built-in server details.

python ansible_inventory.py


This will create:

inventory.yaml

install_nginx.yml

inventory.log

### 📂 2. Run with a JSON input file

Example JSON (servers.json):

[
  {"ip": "10.0.1.5", "hostname": "web1.example.com", "group": "web_servers"},
  {"ip": "10.0.1.20", "hostname": "db1.example.com", "group": "db_servers"}
]


Run:

python ansible_inventory.py --input servers.json

### 🧾 3. Run with a CSV input file

Example CSV (servers.csv):

ip,hostname,group
10.0.1.5,web1.example.com,web_servers
10.0.1.20,db1.example.com,db_servers


Run:

python ansible_inventory.py --input servers.csv

### ⚙️ 4. Skip Playbook Creation

If you only want the inventory file:

python ansible_inventory.py --no-playbook

### 🪵 5. Logging

All events are logged to inventory.log and displayed in the console.

Example log snippet:

2025-10-30 11:30:02 - INFO - Loaded 4 server entries from servers.csv
2025-10-30 11:30:02 - INFO - Inventory file 'inventory.yaml' created successfully!
2025-10-30 11:30:02 - INFO - Playbook 'install_nginx.yml' created successfully.


The log file rotates automatically when it grows too large (maxBytes=10MB, backupCount=50).


## ⚡ Example Output (inventory.yaml)
all:
  children:
    db_servers:
      hosts:
        serverB.example.com:
          ansible_host: 10.0.1.20
    web_servers:
      hosts:
        serverA.example.com:
          ansible_host: 10.0.1.5

## 🧠 How It Works

Loads server data (from file or static defaults)

Builds the correct YAML structure for Ansible

Writes the inventory to file

Creates a playbook (unless --no-playbook is used)

Logs every step for visibility and debugging

## 🛡️ Error Handling

Missing input file → logs an error and stops

Unsupported file type → raises a ValueError

Write permissions or invalid data → logged with full stack trace


## 📜 License

This project is open-source under the MIT License.

## 🏁 Example Command Summary
Command	Description
python ansible_inventory.py	Run with default servers
python ansible_inventory.py --input servers.json	Use JSON input
python ansible_inventory.py --input servers.csv	Use CSV input
python ansible_inventory.py --no-playbook	Skip playbook creation
python ansible_inventory.py --output custom_inventory.yml	Custom output file name