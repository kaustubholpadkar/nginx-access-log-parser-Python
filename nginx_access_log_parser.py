"""nginx_access_log_parser.py - contains methods for parsing the nginx access logs."""

# import required modules
import re													# module providing regular expression matching operations
import time													# module providing various time-related functions
from datetime import datetime								# basic date and time types
from access_log import NginxAccessLog						# class that prototypes nginx access log

# generates list of NginxAccessLog instances for nginx access log
def parse_access_log(access_log):
	"""
	generates list of NginxAccessLog instances for nginx access log

	Parameters
	----------
	access_log : list
		list of strings contains access logs

	Returns
	-------
	list
		 list of NginxAccessLog instances
	"""

	records = []											# create empty list of records

	for log in access_log:									# iterate through each access log
		record = parse_request(log)							# parse request and extract record
		records.append(record)								# append record to the records

	return records											# return records

# generates instance of NginxAccessLog corresponding to nginx access log
def parse_request(log):
	"""
	generates instance of NginxAccessLog corresponding to nginx access log

	Parameters
	----------
	log : string
		access log in form of string

	Returns
	-------
	NginxAccessLog
		 NginxAccessLog instance corresponding to log
	"""

	timestamp = parse_timestamp(log)						# parse timestamp
	status_code = parse_status_code(log)					# parse status_code
	bytes_sent = parse_bytes_sent(log)						# parse bytes_sent

	# return NginxAccessLog instance corresponding to parsed properties
	return NginxAccessLog(timestamp, status_code, bytes_sent)

# extracts the timestamp field from the one nginx access log string
def parse_timestamp(log):
	"""
	generates instance of NginxAccessLog corresponding to nginx access log

	Parameters
	----------
	log : string
		access log in form of string

	Returns
	-------
	timestamp
		 timestamp extracted from log
	"""

	pattern = r"\[(.*)\]"									# regex for timestamp
	search_object = re.search(pattern=pattern, string=log)	# create search object for timestamp
	datetime_string = search_object.group(1)				# extract timestamp
	datetime_format = '%d/%b/%Y:%H:%M:%S %z'				# datetime format
	datetime_object = datetime.strptime(datetime_string, 	# create datetime object for timestamp
									datetime_format)
	timestamp = time.mktime(datetime_object.timetuple())	# convert datetime to timestamp
	return timestamp										# return timestamp

# extracts the status_code field from the one nginx access log string
def parse_status_code(log):
	"""
	generates instance of NginxAccessLog corresponding to nginx access log

	Parameters
	----------
	log : string
		access log in form of string

	Returns
	-------
	string
		 status code extracted from log
	"""

	pattern = r'\"\s\d\d\d\s'								# regex for status_code
	line = re.findall(pattern, log)[0]						# find occurance of status_code
	pattern = r'\d\d\d'										# regex for status_code
	status_code = re.findall(pattern, line)[0]				# find occurance of status_code
	return status_code										# return status_code as string

# extracts the bytes_sent field from the one nginx access log string
def parse_bytes_sent(log):
	"""
	generates instance of NginxAccessLog corresponding to nginx access log

	Parameters
	----------
	log : string
		access log in form of string

	Returns
	-------
	int
		 bytes sent extracted from log
	"""

	pattern = r'\s\d{1,5}\s\"'								# regex for bytes_sent
	line = re.findall(pattern, log)[0]						# find occurance of bytes_sent
	pattern = r'\d{1,5}'									# regex for bytes_sent
	bytes_sent = re.findall(pattern, line)[0]				# find occurance of bytes_sent
	return int(bytes_sent)									# return bytes_sent as integer
