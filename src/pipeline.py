import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstAudio", "1.0")
from gi.repository import Gst, GObject, GLib
from settings import pipeline_settings
import os

Gst.init(None)


class Pipeline:
    def __init__(self, settings: pipeline_settings) -> None:

        self.mainloop = GLib.MainLoop()
        self.pipeline = Gst.Pipeline()

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::error", self.on_error)

        self.settings = settings

        self.src = Gst.ElementFactory.make("filesrc")
        self.src.set_property("location", self.settings.input_file)

        self.decodebin = Gst.ElementFactory.make("decodebin")
        self.decodebin.connect("pad-added", self._on_pad_added)
        # Audio convert
        self.audioconvert = Gst.ElementFactory.make('audioconvert', 'convert')

        self.highpass = None
        self.lowpass = None
        self.echo = None
        self.equalizer = None
        self.karaoke = None

        if self.settings.highpass.enabled:
            self._highpass_filter()

        if self.settings.lowpass.enabled:
            self._lowpass_filter()

        if self.settings.echo.enabled:
            self._echo()

        if self.settings.equalizer.enabled:
            self._equalizer()

        if self.settings.karaoke.enabled:
            self._karaoke()

        self.wavenc = Gst.ElementFactory.make("wavenc")
        self.filesink = Gst.ElementFactory.make("filesink")
        self.filesink.set_property("location", self.settings.output_file)

        # Add elements to the pipeline
        self.pipeline.add(self.src)
        self.pipeline.add(self.decodebin)
        self.pipeline.add(self.audioconvert)
        self.pipeline.add(self.wavenc)
        self.pipeline.add(self.filesink)

        # Link elements
        self.src.link(self.decodebin)
        self.wavenc.link(self.filesink)
        self._link()

    def _on_pad_added(self, decodebin, pad):
        """Used as callback to connect decodebin to the pipeline."""
        caps = pad.get_current_caps()
        compatible_pad = self.audioconvert.get_compatible_pad(pad, caps)
        pad.link(compatible_pad)

    def _highpass_filter(self) -> None:
        """Adds audiowsinclimit element"""
        self.highpass = Gst.ElementFactory.make("audiowsinclimit")
        self.highpass.set_property("cutoff", self.settings.highpass.cutoff)
        self.highpass.set_property("length", self.settings.highpass.length)
        self.highpass.set_property("mode", self.settings.highpass.mode)
        self.highpass.set_property("window", self.settings.highpass.window)

        self.pipeline.add(self.highpass)

    def _lowpass_filter(self) -> None:
        """Adds audiocheblimit element"""
        self.lowpass = Gst.ElementFactory.make("audiocheblimit")
        self.lowpass.set_property("cutoff", self.settings.lowpass.cutoff)
        self.lowpass.set_property("mode", self.settings.lowpass.mode)
        self.lowpass.set_property("poles", self.settings.lowpass.poles)
        self.lowpass.set_property("ripple", self.settings.lowpass.ripple)
        self.lowpass.set_property("type", self.settings.lowpass.type)

        self.pipeline.add(self.lowpass)

    def _echo(self) -> None:
        """Adds echo element"""
        self.echo = Gst.ElementFactory.make("audioecho")
        self.echo.set_property("delay", self.settings.echo.delay)
        self.echo.set_property("feedback", self.settings.echo.feedback)
        self.echo.set_property("intensity", self.settings.echo.intensity)
        self.echo.set_property("max_delay", self.settings.echo.max_delay)

        self.pipeline.add(self.echo)

    def _equalizer(self) -> None:
        """Adds equalizer element"""
        self.equalizer = Gst.ElementFactory.make("equalizer-10bands")
        for i in range(10):
            self.equalizer.set_property(f"band{i}", self.settings.equalizer.bands[i])

        self.pipeline.add(self.equalizer)

    def _karaoke(self) -> None:
        """Adds karaoke element"""
        self.karaoke = Gst.ElementFactory.make("audiokaraoke")
        self.karaoke.set_property("filter-band", self.settings.karaoke.filter_band)
        self.karaoke.set_property("filter-width", self.settings.karaoke.filter_width)
        self.karaoke.set_property("level", self.settings.karaoke.level)
        self.karaoke.set_property("mono-level", self.settings.karaoke.mono_level)

    def _link(self) -> None:
        elements = (
            self.highpass,
            self.lowpass,
            self.echo,
            self.equalizer,
            self.karaoke,
        )

        last = None
        for each in elements:
            if each and last:
                last.link(each)
                last = each
            elif each:
                self.audioconvert.link(each)
                last = each
        if last:
            last.link(self.wavenc)
        else:
            raise SystemExit("Error: No elements were created")

    def run(self) -> None:
        """Runs the pipeline"""
        self.pipeline.set_state(Gst.State.PLAYING)
        self.mainloop.run()

    def kill(self) -> None:
        """Stops the pipeline"""
        self.pipeline.set_state(Gst.State.NULL)
        self.mainloop.quit()

    def on_eos(self, bus, msg) -> None:
        """Callback to stop pipeline on EOS"""
        print(f"EOS: Reached end of stream, stopping pipeline")
        self.kill()

    def on_error(self, bus, msg) -> None:
        """Calback to stop pipeline on error"""
        print(f"Error: {msg.parse_error()}")
        self.kill()

    def graph_pipeline(self) -> None:
        with open("/tmp/pipeline.dot", "w") as f:
            f.write(Gst.debug_bin_to_dot_data(self.pipeline, Gst.DebugGraphDetails.ALL))
        try:
            os.system("dot -Tpdf -o /tmp/pipeline.pdf /tmp/pipeline.dot")
        except Exception as e:
            print(e)


if __name__ == "__main__":

    settings = pipeline_settings()
    # settings.highpass.enabled = True
    # settings.highpass.cutoff = 500.0

    # settings.lowpass.enabled = True

    # settings.echo.enabled = True
    # settings.echo.delay = 5000
    # settings.echo.feedback = 0.5
    # settings.echo.intensity = 0.3

    # settings.equalizer.enabled = True
    # settings.equalizer.bands[0] = -24.0
    # settings.equalizer.bands[1] = -24.0
    # settings.equalizer.bands[2] = -24.0
    # settings.equalizer.bands[3] = -24.0
    pipeline = Pipeline(settings)
    pipeline.graph_pipeline()
    pipeline.run()
