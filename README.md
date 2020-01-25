# FindJobs ~ Job Search Optimization

Search job boards in seconds for listings matching your criteria.

```bash
# search for "Financial Analyst" jobs in New York, NY
$ python3 findjobs.py
```

If you found this program to be useful, consider pledging me on Patreon @ *https://www.patreon.com/colingall*

## Requirements

* python 3.6+
* pip3

## Installation

Install with pip package manager (if available):
```bash
$ pip3 install findjobs
```
On Ubuntu / Mint, install via terminal command line:
```bash
$ sudo apt update
$ sudo apt install python3-dev python3-pip python3-setuptools
$ sudo pip3 install findjobs
```
On MacOS (i.e. OS X), install via [Homebrew](https://brew.sh/):
```bash
$ brew install findjobs
```
On iOS & other operating systems, clone repository:
```bash
$ git clone https://github.com/colin-gall/findjobs
$ cd findjobs
$ python3 setup.py install
```

**NOTE:** You will most likely need to have [Pythonista](http://omz-software.com/pythonista/) downloaded on your mobile device in order to run FindJobs on iOS.

## Tutorial

Search job boards & employment websites for listings that match your desired position or field:
```bash
$ python3 findjobs.py

~ Enter job title or keywords(s) related to desired position: financial analyst
~ Enter name or zipcode (if USA) of city to search for jobs in: new york
```
Alternatively, pass search parameters to skip user prompts:
```bash
$ python3 findjobs.py -j Financial Analyst -a New York
```
You can also add additional keywords that will be used to filter search results and return a condensed list of jobs specifically tailored to your background:
```bash
$ python3 findjobs.py -j engineer -a 60018 -k civil mechanical chemical electrical
```
List of all available options and parameters for user to select when running FindJobs:
```bash
[-h, --help]                show help message and exit
[-v, --version]             show program's version number and exit
[-c, --color]               Turn off color formatting for terminal output
[-o, --output]              Turn off printing to terminal screen
[-j --job [JOB ...]]        Desired job title or keyword(s) related to job type.
[-a --area [AREA ...]]      Name or zipcode (if USA) of city / town.
[-k --keywords [KEYS ...]]  Additional keywords for filtering search results.
[-i --import IMPFILE]       Text or CSV file (including path & extension) for importing past search results.
[-e --export EXPFILE]       Text or CSV file (including path & extension for exporting new search results.
```

## Support

Created by Colin Gallagher *@colin-gall*

* Email: *colin.gall@outlook.com*
* Patreon: *https://www.patreon.com/colingall*
* Repository: *https://github.com/colin-gall/findjobs*

## License

GNU AFFERO GENERAL PUBLIC LICENSE --> find it [here](https://github.com/colin-gall/findjobs/LICENSE.md)
