"""
Raspberry PI - 'schedule_install.py' created on 1/5/2016 at 2:04 PM

@author: dmcdade
"""

activate_this = '/Desktop/Projects/environment/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from subprocess import Popen, PIPE

session = Popen(['pip', 'install numpy'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
session.stdin.write(sqlCommand)
session.communicate()