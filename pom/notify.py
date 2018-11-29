# Copyright: Anders Dalskov, 2018
# See LICENSE

# Functionality for showing a notification to the user. Currently only a method
# based on `notify-send` is available. And if that doesn't exist, the
# notification is written to stdout.

import subprocess
import shutil


if shutil.which('notify-send') is not None:

    def notify_user_done(msg):
        subprocess.run(['notify-send', msg])

else:

    def notify_user_done(msg):
        print(msg)
