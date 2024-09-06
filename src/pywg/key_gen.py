import base64

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
from pathlib import Path

from .datacls import Keys

class KeyGenWG:
    """
    Этот класс предоставляет методы для генерации ключей и сохранения 
    их в файл. Он содержит статические методы, поэтому его можно 
    использовать без создания экземпляра класса.
    """
    @staticmethod
    def generate_keys() -> Keys:
        """
        Метод генерирует пару ключей (приватный и публичный) для использования
        в протоколе WireGuard. Он возвращает объект Keys, содержащий 
        сгенерированные ключи в формате base64.

        :return: Возвращается объект Keys, содержащий оба ключа в виде строк base64.
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
        keys: Keys, 
        title: str,
        path_to_dir: Path = Path("/","etc", "wireguard", "keys")
    ) -> tuple[Path, Path]:
        """
        Метод сохраняет сгенерированные ключи в файлы на диске. 
        Названия файлов можно настроить с помощью параметра title, 
        а директория для сохранения ключей задается параметром path_to_dir. 
        Метод возвращает кортеж с путями к созданным файлам.

        :param keys: Объект класса Keys, содержащий приватный и публичный ключи
        :param title: Строка, используемая для формирования названий файлов 
            (например, "wg0"). Если title не задан, файлы будут названы 
            как privatekey и publickey
        param path_to_dir: Путь к директории, в которой будут сохранены файлы. 
            По умолчанию — /etc/wireguard/keys
        """
        name_privatekey = f"{title}_privatekey" if title else "privatekey"
        with open(path_to_dir / name_privatekey, "w") as file:
            file.write(keys.private)
        
        name_publickey = f"{title}_publickey" if title else "publickey"
        with open(path_to_dir / name_publickey, "w") as file:
                    file.write(keys.public)
        return path_to_dir / name_publickey, path_to_dir / name_privatekey