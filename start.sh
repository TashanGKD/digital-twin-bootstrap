#!/bin/bash
set -e

echo "=== 他山数字分身 Web 版 ==="
echo ""

echo "[1/4] 安装后端依赖..."
cd backend
pip install -r requirements.txt -q

echo "[2/4] 启动后端 (http://localhost:8000)..."
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

echo "[3/4] 安装前端依赖..."
cd ../frontend
npm install --silent

echo "[4/4] 启动前端 (http://localhost:5173)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✓ 后端: http://localhost:8000"
echo "✓ 前端: http://localhost:5173"
echo ""
echo "按 Ctrl+C 退出"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
