@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

CD test
py "factorial.py" 6 precise -d %*
