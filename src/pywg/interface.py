import configparser

from pathlib import Path

from .datacls import InterfaceInfo
from .key_gen import KeyGenWG

from .exceptions import FileConfNotFound

class Interface:
    def __init__(
            self,
            interface_name: str = "wg0",
            config_path: Path =  Path("/","etc","wireguard")
    ) -> None:
        """
        Инициализация объекта Interface.
        
        :param interface_name: Название интерфейса WireGuard, по умолчанию "wg0".
        :param config_path: Путь к директории для конфигурационных файлов, по умолчанию "/etc/wireguard".
        """
        self.interface_name = interface_name
        self.config_path = config_path
        self.check_config = (
            self.config_path / f"{self.interface_name}.conf"
        ).exists()

    def create_interface(
            self,
            address: str = "10.0.0.1/24",
            port: str = 51820,
            private_key: str = None,
            post_up: str = f"iptables -A FORWARD -i %i -j ACCEPT;"+
                " iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
            post_down: str = f"iptables -D FORWARD -i %i -j ACCEPT;"+
                " iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE"
    ) -> InterfaceInfo:
        """
        Создание и запись конфигурационного файла для интерфейса WireGuard.

        Если файл конфигурации уже существует, он будет прочитан и 
        возвращена информация о интерфейсе.
        Если приватный ключ не предоставлен, он будет сгенерирован и сохранен.

        :param address: IP-адрес и маска подсети для интерфейса WireGuard.
        :param port: Порт, на котором будет слушать интерфейс.
        :param private_key: Приватный ключ для интерфейса WireGuard. Если None, будет сгенерирован новый.
        :param post_up: Команды для выполнения после запуска интерфейса.
        :param post_down: Команды для выполнения при остановке интерфейса.
        :return: Объект ConfigInfo с информацией о конфигурации.
        """
        if self.check_config:
            return self.read_config()
        
        config_override = configparser.RawConfigParser()
        config_override.optionxform = str
        if not private_key:
            keys = KeyGenWG.generate_keys()
            
            if not (self.config_path / "keys").exists():
                (self.config_path / "keys").mkdir()
            
            KeyGenWG.save_keys_to_file(
                keys, 
                self.interface_name, 
                self.config_path / "keys"
            )
            private_key = keys.private

        config_override["Interface"] = {
            "Address": address,
            "PostUp": post_up,
            "PostDown": post_down,
            "ListenPort": port,
            "PrivateKey": private_key,
        }
        with open(self.config_path / f"{self.interface_name}.conf", "w") as configfile:
            config_override.write(configfile)
        
        return InterfaceInfo(
            self.config_path / f"{self.interface_name}.conf",
            address,
            post_up, 
            post_down,
            port, 
            keys.private
        )
        
    def read_interface(
            self,
    ) -> InterfaceInfo:
        """
        Чтение конфигурационного файла и возврат информации о интерфейсе.
        
        :return: Объект InterfaceInfo с информацией о интерфейсе.
        """
        if not self.check_config:
            raise FileConfNotFound("Файл конфигурации не найден!")
        config = configparser.RawConfigParser()
        config.optionxform = str
        config.read(
            self.config_path/f"{self.interface_name}.conf"
        )
        interface = config["Interface"]
        return InterfaceInfo(
            self.config_path/f"{self.interface_name}.conf",
            **interface
        )