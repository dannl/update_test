from statics import *
from xlutils.copy import copy
from xlrd import open_workbook
from xlwt import Workbook
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

TASK_TYPE_NORMAL = 'normal';

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

		result_file = 'running_result.xls'

		#first of all, remove the result file.
		try:
			#remove result file.
			subprocess.check_call('adb shell rm sdcard/%s' % result_file, shell=True)
			#remove temp preference.
			subprocess.check_call('adb shell rm sdcard/temp_preference', shell=True)
			#remove apk pair 
			subprocess.check_call('adb shell rm sdcard/temp_input', shell=True)
		except Exception:
			pass

		#write in the from apk name and to apk name.
		try:
			from_file_name = self.from_file_name.replace('.apk','')
			to_file_name = self.to_file_name.replace('.apk','')
			temp_file = open('temp_input', 'w')
			temp_file.write('%s+%s' % (from_file_name, to_file_name))
			temp_file.close()
			subprocess.check_call('adb push temp_input /sdcard/temp_input', shell=True)
			os.remove('temp_input')
		except Exception:
			write_total_case_result(self, "Failed on pushing file to sdcard!")
			return NEXT_TASK

		_uninstall_jetpack()

		update_loop_result = CONTROL_RESTART

		while update_loop_result == CONTROL_RESTART:
			
			print '===install old version==='
			install_result = _install_dolphin(self.from_file, True)


			if install_result != 0:
				return RESTART_TASK

			if self.from_jetpack:
				install_result = _install_dolphin(self.from_jetpack, False)

			if install_result != 0:
				return RESTART_TASK

			#sleep for 5 secs.
			time.sleep(10)

			print '===run test case before upate==='
			result_before_update = _run_test_case(self.from_file_name, self.task_type)

			time.sleep(10)

			if result_before_update == CONTROL_FAILED:
				#write the result to the total result.
				write_total_case_result(self, 'Failed on running case before update')
				return NEXT_TASK
			elif result_before_update == CONTROL_CLEAN_RESTART:
				return RESTART_TASK
			elif result_before_update == CONTROL_UNINSTALL_JETPACK:
				_uninstall_jetpack()
			# elif result_before_update == INSTRUMENTATION_ERR_SUBPROCESS:
			# 	return 

			#sleep for 10 secs to ensure the dolphin is already closed.
			time.sleep(10)

			print '===install new version==='
			install_result = _install_dolphin(self.to_file, False)

			if install_result != 0:
				return RESTART_TASK

			time.sleep(10)

			print '===run test case after update==='
			update_loop_result = _run_test_case(self.to_file_name, self.task_type)
			print '======================loop control====================='
			print update_loop_result
			time.sleep(10)
			
			if update_loop_result == CONTROL_FAILED:
				write_total_case_result(self, 'Failed on running case after update')
				return NEXT_TASK
			elif update_loop_result == CONTROL_CLEAN_RESTART:
				return RESTART_TASK
			elif update_loop_result == CONTROL_RESTART:
				pass



		print '===try opt test result==='
		if not path.exists(RESULT_DIR):
			print '===create result dir==='
			os.mkdir(RESULT_DIR)
		try:
			result_dir = path.join(RESULT_DIR, self.to_string())
			if path.exists(result_dir):
				shutil.rmtree(result_dir)
			os.mkdir(result_dir)
			pc_result_file = path.join(result_dir, self.to_string() + '.xls')
			subprocess.check_call('adb pull /sdcard/%s %s' % (result_file, pc_result_file), shell=True)
			validate_result(self, pc_result_file)
		except subprocess.CalledProcessError:
			print '===failed to opt adb result==='
			write_total_case_result(self, 'Failed to pull file from phone')
			return RESTART_TASK

		return NEXT_TASK

	def to_string(self):
		return "%s_%s_%s_%s" % (self.from_file_name, self.from_jetpack_string, self.to_file_name, self.task_type)

			
def _install_dolphin(package_path, uninstall):
	try:
		if uninstall:
			try:
				ps = subprocess.check_output('adb shell ps', shell=True)
				result = re.search('.+/watch_server', ps)
				if result:
					sub = re.findall('\ ([0-9]+)\ ', result.group(0))
					if sub and len(sub) > 0:
						subprocess.check_call('adb shell kill ' + sub[0], shell=True)
			except Exception:
				pass
			print '===uninstall dolphin==='
			try:
				result = subprocess.check_call('adb uninstall "%s"' % PACKAGE_NAME, shell=True)
			except Exception:
				pass
		print '===install dolphin==='
		result = subprocess.check_call('adb install -r "%s"' % package_path, shell=True)
		return result
	except subprocess.CalledProcessError as err:
		print 'failed to install apk %s' % package_path
		return err.returncode

