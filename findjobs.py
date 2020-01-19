#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import math
import lxml
import time
import datetime
import configparser
import requests
from bs4 import BeautifulSoup as bs


__version__ = '0.0.4'


class FindJobs:
	"""FindJobs search program setup & configuration"""

	opsys = os.name
	pythv = sys.version[:5]
	inifile = 'config.ini'

	#default settings for program
	settings = {
		'DEFAULT': {},
		'Indeed': {'pages':100},
		'Monster': {}}

	# checks Python version
	if pythv[0] != '3' or int(pythv[2]) < 6:
		print("You need to install Python 3.6.1 or later to run this program.")
		sys.exit()

	#Checks for configuration file
	if os.path.isfile(inifile) is True:
		config = configparser.ConfigParser()
		config.read(inifile)
		default = dict(config['DEFAULT'])
		for key, value in default.items():
			settings['DEFAULT'][key] = value
		for s in config.sections():
			if s not in settings.keys():
				settings[s] = {}
			parameters = dict(config[s])
			for key, value in parameters.items():
				settings[s][key] = value

	# formats for menu interface
	colors = {'blue':'\033[95m', 'green':'\033[92m', 'gray':'\033[2m', 'break':'\033[0m'}
	clrscr = {'linux':'clear', 'windows':'cls', 'ios':'clear'}
	fshscr = ['\x1b[1A', '\x1b[2K']
	cmdlist = {
		'search': 'Exit menu and run the job search program',
		'config': 'Information on configuring search parameters',
		'readme': 'Project description from README.md file',
		'license': 'Information regarding the project LICENSE',
		'github': 'Link to development repository on github',
		'contact': 'Contact information for the author of the project',
		'main': 'Return to main menu screen to run program',
		'quit': 'Shutdown and exit the program'}


	def run(self):
		"""Runs FindJobs program"""

		if self.opsys == 'nt':
			os.system('cls')
		else:
			os.system('clear')

		# header for welcome message
		header = self.colors.get('blue') + '\nFindJobs --> Created by Colin Gallagher' + self.colors.get('break') + self.colors.get('gray')
		header += '\nPython {} (findjobs.py, version {}) [https://github.com/colin-gall/findjobs]'.format(self.pythv, __version__)
		header += '\nLocal time {}\n'.format(time.ctime(time.time())) + self.colors.get('break')
		print(header)

		if len(dict(self.settings['DEFAULT'])) < 4:
			self.fields()

		city = self.settings['DEFAULT']['city']
		state = self.settings['DEFAULT']['state']
		title = self.settings['DEFAULT']['title']
		keywords = list(self.settings['DEFAULT']['keywords'])

		response = input("Hit any key to run searcb, or type 'cmd' for command list ~ ")
		if response == 'cmd':
			self.commands()

		bar = [self.settings['DEFAULT']['city'], self.settings['DEFAULT']['state'], self.settings['DEFAULT']['title']]
		print("\nSearching for '{}'jobs in {}, {}\nPlease wait...".format(bar[2], bar[0], bar[1]))
		start = float(time.time())

		# run main search program
		results = self.search()

		duration = round(float(time.time() - start), 2)
		print("\nProgram has finished running [{} seconds]".format(duration))
		matches = 0
		for site, jobs in results.items():
			matches += len(jobs)
		print("Matches found: {}\n".format(matches))

		if self.opsys == 'posix':
			format = [self.colors.get('green'), self.colors.get('gray'), self.colors.get('break')]
		else:
			format = ['', '', '']
		counter = 1
		for site, jobs in results.items():
			print("     Job search results for {}:\n".format(site))
			for job in jobs:
				line = "     ({}) ".format(counter)
				line += format[0] + job[0] + format[2] + ' - ' + job[1]
				if job[2] != '':
					line += format[1] + ' [{}]'.format(job[2]) + format[2]
				print(line)
				counter += 1

		response = input("\nSave search results to a new text file (type 'yes' or 'no') ~ ").lower()
		if response == 'yes' or response == 'y':
			name = input("Enter name for text file to be created ~ ")
			if name[len(name)-4:] != '.txt':
				name = name + '.txt'
			with open(name, 'w') as f:
				for site, jobs in results.items():
					source = "[{}]".format(site.upper())
					f.write(source + '\n')
					for job in jobs:
						line = job[0] + ' - ' + job[1]
						if job[2] != '':
							line += ' - ' + job[2]
						f.write(line + '\n')
			print("Results saved to text file '{}'".format(name))

		print("\nNothing more to do here. Good luck!\n")
		sys.exit()

	def install(self):
		"""Creates new configuration file"""

		conf = configparser.ConfigParser()
		for key, value in self.settings.items():
			conf[key] = value
		with open(self.inifile, 'w') as f:
			conf.write(f)

	def fields(self):
		"""Input fields for search parameters"""

		city = input("Name of city or town (will find listings in 25-50 mile radius) ~ ")
		self.settings['DEFAULT']['city'] = city.lower()
		state = input("Name or abbreviation of state (must be in USA) ~  ")
		self.settings['DEFAULT']['state'] = state.lower()
		title = input("Job title or professional field (i.e. 'finance' or 'financial analyst') ~ ")
		self.settings['DEFAULT']['title'] = title.lower()
		keywords = input("Additional keywords (seperate with commas or leave blank to ignore) ~ ")

		if keywords is not None and keywords != '':
			keywords = keywords.split(',')
			for i in range(len(keywords)):
				keywords[i] = keywords[i].strip().lower()
		else:
			keywords = []
		self.settings['DEFAULT']['keywords'] = keywords

	def commands(self, code=0):
		"""Actions based on user command"""

		print('\n')
		if self.opsys == 'posix':
			line = self.colors.get('green') + "{} --> {}" + self.colors.get('break')
		else:
			line = "{} --> {}"
		for key, value in cmdlist.items():
			print(line.format(key, value))

		cmd = input("\nPlease enter a command ~ ")

		if cmd == 'search':
			return
		elif cmd == 'config':
			self.help()
			self.commands(1)
		elif cmd == 'readme':
			if os.path.exists('README.md'):
				with open('README,md', 'r') as f:
					r = f.read()
					print(r)
			else:
				print("~ Unable to locate README.md file")
			self.commands(1)
		if cmd == 'license':
			if os.path.exists('LICENSE'):
				with open('LICENSE', 'r') as f:
					l = f.read()
					print(l)
			else:
				print("~ GNU Affero General Public License v3.0")
			self.commands(1)
		elif cmd == 'github':
			print('~ https://github.com/colin-gall/findjobs')
			self.commands(1)
		elif cmd == 'contact':
			print('~ colin gallagher (colin.gall@outlook.com)')
			self.commands(1)
		elif cmd == 'quit':
			print('~ exiting program...goodbye')
			sys.exit()
		else:
			print('~ command not recognized...please try again')
			self.commands(0)

	def search(self):
		"""Main search program"""

		city = self.settings['DEFAULT']['city']
		state = self.settings['DEFAULT']['state']
		title = self.settings['DEFAULT']['title']
		keywords = self.settings['DEFAULT']['keywords']

		sites = self.settings.keys()
		boards = JobBoards(city, state, title, keywords)

		pages = int(self.settings['Indeed']['pages'])
		jobs = boards.search(pages)

		return jobs

	def help(self):
		"""Help & information"""

		print('''
		FindJobs use customized search fields for finding the listings you need. These search fields can be set
		in the ~config.ini~ file located in the parent directory of the ~findjobs~ package. Once set, you won't
		need to enter your custom fields when running the script in the future.

		Any custom search parameters stored in the configuration file can always be changed later, or you can elect to
		create your own configuration file. Additionally, you can forgo using a configuration file altogether and instead
		will be prompted to enter your search fields upon running the script each time. If you decide to create your own
		configuration file, or copy the ~config.ini~ from the development repository, make sure the configuration file can
		be found in the current working directory when this script is run.
		''')

