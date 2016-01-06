"""
Ad Hoc - 'WhatTimeUTC.py' created on 11/2/2015 at 3:19 PM

Simple python script to tell me the UTC time for crontab because I always forget how to do it

@author: dmcdade
"""

__author__ = 'dmcdade'

from time import strftime, localtime


def main():
    print '\n'
    current_time_utc = 'Current Time: {0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print current_time_utc
    cron_time = 'Cron Time (m h  dom mon dow): {0}'.format(strftime("%M %H %d %m %w", localtime()))
    print cron_time
    print '\n'

if __name__ == '__main__':
    main()
