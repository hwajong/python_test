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
def parse_matrix(lines, ignore_column):
	mat = ''
	for s in lines:
		s = s.strip()

		# 빈칸이 나올때 까지 매트릭스 값이다.
		if not s:
			break

		# ignore_column 을 버린다 (default 1 : column name)
		row_list = s.split()
		row_list = [row_list[i] for i in range(len(row_list)) if i not in ignore_column]
		fmt = "%8.8s" * len(row_list)
		row = fmt % tuple(row_list)
		mat += (row + '\n')

	return mat


'''
lines 리스트에서 matrix_name 행렬값 string 을 리턴한다.
'''
def get_matrix(lines, matrix_name, num_of_matrix=1, skip_header=4, ignore_column=[0]):
	index = find_index(lines, matrix_name)
	
	if index == -1:
		return ''

	# title 다음 skip_header 째줄 부터 매트릭스 값이 나온다.
	# 헤더는 버림 
	mat = parse_matrix(lines[index+skip_header:], ignore_column)

	# 행렬이 2개 일때 
	if num_of_matrix == 2:
		mat_lines = len(mat.splitlines())
		mat2 = parse_matrix(lines[index+skip_header+mat_lines+2:], ignore_column)
		mat += mat2

	return mat
	
'''
해당 행렬이 없을경우 False 리턴
'''
def check_mat(mat, matrix_name, fname):
	if not mat:
		print('[%s] matrix does not exist! - skip %s') % (matrix_name, fname)
		return False

	return True


# -------------
# MAIN
# -------------
fo = open('all_new.txt', 'w')
for fname in glob.glob("*.out"):

	fi = open(fname, 'r')
	lines = fi.readlines()
	fi.close()

	matrix_name = 'CF-VARIMAX Rotated Factor Matrix'
	mat1 = get_matrix(lines, matrix_name, skip_header=5, ignore_column=[0])
	if not check_mat(mat1, matrix_name, fname):
		continue
	
	index = find_index(lines, matrix_name)
	assert(index != -1)

	matrix_name = 'Factor Correlations'
	mat2 = get_matrix(lines[index:], matrix_name)
	if not check_mat(mat2, matrix_name, fname):
		continue

	matrix_name = 'Standard Errors after Rotation'
	mat3 = get_matrix(lines, matrix_name, num_of_matrix=2)
	if not check_mat(mat3, matrix_name, fname):
		continue

	fo.write(mat1)
	fo.write(mat2)
	fo.write(mat3)
		

