@echo off
REM ===================================================
REM S-Protect-PY 测试运行脚本
REM ===================================================
echo [S-Protect] Running all tests...
python -m pytest tests -v
if %errorlevel% equ 0 (
    echo [S-Protect] All tests PASSED
) else (
    echo [S-Protect] Some tests FAILED
)
pause
