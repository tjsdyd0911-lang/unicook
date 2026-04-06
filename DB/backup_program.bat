@echo off
:menu
cls
echo =========================================
echo       MySQL 관리 도구 (v1.0)
echo =========================================
echo  1. 데이터베이스 백업하기 (Export)
echo  2. 데이터베이스 복구하기 (Import)
echo  3. 종료
echo =========================================
set /p choice="원하는 작업 번호를 입력하세요: "

if "%choice%"=="1" goto backup
if "%choice%"=="2" goto restore
if "%choice%"=="3" exit
goto menu

:backup
set /p db="백업할 DB명: "
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump" -u root -p --routines %db% > %db%_backup.sql
pause
goto menu

:restore
set /p f="가져올 파일명(.sql): "
set /p db="넣을 DB명: "
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -u root -p %db% < %f%
pause
goto menu