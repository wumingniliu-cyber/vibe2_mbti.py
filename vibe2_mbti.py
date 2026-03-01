import streamlit as st
import streamlit.components.v1 as components
import random
import time
import math
import hashlib
import html
import json
from datetime import datetime
import plotly.graph_objects as go

# --- 1. 页面与全局配置 (沉浸式全屏化) ---
st.set_page_config(
    page_title="SDE 核心算力引擎 | 确权终端",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 赛博科技级 UI 引擎 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Orbitron:wght@400;500;700;900&display=swap');

    /* 隐藏 Streamlit 默认UI */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem; max-width: 680px; }

    /* 全局深网背景 */
    html, body, [class*="css"], .stApp { background-color: #030712 !important; font-family: 'Noto Sans SC', sans-serif !important; color: #f8fafc !important; }
    
    /* CRT 扫描线与网格 */
    [data-testid="stAppViewContainer"]::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02)); background-size: 100% 3px, 3px 100%; z-index: 99999; pointer-events: none; opacity: 0.5; }
    [data-testid="stAppViewContainer"] { background-image: radial-gradient(circle at 50% 0%, #0f172a 0%, #030712 80%), linear-gradient(0deg, rgba(0,243,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px) !important; background-size: 100% 100%, 40px 40px, 40px 40px !important; }
    
    .stMarkdown, p, span, h2, h3, h4, li, div { color: #f8fafc !important; }
    [data-testid="stProgress"] > div > div > div { background-color: #00f3ff !important; box-shadow: 0 0 15px rgba(0,243,255,0.8); }
    
    /* Glitch 标题 */
    .hero-title { font-size: 38px !important; font-weight: 900 !important; text-align: center; color: #ffffff !important; letter-spacing: 4px; margin-bottom: 5px; text-shadow: 0 0 20px rgba(0,243,255,0.7), 0 0 40px rgba(0,243,255,0.3); position: relative; display: inline-block; }
    .hero-title::before, .hero-title::after { content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: transparent; }
    .hero-title::before { left: 2px; text-shadow: -2px 0 #f43f5e; animation: glitch-anim-1 2s infinite linear alternate-reverse; }
    .hero-title::after { left: -2px; text-shadow: 2px 0 #00f3ff; animation: glitch-anim-2 3s infinite linear alternate-reverse; }
    @keyframes glitch-anim-1 { 0% { clip-path: inset(20% 0 80% 0); } 20% { clip-path: inset(60% 0 10% 0); } 40% { clip-path: inset(40% 0 50% 0); } 60% { clip-path: inset(80% 0 5% 0); } 80% { clip-path: inset(10% 0 70% 0); } 100% { clip-path: inset(30% 0 20% 0); } }
    @keyframes glitch-anim-2 { 0% { clip-path: inset(10% 0 60% 0); } 20% { clip-path: inset(30% 0 20% 0); } 40% { clip-path: inset(70% 0 10% 0); } 60% { clip-path: inset(20% 0 50% 0); } 80% { clip-path: inset(90% 0 5% 0); } 100% { clip-path: inset(50% 0 30% 0); } }
    .hero-subtitle { text-align: center; color: #00f3ff !important; font-size: 13px; letter-spacing: 5px; opacity: 0.9; margin-bottom: 30px; font-family: 'Orbitron', sans-serif !important; font-weight: 700; }
    
    .terminal-container { background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: 25px; border-radius: 8px; font-family: 'Orbitron', monospace; font-size: 13px; color: #e2e8f0; box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px; }
    .term-line { opacity: 0; margin-bottom: 5px; }
    .term-line:nth-child(1) { animation: scanFade 0.2s 0.2s forwards; }
    .term-line:nth-child(2) { animation: scanFade 0.2s 1.0s forwards; }
    .term-line:nth-child(3) { animation: scanFade 0.2s 1.8s forwards; }
    .term-line-main { opacity: 0; animation: scanFade 0.5s 2.6s forwards; }
    @keyframes scanFade { 0% { opacity: 0; transform: translateX(-10px); filter: blur(2px); } 100% { opacity: 1; transform: translateX(0); filter: blur(0); } }
    .cursor-blink { display: inline-block; width: 8px; height: 16px; background: #00f3ff; animation: blink 1s step-end infinite; vertical-align: middle; margin-left: 5px; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

    /* 输入框与按钮 */
    div[data-testid="stTextInput"] > div > div > input { background-color: rgba(2, 6, 23, 0.9) !important; color: #00f3ff !important; font-family: 'Orbitron', monospace !important; border: 1px solid rgba(0,243,255,0.5) !important; border-radius: 6px !important; text-align: center; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px; box-shadow: inset 0 0 15px rgba(0,243,255,0.1) !important; transition: all 0.3s ease; }
    div[data-testid="stTextInput"] > div > div > input:focus { border-color: #ffd700 !important; box-shadow: 0 0 20px rgba(255,215,0,0.3), inset 0 0 15px rgba(255,215,0,0.1) !important; }
    
    div[data-testid="stSelectbox"] > div > div { background-color: rgba(2, 6, 23, 0.9) !important; border: 1px solid rgba(168, 85, 247, 0.4) !important; color: #a855f7 !important; }

    div.stButton > button { background: #0f172a !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; border-left: 4px solid rgba(0, 243, 255, 0.6) !important; border-radius: 6px !important; min-height: 56px !important; width: 100% !important; padding: 10px 15px !important; text-align: left !important; box-shadow: 0 4px 10px rgba(0,0,0,0.4) !important; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important; }
    div.stButton > button p { color: #ffffff !important; font-size: 15px !important; line-height: 1.5 !important; font-weight: 500 !important; }
    div.stButton > button:hover { background: rgba(0, 243, 255, 0.15) !important; border-color: #00f3ff !important; border-left: 4px solid #00f3ff !important; box-shadow: 0 0 15px rgba(0,243,255,0.3) !important; transform: translateX(3px) !important; }
    div.stButton > button:active { transform: scale(0.98) !important; }
    
    div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #00f3ff, #0088ff) !important; border-left: none !important; text-align: center !important; }
    div.stButton > button[data-testid="baseButton-primary"] p { color: #030712 !important; font-weight: 900 !important; font-size: 16px !important; letter-spacing: 1px !important; }
    div.stButton > button[data-testid="baseButton-primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 0 30px rgba(0,243,255,0.6) !important; }
    
    div[data-testid="stDownloadButton"] > button { background: rgba(5, 10, 21, 0.95) !important; border: 1px dashed rgba(16, 185, 129, 0.6) !important; border-left: 4px solid #10b981 !important; text-align: center !important; margin-top: 15px;}
    div[data-testid="stDownloadButton"] > button p { color: #10b981 !important; font-family: 'Orbitron', monospace !important; font-weight: bold !important; letter-spacing: 1px !important;}
    div[data-testid="stDownloadButton"] > button:hover { background: rgba(16, 185, 129, 0.15) !important; box-shadow: 0 0 20px rgba(16,185,129,0.3) !important; transform: translateY(-2px) !important; }

    .cli-box { background: #000000; border: 1px solid #334155; border-left: 4px solid #00f3ff; padding: 20px; border-radius: 6px; font-family: 'Orbitron', monospace; font-size: 13px; color: #4ade80; box-shadow: inset 0 0 20px rgba(0,243,255,0.1); margin-top: 50px; text-transform: uppercase; word-break: break-all; }

    /* 结果大金卡 */
    .result-card { padding: 35px 20px; border-radius: 12px; background: rgba(11, 17, 32, 0.95) !important; border: 1px solid rgba(255,215,0,0.3); border-top: 5px solid #ffd700; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6); margin-bottom: 30px; position:relative; overflow:hidden;}
    .mbti-code { font-family: 'Orbitron', sans-serif !important; font-size: 72px; font-weight: 900; color: #ffd700 !important; line-height: 1.1; letter-spacing: 4px; text-shadow: 0 0 25px rgba(255,215,0,0.5); margin: 0;}
    .tier-badge { position: absolute; top: 15px; right: -30px; background: #ffd700; color: #000; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 11px; padding: 3px 30px; transform: rotate(45deg); z-index: 10; letter-spacing: 1px; box-shadow: 0 0 15px rgba(255,215,0,0.8);}

    /* 绝密档案折叠框 */
    [data-testid="stExpander"] { background: rgba(2, 6, 23, 0.8) !important; border: 1px solid rgba(244, 63, 94, 0.4) !important; border-radius: 8px !important; margin-bottom: 25px; }
    [data-testid="stExpander"] summary { color: #f43f5e !important; font-weight: 900 !important; font-size: 15px !important; padding: 5px 0 !important; }
    
    /* 任务行动板样式 */
    .mission-item { border-left: 3px solid #f43f5e; padding-left: 15px; margin-bottom: 12px; background: rgba(244,63,94,0.05); padding-top: 10px; padding-bottom: 10px; border-radius: 0 4px 4px 0; }
    
    [data-testid="stTabs"] button { color: #94a3b8 !important; font-family: 'Noto Sans SC', sans-serif !important; font-weight: bold !important; font-size: 15px !important; padding-bottom: 10px !important; }
    [data-testid="stTabs"] button[aria-selected="true"] { color: #00f3ff !important; border-bottom-color: #00f3ff !important; text-shadow: 0 0 10px rgba(0,243,255,0.5); }
    
    [data-testid="stCodeBlock"] { border-radius: 8px !important; margin-top: 10px; }
    [data-testid="stCodeBlock"] > div { background-color: rgba(5, 10, 21, 0.95) !important; border: 1px solid rgba(0, 243, 255, 0.4) !important; border-radius: 8px !important; box-shadow: inset 0 0 20px rgba(0, 243, 255, 0.1) !important; }
    [data-testid="stCodeBlock"] pre, code { color: #e2e8f0 !important; font-family: 'Noto Sans SC', monospace !important; font-size: 13px !important; line-height: 1.6 !important; white-space: pre-wrap !important; }
    [data-testid="stCodeBlock"] button { background-color: rgba(2, 6, 23, 0.9) !important; border: 1px solid rgba(0, 243, 255, 0.4) !important; border-radius: 4px !important; opacity: 1 !important; transition: all 0.3s ease !important; }
    [data-testid="stCodeBlock"] button:hover { background-color: rgba(0, 243, 255, 0.2) !important; border-color: #00f3ff !important; transform: scale(1.05) !important; }
    [data-testid="stCodeBlock"] button svg { fill: #00f3ff !important; stroke: #00f3ff !important; }

    .firework-center { position: fixed; top: 50%; left: 50%; z-index: 99998; pointer-events: none; font-weight: 900; font-family: 'Orbitron', sans-serif; color: #00f3ff; text-shadow: 0 0 20px #00f3ff, 0 0 30px #ffffff; animation: supernova 1.8s cubic-bezier(0.1, 0.9, 0.2, 1) forwards;}
    @keyframes supernova { 0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; } 100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; filter: blur(2px);} }
</style>
""", unsafe_allow_html=True)

def trigger_supernova():
    html_str = ""
    for _ in range(35): 
        tx, ty = random.uniform(250, 900) * math.cos(random.uniform(0, 2 * math.pi)), random.uniform(250, 900) * math.sin(random.uniform(0, 2 * math.pi))
        html_str += f'<div class="firework-center" style="--tx:{tx}px; --ty:{ty}px; --s:{random.uniform(1.0, 3.0)}; --rot:{random.randint(-360, 360)}deg; animation-delay:{random.uniform(0, 0.15)}s; font-size:{random.randint(12, 22)}px;">{random.choice(["DATA", "SDE", "NODE", "HASH", "ASSET", "SYNC"])}</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 深度定制 SDE 业务语境题库 ---
questions = [
    {"q": "推动数商入场时，我倾向于亲自拜访机构进行面对面沟通，而非仅在线上发送标准入驻指引。", "dim": "E"},
    {"q": "代表数据交易所参与行业峰会，发表演讲并扩大 SDE 的市场影响力，会让我充满能量。", "dim": "E"},
    {"q": "面对复杂的数据跨境业务闭环，我更喜欢召集跨部门进行“头脑风暴”，而非独自撰写可行性报告。", "dim": "E"},
    {"q": "我习惯于维护庞大的政企及数商合作网络，并定期主动对接，挖掘潜在的数据产品挂牌机会。", "dim": "E"},
    {"q": "当市场上出现关于公共数据授权运营的新政策，我会立刻在工作群内发起热烈讨论。", "dim": "E"},
    {"q": "在策划年度数据要素生态大会时，我发现与团队高频互动能激发出更多的创新赛道灵感。", "dim": "E"},
    {"q": "处理突发的客户舆情或合作方分歧时，我倾向于立刻拉通会议快速当面（或语音）对齐解决，而非文字往来。", "dim": "E"},
    {"q": "我能极好地适应高频率的商务洽谈和路演活动，并认为这是活跃数据交易市场的核心动作。", "dim": "E"},
    {"q": "相比于坐在工位上独自研究定价模型，我更向往去各省市的大数据中心及数商企业实地调研交流。", "dim": "E"},
    {"q": "我坚信推动数据流通的最大阻力往往源于“信任缺失”，而建立信任最好的方式是高频的线下人际交互。", "dim": "E"},
    {"q": "在评估一项数据资产入表案例时，我会死磕财务科目映射、摊销年限与合规确权等底层细节。", "dim": "S"},
    {"q": "我更信任交易大盘上的真实成交曲线与存证笔数，而不是研究报告中那些定性的宏观趋势预判。", "dim": "S"},
    {"q": "当听到“隐私计算”、“可信数据空间”等前沿概念时，我最先关心的是它在 SDE 现有机房和架构里如何具体落地。", "dim": "S"},
    {"q": "我认为数据交易所当前最核心的任务是把“确权、存证、交付、清算”的每一个动作做到极致的规范与零差错。", "dim": "S"},
    {"q": "审核数据产品上架时，我严格依赖合规审查操作清单，极度排斥带有主观弹性的价值评估。", "dim": "S"},
    {"q": "相比于畅想 2030 年国家级数据大市场的宏伟蓝图，我更关心下个季度的结算系统并发量和撮合效率能否提升。", "dim": "S"},
    {"q": "撰写业务汇报时，我习惯于堆叠详实的交易对比数据和案例证据，极少使用天马行空的产业战略隐喻。", "dim": "S"},
    {"q": "面对复杂的场内交易规则与法律文本，我总能像“排雷”一样敏锐捕捉到可能导致实操卡壳的具体措辞隐患。", "dim": "S"},
    {"q": "我偏好有明确时间节点的阶段性交付成果，即使它只是交易系统后台一个字段的微小改良。", "dim": "S"},
    {"q": "我认为现阶段数据要素市场的建设，最缺的是脚踏实地的“施工图”，而不是天花乱坠的“概念图”。", "dim": "S"},
    {"q": "即使某个数据产品能带来巨大的短期交易额，只要被我发现存在合规硬伤或溯源不清，我也会毫不犹豫按下终止键。", "dim": "T"},
    {"q": "在评选“年度优秀数商”时，我主张完全依靠交易贡献度等客观算法指标，剔除任何行业人情和生态扶持的主观分。", "dim": "T"},
    {"q": "面对前线业务部门抱怨合规流程过于繁琐，我会列举法律底线直接回绝，认为交易所的红线不容人情变通。", "dim": "T"},
    {"q": "当下属在确权或存证操作中出现失误，我会直接指出其操作逻辑的谬误，认为这种单刀直入才是最高效的沟通。", "dim": "T"},
    {"q": "我坚信通过智能合约、自动风控等技术手段替代人工审核，是确保数据交易平台绝对公平与廉洁的唯一途径。", "dim": "T"},
    {"q": "处理数商之间的数据质量交易纠纷时，我只看客观的 API 调用日志和质量检测报告，不考虑双方的情绪诉求。", "dim": "T"},
    {"q": "在跨部门平台资源争夺中，我倾向于寻找“投入产出比”（ROI）最优的数学解，而非努力寻求各方心理的平衡。", "dim": "T"},
    {"q": "合规与风控人员应当像法官一样保持绝对的理智克制，决不能被外界疯狂的数据炒作热潮所干扰。", "dim": "T"},
    {"q": "当公司推行一项新的管理或考核制度，我首先审查其逻辑是否严密、标准是否可量化，而非员工的第一情感接受度。", "dim": "T"},
    {"q": "我认为数据交易所的核心护城河是“严密的规则体系与技术底座”，而非“温情脉脉的商业客情关系”。", "dim": "T"},
    {"q": "在主导大型数据创新项目（如新版交易大盘上线）前，我会建立极其严密的倒排计划表，非常反感进度失去控制。", "dim": "J"},
    {"q": "我的云盘文件夹、数据资产文档拥有严丝合缝的分类与命名逻辑，任何文件乱放都会让我感到极度不适。", "dim": "J"},
    {"q": "如果一场跨部门业务讨论会没有形成明确的会议纪要、SOP决议和责任人，我会认为这是在严重浪费时间。", "dim": "J"},
    {"q": "我倾向于在系统开发初期就锁定所有的核心业务需求，对中途频繁变更“数据产品业务形态”持强烈排斥态度。", "dim": "J"},
    {"q": "即便面临极高压的交易旺季，我也坚持每天下班前进行工作复盘，并雷打不动地更新第二天的待办任务清单。", "dim": "J"},
    {"q": "数据交易所的日常运营应当“重制度设计、轻即兴发挥”，哪怕这会让我们在应对短期市场热点时显得不够快。", "dim": "J"},
    {"q": "我几乎从不拖延核心审批或交付任务，因为“未决事项”停留在待办清单上，会带给我无形的心理重压。", "dim": "J"},
    {"q": "我更喜欢规则清晰、节奏稳定、可预测的工作环境，而不是每天都在“救火”和处理无法预知的突发创新需求。", "dim": "J"},
    {"q": "为了确保向上级或监管交付的数据分析报告万无一失，我总是会刻意提前预留出至少 20% 的缓冲检查时间。", "dim": "J"},
    {"q": "面对多线并行的复杂任务（如同时筹备路演与审核规则），我必须先向领导确认优先级并排好序，否则绝对无法安心执行。", "dim": "J"}
]

# --- 4. 史诗级进化大厂数据库 (新增算力、评级、任务、致命漏洞) ---
mbti_details = {
    "INTJ": {"role": "首席数据架构师", "tier": "UR", "tier_color": "#ff003c", "base_hash": 9850, "desc": "数据要素底座的“造物主”，致力于为错综复杂的数字经济构建严密的底层制度与逻辑规则。", "tags": ["顶层设计", "逻辑闭环", "制度自信"], "advice": "为前台预留沙盒容错空间，适度妥协以换取业务推进速度。", "tasks": ["主导 SDE 核心确权底层逻辑架构设计", "重构下一代高并发撮合交易引擎逻辑"], "black_swan": "过度追求底层架构完美闭环。面临突发政策转向时，系统极易因过于重型而无法敏捷掉头。"},
    "INTP": {"role": "量化风控专家", "tier": "SSR", "tier_color": "#ffd700", "base_hash": 9620, "desc": "穿透数据迷雾，寻找复杂业务表象下的底层逻辑漏洞与确权定价模型的最优解。", "tags": ["深度解构", "模型驱动", "极客思维"], "advice": "尝试将高维理论模型降维封装为傻瓜式的《业务操作指南》。", "tasks": ["研发基于特征因子的数据资产动态定价算法", "建立实时数据异常交易嗅探与阻断模型"], "black_swan": "陷入“分析瘫痪”。在需要极速拍板的确权灰度地带，过度追求模型最优解往往导致商机流失。"},
    "ISTJ": {"role": "合规审查主理官", "tier": "SR", "tier_color": "#a855f7", "base_hash": 8850, "desc": "SDE 底层防线的守夜人，您的评估本身就是安全、严谨与业务零失误的代名词。", "tags": ["绝对合规", "程序正义", "风险兜底"], "advice": "在死守红线的同时，试着用“如何合规地上架”来逆向指导前线业务。", "tasks": ["主导头部数商“数据资产入表”全链路审计", "设计业务合同与智能合约的合规映射SOP"], "black_swan": "过度依赖既有 SOP。面临无先例创新业务时，容易因“无库可查”产生本能的排斥与误杀。"},
    "ESTJ": {"role": "核心业务统筹官", "tier": "SSR", "tier_color": "#ffd700", "base_hash": 9500, "desc": "无可争议的推进器，擅长将国家宏观政策拆解为团队可绝对执行的 KPI 矩阵。", "tags": ["强效统帅", "结果导向", "流程大师"], "advice": "下发高压指令时适度释放情绪价值，信任感往往比指标走得更远。", "tasks": ["发起并统筹 SDE 年度交易额破局百亿攻坚战", "强力调度跨部门资源打通确权交易清算堵点"], "black_swan": "KPI压倒一切导致“团队算力过载”。强推项目时易忽视一线团队的情绪阈值，引发内耗。"},
    "INFJ": {"role": "产业生态智囊", "tier": "UR", "tier_color": "#ff003c", "base_hash": 9200, "desc": "具备极强的跨频段共情能力，能精准预判数据流转对未来实体经济产生的深远变革。", "tags": ["远见卓识", "使命驱动", "战略前瞻"], "advice": "学会用精确的财务测算来锚定您的产业愿景，提升落地说服力。", "tasks": ["规划 SDE 未来五年在实体经济的数据赋能版图", "发起“数据向善”及社会公益数据要素流通倡议"], "black_swan": "强烈的战略直觉若缺乏硬核量化数据支撑，向实干型领导汇报时极易被贴上“不切实际”标签。"},
    "INFP": {"role": "生态价值主张官", "tier": "SR", "tier_color": "#a855f7", "base_hash": 8650, "desc": "冷酷数据背后的灵魂捕捉者，擅长在机械的交易网络中注入引人共鸣的生态文化。", "tags": ["价值感召", "组织粘合", "品牌定调"], "advice": "学会熟练利用预算工具和业务导向来捍卫您的核心价值主张。", "tasks": ["重塑 SDE 在数据交易领域的全球品牌叙事", "实施内部文化与跨部门协作协同凝聚力工程"], "black_swan": "在跨部门冷酷的算力与预算博弈中，容易因厌恶冲突而退缩，导致核心价值观无法落地。"},
    "ENTJ": {"role": "战略开拓领军人", "tier": "UR", "tier_color": "#ff003c", "base_hash": 9900, "desc": "天生的矩阵建设者，在数据跨境、公共数据授权等探索区中展现极强的破局能力。", "tags": ["开疆拓土", "战略铁腕", "极致破局"], "advice": "极速开疆拓土时，放慢半拍听听合规风控预警能避开隐蔽风险。", "tasks": ["主导“公共数据授权运营”省级破冰与资源抢占", "制定并执行跨链互认及全国数据大市场吞并战略"], "black_swan": "狂飙突进时的风控盲区。在极速吞并外部资源时极易因忽视底层合规红线而触发监管熔断。"},
    "ENTP": {"role": "模式创新顾问", "tier": "SSR", "tier_color": "#ffd700", "base_hash": 9400, "desc": "传统交易规则的敏锐挑战者，致力于通过跨界思维寻找下一代数据资产流转范式。", "tags": ["范式重构", "逻辑激辩", "思维跳跃"], "advice": "收敛发散思维，选择一个极具潜力的创新点深度闭环至最终交付。", "tasks": ["研发首个基于 Web3 的新型数据要素凭证通证", "在监管沙盒内主导蓝海型数字产品变现测试"], "black_swan": "无限发散思维导致的交付烂尾。若缺乏强力的落地跟进节点，极易沦为纯粹的纸上谈兵。"},
    "ENFJ": {"role": "数商生态总监", "tier": "SSR", "tier_color": "#ffd700", "base_hash": 9350, "desc": "数据交易所的枢纽中心，能通过卓越的共识构建能力将多方利益竞争者聚拢为盟友。", "tags": ["关系枢纽", "温情领导力", "利益协同"], "advice": "协调利益分配时，大胆引入客观的量化算法确保绝对的规则底座。", "tasks": ["构建辐射全国的 SDE 头部数商与第三方服务联盟", "维稳数据要素多边市场，调解核心生态伙伴冲突"], "black_swan": "对生态伙伴过度包容。处理违规事件时容易被“人情”裹挟，从而损害交易所的绝对中立性。"},
    "ENFP": {"role": "平台资源布道大使", "tier": "SR", "tier_color": "#a855f7", "base_hash": 8900, "desc": "充满感染力的生态火苗，让每一场路演与推介都变成数据要素市场的狂热共识。", "tags": ["无限创意", "跨界纽带", "高频驱动"], "advice": "引入严密的商机里程碑管理，将创意转化为可追踪的业务漏斗。", "tasks": ["领衔 SDE 全国核心城市业务路演与生态宣发大循环", "策划并主持面向千家数商的“数据赋能创新工坊”"], "black_swan": "缺乏结构化数据追踪。路演现场火热但无法转化为 CRM 里的真实入驻率，商业核算价值打折。"},
    "ISFJ": {"role": "清结算运营中枢", "tier": "R", "tier_color": "#3b82f6", "base_hash": 8200, "desc": "最坚韧的底层支点，通过极致纠错与细节控场支撑起整个平台的专业信誉与高吞吐。", "tags": ["极致支撑", "服务巅峰", "高可用节点"], "advice": "在完美支撑中后台运转之余，尝试主动提出冗余流程的优化提案。", "tasks": ["保障全天候撮合及大额资金清结算体系 0 宕机", "极速响应并闭环处理生态节点与数商的底层工单"], "black_swan": "默默承受过载的技术债。不善于向上抗议，可能在交易洪峰期因人工审核量爆表而面临崩溃。"},
    "ESFJ": {"role": "政企商务枢纽", "tier": "SR", "tier_color": "#a855f7", "base_hash": 8750, "desc": "超级连接器，擅长经营多维度的外部政企生态关系，是前线业务部门的最强润滑剂。", "tags": ["协作典范", "客情控制", "社会化支撑"], "advice": "在照顾合作方诉求的同时，保持对 SDE 机构红线的绝对清醒。", "tasks": ["高频维护国家部委及地方大数据局的核心 G 端客情", "统筹落地具有全国影响力的年度数据要素高峰论坛"], "black_swan": "过度满足多方诉求导致的边界失守。极易因“谁都想讨好”而签下严重偏离平台底线的协议。"},
    "ISTP": {"role": "平台风控与排障专家", "tier": "SR", "tier_color": "#a855f7", "base_hash": 8950, "desc": "数据底座的实干派，只对逻辑代码负责，是大并发故障或危机时的定海神针。", "tags": ["极简实干", "故障排查", "硬核运维"], "advice": "将内隐的排查经验强制沉淀为可视化的《应急响应标准手册》。", "tasks": ["执行 SDE 核心交易链路的灾备拉起与物理级排障", "在不影响前台撮合的前提下执行底层架构高危热更新"], "black_swan": "技术彻底黑盒化。过度依赖个人的“极客直觉”排障，一旦休假离线会导致整个系统应急瘫痪。"},
    "ISFP": {"role": "资产交互体验官", "tier": "R", "tier_color": "#3b82f6", "base_hash": 8150, "desc": "赋予枯燥数据以美学权重，致力于提升数字资产在终端大屏展示时的绝对视觉专业质感。", "tags": ["审美溢价", "感官叙事", "体验极致"], "advice": "增加对核心交易协议的理解，让作品拥有直击商业痛点的穿透力。", "tasks": ["重构 SDE 实时交易大盘的动态数据全息视觉渲染", "主导面向数商终端的 UI/UX 操作流敏捷体验升级"], "black_swan": "陷入纯粹形式主义。设计出极其炫酷的大屏，却完全脱离了“数据确权撮合”的核心商业逻辑。"},
    "ESTP": {"role": "前沿敏捷先锋", "tier": "SSR", "tier_color": "#ffd700", "base_hash": 8800, "desc": "数据流通一线的敏锐猎手，能极快捕捉到瞬息万变的市场红利与应用空间的套利机会。", "tags": ["市场直觉", "敏捷收割", "实战专家"], "advice": "在展现高效行动力促成交易时，务必将前置合规审查纳入标准化操作。", "tasks": ["敏锐收割新政策出台后的第一波“短期数据流通红利”", "针对区域内竞所的市场抢夺发起极速实战反制突击"], "black_swan": "为了极速促成首单，倾向于利用捷径绕过繁琐的合规防火墙，一旦溯源出瑕疵将面临毁灭性反噬。"},
    "ESFP": {"role": "官方品牌发声信标", "tier": "SR", "tier_color": "#a855f7", "base_hash": 8300, "desc": "交易所的前台形象窗口，天生具备将复杂的《数据二十条》解码为大众传播话术的超级天赋。", "tags": ["全域表现", "舆情响应", "公关信标"], "advice": "深潜研究政策红头文件，将绝佳表现力建立在扎实的产业根基上。", "tasks": ["在全网引爆 SDE 最新明星数据产品的展会级宣发流量", "冲在第一线对冲平台突发的负面市场舆情并进行柔性公关"], "black_swan": "由于对底层法律条款理解深度不够，对外大范围宣发时极易出现“用词越界”，引发监管舆情风险。"}
}

# 🤝 协同算法引擎
def calculate_synergy(mbti1, mbti2):
    diff = sum(1 for a, b in zip(mbti1, mbti2) if a != b)
    if diff == 0: return 92, "【绝对镜像】决策回路高度一致，沟通0延迟，但需警惕认知盲区严重重叠导致翻车。"
    elif diff == 1: return 98, "【黄金握手】核心逻辑一致且具备极佳微调互补性，堪称 SDE 最强业务推土机小队！"
    elif diff == 2: return 85, "【灰度平衡】思维角度存在差异，能通过激烈碰撞打磨出更抗风险、更完美的业务闭环。"
    elif diff == 3: return 65, "【高频摩擦】存在极大的底层通信壁垒，协同作业时必须强制引入第三方确立明确的中间缓冲协议。"
    else: return 99, "【极致阴阳反转】代码完全相反！在日常沟通中极度痛苦，但若各司其职背靠背，能实现无死角的全域战略包抄！"

# --- 5. 极速状态机 ---
for key, init_val in [('started', False), ('current_q', 0), ('start_time', None), ('end_time', None), ('calculating', False), ('user_alias', "SDE_NODE"), ('total_scores', {"E": 0, "S": 0, "T": 0, "J": 0}), ('firework_played', False)]:
    if key not in st.session_state: st.session_state[key] = init_val

def start_assessment_callback():
    alias = st.session_state.login_input.strip()
    st.session_state.user_alias = html.escape(alias) if alias else "SDE_NODE"
    st.session_state.started = True; st.session_state.start_time = time.time()
def answer_callback(val, dim):
    st.session_state.total_scores[dim] += (val - 3); st.session_state.current_q += 1
    if st.session_state.current_q >= len(questions):
        st.session_state.end_time = time.time(); st.session_state.calculating = True

# --- 6. 核心渲染路由 ---
if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""<div style="text-align: center; margin-bottom: 20px;"><h1 class="hero-title" data-text="上海数据交易所">上海数据交易所</h1><br><h1 class="hero-title" data-text="算力实战仪表盘" style="font-size:32px !important;">算力实战仪表盘</h1><div class="hero-subtitle">▶ SDE MATRIX V1.0_ENTERPRISE</div></div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class='terminal-container'>
        <div class='term-line'><span style='color:#94a3b8;'>[SYSTEM]</span> Establishing secure connection to SDE Core...</div>
        <div class='term-line'><span style='color:#94a3b8;'>[SYSTEM]</span> Loading Talent Capability Algorithm... <span style='color:#00f3ff;'>[OK]</span></div>
        <div class='term-line-main'>
            <span style='color:#ffffff; font-size: 15px; font-family: "Noto Sans SC", sans-serif; line-height: 1.8;'>
            <br><b>2026年是数据要素价值释放的突破之年。</b><br><br>
            在“数据乘数”加速赋能实体经济的当下，本终端将全方位扫描您的职场决策链路与风控模型。<br>
            您的物理能力将被<b>「全息资产化」</b>，系统将为您生成独一无二的<b>高阶数字凭证与上链算力估值</b>。</span>
            <span class="cursor-blink"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.form(key="login_form", border=False):
        st.markdown("<div style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:bold; margin-bottom:8px; text-align:center;'>▼ MOUNT NODE ALIAS (输入职场称呼 / 授权代号) ▼</div>", unsafe_allow_html=True)
        st.text_input("", key="login_input", placeholder="例如： Compliance_Wu", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        st.form_submit_button("▶ 授予系统权限并提取算力资产", on_click=start_assessment_callback, type="primary", use_container_width=True)

elif st.session_state.calculating:
    # 🔥 王炸功能 1：极具逼格的终端数据上链动画
    st.markdown("<h2 class='hero-title' data-text='[ MINTING TO SDE CHAIN ]' style='font-size:28px !important; margin-top:50px;'>[ MINTING TO SDE CHAIN ]</h2>", unsafe_allow_html=True)
    mint_box = st.empty()
    hash_logs = ""
    for _ in range(12):
        fake_hash = hashlib.sha256(str(random.random()).encode()).hexdigest().upper()
        hash_logs = f"<span style='color:#94a3b8;'>[TX_HASH]</span> <span style='color:#ffd700;'>0x{fake_hash}</span> <span style='color:#10b981;'>[CONFIRMED]</span><br>" + hash_logs
        mint_box.markdown(f"<div class='cli-box' style='font-size:11px; height:220px; overflow:hidden; border-color:#ffd700;'>{hash_logs}</div>", unsafe_allow_html=True)
        time.sleep(0.12)
    st.session_state.calculating = False; st.rerun()

elif st.session_state.current_q < len(questions):
    q_data = questions[st.session_state.current_q]
    dim_map = {"E": "[生态交互] 外部联结协同 vs 内部深潜研判", "S": "[感知落地] 颗粒实务穿透 vs 宏观战略推演", "T": "[量化风控] 客观逻辑刚性 vs 生态人际共情", "J": "[秩序治理] 制度架构锚定 vs 敏捷响应沙盒"}
    module_name = dim_map.get(q_data['dim'])
    dynamic_hash = hashlib.sha256(f"BLOCK_{st.session_state.current_q}_{q_data['q']}".encode()).hexdigest()[:10].upper()
    
    st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
    progress_val = (st.session_state.current_q + 1) / len(questions); st.progress(progress_val)
    st.markdown(f"<div style='text-align:right; font-family:Orbitron, monospace; color:#00f3ff; font-size:12px; margin-top:5px;'>MINTING PROCESS: {int(progress_val*100)}%</div>", unsafe_allow_html=True)
    
    st.markdown(f"""<div style='background: rgba(2, 6, 23, 0.85); border: 1px solid rgba(0, 243, 255, 0.4); border-radius: 6px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 15px rgba(0, 243, 255, 0.05); margin-top: 15px; margin-bottom: 25px; border-left: 5px solid #00f3ff;'><div style='display:flex; justify-content:space-between; font-family:monospace; color:#00f3ff; font-size:12px; margin-bottom:15px; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom:10px;'><span class='orbitron-font'>SYS_MOD: {module_name}</span><span class='orbitron-font'>HASH: 0x{dynamic_hash}</span></div><div style='font-size: 16px; color: #ffffff !important; line-height: 1.7; font-weight: 500;'>{q_data['q']}</div></div>""", unsafe_allow_html=True)
    
    opts = [("❌ [ 极度排斥 ] 强制阻断：完全背离我的工作直觉", 1), ("⚠️ [ 较少符合 ] 弱态耦合：仅在特定场景下采用", 2), ("⚖️ [ 中立待定 ] 视境判定：完全视具体业务环境而定", 3), ("🤝 [ 比较符合 ] 逻辑握手：是常用的业务决策链路", 4), ("🔒 [ 绝对锁定 ] 完美同步：完美复刻核心工作思维", 5)]
    for text, val in opts: st.button(text, type="secondary", key=f"q_{st.session_state.current_q}_{val}", on_click=answer_callback, args=(val, q_data['dim']))

else:
    if not st.session_state.firework_played: trigger_supernova(); st.session_state.firework_played = True
        
    res = st.session_state.total_scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    data = mbti_details.get(mbti)
    safe_alias_final, role_name, tier_level, tier_color = st.session_state.user_alias.upper(), data['role'], data['tier'], data['tier_color']
    
    def get_intensity(score): return int(max(15, min(100, 50 + (score * 2.5))))
    val_E, val_I = get_intensity(res["E"]), 100 - get_intensity(res["E"])
    val_S, val_N = get_intensity(res["S"]), 100 - get_intensity(res["S"])
    val_T, val_F = get_intensity(res["T"]), 100 - get_intensity(res["T"])
    val_J, val_P = get_intensity(res["J"]), 100 - get_intensity(res["J"])

    categories = ['生态协同(E)', '颗粒实勘(S)', '量化风控(T)', '架构秩序(J)', '底层深潜(I)', '战略前瞻(N)', '生态共情(F)', '敏捷演进(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]

    p_score, s_score = -res.get("J", 0), res.get("S", 0)
    risk_score = int(max(5, min(95, 50 + (p_score * 1.5) - (s_score * 1.5))))
    if risk_score < 35: r_tag, r_color, r_desc = "底线合规与安全装甲", "#10b981", "对合规红线有天然敬畏，极其适合把守数据存证大门。"
    elif risk_score < 65: r_tag, r_color, r_desc = "动态演进与边界平衡", "#ffd700", "能够在监管锁死与商业吞吐间寻求黄金平衡接口。"
    else: r_tag, r_color, r_desc = "无界扩张与前沿破局", "#f43f5e", "拥有极高爆发性的业务创新能力，能极速抢占新兴赛道。"

    time_taken = max(1, st.session_state.end_time - st.session_state.start_time)
    hash_code = hashlib.sha256(f"{safe_alias_final}{mbti}{time_taken}".encode()).hexdigest()[:16].upper()
    block_height = f"8,{(int(time.time()) % 1000000):06d}"
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    # 🔥 王炸 2 & 3：计算果断度指数与算力链上估值
    avg_q_time = time_taken / len(questions)
    decisiveness = int(min(99, max(35, 100 - (max(0, avg_q_time - 2.5) * 5))))
    extremity_score = sum(abs(v) for v in res.values()) / 40.0
    h_int = int(hash_code[:8], 16)
    random_factor = 0.9 + (h_int % 200) / 1000.0
    asset_valuation = int(data['base_hash'] * (1 + extremity_score * 0.4) * (0.8 + (decisiveness/100.0) * 0.5) * random_factor * 10000)
    valuation_str = f"{round(asset_valuation, -4):,}"
    
    # 部门协同指数
    syn_tech = min(98, max(20, (85 if 'T' in mbti else 60) + (10 if 'N' in mbti else 0) + (h_int % 15) - 7))
    syn_biz = min(98, max(20, (85 if 'E' in mbti else 60) + (10 if 'P' in mbti else 0) + ((h_int >> 4) % 15) - 7))
    syn_comp = min(98, max(20, (85 if 'J' in mbti else 60) + (10 if 'S' in mbti else 0) + ((h_int >> 8) % 15) - 7))

    # =========================================================================
    # ✨✨ 核心面板区 ✨✨
    # =========================================================================
    st.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 15px; border-radius: 8px; margin-bottom: 25px; display: flex; align-items: center; box-shadow: 0 0 15px rgba(16,185,129,0.2);">
        <div style="font-size: 24px; margin-right: 15px;">✅</div>
        <div>
            <div style="color: #10b981; font-weight: bold; font-size: 14px; margin-bottom: 3px;">算力节点图谱已完成 SDE 链上确权存证</div>
            <div style="color: #94a3b8; font-family: 'Orbitron', monospace; font-size: 11px;">区块高度: #{block_height} | 存证时间: {current_time_str}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
        <div class="tier-badge" style="background: {tier_color}; box-shadow: 0 0 15px {tier_color}88;">{tier_level}</div>
        <div class="orbitron-font" style="font-size:13px; color:#94a3b8; letter-spacing:4px; margin-bottom:15px;">SDE CORE NODE DECODED</div>
        <div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:13px; margin-bottom:5px; border-bottom:1px dashed #334155; padding-bottom:10px; display:inline-block;">AUTH_NODE: {safe_alias_final}</div>
        <div class="mbti-code" style="margin-top:10px;">{mbti}</div>
        <div style="font-size: 20px; font-weight: 900; color: #00f3ff !important; margin: 10px 0 15px 0; letter-spacing: 1px;">【 {role_name} 】</div>
        <div style="color:#e2e8f0 !important; font-size:14px; line-height:1.8; margin-bottom:15px; font-weight:400; text-align:left; padding:0 5px;">{data['desc']}</div>
        <div>{" ".join([f'<span style="background:rgba(0, 243, 255, 0.1); color:#00f3ff !important; border:1px solid rgba(0,243,255,0.4); padding:4px 10px; border-radius:4px; font-size:12px; font-weight:700; margin:4px; display:inline-block; font-family:\'Noto Sans SC\', sans-serif;">{t}</span>' for t in data['tags']])}</div>
        
        <div style="display:flex; justify-content:space-between; margin-top:25px; gap:10px;">
            <div style="flex:1; background:rgba(0,0,0,0.6); border:1px solid rgba(255,215,0,0.3); border-radius:8px; padding:15px; text-align:center;">
                <div style="font-size:10px; color:#94a3b8; font-family:'Orbitron', monospace; margin-bottom:4px;">ASSET VALUATION (SDE)</div>
                <div style="font-size:22px; color:#ffd700; font-weight:900; font-family:'Orbitron', sans-serif; text-shadow:0 0 10px rgba(255,215,0,0.6);">💎 {valuation_str}</div>
            </div>
            <div style="flex:1; background:rgba(0,0,0,0.6); border:1px solid rgba(0,243,255,0.3); border-radius:8px; padding:15px; text-align:center;">
                <div style="font-size:10px; color:#94a3b8; font-family:'Orbitron', monospace; margin-bottom:4px;">DECISIVENESS INDEX</div>
                <div style="font-size:22px; color:#00f3ff; font-weight:900; font-family:'Orbitron', sans-serif; text-shadow:0 0 10px rgba(0,243,255,0.6);">⚡ {decisiveness}/100</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 🔥 王炸 4：黑天鹅漏洞预警 (折叠面板，极具专业压迫感)
    with st.expander("⚠️ 绝密档案：系统盲点与黑天鹅压力测试 (仅本人可见)"):
        st.markdown(f"""
        <div style='padding: 5px 10px; font-size: 14px; color: #cbd5e1; line-height: 1.7;'>
            <div style='color: #f43f5e; font-weight: 900; font-size: 15px; margin-bottom: 8px; border-left: 3px solid #f43f5e; padding-left: 10px;'>[ 致命漏洞判定 ]</div>
            <div style='margin-bottom: 20px; padding-left: 13px;'>{data['black_swan']}</div>
            <div style='color: #10b981; font-weight: 900; font-size: 15px; margin-bottom: 8px; border-left: 3px solid #10b981; padding-left: 10px;'>[ 官方防狱补丁 ]</div>
            <div style='padding-left: 13px;'>{data['advice']}</div>
        </div>
        """, unsafe_allow_html=True)

    # 🔥 王炸 5：核心行动指令 & 跨节点协作沙盘
    st.markdown("<h4 style='color:#f43f5e !important; border-left:4px solid #f43f5e; padding-left:10px; font-weight:900; margin-top:30px;'>🎯 核心战略行动指令</h4>", unsafe_allow_html=True)
    tasks_html = "".join([f"<div class='mission-item'><span style='color:#e2e8f0; font-size:14px; font-weight:bold;'>{t}</span></div>" for t in data['tasks']])
    st.markdown(f"""
    <div style="background: rgba(244,63,94,0.05); border: 1px solid rgba(244,63,94,0.3); border-radius: 8px; padding: 20px; margin-bottom: 30px;">
        <div style="color: #f43f5e; font-family: 'Orbitron', sans-serif; font-size: 11px; letter-spacing: 2px; margin-bottom: 15px; border-bottom: 1px dashed rgba(244,63,94,0.3); padding-bottom: 10px;">/// TOP SECRET DIRECTIVES ///</div>
        {tasks_html}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='color:#a855f7 !important; border-left:4px solid #a855f7; padding-left:10px; font-weight:900;'>🤝 跨域算力协同沙盘</h4>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:10px;'>输入同事或领导的标识架构，模拟你们的职场协同匹配度：</div>", unsafe_allow_html=True)
    
    partner_mbti = st.selectbox("🎯 挂载目标协作节点:", options=list(mbti_details.keys()), index=list(mbti_details.keys()).index("ESTJ"), label_visibility="collapsed")
    syn_score, syn_desc = calculate_synergy(mbti, partner_mbti)
    st.markdown(f"""
    <div style="background: rgba(168,85,247,0.1); border: 1px solid rgba(168,85,247,0.4); padding: 20px; border-radius: 8px; margin-bottom:30px; text-align:center; box-shadow: 0 0 20px rgba(168,85,247,0.1);">
        <div style="font-family:'Orbitron', sans-serif; color:#a855f7; font-size:12px; font-weight:bold; margin-bottom:10px; letter-spacing: 2px;">[ CO-OP SYNERGY RATE ]</div>
        <div style="font-family:'Orbitron', sans-serif; font-size:48px; font-weight:900; color:#fff; text-shadow:0 0 25px rgba(168,85,247,0.8); margin-bottom:15px;">{syn_score}%</div>
        <div style="color:#e2e8f0; font-size:14px; font-weight:bold; line-height:1.6;">{syn_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🕸️ 核心算力拓扑矩阵</h4>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.1)', line=dict(color='rgba(0, 243, 255, 0.2)', width=8), hoverinfo='none'))
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=2.5), marker=dict(color='#ff003c', size=6, symbol='diamond')))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC, sans-serif", color='#e2e8f0', size=12), linecolor='rgba(0,243,255,0.2)', gridcolor='rgba(0,243,255,0.15)')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=55, r=55, t=30, b=30), height=350)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🎛️ 风控过载阈值仪</h4>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-size:16px; font-weight:bold; color:{r_color}; font-family:Noto Sans SC; margin-top: 15px;'>{r_tag}</div>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=risk_score, number={'suffix': "%", 'font': {'family': 'Orbitron, sans-serif', 'color': r_color, 'size': 42}}, gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155"}, 'bar': {'color': r_color}, 'bgcolor': "rgba(255,255,255,0.05)", 'steps': [{'range': [0, 35], 'color': "rgba(16, 185, 129, 0.15)"}, {'range': [35, 65], 'color': "rgba(255, 215, 0, 0.15)"}, {'range': [65, 100], 'color': "rgba(244, 63, 94, 0.15)"}]}))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#94a3b8"}, height=240, margin=dict(l=30, r=30, t=10, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

    # =========================================================================
    # ✨✨ 6. 海报提取 & 极客 JSON 档案下载 ✨✨
    # =========================================================================
    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900; margin-top:40px;'>💠 链上资产提取中心</h4>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📸 生成全息大屏海报 (长按发圈)", "📝 提取纯文本名片", "📥 JSON 极客底包下载"])

    with tab1:
        random.seed(hash_code)
        gradient_stops = []
        current_pos = 0
        while current_pos < 100:
            width = random.uniform(0.5, 3.0); space = random.uniform(0.5, 2.0)
            gradient_stops.append(f"rgba(0,243,255,0.6) {current_pos}%, rgba(0,243,255,0.6) {current_pos + width}%, transparent {current_pos + width}%, transparent {current_pos + width + space}%")
            current_pos += width + space
        barcode_css = "linear-gradient(90deg, " + ", ".join(gradient_stops) + ")"
        tags_html = "".join([f'<div style="background:rgba(0,243,255,0.1); border:1px solid rgba(0,243,255,0.4); padding:4px 8px; border-radius:4px; font-size:11px; color:#00f3ff; font-weight:bold;">{t}</div>' for t in data['tags']])

        html_to_image_script = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
            <style>
                body {{ margin: 0; display: flex; flex-direction: column; align-items: center; background-color: transparent; font-family: 'Noto Sans SC', sans-serif; user-select: none; padding: 10px 0;}}
                
                /* 将渲染目标强行脱离文档流，完美解决手机卡死和微信渲染Bug */
                #render-target {{ position: absolute; top: -9999px; left: -9999px; z-index: -100; }}
                
                #capture-box {{ width: 350px; background-color: #030712; padding: 30px 25px; border-radius: 16px; border: 1px solid rgba(0, 243, 255, 0.4); box-shadow: 0 0 30px rgba(0, 243, 255, 0.2); position: relative; overflow: hidden; color: #fff; box-sizing: border-box; }}
                .cyber-grid {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(0deg, rgba(0,243,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.04) 1px, transparent 1px); background-size: 20px 20px; z-index: 0; pointer-events: none; }}
                .top-glow {{ position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: linear-gradient(90deg, transparent, #00f3ff, transparent); z-index: 1; }}
                .tier-badge {{ position: absolute; top: 15px; right: -30px; background: {tier_color}; color: #000; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 12px; padding: 3px 30px; transform: rotate(45deg); z-index: 10; letter-spacing: 1px; box-shadow: 0 0 15px {tier_color}88;}}
                
                .content {{ position: relative; z-index: 2; }}
                .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom: 15px; margin-bottom: 20px; }}
                .logo-text {{ color: #00f3ff; font-family: 'Orbitron', sans-serif; font-size: 15px; font-weight: 900; letter-spacing: 1px; }}
                .sub-logo {{ font-size: 18px; font-weight: 900; margin-top: 5px; letter-spacing: 2px; text-shadow: 0 0 10px rgba(255,255,255,0.2);}}
                .auth-box {{ text-align: right; }}
                .auth-title {{ color: #94a3b8; font-family: 'Orbitron', monospace; font-size: 10px; letter-spacing: 1px; }}
                .auth-hash {{ color: #00f3ff; font-family: 'Orbitron', monospace; font-size: 12px; font-weight: bold; margin-top: 3px; }}
                
                .user-name {{ text-align: center; font-size: 22px; font-weight: 900; letter-spacing: 2px; color: #fff; margin-bottom: 10px; text-transform: uppercase; }}
                .mbti {{ font-family: 'Orbitron', sans-serif; font-size: 66px; font-weight: 900; color: #ffd700; line-height: 1; text-align: center; text-shadow: 0 0 25px rgba(255,215,0,0.6); margin-bottom: 8px; letter-spacing: 4px; }}
                .role {{ text-align: center; font-size: 16px; font-weight: 900; color: #00f3ff; margin-bottom: 20px; letter-spacing: 1px; }}
                
                .tags {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 6px; margin-bottom: 20px; }}
                
                .metrics-box {{ background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 15px; margin-bottom: 20px; }}
                .stat-row {{ display: flex; align-items: center; margin-bottom: 10px; font-size: 11px; font-weight: bold; }}
                .stat-row:last-child {{ margin-bottom: 0; }}
                
                .risk-box {{ border-left: 4px solid {r_color}; background: {r_color}1A; padding: 12px; border-radius: 0 6px 6px 0; margin-bottom: 20px; }}
                .risk-title {{ font-size: 10px; color: #e2e8f0; margin-bottom: 4px; }}
                .risk-val {{ color: {r_color}; font-size: 15px; font-weight: 900; text-shadow: 0 0 10px {r_color}88; }}
                
                .footer {{ text-align: center; color: #64748b; font-family: 'Orbitron', monospace; font-size: 9px; padding-top: 15px; border-top: 1px dashed rgba(255,255,255,0.1); line-height:1.6; }}
                .barcode {{ width: 85%; height: 20px; margin: 0 auto 8px auto; background: {barcode_css}; }}

                #loading-ui {{ font-family: 'Orbitron', sans-serif; color: #00f3ff; font-size: 13px; text-align: center; padding: 40px; animation: pulse 1s infinite alternate; letter-spacing: 2px; }}
                @keyframes pulse {{ 0% {{ opacity: 1; text-shadow: 0 0 10px #00f3ff; }} 100% {{ opacity: 0.4; text-shadow: none; }} }}
                
                #result-img {{ display: none; width: 100%; max-width: 350px; border-radius: 16px; border: 1px solid rgba(0,243,255,0.5); box-shadow: 0 15px 35px rgba(0,0,0,0.8); pointer-events: auto; -webkit-touch-callout: default; margin-top: 5px; }}
                .hint-box {{ display: none; color: #10b981; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); padding: 12px; border-radius: 6px; font-size: 13px; font-weight: bold; text-align: center; margin-top: 20px; line-height: 1.6; width: 100%; max-width: 350px; box-sizing: border-box; }}
            </style>
        </head>
        <body>
            <div id="render-target">
                <div id="capture-box">
                    <div class="cyber-grid"></div>
                    <div class="top-glow"></div>
                    <div class="tier-badge">{tier_level}</div>
                    <div class="content">
                        <div class="header">
                            <div><div class="logo-text">SDE MATRIX</div><div class="sub-logo">上海数据交易所</div></div>
                            <div class="auth-box"><div class="auth-title">SYS_HASH</div><div class="auth-hash">0x{hash_code[:6]}</div></div>
                        </div>
                        <div style="font-size:10px; color:#94a3b8; text-align:center; font-family:'Orbitron', monospace; margin-bottom:4px;">AUTHORIZED NODE</div>
                        <div class="user-name">{safe_alias_final}</div>
                        <div class="mbti">{mbti}</div>
                        <div class="role">【 {role_name} 】</div>
                        
                        <div style="display:flex; justify-content:space-between; text-align:center; margin-bottom: 20px; background:rgba(0,0,0,0.6); border:1px solid rgba(255,215,0,0.3); padding:10px; border-radius:8px;">
                            <div style="flex:1;">
                                <div style="font-size:9px; color:#94a3b8; font-family:Orbitron;">ASSET VALUATION (SDE)</div>
                                <div style="font-size:18px; color:#ffd700; font-weight:bold; font-family:Orbitron; text-shadow:0 0 10px rgba(255,215,0,0.5);">💎 {valuation_str}</div>
                            </div>
                            <div style="border-left:1px dashed rgba(255,255,255,0.2);"></div>
                            <div style="flex:1;">
                                <div style="font-size:9px; color:#94a3b8; font-family:Orbitron;">DECISIVENESS</div>
                                <div style="font-size:18px; color:#00f3ff; font-weight:bold; font-family:Orbitron; text-shadow:0 0 10px rgba(0,243,255,0.5);">⚡ {decisiveness}/100</div>
                            </div>
                        </div>

                        <div class="tags">{tags_html}</div>
                        
                        <div class="metrics-box">
                            <div style="font-family: 'Orbitron', monospace; font-size: 9px; color: #00f3ff; text-align: center; margin-bottom: 12px;">/// HASH METRICS ///</div>
                            <div class="stat-row"><span style="color:#e2e8f0; width:45px;">生态(E)</span><div style="flex-grow:1; height:6px; background:#1e293b; border-radius:3px; margin:0 10px; position:relative; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{val_E}%; background:#00f3ff;"></div></div><span style="color:#94a3b8; width:45px; text-align:right;">深潜(I)</span></div>
                            <div class="stat-row"><span style="color:#e2e8f0; width:45px;">实勘(S)</span><div style="flex-grow:1; height:6px; background:#1e293b; border-radius:3px; margin:0 10px; position:relative; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{val_S}%; background:#a855f7;"></div></div><span style="color:#94a3b8; width:45px; text-align:right;">前瞻(N)</span></div>
                            <div class="stat-row"><span style="color:#e2e8f0; width:45px;">量化(T)</span><div style="flex-grow:1; height:6px; background:#1e293b; border-radius:3px; margin:0 10px; position:relative; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{val_T}%; background:#3b82f6;"></div></div><span style="color:#94a3b8; width:45px; text-align:right;">共情(F)</span></div>
                            <div class="stat-row"><span style="color:#e2e8f0; width:45px;">秩序(J)</span><div style="flex-grow:1; height:6px; background:#1e293b; border-radius:3px; margin:0 10px; position:relative; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{val_J}%; background:#10b981;"></div></div><span style="color:#94a3b8; width:45px; text-align:right;">敏捷(P)</span></div>
                        </div>
                        
                        <div class="risk-box">
                            <div class="risk-title">合规熔断边界阈值</div>
                            <div class="risk-val">{r_tag}</div>
                        </div>
                        
                        <div class="footer">
                            <div class="barcode"></div>
                            <div style="margin-bottom: 4px;">2026 SDE DATA ELEMENT KERNEL</div>
                            <div>BLOCK: #{block_height} | HASH: 0x{hash_code[:8]}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="loading-ui">[ MINTING POSTER TO CLIENT... ]</div>
            <img id="result-img" alt="SDE Matrix Card" title="长按保存或分享" />
            <div id="hint" class="hint-box">✅ 数据资产海报生成成功！<br><span style="color:#fff;">👆 手机端请 <b>长按上方图片</b><br>即可「发送给朋友」或「保存到相册」</span></div>

            <script>
                setTimeout(() => {{
                    const target = document.getElementById('capture-box');
                    if (typeof html2canvas === 'undefined') {{ document.getElementById('loading-ui').innerHTML = '❌ 渲染引擎加载失败。'; return; }}
                    html2canvas(target, {{ scale: 2, backgroundColor: '#030712', useCORS: true, allowTaint: true, logging: false
                    }}).then(canvas => {{
                        document.getElementById('result-img').src = canvas.toDataURL('image/png');
                        document.getElementById('loading-ui').style.display = 'none';
                        document.getElementById('result-img').style.display = 'block';
                        document.getElementById('hint').style.display = 'block';
                        const rt = document.getElementById('render-target');
                        if (rt) rt.remove(); 
                    }}).catch(err => {{
                        document.getElementById('loading-ui').innerHTML = '⚠️ 手机内存受限，您可以直接截屏保存上方网页内容。';
                    }});
                }}, 1500); 
            </script>
        </body>
        </html>
        """
        components.html(html_to_image_script, height=880)

    with tab2:
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:10px; margin-top:10px;'>👇 点击下方代码框右上角的 <b style='color:#00f3ff;'>Copy</b> 图标，复制纯文字名片供群聊使用：</div>", unsafe_allow_html=True)
        share_card = f"""【上海数据交易所 · 核心算力链上凭证】
=================================
👤 确权节点：{safe_alias_final}
💎 算力估值：{valuation_str} SDE
🧬 核心架构：{mbti} ({role_name})
👑 全网评级：{tier_level} (稀缺度 {data['rarity']})
⚡️ 决策指数：{decisiveness}/100
🎯 核心指令：{data['tasks'][0]}
⚖️ 风控偏好：{r_tag}
=================================
🌐 2026 数据要素突破之年，寻找你的协同节点！
🔗 [全息链路校验哈希: 0x{hash_code}]"""
        st.code(share_card, language="plaintext")

    with tab3:
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:15px; margin-top:10px;'>💾 高管/极客视角：导出您的原生底层 JSON 结构树归档：</div>", unsafe_allow_html=True)
        export_data = {
            "node_alias": safe_alias_final, "matrix_id": mbti, "role": role_name, "tier": tier_level, "global_rarity": data['rarity'],
            "hash_signature": hash_code, "asset_valuation_sde": asset_valuation, "decisiveness_index": decisiveness,
            "metrics": {"E_I": val_E, "S_N": val_S, "T_F": val_T, "J_P": val_J},
            "synergy_index": {"Technology": syn_tech, "Business": syn_biz, "Compliance": syn_comp},
            "assigned_tasks": data['tasks'], "fatal_vulnerability": data['black_swan'], "patch_protocol": data['advice'],
            "timestamp": current_time_str
        }
        json_str = json.dumps(export_data, indent=4, ensure_ascii=False)
        st.download_button(label="📥 立即下载节点加密档案 (.JSON)", data=json_str, file_name=f"SDE_NODE_{safe_alias_final}.json", mime="application/json", use_container_width=True)

    def reset_system():
        st.session_state.started = False; st.session_state.current_q = 0; st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
        st.session_state.start_time = None; st.session_state.end_time = None; st.session_state.calculating = False
        st.session_state.user_alias = "SDE_NODE"; st.session_state.firework_played = False

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("⏏ 弹出磁盘并重启矩阵 (SYS_REBOOT)", on_click=reset_system, type="primary", use_container_width=True)

# =========================================================================
# ✨✨ 7. 底部专属版权归属声明 ✨✨
# =========================================================================
st.markdown("""
    <div style='text-align:center; margin-top:60px; margin-bottom:30px; font-family:\"Orbitron\", monospace; position:relative; z-index:10;'>
        <div style='color:#00f3ff !important; font-size:10px; opacity:0.4; letter-spacing:4px; margin-bottom:5px;'>
            POWERED BY SDE DATA ELEMENT KERNEL
        </div>
        <div style='color:#00f3ff !important; font-size:10px; opacity:0.2; letter-spacing:2px; margin-bottom:20px;'>
            SECURE ENTERPRISE BUILD
        </div>
        <div style='color:#94a3b8 !important; font-size:11px; opacity:0.6; font-family: "Noto Sans SC", sans-serif; letter-spacing:1px; border-top: 1px dashed rgba(148,163,184,0.3); padding-top: 15px; display: inline-block;'>
            © 2026 版权归属 <b style='color:#00f3ff; text-shadow: 0 0 10px rgba(0,243,255,0.5);'>无名逆流</b>
        </div>
    </div>
""", unsafe_allow_html=True)
