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
VERSION = "1.0_PRO_MAX_ENTERPRISE"
COPYRIGHT = "无名逆流"
SYS_NAME = "SDE 核心人才算力引擎 | V 1.0"

# 宽屏布局，承载塔台级彭博社双栏大屏，完美兼容手机端瀑布流
st.set_page_config(page_title=SYS_NAME, page_icon="💠", layout="wide", initial_sidebar_state="collapsed")

# ==============================================================================
# 🎨 [ CORE 02 ] 赛博全息 UI 渲染底座 (全顶格书写，物理杜绝 Markdown 识别 Bug)
# ==============================================================================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;600&display=swap');

/* 强制设备内核进入暗黑模式 */
:root { color-scheme: dark; }

[data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
.block-container { padding-top: 2.5rem !important; padding-bottom: 4rem !important; max-width: 1400px !important; margin: 0 auto; overflow-x: hidden; }
html, body, .stApp { background-color: #030712 !important; font-family: 'Noto Sans SC', sans-serif !important; color: #f8fafc !important; overflow-x: hidden; }

/* 视差背景网格 */
[data-testid="stAppViewContainer"]::before { content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, rgba(0, 243, 255, 0.05) 0%, rgba(3, 7, 18, 1) 70%); pointer-events: none; z-index: 0; }
[data-testid="stAppViewContainer"]::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02)); background-size: 100% 3px, 3px 100%; z-index: 99999; pointer-events: none; opacity: 0.5; }

[data-testid="stSidebar"] { background-color: rgba(2, 6, 23, 0.95) !important; border-right: 1px solid rgba(0,243,255,0.2) !important; }

