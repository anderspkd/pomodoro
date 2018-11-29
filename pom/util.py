# various utility functions related for the most part to dealing with strings
# that represent units of time.

import re


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
