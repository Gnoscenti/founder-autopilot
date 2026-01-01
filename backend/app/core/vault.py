"""Secure vault for storing API keys and credentials."""
from cryptography.fernet import Fernet
from typing import Optional, Dict
import json
import os
from pathlib import Path


class SecretVault:
    """Encrypted storage for API keys and credentials."""
    
    def __init__(self, vault_path: str = "./data/vault.enc", encryption_key: Optional[str] = None):
        self.vault_path = Path(vault_path)
        
        # Initialize or load encryption key
        if encryption_key:
            self.key = encryption_key.encode()
        else:
            self.key = self._get_or_create_key()
        
        self.cipher = Fernet(self.key)
        self.secrets: Dict[str, str] = {}
        
        # Load existing vault if it exists
        if self.vault_path.exists():
            self._load()
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key."""
        key_path = self.vault_path.parent / ".vault_key"
        
        if key_path.exists():
            return key_path.read_bytes()
        else:
            # Generate new key
            key = Fernet.generate_key()
            key_path.parent.mkdir(parents=True, exist_ok=True)
            key_path.write_bytes(key)
            # Secure the key file
            os.chmod(key_path, 0o600)
            return key
    
    def _load(self):
        """Load and decrypt vault."""
        try:
            encrypted_data = self.vault_path.read_bytes()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            self.secrets = json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Warning: Could not load vault: {e}")
            self.secrets = {}
    
    def _save(self):
        """Encrypt and save vault."""
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        
        json_data = json.dumps(self.secrets, indent=2)
        encrypted_data = self.cipher.encrypt(json_data.encode())
        
        self.vault_path.write_bytes(encrypted_data)
        # Secure the vault file
        os.chmod(self.vault_path, 0o600)
    
    def set_secret(self, key: str, value: str):
        """Store a secret."""
        self.secrets[key] = value
        self._save()
    
    def get_secret(self, key: str) -> Optional[str]:
        """Retrieve a secret."""
        return self.secrets.get(key)
    
    def delete_secret(self, key: str):
        """Delete a secret."""
        if key in self.secrets:
            del self.secrets[key]
            self._save()
    
    def list_keys(self) -> list[str]:
        """List all secret keys (not values)."""
        return list(self.secrets.keys())
    
    def has_secret(self, key: str) -> bool:
        """Check if a secret exists."""
        return key in self.secrets


# Global vault instance
vault = SecretVault()


# Convenience functions for common credentials
def get_stripe_key() -> Optional[str]:
    """Get Stripe API key."""
    # Try environment variable first
    key = os.getenv("STRIPE_API_KEY")
    if key:
        return key
    # Fall back to vault
    return vault.get_secret("stripe_api_key")


def get_gcloud_credentials() -> Optional[str]:
    """Get Google Cloud credentials path."""
    path = os.getenv("GCLOUD_CREDENTIALS_PATH")
    if path:
        return path
    return vault.get_secret("gcloud_credentials_path")


def get_email_credentials() -> Optional[Dict[str, str]]:
    """Get email provider credentials."""
    provider = os.getenv("EMAIL_PROVIDER", "smtp")
    
    if provider == "smtp":
        return {
            "host": os.getenv("SMTP_HOST") or vault.get_secret("smtp_host"),
            "port": os.getenv("SMTP_PORT") or vault.get_secret("smtp_port"),
            "username": os.getenv("SMTP_USERNAME") or vault.get_secret("smtp_username"),
            "password": os.getenv("SMTP_PASSWORD") or vault.get_secret("smtp_password"),
        }
    
    # Add other providers as needed
    return None
