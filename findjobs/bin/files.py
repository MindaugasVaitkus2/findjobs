#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys



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
