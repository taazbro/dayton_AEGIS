#!/usr/bin/env python3
"""
Secrets Manager — Encrypt/decrypt sensitive files for safe storage
"""

import os
import sys
import base64
import hashlib
from cryptography.fernet import Fernet
from pathlib import Path


class SecretsManager:
    """Manages encryption and decryption of sensitive files."""

    def __init__(self, password: str = None):
        """
        Initialize secrets manager.

        Args:
            password: Master password for encryption (uses env var if not provided)
        """
        self.password = password or os.getenv("AEGIS_MASTER_PASSWORD")
        if not self.password:
            raise ValueError("Master password required. Set AEGIS_MASTER_PASSWORD or provide password.")

        self.key = self._derive_key(self.password)
        self.cipher = Fernet(self.key)

    def _derive_key(self, password: str) -> bytes:
        """
        Derive encryption key from password.

        Args:
            password: Master password

        Returns:
            32-byte encryption key
        """
        # Use PBKDF2 to derive key from password
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            b'aegis-salt-v1',  # Salt
            100000  # Iterations
        )
        return base64.urlsafe_b64encode(key)

    def encrypt_file(self, input_path: str, output_path: str = None) -> str:
        """
        Encrypt a file.

        Args:
            input_path: Path to file to encrypt
            output_path: Path to save encrypted file (defaults to input_path.encrypted)

        Returns:
            Path to encrypted file
        """
        if not output_path:
            output_path = f"{input_path}.encrypted"

        # Read file
        with open(input_path, 'rb') as f:
            data = f.read()

        # Encrypt
        encrypted_data = self.cipher.encrypt(data)

        # Write encrypted file
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

        print(f"✓ Encrypted: {input_path} → {output_path}")
        return output_path

    def decrypt_file(self, input_path: str, output_path: str = None) -> str:
        """
        Decrypt a file.

        Args:
            input_path: Path to encrypted file
            output_path: Path to save decrypted file (defaults to input_path without .encrypted)

        Returns:
            Path to decrypted file
        """
        if not output_path:
            output_path = input_path.replace('.encrypted', '')

        # Read encrypted file
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()

        # Decrypt
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data)
        except Exception as e:
            raise ValueError(f"Decryption failed. Wrong password? Error: {e}")

        # Write decrypted file
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        print(f"✓ Decrypted: {input_path} → {output_path}")
        return output_path

    def encrypt_env_file(self) -> str:
        """
        Encrypt .env file to .env.encrypted.

        Returns:
            Path to encrypted file
        """
        env_path = Path('.env')
        if not env_path.exists():
            raise FileNotFoundError(".env file not found")

        return self.encrypt_file(str(env_path), '.env.encrypted')

    def decrypt_env_file(self) -> str:
        """
        Decrypt .env.encrypted to .env.

        Returns:
            Path to decrypted file
        """
        encrypted_path = Path('.env.encrypted')
        if not encrypted_path.exists():
            raise FileNotFoundError(".env.encrypted file not found")

        return self.decrypt_file(str(encrypted_path), '.env')


def main():
    """CLI interface for secrets manager."""
    import argparse

    parser = argparse.ArgumentParser(description="AEGIS Secrets Manager")
    parser.add_argument('action', choices=['encrypt', 'decrypt', 'encrypt-env', 'decrypt-env'],
                        help='Action to perform')
    parser.add_argument('--file', help='File to encrypt/decrypt')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--password', help='Master password (or use AEGIS_MASTER_PASSWORD env var)')

    args = parser.parse_args()

    try:
        manager = SecretsManager(password=args.password)

        if args.action == 'encrypt':
            if not args.file:
                print("❌ --file required for encrypt action")
                sys.exit(1)
            manager.encrypt_file(args.file, args.output)

        elif args.action == 'decrypt':
            if not args.file:
                print("❌ --file required for decrypt action")
                sys.exit(1)
            manager.decrypt_file(args.file, args.output)

        elif args.action == 'encrypt-env':
            manager.encrypt_env_file()
            print("✓ .env encrypted successfully!")
            print("  You can now safely commit .env.encrypted to git")

        elif args.action == 'decrypt-env':
            manager.decrypt_env_file()
            print("✓ .env decrypted successfully!")
            print("  Remember: .env is in .gitignore and won't be committed")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
