#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Goertzel Test
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class goertzel_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Goertzel Test", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Goertzel Test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "goertzel_test")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.thresh_present = thresh_present = 0.05
        self.thresh_absent = thresh_absent = 0.1
        self.signal_freq2 = signal_freq2 = 1500
        self.signal_freq = signal_freq = 1000
        self.signal_amplitude2 = signal_amplitude2 = 1
        self.signal_amplitude = signal_amplitude = 1
        self.samp_rate = samp_rate = 32000
        self.goertzel_freq2 = goertzel_freq2 = 1500
        self.goertzel_freq = goertzel_freq = 1000
        self.gain = gain = 1

        ##################################################
        # Blocks
        ##################################################

        self._signal_freq2_range = qtgui.Range(0, 10000, 1, 1500, 200)
        self._signal_freq2_win = qtgui.RangeWidget(self._signal_freq2_range, self.set_signal_freq2, "'signal_freq2'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._signal_freq2_win)
        self._signal_freq_range = qtgui.Range(0, 10000, 1, 1000, 200)
        self._signal_freq_win = qtgui.RangeWidget(self._signal_freq_range, self.set_signal_freq, "'signal_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._signal_freq_win)
        self._signal_amplitude2_range = qtgui.Range(0, 5, 0.1, 1, 200)
        self._signal_amplitude2_win = qtgui.RangeWidget(self._signal_amplitude2_range, self.set_signal_amplitude2, "'signal_amplitude2'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._signal_amplitude2_win)
        self._signal_amplitude_range = qtgui.Range(0, 5, 0.1, 1, 200)
        self._signal_amplitude_win = qtgui.RangeWidget(self._signal_amplitude_range, self.set_signal_amplitude, "'signal_amplitude'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._signal_amplitude_win)
        self._goertzel_freq2_range = qtgui.Range(0, 10000, 1, 1500, 200)
        self._goertzel_freq2_win = qtgui.RangeWidget(self._goertzel_freq2_range, self.set_goertzel_freq2, "'goertzel_freq2'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._goertzel_freq2_win)
        self._goertzel_freq_range = qtgui.Range(0, 10000, 1, 1000, 200)
        self._goertzel_freq_win = qtgui.RangeWidget(self._goertzel_freq_range, self.set_goertzel_freq, "'goertzel_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._goertzel_freq_win)
        self._gain_range = qtgui.Range(0, 5, 1, 1, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "'gain'", "dial", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Output", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_1_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.goertzel_fc_0_0 = fft.goertzel_fc(samp_rate, 4096, goertzel_freq2)
        self.goertzel_fc_0 = fft.goertzel_fc(samp_rate, 4096, goertzel_freq)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(thresh_absent, thresh_present, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(thresh_absent, thresh_present, 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(gain)
        self.blocks_float_to_uchar_0_0 = blocks.float_to_uchar(1, 1, 0)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar(1, 1, 0)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_and_xx_0 = blocks.and_bb()
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, signal_freq2, signal_amplitude2, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, signal_freq, signal_amplitude, 0, 0)
        self.Freq2 = qtgui.number_sink(
            gr.sizeof_char,
            0,
            qtgui.NUM_GRAPH_VERT,
            1,
            None # parent
        )
        self.Freq2.set_update_time(0.10)
        self.Freq2.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.Freq2.set_min(i, -1)
            self.Freq2.set_max(i, 1)
            self.Freq2.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.Freq2.set_label(i, "Data {0}".format(i))
            else:
                self.Freq2.set_label(i, labels[i])
            self.Freq2.set_unit(i, units[i])
            self.Freq2.set_factor(i, factor[i])

        self.Freq2.enable_autoscale(False)
        self._Freq2_win = sip.wrapinstance(self.Freq2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._Freq2_win)
        self.Freq1 = qtgui.number_sink(
            gr.sizeof_char,
            0,
            qtgui.NUM_GRAPH_VERT,
            1,
            None # parent
        )
        self.Freq1.set_update_time(0.10)
        self.Freq1.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.Freq1.set_min(i, -1)
            self.Freq1.set_max(i, 1)
            self.Freq1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.Freq1.set_label(i, "Data {0}".format(i))
            else:
                self.Freq1.set_label(i, labels[i])
            self.Freq1.set_unit(i, units[i])
            self.Freq1.set_factor(i, factor[i])

        self.Freq1.enable_autoscale(False)
        self._Freq1_win = sip.wrapinstance(self.Freq1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._Freq1_win)
        self.And = qtgui.number_sink(
            gr.sizeof_char,
            0,
            qtgui.NUM_GRAPH_VERT,
            1,
            None # parent
        )
        self.And.set_update_time(0.10)
        self.And.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.And.set_min(i, -1)
            self.And.set_max(i, 1)
            self.And.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.And.set_label(i, "Data {0}".format(i))
            else:
                self.And.set_label(i, labels[i])
            self.And.set_unit(i, units[i])
            self.And.set_factor(i, factor[i])

        self.And.enable_autoscale(False)
        self._And_win = sip.wrapinstance(self.And.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._And_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_and_xx_0, 0), (self.And, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.Freq1, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_and_xx_0, 0))
        self.connect((self.blocks_float_to_uchar_0_0, 0), (self.Freq2, 0))
        self.connect((self.blocks_float_to_uchar_0_0, 0), (self.blocks_and_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.goertzel_fc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.goertzel_fc_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_float_to_uchar_0_0, 0))
        self.connect((self.goertzel_fc_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.goertzel_fc_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.goertzel_fc_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "goertzel_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_thresh_present(self):
        return self.thresh_present

    def set_thresh_present(self, thresh_present):
        self.thresh_present = thresh_present
        self.blocks_threshold_ff_0.set_hi(self.thresh_present)
        self.blocks_threshold_ff_0_0.set_hi(self.thresh_present)

    def get_thresh_absent(self):
        return self.thresh_absent

    def set_thresh_absent(self, thresh_absent):
        self.thresh_absent = thresh_absent
        self.blocks_threshold_ff_0.set_lo(self.thresh_absent)
        self.blocks_threshold_ff_0_0.set_lo(self.thresh_absent)

    def get_signal_freq2(self):
        return self.signal_freq2

    def set_signal_freq2(self, signal_freq2):
        self.signal_freq2 = signal_freq2
        self.analog_sig_source_x_0_0.set_frequency(self.signal_freq2)

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        self.signal_freq = signal_freq
        self.analog_sig_source_x_0.set_frequency(self.signal_freq)

    def get_signal_amplitude2(self):
        return self.signal_amplitude2

    def set_signal_amplitude2(self, signal_amplitude2):
        self.signal_amplitude2 = signal_amplitude2
        self.analog_sig_source_x_0_0.set_amplitude(self.signal_amplitude2)

    def get_signal_amplitude(self):
        return self.signal_amplitude

    def set_signal_amplitude(self, signal_amplitude):
        self.signal_amplitude = signal_amplitude
        self.analog_sig_source_x_0.set_amplitude(self.signal_amplitude)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.goertzel_fc_0.set_rate(self.samp_rate)
        self.goertzel_fc_0_0.set_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1.set_samp_rate(self.samp_rate)

    def get_goertzel_freq2(self):
        return self.goertzel_freq2

    def set_goertzel_freq2(self, goertzel_freq2):
        self.goertzel_freq2 = goertzel_freq2
        self.goertzel_fc_0_0.set_freq(self.goertzel_freq2)

    def get_goertzel_freq(self):
        return self.goertzel_freq

    def set_goertzel_freq(self, goertzel_freq):
        self.goertzel_freq = goertzel_freq
        self.goertzel_fc_0.set_freq(self.goertzel_freq)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_0.set_k(self.gain)




def main(top_block_cls=goertzel_test, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
