from __future__ import print_function
import sys
from time import time, sleep
import thread

import numpy as np
from PyQt4 import QtGui
from pymuse.ios import MuseIO, MuseIOError
from pymuse.signals import MultiChannelSignal

from mindpong_interface import MindpongInterface
from services.arduino_communication_service import arduino_communication_service

MUSE_BAND_POWER_ACQUISITION_FREQUENCY = 10
MUSE_NUMBER_ELECTRODES = 4
NUMBER_PLAYERS = 2
FIRST_PLAYER_PORT = 5001

def run_server(port, signal):
    try:
        server = MuseIO(port, {'concentration': signal})
        thread.start_new_thread(server.start,())
    except KeyboardInterrupt:
        print("End of program: Caught KeyboardInterrupt")
    except Exception as e:
        print("Caught error while creating server: %s" % e.message)


def update_data(signals, callbacks):
    update_period = 1.0 / signals[0].estimated_acquisition_freq
    last_update_time = time()
    signal_means = [0, 0]

    while True:
        current_time = time()
        if current_time - last_update_time > update_period:
            last_update_time = current_time
            try:
                signal_means = [get_signals_mean(signal) for signal in signals]
            except Exception as e:
                print (e)
            for callback in callbacks:
                callback(signal_means)
        else:
            sleep(update_period/10)
        

def get_signals_mean(signal):
    if signal.lock is not None:
        signal.lock.acquire()
    signal_means = np.nanmean(signal.data[:,-1])
    if signal.lock is not None:
        signal.lock.release()

    return signal_means


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = MindpongInterface()

    signals = [
        MultiChannelSignal(estimated_acquisition_freq=MUSE_BAND_POWER_ACQUISITION_FREQUENCY, number_of_channels=MUSE_NUMBER_ELECTRODES)
        for _ in range(NUMBER_PLAYERS)
    ]

    update_data_callbacks = [
        gui.change_images.emit,
        arduino_communication_service.send_data,
        lambda data: print('I am updating my data', data),
    ]

    for index, signal in enumerate(signals):
        run_server((FIRST_PLAYER_PORT + index), signal)

    try:
        thread.start_new_thread(update_data, (signals, update_data_callbacks))
    except:
        print("Error: unable to start thread")

    sys.exit(app.exec_())
