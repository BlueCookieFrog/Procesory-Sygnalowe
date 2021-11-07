import os
from dataclasses import dataclass, field


class pipeline_settings:
    def __init__(self) -> None:

        self.input_file: str = "/home/borys/Documents/_Git/Procesory-Sygnalowe/sample.wav"
        self.output_file: str = "/tmp/pipeline_out.wav"

        self.highpass = highpass_settings()
        self.lowpass = lowpass_settings()
        self.echo = echo_settings()
        self.equalizer = equalizer_settings()


@dataclass()
class highpass_settings:
    """Highpass filter settings"""

    enabled: bool = False
    cutoff: float = 3       # 0
    length: int = 101       # 101
    mode: int = 1           # 1
    window: int = 0         # 0


@dataclass()
class lowpass_settings:
    """Lowpass filter settings"""

    enabled: bool = False
    cutoff: float = 5       # 0
    mode: int = 0           # 0
    poles: int = 4          # 4
    ripple: float = 0.25    # 0.25
    type: int = 1           # 1


@dataclass()
class echo_settings:
    """Echo filter settings"""

    enabled: bool = False
    delay: int = 1          # 1
    feedback: float = 0.0   # 0.0
    intensity: float = 0.0  # 0.0
    max_delay: int = 1      # 1


@dataclass()
class equalizer_settings:
    """Equalizer settings"""

    enabled: bool = False
    bands: list = field(default_factory=lambda: [0.0 for _ in range(10)])
