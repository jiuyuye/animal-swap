# -*- coding: utf-8 -*-
"""把 run.bat / run_tests.bat 以 GBK(cp936) 编码写出。

cmd.exe 按系统代码页解析 .bat 文件的字节，若用 UTF-8 保存，
中文会被按 GBK 拆开，可能拼出非法命令（'模型层单元测试' is not recognized...）。
"""
import pathlib

ROOT = pathlib.Path(r"C:\Users\mjqqd\Documents\deepseek-harness\default-workspace\动物换位")

RUN = r"""@echo off
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
"""

TESTS = r"""@echo off
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
"""

for name, text in (("run.bat", RUN), ("run_tests.bat", TESTS)):
    # 换行统一成 CRLF，cmd 才不会把行尾 ^ 之类解析错
    data = text.replace("\r\n", "\n").replace("\n", "\r\n")
    (ROOT / name).write_bytes(data.encode("gbk"))
    print("wrote", name, len(data), "chars")

