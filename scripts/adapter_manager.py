#!/usr/bin/env python3
"""
Adapter management script for hot-swapping LoRA adapters
"""

import json
import argparse
import requests
from pathlib import Path
from datetime import datetime

# Configuration
CONFIG_PATH = Path("config/adapters.json")
API_BASE_URL = "http://localhost:8000/api/v1"

def load_adapters_config():
    """Load adapters configuration"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {"adapters": {}, "active_adapters": {}}

def save_adapters_config(config):
    """Save adapters configuration"""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def list_adapters():
    """List all available adapters"""
    config = load_adapters_config()
    print("Available adapters:")
    for name, details in config["adapters"].items():
        status = "✓" if name in config["active_adapters"] else " "
        print(f"  [{status}] {name}: {details['description']}")

def add_adapter(name, path, description=""):
    """Add a new adapter to the configuration"""
    config = load_adapters_config()
    
    if name in config["adapters"]:
        print(f"Adapter '{name}' already exists. Use update to modify it.")
        return False
    
    config["adapters"][name] = {
        "path": path,
        "description": description,
        "added_at": datetime.now().isoformat()
    }
    
    save_adapters_config(config)
    print(f"Adapter '{name}' added successfully.")
    return True

def remove_adapter(name):
    """Remove an adapter from the configuration"""
    config = load_adapters_config()
    
    if name not in config["adapters"]:
        print(f"Adapter '{name}' does not exist.")
        return False
    
    # Deactivate if active
    if name in config["active_adapters"]:
        deactivate_adapter(name)
    
    del config["adapters"][name]
    save_adapters_config(config)
    print(f"Adapter '{name}' removed successfully.")
    return True

def activate_adapter(name, model_type=None):
    """Activate an adapter for use"""
    config = load_adapters_config()
    
    if name not in config["adapters"]:
        print(f"Adapter '{name}' does not exist.")
        return False
    
    # Make API call to activate the adapter
    try:
        response = requests.post(
            f"{API_BASE_URL}/admin/adapters/activate",
            json={"adapter_name": name, "model_type": model_type},
            timeout=10
        )
        
        if response.status_code == 200:
            config["active_adapters"][name] = {
                "activated_at": datetime.now().isoformat(),
                "model_type": model_type
            }
            save_adapters_config(config)
            print(f"Adapter '{name}' activated successfully.")
            return True
        else:
            print(f"Failed to activate adapter: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error activating adapter: {e}")
        return False

def deactivate_adapter(name):
    """Deactivate an adapter"""
    config = load_adapters_config()
    
    if name not in config["active_adapters"]:
        print(f"Adapter '{name}' is not active.")
        return False
    
    # Make API call to deactivate the adapter
    try:
        response = requests.post(
            f"{API_BASE_URL}/admin/adapters/deactivate",
            json={"adapter_name": name},
            timeout=10
        )
        
        if response.status_code == 200:
            del config["active_adapters"][name]
            save_adapters_config(config)
            print(f"Adapter '{name}' deactivated successfully.")
            return True
        else:
            print(f"Failed to deactivate adapter: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error deactivating adapter: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Manage LoRA adapters for Quantum AI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    subparsers.add_parser("list", help="List all adapters")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new adapter")
    add_parser.add_argument("name", help="Name of the adapter")
    add_parser.add_argument("path", help="Path to the adapter files")
    add_parser.add_argument("--description", help="Description of the adapter", default="")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove an adapter")
    remove_parser.add_argument("name", help="Name of the adapter to remove")
    
    # Activate command
    activate_parser = subparsers.add_parser("activate", help="Activate an adapter")
    activate_parser.add_argument("name", help="Name of the adapter to activate")
    activate_parser.add_argument("--model-type", help="Type of model to use with this adapter")
    
    # Deactivate command
    deactivate_parser = subparsers.add_parser("deactivate", help="Deactivate an adapter")
    deactivate_parser.add_argument("name", help="Name of the adapter to deactivate")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_adapters()
    elif args.command == "add":
        add_adapter(args.name, args.path, args.description)
    elif args.command == "remove":
        remove_adapter(args.name)
    elif args.command == "activate":
        activate_adapter(args.name, args.model_type)
    elif args.command == "deactivate":
        deactivate_adapter(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
