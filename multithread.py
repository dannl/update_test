from multiprocessing import Process, Pipe
import time
import subprocess

class Result(object):

	check = ''

	fuck = ''

	def __init__(self):
		pass

def function(main):
	i = 0
	while True:
		print 'hello', main
		i += 1
		time.sleep(3)
		if i > 3:
			print 'terminate the main thread.'
			main.terminate()
			break

def main_thread(cone, name):
	while True:
		subprocess.check_call('echo hello', shell=True)
		name.fuck = 'holy'
		print 'name is:', name
		print 'name.fuck=', name.fuck
		time.sleep(2)
		cone.send('fuck')

check = Result()

if __name__ == '__main__':
	# threads = []
	# for x in xrange(1,5):
	# 	p = Process(target=function, args=('bob', x))
	# 	p.start()
	# 	threads.append(p)
	
	# for t in threads:
	# 	t.join()
	parent_cone, child_cone = Pipe()
	print 'check is', check
	main = Process(target=main_thread, args=(child_cone, check))
	checking = Process(target=function, args=(main,))
	main.start()
	checking.start()
	main.join()
	print "==========", parent_cone.recv()
	checking.terminate()
	print "here."
	print 'check is', check
	print check.fuck
	strings = ['shit', 'fuck']
	string = str(strings)
	print string

