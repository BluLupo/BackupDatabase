#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella
import os
import time
import subprocess
import pymysql
from config import Config

from scheduler import Scheduler

#from getpass import getpass

# set backup directory and filename
backup_dir = 'backupdb'
backup_file = os.path.join(backup_dir, '{}backup.sql'.format(time.strftime('%d%m%Y-%H%M%S')))

# connect to database
schedule = Scheduler()


# Every 4 hours
@schedule.repeat(60 * 60 * 4, True)
async def handler():
    try:
        conn = pymysql.connect(host=Config.db_host, user=Config.db_user, password=Config.db_password,
                               database=Config.db_name)
    except pymysql.Error as err:
        print(f"Error connecting to database: {err}")
        exit()

    # create backup command
    backup_cmd = f"mysqldump -u {Config.db_user} -p'{Config.db_password}' {Config.db_name} > {backup_file}"

    # execute backup command
    subprocess.call(backup_cmd, shell=True)

    # close database connection
    conn.close()

schedule.run()
