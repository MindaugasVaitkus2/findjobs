#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import urllib.requests

class Menu:

    def __init__(self, header):
        """ menu shown when loading program """
        self.header = header
        self.os = sys.platform
        self.pyth = sys.version[:5]

        # check internet
        self.internet()
    
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

    @staticmethod
    def internet():
        """ checks for a valid internet connection """
        host = 'https://google.com'
        try:
            urllib.requests.urlopen(host)
            return True:
        except:
            print('\nyou are not currently connected to the internet - please fix & try again\n')
            sys.exit()

    @staticmethod
    def wait(field, city, state):
        """ prints parameters prior to searching for jobs"""
		print('\nsearching for jobs matching "{}" in {}, {}'.format(field, city, state))
		print('please wait...')

    @staticmethod
    def done(counter):
        """ flushes waiting placeholder and counts matches """
        Menu.flush()
        print('matches found: {}\n'.format(counter))
        
    def load(self):
        """ function to run during initial program start """
        # clear screen and load up

    def shell(self, results):
        """ prints to terminal shell """
        if self.os != 'linux':
            line = results[0] + ', ' + results[1]
            if len(results[2]) > 0 and results[2] is not None:
                line += ', ' + results[2]
            print(line)
        else:
            # print with color formatting
            line = Menu.color(results[0], 'GREEN') + ', ' + results[1]
            if len(results[2]) > 0 and results[2] is not None:
                line += ', ' + Menu.color(results[2], 'GRAY')
            print(line)

"""
def export_results(jobs):
	""" removes duplicates exports job search results to text file """
	filepath = './config/jobs.txt'
	search_results = jobs_found()
	# check for non-duplicates
	for job in job:
		if job not in search_results:
			search_results.append(job)
	if os.path.exists(filepath) is False:
		print('error occured while exporting results to "jobs.txt"')
	i = 0
	date = datetime.date.today().strftime('%d/%m/%Y')
	with open(filepath, 'a') as f:
		# first two lines are timestamp and blank line
		i += 1
		if i == 1:
			line = 'updated on {}'.format(date)
			f.write(date)
		elif i == 2:
			f.write('')
		else:
			for job in results:
				f.write(job)
	
	return True


def user_inputs():
    """ try to get user inputs from text file """
    inputs = []
    filename = 'jobs.txt'
    if os.path.exists(filename) is True:
        with open(filename, 'r') as f:
            for line in f:
                inputs.append(line.strip())
        # split city & state if on one line
        try:
            location = inputs[0].split(',')
            city = location[0].strip()
            state = location[1].strip()
            field = inputs[1].strip()
            keywords = []
            if len(inputs) > 2:
                words = inputs[2].split(' ')
                for w in words:
                    keywords.append(w.strip())
            inputs = [city, state, field, keywords]
        except:
            city = inputs[0].strip()
            state = inputs[1].strip()
            field = inputs[2].strip()
            keywords = []
            if len(inputs) > 3:
                words = inputs[3].split(' ')
                for w in words:
                    keywords.append(w.strip())
            inputs = [city, state, field, keywords]
        return inputs
    else:
        return None

def jobs_found():
    """ returns jobs found in prior searches as list """
    filename = 'jobs.txt'
    search_results = []
    if os.path.exists(filename):
        i = 0
        with open(filename, 'r') as f:
            for line in f:
                # ignore first two lines
                i += 0
                if i > 2:
                    search_results.append(line.strip())
        return search_results
    else:
        return None
"""