/* 文字颜色安全兜底 */
.stMarkdown, p, span, h2, h3, h4, li, label, div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { color: #f8fafc !important; }
[data-testid="stProgress"] > div > div > div { background: linear-gradient(90deg, #00f3ff, #3b82f6) !important; box-shadow: 0 0 15px rgba(0,243,255,0.8); }

/* 暴力劫持下拉框，防浅色模式反转刺眼 */
div[data-baseweb="select"] > div { background-color: rgba(4, 9, 20, 0.95) !important; border: 1px solid rgba(168, 85, 247, 0.5) !important; color: #a855f7 !important; font-weight: bold;}
div[data-baseweb="popover"] > div, div[data-baseweb="popover"] ul { background-color: #0f172a !important; border: 1px solid rgba(168, 85, 247, 0.4) !important; border-radius: 6px !important; }
div[data-baseweb="popover"] li { color: #ffffff !important; background-color: transparent !important; transition: all 0.2s ease;}
div[data-baseweb="popover"] li:hover, div[data-baseweb="popover"] li[aria-selected="true"] { background-color: rgba(168, 85, 247, 0.4) !important; color: #00f3ff !important; font-weight: bold !important; }

/* 💎 硬件加速细腻顶部交易跑马灯 */
.ticker-wrap { width: 100%; overflow: hidden; height: 32px; background-color: rgba(2, 6, 23, 0.98); border-bottom: 1px solid rgba(0,243,255,0.4); position: fixed; top: 0; left: 0; z-index: 99990; box-shadow: 0 2px 15px rgba(0,243,255,0.15); }
.ticker { display: inline-block; white-space: nowrap; padding-right: 100%; box-sizing: content-box; animation: ticker 40s linear infinite; font-family: 'Orbitron', monospace; font-size: 12px; color: #00f3ff; line-height: 32px; letter-spacing: 1px; will-change: transform; transform: translateZ(0); }
.ticker span { margin-right: 50px; } .ticker .up { color: #10b981; text-shadow: 0 0 5px rgba(16,185,129,0.5); } .ticker .down { color: #f43f5e; text-shadow: 0 0 5px rgba(244,63,94,0.5); }
@keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

/* 骇客主标题 */
.hero-title { font-size: clamp(26px, 5vw, 42px) !important; font-weight: 900 !important; text-align: center; color: #ffffff !important; letter-spacing: 4px; margin-bottom: 5px; margin-top: 15px; text-shadow: 0 0 20px rgba(0,243,255,0.7), 0 0 40px rgba(0,243,255,0.3); position: relative; display: inline-block; text-transform: uppercase; }
.hero-title::before, .hero-title::after { content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: transparent; }
.hero-title::before { left: 2px; text-shadow: -2px 0 #f43f5e; animation: glitch-anim-1 2.5s infinite linear alternate-reverse; }
.hero-title::after { left: -2px; text-shadow: 2px 0 #00f3ff; animation: glitch-anim-2 3.5s infinite linear alternate-reverse; }
@keyframes glitch-anim-1 { 0% { clip-path: inset(20% 0 80% 0); } 20% { clip-path: inset(60% 0 10% 0); } 40% { clip-path: inset(40% 0 50% 0); } 60% { clip-path: inset(80% 0 5% 0); } 80% { clip-path: inset(10% 0 70% 0); } 100% { clip-path: inset(30% 0 20% 0); } }
@keyframes glitch-anim-2 { 0% { clip-path: inset(10% 0 60% 0); } 20% { clip-path: inset(30% 0 20% 0); } 40% { clip-path: inset(70% 0 10% 0); } 60% { clip-path: inset(20% 0 50% 0); } 80% { clip-path: inset(90% 0 5% 0); } 100% { clip-path: inset(50% 0 30% 0); } }

/* 终端与游标 */
.terminal-container { background: rgba(8, 15, 30, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: clamp(15px, 4vw, 25px); border-radius: 8px; font-family: 'Fira Code', monospace; font-size: clamp(12px, 3vw, 14px); color: #e2e8f0; box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px; box-sizing: border-box;}
.term-line { opacity: 0; animation: scanFade 0.4s forwards; }
.term-line:nth-child(1) { animation-delay: 0.2s; }
.term-line:nth-child(2) { animation-delay: 0.8s; }
.term-line-main { opacity: 0; animation: scanFade 0.6s 1.6s forwards; }
@keyframes scanFade { 0% { opacity: 0; transform: translateX(-15px); filter: blur(3px); } 100% { opacity: 1; transform: translateX(0); filter: blur(0); } }
.cursor-blink { display: inline-block; width: 10px; height: 18px; background: #00f3ff; animation: blink 1s step-end infinite; vertical-align: middle; margin-left: 5px; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

/* 🚨 终极修复：输入框文字垂直居中防靠下 */
div[data-testid="stForm"] { max-width: 600px; margin: 0 auto; border: none !important; background: transparent !important;}
div[data-testid="stTextInput"] > div > div > input { background-color: rgba(4, 9, 20, 0.9) !important; color: #00f3ff !important; font-family: 'Orbitron', monospace !important; border: 1px solid rgba(0,243,255,0.5) !important; border-radius: 6px !important; text-align: center; font-size: clamp(16px, 4vw, 18px) !important; font-weight: bold !important; letter-spacing: 2px; box-shadow: inset 0 0 20px rgba(0,243,255,0.1) !important; transition: all 0.3s ease; padding: 15px !important; line-height: normal !important; box-sizing: border-box !important;}
div[data-testid="stTextInput"] > div > div > input:focus { border-color: #ffd700 !important; box-shadow: 0 0 25px rgba(255,215,0,0.4), inset 0 0 15px rgba(255,215,0,0.1) !important; transform: scale(1.02); }

div.stButton > button { background: linear-gradient(135deg, #0f172a 0%, #040914 100%) !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; border-left: 4px solid rgba(0, 243, 255, 0.6) !important; border-radius: 6px !important; min-height: 60px !important; width: 100% !important; padding: 10px 15px !important; text-align: left !important; box-shadow: 0 4px 10px rgba(0,0,0,0.4) !important; transition: all 0.2s ease !important; position: relative; overflow: hidden; }
div.stButton > button p { color: #ffffff !important; font-size: clamp(13px, 3.5vw, 15px) !important; font-weight: bold !important; white-space: normal !important; line-height: 1.4 !important; text-align: left;}
div.stButton > button:hover { border-color: #00f3ff !important; border-left: 6px solid #00f3ff !important; box-shadow: 0 0 20px rgba(0,243,255,0.3) !important; transform: translateX(4px) !important; }

div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #00f3ff, #0088ff) !important; border: none !important; text-align: center !important; }
div.stButton > button[data-testid="baseButton-primary"] p { color: #010308 !important; font-weight: 900 !important; font-size: clamp(16px, 4vw, 18px) !important; letter-spacing: 2px !important; text-align: center !important;}
div.stButton > button[data-testid="baseButton-primary"]:hover { transform: translateY(-3px) !important; box-shadow: 0 10px 30px rgba(0,243,255,0.6) !important; }

/* 大屏卡片体系 */
.result-card { padding: clamp(20px, 5vw, 40px) clamp(15px, 4vw, 30px); border-radius: 12px; background: rgba(8, 15, 30, 0.95) !important; border: 1px solid rgba(255,215,0,0.3); border-top: 6px solid #ffd700; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.8), inset 0 0 30px rgba(255,215,0,0.05); margin-bottom: 20px; position:relative; overflow:hidden;}
.mbti-code { position: relative; z-index: 2; font-family: 'Orbitron', sans-serif !important; font-size: clamp(60px, 10vw, 80px); font-weight: 900; color: #ffd700 !important; line-height: 1.1; letter-spacing: 6px; text-shadow: 0 0 35px rgba(255,215,0,0.6); margin: 5px 0;}
.tier-badge { position: absolute; top: 20px; right: -45px; background: #ffd700; color: #000; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 13px; padding: 5px 50px; transform: rotate(45deg); z-index: 10; letter-spacing: 2px; box-shadow: 0 0 20px rgba(255,215,0,0.8);}

.panel-box { background: rgba(10, 17, 32, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: clamp(15px, 4vw, 25px); box-shadow: inset 0 0 20px rgba(0,0,0,0.4); margin-bottom: 20px; box-sizing: border-box;}

/* Tabs 导航坞 */
[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: clamp(14px, 3.5vw, 16px) !important; padding-bottom: 12px !important; transition: all 0.3s ease; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #00f3ff !important; border-bottom-color: #00f3ff !important; border-bottom-width: 3px !important; text-shadow: 0 0 15px rgba(0,243,255,0.6); background: rgba(0,243,255,0.05); }

/* 折叠框与任务板 */
[data-testid="stExpander"] { background: rgba(5, 10, 21, 0.9) !important; border: 1px solid rgba(244, 63, 94, 0.5) !important; border-radius: 8px !important; overflow: hidden; margin-bottom: 20px;}
[data-testid="stExpander"] summary { background: rgba(244, 63, 94, 0.1); color: #f43f5e !important; font-weight: 900 !important; font-size: clamp(13px, 3vw, 15px) !important; padding: 15px !important; }
.mission-item { border-left: 3px solid #f43f5e; padding-left: 15px; margin-bottom: 12px; background: rgba(244,63,94,0.05); padding-top: 10px; padding-bottom: 10px; border-radius: 0 4px 4px 0; }

.cli-box { background: #000000; border: 1px solid #334155; border-left: 4px solid #00f3ff; padding: 20px; border-radius: 8px; font-family: monospace; font-size: 13px; color: #4ade80; box-shadow: inset 0 0 30px rgba(0,243,255,0.15); margin-top: 20px; word-break: break-all; line-height: 1.6;}

/* 专属下载按钮 */
div[data-testid="stDownloadButton"] > button { background: rgba(5, 12, 25, 0.95) !important; border: 1px dashed rgba(16, 185, 129, 0.8) !important; border-left: 6px solid #10b981 !important; margin-top: 20px; border-radius: 6px !important; height: 55px; text-align: center !important; width: 100% !important;}
div[data-testid="stDownloadButton"] > button p { color: #10b981 !important; font-family: 'Orbitron', monospace !important; font-weight: bold !important; letter-spacing: 2px !important; font-size: clamp(13px, 3.5vw, 15px) !important;}
div[data-testid="stDownloadButton"] > button:hover { background: rgba(16, 185, 129, 0.15) !important; box-shadow: 0 0 30px rgba(16,185,129,0.5) !important; transform: scale(1.02) !important; }

/* 💎 无名逆流专属版权呼吸灯特效 */
.copyright-niliu { display: inline-block; padding: 12px 35px; border-radius: 50px; font-size: 13px; font-family: "Noto Sans SC", sans-serif; letter-spacing: 2px; color: #00f3ff; font-weight: 900; background: rgba(0,243,255,0.05); border: 1px solid rgba(0,243,255,0.3); animation: neon-breathe 2.5s infinite alternate; box-shadow: 0 0 20px rgba(0,243,255,0.2); transition: all 0.3s ease; margin-top: 5px; cursor: default;}
.copyright-niliu:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(0,243,255,0.8), inset 0 0 15px rgba(0,243,255,0.5); border-color: #00f3ff; }
@keyframes neon-breathe { 0% { box-shadow: 0 0 10px rgba(0,243,255,0.1), inset 0 0 5px rgba(0,243,255,0.1); border-color: rgba(0,243,255,0.2); text-shadow: none; } 100% { box-shadow: 0 0 25px rgba(0,243,255,0.6), inset 0 0 15px rgba(0,243,255,0.2); border-color: rgba(0,243,255,0.7); text-shadow: 0 0 10px #00f3ff; } }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# 🧬 Web3 级 SVG 矩阵指纹生成器
def generate_identicon_svg(hash_str, base_color):
    svg_html = f'<svg viewBox="0 0 5 5" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; filter: drop-shadow(0 0 5px {base_color}88);">'
    for i in range(25):
        x = i % 5
        y = i // 5
        sym_x = x if x < 3 else 4 - x
        char_idx = (y * 3 + sym_x) % len(hash_str)
        if int(hash_str[char_idx], 16) % 2 == 0:
            svg_html += f'<rect x="{x}" y="{y}" width="1.05" height="1.05" fill="{base_color}" opacity="0.9" rx="0.1"/>'
    svg_html += '</svg>'
    return svg_html

# ==============================================================================
# 📊 [ CORE 03 ] 侧边栏与大盘动态流
# ==============================================================================
HTML_TICKER = """
<div class="ticker-wrap"><div class="ticker">
<span>SDE-CORE: V1.0 SECURE <b class="up">▲ONLINE</b></span>
<span>NODE: IMMUTABLE STATE <b class="up">▲LOCKED</b></span>
<span>ASSET-DATA-77: MINT SUCCESS <b class="up">▲14.2TH/s</b></span>
<span>SYS-RISK: THREAT BLOCKED <b class="up">▲SECURE</b></span>
<span>MARKET-ROI: VOLATILITY DETECTED <b class="down">▼WARN</b></span>
<span>CROSS-BORDER: PROTOCOL SYNC <b class="up">▲ESTABLISHED</b></span>
<span>SDE-CORE: V1.0 SECURE <b class="up">▲ONLINE</b></span>
</div></div>
"""
st.markdown(HTML_TICKER, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='text-align:center; font-family:Orbitron; font-size:24px; font-weight:900; color:#00f3ff; margin-bottom:20px; text-shadow: 0 0 15px rgba(0,243,255,0.6);'>SDE CORE V1.0</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px; color:#94a3b8; font-family:Orbitron; border-bottom:1px solid #334155; padding-bottom:5px; margin-bottom:15px; font-weight:bold;'>/// NETWORK STATUS</div>", unsafe_allow_html=True)
    
    st.metric("Total Network Hashrate", f"{random.uniform(150.0, 155.0):.2f} EH/s", f"+{random.uniform(0.5, 2.5):.2f}%")
    st.metric("Active Node Validators", f"{random.randint(8400, 8500):,}", f"+{random.randint(10, 45)}")
    st.metric("24H Data Tx Volume", f"¥ {random.uniform(12.5, 14.2):.2f} B", f"+{random.uniform(2.0, 8.0):.2f}%")
    
    st.markdown("<div style='font-size:11px; color:#94a3b8; font-family:Orbitron; border-bottom:1px solid #334155; padding-bottom:5px; margin-top:30px; margin-bottom:15px; font-weight:bold;'>/// LIVE TX LOGS</div>", unsafe_allow_html=True)
    
    if "sidebar_logs" not in st.session_state:
        st.session_state.sidebar_logs = "".join([f"<div style='font-family:\"Fira Code\", monospace; font-size:10px; margin-bottom:12px; border-left:2px solid #10b981; padding-left:8px;'><span style='color:#10b981;'>[MINT]</span> <span style='color:#e2e8f0;'>{random.choice(['Gov_Public_Data', 'Med_Research_Set', 'Fin_Risk_API', 'Logistics_GPS', 'Retail_Behavior'])}</span><br><span style='color:#ffd700;'>GAS: {random.randint(12000,45000)} Gwei</span></div>" for _ in range(6)])
    st.markdown(st.session_state.sidebar_logs, unsafe_allow_html=True)

# ==============================================================================
# 🧠 [ CORE 04 ] 题库全量无损归位：40 道极客业务题库 (绝不删减)
# ==============================================================================
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
    {"q": "在评估一项数据资源入表案例时，我会死磕财务科目映射、摊销年限与合规确权等底层细节。", "dim": "S"},
    {"q": "我更信任交易大盘上的真实成交曲线与存证笔数，而不是研究报告中那些定性的宏观趋势预判。", "dim": "S"},
    {"q": "当听到“隐私计算”、“可信数据空间”等前沿概念时，我最先关心的是它在 SDE 现有机房和架构里如何具体落地。", "dim": "S"},
    {"q": "我认为数据交易所当前最核心的任务是把“确权、存证、交付、清算”的每一个动作做到极致的规范与零差错。", "dim": "S"},
    {"q": "审核数据产品上架时，我严格依赖合规审查操作清单，极度排斥带有主观弹性的价值评估。", "dim": "S"},
    {"q": "相比于畅想 2026 年全国数据统一大市场的宏伟蓝图，我更关心下个季度的结算系统并发量和撮合效率能否提升。", "dim": "S"},
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
    {"q": "我的云盘文件夹、数据工作文档拥有严丝合缝的分类与命名逻辑，任何文件乱放都会让我感到极度不适。", "dim": "J"},
    {"q": "如果一场跨部门业务讨论会没有形成明确的会议纪要、SOP决议和责任人，我会认为这是在严重浪费时间。", "dim": "J"},
    {"q": "我倾向于在系统开发初期就锁定所有的核心业务需求，对中途频繁变更“数据产品业务形态”持强烈排斥态度。", "dim": "J"},
    {"q": "即便面临极高压的交易旺季，我也坚持每天下班前进行工作复盘，并雷打不动地更新第二天的待办任务清单。", "dim": "J"},
    {"q": "数据交易所的日常运营应当“重制度设计、轻即兴发挥”，哪怕这会让我们在应对短期市场热点时显得不够快。", "dim": "J"},
    {"q": "我几乎从不拖延核心审批或交付任务，因为“未决事项”停留在待办清单上，会带给我无形的心理重压。", "dim": "J"},
    {"q": "我更喜欢规则清晰、节奏稳定、可预测的工作环境，而不是每天都在“救火”和处理无法预知的突发创新需求。", "dim": "J"},
    {"q": "为了确保向上级或监管交付的数据分析报告万无一失，我总是会刻意提前预留出至少 20% 的缓冲检查时间。", "dim": "J"},
    {"q": "面对多线并行的复杂任务（如同时筹备路演与审核规则），我必须先向领导确认优先级并排好序，否则绝对无法安心执行。", "dim": "J"}
]

# 🚨 18 维满血防爆字典 (无损保留所有 txt 文本描述)
mbti_details = {
    "INTJ": {
        "role": "首席数据架构师", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 1.2%", "base_hash": 9850,
        "desc": "数据要素底座的“造物主”，致力于为错综复杂的数字经济构建严密的底层制度与逻辑规则。",
        "tags": ["顶层设计", "逻辑闭环", "制度自信"], 
        "partner": "ENTJ (高效执行统筹) / INTP (极客算法节点)",
        "partner_advice": "将战略落地全权交由 ENTJ 推进，把 INTP 作为高维模型的逻辑验算机，您只需稳控全局架构不跑偏。",
        "tasks": ["主导 SDE 核心确权底层逻辑架构设计", "重构下一代高并发撮合交易引擎逻辑"],
        "black_swan": "过度追求底层架构完美闭环。面临突发政策转向时，系统极易因过于重型而无法敏捷掉头。",
        "patch": "在构建宏大的交易规则体系时，请适当为前台业务预留“沙盒容错”空间；捕获一线的非结构化反馈，能让制度更具生命力。",
        "evolution": "【绝对算力主宰】掌控数据产品的终极业务定价权"
    },
    "INTP": {
        "role": "量化风控专家", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 3.1%", "base_hash": 9620,
        "desc": "穿透数据迷雾，寻找复杂业务表象下的底层逻辑漏洞与确权定价模型的最优解。",
        "tags": ["深度解构", "模型驱动", "极客思维"], 
        "partner": "INTJ (架构锚定节点) / ENTP (模式发散节点)",
        "partner_advice": "依托 INTJ 将您的理论模型锚定在现实业务框架内，并借助 ENTP 的发散思维寻找商业变现出口。",
        "tasks": ["研发基于特征因子的数据资产动态定价算法", "建立实时数据异常交易嗅探与阻断模型"],
        "black_swan": "陷入“分析瘫痪”。在需要极速拍板的确权灰度地带，过度追求模型最优解往往导致商机流失。",
        "patch": "尝试将您极其高维的理论模型降维封装，形成非技术人员也能看懂的《操作指南》，让算法模型转化为生产力。",
        "evolution": "【全知算法先知】构建百分百无损的跨网底层风控引擎"
    },
    "ISTJ": {
        "role": "合规审查主理官", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 11.6%", "base_hash": 8850,
        "desc": "SDE 底层防线的守夜人，您的评估本身就是安全、严谨与业务零失误的代名词。",
        "tags": ["绝对合规", "程序正义", "风险兜底"], 
        "partner": "ESTJ (业务推进节点) / ISFJ (后勤保障节点)",
        "partner_advice": "配合 ESTJ 建立坚不可摧的业务推进流水线，由 ISFJ 负责兜底后勤细节，形成最硬核的交付闭环。",
        "tasks": ["主导头部数商“数据资源入表”全链路审计", "设计业务合同与智能合约的合规映射SOP"],
        "black_swan": "过度依赖既有 SOP。面临无先例创新业务时，容易因“无库可查”产生本能的排斥与误杀。",
        "patch": "在死守数据合规红线的同时，面对狂飙突进的创新产品，试着用“如何让它合规地上架”来指导业务。",
        "evolution": "【绝对防御壁垒】全国一体化数据市场要素流转网络的终极守门人"
    },
    "ESTJ": {
        "role": "核心业务统筹官", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 8.7%", "base_hash": 9500,
        "desc": "无可争议的推进器，擅长将国家宏观政策拆解为团队可绝对执行的 KPI 矩阵。",
        "tags": ["强效统帅", "结果导向", "流程大师"], 
        "partner": "ISTJ (合规审查节点) / ISTP (应急排障节点)",
        "partner_advice": "让 ISTJ 担任您的品控质检员，在突发高并发危机时，直接将排障指挥权临时移交给 ISTP。",
        "tasks": ["发起并统筹 SDE 年度交易额破局百亿攻坚战", "强力调度跨部门资源打通确权交易清算堵点"],
        "black_swan": "KPI压倒一切导致“团队算力过载”。强推项目时易忽视一线团队的情绪阈值，引发内耗。",
        "patch": "在下发高压任务指令时，适度向团队释放“情绪价值”。具备高信任感的团队往往比单纯的数字目标走得更稳健。",
        "evolution": "【全域秩序引擎】宏观数据业务推进的心脏中枢"
    },
    "INFJ": {
        "role": "产业生态智囊", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 0.9%", "base_hash": 9200,
        "desc": "具备极强的跨频段共情能力，能精准预判数据流转对未来实体经济产生的深远变革。",
        "tags": ["远见卓识", "使命驱动", "战略前瞻"], 
        "partner": "ENFJ (共识布道节点) / ENFP (火种传播节点)",
        "partner_advice": "将您的远见卓识交由 ENFJ 在核心圈层构建共识，让 ENFP 作为布道火种将您的理念扩散至全行业。",
        "tasks": ["规划 SDE 未来五年在实体经济的数据赋能版图", "发起“数据向善”及社会公益数据要素流通倡议"],
        "black_swan": "强烈的战略直觉若缺乏硬核量化数据支撑，向实干型领导汇报时极易被贴上“不切实际”标签。",
        "patch": "学会用精确的财务测算、合规条文来锚定您的宏大产业愿景。将“先知直觉”转化为具体的业务政策专报。",
        "evolution": "【全域生态先知】主导数字经济时代的底层精神共识"
    },
    "INFP": {
        "role": "生态价值主张官", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 4.4%", "base_hash": 8650,
        "desc": "冷酷数据背后的灵魂捕捉者，擅长在机械的交易网络中注入引人共鸣的生态文化。",
        "tags": ["价值感召", "组织粘合", "品牌定调"], 
        "partner": "ENFJ (外部护航节点) / ISFP (美学交互节点)",
        "partner_advice": "依托 ENFJ 的手腕在跨部门博弈中为您护航，联合 ISFP 将抽象的文化主张具象化为绝美的视觉产品。",
        "tasks": ["重塑 SDE 在数据交易领域的全球品牌叙事", "实施内部文化与跨部门协作协同凝聚力工程"],
        "black_swan": "在跨部门冷酷的算力与预算博弈中，容易因厌恶冲突而退缩，导致核心价值观无法落地。",
        "patch": "在跨部门协同博弈中，学会熟练利用预算工具和业务导向来捍卫您的核心价值主张，将柔性文化转化为硬性资产。",
        "evolution": "【灵魂共振奇核】赋予极客冷数据极其昂贵的品牌溢价"
    },
    "ENTJ": {
        "role": "战略开拓领军人", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 1.8%", "base_hash": 9900,
        "desc": "天生的矩阵建设者，在数据跨境、公共数据授权等探索区中展现极强的破局能力。",
        "tags": ["开疆拓土", "战略铁腕", "极致破局"], 
        "partner": "INTJ (战略智囊节点) / ISTP (技术攻坚节点)",
        "partner_advice": "冲锋时将后背交给 INTJ 进行战略兜底，遇到底层技术阻击时，立刻呼叫 ISTP 进行定点爆破。",
        "tasks": ["主导“公共数据授权运营”省级破冰与资源抢占", "制定并执行跨链互认及全国数据大市场吞并战略"],
        "black_swan": "狂飙突进时的风控盲区。在极速吞并外部资源时极易因忽视底层合规红线而触发监管熔断。",
        "patch": "在极速开疆拓土时，请时刻保持与合规团队的数据同步。有时放慢半拍听听风控预警，能避开系统性风险。",
        "evolution": "【无界版图霸主】全国一体化数据市场的超级统帅"
    },
    "ENTP": {
        "role": "模式创新顾问", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 3.2%", "base_hash": 9400,
        "desc": "传统交易规则的敏锐挑战者，致力于通过跨界思维寻找下一代数据要素流转范式。",
        "tags": ["范式重构", "逻辑激辩", "思维跳跃"], 
        "partner": "INTP (逻辑验证节点) / ESTP (市场收割节点)",
        "partner_advice": "把您天马行空的狂野点子丢给 INTP 进行逻辑降维，并指挥 ESTP 去市场上快速收割第一波红利。",
        "tasks": ["研发首个基于 Web3 的新型数据要素凭证通证", "在监管沙盒内主导蓝海型数字产品变现测试"],
        "black_swan": "无限发散思维导致的交付烂尾。若缺乏强力的落地跟进节点，极易沦为纯粹的纸上谈兵。",
        "patch": "适当收敛发散思维，选择一个极具潜力的创新点（如特定行业数据凭证），深度闭环跟进至最终交付。",
        "evolution": "【范式秩序破坏者】亲手定义下个十年的交易元规则"
    },
    "ENFJ": {
        "role": "数商生态总监", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 2.5%", "base_hash": 9350,
        "desc": "数据交易所的枢纽中心，能通过卓越的共识构建能力将多方利益竞争者聚拢为盟友。",
        "tags": ["关系枢纽", "温情领导力", "利益协同"], 
        "partner": "INFJ (深度研究节点) / ESFJ (落地协同节点)",
        "partner_advice": "汲取 INFJ 的深度产业洞察作为布道弹药，并由 ESFJ 将您的宏观共识转化为具体的客情跟进单。",
        "tasks": ["构建辐射全国的 SDE 头部数商与第三方服务联盟", "维稳数据要素多边市场，调解核心生态伙伴冲突"],
        "black_swan": "对生态伙伴过度包容。处理违规事件时容易被“人情”裹挟，从而损害交易所的绝对中立性。",
        "patch": "在协调多方利益分配时，大胆引入客观的量化算法与智能合约刚性指标，确保“生态和谐”建立在规则基石之上。",
        "evolution": "【共识引力波】垄断全国超头数据商的绝对心智"
    },
    "ENFP": {
        "role": "平台资源布道大使", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 8.1%", "base_hash": 8900,
        "desc": "充满感染力的生态火苗，让每一场路演与推介都变成数据要素市场的狂热共识。",
        "tags": ["无限创意", "跨界纽带", "高频驱动"], 
        "partner": "INFJ (导航纠偏节点) / INTJ (架构落地节点)",
        "partner_advice": "在您的创意发散即将失控时，请务必听从 INFJ 的战略纠偏，并强迫自己遵循 INTJ 设定的节点框架。",
        "tasks": ["领衔 SDE 全国核心城市业务路演与生态宣发大循环", "策划并主持面向千家数商的“数据赋能创新工坊”"],
        "black_swan": "缺乏结构化数据追踪。路演现场火热但无法转化为 CRM 里的真实入驻率，商业核算价值打折。",
        "patch": "引入严密的商机日程表与里程碑管理。将您天马行空的生态创意转化为可追踪的业务转化漏斗。",
        "evolution": "【无界传播基站】把控国家全域要素市场的流量高地"
    },
    "ISFJ": {
        "role": "清结算运营中枢", "tier": "R", "tier_color": "#3b82f6", "rarity": "Top 13.8%", "base_hash": 8200,
        "desc": "最坚韧的底层支点，通过极致纠错与细节控场支撑起整个平台的专业信誉与高吞吐。",
        "tags": ["极致支撑", "服务巅峰", "高可用节点"], 
        "partner": "ESFJ (对外链接节点) / ISTJ (合规审核节点)",
        "partner_advice": "将对外的复杂客情交由 ESFJ 抵挡，您只需与 ISTJ 背靠背，打造坚不可摧的后方清结算堡垒。",
        "tasks": ["保障全天候撮合及大额资金清结算体系 0 宕机", "极速响应并闭环处理生态节点与数商的底层工单"],
        "black_swan": "默默承受过载的技术债。不善于向上抗议，可能在交易洪峰期因人工审核量爆表而面临崩溃。",
        "patch": "在完美支撑中后台运转之余，尝试主动提出冗余流程的优化提案。您的实操痛点极具价值。",
        "evolution": "【绝对永动节点】维持交易所生命线的最终坚盾"
    },
    "ESFJ": {
        "role": "政企商务枢纽", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 12.3%", "base_hash": 8750,
        "desc": "超级连接器，擅长经营多维度的外部政企生态关系，是前线业务部门的最强润滑剂。",
        "tags": ["协作典范", "客情控制", "社会化支撑"], 
        "partner": "ISFJ (精细支持节点) / ESTJ (宏观决策节点)",
        "partner_advice": "在前线维护八方客情时，把繁杂的合同流转放心抛给 ISFJ，遇到合规红线问题立刻请 ESTJ 强硬回绝。",
        "tasks": ["高频维护国家部委及地方大数据局的核心 G 端客情", "统筹落地具有全国影响力的年度数据要素高峰论坛"],
        "black_swan": "过度满足多方诉求导致的边界失守。极易因“谁都想讨好”而签下严重偏离平台底线的协议。",
        "patch": "在维护复杂商务生态时，建立更独立的合规风险过滤网。在照顾合作方诉求时保持底线清醒。",
        "evolution": "【政企超导桥梁】构筑不可替代的 G 端业务护城河"
    },
    "ISTP": {
        "role": "平台风控与排障专家", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 5.4%", "base_hash": 8950,
        "desc": "数据底座的实干派，只对事实和逻辑代码负责，是系统面临大并发技术故障时的定海神针。",
        "tags": ["极简实干", "故障排查", "硬核运维"], 
        "partner": "ESTP (前线实战节点) / INTP (算法优化节点)",
        "partner_advice": "当 ESTP 在前线疯狂接单导致系统过载时，由您负责底层扩容，并与 INTP 联手重构最优并发算法。",
        "tasks": ["执行 SDE 核心交易链路的灾备拉起与物理级排障", "在不影响前台撮合的前提下执行底层架构高危热更新"],
        "black_swan": "技术彻底黑盒化。过度依赖个人的“极客直觉”排障，一旦休假离线会导致整个系统应急瘫痪。",
        "patch": "尝试将您极度内隐的底层排查经验，沉淀为可视化的《应急响应标准手册》。打破沟通壁垒。",
        "evolution": "【底层代码幽灵】掌控国家要素机房的绝对生命力"
    },
    "ISFP": {
        "role": "资产交互体验官", "tier": "R", "tier_color": "#3b82f6", "rarity": "Top 8.8%", "base_hash": 8150,
        "desc": "赋予枯燥数据以美学权重，致力于提升数据产品在终端大屏展示时的绝对视觉专业质感。",
        "tags": ["审美溢价", "感官叙事", "体验极致"], 
        "partner": "ESFP (公众表达节点) / INFP (共情叙事节点)",
        "partner_advice": "将您的美学产出交由 ESFP 在各大峰会上高调发布，并从 INFP 构筑的生态故事中汲取设计灵感。",
        "tasks": ["重构 SDE 实时交易大盘的动态数据全息视觉渲染", "主导面向数商终端的 UI/UX 操作流敏捷体验升级"],
        "black_swan": "陷入纯粹形式主义。设计出极其炫酷的大屏，却完全脱离了“数据确权撮合”的核心商业逻辑。",
        "patch": "在追求终端展示的美学溢价时，适度增加对核心确权流转逻辑和底层交易协议的理解。",
        "evolution": "【感官具象师】以一己之力拉升数据产品视觉溢价"
    },
    "ESTP": {
        "role": "前沿敏捷先锋", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 4.3%", "base_hash": 8800,
        "desc": "数据流通一线的敏锐猎手，能极快捕捉到瞬息万变的市场红利与应用空间的套利机会。",
        "tags": ["市场直觉", "敏捷收割", "实战专家"], 
        "partner": "ISTP (底层兜底节点) / ENTJ (战略统筹节点)",
        "partner_advice": "尽情在市场前线厮杀套利，让 ISTP 为您搭建最稳固的技术跳板，遇到僵局迅速呼叫 ENTJ 支援。",
        "tasks": ["敏锐收割新政策出台后的第一波“短期数据流通红利”", "针对区域内竞所的市场抢夺发起极速实战反制突击"],
        "black_swan": "为了极速促成首单，倾向于利用捷径绕过繁琐的合规防火墙，一旦溯源出瑕疵将面临毁灭性反噬。",
        "patch": "在捕捉市场瞬时机遇、展现高效行动力促成交易时，务必将前置合规审查纳入操作流程中。",
        "evolution": "【极速套利猎手】全网数据交易套利空间的绝杀狙击者"
    },
    "ESFP": {
        "role": "官方品牌发声信标", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 9.9%", "base_hash": 8300,
        "desc": "交易所的前台形象窗口，天生具备将复杂的政策解码为大众传播话术的超级天赋。",
        "tags": ["全域表现", "舆情响应", "公关信标"], 
        "partner": "ISFP (视觉美学节点) / ENFP (创意破局节点)",
        "partner_advice": "用您极具感染力的表现为 ISFP 的视觉产品带货，并与 ENFP 联手策划能掀起全网狂潮的顶级路演。",
        "tasks": ["在全网引爆 SDE 最新明星数据产品的展会级宣发流量", "冲在第一线对冲平台突发的负面市场舆情并进行柔性公关"],
        "black_swan": "由于对底层条款理解深度不够，对外宣发时极易出现“用词越界”，引发监管舆情风险。",
        "patch": "花时间深潜研究数据要素的底层逻辑与政策红头文件。将您的绝佳表现力建立在扎实的产业根基上。",
        "evolution": "【极速情绪信标】左右资本市场情绪波动的首席发声端"
    }
}

# 🛡️ 自动打补丁：在后台无损注入 18 维高阶属性，彻底闭环 JSON 导出报错
patch_data = {
    "INTJ": {"skills": ["全局视野(Lv.Max)", "数据解构", "生态共振"], "base_roi": 1.45, "volatility": 0.20, "market_style": "宏观架构对冲与长期趋势跟踪策略", "evolution_path": ["L1 架构规划官", "L2 核心规则主理人"]},
    "INTP": {"skills": ["特征抽取(Lv.Max)", "漏洞侦测", "异动推演"], "base_roi": 1.60, "volatility": 0.45, "market_style": "高频统计套利与多因子量化模型", "evolution_path": ["L1 风控分析师", "L2 模型主理人"]},
    "ISTJ": {"skills": ["合规映射(Lv.Max)", "程序正义", "风险阻断"], "base_roi": 1.15, "volatility": 0.10, "market_style": "绝对风险厌恶与固收类稳健策略", "evolution_path": ["L1 审查风控官", "L2 规则执行官"]},
    "ESTJ": {"skills": ["目标拆解(Lv.Max)", "资源调度", "铁腕压制"], "base_roi": 1.35, "volatility": 0.25, "market_style": "动量突破与大容量核心资产配置", "evolution_path": ["L1 战区指挥官", "L2 跨域推进者"]},
    "INFJ": {"skills": ["战略先知(Lv.Max)", "跨频共情", "信仰织网"], "base_roi": 1.55, "volatility": 0.35, "market_style": "宏观周期预判与长线价值发现", "evolution_path": ["L1 行业分析师", "L2 战略规划官"]},
    "INFP": {"skills": ["文化塑形(Lv.Max)", "灵魂叙事", "隐性品牌溢价"], "base_roi": 1.25, "volatility": 0.30, "market_style": "ESG 价值投资与利基市场长尾策略", "evolution_path": ["L1 体验叙事者", "L2 品牌调性官"]},
    "ENTJ": {"skills": ["铁腕破局(Lv.Max)", "全域吞并", "降维打击"], "base_roi": 1.70, "volatility": 0.55, "market_style": "杠杆并购、特殊机会与高举高打", "evolution_path": ["L1 开拓先锋", "L2 战区统帅"]},
    "ENTP": {"skills": ["范式重塑(Lv.Max)", "跨界骇入", "逻辑破壁"], "base_roi": 1.65, "volatility": 0.60, "market_style": "风险套利、期权重组与颠覆性投资", "evolution_path": ["L1 沙盒破坏者", "L2 跨界重组官"]},
    "ENFJ": {"skills": ["共识结盟(Lv.Max)", "温情统御场", "利益平衡"], "base_roi": 1.40, "volatility": 0.25, "market_style": "庞大资产池宏观调配与网络效应增强", "evolution_path": ["L1 渠道统筹", "L2 联盟主理人"]},
    "ENFP": {"skills": ["情绪煽动(Lv.Max)", "流量黑洞", "资源嫁接"], "base_roi": 1.40, "volatility": 0.40, "market_style": "高波动趋势追逐与注意力经济炒作", "evolution_path": ["L1 宣发先锋官", "L2 流量矩阵中枢"]},
    "ISFJ": {"skills": ["极限并发支撑(Lv.Max)", "毫米级纠错", "绝对防线"], "base_roi": 1.10, "volatility": 0.08, "market_style": "极低回撤避险与无风险套利策略", "evolution_path": ["L1 运营专员", "L2 平台质检官"]},
    "ESFJ": {"skills": ["超级链接(Lv.Max)", "社会化缓冲网", "负载均衡"], "base_roi": 1.20, "volatility": 0.15, "market_style": "庞大资金盘稳健配置与政企引导基金模式", "evolution_path": ["L1 商务专员", "L2 政企主理"]},
    "ISTP": {"skills": ["物理拔线(Lv.Max)", "黑盒破解", "极客直觉"], "base_roi": 1.35, "volatility": 0.35, "market_style": "事件驱动、困境反转与系统级技术套利", "evolution_path": ["L1 底层架构师", "L2 灾备指挥官"]},
    "ISFP": {"skills": ["感官叙事(Lv.Max)", "美学重构", "心流捕获"], "base_roi": 1.18, "volatility": 0.22, "market_style": "艺术品级别非标资产与另类投资估值", "evolution_path": ["L1 UI视觉专员", "L2 交互总监"]},
    "ESTP": {"skills": ["瞬时收割(Lv.Max)", "火力覆盖", "红利嗅探"], "base_roi": 1.50, "volatility": 0.50, "market_style": "超高频日内交易与极限突发利好收割", "evolution_path": ["L1 突击交易员", "L2 战地狼王"]},
    "ESFP": {"skills": ["舆论控场(Lv.Max)", "全域调控", "危机降维"], "base_roi": 1.35, "volatility": 0.38, "market_style": "舆论驱动、社交媒体共振与情绪面交易", "evolution_path": ["L1 品牌代言", "L2 首席发言人"]}
}
for k, v in mbti_details.items():
    if k in patch_data: v.update(patch_data[k])

# 🤝 协同与 K 线算法
def calculate_synergy(m1, m2):
    diff = sum(1 for a, b in zip(m1, m2) if a != b)
    if diff == 0: return 92, "【绝对镜像】决策回路高度一致，沟通0延迟，但需警惕盲区重叠。"
    elif diff == 1: return 98, "【黄金并网】核心逻辑一致且具备极佳微调互补性，堪称最强推土机小队！"
    elif diff == 2: return 85, "【灰度容错】视角存在差异，能通过激烈碰撞打磨出更抗风险的业务闭环。"
    elif diff == 3: return 65, "【高频摩擦】存在极大的底层通信壁垒，协同作业必须强制引入第三方确立中间协议。"
    else: return 99, "【阴阳反转】底层代码完全相反！日常沟通极度痛苦，但若各司其职，能实现无死角包抄！"

def generate_alpha_curve(base_roi, volatility, seed):
    rng = np.random.RandomState(seed) 
    days = [f"T+{i}" for i in range(1, 31)] 
    roi = [100.0]
    for _ in range(29): roi.append(max(30.0, roi[-1] + (base_roi - 1.0) * 8 + rng.normal(0, volatility * 25)))
    return days, roi

# ==============================================================================
# ⚙️ [ CORE 05 ] 极速状态机管理 (🔐 核心不可篡改锁)
# ==============================================================================
for key, init_val in [('started', False), ('current_q', 0), ('start_time', None), ('end_time', None), ('calculating', False), ('user_alias', "Compliance_Wu"), ('total_scores', {"E": 0, "S": 0, "T": 0, "J": 0}), ('anim_played', False), ('boot_played', False)]:
    if key not in st.session_state: st.session_state[key] = init_val

def start_assessment_callback():
    alias = st.session_state.login_input.strip()
    st.session_state.user_alias = html.escape(alias) if alias else "Compliance_Wu"
    st.session_state.started = True
    st.session_state.start_time = time.time()

def answer_callback(val, dim):
    st.session_state.total_scores[dim] += (val - 3)
    st.session_state.current_q += 1
    if st.session_state.current_q >= len(questions):
        st.session_state.end_time = time.time()
        st.session_state.calculating = True

def center_container(): return st.columns([1, 2, 1])[1]

# ==============================================================================
# 🖥️ [ CORE 06 ] 塔台级路由与全息仪表盘渲染
# ==============================================================================
if not st.session_state.started:
    st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
    
    # 🎬 满血开机动画 (纯顶格无缩进防截断)
    if not st.session_state.boot_played:
        HTML_BOOT = """
<style>
.sys-boot-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100dvh; background: #030712; z-index: 9999999; display: flex; justify-content: center; align-items: center; flex-direction: column; animation: sys-boot-fade 1.5s 1s cubic-bezier(0.8, 0, 0.2, 1) forwards; pointer-events: none; }
.sys-boot-logo { color: #00f3ff; font-family: 'Orbitron', monospace; font-size: 24px; font-weight: 900; letter-spacing: 4px; overflow: hidden; border-right: 3px solid #00f3ff; white-space: nowrap; animation: typing-boot 0.8s steps(20, end) forwards, blink-boot 0.4s step-end infinite; }
.sys-boot-bar-bg { width: 260px; height: 2px; background: rgba(0,243,255,0.1); margin-top: 20px; position: relative; }
.sys-boot-bar-fill { position: absolute; top: 0; left: 0; height: 100%; background: #00f3ff; box-shadow: 0 0 15px #00f3ff; animation: load-boot 1s ease-out forwards; }
@keyframes typing-boot { from { width: 0; } to { width: 300px; } }
@keyframes blink-boot { 50% { border-color: transparent; } }
@keyframes load-boot { 0% { width: 0%; } 100% { width: 100%; } }
@keyframes sys-boot-fade { to { opacity: 0; visibility: hidden; } }
</style>
<div class="sys-boot-overlay"><div class="sys-boot-logo">SDE_KERNEL_V1.0</div><div class="sys-boot-bar-bg"><div class="sys-boot-bar-fill"></div></div></div>
"""
        st.markdown(HTML_BOOT, unsafe_allow_html=True)
        st.session_state.boot_played = True

    with center_container():
        HTML_TITLE = """
<div style="text-align: center; margin-bottom: 20px;">
<div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:14px; letter-spacing:8px; margin-bottom:10px;">SHANGHAI DATA EXCHANGE</div>
<h1 class="hero-title" data-text="职场算力终端 V 1.0">职场算力终端 V 1.0</h1><br>
<div style="color:#00f3ff; font-family:'Orbitron', sans-serif; font-size:13px; font-weight:700; letter-spacing:6px; margin-bottom:30px;">PRO_MAX_FINAL</div>
</div>
"""
        st.markdown(HTML_TITLE, unsafe_allow_html=True)

        HTML_TERM = """
<div class="terminal-container">
<div class="term-line"><span style="color:#94a3b8;">[SYSTEM]</span> Securing root connection to SDE Ledger... <span style="color:#00f3ff;">[ESTABLISHED]</span></div>
<div class="term-line"><span style="color:#94a3b8;">[KERNEL]</span> Loading 40-Node Matrix Algorithm V1.0... <span style="color:#00f3ff;">[READY]</span></div>
<div class="term-line-main">
<span style="color:#ffffff; font-size: 15px; font-family: 'Noto Sans SC', sans-serif; line-height: 1.8;">
<br><b>2026年是数据要素价值释放的突破之年。</b><br><br>
在“数据乘数”加速赋能实体经济的当下，本终端将全方位扫描您的职场决策链路与风控模型。<br>
您的物理能力将被<b>「全息要素化」</b>，系统将为您生成不可篡改的<b>高阶职场算力凭证与智能合约面板</b>。</span>
<span class="cursor-blink"></span>
</div>
</div>
"""
        st.markdown(HTML_TERM, unsafe_allow_html=True)

        with st.form(key="login_form", border=False):
            st.markdown("<div style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:bold; margin-bottom:8px; text-align:center;'>▼ MOUNT NODE IDENTIFIER (输入授权节点代号) ▼</div>", unsafe_allow_html=True)
            st.text_input("", key="login_input", placeholder="例如：Compliance_Wu", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            st.form_submit_button("▶ 同意算力测试并提取模型特征", on_click=start_assessment_callback, type="primary", use_container_width=True)

elif st.session_state.calculating:
    with center_container():
        # 🎬 ZK-Proof 零知识证明加载矩阵动效
        st.markdown("<h2 class='hero-title' data-text='[ ZK-PROOF SYNCING... ]' style='font-size:clamp(20px, 4vw, 28px) !important; margin-top:50px; text-align:center; display:block;'>[ ZK-PROOF SYNCING... ]</h2>", unsafe_allow_html=True)
        mint_box = st.empty()
        h_logs = ""
        phases = ["[SYNCING EVM]", "[EXTRACTING]", "[ZK-PROOF]", "[MINTING SBT]"]
        for i in range(12):
            fake_hash = hashlib.sha256(str(random.random()).encode()).hexdigest().upper()
            phase = phases[i % 4]
            h_logs = f"<span style='color:#94a3b8;'>{phase}</span> <span style='color:#ffd700;'>0x{fake_hash[:24]}...</span> <span style='color:#10b981;'>[OK]</span><br>" + h_logs
            mint_box.markdown(f"<div class='cli-box' style='height:250px; overflow:hidden; border-color:#ffd700;'>{h_logs}</div>", unsafe_allow_html=True)
            time.sleep(0.15)
        st.session_state.calculating = False
        st.rerun()

elif st.session_state.current_q < len(questions):
    with center_container():
        q_data = questions[st.session_state.current_q]
        dim_map = {"E": "ECO_NETWORK / 外联协同网络", "S": "EXEC_GRANULAR / 颗粒实务穿透", "T": "RISK_QUANT / 客观量化风控", "J": "ORDER_ARCH / 秩序架构锚定"}
        module_name = dim_map.get(q_data['dim'])
        dynamic_hash = hashlib.sha256(f"BLOCK_{st.session_state.current_q}_{q_data['q']}".encode()).hexdigest()[:10].upper()
        
        st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
        progress_val = (st.session_state.current_q + 1) / len(questions)
        st.progress(progress_val)
        st.markdown(f"<div style='text-align:right; font-family:Orbitron, monospace; color:#00f3ff; font-size:12px; margin-top:5px;'>MINTING PROCESS: {int(progress_val*100)}%</div>", unsafe_allow_html=True)
        
        HTML_Q = f"""
<div style="background: rgba(10, 15, 25, 0.9); border: 1px solid rgba(0, 243, 255, 0.4); border-radius: 8px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 20px rgba(0, 243, 255, 0.05); margin-top: 20px; margin-bottom: 30px; border-left: 5px solid #00f3ff;">
<div style="display:flex; justify-content:space-between; font-family:monospace; color:#00f3ff; font-size:12px; margin-bottom:15px; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom:10px;">
<span class="orbitron-font">SYS_MOD: {module_name}</span>
<span class="orbitron-font">HASH: 0x{dynamic_hash}</span>
</div>
<div style="font-size: 18px; color: #ffffff !important; line-height: 1.8; font-weight: 700;">{q_data['q']}</div>
</div>
"""
        st.markdown(HTML_Q, unsafe_allow_html=True)
        
        opts = [("🚫 [ 强制阻断 ] 危险：完全背离我的直觉", 1), ("⚠️ [ 弱态耦合 ] 降级：仅在极端场景才用", 2), ("⚖️ [ 视境判定 ] 悬空：视具体业务环境而定", 3), ("🤝 [ 逻辑握手 ] 安全：常用的标准决策流", 4), ("🔒 [ 绝对锁定 ] 同步：完美复刻底层思维", 5)]
        for text, val in opts: st.button(text, type="secondary", key=f"q_{st.session_state.current_q}_{val}", on_click=answer_callback, args=(val, q_data['dim']))

else:
    # 💥 全息结算与 GPU 动画 (0卡顿 EMP 矩阵扫描特效，无缩进防截断)
    if not st.session_state.anim_played: 
        HTML_EMP = """
<style>
.cyber-emp-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100dvh; background: rgba(3,7,18,0.95); z-index: 999999; display: flex; justify-content: center; align-items: center; flex-direction: column; animation: cyber-fadeout 2.8s cubic-bezier(0.8, 0, 0.2, 1) forwards; pointer-events: none; backdrop-filter: blur(5px); }
.matrix-code { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: #10b981; font-family: 'Fira Code', monospace; font-size: 16px; text-align: center; line-height: 1.8; opacity: 0; animation: matrix-glitch 2s forwards; white-space: pre; text-shadow: 0 0 10px #10b981; margin-bottom: 30px;}
.cyber-text { font-family: 'Orbitron', sans-serif; font-size: clamp(24px, 5vw, 56px); font-weight: 900; color: #fff; letter-spacing: 10px; text-shadow: 0 0 30px #00f3ff, 0 0 60px #00f3ff; opacity: 0; animation: pop-in 2.5s cubic-bezier(0.1, 0.8, 0.3, 1) forwards; position: relative; z-index: 2; margin-top: 60px;}
@keyframes matrix-glitch { 0% { opacity: 0; } 10% { opacity: 1; } 80% { opacity: 1; } 100% { opacity: 0; filter: blur(5px);} }
@keyframes pop-in { 0% { transform: scale(0.8); opacity: 0; } 20% { transform: scale(1.05); opacity: 1; } 80% { transform: scale(1); opacity: 1; } 100% { transform: scale(1.3); opacity: 0; filter: blur(10px);} }
@keyframes cyber-fadeout { 0%, 80% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }
</style>
<div class="cyber-emp-overlay">
<div class="matrix-code">01001100 01001111 01000011 01001011<br>HASHING NEURAL NETWORK...<br>EXTRACTING FEATURES...<br>MINTING TO SDE CHAIN...</div>
<div class="cyber-text">ACCESS GRANTED</div>
</div>
"""
        st.markdown(HTML_EMP, unsafe_allow_html=True)
        st.session_state.anim_played = True
        
    res = st.session_state.total_scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    
    data = mbti_details.get(mbti) or mbti_details["INTJ"] 
    safe_alias_final, role_name, tier_level, tier_color = st.session_state.user_alias.upper(), data['role'], data['tier'], data['tier_color']
    
    # 🚨 40题极值精准归一化
    def get_intensity(score): return int(max(0, min(100, 50 + (score * 2.5))))
    val_E, val_I = get_intensity(res["E"]), 100 - get_intensity(res["E"])
    val_S, val_N = get_intensity(res["S"]), 100 - get_intensity(res["S"])
    val_T, val_F = get_intensity(res["T"]), 100 - get_intensity(res["T"])
    val_J, val_P = get_intensity(res["J"]), 100 - get_intensity(res["J"])

    categories = ['生态协同(E)', '颗粒实勘(S)', '量化风控(T)', '架构秩序(J)', '底层深潜(I)', '战略前瞻(N)', '生态共情(F)', '敏捷演进(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]

    p_score, s_score = -res.get("J", 0), res.get("S", 0)
    risk_score = int(max(5, min(95, 50 + (p_score * 1.5) - (s_score * 1.5))))
    if risk_score < 35: r_tag, r_color = "绝对合规与防线兜底", "#10b981"
    elif risk_score < 65: r_tag, r_color = "动态演进与灰度平衡", "#ffd700"
    else: r_tag, r_color = "无界扩张与极限破局", "#f43f5e"

    time_taken = max(1.0, st.session_state.end_time - st.session_state.start_time)
    
    # 🔐 资产防篡改物理锁：彻底闭环 JSON 导出 NameError Bug
    if "asset_minted" not in st.session_state:
        h_code = hashlib.sha256(f"{safe_alias_final}{mbti}{time_taken}V1.0".encode()).hexdigest().upper()
        h_int = int(h_code[:8], 16)
        st.session_state.asset_minted = {
            "hash_code": h_code,
            "block_height": f"V1.0-{(int(time.time()) % 1000000):06d}",
            "time_str": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "token_id": int(hashlib.md5(f"{safe_alias_final}{time_taken}".encode()).hexdigest()[:8], 16),
            "contract_addr": "0x" + hashlib.sha256(f"contract_{mbti}_{h_int}".encode()).hexdigest()[:38],
            "syn_tech": min(98, max(20, (85 if 'T' in mbti else 60) + (10 if 'N' in mbti else 0) + (h_int % 15) - 7)),
            "syn_biz": min(98, max(20, (85 if 'E' in mbti else 60) + (10 if 'P' in mbti else 0) + ((h_int >> 4) % 15) - 7)),
            "syn_comp": min(98, max(20, (85 if 'J' in mbti else 60) + (10 if 'S' in mbti else 0) + ((h_int >> 8) % 15) - 7))
        }
        st.session_state.asset_minted["d_arr"], st.session_state.asset_minted["roi_arr"] = generate_alpha_curve(data.get('base_roi', 1.35), data.get('volatility', 0.35), int(h_code[:6], 16))

    asset = st.session_state.asset_minted
    hash_code, block_height, current_time_str = asset["hash_code"], asset["block_height"], asset["time_str"]
    token_id, contract_addr = asset["token_id"], asset["contract_addr"]
    d_arr, roi_arr = asset["d_arr"], asset["roi_arr"]
    
    # 全量闭环兜底，绝对不再报 NameError
    syn_tech = asset.get("syn_tech", 85)
    syn_biz = asset.get("syn_biz", 80)
    syn_comp = asset.get("syn_comp", 90)

    avg_q_time = time_taken / len(questions)
    decisiveness = int(min(99, max(35, 100 - (max(0, avg_q_time - 2.5) * 5))))
    extremity_score = sum(abs(v) for v in res.values()) / 80.0
    random_factor = 0.9 + (int(hash_code[:8], 16) % 200) / 1000.0
    asset_valuation = int(data.get('base_hash', 8000) * (1 + extremity_score * 0.4) * (0.8 + (decisiveness/100.0) * 0.5) * random_factor * 10000)
    valuation_str = f"{round(asset_valuation, -4):,}"
    pct_beat = round(min(99.9, max(50.0, 60 + (decisiveness * 0.3) + (extremity_score * 20))), 1)

    # =========================================================================
    # 📱【核心重排】瀑布流式 UX 布局 (专门优化微信下拉浏览习惯)
    # =========================================================================
    
    HTML_BANNER = f"""
<div style="background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(10,10,30,0.9)); border: 1px solid #10b981; border-radius: 8px; padding: 15px 25px; margin-bottom: 25px; font-family: 'Orbitron', monospace; box-shadow: 0 0 20px rgba(16,185,129,0.2);">
<div style="color: #10b981; font-size: 14px; font-weight: bold; border-bottom: 1px dashed #10b981; padding-bottom: 10px; margin-bottom: 12px; display:flex; align-items:center;">
<span style="font-size:20px; margin-right:10px;">🏅</span> <span>SDE SOULBOUND TOKEN (SBT) MINTED [ V 1.0 ]</span>
</div>
<div style="font-size: 12px; color: #94a3b8; line-height: 1.8; display:flex; flex-wrap: wrap; justify-content: space-between; gap: 10px;">
<div><div><span style="color:#e2e8f0;">BLOCK HEIGHT:</span> {block_height}</div><div><span style="color:#e2e8f0;">CONTRACT:</span> {contract_addr[:20]}...</div></div>
<div style="text-align: left;"><div><span style="color:#e2e8f0;">TOKEN ID:</span> #{token_id}</div><div><span style="color:#e2e8f0;">TIMESTAMP:</span> {current_time_str}</div></div>
</div>
</div>
"""
    st.markdown(HTML_BANNER, unsafe_allow_html=True)

    # 1. 核心首屏区：左侧身份大卡，右侧互动沙盘 (手机端会自适应瀑布流)
    col_top_l, col_top_r = st.columns([1.1, 1.3], gap="large")

    with col_top_l:
        tags_html_web = " ".join([f"<span style='background:rgba(0, 243, 255, 0.1); color:#00f3ff !important; border:1px solid rgba(0,243,255,0.4); padding:6px 14px; border-radius:6px; font-size:13px; font-weight:900; margin:4px; display:inline-block;'>{t}</span>" for t in data.get('tags', [])])
        # 🚨 满血找回：Web 端高阶专属技能树！
        skills_html_web = " ".join([f"<span style='background:linear-gradient(90deg, rgba(168,85,247,0.3), rgba(168,85,247,0.1)); border:1px solid rgba(168,85,247,0.6); border-left:3px solid #a855f7; padding:4px 10px; border-radius:4px; font-size:12px; color:#e9d5ff; font-weight:bold; display:inline-block; margin:4px; box-shadow: 0 0 10px rgba(168,85,247,0.2);'>{s}</span>" for s in data.get('skills', [])])
        
        HTML_CARD = f"""
<div class="result-card">
<div class="tier-badge" style="background:{tier_color}; box-shadow:0 0 25px {tier_color}99;">{tier_level}</div>
<div class="orbitron-font" style="font-size:12px; color:#94a3b8; letter-spacing:6px; margin-bottom:15px;">SDE NEURAL DECODING V1.0</div>
<div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:18px; margin-bottom:5px; border-bottom:1px dashed #334155; padding-bottom:10px; display:inline-block; font-weight:bold;">{safe_alias_final}</div>
<div class="mbti-code">{mbti}</div>
<div style="text-align:center;font-size:13px;color:#94a3b8;margin-bottom:15px;">GLOBAL RARITY: <span style="color:{tier_color};font-family:Orbitron;font-weight:bold;font-size:15px;">{data.get('rarity', 'Top 5%')}</span></div>
<div style="font-size: 24px; font-weight: 900; color: #00f3ff !important; margin: 10px 0 20px 0; letter-spacing: 2px;">【 {role_name} 】</div>
<div style="display:flex; flex-wrap: wrap; justify-content:space-between; gap:15px; margin-bottom: 25px;">
<div style="flex:1; background:rgba(0,0,0,0.8); border:1px solid rgba(255,215,0,0.4); border-radius:8px; padding:20px; min-width:120px;">
<div style="font-size:11px; color:#94a3b8; font-family:'Orbitron'; margin-bottom:8px;">HASHRATE (SDE)</div>
<div style="font-size:26px; color:#ffd700; font-weight:900; font-family:'Orbitron'; text-shadow:0 0 15px rgba(255,215,0,0.8);">💎 {valuation_str}</div>
</div>
<div style="flex:1; background:rgba(0,0,0,0.8); border:1px solid rgba(0,243,255,0.4); border-radius:8px; padding:20px; min-width:120px;">
<div style="font-size:11px; color:#94a3b8; font-family:'Orbitron'; margin-bottom:8px;">PERCENTILE</div>
<div style="font-size:26px; color:#00f3ff; font-weight:900; font-family:'Orbitron'; text-shadow:0 0 15px rgba(0,243,255,0.8);">⚡ TOP {100 - pct_beat:.1f}%</div>
</div>
</div>
<div style="text-align:center; margin-bottom:15px;">
<div style="font-size:12px; color:#a855f7; margin-bottom:10px; font-family:Orbitron; letter-spacing:2px; font-weight:bold;">[ SKILL TREE ]</div>
{skills_html_web}
</div>
<div style="margin-bottom:25px;">{tags_html_web}</div>
<div style="color:#e2e8f0 !important; font-size:14px; line-height:1.8; margin-bottom:10px; font-weight:400; text-align:justify; background:rgba(255,255,255,0.03); padding: 15px; border-radius: 8px;">{data.get('desc', '')}</div>
</div>
"""
        st.markdown(HTML_CARD, unsafe_allow_html=True)

    with col_top_r:
        # 👑 UX：将社交高频交互直接前置
        options_list = list(mbti_details.keys())
        format_func = lambda x: f"{x} - {mbti_details[x]['role']}"
        
        st.markdown("<h4 style='color:#3b82f6 !important; border-left:4px solid #3b82f6; padding-left:10px; font-weight:900;'>🤝 跨域算力协同沙盘 (双轨重叠)</h4>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:15px;'>输入团队成员或领导的核心架构代码，系统将进行双轨雷达重叠与匹配度测算：</div>", unsafe_allow_html=True)
        pmbti = st.selectbox("🎯 挂载目标协作节点 (选择对方代码):", options=options_list, index=options_list.index("ESTJ"), format_func=format_func, label_visibility="collapsed")
        sc, sd = calculate_synergy(mbti, pmbti)
        
        # 🛰️ 极客双轨重叠雷达引擎
        t_E = 85 if 'E' in pmbti else 15
        t_S = 85 if 'S' in pmbti else 15
        t_T = 85 if 'T' in pmbti else 15
        t_J = 85 if 'J' in pmbti else 15
        target_values = [t_E, t_S, t_T, t_J, 100-t_E, 100-t_S, 100-t_T, 100-t_J]

        fig_syn = go.Figure()
        fig_syn.add_trace(go.Scatterpolar(r=target_values + [target_values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(168, 85, 247, 0.1)', line=dict(color='rgba(168, 85, 247, 0.6)', width=2, dash='dash'), name=f'目标 ({pmbti})'))
        fig_syn.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=3), name='我方节点'))
        fig_syn.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC, sans-serif", color='#e2e8f0', size=10))), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#fff")), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=25, r=25, t=20, b=20), height=280)
        
        st.plotly_chart(fig_syn, use_container_width=True, config={'displayModeBar': False}, theme=None)

        HTML_SYN = f"""
<div style="background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.5); padding: 25px; border-radius: 12px; margin-top:0px; text-align:center; box-shadow: 0 0 30px rgba(59,130,246,0.15);">
<div style="font-family:'Orbitron'; color:#3b82f6; font-size:12px; font-weight:bold; margin-bottom:10px; letter-spacing: 3px;">[ SYNERGY MATCH RATE ]</div>
<div style="font-family:'Orbitron'; font-size:55px; font-weight:900; color:#fff; text-shadow:0 0 35px rgba(59,130,246,0.8); margin-bottom:15px;">{sc}%</div>
<div style="color:#e2e8f0; font-size:14px; font-weight:bold; line-height:1.7;">{sd}</div>
</div>
"""
        st.markdown(HTML_SYN, unsafe_allow_html=True)
        
        st.markdown("<h5 style='color:#10b981; margin-top:20px; margin-bottom:10px;'>💡 黄金搭档建议：</h5>", unsafe_allow_html=True)
        HTML_PARTNER = f"""
<div style='background: rgba(16,185,129,0.1); border-left:4px solid #10b981; padding:20px; border-radius:4px; font-size:14px; color:#e2e8f0; line-height: 1.6;'>
您目前的最佳生态拍档为：<b style='color:#10b981; font-size:16px;'>{data.get('partner', '')}</b><br><br>{data.get('partner_advice', '')}
</div>
"""
        st.markdown(HTML_PARTNER, unsafe_allow_html=True)

    # 2. 数据深潜区：双向能量图与风控仪
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    
    col_mid_l, col_mid_r = st.columns([1.1, 1.3], gap="large")
    
    with col_mid_l:
        st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🕸️ 核心对抗能量矩阵</h4>", unsafe_allow_html=True)
        
        # 🚨 全新重构双向对抗能量条
        HTML_BARS = f"""
<div style="background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:25px 20px; margin-top:10px; margin-bottom: 20px;">
<div style="font-size:clamp(10px, 2.5vw, 12px); color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;"><span>生态联结 (E) {val_E}%</span><span style="color:#94a3b8;">深潜独立 (I) {val_I}%</span></div>
<div style="background:rgba(255,255,255,0.05); border-radius:4px; height:8px; margin:6px 0 15px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"><div style="position:absolute; top:0; left:0; height:100%; border-radius:4px; width:{val_E}%; background:#00f3ff; box-shadow:0 0 10px #00f3ff;"></div></div>

<div style="font-size:clamp(10px, 2.5vw, 12px); color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; margin-top:15px; font-weight:bold;"><span>实务颗粒 (S) {val_S}%</span><span style="color:#94a3b8;">宏观前瞻 (N) {val_N}%</span></div>
<div style="background:rgba(255,255,255,0.05); border-radius:4px; height:8px; margin:6px 0 15px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"><div style="position:absolute; top:0; left:0; height:100%; border-radius:4px; width:{val_S}%; background:#a855f7; box-shadow:0 0 10px #a855f7;"></div></div>

<div style="font-size:clamp(10px, 2.5vw, 12px); color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; margin-top:15px; font-weight:bold;"><span>量化风控 (T) {val_T}%</span><span style="color:#94a3b8;">生态共情 (F) {val_F}%</span></div>
<div style="background:rgba(255,255,255,0.05); border-radius:4px; height:8px; margin:6px 0 15px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"><div style="position:absolute; top:0; left:0; height:100%; border-radius:4px; width:{val_T}%; background:#3b82f6; box-shadow:0 0 10px #3b82f6;"></div></div>

<div style="font-size:clamp(10px, 2.5vw, 12px); color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; margin-top:15px; font-weight:bold;"><span>秩序架构 (J) {val_J}%</span><span style="color:#94a3b8;">敏捷演进 (P) {val_P}%</span></div>
<div style="background:rgba(255,255,255,0.05); border-radius:4px; height:8px; margin:6px 0 0 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"><div style="position:absolute; top:0; left:0; height:100%; border-radius:4px; width:{val_J}%; background:#10b981; box-shadow:0 0 10px #10b981;"></div></div>
</div>
"""
        st.markdown(HTML_BARS, unsafe_allow_html=True)

    with col_mid_r:
        st.markdown("<h4 style='color:#f43f5e !important; border-left:4px solid #f43f5e; padding-left:10px; font-weight:900;'>🎛️ 业务风控熔断仪</h4>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-size:16px; font-weight:bold; color:{r_color}; font-family:Noto Sans SC; margin-top: 5px;'>{r_tag}</div>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=risk_score, number={'suffix': "%", 'font': {'family': 'Orbitron, sans-serif', 'color': r_color, 'size': 40}}, gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155"}, 'bar': {'color': r_color}, 'bgcolor': "rgba(255,255,255,0.05)", 'steps': [{'range': [0, 35], 'color': "rgba(16, 185, 129, 0.15)"}, {'range': [35, 65], 'color': "rgba(255, 215, 0, 0.15)"}, {'range': [65, 100], 'color': "rgba(244, 63, 94, 0.15)"}]}))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#94a3b8"}, height=200, margin=dict(l=30, r=30, t=10, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False}, theme=None)

        # 3. 极客拓展面板 (用 Tabs 折叠，拯救竖屏长滚动)
        st.markdown("<h4 style='color:#a855f7 !important; border-left:4px solid #a855f7; padding-left:10px; font-weight:900; margin-top:20px; margin-bottom:15px;'>🗄️ 算力深潜控制台 (DEEP DIVE)</h4>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:right; font-size:12px; color:#94a3b8; margin-bottom:10px; opacity:0.8;'>👉 手机端可左右滑动切换面板</div>", unsafe_allow_html=True)
        
        t_evo, t_mkt, t_3d, t_sol = st.tabs(["🔮 终极演进路线", "📉 市场 Alpha 压测", "🌌 3D 认知星图", "💻 智能合约"])
        
        with t_evo:
            evo_path = data.get('evolution_path', ["L1 初级节点", "L2 核心中枢"])
            HTML_EVO = f"""
<div style="margin-top:15px; margin-bottom:15px; border-left:3px solid #00f3ff; padding-left:15px; background:linear-gradient(90deg, rgba(0,243,255,0.1), transparent); padding-top:10px; padding-bottom:10px; border-radius: 0 6px 6px 0;">
<div style="color:#00f3ff; font-family:Orbitron; font-size:11px; margin-bottom:2px; letter-spacing:1px;">PHASE 1 (CURRENT STATE)</div><div style="color:#fff; font-weight:bold; font-size:16px;">{evo_path[0]}</div>
</div>
<div style="margin-bottom:15px; border-left:3px solid #a855f7; padding-left:15px; background:linear-gradient(90deg, rgba(168,85,247,0.1), transparent); padding-top:10px; padding-bottom:10px; border-radius: 0 6px 6px 0; margin-left: 20px;">
<div style="color:#a855f7; font-family:Orbitron; font-size:11px; margin-bottom:2px; letter-spacing:1px;">PHASE 2 (AWAKENING)</div><div style="color:#fff; font-weight:bold; font-size:16px;">{evo_path[1]}</div>
</div>
<div style="border-left:3px solid #ffd700; padding-left:15px; background:linear-gradient(90deg, rgba(255,215,0,0.15), transparent); padding-top:10px; padding-bottom:10px; border-radius: 0 6px 6px 0; margin-left: 40px; box-shadow: 0 0 20px rgba(255,215,0,0.1); margin-bottom:25px;">
<div style="color:#ffd700; font-family:Orbitron; font-size:11px; margin-bottom:2px; letter-spacing:1px;">PHASE 3 (ULTIMATE DOMINANCE)</div><div style="color:#ffd700; font-weight:900; font-size:18px;">{data.get('ultimate_evolution', '')}</div>
</div>
"""
            st.markdown(HTML_EVO, unsafe_allow_html=True)
            with st.expander("⚠️ 绝密防线：SDE 史诗级黑天鹅宕机推演"):
                HTML_SWAN = f"""
<div style="padding: 5px 10px; font-size: 14px; color: #cbd5e1; line-height: 1.7;">
<div style="color: #f43f5e; font-weight: 900; margin-bottom: 5px; font-size:15px;">[ 致命崩溃盲点 ]</div>
<div style="margin-bottom: 15px;">{data.get('black_swan', '')}</div>
<div style="color: #10b981; font-weight: 900; margin-bottom: 5px; font-size:15px;">[ 官方热修复补丁 ]</div>
<div>{data.get('patch', '')}</div>
</div>
"""
                st.markdown(HTML_SWAN, unsafe_allow_html=True)

        with t_mkt:
            st.markdown("<div class='panel-title' style='color:#ffd700; border-color:#ffd700; margin-top:15px;'>/// 30-DAY MARKET ROI SIMULATION (ALPHA)</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:14px; color:#e2e8f0; margin-bottom:10px;'>基于随机游走推演的交易风格：<br><span style='color:#ffd700; font-weight:bold; font-size:15px;'>【 {data.get('market_style', '')} 】</span></div>", unsafe_allow_html=True)
            fig_roi = go.Figure()
            lc = "#10b981" if roi_arr[-1] >= 100 else "#f43f5e"
            fig_roi.add_trace(go.Scatter(x=d_arr, y=roi_arr, mode='lines', line=dict(color=lc, width=3), fill='tozeroy', fillcolor=f'rgba({16 if roi_arr[-1]>=100 else 244}, {185 if roi_arr[-1]>=100 else 63}, {129 if roi_arr[-1]>=100 else 94}, 0.15)'))
            fig_roi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='SDE Alpha Net Value'))
            st.plotly_chart(fig_roi, use_container_width=True, config={'displayModeBar': False}, theme=None)

        with t_3d:
            st.markdown("<div class='panel-title' style='color:#00f3ff; border-color:#00f3ff; margin-top:15px;'>/// 3D COGNITIVE TOPOLOGY MAP</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:10px;'>将多维指标降维映射至三维空间 (支持鼠标 360° 拖拽)。背景点阵为抽样全网节点。</div>", unsafe_allow_html=True)
            rng_3d = np.random.RandomState(int(hash_code[:6], 16))
            x_v = val_E if res['E'] >= 0 else -val_I
            y_v = val_N if res['S'] <= 0 else -val_S
            z_v = val_T if res['T'] >= 0 else -val_F
            f3d = go.Figure()
            f3d.add_trace(go.Scatter3d(x=rng_3d.randint(-100,100,size=100), y=rng_3d.randint(-100,100,size=100), z=rng_3d.randint(-100,100,size=100), mode='markers', marker=dict(size=4, color='#334155', opacity=0.6), name='全网抽样节点'))
            f3d.add_trace(go.Scatter3d(x=[x_v], y=[y_v], z=[z_v], mode='markers+text', text=[mbti], textposition="top center", marker=dict(size=16, color=tier_color, symbol='diamond', line=dict(color='#fff', width=2)), textfont=dict(color=tier_color, size=18, family="Orbitron", weight="bold"), name='当前授权节点'))
            f3d.update_layout(scene=dict(xaxis_title='执行↔深潜', yaxis_title='实务↔前瞻', zaxis_title='共情↔刚性', xaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b"), yaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b"), zaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b")), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=400, showlegend=False)
            st.plotly_chart(f3d, use_container_width=True, config={'displayModeBar': False}, theme=None)

        with t_sol:
            st.markdown("<div class='panel-title' style='color:#10b981; border-color:#10b981; margin-top:15px;'>/// SOLIDITY SMART CONTRACT MINT LOG</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:12px; color:#94a3b8; margin-bottom:10px;'>系统已自动为您生成专属的以太坊 ERC721 确权智能合约源码。</div>", unsafe_allow_html=True)
            
            # 🍎 Mac-Style 智能合约黑盒 (100% 免疫浅色模式污染)
            code_block = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@sde-network/contracts/token/ERC721.sol";

contract SDE_Talent_Registry_V1 is ERC721 {{
    struct Profile {{
        string matrix_id;
        uint256 valuation_sde;
        uint8 decisiveness;
        string tier;
    }}
    
    mapping(uint256 => Profile) public nodes;
    
    constructor() ERC721("SDE_NODE_V1", "SDEN") {{}}

    // =====================================
    // SYSTEM MINT LOG 
    // MINTED_TO: {safe_alias_final}
    // BLOCK_HEIGHT: {block_height}
    // CONTRACT_ADDR: {contract_addr}
    // =====================================
    
    function executeMint() public {{
        uint256 tokenId = {token_id};
        nodes[tokenId] = Profile("{mbti}", {asset_valuation}, {decisiveness}, "{tier_level}");
        _mint(msg.sender, tokenId);
    }}
}}"""
            safe_code = html.escape(code_block)
            HTML_SOLIDITY = f"""
<div style="background: #050505; border-radius: 8px; border: 1px solid #334155; border-left: 4px solid #10b981; width: 100%; box-sizing: border-box; box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(0,243,255,0.05); margin-top: 15px; margin-bottom: 20px; overflow: hidden;">
<div style="background: #0f172a; padding: 10px 15px; display: flex; align-items: center; border-bottom: 1px solid #334155;">
<div style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f56; margin-right: 8px;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e; margin-right: 8px;"></div>
<div style="width: 12px; height: 12px; border-radius: 50%; background: #27c93f; margin-right: 15px;"></div>
<div style="color: #94a3b8; font-size: 11px; font-family: 'Fira Code', monospace; letter-spacing: 1px;">SDE_Smart_Contract.sol</div>
</div>
<div style="padding: 15px; overflow-x: auto;">
<pre style="margin: 0; font-family: 'Fira Code', monospace; font-size: 12px; color: #10b981 !important; line-height: 1.6; background: transparent; border: none; user-select: all; cursor: text;"><code>{safe_code}</code></pre>
</div>
</div>
"""
            st.markdown(HTML_SOLIDITY, unsafe_allow_html=True)
            
            st.markdown("<div class='panel-title' style='color:#f43f5e; border-color:#f43f5e; margin-top:20px; border-bottom:none;'>/// TOP SECRET DIRECTIVES ///</div>", unsafe_allow_html=True)
            tasks_html = "".join([f"<div class='mission-item'><span style='color:#e2e8f0; font-size:14px; font-weight:bold;'>{t}</span></div>" for t in data.get('tasks', [])])
            st.markdown(f"<div style='margin-bottom: 10px;'>{tasks_html}</div>", unsafe_allow_html=True)

    # =========================================================================
    # 💠 4. 【沉底提取中心】防白屏海报与 JSON 协议下发
    # =========================================================================
    st.markdown("<h4 style='color:#00f3ff !important; border-left:5px solid #00f3ff; padding-left:12px; font-weight:900; margin-top:40px; margin-bottom:20px;'>💠 数据要素大屏提取终端</h4>", unsafe_allow_html=True)
    t_img, t_txt, t_json = st.tabs(["📸 防白屏全息海报 (长按发圈)", "📝 纯文本通讯协议 (液态排版)", "📥 极客 JSON 底包档案"])

    with t_img:
        st.markdown("<div style='font-size:13px; color:#10b981; margin-bottom:10px;'>系统已启用最高优先级【防显存溢出引擎】压制高清海报，请等待 2 秒...</div>", unsafe_allow_html=True)
        random.seed(hash_code)
        gradient_stops = []
        for p in range(0, 100, int(random.uniform(2, 6))): 
            gradient_stops.append(f"rgba(0,243,255,0.7) {p}%, rgba(0,243,255,0.7) {p+1}%, transparent {p+1}%, transparent {p+2}%")
        barcode_css = "linear-gradient(90deg, " + ", ".join(gradient_stops) + ")"
        
        tags_html_poster = "".join([f"<span style='background:rgba(0,243,255,0.1); border:1px solid rgba(0,243,255,0.5); padding:4px 8px; border-radius:4px; font-size:11px; color:#00f3ff; font-weight:bold; margin:3px; display:inline-block;'>{t}</span>" for t in data.get('tags', [])])
        skills_html_poster = "".join([f"<span style='background:linear-gradient(90deg, rgba(168,85,247,0.3), rgba(168,85,247,0.1)); border:1px solid rgba(168,85,247,0.6); border-left:3px solid #a855f7; padding:4px 8px; border-radius:4px; font-size:11px; color:#e9d5ff; font-weight:bold; display:inline-block; margin:3px;'>{s}</span>" for s in data.get('skills', [])])

        # 🚨 终极安全锁：将 capture-box 画板锁定 320px，完美兼容最老的 iPhone SE 且不裁切！不再监听会导致死锁的 document.fonts！
        HTML_POSTER = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
/* 拔掉 Google Fonts 引用，使用原生安全字体防止白屏死锁 */
body {{ margin: 0; display: flex; flex-direction: column; align-items: center; background-color: transparent !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif; user-select: none; padding: 10px 0; color: #ffffff; overflow-x: hidden; }}
#render-target {{ position: absolute; top: 0; left: 50%; transform: translateX(-50%); display: flex; justify-content: center; opacity: 0.01; z-index: -100; pointer-events: none; }}

/* 🚨 物理锁死海报画布为 320px，兼容一切小屏手机 */
#capture-box {{ width: 320px; background-color: #010308; padding: 30px 15px; border-radius: 16px; border: 1px solid rgba(0, 243, 255, 0.5); box-shadow: 0 0 40px rgba(0, 243, 255, 0.2); position: relative; overflow: hidden; color: #fff; box-sizing: border-box; margin: 0 auto; }}
.cyber-grid {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(0deg, rgba(0,243,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.05) 1px, transparent 1px); background-size: 25px 25px; z-index: 0; pointer-events:none;}}
.top-glow {{ position: absolute; top: 0; left: 0; width: 100%; height: 6px; background: linear-gradient(90deg, transparent, #00f3ff, transparent); z-index: 1; }}
.bdg {{ position: absolute; top: 22px; right: -35px; background: {tier_color}; color: #000; font-weight: 900; font-size: 10px; padding: 3px 35px; transform: rotate(45deg); z-index: 10; letter-spacing: 2px; box-shadow: 0 0 15px {tier_color}88; }}
.ct {{ position: relative; z-index: 2; }}
.hd {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom: 15px; margin-bottom: 20px; }}
.nm {{ text-align: center; font-size: 20px; font-weight: 900; letter-spacing: 2px; margin-bottom: 8px; color: #fff; text-transform: uppercase; }}
.mb {{ font-size: 58px; font-weight: 900; color: #ffd700; line-height: 1; text-align: center; text-shadow: 0 0 30px rgba(255,215,0,0.6); margin-bottom: 8px; letter-spacing: 4px; font-family: Impact, sans-serif; }}
.rl {{ text-align: center; font-size: 14px; font-weight: 900; color: #00f3ff; margin-bottom: 20px; letter-spacing: 2px; }}
.vb {{ display:flex; justify-content:space-between; text-align:center; background:rgba(0,0,0,0.8); border:1px solid rgba(255,215,0,0.4); padding:10px; border-radius:8px; margin-bottom: 20px; gap: 5px; }}
.rb {{ border-left: 4px solid {r_color}; background: {r_color}1A; padding: 12px; border-radius: 0 8px 8px 0; margin-bottom: 20px; }}
.ft {{ text-align: center; color: #64748b; font-size: 9px; padding-top: 12px; border-top: 1px dashed rgba(255,255,255,0.1); line-height: 1.6; font-family: monospace; }}
.bc {{ width: 90%; height: 20px; margin: 0 auto 8px auto; background: {barcode_css}; }}

#ui {{ color: #00f3ff; font-size: 13px; text-align: center; padding: 50px; animation: p 1s infinite alternate; letter-spacing: 2px; font-weight:bold;}}
@keyframes p {{ 0% {{ opacity: 1; text-shadow: 0 0 10px #00f3ff; }} 100% {{ opacity: 0.4; }} }}
#img {{ display: none; width: 100%; max-width: 320px; height: auto; border-radius: 16px; border: 1px solid rgba(0,243,255,0.6); box-shadow: 0 20px 40px rgba(0,0,0,0.9); pointer-events: auto; margin: 10px auto; box-sizing: border-box;}}
.ht {{ display: none; background: rgba(16,185,129,0.15); border: 1px solid #10b981; padding: 15px; border-radius: 8px; font-size: 14px; color: #fff; text-align: center; margin: 20px auto 0 auto; width: 100%; max-width: 320px; box-sizing: border-box; text-shadow: 0 0 5px rgba(0,0,0,0.8); line-height: 1.6;}}
.stat-row {{ display: flex; align-items: center; margin-bottom: 8px; font-size: 10px; font-weight: bold; justify-content: space-between; }}
.stat-row:last-child {{ margin-bottom: 0; }}
.sbc {{ background: rgba(255,255,255,0.05); border-radius: 3px; height: 5px; width: 130px; position: relative; overflow: hidden; margin: 0 6px; }}
.sbf {{ position: absolute; left: 0; top: 0; height: 100%; }}
</style>
</head>
<body>
<div id="render-target">
<div id="capture-box">
<div class="cyber-grid"></div><div class="top-glow"></div>
<div class="bdg">{tier_level}</div>
<div class="ct">
<div class="hd">
<div><div style="color:#00f3ff;font-size:14px;font-weight:900;">SDE MATRIX</div><div style="font-size:15px;font-weight:900;letter-spacing:4px;">上海数据交易所</div></div>
<div style="text-align:right;"><div style="color:#94a3b8;font-size:9px;">V1.0 HASH</div><div style="color:#00f3ff;font-size:11px;font-weight:bold;font-family:monospace;">0x{hash_code[:8]}</div></div>
</div>
<div style="font-size:10px;color:#94a3b8;text-align:center;margin-bottom:5px;">AUTHORIZED NODE</div>
<div class="nm">{safe_alias_final}</div><div class="mb">{mbti}</div>
<div style="text-align:center;font-size:11px;color:#94a3b8;margin-bottom:15px;">GLOBAL RARITY: <span style="color:{tier_color};font-weight:bold;font-size:13px;">{data.get('rarity', 'Top 5%')}</span></div>
<div class="rl">【 {role_name} 】</div>
<div class="vb">
<div style="flex:1;"><div style="font-size:9px;color:#94a3b8;margin-bottom:5px;">HASHRATE (SDE)</div><div style="font-size:17px;color:#ffd700;font-weight:900;">💎 {round(asset_valuation, -4):,}</div></div>
<div style="border-left:1px dashed rgba(255,255,255,0.3);"></div>
<div style="flex:1;"><div style="font-size:9px;color:#94a3b8;margin-bottom:5px;">PERCENTILE</div><div style="font-size:17px;color:#00f3ff;font-weight:900;">⚡ TOP {100-pct_beat:.1f}%</div></div>
</div>
<div style="text-align:center; margin-bottom:12px;"><div style="font-size:10px; color:#a855f7; margin-bottom:6px; font-weight:bold;">[ SKILL TREE ]</div>{skills_html_poster}</div>
<div style="text-align:center; margin-bottom:20px;">{tags_html_poster}</div>

<div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 10px; margin-bottom: 20px;">
<div style="font-family: monospace; font-size: 9px; color: #00f3ff; text-align: center; margin-bottom: 10px;">/// HASH METRICS ///</div>
<div class="stat-row"><span style="color:#e2e8f0; width:50px;">生态 {val_E}%</span><div class="sbc"><div class="sbf" style="width:{val_E}%; background:#00f3ff;"></div></div><span style="color:#94a3b8; width:50px; text-align:right;">深潜 {val_I}%</span></div>
<div class="stat-row"><span style="color:#e2e8f0; width:50px;">实勘 {val_S}%</span><div class="sbc"><div class="sbf" style="width:{val_S}%; background:#a855f7;"></div></div><span style="color:#94a3b8; width:50px; text-align:right;">前瞻 {val_N}%</span></div>
<div class="stat-row"><span style="color:#e2e8f0; width:50px;">量化 {val_T}%</span><div class="sbc"><div class="sbf" style="width:{val_T}%; background:#3b82f6;"></div></div><span style="color:#94a3b8; width:50px; text-align:right;">共情 {val_F}%</span></div>
<div class="stat-row"><span style="color:#e2e8f0; width:50px;">秩序 {val_J}%</span><div class="sbc"><div class="sbf" style="width:{val_J}%; background:#10b981;"></div></div><span style="color:#94a3b8; width:50px; text-align:right;">敏捷 {val_P}%</span></div>
</div>

<div style="background: rgba(255,0,60,0.1); border-left: 4px solid #ff003c; padding: 10px; margin-bottom: 15px; border-radius: 0 6px 6px 0;">
<div style="font-size:8px; color:#ff003c; margin-bottom:4px; letter-spacing:1px;">/// 2026 EVOLUTION ///</div>
<div style="font-size:12px; font-weight:bold; color:#fff; text-shadow:0 0 10px rgba(255,0,60,0.6);">{data.get('ultimate_evolution', '')}</div>
</div>

<div class="rb"><div style="font-size:9px;color:#e2e8f0;margin-bottom:4px;font-weight:bold;">SYS_WARNING: 职场风控边界</div><div style="color:{r_color};font-size:13px;font-weight:900;">{r_tag}</div></div>
<div class="ft"><div class="bc"></div><div style="margin-bottom:4px;font-weight:bold;">SDE DATA ELEMENT KERNEL V1.0</div><div style="color:#475569;">© {COPYRIGHT} | TOKEN: #{token_id}</div></div>
</div>
</div>
</div>

<div id="ui">[ MINTING V1.0 HIGH-RES POSTER... ]</div>
<img id="result-img" alt="SDE Matrix V1.0" title="长按保存或分享" />
<div id="hint" class="ht"><span style="font-size:18px;">✅</span> <b>全息海报强力渲染完成！</b><br><span style="color:#10b981;">👆 手机端请 <b>长按上方图片</b> 保存发圈</span></div>

<script>
// 极速强绘：定时器轮询探测渲染引擎，保证 100% 成功率！
let checkCount = 0;
function renderPoster() {{
    const target = document.getElementById('capture-box');
    if (!target) return;
    
    html2canvas(target, {{
        scale: window.devicePixelRatio || 2, 
        backgroundColor: '#010308', 
        useCORS: true, 
        allowTaint: true,
        logging: false,
        onclone: function(clonedDoc) {{
            var rt = clonedDoc.getElementById('render-target');
            if (rt) {{
                rt.style.opacity = '1';
                rt.style.position = 'relative';
                rt.style.left = '0';
                rt.style.top = '0';
                rt.style.transform = 'none';
                rt.style.zIndex = '1';
            }}
        }}
    }}).then(canvas => {{ 
        document.getElementById('result-img').src = canvas.toDataURL('image/png'); 
        document.getElementById('ui').style.display = 'none'; 
        document.getElementById('result-img').style.display = 'block'; 
        document.getElementById('hint').style.display = 'block'; 
        document.getElementById('render-target').style.display = 'none'; 
    }}).catch(err => {{ 
        document.getElementById('ui').innerHTML='⚠️ 手机内存受限，请直接截屏保存上方网页。'; 
    }});
}}

function checkAndRender() {{
    if (typeof html2canvas !== 'undefined') {{
        setTimeout(renderPoster, 800); 
    }} else {{
        checkCount++;
        if(checkCount < 20) {{
            setTimeout(checkAndRender, 500);
        }} else {{
            document.getElementById('ui').innerHTML='❌ 渲染引擎加载超时，请检查网络。';
        }}
    }}
}}
checkAndRender();
</script>
</body>
</html>
"""
        st.markdown(HTML_POSTER, unsafe_allow_html=True)

    with t_txt:
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:10px; margin-top:10px;'>👇 长按下方文本框，可一键全选并复制纯文字名片：</div>", unsafe_allow_html=True)
        share_card = f"""【上海数据交易所 · 算力链上凭证 V1.0】
=================================
👤 确权节点：{safe_alias_final}
💎 算力估值：{round(asset_valuation, -4):,} SDE
🧬 核心架构：{mbti} ({role_name})
👑 全网评级：{tier_level} (稀缺度 {data.get('rarity', 'Top 5%')})
⚡️ 算力击败：全球 TOP {100 - pct_beat:.1f}%
🚀 终极演进：{data.get('ultimate_evolution', '')}
🎯 核心指令：{data.get('tasks', ['无'])[0]}
⚖️ 风控偏好：{r_tag}
=================================
🌐 2026 数据要素突破之年，寻找你的协同节点！
🔗 [Token ID: #{token_id} | Hash: 0x{hash_code[:8]}]"""
        
        # 🚨 终极自适应：在手机端不再是被截断的长条，而是液态换行，一键可全选！
        safe_share = html.escape(share_card)
        HTML_TXT = f"""
<div style="background-color: #050505 !important; border: 1px solid #334155 !important; border-left: 4px solid #00f3ff !important; border-radius: 8px; padding: 20px; overflow-x: hidden; margin-bottom: 20px; margin-top: 10px; box-shadow: inset 0 0 20px rgba(0,0,0,0.8); user-select: all; -webkit-user-select: all;">
<pre style="margin: 0; font-family: 'Noto Sans SC', sans-serif; font-size: 13px; color: #e2e8f0 !important; line-height: 1.6; background: transparent; border: none; white-space: pre-wrap; word-break: break-all; word-wrap: break-word;"><code>{safe_share}</code></pre>
</div>
"""
        st.markdown(HTML_TXT, unsafe_allow_html=True)

    with t_json:
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:15px; margin-top:10px;'>💾 高管/极客视角：导出您的原生底层 JSON 结构树归档：</div>", unsafe_allow_html=True)
        
        # 🚨 终极免疫 JSON 导出 NameError！全量闭环变量读取
        export_data = {
            "version": VERSION,
            "node_alias": safe_alias_final, 
            "matrix_id": mbti, 
            "role": role_name, 
            "tier": tier_level, 
            "global_rarity": data.get('rarity', ''),
            "soulbound_token": {
                "contract": contract_addr,
                "token_id": token_id,
                "hash_signature": hash_code,
                "block_height": block_height
            },
            "asset_valuation_sde": asset_valuation, 
            "global_percentile": pct_beat,
            "decisiveness_index": decisiveness,
            "metrics": {"E_I": val_E, "S_N": val_S, "T_F": val_T, "J_P": val_J},
            "synergy_index": {"Technology": syn_tech, "Business": syn_biz, "Compliance": syn_comp},
            "unlocked_skills": data.get('skills', []),
            "assigned_tasks": data.get('tasks', []), 
            "fatal_vulnerability": data.get('black_swan', ''), 
            "patch_protocol": data.get('patch', ''),
            "ultimate_evolution": data.get('ultimate_evolution', ''),
            "timestamp": current_time_str
        }
        json_str = json.dumps(export_data, indent=4, ensure_ascii=False)
        st.download_button(label="📥 立即下载节点加密档案 (.JSON)", data=json_str, file_name=f"SDE_NODE_{safe_alias_final}.json", mime="application/json", use_container_width=True)

    def reset_system():
        st.session_state.clear()

    with center_container():
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⏏ 强行切断连接并重启终端 (SYS_REBOOT)", type="primary", use_container_width=True):
            reset_system()
            st.rerun()

# =========================================================================
# 🛑 [ CORE 07 ] 赛博呼吸专属版权区
# =========================================================================
HTML_FOOTER = f"""
<div style="text-align:center; margin-top:80px; margin-bottom:40px; position:relative; z-index:10;">
<div style="color:#00f3ff !important; font-family:'Orbitron', monospace; font-size:10px; opacity:0.3; letter-spacing:6px; margin-bottom:8px;">POWERED BY SDE DATA ELEMENT KERNEL</div>
<div style="color:#00f3ff !important; font-family:'Orbitron', monospace; font-size:10px; opacity:0.2; letter-spacing:3px; margin-bottom:30px;">SYSTEM VERSION: {VERSION}</div>
<div class="copyright-niliu">© 2026 版权归属 · <b style="font-family:'Orbitron', sans-serif; letter-spacing: 4px;">{COPYRIGHT}</b></div>
</div>
"""
st.markdown(HTML_FOOTER, unsafe_allow_html=True)

# ================================= EOF ==================================

