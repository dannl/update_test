from statics import *
import os
from os import path
import subprocess
import shutil
import time
import re

COLUMN_COUNT = 4;

COLUMN_FROM_APK = 0;

COLUMN_FROM_JETPACK = 1

COLUMN_TO_APK = 2;

COLUMN_TASK_TYPE = 3;

TASK_TYPE_SHELL_ONEPKG = 'shell_onepkg';

TASK_TYPE_SHELL_JETPACK_ONEPKG = 'shell_jetpack_onepkg';

TASK_TYPE_ONEPKG_ONEPKG = 'onepkg_onepkg';

TASK_TYPE_10_X = 'v10_v11';

TASK_TYPE_11_X = 'v11_v11';

class Task(object):

	from_file_name = ''

	from_file = ''

	from_jetpack_string = ''

	from_jetpack = ''

	to_file = ''

	to_file_name = ''

	task_type = ''

	def __init__(self, sheet, row):
		if sheet.ncols != COLUMN_COUNT:
			raise task_error('bad formated of tasks, task sheet column should be %d' % COLUMN_COUNT)
		self.from_file_name = sheet.cell_value(row, COLUMN_FROM_APK)
		self.from_file = path.join(SRC_DIR, self.from_file_name)
		from_jetpack_string = sheet.cell_value(row, COLUMN_FROM_JETPACK)
		if from_jetpack_string:
			self.from_jetpack = path.join(SRC_DIR, from_jetpack_string)
		self.from_jetpack_string = from_jetpack_string
		self.to_file_name = sheet.cell_value(row, COLUMN_TO_APK)
		self.to_file = path.join(SRC_DIR, self.to_file_name)
		self.task_type = sheet.cell_value(row, COLUMN_TASK_TYPE)

	def excute(self):
		if not path.exists(self.from_file):
			print'%s does not exists!!' % self.from_file
			return 0
		elif not path.exists(self.to_file):
			print'%s does not exists!!' % self.to_file
			return 0

		result_file = ''
		if self.task_type == TASK_TYPE_SHELL_ONEPKG:
			result_file = TEST_RESULT_SHELL_ONEPKG
		elif self.task_type == TASK_TYPE_SHELL_JETPACK_ONEPKG:
			result_file = TEST_RESULT_SHELL_JETPACK_ONEPKG
		elif self.task_type == TASK_TYPE_ONEPKG_ONEPKG:
			result_file = TEST_RESULT_ONEPKG_ONEPKG
		elif self.task_type == TASK_TYPE_10_X:
			result_file = TEST_RESULT_V10_V11
		elif self.task_type == TASK_TYPE_11_X:
			result_file = TEST_RESULT_V11_V11
			
		#first of all, remove the result file.
		try:
			subprocess.check_call('adb shell \'rm sdcard/%s\'' % result_file, shell=True)
			subprocess.check_call('adb shell \'rm sdcard/jetpack_update\'', shell=True)
		except Exception:
			pass

		_uninstall_jetpack()

		update_loop_result = "continue"

		while update_loop_result == 'continue':
			
			print '===install old version==='
			install_result = _install_dolphin(self.from_file, True)


			if install_result != 0:
				return -1

			if self.from_jetpack:
				install_result = _install_dolphin(self.from_jetpack, False)

			if install_result != 0:
				return -1

			#sleep for 5 secs.
			time.sleep(5)

			print '===run test case before upate==='
			result_before_update = _run_test_case(self.task_type)

			time.sleep(3)

			if result_before_update == 'failed':
				return -1
			elif result_before_update == 'uninstall_jetpack':
				_uninstall_jetpack()

			#sleep for 10 secs to ensure the dolphin is already closed.
			time.sleep(10)

			print '===install new version==='
			install_result = _install_dolphin(self.to_file, False)

			if install_result != 0:
				return -1

			time.sleep(5)

			print '===run test case after update==='
			update_loop_result = _run_test_case(self.task_type)
			print '======================loop control====================='
			print update_loop_result
			time.sleep(3)
			
			if update_loop_result == 'failed':
				return -1



		print '===try opt test result==='
		if not path.exists(RESULT_DIR):
			print '===create result dir==='
			os.mkdir(RESULT_DIR)
		try:
			result_dir = path.join(RESULT_DIR, self.to_string())
			if path.exists(result_dir):
				shutil.rmtree(result_dir)
			os.mkdir(result_dir)
			subprocess.check_call('adb pull /sdcard/%s %s' % (result_file, result_dir), shell=True)
		except subprocess.CalledProcessError:
			print '===failed to opt adb result==='
			return -1

		return 0

	def to_string(self):
		return "%s_%s_%s_%s" % (self.from_file_name, self.from_jetpack_string, self.to_file_name, self.task_type)

			
def _install_dolphin(package_path, uninstall):
	try:
		if uninstall:
			print '===uninstall dolphin==='
			try:
				result = subprocess.check_call('adb uninstall %s' % PACKAGE_NAME, shell=True)
			except Exception:
				pass
		print '===install dolphin==='
		result = subprocess.check_call('adb install -r %s' % package_path, shell=True)
		return result
	except subprocess.CalledProcessError as err:
		print 'failed to install apk %s' % package_path
		return err.returncode

def _run_test_case(task_type):


	logout = 'restart'
	while logout == 'restart':
		print '===clean logs==='
		subprocess.check_output('adb logcat -c', shell=True)
		case_name = ''
		if task_type == TASK_TYPE_SHELL_ONEPKG:
			case_name = TEST_CLASS_SHELL_ONEPKG
		elif task_type == TASK_TYPE_SHELL_JETPACK_ONEPKG:
			case_name = TEST_CLASS_SHELL_JETPACK_ONEPKG
		elif task_type == TASK_TYPE_ONEPKG_ONEPKG:
			case_name = TEST_CLASS_ONEPKG_ONEPKG
		elif task_type == TASK_TYPE_10_X:
			case_name = TEST_CLASS_V10_V11
		elif task_type == TASK_TYPE_11_X:
			case_name = TEST_CLASS_V11_V11
		try:
			command = 'adb shell am instrument -e class %s -w %s' % (TEST_CLASS_FORMAT % case_name, PACKAGE_TEST_CASE)
			subprocess.check_call(command, shell=True)
		except subprocess.CalledProcessError:
			print 'failed to run class %s ' % case_name
			return 'failed'

		log = subprocess.check_output('adb logcat -d', shell=True)
		logout = _check_output(log)
	return logout

def _check_output(log):
	m = TEST_UNINSTALL_JETPACK_REG.search(log)
	if not m:
		m = TEST_CASE_OUTPUT_REG.search(log)
		if not m:
			return 'failed'
	return m.group(1)

def _uninstall_jetpack():
	try:
		subprocess.check_call('adb uninstall com.dolphin.browser.engine', shell=True)
	except Exception:
		pass

	
class task_error(Exception):

	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

