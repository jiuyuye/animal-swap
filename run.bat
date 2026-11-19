@echo off
chcp 936 >nul 2>nul
setlocal
set "ROOT=%~dp0"
cd /d "%ROOT%"

echo ============================================
echo    动物换位游戏  Animal Swap Game
echo ============================================
echo.

where javac >nul 2>nul
if errorlevel 1 goto :nojavac
java -version 2>&1 | findstr /i "version"
echo.

echo [1/2] 正在编译源代码...
if not exist "build\classes" mkdir "build\classes"
javac -encoding UTF-8 -d build\classes -sourcepath src src\animalgame\*.java src\animalgame\model\*.java src\animalgame\view\*.java src\animalgame\controller\*.java src\animalgame\test\*.java src\animalgame\tools\*.java
if errorlevel 1 goto :compilefail
echo       编译成功。
echo.

echo [2/2] 正在启动游戏窗口...
echo.
java -Dstdout.encoding=GBK -Dstderr.encoding=GBK -cp "build\classes" animalgame.Main
if errorlevel 1 goto :runfail
goto :eof

:nojavac
echo [错误] 找不到 javac 命令：系统没有安装 JDK，或者 JDK 没有加入 PATH。
echo.
echo 请安装 JDK 8 或更高版本（推荐 17/21），安装时勾选 "Add to PATH"，
echo 然后关掉本窗口重新双击运行。
echo.
pause
exit /b 1

:compilefail
echo.
echo [错误] 编译失败，错误信息见上面的输出。
echo 常见原因：JDK 版本过低，或 src 目录不完整。
echo.
pause
exit /b 1

:runfail
echo.
echo [错误] 程序运行出错并退出，错误信息见上面的输出。
echo.
pause
exit /b 1
