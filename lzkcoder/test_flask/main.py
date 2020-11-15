# coding: utf-8
from markdown import markdown
import sys

fd = open('../posts/test_file.md').read().decode('utf-8')
md = '# hello , wor力争'
md = md.decode('utf-8')

print markdown(fd)