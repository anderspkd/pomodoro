#!/usr/bin/env python3

# Copyright: Anders Dalskov, 2018
# See LICENSE

import argparse
import time
import subprocess  # for send-notify
import threading
import re
import shutil


description = """
Pomodoro technique utility.

The basic idea of the Pomodoro study technique is to work in intervals of e.g.,
25 minutes. A short break is taken after each interval, and after a couple of
intervals, a longer break is held.

See: https://en.wikipedia.org/wiki/Pomodoro_Technique
"""


RES = re.compile(r'[0-9]+s')
REM = re.compile(r'[0-9]+m')
REH = re.compile(r'[0-9]+h')


def parse_time(ts):
    """Convert a string specifying a time interval into seconds.

    Examples:

    parse_time('25m')    =>   60 * 25 = 1500
    parse_time('25m10s') =>   60 * 25 + 10 = 1510
    parse_time('2h10s')  =>   3600 * 2 + 10 = 7210

    The order of the units doesn't matter. I.e., '25m10s' and '10s25m' are
    equivalent.

    """
    s = 0

    # seconds
    m = re.search(RES, ts)
    if m is not None:
        ss = m.group(0)
        s = int(ss[:ss.index('s')])

    # minutes
    m = re.search(REM, ts)
    if m is not None:
        ss = m.group(0)
        s += int(ss[:ss.index('m')]) * 60

    # hours
    m = re.search(REH, ts)
    if m is not None:
        ss = m.group(0)
        s += int(ss[:ss.index('h')]) * 3600

    # assume a time of 0 is because we could not parse the user's input.
    if s == 0:
        raise ValueError(f'could not parse string: {ts}')
    else:
        return s


def format_time(tm):
    """Converts an integer intepreted as seconds into a readable
    representation. This is essentially the reverse of `parse_time`.

    Examples:

    format_time(1500)  =>  '25 minutes'
    format_time(1510)  =>  '25 minutes 10 seconds'

    """
    tm = int(tm)

    if tm <= 1:
        return f'1 second!!'

    # x minute(s) y second(s)
    if 0 < tm < 3600:
        tm_m = tm // 60
        sm = f'{tm_m} minute{"" if tm_m == 1 else "s"}'
        tm_s = tm % 60
        ss = f'{tm_s} second{"" if tm_s == 1 else "s"}'
        if tm_m > 0:
            if tm_s > 0:
                return sm + ' ' + ss
            return sm
        return ss

    # x hour(s) y minute(s)
    if 3600 <= tm:
        tm_h = tm // 3600
        sh = f'{tm_h} hour{"" if tm_h == 1 else "s"}'
        tm_m = (tm % 3600) // 60
        sm = f'{tm_m} minute{"" if tm_m == 1 else "s"}'
        if tm_m > 0:
            return sh + ' ' + sm
        return sh


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


def run(interval, msg):
    """Main loop.

    Information about whether or not the user bailed, paused as well as
    remaining time and so on, is stored in `obj`. This dict is used to
    communicate with the thread handling user input.

    """

    # setup the "communication channel" with the other thread.
    obj = {'remainingtime': parse_time(interval), 'paused': False,
           'bail': False}

    # start input thread
    t = threading.Thread(target=cli_input_loop, args=(obj,), daemon=True)
    t.start()

    # we're done if `interval` time has elapsed or the user exited early.
    while not (obj['remainingtime'] <= 0 or obj['bail'] is True):
        time.sleep(1)
        # this is a bit crude, but works well enough for our purposes.
        obj['remainingtime'] -= 1
        if obj['paused']:
            # wait for user to unpause
            while obj['paused']:
                time.sleep(1)

    # finally, signal the user if we exited normally. Otherwise just exit
    # silently (we assume the user is aware of a premature exit, since this
    # would have been performed by the user)
    if not obj['bail']:
        notify_user_done(msg)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=description,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('--message',
                   help='notification message',
                   default='ding!'
    )
    p.add_argument('--interval',
                   help='interval time',
                   default='25m'
    )
    a = p.parse_args()
    run(a.interval, a.message)
