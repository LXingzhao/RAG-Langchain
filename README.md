# 🏢 企业智能顾问 (AI Corporate Consultant)

基于 **LangChain**、**Streamlit** 和 **阿里云通义千问 (DashScope)** 构建的检索增强生成 (RAG) 系统。该系统支持多种文档格式解析、向量存储、流式对话以及多会话历史管理。

## ✨ 功能特性

- **📂 多格式文档解析**：支持 `.txt`, `.pdf`, `.docx` 格式的知识库文件上传。
- **🧠 智能检索问答**：基于 Chroma 向量数据库，实现精准的本地知识库检索与增强生成。
- **💬 多会话管理**：支持创建、切换及删除对话，自动将聊天记录持久化保存到本地。
- **⚡ 流式响应**：集成通义千问大模型，提供流畅的打字机式对话体验。
- **🛡️ 查重机制**：通过 MD5 校验避免重复上传相同的文档内容。

## 📸 界面预览

![系统运行截图](./assets/demo_view.png)

## 🛠️ 技术栈

- **前端框架**: [Streamlit](https://streamlit.io/)
- **大模型框架**: [LangChain](https://www.langchain.com/)
- **向量数据库**: [Chroma](https://www.trychroma.com/)
- **大模型 API**: 阿里云 DashScope (通义千问)
- **文档处理**: `pdfplumber`, `python-docx`

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone [https://github.com/你的用户名/你的仓库名.git](https://github.com/你的用户名/你的仓库名.git)
cd 你的仓库名
```
