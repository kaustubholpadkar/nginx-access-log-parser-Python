"""processor.py - contains global variables as well as methods for processing records and displaying summary."""

# import required libraries
import curses																# terminal-independent screen-painting and keyboard-handling facility for text-based terminals
import time																	# module providing various time-related functions
import threading															# multithreading library
from terminaltables import AsciiTable										# generate simple tables in terminals from a nested list of strings

from nginx_access_log_parser import parse_request

##
## global variables
##

# progress details
initial_timestamp = 0
requests_processed = 0														# no of requests processed
total_time = 0																# total_time
requests_per_second = 0														# requests per second

# table details
count = 0																	# count for no of requests
total_bytes_sent = 0
avg_bytes_sent = 0															# average bytes sent
xx2 = 0																		# no of 2XX status code
xx3 = 0																		# no of 3XX status code
xx4 = 0																		# no of 4XX status code
xx5 = 0																		# no of 5XX status code

stdscr = None																# screen variable for curses
parsed = False																# flag to check if requests are parsed
threadLock = None															# thread lock variable

def set_requests_per_second():
	global requests_per_second, requests_processed, total_time
	set_total_time()
	requests_per_second = requests_processed / total_time

def set_threadlock():
	global threadLock														# threadLock global variable\
	threadLock = threading.Lock()

# processes the records and generate summary
def summary(records):
	"""
	processes the records

	Parameters
	----------
	records : list
		list of NginxAccessLog instances

	Returns
	-------
	Returns Nothing

	"""

	global threadLock														# threadLock global variable\
	threadLock = threading.Lock()											# create thread lock

	processor(records)														# processes the records

	show_details()															# prints the summary

# processes the records
def processor(records):
	"""
	processes the records

	Parameters
	----------
	records : list
		list of NginxAccessLog instances

	Returns
	-------
	Returns Nothing

	"""

	global requests_processed, total_time, requests_per_second				# global variables
	global count, xx2, xx3, xx4, xx5, avg_bytes_sent, parsed				# global variables

	initial_timestamp = time.time()
	total_bytes_sent = 0													# initialize total_bytes_sent with 0

	for record in records:													# iterate through each record
		# time.sleep(0.3)														## to be removed after testing
		code = record.status_code[0]										# extract status_code

		if code == '2':														# 2XX status_code
			xx2 += 1														# increment xx2
		elif code == '3':													# 3XX status_code
			xx3 += 1														# increment xx3
		elif code == '4':													# 4XX status_code
			xx4 += 1														# increment xx4
		elif code == '5':													# 5XX status_code
			xx5 += 1														# increment xx5

		total_bytes_sent += record.bytes_sent								# increase total_bytes_sent by bytes_sent
		count += 1															# increment the count

		current_timestamp = time.time()										# get current_timestamp
		total_time = current_timestamp - initial_timestamp					# calculate total_time
		requests_processed += 1												# increment requests_processed
		requests_per_second = requests_processed / total_time				# calculate requests_per_second

	avg_bytes_sent = total_bytes_sent / count								# calculating avg_bytes_sent
	parsed = True															# parsing completed

# prints the summary and detailed table for the nginx logs after parsing is completed
def show_details():
	"""
	prints the summary and detailed table for the nginx logs after parsing is completed

	Parameters
	----------
	No Parameters

	Returns
	-------
	Returns Nothing

	"""

	# global count, xx2, xx3, xx4, xx5, avg_bytes_sent, parsed				# global variables

	print("Summary :")														# Display Summary
	print("Number of requests processed : {0}".format(requests_processed))	# No of requests processed
	print("Total time: {0} sec".format(total_time))							# Total Time
	print("Request/sec: {0} req/sec".format(requests_per_second))			# Request/sec

	table_data = [															# generate table_data
		["count", "avg_bytes_sent", "2xx", "3xx", "4xx", "5xx"],			# define headers for specified field
		[count, avg_bytes_sent, xx2, xx3, xx4, xx5]							# specify the values for each field
	]

	table = AsciiTable(table_data)											# generate AsciiTable from table_data

	print()																	# print empty line
	print(table.table)														# print the table

def new_progress(lines):

	global threadLock
	global count, xx2, xx3, xx4, xx5, total_bytes_sent, requests_processed				# global variables

	threadLock.acquire()

	for line in lines:
		record = parse_request(line)

		code = record.status_code[0]										# extract status_code

		if code == '2':														# 2XX status_code
			xx2 += 1														# increment xx2
		elif code == '3':													# 3XX status_code
			xx3 += 1														# increment xx3
		elif code == '4':													# 4XX status_code
			xx4 += 1														# increment xx4
		elif code == '5':													# 5XX status_code
			xx5 += 1														# increment xx5

		total_bytes_sent += record.bytes_sent								# increase total_bytes_sent by bytes_sent
		count += 1															# increment the count

		requests_processed += 1												# increment requests_processed

	threadLock.release()

def set_avg_bytes_sent():
	global total_bytes_sent, avg_bytes_sent, requests_processed
	avg_bytes_sent = total_bytes_sent / requests_processed

def set_initial_timestamp():
	global initial_timestamp
	initial_timestamp = time.time()

def set_total_time():
	global total_time, initial_timestamp
	total_time = time.time() - initial_timestamp
