from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True, frozen=True)
class Keys:
    public: str
    private: str

@dataclass(slots=True, frozen=True)
class ConfigInfo:
    path_to_config: Path
    address: str
    postup: str
    postdown: str
    listenport: str
    privatekey: str

    def __str__(self) -> str:
        return (
            f"Path: {self.path_to_config}\n"
            f"Address {self.address}\n"
            f"PostUp {self.postup}\n"
            f"PostDown {self.postdown}\n"
            f"ListenPort {self.listenport}\n"
            f"PrivateKey {self.privatekey}\n"
        )