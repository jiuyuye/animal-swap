@echo off
chcp 936 >nul 2>nul
setlocal
set "ROOT=%~dp0"
cd /d "%ROOT%"

echo ============================================
echo    动物换位游戏 - 模型层单元测试
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

echo [2/2] 正在运行测试...
echo.
java -Dstdout.encoding=GBK -Dstderr.encoding=GBK -cp "build\classes" animalgame.test.GameModelTest
echo.
pause
goto :eof

:nojavac
echo [错误] 找不到 javac 命令，请先安装 JDK 8 或更高版本并加入 PATH。
echo.
pause
exit /b 1

:compilefail
echo.
echo [错误] 编译失败，错误信息见上面的输出。
echo.
pause
exit /b 1
