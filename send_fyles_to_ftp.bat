@Echo off
rem send files to server by ftp
set ftpscenario=%temp%\ftpscen.txt
call :genscen > %ftpscenario%
REM ftp -i -s:%ftpscenario%
REM del %ftpscenario%
pause
exit 0
:genscen
REM ftp.txt must contain:
REM ftpserver=<SERVER>
REM ftpusrname=<USERNAME>
REM ftppass=<PASSWORD>
for /f "delims== tokens=1,2" %%G in (ftp.txt) do set %%G=%%H
if defined ftpserver (
echo open %ftpserver%
)else (
exit
)
if defined ftpusrname (
echo %ftpusrname%
)else (
exit
)
if defined ftppass (
echo %ftppass%
)else (
exit
)
echo cd y9017159.beget.tech/public_html/cgi/
echo mput C:\Users\qwert\Desktop\Programms\C++_apache2_volume\*.cgi
echo quit
exit /b