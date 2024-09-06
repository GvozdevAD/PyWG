import configparser
import subprocess

from pathlib import Path

class Interface:
    def __init__(
            self,
            interface_name: str,
            config_path: Path =  Path("etc","wireguard")
    ) -> None:
        self.interface_name = interface_name
        self.config_path = config_path
        self.config = configparser.ConfigParser(
            allow_no_value=True
        )
        self.check_config = None

    def check_config(self) -> bool:
        """
        """
        if not (self.congig_path / self.interface_name).exists:
            """
            """
            return False
        return True

    def create_config(
            self,
            addres: str = "10.0.0.1/24",
            port: str = 51820,
            private_key: str = None,
            post_up: str = "iptables -A FORWARD -i %i -j ACCEPT;"\
                " iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
            post_down: str = "iptables -D FORWARD -i %i -j ACCEPT;"\
                " iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE"
    ):
        """
        [Interface]
        Address = 10.0.0.1/24
        PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
        PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
        ListenPort = 51820
        PrivateKey = <SERVER-PRIV-KEY>
        """
        pass
        
    def read_config(
            self,
    ):
        """
        """
    
    