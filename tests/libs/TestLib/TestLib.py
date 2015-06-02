from robot.api import logger

__version__ = '0.0.1'
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'

def this_is_log_message():
  logger.console('run method')
  return 'simple log message'
