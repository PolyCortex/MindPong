import sys
from PyQt4 import QtGui
import time
import thread
import numpy as np

from pymuse.ios import MuseIO, MuseIOError
from pymuse.signals import MultiChannelSignal
from pymuse.processes import Process
from mindpong_interface import MindpongInterface

def update_data(update_frequency=20.0, gui=None, signal_P1=None, signal_P2=None):
    if gui is not None:
        times_web = 0.0
        while True:
            # put data in queue for HTML server to get it
            now = time.time()
            if now - times_web > 1.0 / update_frequency:
                analysis_frequency = 1.0 / (now - times_web)
                times_web = now

                if signal_P1.lock is not None:
                    signal_P1.lock.acquire()
                dP1 = np.nanmean(signal_P1.data[:,-1])
                if signal_P1.lock is not None:
                    signal_P1.lock.release()

                if signal_P2.lock is not None:
                    signal_P2.lock.acquire()
                dP2 = np.nanmean(signal_P2.data[:,-1])
                if signal_P2.lock is not None:
                    signal_P2.lock.release()

                print 'I am updating my data', dP1, dP2, analysis_frequency
                gui.change_images.emit([dP1, dP2])

            else:
                time.sleep(0.25 / update_frequency)


def run_server(port=5001, player_signal=None):
    signals = dict()

    # EEG signal
    if player_signal is None:
        signal_concentration = MultiChannelSignal(length=300,
                                                  estimated_acquisition_freq=10.0,
                                                  number_of_channels=4)
    else:
        signal_concentration = player_signal

    signals['concentration'] = signal_concentration

    # Initializing the server
    try:
        server = MuseIO(port, signals)
    except MuseIOError, err:
        print str(err)
        sys.exit(1)

    # Starting the server
    try:
        thread.start_new_thread(server.start, ())
    except KeyboardInterrupt:
        print "\nEnd of program: Caught KeyboardInterrupt"
        sys.exit(0)


def main():
    app = QtGui.QApplication(sys.argv)
    gui = MindpongInterface()

    signal_concentration_P1 = MultiChannelSignal(length=300,
                                                 estimated_acquisition_freq=10.0,
                                                 number_of_channels=4)

    signal_concentration_P2 = MultiChannelSignal(length=300,
                                                 estimated_acquisition_freq=10.0,
                                                 number_of_channels=4)

    run_server(port=5001, player_signal=signal_concentration_P1)
    run_server(port=5002, player_signal=signal_concentration_P2)


    update_frequency = 0.5
    try:
        thread.start_new_thread(update_data, (update_frequency, gui, signal_concentration_P1, signal_concentration_P2))
    except:
        print "Error: unable to start thread"

    sys.exit(app.exec_())

main()
