import subprocess
import re

#first of all, remove the result file.
try:
	#remove result file.
	subprocess.check_call('adb shell rm sdcard/running_result.xls', shell=True)
	#remove temp preference.
	subprocess.check_call('adb shell rm sdcard/temp_preference', shell=True)
	#remove apk pair 
	subprocess.check_call('adb shell rm sdcard/temp_input', shell=True)
except Exception:
	pass
try:
	subprocess.check_call('adb uninstall com.dolphin.browser.engine', shell=True)
except Exception:
	pass
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
	result = subprocess.check_call('adb uninstall mobi.mgeek.TunnyBrowser', shell=True)
except Exception:
	pass