#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FindJobs ~ Job Search Optimization (Python 3.6+, Unix/Mac/iOS/Win)
------------------------------------------------------------------
Search job boards in seconds for listings matching your criteria.
Created by Colin Gallagher
"""

import os
import sys
import csv
import time
import datetime
import argparse
import configparser
from pathlib import Path

import requests
import configparser
from pathlib import Path
from bs4 import BeautifulSoup as bs
from uszipcode import SearchEngine, Zipcode

__module__ = 'FindJobs'
__short__ = 'Job Search Optimization'
__long__ = 'Search job boards in seconds for listings matching your criteria.'
__author__ = 'Colin Gallagher'
__repo__ = 'https://github.com/colin-gall/findjobs'
__version__ = '0.0.8'

__os__ = os.name
__platform__ = sys.platform
__path__ = str(Path.home())
__python__ = sys.version[:5]

class COLORS:
	reset='\033[0m'
	bold='\033[01m'
	underline='\033[04m'
	red='\033[91m'
	green='\033[92m'
	yellow='\033[93m'
	pink='\033[95m'
	cyan='\033[96m'
	grey='\033[90m'
	white='\033[97m'

def clear_screen():
	"""Clears terminal window screen."""
	if __platform__ == 'windows':
		os.system('cls')
	else:
		os.system('clear')

def print_header(format=[COLORS.red, COLORS.bold], color=True):
	"""Prints header message upon program startup."""
	header = 'FindJobs {} ~ Job Search Optimization'.format(__version__)
	if color:
		header = format[0] + format[1] + header + COLORS.reset + ' (Python {}, {})'.format(__python__, __platform__.capitalize())
	clear_screen()
	print(header)
	print('------------------------------------------------------------------')

def print_info(job_info, counter, format=[COLORS.green, COLORS.cyan, COLORS.grey], color=True):
	"""Prints single search result with color if formatting if desired."""
	if color:
		job_info['Title'] = format[0] + job_info['Title'] + COLORS.reset
		#job_info['Company'] = COLORS.white + job_info['Company'] + COLORS.reset
		if job_info['Location'] is not None and job_info['Location'] != '':
			job_info['Location'] = format[2] + job_info['Location'] + COLORS.reset
		counter = format[1] + str(counter) + COLORS.reset
	line = ', '.join(job_info.values())
	num = '[' + counter + ']'
	print(num + ' ' + line)

def title_input():
	"""Prompts user for job title / keyword input."""
	response = input('~ Enter job title, job type, or professional field related to desired position: ')
	return response

def area_input():
	"""Prompts user for city or zipcode input."""
	response = input('~ Enter name or zipcode (if USA) of city corresponding to desired location: ')
	return response

def keywords_input():
	"""Prompts user for keywords for filtering search results."""
	response = input('~ Enter additional keywords to search for (seperated by comma; leave blank to ignore): ')
	if response is None or response.strip() == '':
		return None
	else:
		keywords = response.split(',')
		for k in range(len(keywords)):
			keywords[k] = keywords[k].strip()
		return keywords
	return response

def error_message():
	"""Prints error message if user turns off output & doesn't call script with args."""
	print('''
	~ ~ ~
	FindJobs needs search parameters such as job title, area identifier, and optional keywords to run properly.
	Since you elected to shut off output to terminal, the program's ability to ask you to input the search parameters
	has been disabled. If you would like to shut off output and still run FindJobs, please pass the search parameters
	as system arguments when running the script from the command line (run '$ python3 findjobs.py -h' for more info).
	~ ~ ~
	''')
	sys.exit(1)

def read_file(filename):
	"""Reads text file if user elects to ignore old search results"""
	if os.path.isfile(filename) is False:
		return None
	else:
		file_contents = []
		if filename[len(filename)-4:] == '.csv':
			with open(filename, 'r', newline='') as f:
				reader = csv.reader(f, delimiter=' ')
				for row in reader:
					contents = ', '.join(row)
					file_contents.append(contents)
		else:
			with open(filename, 'r') as f:
				for line in f.readlines():
					info = line.split(', ')
					contents = {'Title':info[0], 'Company':info[1], 'Location':info[2]}
					file_contents.append(contents)
		return file_contents

def write_file(filename, results):
	"""Writes search results to text file."""
	if filename[len(filename)-4:] != '.txt' and filename[len(filename)-4:] != '.csv':
		return False
	else:
		if filename[len(filename)-4:] == '.csv':
			with open(filename, 'w', newline='') as f:
				writer = csv.writer(f, delimiter=' ')
				for job in results:
					writer.writerow([job['Title'], job['Company'], job['Location']])
		else:
			with open(filename, 'a') as f:
				for job in results:
					line = ', '.join(job.values())
					f.write(line + '\n')
	return True

def check_connection():
	"""Checks for valid internet connection."""
	url = 'https://google.com'
	page = requests.get(url)
	if page.status_code != 200:
		return False
	return True

