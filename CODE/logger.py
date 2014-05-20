#! /usr/bin/env python
# logger.py
# David Prager Branner and Gina Schmalzle
# 20140520

"""Instantiate logging object for Weather Study project."""

import logging

class Logger():
    def __init__(self, name, filename):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.ERROR)
        logging.basicConfig(level=logging.ERROR,
                filename=filename,
                format='''%(asctime)s - %(name)s: %(module)s.%(funcName)s: '''
                '''\n    %(levelname)s - %(message)s''')
