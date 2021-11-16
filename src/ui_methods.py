from shutil import copyfile
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.MainWindow import Ui_ProcesorySygnaowe
from src.settings import pipeline_settings
from src.pipeline import Pipeline


class UiMethods:
    def __init__(
        self,
        ui: Ui_ProcesorySygnaowe,
        main_window: QtWidgets.QMainWindow,
        settings: pipeline_settings,
    ) -> None:

        self.ui = ui
        self.parent = main_window
        self.settings = settings

    def select_input_file(self) -> None:
        """Opens open file dialog and saves its location"""
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent, "Open file", "", "Audio files (*.wav)"
        )

        if file:
            self.settings.input_file = file
            self.ui.FilePath.setText(file)
            self.ui.Run.setEnabled(True)

    def save_path(self, file: str):
        """Checks if user typed extension"""

        if file.endswith(".wav"):
            return file
        else:
            return f"{file}.wav"

    def save_output(self) -> None:
        """Opens save file dialog and saves file to provided location"""
        file, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.parent, "Save file", "", ""
        )

        if file:
            try:
                copyfile(self.settings.output_file, self.save_path(file))
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Success")
                msg.setInformativeText("Output file saved successfully.")
                msg.setWindowTitle("File saved")
                msg.exec_()
            except Exception as e:
                print(e)
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("Error while saving file.")
                msg.setWindowTitle("Error")
                msg.exec_()

    # HighPass
    def update_highpass_settings(self):
        """Updates highpass settings"""
        self.settings.highpass.enabled = self.ui.enable_HighPass.isChecked()

        self.settings.highpass.cutoff = self.ui.highpass_cutoff.value()
        self.settings.highpass.length = self.ui.highpass_length.value()
        self.settings.highpass.window = self.ui.highpass_window.currentIndex()

    # LowPass
    def update_lowpass_settings(self):
        """Updates lowpass settings"""
        self.settings.lowpass.enabled = self.ui.enable_LowPass.isChecked()

        self.settings.lowpass.cutoff = self.ui.lowpass_cutoff.value()
        self.settings.lowpass.poles = self.ui.lowpass_poles.value()
        self.settings.lowpass.ripple = self.ui.lowpass_ripple.value()
        self.settings.lowpass.type = self.ui.lowpass_type.currentIndex() + 1

    # Echo
    def update_echo_settings(self):
        """Updates echo settings"""
        self.settings.echo.enabled = self.ui.enable_Echo.isChecked()

        self.settings.echo.delay = (
            self.ui.echo_delay.value() * 1000000
        )  # Gstreamer uses ns so we convert it to ms
        self.settings.echo.feedback = self.ui.echo_feedback.value() / 100
        self.settings.echo.intensity = self.ui.echo_intensity.value() / 100
        self.settings.echo.max_delay = self.settings.echo.delay * 10

    # Karaoke
    def update_karaoke_settings(self):
        """Updates karaoke settings"""
        self.settings.karaoke.enabled = self.ui.enable_Karaoke.isChecked()

        self.settings.karaoke.filter_band = self.ui.karaoke_filter_band.value()
        self.settings.karaoke.filter_width = self.ui.karaoke_filter_width.value()
        self.settings.karaoke.level = self.ui.karaoke_level.value() / 100
        self.settings.karaoke.mono_level = self.ui.karaoke_mono_level.value() / 100

    # Equalizer
    def update_equalizer_settings(self):
        """Updates equalizer values"""
        self.settings.equalizer.enabled = self.ui.enable_Equalizer.isChecked()

        self.settings.equalizer.bands[0] = self.ui.verticalSlider_0.value()
        self.settings.equalizer.bands[1] = self.ui.verticalSlider_1.value()
        self.settings.equalizer.bands[2] = self.ui.verticalSlider_2.value()
        self.settings.equalizer.bands[3] = self.ui.verticalSlider_3.value()
        self.settings.equalizer.bands[4] = self.ui.verticalSlider_4.value()
        self.settings.equalizer.bands[5] = self.ui.verticalSlider_5.value()
        self.settings.equalizer.bands[6] = self.ui.verticalSlider_6.value()
        self.settings.equalizer.bands[7] = self.ui.verticalSlider_7.value()
        self.settings.equalizer.bands[8] = self.ui.verticalSlider_8.value()
        self.settings.equalizer.bands[9] = self.ui.verticalSlider_9.value()

    def run_pipeline(self):
        """Runs pipeline"""
        # self.print_settings()
        pipeline = Pipeline(self.settings)
        pipeline.run()
        self.ui.SaveFile.setEnabled(True)

    def print_settings(self):
        """Prints settings class values"""
        print(self.settings)
