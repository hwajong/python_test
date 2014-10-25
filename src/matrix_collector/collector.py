#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import glob

'''
lines 리스트에서 find_str 스트링이 있는 index 리턴
'''
def find_index(lines, find_str):
	index = -1
	for line in lines:
		if line.find(find_str) != -1:
			index = lines.index(line)
			break

	return index

'''
행렬값을 파싱해 정해진 포맷스트링으로 리턴
'''
def parse_matrix(lines):
	mat = ''
	for s in lines:
		s = s.strip()

		# 빈칸이 나올때 까지 매트릭스 값이다.
		if not s:
			break

		# 첫째 열은 버린다(row name)
		row_list = s.split()[1:]
		fmt = "%8.8s" * len(row_list)
		row = fmt % tuple(row_list)
		mat += (row + '\n')

	return mat


'''
lines 리스트에서 matrix_name 행렬값 string 을 리턴한다.
'''
def get_matrix(lines, matrix_name, num_of_matrix=1):
	index = find_index(lines, matrix_name)
	
	if index == -1:
		return ''

	# title 다음 4째줄 부터 매트릭스 값이 나온다.
	# 3번째 줄은 헤더 
	mat = parse_matrix(lines[index+4:])

	# 행렬이 2개 일때 
	if num_of_matrix == 2:
		mat_lines = len(mat.splitlines())
		mat2 = parse_matrix(lines[index+4+mat_lines+2:])
		mat += mat2

	return mat
	

# -------------
# MAIN
# -------------
fo = open('all_new.txt', 'w')
for fname in glob.glob("*.out"):

	fi = open(fname, 'r')
	lines = fi.readlines()
	fi.close()

	mat = get_matrix(lines, 'CF-VARIMAX Rotated Factor Matrix')
	assert(mat)
	fo.write(mat)

	mat = get_matrix(lines, 'GEOMIN Rotated Factor Matrix')
	assert(mat)
	fo.write(mat)
	
	index = find_index(lines, 'GEOMIN Rotated Factor Matrix')
	assert(index != -1)

	mat = get_matrix(lines[index:], 'Factor Correlations')
	assert(mat)
	fo.write(mat)

	mat = get_matrix(lines, 'Standard Errors after Rotation', 2)
	assert(mat)
	fo.write(mat)