def _run_test_case(apk_file, task_type):


	logout = CONTROL_CONTINUE
	retry_count = 0
	while logout == CONTROL_CONTINUE:
		print '===clean logs==='
		subprocess.check_output('adb logcat -c', shell=True)
		case_name = _format_case_name(apk_file, task_type)
		# if task_type == TASK_TYPE_SHELL_ONEPKG:
		# 	case_name = TEST_CLASS_SHELL_ONEPKG
		# elif task_type == TASK_TYPE_SHELL_JETPACK_ONEPKG:
		# 	case_name = TEST_CLASS_SHELL_JETPACK_ONEPKG
		# elif task_type == TASK_TYPE_ONEPKG_ONEPKG:
		# 	case_name = TEST_CLASS_ONEPKG_ONEPKG
		# elif task_type == TASK_TYPE_10_X:
		# 	case_name = TEST_CLASS_V10_V11
		# elif task_type == TASK_TYPE_11_X:
		# 	case_name = TEST_CLASS_V11_V11
		# elif task_type == TASK_TYPE_10_10:
		# 	case_name = TEST_CLASS_V10_V10
		call_result = ''
		try:
			command = 'adb shell am instrument -e class %s -w %s' % (case_name, PACKAGE_TEST_CASE)
			call_result = subprocess.check_output(command, shell=True)
			print "call_result"
			print call_result
			call_result = _check_instrumentation_output(call_result)
			print "after check call result: " + call_result
		except subprocess.CalledProcessError:
			print 'failed to run class %s ' % case_name
			return INSTRUMENTATION_ERR_SUBPROCESS
		#while process crash happen., retry this case for 5 times.
		#if crash always happens, restart the entier task.
		if call_result == INSTRUMENTATION_ERR_PROCESS_CRASHED:
			retry_count += 1
			if retry_count == 5:
				logout = CONTROL_CONTINUE
			else:
				logout = CONTROL_CLEAN_RESTART
		elif call_result == INSTRUMENTATION_ERR_FAILURES:
			logout = CONTROL_FAILED
		else:
			print 'check nomal out put'
			log = subprocess.check_output('adb logcat -d', shell=True)
			logout = _check_output(log)
			print logout
	return logout

#check the instrumentation outout.
def _check_instrumentation_output(log):
	if re.search('Process\ crashed', log) or re.search('Native\ crash', log) or re.search('Exception', log):
		return INSTRUMENTATION_ERR_PROCESS_CRASHED
	elif re.search('FAILURES', log):
		return INSTRUMENTATION_ERR_FAILURES
	else:
		return INSTRUMENTATION_OK

def _check_output(log):
	m = TEST_UNINSTALL_JETPACK_REG.search(log)
	if not m:
		m = TEST_CASE_OUTPUT_REG.search(log)
		if not m:
			return CONTROL_FAILED
	return m.group(1)

def _uninstall_jetpack():
	try:
		subprocess.check_call('adb uninstall com.dolphin.browser.engine', shell=True)
	except Exception:
		pass

def _format_case_name(from_file, task_type):
	case_name = ''
	if task_type == TASK_TYPE_SHELL_ONEPKG:
		case_name = KERNAL_TEST_CLASS_FORMAT % TEST_CLASS_SHELL_ONEPKG
	elif task_type == TASK_TYPE_SHELL_JETPACK_ONEPKG:
		case_name = KERNAL_TEST_CLASS_FORMAT % TEST_CLASS_SHELL_JETPACK_ONEPKG
	elif task_type == TASK_TYPE_ONEPKG_ONEPKG:
		case_name = KERNAL_TEST_CLASS_FORMAT % TEST_CLASS_ONEPKG_ONEPKG
	elif task_type == TASK_TYPE_NORMAL:
		case_name = NORMAL_TEST_CLASS
	print case_name
	return case_name

def write_total_case_result(task, result):
	if not path.exists(RESULT_DIR):
		print '===create result dir==='
		os.mkdir(RESULT_DIR)
	from_row = 0
	book = None
	if path.exists(TOTAL_RESULT_FILE):
		book = open_workbook(TOTAL_RESULT_FILE)
		sheet = book.sheet_by_index(0)
		from_row = sheet.nrows
	wb = None
	if book:
		wb = copy(book)
	else:
		wb = Workbook()

	ws = None
	try:
		ws = wb.get_sheet(0)
	except Exception:
		pass
	if not ws:
		ws = wb.add_sheet('total_result')

	if from_row == 0:
		ws.row(0).write(0, 'from apk')
		ws.row(0).write(1, 'from jetpack')
		ws.row(0).write(2, 'to apk')
		ws.row(0).write(3, 'type')
		ws.row(0).write(4, 'result')
		from_row += 1
	ws.row(from_row).write(0, task.from_file_name)
	ws.row(from_row).write(1, task.from_jetpack_string)
	ws.row(from_row).write(2, task.to_file_name)
	ws.row(from_row).write(3, task.task_type)
	ws.row(from_row).write(4, result)

	wb.save(TOTAL_RESULT_FILE)

def validate_result(task, result_path):
	print '===========result path========='
	print result_path
	if os.path.exists(result_path):
		book = open_workbook(result_path)
		sheet = book.sheet_by_index(0)
		column_count = sheet.ncols
		row_count = sheet.nrows
		if column_count == 0 or row_count == 0:
			write_total_case_result(task, 'Result is empty!')
		for x in xrange(1, row_count):
			cell_value = sheet.cell_value(x, column_count - 1)
			if cell_value == 'FAILED' or cell_value == 'FAILED_BEFORE_UPDATE':
				write_total_case_result(task, 'FAILED')
				return
		write_total_case_result(task, 'Passed')
	else:
		write_total_case_result(task, 'Result File not found')

class task_error(Exception):

	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return repr(self.value)

