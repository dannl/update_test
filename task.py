from statics import *
from os import path
import subprocess

COLUMN_COUNT = 3;

COLUMN_FROM_APK = 0;

COLUMN_TO_APK = 1;

COLUMN_TASK_TYPE = 2;

TASK_TYPE_KERNAL = 'kernal';

TASK_TYPE_10_X = 'v10';

TASK_TYPE_11_X = 'v11';

class Task(object):

	from_file = ''

	to_file = ''

	task_type = ''

	def __init__(self, sheet, row):
		if sheet.ncols != COLUMN_COUNT:
			raise task_error('bad formated of tasks, task sheet column should be %d' % COLUMN_COUNT)
		self.from_file = path.join(SRC_DIR, sheet.cell_value(row, COLUMN_FROM_APK))
		self.to_file = path.join(SRC_DIR, sheet.cell_value(row, COLUMN_TO_APK))
		self.task_type = path.join(SRC_DIR, sheet.cell_value(row, COLUMN_TASK_TYPE))

	def excute(self):
		if not path.exists(self.from_file):
			raise task_error('%s does not exists!!' % self.from_file)
		elif not path.exists(self.to_file):
			raise task_error('%s does not exists!!' % self.to_file)
		try:
			subprocess.check_output('adb logcat -c', shell=True)
			result = subprocess.check_output('adb install %s' % self.from_file, shell=True)
			result = subprocess.check_output('adb logcat -d', shell=True)
			print 'printing result'
			print result
		except subprocess.CalledProcessError as err:
			print err
			raise task_error('failed to install apk %s' % self.from_file)


	def to_string(self):
		print 'from_apk: %s to_apk: %s task_type: %s' % (self.from_file, self.to_file, self.task_type)

class task_error(Exception):

	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

