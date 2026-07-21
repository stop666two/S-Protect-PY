@echo off
REM ===================================================
REM S-Protect-PY 启动脚本
REM 用法: sprotect <command> [options]
REM 示例: sprotect version
REM       sprotect config init
REM       sprotect encrypt-project .
REM       sprotect run .
REM ===================================================
python -m sprotect %*
