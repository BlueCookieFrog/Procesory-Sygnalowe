import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from src.settings import pipeline_settings
from ui.MainWindow import Ui_ProcesorySygnaowe
from src.ui_methods import UiMethods


def main():

    app = QtWidgets.QApplication(sys.argv)

    settings = pipeline_settings()

    main_window = QtWidgets.QMainWindow()
    ui = Ui_ProcesorySygnaowe()
    ui.setupUi(main_window)
    ui.SaveFile.setEnabled(False)
    ui.Run.setEnabled(False)
    methods = UiMethods(ui=ui, main_window=main_window, settings=settings)

    # General
    ui.OpenFile.clicked.connect(lambda: methods.select_input_file())
    ui.Run.clicked.connect(lambda: methods.run_pipeline())
    ui.SaveFile.clicked.connect(lambda: methods.save_output())
    # HighPass
    ui.enable_HighPass.stateChanged.connect(lambda: methods.update_highpass_settings())
    ui.highpass_cutoff.valueChanged.connect(lambda: methods.update_highpass_settings())
    ui.highpass_length.valueChanged.connect(lambda: methods.update_highpass_settings())
    ui.highpass_window.currentIndexChanged.connect(
        lambda: methods.update_highpass_settings()
    )

    # LowPass
    ui.enable_LowPass.stateChanged.connect(lambda: methods.update_lowpass_settings())
    ui.lowpass_cutoff.valueChanged.connect(lambda: methods.update_lowpass_settings())
    ui.lowpass_poles.valueChanged.connect(lambda: methods.update_lowpass_settings())
    ui.lowpass_ripple.valueChanged.connect(lambda: methods.update_lowpass_settings())
    ui.lowpass_type.currentIndexChanged.connect(
        lambda: methods.update_lowpass_settings()
    )

    # Echo
    ui.enable_Echo.stateChanged.connect(lambda: methods.update_echo_settings())
    ui.echo_delay.valueChanged.connect(lambda: methods.update_echo_settings())
    ui.echo_feedback.valueChanged.connect(lambda: methods.update_echo_settings())
    ui.echo_intensity.valueChanged.connect(lambda: methods.update_echo_settings())

    # Karaoke
    ui.enable_Karaoke.stateChanged.connect(lambda: methods.update_karaoke_settings())
    ui.karaoke_filter_band.valueChanged.connect(
        lambda: methods.update_karaoke_settings()
    )
    ui.karaoke_filter_width.valueChanged.connect(
        lambda: methods.update_karaoke_settings()
    )
    ui.karaoke_level.valueChanged.connect(lambda: methods.update_karaoke_settings())
    ui.karaoke_mono_level.valueChanged.connect(
        lambda: methods.update_karaoke_settings()
    )

    # Equalizer
    ui.enable_Equalizer.stateChanged.connect(lambda: methods.update_equalizer_settings())
    ui.verticalSlider_0.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_1.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_2.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_3.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_4.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_5.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_6.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_7.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_8.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )
    ui.verticalSlider_9.valueChanged.connect(
        lambda: methods.update_equalizer_settings()
    )

    main_window.show()

    return app.exec_()


if __name__ == "__main__":

    sys.exit(main())
