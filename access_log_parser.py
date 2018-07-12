"""access_log_parser - ad-hoc query for nginx access log.

Usage:
	access_log_parser
    access_log_parser [options] (input) <var>
    access_log_parser --info

Options:
    --input <file>	path to access log file to parse.

	--info	print the help menu. [required]

Examples:
	Generate Summary for the nginx access log file
	Default location for nginx access log file is /var/log/nginx/access.log
	$ access_log_parser

	Generate Summary for the nginx access log located at /var/log/nginx/access.log
	Explicit specification for the path for nginx access log file
    $ access_log_parser --input /var/log/nginx/access.log

	Detailed Information about the access_log_parser
	$ access_log_parser --info
"""

# import required modules
from argument_parser import parse_arguments				# parser for application arguments
from nginx_access_log_parser import parse_access_log	# parser for nginx access log
from processor import summary							# processing and summary of access logs

DEFAULT_ACCESS_LOG_PATH = 'access.log'	# default path to nginx access log file

# main method - Entry point to the application
def main():
	"""
	main method - Entry point to the application
	"""

	args = parse_arguments()							# extract arguments

	if ((not args.input) and args.info):				# if Information is requested
		# print application details
		print('nginx access log parser')
		print('displays the summary of:')
		print('number of requests')
		print('average number of bytes sent')
		print('no of 2XX, 3XX, 4XX, 5XX status codes')
		print()
		print('Examples:')
		print('Generate Summary for the nginx access log file')
		print('Default location for nginx access log file is /var/log/nginx/access.log')
		print('$ access_log_parser')
		print()
		print('Generate Summary for the nginx access log located at /var/log/nginx/access.log')
		print('Explicit specification for the path for nginx access log file')
		print('$ access_log_parser --input /var/log/nginx/access.log')
		print()
		print('Detailed Information about the access_log_parser')
		print('$ access_log_parser --info')

		exit(0)
	elif ((not args.input) and (not args.info)):		# if no option is passed
		# print(DEFAULT_ACCESS_LOG_PATH)
		args.input = DEFAULT_ACCESS_LOG_PATH			# default access log path
	elif (args.input and args.info):					# if --input and --info both options are supplied
		# print appropriate message
		print('can not show information as well as summary together')
		print('can not use --info and --input options together')
		exit(0)

	access_log_path = args.input						# nginx access log file path

	try:
		access_log_file = open(access_log_path, 'r')	# read access log file
	except Exception as e:								# file can not be opened if
		print('Incorrect File or Path')					# file or path is Incorrect
		exit(0)

	access_log = access_log_file.readlines()			# convert logs to list of strings

	try:
		records = parse_access_log(access_log)			# parse and convert logs into records
	except Exception as e:								# parsing will not be successful if
		print("File structure not supported or\n"		# file structure is not supported or
				+ "Currupted Log File or\n"				# log file is Currupted
				+ "Not a Log File or")					# given file is not a log file
		exit(0)

	summary(records)									# processing logs and print summary

if __name__ == '__main__':
	main()
