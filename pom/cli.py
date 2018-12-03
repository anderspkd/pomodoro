# Copyright: Anders Dalskov, 2018
# See LICENSE

# CLI based interface.

import threading

from .util import format_time


class Cli():
    """A CLI based user interface. Which makes this a TUI, I suppose.

    Supports three commands:

    `p` pauses the timer,
    `q` exists the program
    `ENTER` shows the remaining time.

    """

    def __init__(self, obj):
        self.obj = obj
        self._thr = threading.Thread(target=self.run, daemon=True)
        self._thr.start()

    def show_remaining_time(self):
        ts = format_time(self.obj['remainingtime'])
        print(f'time left: {ts}')

    def run(self):
        print('[p] to pause, [q] to quit, [ENTER] to see remaining time')
        self.show_remaining_time()

        while True:
            i = input()
            if i == 'p':
                self.show_remaining_time()
                print('PAUSED. Press any key to unpause ...')
                self.obj['paused'] = True
                input()
                self.obj['paused'] = False
                print('Resuming ...')
            if i == '':
                self.show_remaining_time()
            if i == 'q':
                self.obj['bail'] = True
                self.show_remaining_time()
                print('exiting ...')
                break
