@echo off
setlocal

for %%D in (
    "%~dp0..\exports"
    "%~dp0..\pdfs"
    "%~dp0..\emails"
) do (
    if exist "%%~D" (
        echo removing "%%~D"
        rmdir /s /q "%%~D"
    )
    mkdir "%%~D" 2>nul
)

endlocal