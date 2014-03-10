import os
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

RESULT_DIR = os.path.join(PROJECT_ROOT, 'result')

TASK_FILE = os.path.join(SRC_DIR, 'task_list.xls')

PACKAGE_NAME = 'mobi.mgeek.TunnyBrowser'

PACKAGE_TEST_CASE = "mobi.mgeek.TunnyBrowser_test/com.dolphin.android.test.InstrumentationTestRunner"

TEST_CLASS_FORMAT = 'com.adolphin.update/%s'

TEST_CLASS_KERNAL = 'TestKernal'

TEST_CLASS_V10_V11 = 'TestUpdateFromV10'

TEST_CLASS_V11_V11 = 'TestUpdateFromV11'

TEST_RESULT_KERNAL = 'test_result_kernal.xls'

TEST_RESULT_V10_V11 = 'test_result_v10_v11.xls'

TEST_RESULT_V11_V11 = 'test_result_v11_v11.xls'
