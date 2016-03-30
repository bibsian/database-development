#!/usr/bin/env python
import logging
import datetime as dt

# This class is used to extent the fileHandler for logging data
# (logging.config) and allow me to title log files with dates.

# Inheriting frm FileHandler class
class MyFileHandler(logging.FileHandler):
    def __init__(self, fileName):
        date = (str(dt.datetime.now()).split()[0]).replace("-", "_")        
        super().__init__('{}_{}.log'.format(fileName, date))
