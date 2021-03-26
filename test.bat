@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

CD test
py "calculator.py" all -d %*
