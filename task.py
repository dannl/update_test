from statics import *
import os
from os import path
import subprocess

COLUMN_COUNT = 3;

COLUMN_FROM_APK = 0;

COLUMN_TO_APK = 1;

COLUMN_TASK_TYPE = 2;

TASK_TYPE_KERNAL = 'kernal';

TASK_TYPE_10_X = 'v10_v11';

TASK_TYPE_11_X = 'v11_v11';

class Task(object):

	from_file = ''

	to_file = ''

	task_type = ''

	def __init__(self, sheet, row):
		if sheet.ncols != COLUMN_COUNT:
			raise task_error('bad formated of tasks, task sheet column should be %d' % COLUMN_COUNT)
		self.from_file = path.join(SRC_DIR, sheet.cell_value(row, COLUMN_FROM_APK))
		self.to_file = path.join(SRC_DIR, sheet.cell_value(row, COLUMN_TO_APK))
		self.task_type = sheet.cell_value(row, COLUMN_TASK_TYPE)

	def excute(self):
		if not path.exists(self.from_file):
			print'%s does not exists!!' % self.from_file
			return 0
		elif not path.exists(self.to_file):
			print'%s does not exists!!' % self.to_file
			return 0

		result_file = ''
		if self.task_type == TASK_TYPE_KERNAL:
			result_file = TEST_RESULT_KERNAL
		elif self.task_type == TASK_TYPE_10_X:
			result_file = TEST_RESULT_V10_V11
		elif self.task_type == TASK_TYPE_11_X:
			result_file = TEST_RESULT_V11_V11
			
		#first of all, remove the result file.
		try:
			subprocess.check_call('adb shell \'rm sdcard/%s\'' % result_file, shell=True)
		except Exception, e:
			pass

		print '===install old version==='
		install_result = _install_dolphin(self.from_file, True)

		if install_result != 0:
			return -1

		# print '===clean logs==='
		# subprocess.check_output('adb logcat -c', shell=True)

		print '===run test case before upate==='
		result_before_update = _run_test_case(self.task_type)

		if result_before_update != 0:
			return -1

		print '===install new version==='
		install_result = _install_dolphin(self.to_file, False)

		if install_result != 0:
			return -1

		print '===run test case after update==='
		result_after_update = _run_test_case(self.task_type)

		if result_after_update != 0:
			return -1

		print '===try opt test result==='
		if not path.exists(RESULT_DIR):
			print '===create result dir==='
			os.mkdir(RESULT_DIR)
		try:
			subprocess.check_call('adb pull /sdcard/%s %s' % (result_file, RESULT_DIR), shell=True)
		except subprocess.CalledProcessError:
			print '===failed to opt adb result==='
			return -1

		return 0

	def to_string(self):
		print 'from_apk: %s to_apk: %s task_type: %s' % (self.from_file, self.to_file, self.task_type)

			
def _install_dolphin(package_path, uninstall):
	try:
		if uninstall:
			print '===uninstall dolphin==='
			try:
				result = subprocess.check_call('adb uninstall %s' % PACKAGE_NAME, shell=True)
			except Exception, e:
				pass
		print '===install dolphin==='
		result = subprocess.check_call('adb install -r %s' % package_path, shell=True)
		return result
	except subprocess.CalledProcessError as err:
		print 'failed to install apk %s' % package_path
		return err.returncode

def _run_test_case(task_type):
	case_name = ''
	if task_type == TASK_TYPE_KERNAL:
		case_name = TEST_CLASS_KERNAL
	elif task_type == TASK_TYPE_10_X:
		case_name = TEST_CLASS_V10_V11
	elif task_type == TASK_TYPE_11_X:
		case_name = TEST_CLASS_V11_V11
	try:
		command = 'adb shell am instrument -e class %s -w %s' % (TEST_CLASS_FORMAT % case_name, PACKAGE_TEST_CASE)
		print command
		subprocess.check_call(command, shell=True)
		return 0
	except subprocess.CalledProcessError as err:
		print 'failed to run class %s ' % case_name
		return err.returncode
	
class task_error(Exception):

	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

