#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import lxml
import requests
import urllib.requests
from bs4 import BeautifulSoup as bs

class indeed:

	def __init__(self, city, state, field, keywords=[], postings=100):
		""" aggregrate results from indeed.com """
		self.city = city
		self.state = state
		self.field = field
		self.keywords = keywords
        self.postings = postings

        # url to connect to indeed.com
        self.url ='https://www.indeed.com/jobs?q={}&l={}%2C+{}'

		# create blank list to store results
		self.jobs = []
    
    def location(self):
        """ returns state abbreviation """
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
        """ returns BeautifulSoup object for url """
        state = self.location(self.state)
        url = self.url.format(self.field.lower(), self.city.title(), state)
        page = requests.get(url)
        if page.status_code != 200:
            print('Unable to connect to {}'.format(url))
            return None
        else:
            soup = bs(page.text, 'lxml')
            return soup

	def search(self):
		""" function to search for job postings """
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

    def filter(self, raw):
        """ filters jobs based on keyword parameters """
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
