import os
import json
import yaml
from typing import Dict, Any
from cryptography.fernet import Fernet

class ConfigManager:
    """
    Comprehensive configuration management with encryption and multiple format support
    """
    def __init__(self, config_dir=None):
        """
        Initialize ConfigManager
        
        Args:
            config_dir (str, optional): Directory to store configurations
        """
        self.config_dir = config_dir or os.path.join(os.path.expanduser("~"), ".ai_config")
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Encryption key management
        self.key_file = os.path.join(self.config_dir, "encryption.key")
        self._load_or_generate_key()

    def _load_or_generate_key(self):
        """
        Load existing encryption key or generate a new one
        """
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
                with open(self.key_file, 'rb') as f:
                    self.encryption_key = f.read()
        
        self.cipher_suite = Fernet(self.encryption_key)

    def save_config(self, config_name: str, config_data: Dict[str, Any], format: str = 'json', encrypt: bool = True):
        """
        Save configuration with optional encryption and format support
        
        Args:
            config_name (str): Name of the configuration
            config_data (Dict): Configuration data
            format (str): File format (json, yaml)
            encrypt (bool): Whether to encrypt the configuration
        """
        config_path = os.path.join(self.config_dir, f"{config_name}.{format}")
        
        if encrypt:
            # Convert config to JSON string and encrypt
            json_data = json.dumps(config_data)
            encrypted_data = self.cipher_suite.encrypt(json_data.encode())
            
            with open(config_path, 'wb') as f:
                f.write(encrypted_data)
        else:
            # Save in specified format without encryption
            with open(config_path, 'w') as f:
                if format == 'json':
                    json.dump(config_data, f, indent=2)
                elif format == 'yaml':
                    yaml.safe_dump(config_data, f, default_flow_style=False)

    def load_config(self, config_name: str, format: str = 'json', decrypt: bool = True):
        """
        Load configuration with optional decryption and format support
        
        Args:
            config_name (str): Name of the configuration
            format (str): File format (json, yaml)
            decrypt (bool): Whether to decrypt the configuration
        
        Returns:
            Dict: Loaded configuration
        """
        config_path = os.path.join(self.config_dir, f"{config_name}.{format}")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration {config_name} not found")
        
        with open(config_path, 'rb' if decrypt else 'r') as f:
            if decrypt:
                # Decrypt and parse JSON
                encrypted_data = f.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                return json.loads(decrypted_data)
            else:
                # Load based on format
                if format == 'json':
                    return json.load(f)
                elif format == 'yaml':
                    return yaml.safe_load(f)

    def list_configs(self):
        """
        List all available configurations
        
        Returns:
            List[str]: Configuration names
        """
        configs = []
        for filename in os.listdir(self.config_dir):
            if filename != "encryption.key":
                configs.append(os.path.splitext(filename))
        return configs

    def delete_config(self, config_name: str):
        """
        Delete a specific configuration
        
        Args:
            config_name (str): Name of the configuration to delete
        """
        config_path = os.path.join(self.config_dir, f"{config_name}.*")
        import glob
        
        for file in glob.glob(config_path):
            os.remove(file)

    def merge_configs(self, base_config: str, overlay_config: str):
        """
        Merge two configurations, with overlay taking precedence
        
        Args:
            base_config (str): Base configuration name
            overlay_config (str): Configuration to overlay on base
        
        Returns:
            Dict: Merged configuration
        """
        base = self.load_config(base_config)
        overlay = self.load_config(overlay_config)
        
        def deep_merge(dict1, dict2):
            """Recursively merge two dictionaries"""
            for key, value in dict2.items():
                if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                                        deep_merge(dict1[key], value)
                else:
                    dict1[key] = value
            return dict1

        merged_config = deep_merge(base.copy(), overlay)
        return merged_config

def interactive_config_manager():
    """
    Interactive CLI for configuration management
    """
    config_manager = ConfigManager()

    while True:
        print("\n--- Configuration Manager ---")
        print("1. Create New Configuration")
        print("2. Load Configuration")
        print("3. List Configurations")
        print("4. Delete Configuration")
        print("5. Merge Configurations")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            config_name = input("Enter configuration name: ")
            format_choices = ['json', 'yaml']
            print("Formats:")
            for i, fmt in enumerate(format_choices, 1):
                print(f"{i}. {fmt}")
            
            format_choice = input("Select format (default: json): ") or '1'
            format_name = format_choices[int(format_choice) - 1]

            encrypt = input("Encrypt configuration? (y/N): ").lower() == 'y'

            # Interactive config creation
            config_data = {}
            while True:
                key = input("Enter key (or press Enter to finish): ")
                if not key:
                    break
                value = input(f"Enter value for {key}: ")
                config_data[key] = value

            config_manager.save_config(
                config_name, 
                config_data, 
                format=format_name, 
                encrypt=encrypt
            )
            print(f"Configuration {config_name} saved successfully.")

        elif choice == '2':
            configs = config_manager.list_configs()
            print("\nAvailable Configurations:")
            for i, config in enumerate(configs, 1):
                print(f"{i}. {config}")

            config_choice = input("Select configuration to load: ")
            try:
                selected_config = configs[int(config_choice) - 1]
                decrypt = input("Decrypt configuration? (y/N): ").lower() == 'y'
                
                config = config_manager.load_config(
                    selected_config, 
                    decrypt=decrypt
                )
                print("\nLoaded Configuration:")
                print(json.dumps(config, indent=2))
            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == '3':
            configs = config_manager.list_configs()
            print("\nAvailable Configurations:")
            for config in configs:
                print(config)

        elif choice == '4':
            configs = config_manager.list_configs()
            print("\nAvailable Configurations:")
            for i, config in enumerate(configs, 1):
                print(f"{i}. {config}")

            config_choice = input("Select configuration to delete: ")
            try:
                selected_config = configs[int(config_choice) - 1]
                confirm = input(f"Are you sure you want to delete {selected_config}? (y/N): ")
                if confirm.lower() == 'y':
                    config_manager.delete_config(selected_config)
                    print(f"Configuration {selected_config} deleted.")
            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == '5':
            configs = config_manager.list_configs()
            print("\nAvailable Configurations:")
            for i, config in enumerate(configs, 1):
                print(f"{i}. {config}")

            base_choice = input("Select base configuration: ")
            overlay_choice = input("Select overlay configuration: ")

            try:
                base_config = configs[int(base_choice) - 1]
                overlay_config = configs[int(overlay_choice) - 1]

                merged_config = config_manager.merge_configs(base_config, overlay_config)
                print("\nMerged Configuration:")
                print(json.dumps(merged_config, indent=2))

                save_merged = input("Save merged configuration? (y/N): ").lower() == 'y'
                if save_merged:
                    merged_config_name = input("Enter name for merged configuration: ")
                    config_manager.save_config(merged_config_name, merged_config)
                    print(f"Merged configuration saved as {merged_config_name}")

            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == '6':
            break
        
        else:
            print("Invalid choice. Please try again.")

def main():
    """
    Main execution point for configuration manager
    """
    interactive_config_manager()

if __name__ == "__main__":
    main()