def scrape_website(url):
	"""Returns bs4 object for url."""
	page = requests.get(url)
	if page.status_code != 200:
		print('Unable to connect to {}'.format(url))
		return None
	else:
		soup = bs(page.text, 'lxml')
		return soup

def location_info(area_id):
	"""Returns city and/or state based on city name or zip code."""
	engine = SearchEngine(simple_zipcode=True)
	try:
		location = engine.by_zipcode(area_id)
		city = location.city
		state = location.state
	except ValueError:
		city = area_id.title()
		location = engine.by_city(city, sort_by=Zipcode.population)
		state = location[0].state_abbr
	finally:
		if city is None or state is None:
			city = area_id.title()
			location = engine.by_city(city, sort_by=Zipcode.population)
			state = location[0].state_abbr
	return city, state

def cleanup_contents(contents):
	"""Cleans up formatting of job post information."""
	if contents is None or len(contents) == 0:
		contents = ''
	elif (contents[:1]+contents[len(contents)-1:]) == '()' or (contents[:1]+contents[len(contents)-1:]) == '[]':
		contents = contents[1:len(contents)-1]
	return contents

def remove_priors(search_results, prior_results, output):
	"""Checks for duplicate search results in old searches."""
	new_results = []
	for job in search_results:
		if job not in prior_results:
			new_results.append(job)
	if len(new_results) > 0:
		if output is True:
			removals = int(len(search_results) - len(new_results))
			print('~ Removed {} duplicate listings from search results.'.format(removals))
		return new_results
	else:
		return search_results

def remove_duplicates(job_list_1, job_list_2):
	"""Removes duplicate listings across job board sites."""
	combined_results = []
	for job in job_list_1:
		if job not in combined_results:
			combined_results.append(job)
	for job in job_list_2:
		if job not in combined_results:
			combined_results.append(job)
	return combined_results

def filter_keywords(search_results, keywords, output=True):
	"""Removes listings from results not containing any keywords."""
	if keywords is None or len(keywords) == 0:
		return search_results
	else:
		filtered_results = []
		for job in search_results:
			for key in keywords:
				if key in job['Title'] or key in job['Company'] or key in job['Location']:
					filtered_results.append(job)
					break
				elif key.capitalize() in job['Title'] or key.capitalize() in job['Company'] or key.capitalize() in job['Location']:
					filtered_results.append(job)
					break
		if len(filtered_results) == 0:
			if output is True:
				print('~ No listings containing keywords were found. Returning full list.')
			return search_results
		else:
			if output is True:
				print('~ Search results contained {} listings matching one or more keywords.'.format(len(filtered_results)))
			return filtered_results

def search_indeed(job_title, city, state, pages=10):
	"""Search indeed.com for jobs matching criteria."""
	indeed_url = 'https://www.indeed.com/jobs?q={}&l={}%2C+{}'
	job_title = job_title.replace('-', '+')
	city = city.replace('-', '+')
	# url for indeed.com (formatted in 'connect' function)
	start_url = indeed_url.format(job_title, city, state)
	page_url = start_url + '&start={}'
	#blank lists to hold job posts
	jobs_found = []
	# run search query
	for page in range(pages):
		if page == 0:
			soup = scrape_website(start_url)
		else:
			page_num = int(page*10)
			soup = scrape_website(page_url.format(page_num))
		listings = soup.find_all('div', {'class':'title'})
		for position in listings:
			elem = position.find('a')
			try:
				title = elem.get_text().strip()
				company = position.find_next_sibling('div', {'class':'sjcl'}).find_all('div')[0].get_text().strip().split('\n')[0]
			except:
				continue
			try:
				location = position.find_next_sibling('div', {'class':'sjcl'}).find_all('div')[1].nextSibling.nextSibling.get_text().strip().split('\n')[0]
			except:
				location = ''
			location = cleanup_contents(location)
			job_post_info = {
				'Title':title,
				'Company':company,
				'Location':location}
			jobs_found.append(job_post_info)
	return jobs_found

def search_monster(job_title, city, state, pages=10):
	"""Search monster.com for jobs matching criteria."""
	monster_url = 'https://www.monster.com/jobs/search/?q={}&where={}__2C-{}&intcid=skr_navigation_nhpso_searchMain'
	# url for monster.com (formatted in 'connect' function)
	start_url = monster_url.format(job_title, city, state)
	page_url = start_url + '&stpage=1&page={}'
	#blank lists to hold job posts
	jobs_found = []
	# run search query
	for page in range(pages):
		if page == 0:
			soup = scrape_website(start_url)
		else:
			soup = scrape_website(page_url.format(page+1))
		div = soup.find('div', id='SearchResults')
		sections = div.find_all('section', {'class':'card-content'})
		for post in sections:
			try:
				title = post.find('h2', {'class':'title'}).get_text().strip()
				company = post.find('div', {'class':'company'}).get_text().strip()
			except:
				continue
			try:
				location = post.find('div', {'class':'location'}).get_text().strip()
			except:
				location = ''
			location = cleanup_contents(location)
			job_post_info = {
				'Title':title,
				'Company':company,
				'Location':location}
			jobs_found.append(job_post_info)
	return jobs_found

