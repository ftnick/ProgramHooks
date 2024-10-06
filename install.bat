@echo off

for %%f in (*) do (
    if not "%%f"=="hook_manager.py" (
        del "%%f"
    )
)

for /d /a %%d in (*) do (
    if not "%%d"=="plugins" (
        rmdir /s /q "%%d"
    )
)

timeout /t 2 >nul
del "%~f0"
