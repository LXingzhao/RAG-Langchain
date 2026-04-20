import time
import streamlit as st
import pdfplumber
from docx import Document
from io import BytesIO
from knowledge_base import KnowledgeBaseService


# 辅助函数：根据文件类型提取文本
def extract_text_from_file(uploaded_file):
    file_name = uploaded_file.name

    if file_name.endswith('.txt'):
        # TXT 直接解码
        return uploaded_file.getvalue().decode("utf-8")

    elif file_name.endswith('.pdf'):
        # PDF 解析
        with pdfplumber.open(uploaded_file) as pdf:
            content = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return content

    elif file_name.endswith('.docx'):
        # Docx 解析
        doc = Document(BytesIO(uploaded_file.getvalue()))
        content = "\n".join([para.text for para in doc.paragraphs])
        return content

    return None


# --- Streamlit 界面 ---

st.title("知识库更新服务")

# 初始化 Service
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# 文件上传
uploader_file = st.file_uploader(
    "请上传 pdf、docx、txt 文件",
    type=['txt', 'pdf', 'docx'],
    accept_multiple_files=False,
)

if uploader_file is not None:
    # 展示文件基本信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024  # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    try:
        with st.spinner("解析并载入知识库中..."):
            # 1. 核心改动：不再直接 decode，而是调用解析函数获取字符串
            file_content = extract_text_from_file(uploader_file)

            if file_content:
                time.sleep(1)
                # 2. 将解析出的文本传入你原来的 service 方法
                result = st.session_state["service"].upload_by_str(file_content, file_name)
                st.success("处理成功！")
                st.write(result)
            else:
                st.error("未能提取到有效文本内容。")

    except Exception as e:
        st.error(f"处理文件时出错: {e}")