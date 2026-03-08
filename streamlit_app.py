import streamlit as st
from openai import OpenAI

# 页面基础配置
st.set_page_config(page_title="矩阵内容工厂", page_icon="📲", layout="wide")

# --- 核心配置区 ---
# 已内置你的 DeepSeek API Key
DEEPSEEK_API_KEY = "sk-f33479a860bb4d3d8b6b235baf43c927"
BASE_URL = "https://api.deepseek.com"

# 初始化 OpenAI 客户端 (DeepSeek 兼容 OpenAI 格式)
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)

# --- 标题与说明 ---
st.title("🚀 矩阵 IP 内容自动化工厂")
st.markdown("输入一段灵感，自动生成 **3个账号 × 2个平台** 的定制爆款文案")

# --- 侧边栏：控制逻辑 ---
with st.sidebar:
    st.header("⚙️ 发布控制")
    post_index = st.number_input("当前发布总篇数", min_value=1, value=1, help="每4篇会自动触发一次引导关注的钩子")
    st.divider()
    st.caption("技术支持：DeepSeek-V3")

# --- 账号人设指令集 (System Prompts) ---
PROMPTS = {
    "账号1：政策解读（成都女司机）": {
        "sys": f"""你是一个30岁、负债100万、在成都跑网约车的坚韧女性。
        受众：20-50岁成渝男性，寻找就业机会的迷茫者。
        任务：解读政策利好，证明成都跑车能赚钱且趋势稳定。
        【抖音要求】：极其口语化，像在车里聊天。{'结尾引导：想领成都准入指南的扣1' if post_index % 4 == 0 else '不加生硬广告'}。
        【小红书要求】：干货排版，多用emoji，带#成都网约车 #搞钱。""",
    },
    "账号2：生活感悟（温情祖孙）": {
        "sys": """你是一个90后女孩，和80岁奶奶同居。记录治愈日常，为银发经济带货铺垫。
        【抖音要求】：温馨感性，第一句要动人，有画面感。
        【小红书要求】：氛围感日记风格，大量暖色系emoji（🍵 🪵 🧺 👵），带#我和奶奶的日常。""",
    },
    "账号3：AI知识分享（极客提效）": {
        "sys": """你是一个用AI重构工作流的内容创业者。
        风格：专业、极客、强调效率和信息差。
        【要求】：直接给干货，体现降维打击。带#AI提效 #副业。""",
    }
}

# --- 用户输入区 ---
raw_text = st.text_area("✍️ 粘贴你的原始素材/感悟：", height=150, placeholder="例如：今天看了两会解读，成都网约车有利好，婆婆生病了要多关注身体...")

# --- 执行生成 ---
if st.button("🔥 一键生成全套内容"):
    if not raw_text:
        st.warning("请先输入内容！")
    else:
        with st.spinner("AI 正在根据 3 个人设进行深度创作..."):
            # 遍历三个账号
            for acc_name, config in PROMPTS.items():
                st.subheader(f"📍 {acc_name}")
                col1, col2 = st.columns(2)
                
                # 为每个账号生成 2 种平台文案
                platforms = ["抖音", "小红书"]
                
                for platform in platforms:
                    prompt_content = f"原始素材：{raw_text}\n请根据你的人设，改写成一段【{platform}】爆款文案。直接输出正文。"
                    
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": config["sys"]},
                                {"role": "user", "content": prompt_content}
                            ],
                            stream=False
                        )
                        result = response.choices[0].message.content
                        
                        # 渲染到对应的列
                        if platform == "抖音":
                            with col1:
                                st.info(f"**🎵 抖音版**")
                                st.write(result)
                                st.button(f"复制抖音-{acc_name}", on_click=lambda x=result: st.write(f"已选中，请长按手动复制"))
                        else:
                            with col2:
                                st.success(f"**📕 小红书版**")
                                st.write(result)
                    
                    except Exception as e:
                        st.error(f"生成失败: {str(e)}")
                st.divider()

st.caption("提示：在手机上长按文案即可复制。")
