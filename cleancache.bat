@echo off
setlocal enabledelayedexpansion
echo ========================================
echo Nexus Cache Cleaner
echo ========================================
echo.

echo Starting cache cleanup...
echo.

@REM Counter initialization
set "pycache_count=0"
set "temp_count=0"

REM Clean up the Python __pycache__ directory
echo [1/2] Cleaning Python cache files...
for /f "delims=" %%d in ('dir /s /b /ad __pycache__ 2^>nul') do (
    echo   Deleting: %%d
    rd /s /q "%%d" 2>nul
    if !errorlevel! equ 0 (
        set /a pycache_count+=1
    )
)

REM Clean up temporary files
echo [2/2] Cleaning temporary files...
for %%ext in (*.tmp *.pyc *.temp *.pyo) do (
    for /f "delims=" %%f in ('dir /s /b "%%ext" 2^>nul') do (
        echo   Deleting: %%f
        del /f /q "%%f" 2>nul
        if !errorlevel! equ 0 (
            set /a temp_count+=1
        )
    )
)

echo.
echo ========================================
echo Cleanup Summary:
echo   Python cache directories: !pycache_count!
echo   Temporary files: !temp_count!
echo ========================================

if !pycache_count! gtr 0 (
    echo Cache cleanup completed successfully!
) else if !temp_count! gtr 0 (
    echo Temporary files cleanup completed!
) else (
    echo No cache files found to clean.
)

echo.
pause