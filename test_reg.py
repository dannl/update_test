#!/usr/bin/python

import subprocess
from task import *
from statics import *
import shutil
from os import listdir
from os.path import isfile, join
# onlyfiles = [ f for f in listdir(SRC_DIR) if isfile(join(SRC_DIR,f)) ]

# for f in onlyfiles:
# 	subprocess.check_call('sign \'%s\'' % join(SRC_DIR, f), shell=True)

# def _check_instrumentation_output(log):
# 	if re.search('Process\ crashed', log):
# 		return INSTRUMENTATION_ERR_PROCESS_CRASHED
# 	elif re.search('FAILURES', log):
# 		return INSTRUMENTATION_ERR_FAILURES
# 	else:
# 		return INSTRUMENTATION_OK

# def _format_case_name(from_file, task_type):
	# if task_type == TASK_TYPE_SHELL_ONEPKG:
	# 	case_name = TEST_CLASS_SHELL_ONEPKG
	# elif task_type == TASK_TYPE_SHELL_JETPACK_ONEPKG:
	# 	case_name = TEST_CLASS_SHELL_JETPACK_ONEPKG
	# elif task_type == TASK_TYPE_ONEPKG_ONEPKG:
	# 	case_name = TEST_CLASS_ONEPKG_ONEPKG
	# elif task_type == TASK_TYPE_NORMAL:
	# 	case_name == TEST_CLASS_NORMAL
	# 	case_name = case_name + from_file.replace('.apk','').replace('.','_')
	# return case_name
# 	return 'EmptyTest'

# task_type = "onepkg_onepkg"
# apk_file = '10.0.3.apk'

# subprocess.check_output('adb logcat -c', shell=True)
# case_name = _format_case_name(apk_file, task_type)
# try:
# 	command = 'adb shell am instrument -e class %s -w %s' % (TEST_CLASS_FORMAT % case_name, PACKAGE_TEST_CASE)
# 	result = subprocess.check_output(command, shell=True)
# 	print "===="
# 	print _check_instrumentation_output(result)
# except subprocess.CalledProcessError:
# 	print 'failed to run class %s ' % case_name
# shutil.rmtree(RESULT_DIR)
ps = subprocess.check_output('adb shell ps', shell=True)
result = re.search('.+/watch_server', ps)
if result:
	sub = re.findall('\ ([0-9]+)\ ', result.group(0))
	if sub and len(sub) > 0:
		subprocess.check_call('adb shell kill ' + sub[0], shell=True)
	# subprocess.check_call('adb shell kill ')



