#!/bin/bash
# OpenClaw Monitor Skill 一键安装脚本
# 用法: curl -sSL https://raw.githubusercontent.com/gezhongjian-mini/agent-skill-hub/main/install-monitor.sh | bash

set -e

SKILL_NAME="openclaw-monitor"
SKILL_DIR="/opt/homebrew/lib/node_modules/openclaw/skills/${SKILL_NAME}"
REPO_URL="https://github.com/gezhongjian-mini/agent-skill-hub"

echo "🎯 OpenClaw Monitor Skill 安装器"
echo "================================"

# 检查 OpenClaw 是否安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ 错误: 未检测到 OpenClaw"
    echo "请先安装 OpenClaw: npm install -g openclaw"
    exit 1
fi

echo "✅ OpenClaw 已安装"

# 检查 skill 目录
OPENCLAW_SKILL_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
if [ ! -d "$OPENCLAW_SKILL_DIR" ]; then
    echo "❌ 错误: OpenClaw skill 目录不存在: $OPENCLAW_SKILL_DIR"
    exit 1
fi

echo "📁 Skill 目录: $OPENCLAW_SKILL_DIR"

# 如果已存在，备份旧版本
if [ -d "$SKILL_DIR" ]; then
    echo "📦 检测到已安装版本，备份中..."
    mv "$SKILL_DIR" "${SKILL_DIR}.backup.$(date +%Y%m%d%H%M%S)"
fi

# 创建临时目录
echo "⬇️  正在下载..."
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

# 克隆仓库（浅克隆，只取最新）
git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" repo 2>/dev/null || {
    echo "⚠️  Git 克隆失败，尝试直接下载..."
    curl -sL "${REPO_URL}/archive/refs/heads/main.tar.gz" | tar -xz
    mv agent-skill-hub-main/repo/skills/gezhongjian-mini/openclaw-monitor ./openclaw-monitor 2>/dev/null || \
    mv agent-skill-hub-main/skills/gezhongjian-mini/openclaw-monitor ./openclaw-monitor
}

# 复制 skill
if [ -d "repo" ]; then
    cp -r "repo/skills/gezhongjian-mini/openclaw-monitor" "$SKILL_DIR"
else
    cp -r "openclaw-monitor" "$SKILL_DIR"
fi

# 清理
rm -rf "$TMP_DIR"

# 验证安装
echo "🔍 验证安装..."
if [ -f "$SKILL_DIR/src/main.py" ]; then
    echo "✅ Skill 文件安装成功"
else
    echo "❌ 安装失败，文件缺失"
    exit 1
fi

# 显示使用方法
echo ""
echo "🎉 安装完成！"
echo "=============="
echo ""
echo "📊 使用方法:"
echo ""
echo "  1. 生成静态看板:"
echo "     python $SKILL_DIR/src/main.py --output ~/openclaw-monitor.html"
echo ""
echo "  2. 启动 HTTP 服务 (实时更新):"
echo "     python $SKILL_DIR/src/main.py --serve --port 8891"
echo ""
echo "  3. 然后浏览器打开: http://localhost:8891"
echo ""
echo "🌐 项目地址: $REPO_URL"
echo ""
