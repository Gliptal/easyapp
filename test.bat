@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

CD test
py "factorial.py" 10 approximate -d %*
