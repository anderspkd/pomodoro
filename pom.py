#!/usr/bin/env python3

# Copyright: Anders Dalskov, 2018
# See LICENSE

import argparse

from pom.cli import cli_input_loop, notify_user_done
from pom.main import run

description = """
Pomodoro technique utility.

The basic idea of the Pomodoro study technique is to work in intervals of e.g.,
25 minutes. A short break is taken after each interval, and after a couple of
intervals, a longer break is held.

See: https://en.wikipedia.org/wiki/Pomodoro_Technique
"""

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
    run(a.interval, a.message, cli_input_loop, notify_user_done)
