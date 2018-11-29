# Main loop

import time
import threading

from .util import parse_time

def run(interval, msg, input_fun, notify_fun):
    """Main loop.

    Information about whether or not the user bailed, paused as well as
    remaining time and so on, is stored in `obj`. This dict is used to
    communicate with the thread handling user input.

    """

    # setup the "communication channel" with the other thread.
    obj = {'remainingtime': parse_time(interval), 'paused': False,
           'bail': False}

    # start input thread
    t = threading.Thread(target=input_fun, args=(obj,), daemon=True)
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
        notify_fun(msg)
