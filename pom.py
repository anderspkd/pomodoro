#!/usr/bin/env python3

# Copyright: Anders Dalskov, 2018
# See LICENSE

import argparse
import time

from pom.cli import Cli
from pom.notify import notify_user_done
from pom.util import parse_time

description = """
Pomodoro technique utility.

The basic idea of the Pomodoro study technique is to work in intervals of e.g.,
25 minutes. A short break is taken after each interval, and after a couple of
intervals, a longer break is held.

See: https://en.wikipedia.org/wiki/Pomodoro_Technique
"""

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--message',
                    help='notification message',
                    default='ding!'
)
parser.add_argument('--interval',
                    help='interval time',
                    default='25m'
)
args = parser.parse_args()


def run(interval, msg, input_handler):
    """Main loop.

    Information about whether or not the user bailed, paused as well as
    remaining time and so on, is stored in `obj`. This dict is used to
    communicate with the thread handling user input.

    """

    # setup the "communication channel" with the other thread.
    obj = {'remainingtime': parse_time(interval), 'paused': False,
           'bail': False}

    _ = input_handler(obj)

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
    run(args.interval, args.message, Cli)
