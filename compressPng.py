#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8
import os, time
import sys
import os.path
import click
import tinify
import subprocess

# tinify API KEY  申请地址 https://tinypng.com
tinify.key = ""
#压缩是否成功，全局标示只要有失败则返回
compressSuccess = True
compressPngCount = 0

# 压缩的核心
def compress_core(inputFile, outputFile, img_width):
	source = tinify.from_file(inputFile)
	if img_width is not -1:
		resized = source.resize(method = "scale", width  = img_width)
		resized.to_file(outputFile)
	else:
		source.to_file(outputFile)

# 仅压缩指定文件  width为-1默认不变
def compress_file(inputFile, width):
	if not os.path.isfile(inputFile):
		print "这不是一个文件，请输入文件的正确路径!"
		return
	print "file = %s" %inputFile
	dirname  = os.path.dirname(inputFile)
	basename = os.path.basename(inputFile)
	fileName, fileSuffix = os.path.splitext(basename)
	if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg':
		compress_core(inputFile, dirname+"/tiny_"+basename, width)
		#替换图片 先删除原来的图片 再把压缩的图片名替换成原来的名字
		if os.path.isfile(dirname+"/"+basename):
			os.remove(dirname+"/"+basename)
			global compressPngCount
			compressPngCount+=1
		else:
			print ("delete %s/%s failed" %(dirname, basename))
			compressSuccess = False
		if os.path.isfile(dirname+"/tiny_"+basename):
			os.rename(dirname+"/tiny_"+basename,dirname+"/"+basename)
		else:
			compressSuccess = False
			print ("rename %s/tiny_%s failed" %(dirname, basename))
	else:
		compressSuccess = False
		print "不支持该文件类型!"


#root directory
def compressPngStartDate(startDate, branchName):
	os.system('git rev-parse --abbrev-ref HEAD')
	rootdir=os.getcwd()
	os.system('git log --name-status --since=\"'+ startDate +'\" > gitlog.txt')
	gitlogFile = open("gitlog.txt")

	#过滤重复的提交记录 把重复添加的，重复修改的或者 既有添加又有修改的保留一个即可
	filterLogPointer=file("filterLog.txt", "w")
	hashKey={}
	for fileLine in gitlogFile:
		# Android匹配规则
		# if ((fileLine.find("9.png") == -1) and (fileLine.find(".png") != -1) and (fileLine.find("A	") != -1 or fileLine.find("M	") != -1) ):
		# iOS匹配规则
		if ((fileLine.find("Images.xcassets") != -1) and (fileLine.find(".png") != -1) and (fileLine.find("A	") != -1 or fileLine.find("M	") != -1) ):
			gitPngPath=fileLine[2:]
			if not hashKey.has_key(gitPngPath):
				hashKey[gitPngPath]=1
				filterLogPointer.write(fileLine)
	filterLogPointer.close()

	filterLogFile = open("filterLog.txt")
	for gitlogLine in filterLogFile.xreadlines():
		# print(gitlogLine)
		if (gitlogLine.find("A	") != -1 and gitlogLine.find(".png") != -1):
			#Add Png
			pngPath=rootdir+"/"+gitlogLine[2:]
			pngPath=pngPath.strip('\n')
			#虽然是Add 但是防止Add之后又Delete此时这个图片是不存在的
			if os.path.isfile(pngPath):
				print(pngPath)
				compress_file(pngPath, -1)
		elif (gitlogLine.find("M	") != -1 and gitlogLine.find(".png") != -1):
			#Modify Png
			pngPath=rootdir+"/"+gitlogLine[2:]
			pngPath=pngPath.strip('\n')
			#虽然是Modify 但是防止Modify之后又Delete此时这个图片是不存在的
			if os.path.isfile(pngPath):
				print(pngPath)
				compress_file(pngPath, -1)
	os.remove(rootdir+'/gitlog.txt')
	os.remove(rootdir+'/filterLog.txt')
	if (compressPngCount):
		if (compressSuccess):
			date = time.strftime("%y-%m-%d-%H:%M", time.localtime(time.time() + 300))
			f = open('startDate.txt','r+')
			f.write(date)
			f.close()
			print("compressSuccess")
			os.system('git stash')
			os.system('git pull')
			os.system('git stash pop')
			os.system('git status')
			os.system('git add -A')
			os.system('git commit -m "Change 自动化压缩图片"')
			os.system('git push --set-upstream origin {0}'.format(branchName))
		else:
			print("compressFailed")
			os.system('git stash')
	else:
		date = time.strftime("%y-%m-%d-%H:%M", time.localtime(time.time() + 300))
		f = open('startDate.txt','r+')
		f.write(date)
		f.close()
		os.system('git stash')
		os.system('git pull')
		os.system('git stash pop')
		os.system('git status')
		os.system('git add -A')
		os.system('git commit -m "Change 修改自动化压缩时间"')
		os.system('git push --set-upstream origin {0}'.format(branchName))
		print('no pngCompress')