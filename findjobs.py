#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FindJobs ~ Job Search Optimization
----------------------------------------------------------------
Search job boards in seconds for listings matching your criteria.
Created by Colin Gallagher
"""

import os
import sys
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

def print_header(format=[COLORS.pink, COLORS.bold], color=True):
	"""Prints header message upon program startup."""
	header = 'FindJobs {} ~ Job Search Optimization'.format(__version__)
	if color:
		header = format[0] + format[1] + header + COLORS.reset + ' (Python {}, {})'.format(__python__, __platform__.capitalize())
	clear_screen()
	print(header)
	print('-------------------------------------------------------------------')

def print_info(job_info, counter, format=[COLORS.red, COLORS.cyan, COLORS.grey], color=True):
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
	response = input('~ Enter job title or keyword(s) related to desired position: ')
	return response

def area_input():
	"""Prompts user for city or zipcode input."""
	response = input('~ Enter name or zipcode (if USA) of city to search for jobs: ')
	return response

def read_file(filename):
	"""Reads text file if user elects to ignore old search results"""
	if os.path.isfile(filename) is False:
		return None
	else:
		file_contents = []
		with open(filename, 'r') as f:
			for line in f.readlines():
				info = line.split(', ')
				contents = {'Title':info[0], 'Company':info[1], 'Location':info[2]}
				file_contents.append(contents)
		return file_contents

def write_file(filename, results):
	"""Writes search results to text file."""
	with open(filename, 'a') as f:
		for job in results:
			line = ', '.join(job.values())
			f.write(line + '\n')

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

def remove_priors(search_results, prior_results):
	"""Checks for duplicate search results in old searches."""
	new_results = []
	for job in search_results:
		if job not in prior_results:
			new_results.append(job)
	return new_results

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

def findjobs(job_title, area_id, old_jobs=None, maxjobs=250, color=True, output=True, export=False, pages=10):
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
		print("~ Finished running job search [{} seconds]".format(duration))
		print("~ Matches found: {}".format(len(search_results)))
		print('-------------------------------------------------------------------')
	if len(search_results) > maxjobs:
		search_results = search_results[0:maxjobs]
	if old_jobs is not None:
		search_results = remove_priors(search_results, old_jobs)
	if output is True:
		counter = 1
		for job in search_results:
			print_info(job, counter, color=color)
			counter += 1
		print('-------------------------------------------------------------------')
	if export is not False:
		if output is True:
			print('~ Exporting search results to text file...')
		write_file(export, search_results)
		if output is True:
			print('Search results saved to {}'.format(export))
			print('-------------------------------------------------------------------')
	if output is True:
		print("Nothing more to do.\nTo see more jobs, run the script again.\n")
	sys.exit()

def main():
	"""Main function containing script logic."""
	print_header()
	# parse in arguments if any are given
	parser = argparse.ArgumentParser(description='Job search parameters for main module.')
	parser.add_argument('-t', '--title', type=str, dest='title', nargs='*', help='Desired job title or keyword(s) related to job type.')
	parser.add_argument('-a', '--area', type=str, dest='area', nargs='*', help='Name or zipcode (if USA) of city / town.')
	parser.add_argument('-f', '--file', type=str, dest='file', help='Name of .txt file (including path) containing prior search results.')
	parser.add_argument('-c', '--color', action='store_true', dest='color', help='Turn off color formatting for terminal output.')
	parser.add_argument('-o', '--output', action='store_true', dest='output', help='Turn off printing to terminal screen.')
	parser.add_argument('-e', '--export', dest='export', help='Name of file to export search results to.')
	parser.add_argument('-m', '--max', type=int, dest='max', help='Maximum number of job posts to return during search.')
	args = parser.parse_args()
	# check arguments for validity
	if args.title:
		job_title = '-'.join(args.title)
	else:
		job_title = title_input()
	if args.area:
		area_id = '-'.join(args.area)
	else:
		area_id = area_input()
	if args.file:
		old_jobs = read_file(args.file)
		if old_jobs is None:
			raise Exception('Unable to find text file named "{}" in PATH directories.'.format(args.file))
	else:
		old_jobs = None
	if args.max:
		maxjobs = int(args.max)
	else:
		maxjobs = 250
	options = [True, True, False]
	if args.color:
		options[0] = False
	if args.output:
		options[1] = False
	if args.export:
		options[2] = args.export
	# check for internet connection
	if check_connection() is False:
		print('Internet connection is needed in order to connect to job sites.')
		sys.exit(1)
	print('~ Please wait while the program configures the search parameters...')
	# run job search function
	findjobs(job_title, area_id, old_jobs, maxjobs=maxjobs, color=options[0], output=options[1], export=options[2])

if __name__ == '__main__':
	main()
