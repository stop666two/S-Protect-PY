@echo off
REM ===================================================
REM S-Protect-PY launcher
REM Usage: sprotect <command> [options]
REM Examples:
REM   sprotect version
REM   sprotect config init
REM   sprotect build --clean
REM   sprotect run
REM ===================================================
python -m sprotect %*
