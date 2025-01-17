import os
import json
import base64
from cryptography.fernet import Fernet
from typing import Dict, Optional

class SecureAPIKeyManager:
    def __init__(self, key_storage_path: str = os.path.expanduser("~/.ai_api_keys")):
        """
        Initialize the API Key Manager with secure storage
        
        Args:
            key_storage_path (str): Path to store encrypted API keys
        """
        self.key_storage_path = key_storage_path
        self._ensure_storage_dir()
        self._load_encryption_key()

    def _ensure_storage_dir(self):
        """Ensure the key storage directory exists"""
        os.makedirs(self.key_storage_path, exist_ok=True)

    def _load_encryption_key(self):
        """
        Load or generate an encryption key
        
        The key is stored in a separate file and used for encrypting/decrypting API keys
        """
        key_file = os.path.join(self.key_storage_path, 'encryption.key')
        
        if not os.path.exists(key_file):
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        
        with open(key_file, 'rb') as f:
            self.encryption_key = f.read()
        
        self.cipher_suite = Fernet(self.encryption_key)

    def store_api_key(self, service: str, api_key: str):
        """
        Securely store an API key for a specific service
        
        Args:
            service (str): Name of the service (e.g., 'openai', 'google')
            api_key (str): API key to store
        """
        encrypted_key = self.cipher_suite.encrypt(api_key.encode())
        
        key_file = os.path.join(self.key_storage_path, f'{service}_key.enc')
        with open(key_file, 'wb') as f:
            f.write(encrypted_key)

    def retrieve_api_key(self, service: str) -> Optional[str]:
        """
        Retrieve a decrypted API key for a specific service
        
        Args:
            service (str): Name of the service
        
        Returns:
            Optional[str]: Decrypted API key or None if not found
        """
        key_file = os.path.join(self.key_storage_path, f'{service}_key.enc')
        
        if not os.path.exists(key_file):
            return None
        
        with open(key_file, 'rb') as f:
            encrypted_key = f.read()
        
        try:
            decrypted_key = self.cipher_suite.decrypt(encrypted_key).decode()
            return decrypted_key
        except Exception as e:
            print(f"Error decrypting API key for {service}: {e}")
            return None

    def list_stored_services(self) -> list:
        """
        List all services with stored API keys
        
        Returns:
            list: Services with stored keys
        """
        services = []
        for filename in os.listdir(self.key_storage_path):
            if filename.endswith('_key.enc'):
                services.append(filename.replace('_key.enc', ''))
        return services

    def delete_api_key(self, service: str):
        """
        Delete an API key for a specific service
        
        Args:
            service (str): Name of the service
        """
        key_file = os.path.join(self.key_storage_path, f'{service}_key.enc')
        
        if os.path.exists(key_file):
            os.remove(key_file)

    def validate_api_key(self, service: str, api_key: str) -> bool:
        """
        Validate an API key for a specific service
        
        Args:
            service (str): Name of the service
            api_key (str): API key to validate
        
        Returns:
            bool: Whether the API key is valid
        """
        try:
            if service == 'openai':
                import openai
                openai.api_key = api_key
                openai.Model.list()
            elif service == 'google':
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                genai.list_models()
            elif service == 'anthropic':
                from anthropic import Anthropic
                client = Anthropic(api_key=api_key)
                client.models.list()
            return True
        except Exception as e:
            print(f"API key validation failed for {service}: {e}")
            return False

def interactive_key_setup():
    """
    Interactive CLI for setting up and managing API keys
    """
    manager = SecureAPIKeyManager()
    
    while True:
        print("\n--- API Key Manager ---")
        print("1. Store API Key")
        print("2. Retrieve API Key")
        print("3. List Stored Services")
        print("4. Delete API Key")
        print("5. Validate API Key")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            service = input("Enter service name (openai/google/anthropic): ").lower()
            api_key = input("Enter API key: ")
            manager.store_api_key(service, api_key)
            print(f"API key for {service} stored successfully.")
        
        elif choice == '2':
            service = input("Enter service name: ").lower()
            key = manager.retrieve_api_key(service)
            print(f"API key for {service}: {key}")
        
        elif choice == '3':
            services = manager.list_stored_services()
            print("Stored Services:", services)
        
        elif choice == '4':
            service = input("Enter service name to delete: ").lower()
            manager.delete_api_key(service)
            print(f"API key for {service} deleted.")
        
        elif choice == '5':
            service = input("Enter service name: ").lower()
            api_key = input("Enter API key to validate: ")
            is_valid = manager.validate_api_key(service, api_key)
            print(f"API key validation result: {'Valid' if is_valid else 'Invalid'}")
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    interactive_key_setup

