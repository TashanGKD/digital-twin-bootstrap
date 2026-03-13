"""一键启动前后端（跨平台，单终端）"""
import subprocess
import sys
import os
import signal
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent
BACKEND_DIR = WEB_DIR / "backend"
FRONTEND_DIR = WEB_DIR / "frontend"

processes = []


def cleanup(*_):
    for p in processes:
        try:
            p.terminate()
        except Exception:
            pass
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

print("=" * 50)
print("  他山数字分身 Web 版 — 一键启动")
print("=" * 50)
print()

# 安装后端依赖
print("[1/4] 安装后端依赖...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"],
    cwd=BACKEND_DIR,
    check=True,
)

# 启动后端
print("[2/4] 启动后端 (http://localhost:8000)...")
backend = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
    cwd=BACKEND_DIR,
)
processes.append(backend)

# 安装前端依赖
print("[3/4] 安装前端依赖...")
npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
subprocess.run([npm_cmd, "install", "--silent"], cwd=FRONTEND_DIR, check=True)

# 启动前端
print("[4/4] 启动前端 (http://localhost:5173)...")
frontend = subprocess.Popen(
    [npm_cmd, "run", "dev"],
    cwd=FRONTEND_DIR,
)
processes.append(frontend)

print()
print("  后端: http://localhost:8000")
print("  前端: http://localhost:5173  ← 浏览器打开这个")
print()
print("  按 Ctrl+C 退出")
print()

try:
    backend.wait()
except KeyboardInterrupt:
    cleanup()
