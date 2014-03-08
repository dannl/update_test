#!/usr/bin/python
from xlrd import open_workbook
from task import *
from statics import *

if __name__ == '__main__':

	book = open_workbook(TASK_FILE);

	sheet = book.sheet_by_index(0)

	for i in range(1, sheet.nrows):
		print 'looping-------'
		single = Task(sheet, i)
		single.excute()
