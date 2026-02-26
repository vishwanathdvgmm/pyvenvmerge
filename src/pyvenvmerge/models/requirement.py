from dataclasses import dataclass

@dataclass
class Requirement:
    name: str
    version: str
    raw_line: str
