# A CLI based input/output reader

import subprocess
import shutil

from .util import format_time


def cli_input_loop(obj):
    """A CLI based input loop.

    `obj` is the object that the main thread (cf. the `run` function) uses to
    pass data to this thread.

    """

    def show_remaining_time():
        print(f'time left: {format_time(obj["remainingtime"])}')

    print('[p] to pause, [q] to quit, [ENTER] to see remaining time')
    show_remaining_time()

    while True:
        i = input()
        if i == 'p':
            show_remaining_time()
            print('Press any key to unpause ...')
            obj['paused'] = True
            input()
            obj['paused'] = False
        if i == '':
            show_remaining_time()
        if i == 'q':
            obj['bail'] = True
            show_remaining_time()
            print('exiting ...')
            break


if shutil.which('notify-send') is not None:
    def notify_user_done(msg):
        subprocess.run(['notify-send', msg])
else:
    def notify_user_done(msg):
        print(msg)
