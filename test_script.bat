@echo off
start /B py s.py 1

py test.py > test.log 2>&1
pause