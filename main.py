#!/usr/bin/python
from xlrd import open_workbook
from task import *
from statics import *
import sys

if __name__ == '__main__':

	print str(sys.argv)

	args = sys.argv

	if len(args) == 1 or len(args) == 3:

		if len(args) == 1:
			book = open_workbook(TASK_FILE);

			sheet = book.sheet_by_index(0)

			if os.path.exists(TOTAL_RESULT_FILE):
				os.remove(TOTAL_RESULT_FILE)

			for i in range(1, sheet.nrows):
				print 'looping-------'
				# if i == 1 or i == 3:
				# 	continue
				single = Task(sheet, i)
				result = -1
				retry_count = 0
				while result != NEXT_TASK and retry_count < 5:
					if retry_count != 0:
						try:
							subprocess.check_call('adb kill-server', shell=True)
							subprocess.check_call('adb start-server', shell=True)
						except Exception:
							pass
					result = single.excute()
					retry_count += 1
				if result != NEXT_TASK:
					#which means the task is failed forever, write the result
					write_total_case_result(single, 'Faild for adb err')
		else:
			book = open_workbook(args[1]);

			sheet = book.sheet_by_index(0)

			if os.path.exists(TOTAL_RESULT_FILE):
				os.remove(TOTAL_RESULT_FILE)

			for i in range(1, sheet.nrows):
				print 'looping-------'
				# if i == 1 or i == 3:
				# 	continue
				single = Task(sheet, i)
				single.setdevice(args[2])
				result = -1
				retry_count = 0
				while result != NEXT_TASK and retry_count < 5:
					# if retry_count != 0:
					# 	try:
					# 		subprocess.check_call('adb kill-server', shell=True)
					# 		subprocess.check_call('adb start-server', shell=True)
					# 	except Exception:
					# 		pass
					result = single.excute()
					retry_count += 1
				if result != NEXT_TASK:
					#which means the task is failed forever, write the result
					write_total_case_result(single, 'Faild for adb err')

				
	# for i in range(1, sheet.nrows):
	# 	print 'looping-------'
	# 	single = Task(sheet, i)
	# 	validate_result(single, path.join(RESULT_DIR, single.to_string(), "running_result.xls"))
