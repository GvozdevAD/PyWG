import subprocess

class WireGuard:
    def __init__(self) -> None:
        pass

    def apply(self):
        """Применение конфигурации WireGuard"""
        config_path = self.generate_config()
        subprocess.run(
            ["wg-quick", "up", self.interface_name], 
            check=True
        )
    
    def down(self):
        """Отключение WireGuard интерфейса"""
        subprocess.run(
            ["wg-quick", "down", self.interface_name],
            check=True
        )

    def status(self):
        """Получение статуса WireGuard интерфейса"""
        result = subprocess.run(
            ["wg", "show", self.interface_name], 
            capture_output=True, 
            text=True
        )
        return result.stdout
