#!/usr/bin/python
#-*- coding: utf-8 -*-
#encoding=utf-8
import compressPng, os, getopt, sys

f=open("startDate.txt")
date = f.readline()
# 示例 分支名称可以通过脚本获取 
compressPng.compressPngStartDate(date, 'dev_2.9.9.0')
f.close()