class JobBoards:
	"""Search job boards for recent listings"""

	def __init__(self, city, state, title, keywords=[]):
		"""Class.__init__"""

		self.city = city.capitalize()
		self.state = state.capitalize()
		self.title = title.capitalize()
		self.keywords = keywords

		for k in range(len(keywords)):
			keywords[k] = keywords[k].capitalize()

	def search(self, pages=100):
		"""Aggregate job board search results"""

		jobs = {}

		try:
			indeed = self.indeed(pages)
			jobs['Indeed'] = indeed
		except:
			print("Unable to search indeed.com for job postings")

		#try:
			#monster = self.monster()
			#jobs['Monster'] = monster
		#except:
			#print("Unable to search monster.com for job postings")

		return jobs

	def connect(self, url):
		"""Returns bs4 object"""

		page = requests.get(url)
		if page.status_code != 200:
			print('Unable to connect to {}'.format(url))
			return None
		else:
			soup = bs(page.text, 'lxml')
			return soup

	def filter(self, raw):
		"""Filters jobs based on keyword parameters"""

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

	def location(self, state):
		"""Returns state name"""

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

		states = dict(map(reversed, state_dict.items()))

		if state in states.keys():
			return state.upper()
		else:
			if state in states.values():
				for key, value in states.items():
					if value == state:
						return key
		return 'NA'

	def indeed(self, pages=100):
		"""Searches indeed.com for jobs"""

		# url for indeed.com (formatted in 'connect' function)
		title = self.title
		city = self.city.title()
		state = self.location(self.state)
		url = 'https://www.indeed.com/jobs?q={}&l={}%2C+{}'.format(title, city, state)
		soup = self.connect(url)

		postings = []
		cache = []
		# number of web pages to search
		max_jobs = max(min(pages, 100), 20)
		max_page = math.ceil(max_jobs / 20) - 1
		for page in range(max_page):
			if page > 0:
				num = page * 10
				url += '&start={}'.format(str(num))
			postings = []
			soup = self.connect(url)
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
				details[1] = details[1][0]

				# check to see if area is blank
				if details[2][:1] == '(' or details[2][:1] == '[':
					details[2] = details[2][1:len(details[2])]
				elif details[2] is None or details[2] == 'NA' or details[2] == 'N/A':
					details[2] == ''
				duplicate = str(title) + str(company[0])

				# check cache for duplicates
				if duplicate not in cache:
					postings.append(details)
					cache.append(duplicate)

			# filter postings for keywords if provided
			results = self.filter(postings)
			return results

		def monster(self):
			"""Searches monster.com for jobs"""
			pass

def main():
	"""Main function for findjobs.py"""

	program = FindJobs()
	program.run()

if __name__ == '__main__':
	main()
