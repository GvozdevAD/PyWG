import base64

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
from pathlib import Path

from datacls import Keys

class KeyGenWG:
    @staticmethod
    def generate_keys() -> Keys:
        """
        """
        private_key = x25519.X25519PrivateKey.generate()
        private_key_bytes = private_key.private_bytes(
            serialization.Encoding.Raw,
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption()
        )

        public_key = private_key.public_key()
        public_key_bytes = public_key.public_bytes(
            serialization.Encoding.Raw,
            serialization.PublicFormat.Raw
        )

        private_key_b64 = base64.b64encode(
            private_key_bytes
        ).decode('utf-8')
        public_key_b64 = base64.b64encode(
            public_key_bytes
        ).decode('utf-8')

        return Keys(public_key_b64, private_key_b64)
    
    @staticmethod
    def save_keys_to_file(
        key: str, 
        title: str
    ) -> Path:
        """
        """