def findjobs(job_title, area_id, keywords=None, import_file=None, export_file=None, color=True, output=True, pages=10):
	"""Search job boards for recent listings."""
	start_time = float(time.time())
	job_title = job_title.capitalize()
	city, state = location_info(area_id)
	state = state.upper()
	if output is True:
		print("~ Running search query for jobs matching '{}' in {}, {}".format(job_title, city, state))
	try:
		indeed_jobs = search_indeed(job_title, city, state)
	except:
		raise Exception('~ Unable to search indeed.com.')
		indeed_jobs = []
	try:
		monster_jobs = search_monster(job_title, city, state)
	except:
		raise Exception('~ Unable to search monster.com')
	start = time.time()
	search_results = remove_duplicates(indeed_jobs, monster_jobs)
	end_time = float(time.time())
	duration = round(end_time- start_time, 2)
	if search_results is None or len(search_results) == 0:
		raise Exception('~ Could not find any job posts matching your critera (maybe something went wrong?)')
		sys.exit()
	if output is True:
		print("~ Finished running job search ({} matches found - {} seconds)".format(len(search_results), duration))
	if keywords is not None and len(keywords) > 0:
		job_listings = filter_keywords(search_results, keywords, output)
	else:
		job_listings = search_results
	if import_file is not None:
		if os.path.isfile(import_file) is False:
			raise Exception('~ Unable to find text file named "{}" in PATH directories.'.format(import_file))
		imported_jobs = read_file(import_file)
		job_listings = remove_priors(job_listings, imported_jobs, output)
	print('------------------------------------------------------------------')
	if output is True:
		counter = 1
		for job in job_listings:
			print_info(job, counter, color=color)
			counter += 1
		print('------------------------------------------------------------------')
	if export_file is not None:
		if output is True:
			print('~ Exporting search results to text file...')
		check = write_file(export_file, job_listings)
		if check is True:
			if output is True:
				print('~ Search results saved to {}'.format(export_file))
		else:
			print('~ Unable to export search results to "{}".'.format(export_file))
			print('~ Make sure filepath & extension for filetype are both correct next time script is run.')
		print('------------------------------------------------------------------')
	if output is True:
		print("~ Nothing more to do.\n~ To search for more jobs, run the script again.\n")
	sys.exit()

def main():
	"""Main function containing script logic."""
	print_header()
	# check for internet connection
	if check_connection() is False:
		print('~ Internet connection is needed in order to connect to job sites.')
		sys.exit(1)
	# parse in arguments if any are given
	parser = argparse.ArgumentParser(description=__module__+' '+__version__+' ~ '+__short__)
	parser.add_argument('-v', '--version', action='version', version='findjobs {}'.format(__version__))
	parser.add_argument('-c', '--color', action='store_true', dest='color', help='Turn off color formatting for terminal output')
	parser.add_argument('-o', '--output', action='store_true', dest='output', help='Turn off printing to terminal screen')
	parser.add_argument('-j', '--job', type=str, dest='job', nargs='+', metavar='JOB', help='Desired job title or keyword(s) related to job type')
	parser.add_argument('-a', '--area', type=str, dest='area', nargs='+', metavar='AREA', help='Name or zipcode (if USA) of city / town.')
	parser.add_argument('-k', '--keywords', type=str, dest='keywords', default=None, nargs='+', metavar='KEYS', help='Additional keywords for filtering search results')
	parser.add_argument('-i', '--import', type=str, dest='impfile', default=None, help='Text or CSV file (including path & extension) for importing past search results')
	parser.add_argument('-e', '--export', type=str, dest='expfile', default=None, help='Text or CSV file (including path & extension for exporting new search results')
	args = parser.parse_args()
	# check arguments for validity
	if args.job:
		job_title = '-'.join(args.job)
	else:
		if output is False:
			error_message()
		else:
			job_title = title_input()
	if args.area:
		area_id = '-'.join(args.area)
	else:
		if output is False:
			error_message()
		else:
			area_id = area_input()
	if args.keywords:
		keywords = args.keywords
	else:
		if output is False:
			error_message()
		else:
			keywords = keywords_input()
	if args.impfile:
		import_file = args.impfile
	else:
		import_file = None
	if args.expfile:
		export_file = args.expfile
	else:
		export_file = None
	if args.color:
		color = False
	else:
		color = True
	if args.output:
		output = False
	else:
		output = True
	print('~ Please wait while the program configures the search parameters...')
	# run job search function
	findjobs(job_title, area_id, keywords, import_file, export_file, color, output)

if __name__ == '__main__':
	main()
