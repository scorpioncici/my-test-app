import streamlit as st
import deepseek-chat # 或者使用其他大模型SDK

# --- 页面配置 ---
st.set_page_config(page_title="AI 矩阵内容生成器", layout="wide")

st.title("📱 矩阵 IP 内容一键分发")
st.caption("输入一段灵感，生成 3 个账号 × 2 个平台的爆款文案")

# --- 侧边栏：API 配置 ---
with st.sidebar:
    st.header("设置")
    api_key = st.text_input("sk-f33479a860bb4d3d8b6b235baf43c927")
    model_name = st.selectbox("选择模型", ["deepseek-chat"])
    counter = st.number_input("当前篇数（影响互动引导出现频率）", min_value=1, value=1)

# --- 核心提示词库 ---
PROMPTS = {
    "账号1_政策解读": {
        "role": "30岁女性，成都网约车司机，负债100万还债中。人设坚韧、专业、接地气。",
        "target": "20-50岁成渝男性，文化水平大学及以下，寻找就业机会或迷茫者。",
        "logic": "通过解读成都网约车政策，证明‘成都跑车能赚钱’且‘趋势稳定’，转化迷茫人群。",
        "dy_style": "口语化开头，埋钩子，多用‘听我说’、‘实话实说’，每4篇加一次引导（咨询/关注）。",
        "xhs_style": "emoji分段，硬核干货，#成都网约车 #搞钱 #职业规划。"
    },
    "账号2_生活感悟": {
        "role": "90后女孩，与80岁奶奶同居，治愈系生活记录者。",
        "target": "关注银发经济、追求生活品质、情感共鸣群体。",
        "logic": "记录祖孙相处智慧，为银发经济铺路，侧重老人好物潜移默化的心智占领。",
        "dy_style": "温馨感性，‘奶奶说...’开头，慢节奏文案，每4篇加一次情感互动。",
        "xhs_style": "氛围感，精致排版，多用暖色调emoji，#我和奶奶的日常 #银发经济 #治愈。"
    },
    "账号3_AI分享": {
        "role": "正在用AI重塑工作流的内容创业者/数字IP开发者。",
        "target": "内容创作者、副业探索者、对新技术好奇的年轻人。",
        "logic": "展示AI如何降维打击传统创作，打造高效人设，分享实操经验。",
        "dy_style": "节奏快，强调‘效率’、‘省钱’、‘变现’，每4篇引导一次资源领取。",
        "xhs_style": "极简工业风，分步骤拆解，#AI提效 #副业 #数字游民。"
    }
}

# --- UI 交互 ---
raw_input = st.text_area("✍️ 在这里输入你的原始文字/灵感：", height=150, placeholder="例如：今天成都下雨，跑车单子特别多，但奶奶在家等我吃饭...")

if st.button("🚀 批量生成全网文案"):
    if not api_key:
        st.error("请先在左侧输入 API Key！")
    elif not raw_input:
        st.warning("请输入一段文字。")
    else:
        with st.spinner("正在针对不同人设深度创作..."):
            # 模拟循环生成
            for acc_name, config in PROMPTS.items():
                st.subheader(f"📍 {acc_name}")
                col1, col2 = st.columns(2)
                
                # 是否加入引导语
                needs_hook = (counter % 4 == 0)
                
                # 此处封装 API 调用逻辑 (以伪代码展示)
                # res_dy = call_llm(config, platform="抖音", text=raw_input, hook=needs_hook)
                # res_xhs = call_llm(config, platform="小红书", text=raw_input)

                with col1:
                    st.info("**抖音短视频文案**")
                    st.write(f"【爆款开头】\n{config['dy_style'][:15]}...") # 替换为 API 返回值
                    st.button(f"复制抖音-{acc_name}", key=f"dy_{acc_name}")

                with col2:
                    st.success("**小红书图文文案**")
                    st.write(f"【笔记正文】\n✨ {config['xhs_style'][:15]}...") # 替换为 API 返回值
                    st.button(f"复制小红书-{acc_name}", key=f"xhs_{acc_name}")
                st.divider()

st.markdown("---")
st.caption("提示：在手机浏览器访问时，长按即可快速选择文案进行分发。")
