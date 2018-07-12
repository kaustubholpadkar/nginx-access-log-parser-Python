"""access_log.py - NginxAccessLog : class that prototypes nginx access log."""

class NginxAccessLog:
	"""nginx access log class

	Arguments:
		timestamp: server timestamp for the request
		status_code: response status
		bytes_sent: the number of bytes sent to a client [Default: 0]

	Properties:
		timestamp: server timestamp for the request
		status_code: response status
		bytes_sent: the number of bytes sent to a client
	"""

	# Constructor : instantiates object of NginxAccessLog
	def __init__(self, timestamp, status_code, bytes_sent=0):
		# instantiate class attributes from arguments
		self.timestamp = timestamp											# timestamp
		self.status_code = status_code										# status code
		self.bytes_sent = bytes_sent										# bytes sent
