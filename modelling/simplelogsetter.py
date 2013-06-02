import sys, os, logging


class SimpleLogSetter(object):
	"""
	Simple logger starter
	"""

	DefaultLoggingFormat = '%(asctime)s %(levelname)-8s %(message)s'
	DefaultLoggingLevel = logging.DEBUG
	
	
	def __init__(self, format=None, verbosity=None):
		level = self.getLevelFromVerbosity(verbosity)
		if format is None:
			format = self.DefaultLoggingFormat
		
		self.level = level
		self.format = format

		logging.basicConfig(level=self.level, format=self.format)

		
	def startLogging(self):
		self.logCommandLine()
		

	@staticmethod
	def getLevelFromVerbosity(verbosity):
		"""
		Standard mapping of verbosity to log level
		"""
		loggingLevel = logging.ERROR
		if isinstance(verbosity, bool) and verbosity:
			loggingLevel = logging.DEBUG
		elif verbosity == 1:
			loggingLevel = logging.WARNING
		elif verbosity == 2:
			loggingLevel = logging.INFO
		elif verbosity >= 3:
			loggingLevel = logging.DEBUG
		
		return loggingLevel
	
	@classmethod
	def _getScriptName(cls):
		return os.path.splitext(os.path.basename(sys.argv[0]))[0]
		

	def logCommandLine(self, args=None):
		if args is None:
			args = sys.argv
		logging.info("Command-line: %s" % " ".join(args))
		logging.info("Command-line dash-split: %s" % " - ".join(args))
		
