from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Keys:
    public: str
    private: str