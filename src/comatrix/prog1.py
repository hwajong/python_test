#!/usr/bin/python
# -*- coding:utf-8 -*-

import glob

META_DATA_FILE = "null.txt"
OUTPUT_PREFIX = "meta_added_"

# null.txt 메타데이터 로딩
f = open(META_DATA_FILE, 'r') 
meta_data = f.read()
f.close()

print "** Meta data read success!"
print(meta_data)


# 현 디렉토리의 모든 txt 파일에 
# 메타데이터를 붙여 새로운 파일을 만든다.
for fname in glob.glob("*.txt"):
	if fname.find(OUTPUT_PREFIX) == 0:
		continue

	if fname == META_DATA_FILE:
		continue

	fin = open(fname, 'r') 
	fdata = fin.read()
	fin.close()

	# 결과파일 생성
	fname_out = OUTPUT_PREFIX + fname
	fout = open(fname_out, "w")
	fout.write(meta_data);
	fout.write(fdata);
	fout.close()

	print "** new maatrix file created! - " + fname_out


