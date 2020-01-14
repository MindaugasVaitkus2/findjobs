#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import pickle
import configparser

from src import indeed

class config:
    """ configuration parameters """
    def __init__(self, file='./lib/config.ini'):
        self.file = file
        # read .ini file
        conf = configparser.ConfigParser()
        conf.read(self.file)
        # default configuration
        city = conf['DEFAULT']['City']
        state = conf['DEFAULT']['State']
        field = conf['DEFAULT']['Field']
        keywords = conf['DEFAULT']['Keywords']
        self.default = [city, state, field, keywords]
        # configurations for indeed
        postings = conf['indeed.com']['Postings']
        self.indeed = int(postings)
        # configurations for monster
        self.monster = None

class results:
    """ pickle file manipulation """
    def __init__(self, file='./lib/results.pkl'):
        self.file = file
        # seperate raw data and unix formatted data
        pkl = pickle.load(open(self.file, 'rb'))
        self.data = pkl[0]
        self.unix = pkl[1]
    def export(self, data, unix):
        pickle.dump([data, unix], open(self.file, 'wb'))

class listings:
    """ search job boards """
    def __init__(self):
        # read in parameters from config file
        settings = config()
        # default parameters
        self.city = settings.default.[0]
        self.state = settings.default`[1]
        self.field = settings.default[2]
        self.keywords = settings.default[3]
        # indeed.com parameters
        self.postings = settings.indeed
        # print status update before search`
        print('\nsearching for jobs matching "{}" in {}, {}'.format(self.field.lower(), self.city.lower(), self.state.lower()))
		print('please wait for the program to finish running...')
        # search indeed.com
        indeed_jobs = indeed(self.city, self.state, self.field, self.keywords, self.postings)
        # search monster.com
        monster_jobs = []
        # aggregate resu;ts
        self.jobs= indeed_jobs + monster_jobs
        # flush waiting placeholder and print number of listings found
        menu.flush()
        print('matches found: {}\n'.format(len(self.jobs)))

class menu:
    """ boot menu window """
    def __init__(self):
        menu.clear()
        head = menu.color('findjobs ~ python {}'.format(sys.version[:5]), 'HEADER')
        info = menu.color('configuration and archive can be found in the "./lib/" directory', 'GRAY')
        print(head, '\n', info, '\n')
    @staticmethod
    def clear():
        """ clears screen if on linux / windows"""
        if self.os == 'linux':
            os.system('clear')
        elif self.os == 'windows':
            os.system('cls')
    @staticmethod
    def flush():
        """ deletes previous line if on linux """
        if self.os == 'linux':
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')
    @staticmethod
    def color(line, selection='GRAY'):
        """ prints line with color formatting"""
        colors = {
            'HEADER': '\033[95m',
            'BOLD': '\033[1m',
            'RED': '\033[91m',
            'BLUE': '\033[94m',
            'GREEN': '\033[92m',
            'GRAY': '\033[2m'}
        close = '\033[0m'
        if selection in colors.keys():
            choose = colors.get(color)
            pretty = choose + line + close
            return pretty
        else:
            return line
