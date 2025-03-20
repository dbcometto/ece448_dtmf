#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: DTMF Encoder
# Author: Ben Cometto
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from GRCdtmfgenerator import GRCdtmfgenerator  # grc-generated hier_block
from dtmf_goertzel_bank import dtmf_goertzel_bank  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class dtmf_encoder(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "DTMF Encoder", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("DTMF Encoder")
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

        self.settings = Qt.QSettings("GNU Radio", "dtmf_encoder")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sleeptime = sleeptime = 10
        self.samp_rate = samp_rate = 32000
        self.ontime = ontime = 5
        self.offtime = offtime = 1
        self.message = message = "12 45"
        self.goertzel_length = goertzel_length = 1024
        self.default_message = default_message = "12 34 56 78 90 AB CD *#"
        self.char_per_sec = char_per_sec = 1

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_char,
            0,
            qtgui.NUM_GRAPH_VERT,
            4,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.00001)
        self.qtgui_number_sink_0.set_title("")

        labels = ['1', '2', '3', '4', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(4):
            self.qtgui_number_sink_0.set_min(i, 0)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "DTMF Signal", #name
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
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
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
        self.dtmf_goertzel_bank_0 = dtmf_goertzel_bank(
            gain=3,
            goertzel_length=1024,
            samp_rate=32000,
        )

        self.top_layout.addWidget(self.dtmf_goertzel_bank_0)
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_char*1, 4)
        self.GRCdtmfgenerator_0 = GRCdtmfgenerator(
            char_per_sec=char_per_sec,
            dtmftext=message,
            offtime=offtime,
            ontime=ontime,
            samp_rate=samp_rate,
            sleeptime=sleeptime,
        )

        self.top_layout.addWidget(self.GRCdtmfgenerator_0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.GRCdtmfgenerator_0, 0), (self.dtmf_goertzel_bank_0, 0))
        self.connect((self.GRCdtmfgenerator_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 2), (self.qtgui_number_sink_0, 2))
        self.connect((self.blocks_vector_to_streams_0, 1), (self.qtgui_number_sink_0, 1))
        self.connect((self.blocks_vector_to_streams_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 3), (self.qtgui_number_sink_0, 3))
        self.connect((self.dtmf_goertzel_bank_0, 0), (self.blocks_vector_to_streams_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "dtmf_encoder")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sleeptime(self):
        return self.sleeptime

    def set_sleeptime(self, sleeptime):
        self.sleeptime = sleeptime
        self.GRCdtmfgenerator_0.set_sleeptime(self.sleeptime)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.GRCdtmfgenerator_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_ontime(self):
        return self.ontime

    def set_ontime(self, ontime):
        self.ontime = ontime
        self.GRCdtmfgenerator_0.set_ontime(self.ontime)

    def get_offtime(self):
        return self.offtime

    def set_offtime(self, offtime):
        self.offtime = offtime
        self.GRCdtmfgenerator_0.set_offtime(self.offtime)

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
        self.GRCdtmfgenerator_0.set_dtmftext(self.message)

    def get_goertzel_length(self):
        return self.goertzel_length

    def set_goertzel_length(self, goertzel_length):
        self.goertzel_length = goertzel_length

    def get_default_message(self):
        return self.default_message

    def set_default_message(self, default_message):
        self.default_message = default_message

    def get_char_per_sec(self):
        return self.char_per_sec

    def set_char_per_sec(self, char_per_sec):
        self.char_per_sec = char_per_sec
        self.GRCdtmfgenerator_0.set_char_per_sec(self.char_per_sec)




def main(top_block_cls=dtmf_encoder, options=None):

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
