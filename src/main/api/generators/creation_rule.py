from dataclasses import dataclass

from steps.base_steps import BaseSteps

@dataclass
class CreationRule:
    refex: str