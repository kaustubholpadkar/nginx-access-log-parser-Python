"""argument_parser.py - contains method for parsing the application arguments."""

# import required modules
import argparse						# Parser for command-line options, arguments and sub-commands

# parse and return the application arguments
def parse_arguments():
	"""
	Returns arguments received by the application

	Parameters
	----------
	No Parameters

	Returns
	-------
	Namespace
		arguments received by the application

	"""

	try:
		# create ArgumentParser instance
		parser = argparse.ArgumentParser(description='Parser for nginx access log file')

		# add --input argument
		parser.add_argument('--input',
							type=str,
							help='Path to nginx access log file to parse')
		# add --info argument
		parser.add_argument('--info',
							action="store_true",
							help='Information about nginx access log parser')

		# parse the arguments
		args = parser.parse_args()

		# return arguments
		return args
	except Exception as e:
		# print exception and exit application
		print(e)
		exit(0)
