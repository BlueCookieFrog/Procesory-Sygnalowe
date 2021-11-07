import os
from dataclasses import dataclass, field


class pipeline_settings:
    def __init__(self) -> None:

        self.input_file: str = "/home/borys/Documents/_Git/Procesory-Sygnalowe/sample.wav"
        # self.input_file: str = "/home/borys/Documents/_Git/Procesory-Sygnalowe/sine.wav"
        self.output_file: str = "/tmp/pipeline_out.wav"

        self.highpass = highpass_settings()
        self.lowpass = lowpass_settings()
        self.echo = echo_settings()
        self.equalizer = equalizer_settings()
        self.karaoke = karaoke_settings()


@dataclass()
class highpass_settings:
    """Highpass filter settings
    https://gstreamer.freedesktop.org/documentation/audiofx/audiowsinclimit.html?gi-language=python"""

    enabled: bool = False
    cutoff: float = 3  # 0
    length: int = 101  # 101
    mode: int = 1  # 1
    window: int = 0  # 0


@dataclass()
class lowpass_settings:
    """Lowpass filter settings
    https://gstreamer.freedesktop.org/documentation/audiofx/audiocheblimit.html?gi-language=python"""

    enabled: bool = False
    cutoff: float = 5  # 0
    mode: int = 0  # 0
    poles: int = 4  # 4
    ripple: float = 0.25  # 0.25
    type: int = 1  # 1


@dataclass()
class echo_settings:
    """Echo filter settings
    https://gstreamer.freedesktop.org/documentation/audiofx/audioecho.html?gi-language=python"""

    enabled: bool = False
    delay: int = 1  # 1
    feedback: float = 0.0  # 0.0 (percent)
    intensity: float = 0.0  # 0.0 (percent)
    max_delay: int = 1  # 1


@dataclass()
class equalizer_settings:
    """Equalizer settings
    https://gstreamer.freedesktop.org/documentation/equalizer/equalizer-10bands.html?gi-language=python
    """

    enabled: bool = False
    bands: list = field(default_factory=lambda: [0.0 for _ in range(10)])


@dataclass()
class karaoke_settings:
    """Karaoke settings
    https://gstreamer.freedesktop.org/documentation/audiofx/audiokaraoke.html?gi-language=python"""

    enabled: bool = False
    filter_band: float = 220.0  # 220.0
    filter_width: float = 100.0  # 100
    level: float = 1.0  # 1.0 (percent)
    mono_level = 1.0  # 1.0 (percent)
