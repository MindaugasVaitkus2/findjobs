#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import pickle
import configparser
import math
import lxml
import requests
from bs4 import BeautifulSoup as bs

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

class indeed:
	""" search indeed.com for jobs """
	def __init__(self, city, state, field, keywords=[], postings=100):
		self.city = city
		self.state = state
		self.field = field
		self.keywords = keywords
        self.postings = postings
        # url to connect to indeed.com
        self.url ='https://www.indeed.com/jobs?q={}&l={}%2C+{}'
		# create blank list to store results
		self.jobs = []
		# run search
		self.search()
    def location(self):
        # returns state abbreviation
        state_dict = {
            'Alabama': 'AL',
            'Alaska': 'AK',
            'Arizona': 'AZ',
            'Arkansas': 'AR',
            'California': 'CA',
            'Colorado': 'CO',
            'Connecticut': 'CT',
            'Delaware': 'DE',
            'District of Columbia': 'DC',
            'Florida': 'FL',
            'Georgia': 'GA',
            'Hawaii': 'HI',
            'Idaho': 'ID',
            'Illinois': 'IL',
            'Indiana': 'IN',
            'Iowa': 'IA',
            'Kansas': 'KS',
            'Kentucky': 'KY',
            'Louisiana': 'LA',
            'Maine': 'ME',
            'Maryland': 'MD',
            'Massachusetts': 'MA',
            'Michigan': 'MI',
            'Minnesota': 'MN',
            'Mississippi': 'MS',
            'Missouri': 'MO',
            'Montana': 'MT',
            'Nebraska': 'NE',
            'Nevada': 'NV',
            'New Hampshire': 'NH',
            'New Jersey': 'NJ',
            'New Mexico': 'NM',
            'New York': 'NY',
            'North Carolina': 'NC',
            'North Dakota': 'ND',
            'Northern Mariana Islands':'MP',
            'Ohio': 'OH',
            'Oklahoma': 'OK',
            'Oregon': 'OR',
            'Palau': 'PW',
            'Pennsylvania': 'PA',
            'Puerto Rico': 'PR',
            'Rhode Island': 'RI',
            'South Carolina': 'SC',
            'South Dakota': 'SD',
            'Tennessee': 'TN',
            'Texas': 'TX',
            'Utah': 'UT',
            'Vermont': 'VT',
            'Virgin Islands': 'VI',
            'Virginia': 'VA',
            'Washington': 'WA',
            'West Virginia': 'WV',
            'Wisconsin': 'WI',
            'Wyoming': 'WY',
        }
        states = dict(map(reversed, states_dict.items()))
	    if self.state in states.keys():
		    return self.state.upper()
	    else:
		    if self.state in states.values():
			    for key, value in states.items():
				    if value == self.state:
					    return key
	    return 'NA'
    def connect(self):
        # returns BeautifulSoup object for url
        state = self.location(self.state)
        url = self.url.format(self.field.lower(), self.city.title(), state)
        page = requests.get(url)
        if page.status_code != 200:
            print('Unable to connect to {}'.format(url))
            return None
        else:
            soup = bs(page.text, 'lxml')
            return soup
	def filter(self, raw):
        # filters jobs based on keyword parameters
        if len(self.keywords) == 0:
            return raw
        matches = []
        for job in raw:
            job_title = job[0].lower()
            for key in self.keywords:
                check = (key in job_title)
                if check is True:
                    matches.append(job)
                    break
        return matches
	def search(self):
		# function to search for job postings
		postings = []
		cache = []
        # number of web pages to search
		max_jobs = max(min(self.postings, 100), 20)
		max_page = math.ceil(max_jobs / 20) - 1
		for page in range(max_page):
			if page > 0:
				num = page * 10
				url += '&start={}'.format(str(num))
			postings = []
			soup = self.connect()
			listings = soup.find_all('div', {'class':'title'})
			for position in listings:
				details = []
				elem = position.find('a')
				if elem is not None:
					title = elem.get_text().strip()
					details.append(title)
				else:
					details.append('')
				info = position.find_next_sibling('div', {'class':'sjcl'})
				div = info.find_all('div')
				if len(div) > 0:
					company = div[0].get_text().strip().split('\n')
					area = div[len(div)-1].get_text().strip()
					details.extend([company, area])
				else:
					details.extend()
				details = [title, company[0], area]
				duplicate = str(title) + str(company[0])
                # check cache for duplicates
				if duplicate not in cache:
					postings.append(details)
					cache.append(duplicate)
            # filter postings for keywords if provided
			results = self.filter(postings)
            # check for duplicates if search run multiple times
            for job in results:
                if job not in self.jobs:
                    self.jobs.append(job)
            return results

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
