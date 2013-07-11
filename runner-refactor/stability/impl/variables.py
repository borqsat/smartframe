'''
class for represent global path.
'''
__all__ = ['WORK_SPACE']

from os.path import dirname,abspath,join,exists
PLATFORM = 'android'
WORK_SPACE = dirname(dirname(dirname(abspath(__file__))))
SERVER_CONFIG_PATH = join(WORK_SPACE, 'server.config')
DEVICE_CONFIG_PATH = join(WORK_SPACE, 'device.config')
TOKEN_CONFIG_PATH = join(WORK_SPACE, '.token')

RESULT_FILE_NAME = '.result'
FOLDER_NAME_SYMBOL = '-'


REPORT_DIR_NAME = 'report'
RESULT_DIR_NAME = 'result'
ALL_DIR_NAME = 'all'
PASS_DIR_NAME = 'pass'
FAILE_DIR_NAME = 'fail'
ERROR_DIR_NAME = 'error'
IMAGE_SUFFIX = '.png'

#TIME_STAMP_FORMAT = '%Y.%m.%d-%H.%M.%S'
TIME_STAMP_FORMAT = '%Y-%m-%d_%H:%M:%S'
