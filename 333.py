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

# --- 1. 页面与全局配置 (沉浸式全屏化) ---
st.set_page_config(
    page_title="SDE 核心算力引擎 | 确权终端 V1.0",
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

# --- 4. 万行级精简：全系 16 型人格属性矩阵 (修复 KeyError 并补全必要字段) ---
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
    # 算法自动反转寻找最佳互补节点
    p_mbti = "".join(["E" if c=="I" else "I" if c=="E" else "N" if c=="S" else "S" if c=="N" else "F" if c=="T" else "T" if c=="F" else "P" if c=="J" else "J" for c in k])
    
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
        # ✨ 修复 KeyError: 拆分出 patch 和 partner_advice 字段
        "patch": "强制引入对抗性测试与沙盒模拟，保持系统级的冗余与弹性容错。",
        "partner": f"{p_mbti} (互补型算力节点)",
        "partner_advice": "建立明确的数据交接 SOP，利用对方的优势弥补自身维度的计算盲区，形成绝对业务闭环。"
    }

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
    
    # ✨ 核心修复：统一使用 v_E 等变量名，杜绝 NameError
    def get_int(s): return int(max(15, min(100, 50 + (s * 3.5))))
    v_E, v_I = get_int(res["E"]), 100 - get_int(res["E"])
    v_S, v_N = get_int(res["S"]), 100 - get_int(res["S"])
    v_T, v_F = get_int(res["T"]), 100 - get_int(res["T"])
    v_J, v_P = get_int(res["J"]), 100 - get_int(res["J"])

    r_score = int(max(5, min(95, 50 + (-res["J"] * 2) - (res["S"] * 1.5))))
    if r_score < 35: r_tag, r_color = "绝对合规与防线兜底", "#10b981"
    elif r_score < 65: r_tag, r_color = "动态演进与灰度套利", "#ffd700"
    else: r_tag, r_color = "无界扩张与颠覆突变", "#f43f5e"

    t_taken = max(1, st.session_state.end_time - st.session_state.start_time)
    h_code = hashlib.sha256(f"{safe_alias}{mbti}{t_taken}V1.0".encode()).hexdigest().upper()
    b_height = f"V1.0-{(int(time.time()) % 1000000):06d}"
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    avg_t = t_taken / len(questions)
    dec = int(min(99, max(35, 100 - (max(0, avg_t - 2.5) * 5))))
    ext = sum(abs(v) for v in res.values()) / 40.0
    val = int(data['base_hash'] * (1 + ext * 0.4) * (0.8 + (dec/100.0) * 0.5) * (0.9 + (int(h_code[:8], 16) % 200)/1000.0) * 10000)
    pct = round(min(99.9, max(50.0, 60 + (dec * 0.3) + (ext * 10))), 1)
    valuation_str = f"{round(val, -4):,}"

    # ==========================================
    # 🖥️ 塔台级 UI 渲染开始 (分栏设计)
    # ==========================================
    st.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 15px 20px; border-radius: 8px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 20px rgba(16,185,129,0.3);">
        <div><span style="font-size: 18px; margin-right: 10px;">✅</span><span style="color: #10b981; font-weight: 900; font-size: 14px; letter-spacing: 1px;">SDE CORE NODE MINTED [ V 1.0 ]</span></div>
        <div style="color: #94a3b8; font-family: 'Orbitron', monospace; font-size: 12px; font-weight:bold;">BLOCK: #{b_height} | TX: 0x{h_code[:10]}</div>
    </div>
    """, unsafe_allow_html=True)

    tags_html_card = " ".join([f"<span style='background:rgba(0, 243, 255, 0.1); color:#00f3ff !important; border:1px solid rgba(0,243,255,0.4); padding:4px 10px; border-radius:4px; font-size:12px; font-weight:700; margin:4px; display:inline-block;'>{t}</span>" for t in data['tags']])

    st.markdown(f"""
    <div class="result-card" style="max-width: 800px; margin: 0 auto 30px auto;">
        <div class="tier-badge" style="background:{t_col}; box-shadow:0 0 15px {t_col}88;">{t_lvl}</div>
        <div class="orbitron-font" style="font-size:13px; color:#94a3b8; letter-spacing:4px; margin-bottom:15px;">SDE CORE NODE DECODED</div>
        <div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:13px; margin-bottom:5px; border-bottom:1px dashed #334155; padding-bottom:10px; display:inline-block;">AUTH_NODE: {safe_alias}</div>
        <div class="mbti-code" style="margin-top:10px;">{mbti}</div>
        <div style="font-size: 20px; font-weight: 900; color: #00f3ff !important; margin: 10px 0 15px 0; letter-spacing: 1px;">【 {role} 】</div>
        <div style="color:#e2e8f0 !important; font-size:14px; line-height:1.8; margin-bottom:15px; font-weight:400; padding:0 5px;">{data['desc']}</div>
        <div>{tags_html_card}</div>
        <div style="display:flex; justify-content:space-between; margin-top:25px; gap:10px;">
            <div style="flex:1; background:rgba(0,0,0,0.6); border:1px solid rgba(255,215,0,0.3); border-radius:8px; padding:15px; text-align:center;">
                <div style="font-size:10px; color:#94a3b8; font-family:'Orbitron', monospace; margin-bottom:4px;">ASSET VALUATION (SDE)</div>
                <div style="font-size:22px; color:#ffd700; font-weight:900; font-family:'Orbitron', sans-serif; text-shadow:0 0 10px rgba(255,215,0,0.6);">💎 {valuation_str}</div>
            </div>
            <div style="flex:1; background:rgba(0,0,0,0.6); border:1px solid rgba(0,243,255,0.3); border-radius:8px; padding:15px; text-align:center;">
                <div style="font-size:10px; color:#94a3b8; font-family:'Orbitron', monospace; margin-bottom:4px;">DECISIVENESS INDEX</div>
                <div style="font-size:22px; color:#00f3ff; font-weight:900; font-family:'Orbitron', sans-serif; text-shadow:0 0 10px rgba(0,243,255,0.6);">⚡ {dec}/100</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("⚠️ 绝密档案：系统盲点与黑天鹅压力测试 (仅本人可见)"):
        st.markdown(f"""
    <div style="padding: 5px 10px; font-size: 14px; color: #cbd5e1; line-height: 1.7;">
        <div style="color: #f43f5e; font-weight: 900; font-size: 15px; margin-bottom: 8px; border-left: 3px solid #f43f5e; padding-left: 10px;">[ 致命漏洞判定 ]</div>
        <div style="margin-bottom: 20px; padding-left: 13px;">{data['black_swan']}</div>
        <div style="color: #10b981; font-weight: 900; font-size: 15px; margin-bottom: 8px; border-left: 3px solid #10b981; padding-left: 10px;">[ 官方防狱补丁 ]</div>
        <div style="padding-left: 13px;">{data['patch']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='color:#10b981 !important; border-left:4px solid #10b981; padding-left:10px; font-weight:900; margin-top:30px;'>💡 生态网络协同指引</h4>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, rgba(16, 185, 129, 0.08), rgba(0,0,0,0)); border-left: 4px solid #10b981; padding: 20px; border-radius: 4px; font-size: 14px; line-height: 1.7; color: #e2e8f0; border-top: 1px solid rgba(16, 185, 129, 0.3); border-bottom: 1px solid rgba(16, 185, 129, 0.3); box-shadow: 0 5px 20px rgba(0,0,0,0.5); margin: 15px 0 30px 0;">
        <div style="color: #10b981; font-weight: 900; font-size: 13px; margin-bottom: 8px; font-family: 'Orbitron', sans-serif; letter-spacing: 2px;">[ 黄金并网节点 ]</div>
        <div style="margin-bottom:15px; color:#ffffff; font-weight:900; font-size:15px;">{data['partner']}</div>
        <div style="color: #10b981; font-weight: 900; font-size: 13px; margin-bottom: 8px; font-family: 'Orbitron', sans-serif; letter-spacing: 2px;">[ 协同超频建议 ]</div>
        <div>{data['partner_advice']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================
    # 🔥 防爆海报提取中心
    # ==========================
    st.markdown("<h4 style='color:#00f3ff !important; border-left:5px solid #00f3ff; padding-left:12px; font-weight:900; margin-top:40px;'>💠 链上资产提取终端 (V 1.0)</h4>", unsafe_allow_html=True)
    t_img, t_txt, t_json = st.tabs(["📸 V1.0 视网膜全息海报 (长按发圈)", "📝 纯文本通讯协议", "📥 极客 JSON 底包"])

    with t_img:
        st.markdown("<div style='font-size:13px; color:#10b981; margin-bottom:10px;'>系统已启用防爆内存引擎压制高清海报，请等待 1.5 秒...</div>", unsafe_allow_html=True)
        random.seed(h_code); g_stops = []
        for p in range(0, 100, int(random.uniform(2, 6))): g_stops.append(f"rgba(0,243,255,0.7) {p}%, rgba(0,243,255,0.7) {p+1}%, transparent {p+1}%, transparent {p+2}%")
        b_css = "linear-gradient(90deg, " + ", ".join(g_stops) + ")"
        tag_h = "".join([f'<span style="background:rgba(0,243,255,0.1); border:1px solid rgba(0,243,255,0.5); padding:4px 8px; border-radius:4px; font-size:12px; color:#00f3ff; font-weight:bold; margin:3px; display:inline-block;">{t}</span>' for t in data['tags']])
        sk_h = "".join([f'<span style="background:linear-gradient(90deg, rgba(168,85,247,0.3), rgba(168,85,247,0.1)); border:1px solid rgba(168,85,247,0.6); border-left:3px solid #a855f7; padding:4px 8px; border-radius:4px; font-size:11px; color:#e9d5ff; font-weight:bold; display:inline-block; margin:3px;">{s}</span>' for s in data['skills']])

        html_to_image_script = f"""
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
                    <div class="ft"><div class="bc"></div><div style="margin-bottom:5px;font-weight:bold;">SDE DATA ELEMENT KERNEL V1.0</div><div style="color:#475569;">© 无名逆流 | TX: 0x{h_code}</div></div>
                </div></div></div>
            <div id="ui">[ MINTING V1.0 HIGH-RES POSTER... ]</div><img id="img" alt="SDE Matrix V1.0" title="长按保存或分享" />
            <div id="ht" class="ht"><span style="font-size:20px;">✅</span><br><b>全息海报 (V 1.0) 强力渲染完成！</b><br><br><span style="color:#10b981;">👆 手机端请 <b>长按上方图片</b><br>即可「发送给朋友」或「保存到相册」</span></div>
            <script>setTimeout(()=>{{ if(typeof html2canvas === 'undefined') {{ document.getElementById('ui').innerHTML='❌ 渲染引擎加载失败。'; return; }} html2canvas(document.getElementById('cb'), {{scale: 2, backgroundColor: '#010308', useCORS: true, logging: false}}).then(c=>{{ document.getElementById('img').src=c.toDataURL('image/png'); document.getElementById('ui').style.display='none'; document.getElementById('img').style.display='block'; document.getElementById('ht').style.display='block'; document.getElementById('rt').remove(); }}).catch(e=>{{ document.getElementById('ui').innerHTML='⚠️ 手机内存受限，您可以直接截屏保存上方网页。'; }});}}, 1500);</script>
        </body></html>"""
        components.html(html_to_image_script, height=1050)

    with t_txt:
        st.code(f"【上海数据交易所 · 核心算力链上凭证 V 1.0】\n=================================\n👤 确权节点：{safe_alias}\n💎 算力估值：{round(val, -4):,} SDE\n🧬 核心架构：{mbti} ({role})\n👑 全网评级：{t_lvl} (稀缺度 {rar})\n⚡️ 算力击败：全球 TOP {100 - pct:.1f}%\n🗺️ 终极进化：{data['evolution'][2]}\n⚖️ 风控偏好：{r_tag}\n=================================\n🌐 2026 数据要素突破之年，寻找你的协同节点！\n🔗 [ V1.0 链路校验哈希: 0x{h_code[:12]} ]", language="plaintext")

    with t_json:
        export_data = {"SYS_VERSION": "1.0_ENTERPRISE", "node_alias": safe_alias, "matrix_id": mbti, "role": role, "tier": t_lvl, "global_rarity": rar, "hash_signature": h_code, "asset_valuation": val, "global_percentile": pct, "metrics": res, "unlocked_skills": data['skills'], "evolution_roadmap": data['evolution'], "assigned_tasks": data['tasks'], "fatal_vulnerability": data['black_swan'], "timestamp": curr_time, "copyright": "无名逆流"}
        st.download_button("📥 下载节点加密档案 (V1.0 .JSON)", data=json.dumps(export_data, indent=4, ensure_ascii=False), file_name=f"SDE_V1_{safe_alias}.json", mime="application/json", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("⏏ 强行切断连接并重启终端 (SYS_REBOOT)", on_click=lambda: st.session_state.clear(), type="primary", use_container_width=True)

# ==========================================
# 🛑 [ CORE 07 ] 赛博呼吸专属版权区
# ==========================================
st.markdown(f"""
    <div style='text-align:center; margin-top:80px; margin-bottom:40px; position:relative; z-index:10;'>
        <div style='color:#00f3ff !important; font-family:"Orbitron", monospace; font-size:10px; opacity:0.3; letter-spacing:6px; margin-bottom:8px;'>POWERED BY SDE KERNEL</div>
        <div style='color:#00f3ff !important; font-family:"Orbitron", monospace; font-size:10px; opacity:0.2; letter-spacing:3px; margin-bottom:30px;'>SYSTEM VERSION: 1.0_ENTERPRISE_BUILD</div>
        <div class="copyright-niliu" style="font-size: 13px; font-family: 'Noto Sans SC', sans-serif; letter-spacing: 2px; color: #00f3ff; display: inline-block; padding: 12px 30px; border-radius: 50px; border: 1px solid rgba(0,243,255,0.3); background: rgba(0,243,255,0.05); font-weight: 900; box-shadow: 0 0 20px rgba(0,243,255,0.2);">
            © 2026 版权归属 · <b style="font-family:'Orbitron', sans-serif; letter-spacing: 4px;">无名逆流</b>
        </div>
    </div>
""", unsafe_allow_html=True)
