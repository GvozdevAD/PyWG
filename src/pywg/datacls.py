from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True, frozen=True)
class Keys:
    public: str
    private: str


@dataclass(slots=True, frozen=True)
class InterfaceInfo:
    PathToConfig: Path
    Address: str
    PostUp: str
    PostDown: str
    ListenPort: str
    PrivateKey: str

    def __str__(self) -> str:
        return (
            f"Path: {self.path_to_config}\n"
            f"Address {self.Address}\n"
            f"PostUp {self.PostUp}\n"
            f"PostDown {self.PostDown}\n"
            f"ListenPort {self.ListenPort}\n"
            f"PrivateKey {self.PrivateKey}\n"
        )


@dataclass(slots=True, frozen=True)
class PeerInfo:
    title: str
    PublicKey: str
    AllowedIps: str

@dataclass(slots=True, frozen=True)
class ConfigInfo:
    interface: InterfaceInfo
    peers: list[PeerInfo]