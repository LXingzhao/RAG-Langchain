import time
import streamlit as st
import pdfplumber
from docx import Document
from io import BytesIO
from knowledge_base import KnowledgeBaseService
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes


# --------------------------
# 带OCR的文件解析函数
# --------------------------
def extract_text_from_file_large(uploaded_file, chunk_size=1024 * 1024):
    file_name = uploaded_file.name
    full_text = []

    try:
        if file_name.endswith('.txt'):
            uploaded_file.seek(0)
            while chunk := uploaded_file.read(chunk_size):
                full_text.append(chunk.decode("utf-8", errors="ignore"))

        elif file_name.endswith('.pdf'):
            uploaded_file.seek(0)
            # 第一步：先用pdfplumber尝试提取文本
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
                    if page_text:
                        full_text.append(page_text)
                    page.flush_cache()

            # 如果文本提取失败，说明是扫描件，用OCR识别
            if not full_text:
                st.info("检测到扫描件PDF，正在使用OCR识别...")
                uploaded_file.seek(0)
                images = convert_from_bytes(uploaded_file.read())
                for img in images:
                    # 识别图片中的文字，支持中文
                    text = pytesseract.image_to_string(img, lang='chi_sim')
                    if text.strip():
                        full_text.append(text)

        elif file_name.endswith('.docx'):
            uploaded_file.seek(0)
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                t = para.text.strip()
                if t:
                    full_text.append(t)

        return "\n".join(full_text)

    except Exception as e:
        st.warning(f"文件读取警告：{str(e)}")
        return "\n".join(full_text)


# --- Streamlit 界面 ---
st.title("知识库更新服务")

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# 注意：这里变量名是 uploader_file，下面要和它对应
uploader_file = st.file_uploader(
    "请上传 pdf、docx、txt 文件（支持100MB+大文件/扫描件PDF）",
    type=['txt', 'pdf', 'docx'],
    accept_multiple_files=False,
)

if uploader_file is not None:
    file_name = uploader_file.name
    file_size = uploader_file.size / 1024 / 1024  # MB

    st.subheader(f"文件名：{file_name}")
    st.write(f"大小：{file_size:.2f} MB")

    try:
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("正在解析文件...")
        progress_bar.progress(30)

        # 关键修复：把 uploader_file 传给函数
        file_content = extract_text_from_file_large(uploader_file)

        progress_bar.progress(60)
        status_text.text("正在导入知识库...")

        if file_content.strip():
            # 分块上传知识库（避免一次性提交超大文本）
            max_chunk = 8000
            chunks = [file_content[i:i + max_chunk] for i in range(0, len(file_content), max_chunk)]
            total = len(chunks)

            for i, chunk in enumerate(chunks):
                status_text.text(f"正在上传第 {i + 1}/{total} 块...")
                result = st.session_state["service"].upload_by_str(chunk, file_name)

            progress_bar.progress(100)
            status_text.text("处理完成！")
            st.success("✅ 处理成功！")
            st.write(result)
        else:
            st.error("未能提取到有效文本内容。")

        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

    except Exception as e:
        st.error(f"处理文件时出错: {str(e)}")