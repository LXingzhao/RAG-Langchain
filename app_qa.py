import streamlit as st
import time
from datetime import datetime
from rag import RagService
import config_data as config

# --- 1. 页面配置 ---
st.set_page_config(page_title="企业智能顾问", layout="wide")

# --- 2. 初始化全局 Service ---
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# --- 3. 初始化多会话管理数据结构 ---
if "chat_history_dict" not in st.session_state:
    # 初始默认会话
    initial_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    st.session_state["chat_history_dict"] = {
        initial_id: [{"role": "assistant", "content": "你好，我是您的企业智能顾问，请问有什么可以帮您？"}]
    }
    st.session_state["active_chat_id"] = initial_id

# --- 4. 侧边栏：会话管理 ---
with st.sidebar:
    st.title("AI控制面板")

    # 新建会话
    if st.button("➕ 新建会话", use_container_width=True):
        new_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        st.session_state["chat_history_dict"][new_id] = [
            {"role": "assistant", "content": "你好，新会话已开启。"}
        ]
        st.session_state["active_chat_id"] = new_id
        st.rerun()

    st.divider()
    st.subheader("会话历史")

    # 渲染历史列表
    # 使用 list(keys) 防止在循环中删除导致的报错
    for chat_id in list(st.session_state["chat_history_dict"].keys()):
        col_btn, col_del = st.columns([0.8, 0.2])

        # 当前会话高亮显示 (primary 类型通常为红色或蓝色，视主题而定)
        is_active = (chat_id == st.session_state["active_chat_id"])

        if col_btn.button(
                chat_id,
                key=f"btn_{chat_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
        ):
            st.session_state["active_chat_id"] = chat_id
            st.rerun()

        # 删除按钮
        if col_del.button("❌", key=f"del_{chat_id}"):
            if len(st.session_state["chat_history_dict"]) > 1:
                del st.session_state["chat_history_dict"][chat_id]
                # 如果删的是当前激活的，自动切回第一个
                if is_active:
                    st.session_state["active_chat_id"] = list(st.session_state["chat_history_dict"].keys())[0]
                st.rerun()
            else:
                st.toast("最后一个会话不能删除哦")

# --- 5. 主界面：对话框形式 ---
st.title("企业智能顾问")
st.caption(f"当前通话 ID: {st.session_state['active_chat_id']}")

# 获取当前选中的消息记录
messages = st.session_state["chat_history_dict"][st.session_state["active_chat_id"]]

# 滚动显示历史对话内容
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 6. 底部对话输入框 ---
# 使用 st.chat_input 会自动固定在页面底部
if prompt := st.chat_input("请输入您的问题..."):

    # 展示并保存用户输入
    with st.chat_message("user"):
        st.write(prompt)
    messages.append({"role": "user", "content": prompt})

    # AI 生成逻辑
    with st.chat_message("assistant"):
        placeholder = st.empty()  # 创建占位符用于流式显示内容
        full_response = ""

        with st.spinner("思考中..."):
            try:
                # 获取流式输出
                res_stream = st.session_state["rag"].chain.stream(
                    {"input": prompt},
                    config=config.session_config
                )

                # 使用 write_stream 直接渲染流，这是 Streamlit 最推荐的对话框写法
                full_response = st.write_stream(res_stream)

                # 保存 AI 回复到历史
                messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"连接出错了: {str(e)}")