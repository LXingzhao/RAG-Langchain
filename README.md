# 🏢 企业智能顾问 RAG 系统

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Streamlit-1.30+-red.svg" alt="Streamlit Version">
  <img src="https://img.shields.io/badge/LangChain-0.1+-green.svg" alt="LangChain Version">
  <img src="https://img.shields.io/badge/ChromaDB-0.4+-orange.svg" alt="ChromaDB Version">
  <img src="https://img.shields.io/badge/通义千问-API-yellow.svg" alt="Tongyi Qwen">
</div>

<br>

一款基于 RAG（检索增强生成）的企业智能法律顾问系统，支持上传 PDF/Word/TXT 法律文档构建知识库，结合通义千问大模型实现精准的法律问题问答，同时支持多会话管理、对话历史持久化。

## 📋 功能特性
- 📄 **多格式文件解析**：支持 PDF、DOCX、TXT 格式文件上传，自动提取文本内容；
- 🔍 **智能检索增强**：基于 Chroma 向量库检索相关法律文档片段，精准回答问题；
- 💬 **多会话管理**：支持新建/删除会话，对话历史本地持久化存储；
- 🚫 **重复内容过滤**：基于 MD5 校验，避免重复上传相同内容到知识库；
- 🎨 **友好交互界面**：Streamlit 搭建的可视化界面，操作简单易上手；
- ⚡ **流式输出回答**：AI 回答实时流式展示，提升交互体验。

## 🚀 快速开始

### 1. 环境准备
- Python 3.10+
- 阿里云 DashScope 通义千问 API 密钥（需自行申请：[阿里云百炼](https://dashscope.console.aliyun.com/)）

### 2. 安装依赖
```bash
# 克隆仓库
git clone https://github.com/你的用户名/企业法律顾问RAG.git
cd 企业法律顾问RAG

# 安装依赖
pip install -r requirements.txt
