#!/usr/bin/python
# -*- coding:utf-8 -*-

import glob
import re
import os

META_DATA_FILE = "cefa_rep1.inp"
OUTPUT_PREFIX = "unrotated_factor_"

# null.txt 메타데이터 로딩
f = open(META_DATA_FILE, 'r') 
meta_data = f.read()
f.close()

print "** Meta data read success!"
print(meta_data)

# 현 디렉토리의 모든 out 파일에서 Unrotated Factor Loadings 행렬을
# 가져와 메타데이터를 붙여 새로운 파일을 만든다.
for fname in glob.glob("*.out"):
	if fname.find(OUTPUT_PREFIX) == 0:
		continue

	fin = open(fname, 'r') 
	fdata = fin.read()
	fin.close()
	
	# 정규식을 이용해 해당 행렬을 추출한다. 
	
	pattern = re.compile("Unrotated Factor Loadings:[\d\s\.+-]*", re.S)
	match = pattern.findall(fdata)

	if len(match) < 1:
		print "Rotated Factor does not exist! - " + fname
		continue

	print "** matrix find success!"
	print match[0]

	# 정규식을 이용해 순번은 분리한다.
	# 읽어들이려는 행렬의 행이 4가 아니면 정규식 수정해야 함. ----> \s+[\d\.+-]+ 을 늘어난 개수만큼 추가   
	pattern = re.compile("\s*\d+\s+([\d\.+-]+\s+[\d\.+-]+\s+[\d\.+-]+\s+[\d\.+-]+)\s*\n")
	match = pattern.findall(match[0])

	# 항상 행렬은 12열 이어야 한다.
	# 읽어들이려는 행렬의 열이 12개가 아니면 수정해야함. 
	if len(match) != 12:
		print "Wrong unrotated Factor matrix size : " + len(match)
		continue

	mat = "\n".join(match)
	mat += "\n"
	print "** parse matrix success!"
	print mat

	# 결과파일 생성
	fname_out = OUTPUT_PREFIX + os.path.splitext(fname)[0] + ".inp"
	fout = open(fname_out, "w")
	fout.write(meta_data);
	fout.write(mat)
	fout.close()

	print "** new maatrix file created! - " + fname_out





