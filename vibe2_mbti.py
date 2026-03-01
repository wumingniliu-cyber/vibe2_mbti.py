import streamlit as st
import streamlit.components.v1 as components
import random
import time
import math
import hashlib
import html
import json
from datetime import datetime
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# 🌌 [ CORE 01 ] 系统内核与物理引擎配置
# ==============================================================================
VERSION = "1.0_ENTERPRISE_BUILD"
COPYRIGHT = "无名逆流"
SYS_NAME = f"SDE 全息算力引擎 | V 1.0"

st.set_page_config(page_title=SYS_NAME, page_icon="💠", layout="wide", initial_sidebar_state="expanded")

# ==============================================================================
# 🎨 [ CORE 02 ] 赛博全息 UI 渲染底座 (极限压缩千行 CSS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;600&display=swap');

    /* 强制全屏化与极致暗黑隔离 */
    [data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
    .block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; max-width: 1300px !important; }
    html, body, .stApp { background-color: #010409 !important; font-family: 'Noto Sans SC', sans-serif !important; color: #f8fafc !important; }
    
    /* 视网膜扫描与全息网格视差背景 */
    [data-testid="stAppViewContainer"]::before { content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, rgba(0, 243, 255, 0.05) 0%, rgba(1, 4, 9, 1) 70%); pointer-events: none; z-index: 0; }
    [data-testid="stAppViewContainer"]::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02)); background-size: 100% 3px, 3px 100%; z-index: 99999; pointer-events: none; opacity: 0.6; }
    
    /* 侧边栏深度穿透 */
    [data-testid="stSidebar"] { background-color: rgba(2, 6, 23, 0.95) !important; border-right: 1px solid rgba(0,243,255,0.2) !important; }
    .stMarkdown, p, span, h2, h3, h4, li, div { color: #e2e8f0 !important; z-index: 1; position: relative; }
    [data-testid="stProgress"] > div > div > div { background: linear-gradient(90deg, #00f3ff, #3b82f6) !important; box-shadow: 0 0 15px rgba(0,243,255,0.8); }
    
    /* 顶部 CSS 硬件加速交易大盘流 */
    .ticker-wrap { width: 100vw; overflow: hidden; height: 28px; background-color: rgba(2, 6, 23, 0.95); border-bottom: 1px solid rgba(0,243,255,0.3); position: fixed; top: 0; left: 0; z-index: 99990; box-shadow: 0 2px 10px rgba(0,243,255,0.1); }
    .ticker { display: inline-block; white-space: nowrap; padding-right: 100%; box-sizing: content-box; animation: ticker 40s linear infinite; font-family: 'Orbitron', monospace; font-size: 11px; color: #00f3ff; line-height: 28px; letter-spacing: 1px; }
    .ticker span { margin-right: 40px; } .ticker .up { color: #10b981; } .ticker .down { color: #f43f5e; }
    @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

    /* 骇客级故障风主标题 */
    .hero-title { font-size: 46px !important; font-weight: 900 !important; text-align: center; color: #ffffff !important; letter-spacing: 6px; margin-bottom: 5px; margin-top: 15px; text-shadow: 0 0 20px rgba(0,243,255,0.7), 0 0 40px rgba(0,243,255,0.3); position: relative; display: inline-block; text-transform: uppercase; }
    .hero-title::before, .hero-title::after { content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: transparent; }
    .hero-title::before { left: 2px; text-shadow: -2px 0 #f43f5e; animation: glitch-anim-1 2.5s infinite linear alternate-reverse; }
    .hero-title::after { left: -2px; text-shadow: 2px 0 #00f3ff; animation: glitch-anim-2 3.5s infinite linear alternate-reverse; }
    @keyframes glitch-anim-1 { 0% { clip-path: inset(20% 0 80% 0); } 20% { clip-path: inset(60% 0 10% 0); } 40% { clip-path: inset(40% 0 50% 0); } 60% { clip-path: inset(80% 0 5% 0); } 80% { clip-path: inset(10% 0 70% 0); } 100% { clip-path: inset(30% 0 20% 0); } }
    @keyframes glitch-anim-2 { 0% { clip-path: inset(10% 0 60% 0); } 20% { clip-path: inset(30% 0 20% 0); } 40% { clip-path: inset(70% 0 10% 0); } 60% { clip-path: inset(20% 0 50% 0); } 80% { clip-path: inset(90% 0 5% 0); } 100% { clip-path: inset(50% 0 30% 0); } }
    .hero-subtitle { text-align: center; color: #00f3ff !important; font-size: 13px; letter-spacing: 6px; opacity: 0.9; margin-bottom: 30px; font-family: 'Orbitron', sans-serif !important; font-weight: 700; background: rgba(0,243,255,0.1); display: inline-block; padding: 4px 20px; border-radius: 4px; border: 1px solid rgba(0,243,255,0.4); margin-top: 10px; }
    
    /* 终端及表单件 */
    .terminal-container { background: rgba(8, 15, 30, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: 25px; border-radius: 8px; font-family: 'Fira Code', monospace; font-size: 13px; color: #e2e8f0; box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px; max-width: 800px; margin-left: auto; margin-right: auto;}
    .cursor-blink { display: inline-block; width: 10px; height: 18px; background: #00f3ff; animation: blink 1s step-end infinite; vertical-align: middle; margin-left: 5px; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

    div[data-testid="stTextInput"] > div > div > input { background-color: rgba(4, 9, 20, 0.9) !important; color: #00f3ff !important; font-family: 'Orbitron', monospace !important; border: 1px solid rgba(0,243,255,0.5) !important; border-radius: 6px !important; text-align: center; font-size: 18px !important; font-weight: bold !important; letter-spacing: 2px; box-shadow: inset 0 0 20px rgba(0,243,255,0.1) !important; transition: all 0.3s ease; height: 50px; }
    div[data-testid="stTextInput"] > div > div > input:focus { border-color: #ffd700 !important; box-shadow: 0 0 25px rgba(255,215,0,0.4), inset 0 0 15px rgba(255,215,0,0.1) !important; }
    div[data-testid="stSelectbox"] > div > div { background-color: rgba(4, 9, 20, 0.95) !important; border: 1px solid rgba(168, 85, 247, 0.5) !important; color: #a855f7 !important; font-weight: bold;}

    div.stButton > button { background: linear-gradient(135deg, #0f172a 0%, #040914 100%) !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; border-left: 4px solid rgba(0, 243, 255, 0.6) !important; border-radius: 6px !important; min-height: 60px !important; width: 100% !important; padding: 10px 15px !important; text-align: left !important; box-shadow: 0 4px 10px rgba(0,0,0,0.4) !important; transition: all 0.2s ease !important; position: relative; overflow: hidden; }
    div.stButton > button::before { content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(0,243,255,0.15), transparent); transition: left 0.5s ease; }
    div.stButton > button:hover::before { left: 150%; }
    div.stButton > button p { color: #ffffff !important; font-size: 15px !important; font-weight: bold !important; }
    div.stButton > button:hover { border-color: #00f3ff !important; border-left: 6px solid #00f3ff !important; box-shadow: 0 0 20px rgba(0,243,255,0.3) !important; transform: translateX(4px) !important; }
    div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #00f3ff, #0088ff) !important; border: none !important; text-align: center !important; }
    div.stButton > button[data-testid="baseButton-primary"] p { color: #010308 !important; font-weight: 900 !important; font-size: 18px !important; letter-spacing: 2px !important; }
    div.stButton > button[data-testid="baseButton-primary"]:hover { transform: translateY(-3px) !important; box-shadow: 0 10px 30px rgba(0,243,255,0.6) !important; }
    
    /* 彭博大屏卡片体系 */
    .result-card { padding: 40px 30px; border-radius: 12px; background: rgba(8, 15, 30, 0.95) !important; border: 1px solid rgba(255,215,0,0.3); border-top: 6px solid #ffd700; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.8), inset 0 0 30px rgba(255,215,0,0.05); margin-bottom: 30px; position:relative; overflow:hidden; height:100%;}
    .mbti-code { font-family: 'Orbitron', sans-serif !important; font-size: 80px; font-weight: 900; color: #ffd700 !important; line-height: 1.1; letter-spacing: 6px; text-shadow: 0 0 35px rgba(255,215,0,0.6); margin: 5px 0;}
    .tier-badge { position: absolute; top: 20px; right: -45px; background: #ffd700; color: #000; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 13px; padding: 5px 50px; transform: rotate(45deg); z-index: 10; letter-spacing: 2px; box-shadow: 0 0 20px rgba(255,215,0,0.8);}
    
    .panel-box { background: rgba(10, 17, 32, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 20px; height: 100%; box-shadow: inset 0 0 20px rgba(0,0,0,0.4); margin-bottom: 20px;}
    .panel-title { color: #94a3b8; font-family: 'Orbitron', sans-serif; font-size: 13px; font-weight: bold; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 15px; letter-spacing: 1px; }

    .skill-badge { background: linear-gradient(90deg, rgba(168,85,247,0.2), rgba(168,85,247,0.05)); border: 1px solid rgba(168,85,247,0.5); border-left: 3px solid #a855f7; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; color: #e9d5ff; display: inline-block; margin: 4px; box-shadow: 0 0 10px rgba(168,85,247,0.2); }
    
    .cli-box { background: #000000; border: 1px solid #334155; border-left: 4px solid #00f3ff; padding: 20px; border-radius: 8px; font-family: 'Fira Code', monospace; font-size: 13px; color: #4ade80; box-shadow: inset 0 0 30px rgba(0,243,255,0.15); margin-top: 20px; word-break: break-all; line-height: 1.6;}

    /* 高级 Tabs 穿透 */
    [data-testid="stTabs"] button { color: #64748b !important; font-family: 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: 16px !important; padding-bottom: 15px !important; transition: all 0.3s ease; }
    [data-testid="stTabs"] button[aria-selected="true"] { color: #00f3ff !important; border-bottom-color: #00f3ff !important; border-bottom-width: 3px !important; text-shadow: 0 0 15px rgba(0,243,255,0.6); background: rgba(0,243,255,0.05); }

    /* 折叠黑匣子与代码块 */
    [data-testid="stExpander"] { background: rgba(5, 10, 21, 0.9) !important; border: 1px solid rgba(244, 63, 94, 0.5) !important; border-radius: 8px !important; overflow: hidden; margin-bottom: 20px;}
    [data-testid="stExpander"] summary { background: rgba(244, 63, 94, 0.1); color: #f43f5e !important; font-weight: 900 !important; font-size: 15px !important; padding: 15px !important; }
    
    [data-testid="stCodeBlock"] > div { background-color: #050505 !important; border: 1px solid #333 !important; border-left: 3px solid #10b981 !important; border-radius: 6px !important; }
    [data-testid="stCodeBlock"] pre, code { font-family: 'Fira Code', monospace !important; font-size: 12px !important; color: #4ade80 !important; line-height: 1.5 !important;}

    /* 下载按钮极客化 */
    div[data-testid="stDownloadButton"] > button { background: rgba(5, 12, 25, 0.95) !important; border: 1px dashed rgba(16, 185, 129, 0.8) !important; border-left: 6px solid #10b981 !important; margin-top: 20px; border-radius: 6px !important; height: 55px;}
    div[data-testid="stDownloadButton"] > button p { color: #10b981 !important; font-family: 'Orbitron', monospace !important; font-weight: bold !important; letter-spacing: 2px !important; font-size: 15px !important;}
    div[data-testid="stDownloadButton"] > button:hover { background: rgba(16, 185, 129, 0.15) !important; box-shadow: 0 0 30px rgba(16,185,129,0.5) !important; transform: scale(1.02) !important; }
    
    /* 赛博呼吸版权印记 */
    .copyright-niliu { font-size: 13px; font-family: "Noto Sans SC", sans-serif; letter-spacing: 2px; color: #00f3ff; display: inline-block; padding: 12px 35px; border-radius: 50px; border: 1px solid rgba(0,243,255,0.3); background: rgba(0,243,255,0.05); font-weight: 900; animation: neon-breathe 2.5s infinite alternate; box-shadow: 0 0 20px rgba(0,243,255,0.2);}
    @keyframes neon-breathe { 0% { box-shadow: 0 0 10px rgba(0,243,255,0.1), inset 0 0 5px rgba(0,243,255,0.1); border-color: rgba(0,243,255,0.2); } 100% { box-shadow: 0 0 25px rgba(0,243,255,0.6), inset 0 0 15px rgba(0,243,255,0.2); border-color: rgba(0,243,255,0.7); text-shadow: 0 0 10px #00f3ff; } }
</style>

<div class="ticker-wrap"><div class="ticker">
    <span>SDE-CORE: V1.0 INITIALIZED <b class="up">▲200%</b></span>
    <span>NODE-COMPLIANCE_WU: CONNECTED <b class="up">▲ACTIVE</b></span>
    <span>ASSET-DATA-77: MINT SUCCESS <b class="up">▲14.2TH/s</b></span>
    <span>SYS-RISK: THREAT BLOCKED <b class="up">▲SECURE</b></span>
    <span>MARKET-ROI: VOLATILITY DETECTED <b class="down">▼WARN</b></span>
    <span>CROSS-BORDER: PROTOCOL SYNC <b class="up">▲ESTABLISHED</b></span>
    <span>SDE-CORE: V1.0 INITIALIZED <b class="up">▲200%</b></span>
</div></div>
""", unsafe_allow_html=True)

# ==========================================
# 📊 [ CORE 03 ] 侧边栏：大厂生产网监听器
# ==========================================
with st.sidebar:
    st.markdown("<div style='text-align:center; font-family:Orbitron; font-size:28px; font-weight:900; color:#00f3ff; margin-bottom:20px; text-shadow: 0 0 15px #00f3ff;'>SDE CORE</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:12px; color:#94a3b8; font-family:Orbitron; border-bottom:1px solid #334155; padding-bottom:5px; margin-bottom:15px; font-weight:bold;'>/// NETWORK STATUS V1.0</div>", unsafe_allow_html=True)
    
    st.metric("Total Network Hashrate", f"{random.uniform(150.0, 155.0):.2f} EH/s", f"+{random.uniform(0.5, 2.5):.2f}%")
    st.metric("Active Node Validators", f"{random.randint(8400, 8500):,}", f"+{random.randint(10, 45)}")
    st.metric("24H Data Tx Volume", f"¥ {random.uniform(12.5, 14.2):.2f} B", f"+{random.uniform(2.0, 8.0):.2f}%")
    
    st.markdown("<div style='font-size:12px; color:#94a3b8; font-family:Orbitron; border-bottom:1px solid #334155; padding-bottom:5px; margin-top:30px; margin-bottom:15px; font-weight:bold;'>/// RECENT TX LOGS</div>", unsafe_allow_html=True)
    ticker_html = ""
    assets = ["Gov_Public_Data", "Med_Research_Set", "Fin_Risk_API", "Logistics_GPS", "Retail_Behavior"]
    for _ in range(6):
        ticker_html += f"<div style='font-family:Fira Code; font-size:11px; margin-bottom:10px; border-left:2px solid #10b981; padding-left:8px;'><span style='color:#10b981;'>[MINT]</span> <span style='color:#e2e8f0;'>{random.choice(assets)}</span><br><span style='color:#ffd700;'>GAS: {random.randint(12000,45000)} Gwei</span></div>"
    st.markdown(ticker_html, unsafe_allow_html=True)

# ==========================================
# 🧠 [ CORE 04 ] 题库与全系 16 型 100% 防崩字典
# ==========================================
questions = [
    {"q": "推动数商入场时，我倾向于亲自拜访机构进行面对面沟通，而非仅在线上发送标准入驻指引。", "dim": "E"},
    {"q": "代表数据交易所参与行业峰会，发表演讲并扩大 SDE 的市场影响力，会让我充满能量。", "dim": "E"},
    {"q": "面对复杂的数据跨境业务闭环，我更喜欢召集跨部门进行“头脑风暴”，而非独自撰写可行性报告。", "dim": "E"},
    {"q": "我习惯于维护庞大的政企及数商合作网络，并定期主动对接，挖掘潜在的数据产品挂牌机会。", "dim": "E"},
    {"q": "当市场上出现关于公共数据授权运营的新政策，我会立刻在工作群内发起热烈讨论。", "dim": "E"},
    {"q": "在评估一项数据资产入表案例时，我会死磕财务科目映射、摊销年限与合规确权等底层细节。", "dim": "S"},
    {"q": "我更信任交易大盘上的真实成交曲线与存证笔数，而不是研究报告中那些定性的宏观趋势预判。", "dim": "S"},
    {"q": "当听到“隐私计算”等前沿概念时，我最先关心的是它在 SDE 现有机房和架构里如何具体落地。", "dim": "S"},
    {"q": "我认为数据交易所当前最核心的任务是把“确权、存证、交付、清算”的每一个动作做到极致规范。", "dim": "S"},
    {"q": "审核数据产品上架时，我严格依赖合规审查操作清单，极度排斥带有主观弹性的价值评估。", "dim": "S"},
    {"q": "即使某个数据产品能带来巨大短期交易额，只要被发现合规硬伤，我也会毫不犹豫按下终止键。", "dim": "T"},
    {"q": "在评选“年度优秀数商”时，我主张完全依靠交易贡献度等客观算法指标，剔除任何人情主观分。", "dim": "T"},
    {"q": "面对前线业务部门抱怨合规流程繁琐，我会列举法律底线直接回绝，认为交易所的红线不容变通。", "dim": "T"},
    {"q": "当下属在确权或存证操作中出现失误，我会直接指出其操作逻辑的谬误，认为这种单刀直入最高效。", "dim": "T"},
    {"q": "我坚信通过智能合约等技术手段替代人工审核，是确保数据交易平台绝对公平与廉洁的唯一途径。", "dim": "T"},
    {"q": "在主导大型数据创新项目前，我会建立极其严密的倒排计划表，非常反感进度失去控制。", "dim": "J"},
    {"q": "我的云盘文件夹、数据资产文档拥有严丝合缝的分类与命名逻辑，任何文件乱放都会让我极度不适。", "dim": "J"},
    {"q": "如果一场跨部门业务讨论会没有形成明确的会议纪要、SOP决议和责任人，我会认为这是在浪费时间。", "dim": "J"},
    {"q": "我倾向于在系统开发初期就锁定所有的核心业务需求，对中途频繁变更需求持强烈排斥态度。", "dim": "J"},
    {"q": "即便面临极高压的交易旺季，我也坚持每天下班前进行工作复盘，并雷打不动地更新明日待办清单。", "dim": "J"}
]

# 万行级精简：全系 16 型人格属性矩阵完全补齐，0 KeyError 隐患
mbti_base = {
    "INTJ": ["首席数据架构师", "UR", "#ff003c", "数据要素底座的造物主，构建严密的底层制度与逻辑规则。"],
    "INTP": ["量化风控极客", "SSR", "#ffd700", "穿透数据迷雾，寻找确权定价模型与逻辑漏洞的最优解。"],
    "ENTJ": ["战略开拓领军人", "UR", "#ff003c", "天生的矩阵建设者，在数据探索区展现极强的破局能力。"],
    "ENTP": ["模式重构极客", "SSR", "#ffd700", "传统交易规则的挑战者，寻找下一代数据资产流转范式。"],
    "INFJ": ["产业战略先知", "UR", "#ff003c", "精准预判数据流转对未来实体经济产生的深远变革。"],
    "INFP": ["价值主张锚定者", "SR", "#a855f7", "冷酷数据背后的灵魂捕捉者，注入引人共鸣的生态信仰。"],
    "ENFJ": ["生态联盟主理人", "SSR", "#ffd700", "数据交易所的枢纽中心，卓越的共识构建与资源聚拢能力。"],
    "ENFP": ["资源布道狂热者", "SR", "#a855f7", "充满感染力的生态火苗，让路演推介变成市场的狂热共识。"],
    "ISTJ": ["合规审查主理官", "SR", "#a855f7", "SDE 底层防线的守夜人，安全、严谨与业务零失误的代名词。"],
    "ISFJ": ["清结算永动机", "R", "#3b82f6", "最坚韧的底层支点，通过极致纠错与细节控场支撑平台吞吐。"],
    "ESTJ": ["全域业务统筹官", "SSR", "#ffd700", "无可争议的推进器，将宏观政策拆解为团队可绝对执行的 KPI。"],
    "ESFJ": ["政企外联中枢", "SR", "#a855f7", "超级连接器，擅长经营多维政企生态，前线业务的最强润滑剂。"],
    "ISTP": ["底层灾备指挥官", "SR", "#a855f7", "数据底座的实干派，只对逻辑代码负责，系统危机的定海神针。"],
    "ISFP": ["数字美学重构官", "R", "#3b82f6", "赋予枯燥数据美学权重，提升资产路演与终端大屏的绝对质感。"],
    "ESTP": ["敏捷套利黑客", "SSR", "#ffd700", "数据流通一线的敏锐猎手，极快捕捉市场红利与套利机会。"],
    "ESFP": ["品牌磁场信标", "SR", "#a855f7", "前台形象窗口，具备将复杂政策解码为大众传播话术的超级天赋。"]
}

mbti_details = {}
for k, v in mbti_base.items():
    mbti_details[k] = {
        "role": v[0], "tier": v[1], "tier_color": v[2], "desc": v[3],
        "rarity": f"{random.uniform(0.1, 8.5):.2f}%",
        "base_hash": random.randint(8000, 9999),
        "base_roi": random.uniform(1.05, 1.65),
        "volatility": random.uniform(0.1, 0.6),
        "market_style": "动态量化对冲与趋势跟踪混合策略",
        "tags": ["高维节点", "V1.0 认证", "算力引擎"],
        "skills": ["全局视野 (Lv.Max)", "数据解构", "生态共振"],
        "evolution": ["L1 核心执行官", "L2 跨域协议主理人", "L3 联邦生态造物主"],
        "tasks": [f"主导 SDE [{k}] 级战略架构落地", "重构平台级业务流转核心闭环"],
        "black_swan": "在极端的黑天鹅市场波动下，可能因底层惯性思维导致短期的算力阻断与决策延迟。",
        "advice": "强制引入对抗性测试与沙盒模拟，保持系统级的冗余与弹性容错。"
    }

# --- 算法：量化金融 K 线生成器 ---
def generate_alpha_curve(base_roi, volatility, seed):
    np.random.seed(seed)
    days, roi = list(range(1, 31)), [100.0]
    for _ in range(29):
        roi.append(max(30.0, roi[-1] + (base_roi - 1.0) * 10 + np.random.normal(0, volatility * 35)))
    return days, roi

def calc_synergy(m1, m2):
    diff = sum(1 for a, b in zip(m1, m2) if a != b)
    if diff == 0: return 92, "【绝对镜像】决策同频，沟通0阻力，但盲区完全重合，极易导致系统性翻车。"
    elif diff == 1: return 98, "【黄金并网】核心逻辑一致且具备神级微调互补，SDE 最强双核业务推土机！"
    elif diff == 2: return 85, "【灰度容错】视角存在差异，能通过激烈碰撞打磨出更抗击打的绝美业务闭环。"
    elif diff == 3: return 65, "【高频摩擦】存在底层通信壁垒，协同作业必须强制引入第三方作为缓冲层。"
    else: return 99, "【阴阳反转】代码完全相反！日常沟通极度痛苦，但背靠背能实现无死角全域降维打击！"

# ==========================================
# ⚙️ [ CORE 05 ] 状态机管理
# ==========================================
for key, val in [('started', False), ('current_q', 0), ('start_time', None), ('end_time', None), ('calculating', False), ('user_alias', "Compliance_Wu"), ('scores', {"E": 0, "S": 0, "T": 0, "J": 0}), ('firework', False)]:
    if key not in st.session_state: st.session_state[key] = val

def cb_start():
    alias = st.session_state.login_input.strip()
    st.session_state.user_alias = html.escape(alias) if alias else "Compliance_Wu"
    st.session_state.started = True; st.session_state.start_time = time.time()
def cb_ans(val, dim):
    st.session_state.scores[dim] += (val - 3); st.session_state.current_q += 1
    if st.session_state.current_q >= len(questions):
        st.session_state.end_time = time.time(); st.session_state.calculating = True

# ==========================================
# 🖥️ [ CORE 06 ] 前台路由与全息视图
# ==========================================
if not st.session_state.started:
    st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align: center; margin-bottom: 20px;"><div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:14px; letter-spacing:8px; margin-bottom:10px;">SHANGHAI DATA EXCHANGE</div><h1 class="hero-title" data-text="职场算力系统 V 1.0">职场算力系统 V 1.0</h1><div class="hero-subtitle">ENTERPRISE_BUILD</div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class='terminal-container' style='max-width:800px; margin:0 auto 30px auto;'><div class='term-line'><span style='color:#94a3b8;'>[SYSTEM]</span> Securing root connection to SDE Ledger... <span style='color:#00f3ff;'>[ESTABLISHED]</span></div><div class='term-line'><span style='color:#94a3b8;'>[KERNEL]</span> Loading 6D Multi-Matrix Algorithm V1.0... <span style='color:#00f3ff;'>[LOADED]</span></div><div class='term-line-main'><span style='color:#ffffff; font-size: 15px; font-family: "Noto Sans SC", sans-serif; line-height: 1.8;'><br><b>警告：系统将对您的职场大脑进行物理级拆解与链上确权。</b><br><br>您的决策本能、风控阈值与业务嗅觉将被全面数据化。一旦扫描完成，系统将生成不可篡改的<b>高阶职场算力凭证</b>。</span><span class="cursor-blink"></span></div></div>""", unsafe_allow_html=True)
    with st.form(key="login", border=False):
        st.markdown("<div style='max-width:600px; margin:0 auto;'><div style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:bold; margin-bottom:8px; text-align:center;'>▼ MOUNT NODE IDENTIFIER (输入授权节点代号) ▼</div>", unsafe_allow_html=True)
        st.text_input("", key="login_input", placeholder="例如：Compliance_Wu", value="Compliance_Wu", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        st.form_submit_button("▶ 授予最高权限并提取物理算力资产", on_click=cb_start, type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.calculating:
    st.markdown("<h2 class='hero-title' data-text='[ HASHING NEURAL NETWORK ]' style='font-size:28px !important; margin-top:50px; text-align:center; display:block;'>[ HASHING NEURAL NETWORK ]</h2>", unsafe_allow_html=True)
    mint_box = st.empty()
    h_logs = ""
    for _ in range(12):
        h_logs = f"<span style='color:#94a3b8;'>[BLOCK_MINT]</span> <span style='color:#ffd700;'>0x{hashlib.sha256(str(random.random()).encode()).hexdigest().upper()[:24]}...</span> <span style='color:#10b981;'>[CONFIRMED]</span><br>" + h_logs
        mint_box.markdown(f"<div class='cli-box' style='max-width:800px; margin:0 auto; height:250px; overflow:hidden; border-color:#00f3ff;'>{h_logs}</div>", unsafe_allow_html=True)
        time.sleep(0.12)
    st.session_state.calculating = False; st.rerun()

elif st.session_state.current_q < len(questions):
    st.markdown("<div style='max-width: 800px; margin: 0 auto;'>", unsafe_allow_html=True)
    q = questions[st.session_state.current_q]
    m_name = {"E": "ECO_NETWORK / 外联网络", "S": "EXEC_GRANULAR / 颗粒实勘", "T": "RISK_QUANT / 量化风控", "J": "ORDER_ARCH / 秩序架构"}.get(q['dim'])
    d_hash = hashlib.sha256(f"B_{st.session_state.current_q}_{q['q']}".encode()).hexdigest()[:12].upper()
    
    st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
    p_val = (st.session_state.current_q + 1) / len(questions)
    st.progress(p_val)
    st.markdown(f"<div style='text-align:right; font-family:Orbitron, monospace; color:#00f3ff; font-size:12px; margin-top:8px;'>DATA PIPELINE: {int(p_val*100)}%</div>", unsafe_allow_html=True)
    st.markdown(f"""<div style='background: rgba(10, 15, 25, 0.9); border: 1px solid rgba(0, 243, 255, 0.4); border-radius: 8px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 20px rgba(0, 243, 255, 0.05); margin-top: 20px; margin-bottom: 30px; border-left: 5px solid #00f3ff;'><div style='display:flex; justify-content:space-between; font-family:Orbitron; color:#00f3ff; font-size:12px; margin-bottom:15px; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom:10px;'><span>SYS_MOD: {m_name}</span><span>HASH: 0x{d_hash}</span></div><div style='font-size: 18px; color: #ffffff !important; line-height: 1.8; font-weight: 700;'>{q['q']}</div></div>""", unsafe_allow_html=True)
    
    for txt, v in [("🚫 [ 强制阻断 ] 危险：完全背离我的直觉", 1), ("⚠️ [ 弱态耦合 ] 降级：仅在极端场景才用", 2), ("⚖️ [ 视境判定 ] 悬空：视具体业务环境而定", 3), ("🤝 [ 逻辑握手 ] 安全：常用的标准决策流", 4), ("🔒 [ 绝对锁定 ] 同步：完美复刻底层思维", 5)]:
        st.button(txt, type="secondary", key=f"q_{st.session_state.current_q}_{v}", on_click=cb_ans, args=(v, q['dim']))
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- 💎 高能算法结算 ---
    if not st.session_state.firework: trigger_supernova(); st.session_state.firework = True
    
    res = st.session_state.scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    data = mbti_details.get(mbti, mbti_details["INTJ"]) # 绝对安全兜底
    
    safe_alias, role, t_lvl, t_col, rar = st.session_state.user_alias.upper(), data['role'], data['tier'], data['tier_color'], data['rarity']
    
    def get_int(s): return int(max(15, min(100, 50 + (s * 3.5))))
    v_E, v_I = get_int(res["E"]), 100 - get_int(res["E"])
    v_S, v_N = get_int(res["S"]), 100 - get_int(res["S"])
    v_T, v_F = get_int(res["T"]), 100 - get_int(res["T"])
    v_J, v_P = get_int(res["J"]), 100 - get_int(res["J"])

    # 六维衍生算法
    dim_str = int(max(20, min(100, 50 - res["S"]*4 + res["T"]*2 + (10 if "N" in mbti else 0))))
    dim_exe = int(max(20, min(100, 50 + res["S"]*5 + res["J"]*3 + (10 if "S" in mbti else 0))))
    dim_com = int(max(20, min(100, 50 + res["J"]*4 + res["T"]*3 + (10 if "J" in mbti else 0))))
    dim_inn = int(max(20, min(100, 50 - res["S"]*3 - res["J"]*3 + (10 if "P" in mbti else 0))))
    dim_emp = int(max(20, min(100, 50 + res["E"]*4 - res["T"]*3 + (10 if "F" in mbti else 0))))
    dim_tec = int(max(20, min(100, 50 - res["E"]*3 + res["T"]*4 + (10 if "T" in mbti else 0))))

    r_score = int(max(5, min(95, 50 + (-res["J"] * 2) - (res["S"] * 1.5))))
    if r_score < 35: r_tag, r_color = "绝对合规与防线兜底", "#10b981"
    elif r_score < 65: r_tag, r_color = "动态演进与灰度套利", "#ffd700"
    else: r_tag, r_color = "无界扩张与颠覆突变", "#f43f5e"

    t_taken = max(1, st.session_state.end_time - st.session_state.start_time)
    h_code = hashlib.sha256(f"{safe_alias}{mbti}{t_taken}V1.0".encode()).hexdigest().upper()
    b_height = f"V1.0-{(int(time.time()) % 1000000):06d}"
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # 高管装逼属性
    avg_t = t_taken / len(questions)
    dec = int(min(99, max(35, 100 - (max(0, avg_t - 2.5) * 5))))
    ext = sum(abs(v) for v in res.values()) / 40.0
    val = int(data['base_hash'] * (1 + ext * 0.4) * (0.8 + (dec/100.0) * 0.5) * (0.9 + (int(h_code[:8], 16) % 200)/1000.0) * 10000)
    pct = round(min(99.9, max(50.0, 60 + (dec * 0.3) + (ext * 10))), 1)
    
    d_arr, roi_arr = generate_alpha_curve(data['base_roi'], data['volatility'], int(h_code[:6], 16))

    # ==========================================
    # 🖥️ 塔台级 UI 渲染开始 (分栏设计)
    # ==========================================
    st.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 15px 20px; border-radius: 8px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 20px rgba(16,185,129,0.3);">
        <div><span style="font-size: 18px; margin-right: 10px;">✅</span><span style="color: #10b981; font-weight: 900; font-size: 14px; letter-spacing: 1px;">SDE CORE NODE MINTED [ V 1.0 ]</span></div>
        <div style="color: #94a3b8; font-family: 'Orbitron', monospace; font-size: 12px; font-weight:bold;">BLOCK: #{b_height} | TX: 0x{h_code[:10]}</div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1.3], gap="large")
    
    with col_l:
        st.markdown(f"""
        <div class="result-card">
            <div class="tier-badge" style="background: {t_col}; box-shadow: 0 0 25px {t_col}99;">{t_lvl}</div>
            <div class="orbitron-font" style="font-size:12px; color:#94a3b8; letter-spacing:6px; margin-bottom:15px;">SDE NEURAL DECODING V1.0</div>
            <div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:16px; margin-bottom:5px; border-bottom:1px dashed #334155; padding-bottom:10px; display:inline-block; font-weight:bold;">{safe_alias}</div>
            <div class="mbti-code">{mbti}</div>
            <div style="font-size: 24px; font-weight: 900; color: #00f3ff !important; margin: 10px 0 20px 0; letter-spacing: 2px;">【 {role} 】</div>
            <div style="color:#e2e8f0 !important; font-size:15px; line-height:1.8; margin-bottom:20px; font-weight:400;">{data['desc']}</div>
            <div style="margin-bottom:25px;">{" ".join([f'<span style="background:rgba(0, 243, 255, 0.1); color:#00f3ff !important; border:1px solid rgba(0,243,255,0.4); padding:6px 14px; border-radius:6px; font-size:13px; font-weight:900; margin:4px; display:inline-block;">{t}</span>' for t in data['tags']])}</div>
            
            <div style="display:flex; justify-content:space-between; gap:15px;">
                <div style="flex:1; background:rgba(0,0,0,0.8); border:1px solid rgba(255,215,0,0.4); border-radius:8px; padding:20px;">
                    <div style="font-size:11px; color:#94a3b8; font-family:'Orbitron'; margin-bottom:8px;">HASHRATE VALUATION</div>
                    <div style="font-size:26px; color:#ffd700; font-weight:900; font-family:'Orbitron'; text-shadow:0 0 15px rgba(255,215,0,0.8);">💎 {round(val, -4):,}</div>
                </div>
                <div style="flex:1; background:rgba(0,0,0,0.8); border:1px solid rgba(0,243,255,0.4); border-radius:8px; padding:20px;">
                    <div style="font-size:11px; color:#94a3b8; font-family:'Orbitron'; margin-bottom:8px;">GLOBAL PERCENTILE</div>
                    <div style="font-size:26px; color:#00f3ff; font-weight:900; font-family:'Orbitron'; text-shadow:0 0 15px rgba(0,243,255,0.8);">⚡ TOP {100 - pct:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 市场压测", "🌌 3D星图", "🔮 进化树", "💻 智能合约", "🤝 协同沙盘"])
        
        with tab1:
            st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title' style='color:#ffd700; border-color:#ffd700;'>/// 30-DAY MARKET ROI SIMULATION (ALPHA)</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:13px; color:#94a3b8; margin-bottom:10px;'>系统基于高斯随机游走为您推演的业务风格：<span style='color:#ffd700; font-weight:bold;'>{data['market_style']}</span></div>", unsafe_allow_html=True)
            fig_roi = go.Figure()
            lc = "#10b981" if roi_arr[-1] >= 100 else "#f43f5e"
            fig_roi.add_trace(go.Scatter(x=d_arr, y=roi_arr, mode='lines', line=dict(color=lc, width=3), fill='tozeroy', fillcolor=f'rgba({16 if roi_arr[-1]>=100 else 244}, {185 if roi_arr[-1]>=100 else 63}, {129 if roi_arr[-1]>=100 else 94}, 0.15)'))
            fig_roi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10), height=320, xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='Trading Days (T)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='SDE Alpha Net Value'))
            st.plotly_chart(fig_roi, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>/// 3D COGNITIVE TOPOLOGY MAP</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:12px; color:#94a3b8; margin-bottom:10px;'>降维映射至三维坐标系 (支持360°触控拖拽)。背景为全网 100 个模拟节点。</div>", unsafe_allow_html=True)
            np.random.seed(int(h_code[:6], 16))
            x_v = v_E if res['E']>0 else -v_I
            y_v = v_N if res['S']<=0 else -v_S
            z_v = v_T if res['T']>0 else -v_F
            f3d = go.Figure()
            f3d.add_trace(go.Scatter3d(x=np.random.randint(-100,100,100), y=np.random.randint(-100,100,100), z=np.random.randint(-100,100,100), mode='markers', marker=dict(size=4, color='#334155', opacity=0.6), name='全网节点'))
            f3d.add_trace(go.Scatter3d(x=[x_v], y=[y_v], z=[z_v], mode='markers+text', text=[mbti], textposition="top center", marker=dict(size=16, color=t_col, symbol='diamond', line=dict(color='#fff', width=2)), textfont=dict(color=t_col, size=18, family="Orbitron", weight="bold"), name='当前授权节点'))
            f3d.update_layout(scene=dict(xaxis_title='执行↔深潜', yaxis_title='实务↔前瞻', zaxis_title='共情↔刚性', xaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b"), yaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b"), zaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b")), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=380, showlegend=False)
            st.plotly_chart(f3d, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)

        with tab3:
            st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title' style='color:#a855f7; border-color:#a855f7;'>/// CAREER EVOLUTION TREE</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="margin-bottom:15px; border-left:3px solid #00f3ff; padding-left:15px; background:linear-gradient(90deg, rgba(0,243,255,0.1), transparent); padding-top:10px; padding-bottom:10px; border-radius: 0 6px 6px 0;">
                <div style="color:#00f3ff; font-family:Orbitron; font-size:10px; margin-bottom:2px;">PHASE 1 (CURRENT)</div><div style="color:#fff; font-weight:bold; font-size:15px;">{data['evolution'][0]}</div>
            </div>
            <div style="margin-bottom:15px; border-left:3px solid #a855f7; padding-left:15px; background:linear-gradient(90deg, rgba(168,85,247,0.1), transparent); padding-top:10px; padding-bottom:10px; border-radius: 0 6px 6px 0; margin-left: 20px;">
                <div style="color:#a855f7; font-family:Orbitron; font-size:10px; margin-bottom:2px;">PHASE 2 (AWAKENING)</div><div style="color:#fff; font-weight:bold; font-size:15px;">{data['evolution'][1]}</div>
            </div>
            <div style="border-left:3px solid #ffd700; padding-left:15px; background:linear-gradient(90deg, rgba(255,215,0,0.15), transparent); padding-top:10px; padding-bottom:10px; border-radius: 0 6px 6px 0; margin-left: 40px; box-shadow: 0 0 15px rgba(255,215,0,0.2);">
                <div style="color:#ffd700; font-family:Orbitron; font-size:10px; margin-bottom:2px;">PHASE 3 (ULTIMATE)</div><div style="color:#ffd700; font-weight:900; font-size:17px;">{data['evolution'][2]}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("⚠️ 绝密压测：SDE 史诗级黑天鹅宕机演习 (点击解密)"):
                st.markdown(f"<div style='padding: 5px 10px; font-size: 13px; color: #cbd5e1; line-height: 1.7;'><div style='color: #f43f5e; font-weight: 900; margin-bottom: 5px;'>[ 致命崩溃盲点 ]</div><div style='margin-bottom: 15px;'>{data['black_swan']}</div><div style='color: #10b981; font-weight: 900; margin-bottom: 5px;'>[ 官方热修复建议 ]</div><div>{data['advice']}</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab4:
            st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title' style='color:#10b981; border-color:#10b981;'>/// SOLIDITY SMART CONTRACT MINT LOG</div>", unsafe_allow_html=True)
            code = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@sde-network/contracts/token/ERC721.sol";

contract SDE_Talent_Registry_V1 is ERC721 {{
    struct Profile {{
        string matrix_id;
        uint256 valuation;
        uint8 decisiveness;
        string tier;
    }}
    mapping(uint256 => Profile) public nodes;
    constructor() ERC721("SDE_NODE_V1", "SDEN") {{}}

    // MINTED: {safe_alias}
    // BLOCK: {b_height}
    function executeMint() public {{
        uint256 tokenId = uint256(0x{h_code[:8]});
        nodes[tokenId] = Profile("{mbti}", {val}, {dec}, "{t_lvl}");
        _mint(msg.sender, tokenId);
    }}
}}"""
            st.code(code, language="solidity")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab5:
            st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title' style='color:#3b82f6; border-color:#3b82f6;'>/// TEAM SYNERGY ENGINE</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:14px; color:#94a3b8; margin-bottom:15px;'>输入团队成员的底层架构，系统将运用算法计算你们的协同匹配度</div>", unsafe_allow_html=True)
            pmbti = st.selectbox("🎯 挂载目标协作节点:", options=list(mbti_details.keys()), index=list(mbti_details.keys()).index("ESTJ"), label_visibility="collapsed")
            sc, sd = calc_synergy(mbti, pmbti)
            st.markdown(f"""<div style="background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.5); padding: 30px; border-radius: 12px; margin-bottom:20px; text-align:center; box-shadow: 0 0 30px rgba(59,130,246,0.15);"><div style="font-family:'Orbitron'; color:#3b82f6; font-size:14px; font-weight:bold; margin-bottom:15px; letter-spacing: 3px;">[ SYNERGY MATCH RATE ]</div><div style="font-family:'Orbitron'; font-size:60px; font-weight:900; color:#fff; text-shadow:0 0 30px rgba(59,130,246,0.8); margin-bottom:20px;">{sc}%</div><div style="color:#e2e8f0; font-size:15px; font-weight:bold; line-height:1.7;">{sd}</div></div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ==========================
    # 🔥 防爆海报提取中心
    # ==========================
    st.markdown("<h4 style='color:#00f3ff !important; border-left:5px solid #00f3ff; padding-left:12px; font-weight:900; margin-top:30px;'>💠 链上资产提取终端 (V 1.0)</h4>", unsafe_allow_html=True)
    t_img, t_txt, t_json = st.tabs(["📸 V1.0 视网膜全息海报 (长按发圈)", "📝 纯文本通讯协议", "📥 极客 JSON 底包"])

    with t_img:
        st.markdown("<div style='font-size:13px; color:#10b981; margin-bottom:10px;'>系统已启用防爆内存引擎压制高清海报，请等待 1.5 秒...</div>", unsafe_allow_html=True)
        random.seed(h_code); g_stops = []
        for p in range(0, 100, int(random.uniform(2, 6))): g_stops.append(f"rgba(0,243,255,0.7) {p}%, rgba(0,243,255,0.7) {p+1}%, transparent {p+1}%, transparent {p+2}%")
        b_css = "linear-gradient(90deg, " + ", ".join(g_stops) + ")"
        tag_h = "".join([f'<span style="background:rgba(0,243,255,0.1); border:1px solid rgba(0,243,255,0.5); padding:4px 8px; border-radius:4px; font-size:12px; color:#00f3ff; font-weight:bold; margin:3px; display:inline-block;">{t}</span>' for t in data['tags']])
        sk_h = "".join([f'<span style="background:linear-gradient(90deg, rgba(168,85,247,0.3), rgba(168,85,247,0.1)); border:1px solid rgba(168,85,247,0.6); border-left:3px solid #a855f7; padding:4px 8px; border-radius:4px; font-size:11px; color:#e9d5ff; font-weight:bold; display:inline-block; margin:3px;">{s}</span>' for s in data['skills']])

        h2c_script = f"""
        <!DOCTYPE html><html><head><meta charset="utf-8">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
        <style>
            body {{ margin: 0; background: transparent; font-family: 'Noto Sans SC', sans-serif; display: flex; flex-direction: column; align-items: center; padding-top: 10px;}}
            #rt {{ position: absolute; top: -9999px; left: -9999px; z-index: -100; }}
            #cb {{ width: 380px; background: #010308; padding: 40px 30px; border-radius: 16px; border: 1px solid rgba(0, 243, 255, 0.5); box-shadow: 0 0 40px rgba(0, 243, 255, 0.2); position: relative; overflow: hidden; color: #fff; box-sizing: border-box; }}
            .bg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(0deg, rgba(0,243,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.05) 1px, transparent 1px); background-size: 25px 25px; z-index: 0; }}
            .gl {{ position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: linear-gradient(90deg, transparent, #00f3ff, transparent); z-index: 1; }}
            .bdg {{ position: absolute; top: 22px; right: -40px; background: {t_col}; color: #000; font-family: 'Orbitron'; font-weight: 900; font-size: 13px; padding: 5px 45px; transform: rotate(45deg); z-index: 10; letter-spacing: 2px; }}
            .ct {{ position: relative; z-index: 2; }}
            .hd {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom: 15px; margin-bottom: 25px; }}
            .nm {{ text-align: center; font-size: 26px; font-weight: 900; letter-spacing: 2px; margin-bottom: 10px; color: #fff; text-transform: uppercase; }}
            .mb {{ font-family: 'Orbitron'; font-size: 80px; font-weight: 900; color: #ffd700; line-height: 1; text-align: center; text-shadow: 0 0 30px rgba(255,215,0,0.6); margin-bottom: 10px; letter-spacing: 5px; }}
            .rl {{ text-align: center; font-size: 18px; font-weight: 900; color: #00f3ff; margin-bottom: 25px; letter-spacing: 2px; }}
            .vb {{ display:flex; justify-content:space-between; text-align:center; background:rgba(0,0,0,0.8); border:1px solid rgba(255,215,0,0.4); padding:15px; border-radius:8px; margin-bottom: 20px; }}
            .rb {{ border-left: 4px solid {r_color}; background: {r_color}1A; padding: 15px; border-radius: 0 8px 8px 0; margin-bottom: 25px; }}
            .ft {{ text-align: center; color: #64748b; font-family: 'Orbitron'; font-size: 10px; padding-top: 15px; border-top: 1px dashed rgba(255,255,255,0.1); line-height: 1.8; }}
            .bc {{ width: 90%; height: 25px; margin: 0 auto 10px auto; background: {b_css}; }}
            #ui {{ font-family: 'Orbitron'; color: #00f3ff; font-size: 14px; text-align: center; padding: 50px; animation: p 1s infinite alternate; letter-spacing: 2px; font-weight:bold;}}
            @keyframes p {{ 0% {{ opacity: 1; text-shadow: 0 0 10px #00f3ff; }} 100% {{ opacity: 0.4; }} }}
            #img {{ display: none; width: 100%; max-width: 380px; border-radius: 16px; border: 1px solid rgba(0,243,255,0.6); box-shadow: 0 20px 40px rgba(0,0,0,0.9); pointer-events: auto; margin-top: 10px;}}
            .ht {{ display: none; background: rgba(16,185,129,0.15); border: 1px solid #10b981; padding: 15px; border-radius: 8px; font-size: 14px; color: #fff; text-align: center; margin-top: 20px; width: 100%; max-width: 380px; box-sizing: border-box; }}
        </style></head><body>
            <div id="rt"><div id="cb"><div class="bg"></div><div class="gl"></div><div class="bdg">{t_lvl}</div>
                <div class="ct"><div class="hd"><div><div style="color:#00f3ff;font-family:Orbitron;font-size:16px;font-weight:900;">SDE MATRIX</div><div style="font-size:20px;font-weight:900;letter-spacing:4px;">上海数据交易所</div></div><div style="text-align:right;"><div style="color:#94a3b8;font-family:Orbitron;font-size:10px;">V1.0 HASH</div><div style="color:#00f3ff;font-family:Orbitron;font-size:12px;font-weight:bold;">0x{h_code[:8]}</div></div></div>
                    <div style="font-size:11px;color:#94a3b8;text-align:center;font-family:Orbitron;margin-bottom:5px;">AUTHORIZED NODE</div>
                    <div class="nm">{safe_alias}</div><div class="mb">{mbti}</div>
                    <div style="text-align:center;font-size:12px;color:#94a3b8;margin-bottom:20px;">GLOBAL RARITY: <span style="color:{t_col};font-family:Orbitron;font-weight:bold;font-size:14px;">{rar}</span></div>
                    <div class="rl">【 {role} 】</div>
                    <div class="vb">
                        <div style="flex:1;"><div style="font-size:10px;color:#94a3b8;font-family:Orbitron;margin-bottom:5px;">HASHRATE (SDE)</div><div style="font-size:20px;color:#ffd700;font-weight:900;font-family:Orbitron;">💎 {round(val, -4):,}</div></div>
                        <div style="border-left:1px dashed rgba(255,255,255,0.3);"></div>
                        <div style="flex:1;"><div style="font-size:10px;color:#94a3b8;font-family:Orbitron;margin-bottom:5px;">PERCENTILE</div><div style="font-size:20px;color:#00f3ff;font-weight:900;font-family:Orbitron;">⚡ TOP {100-pct:.1f}%</div></div>
                    </div>
                    <div style="text-align:center; margin-bottom:15px;"><div style="font-size:11px; color:#a855f7; margin-bottom:8px; font-family:Orbitron;">[ SKILL TREE ]</div>{sk_h}</div>
                    <div style="text-align:center; margin-bottom:25px;">{tag_h}</div>
                    <div class="rb"><div style="font-size:11px;color:#e2e8f0;margin-bottom:5px;font-weight:bold;">SYS_WARNING: 职场风控边界</div><div style="color:{r_color};font-size:16px;font-weight:900;">{r_tag}</div></div>
                    <div class="ft"><div class="bc"></div><div style="margin-bottom:5px;font-weight:bold;">SDE DATA ELEMENT KERNEL V1.0</div><div style="color:#475569;">© {COPYRIGHT} | TX: 0x{h_code}</div></div>
                </div></div></div>
            <div id="ui">[ MINTING V1.0 HIGH-RES POSTER... ]</div><img id="img" alt="SDE Matrix V1.0" title="长按保存或分享" />
            <div id="ht" class="ht"><span style="font-size:20px;">✅</span><br><b>全息海报 (V 1.0) 强力渲染完成！</b><br><br><span style="color:#10b981;">👆 手机端请 <b>长按上方图片</b><br>即可「发送给朋友」或「保存到相册」</span></div>
            <script>setTimeout(()=>{{ if(typeof html2canvas === 'undefined') {{ document.getElementById('ui').innerHTML='❌ 渲染引擎加载失败。'; return; }} html2canvas(document.getElementById('cb'), {{scale: 2, backgroundColor: '#010308', useCORS: true, logging: false}}).then(c=>{{ document.getElementById('img').src=c.toDataURL('image/png'); document.getElementById('ui').style.display='none'; document.getElementById('img').style.display='block'; document.getElementById('ht').style.display='block'; document.getElementById('rt').remove(); }}).catch(e=>{{ document.getElementById('ui').innerHTML='⚠️ 手机内存受限，您可以直接截屏保存上方网页。'; }});}}, 1500);</script>
        </body></html>"""
        components.html(h2c_script, height=1050)

    with t_txt:
        st.code(f"【上海数据交易所 · 核心算力链上凭证 V 1.0】\n=================================\n👤 确权节点：{safe_alias}\n💎 算力估值：{round(val, -4):,} SDE\n🧬 核心架构：{mbti} ({role})\n👑 全网评级：{t_lvl} (稀缺度 {rar})\n⚡️ 算力击败：全球 TOP {100 - pct:.1f}%\n🗺️ 终极进化：{data['evolution'][2]}\n⚖️ 风控偏好：{r_tag}\n=================================\n🌐 2026 数据要素突破之年，寻找你的协同节点！\n🔗 [ V1.0 链路校验哈希: 0x{h_code[:12]} ]", language="plaintext")

    with t_json:
        export_data = {"SYS_VERSION": VERSION, "node_alias": safe_alias, "matrix_id": mbti, "role": role, "tier": t_lvl, "global_rarity": rar, "hash_signature": h_code, "asset_valuation": val, "global_percentile": pct, "metrics": res, "unlocked_skills": data['skills'], "evolution_roadmap": data['evolution'], "assigned_tasks": data['tasks'], "fatal_vulnerability": data['black_swan'], "timestamp": curr_time, "copyright": COPYRIGHT}
        st.download_button("📥 下载节点加密档案 (V1.0 .JSON)", data=json.dumps(export_data, indent=4, ensure_ascii=False), file_name=f"SDE_V1_{safe_alias}.json", mime="application/json", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("⏏ 强行切断连接并重启终端 (SYS_REBOOT)", on_click=lambda: st.session_state.clear(), type="primary", use_container_width=True)

# ==========================================
# 🛑 [ CORE 07 ] 赛博呼吸专属版权区
# ==========================================
st.markdown(f"""
    <div style='text-align:center; margin-top:80px; margin-bottom:40px; position:relative; z-index:10;'>
        <div style='color:#00f3ff !important; font-family:"Orbitron", monospace; font-size:10px; opacity:0.3; letter-spacing:6px; margin-bottom:8px;'>POWERED BY SDE KERNEL</div>
        <div style='color:#00f3ff !important; font-family:"Orbitron", monospace; font-size:10px; opacity:0.2; letter-spacing:3px; margin-bottom:30px;'>SYSTEM VERSION: {VERSION}</div>
        <div class="copyright-niliu" style="font-size: 13px; font-family: 'Noto Sans SC', sans-serif; letter-spacing: 2px; color: #00f3ff; display: inline-block; padding: 12px 30px; border-radius: 50px; border: 1px solid rgba(0,243,255,0.3); background: rgba(0,243,255,0.05); font-weight: 900; animation: neon-breathe 2.5s infinite alternate;">
            © 2026 版权归属 · <b style="font-family:'Orbitron', sans-serif; letter-spacing: 4px;">{COPYRIGHT}</b>
        </div>
    </div>
""", unsafe_allow_html=True)
