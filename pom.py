#!/usr/bin/env python3

import argparse
import time
import subprocess
import os
import json

CONF_FILE = os.path.expanduser('~/.config/pom.conf')

desc = ('Pomodoro technique utility.'
        '\n\n'
        'If run without any arguments, it uses settings present in config file'
        '\n'
        'from $HOME/.config/pom.conf.')

p = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
p.add_argument('-m', help='message to show in notifcation',
               default='ding!', metavar='message')
p.add_argument('-t', help='interval time', metavar='time', type=int)
p.add_argument('-u', help='time unit', metavar='unit')
p.add_argument('--notify-time', help='time notification is visible', default=None)
p.add_argument('--config', help='config file')
args = p.parse_args()


t = m = u = None
msg = args.m

def read_settings_from_config(conf):
    global m
    global t
    global u

    if conf is None:
        with open(CONF_FILE, 'r') as f:
            x = json.loads(f.read())
    elif not os.path.exists(conf):
        print(f'No such file: {conf}')
        exit(1)
    else:
        with open(conf, 'r') as f:
            x = json.loads(f.read())

    t = int(x['time'])
    u = x['unit']
    if 'message' in x:
        msg = x['message']
    if u in ('s', 'seconds'):
        m = 1
        u = 'seconds'
    elif u in ('m', 'minutes'):
        m = 60
        u = 'minutes'
    elif u in ('h', 'hours'):
        m = 60 * 60
        u = 'hours'
    if t == 1:
        u = u[-1:]


if args.t is None:
    read_settings_from_config(args.config)
else:
    t = args.t
    if args.u not in ('m', 'minutes', 'h', 'hours'):
        m = 1
        u = 'seconds'
    elif args.u in ('m', 'minutes'):
        m = 60
        u = 'minutes'
    elif args.u in ('h', 'hours'):
        m = 60 * 60
        u = 'hours'
    if t == 1:
        u = u[-1:]

t = t * m

def notify(msg, t=None):
    cmd = ['notify-send', f'{msg}']
    if t:
        cmd += ['-t', t]
    subprocess.run(cmd)


print(f'Interval is {t//m} {u}. Hit Ctrl-C to pause or stop.')

stime = time.time()
while True:
    try:
        time.sleep(t)
        break
    except KeyboardInterrupt:
        print()
        # remaining time
        t = int(t - (time.time() - stime))
        stime = time.time()
        y = input('stop(q)?, or Enter to continue... ')
        if y == 'q':
            exit(0)
        print(f'{t//m} {u} remaining ...')

notify(args.m, t=args.notify_time)
