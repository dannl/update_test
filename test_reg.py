#!/usr/bin/python
import re

m = re.compile('.*UpateTestResult.*?====(\w+)====')

output = 'soadufosudUpateTestResultouoweurouwouwer====holy====\nsoadufosudUpateTestResultouoweurouwouwer====holy====soadufosudUpateTestResultouoweurouwouwer====holy====soadufosudUpateTestResultouoweurouwouwer====holy====soadufosudUpateTestResultouoweurouwouwer====holy===='

result = m.search(output)

print result

print result.group(1)