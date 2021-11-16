import os
from dataclasses import dataclass, field


class pipeline_settings:
    def __init__(self) -> None:

        self.input_file: str = ""
        self.output_file: str = "/tmp/pipeline_out.wav"

        self.highpass = highpass_settings()
        self.lowpass = lowpass_settings()
        self.echo = echo_settings()
        self.equalizer = equalizer_settings()
        self.karaoke = karaoke_settings()

    def __repr__(self) -> str:
        data = f"""
        Pipeline settings:
        In: {self.input_file}
        Out: {self.output_file}\n
        Highpass:
        {self.highpass}\n
        Lowpass:
        {self.lowpass}\n
        Echo:
        {self.echo}\n
        Karaoke:
        {self.karaoke}\n
        Equalizer:
        {self.equalizer}
        """
        return data


@dataclass(repr=True)
class highpass_settings:
    """Highpass filter settings
    https://gstreamer.freedesktop.org/documentation/audiofx/audiowsinclimit.html?gi-language=python"""

    enabled: bool = False
    cutoff: float = 0  # 0
    length: int = 101  # 101
    mode: int = 1  # 1 (highpass)
    window: int = 0  # 0


@dataclass(repr=True)
class lowpass_settings:
    """Lowpass filter settings
    https://gstreamer.freedesktop.org/documentation/audiofx/audiocheblimit.html?gi-language=python"""

    enabled: bool = False
    cutoff: float = 0  # 0
    mode: int = 0  # 0 (lowpass)
    poles: int = 4  # 4
    ripple: float = 0.25  # 0.25
    type: int = 1  # 1


@dataclass(repr=True)
class echo_settings:
    """Echo filter settings
    https://gstreamer.freedesktop.org/documentation/audiofx/audioecho.html?gi-language=python"""

    enabled: bool = False
    delay: int = 1000000  # 1000000 (ns) -> 1ms
    feedback: float = 0.0  # 0.0 (percent)
    intensity: float = 0.0  # 0.0 (percent)
    max_delay: int = 1000000  # 1 (ns)


@dataclass(repr=True)
class equalizer_settings:
    """Equalizer settings
    https://gstreamer.freedesktop.org/documentation/equalizer/equalizer-10bands.html?gi-language=python
    """

    enabled: bool = False
    bands: list = field(default_factory=lambda: [0.0 for _ in range(10)])


@dataclass(repr=True)
class karaoke_settings:
    """Karaoke settings
    https://gstreamer.freedesktop.org/documentation/audiofx/audiokaraoke.html?gi-language=python"""

    enabled: bool = False
    filter_band: float = 220.0  # 220.0
    filter_width: float = 100.0  # 100
    level: float = 1.0  # 1.0 (percent)
    mono_level = 1.0  # 1.0 (percent)
