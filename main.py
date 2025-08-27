import streamlit as st
from utils import generate_script

st.title("🎞️小红书视频脚本生成器")

st.divider()

with st.sidebar:
    api_key = st.text_input("请输入您的API密钥", type="password")
    st.markdown("[获取DeepSeekapi密钥](https://platform.deepseek.com/api_keys)")

column1, column2, column3 = st.columns([1, 1, 1])
with column1:
    group = st.text_input("👥请输入您的观众类型")

with column2:
    emotion = st.text_input("💕请输入视频的情感基调")

with column3:
    type = st.text_input("🛒请输入视频的类型")


subject = st.text_input("💡请输入视频主题")
video_length = st.number_input("⏰请输入期望时长(单位：min）", value=1.0, min_value=0.1,
                               max_value=10.0, step=0.1)
creativity = st.slider("🪄请选择需要的创造力",value=0.3, min_value=0.0,
                       max_value=1.0, step=0.1)
submit = st.button("立即生成！")

#如果有一个参数没输入就不能执行生成按钮，即执行以下操作
if submit and not api_key:
    st.info("请确定您已获得API密钥，若没有请于官网申请")
    st.stop()#停止后续一切操作
if submit and not subject:
    st.info("请输入主题")
    st.stop()
if submit and not video_length >= 0.1 :
    st.info("视频时长需大于0.1")
    st.stop()
if submit and not type:
    st.info("请输入视频类型")
    st.stop()
if submit and not emotion:
    st.info("请输入情感基调")
    st.stop()
if submit and not group:
    st.info("请输入观众类型")
    st.stop()

if submit:
    with st.spinner("AI正在思考中..."):
        title, script, search_result = generate_script(subject, video_length, creativity, api_key, emotion, type, group)
    st.success("生成脚本如下：")

    st.subheader("标题：")#标题方法
    st.write(title)

    st.subheader("脚本：")
    st.write(script)

    with st.expander("百度百科搜索结果"):
        st.write(search_result)






