import os
import re
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

RESULT_DIR = os.path.join(PROJECT_ROOT, 'result')

TASK_FILE = os.path.join(SRC_DIR, 'task_list.xls')

TOTAL_RESULT_FILE = os.path.join(RESULT_DIR, 'total_reuslt.xls')

PACKAGE_NAME = 'mobi.mgeek.TunnyBrowser'

PACKAGE_TEST_CASE = "mobi.mgeek.TunnyBrowser_test/com.dolphin.android.test.InstrumentationTestRunner"

KERNAL_TEST_CLASS_FORMAT = 'com.adolphin.update.kernal/%s'

NORMAL_TEST_CLASS = 'com.adolphin.update.normal/TestNormal'

TEST_CLASS_SHELL_ONEPKG = 'TestKernal_shell_onepkg'

TEST_CLASS_SHELL_JETPACK_ONEPKG = 'TestKernal_shell_jetpack_onepkg'

TEST_CLASS_ONEPKG_ONEPKG = 'TestKernal_onepkg_onepkg'

TEST_CASE_OUTPUT_REG = re.compile('.*UpateTestResult.*?====(\w+)====')

TEST_UNINSTALL_JETPACK_REG = re.compile('.*UpateTestResult.*?=====(\w+)=====')

RESTART_TASK = -1

NEXT_TASK = 0

INSTRUMENTATION_ERR_PROCESS_CRASHED = "process_crashed"

INSTRUMENTATION_ERR_FAILURES = "case_failures"

INSTRUMENTATION_ERR_OK = "case_ok"

INSTRUMENTATION_ERR_SUBPROCESS = "subprocess_err"

CONTROL_CLEAN_RESTART = "clean_restart"

CONTROL_RESTART = 'restart'

CONTROL_CONTINUE = 'continue'

CONTROL_FAILED = "failed"

CONTROL_UNINSTALL_JETPACK = "uninstall_jetpack"

