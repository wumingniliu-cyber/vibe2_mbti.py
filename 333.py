import streamlit as st
import streamlit.components.v1 as components
import random
import time
import hashlib
import html
import json
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
import copy

# ==============================================================================
# 🌌 [ SDE TCG 01 ] 宇宙级内核与卡游物理引擎
# ==============================================================================
VERSION = "11.0_GOD_MODE_METAVERSE"
COPYRIGHT = "无名逆流"
SYS_NAME = "SDE 职场元宇宙 | 创世卡牌 V11.0"

st.set_page_config(page_title=SYS_NAME, page_icon="🃏", layout="wide", initial_sidebar_state="collapsed")

# 🚨 绝对安全的初始化兜底 (从物理底层免疫 KeyError)
def init_state():
    defaults = {
        'started': False, 'current_q': 0, 'start_time': None, 'end_time': None,
        'calculating': False, 'user_alias': "SDE_PLAYER", 
        'total_scores': {"E": 0, "S": 0, "T": 0, "J": 0},
        'anim_played': False, 'boot_played': False,
        'tokens': 0, 'boss_hp': 10000000, 'combat_logs': [], 'pvp_logs': [],
        'inventory': [], 'equipped_relics': [], 'stamina': 120, 'level': 1, 'exp': 0,
        'gacha_msg': "消耗 1,000 SDE 抽取高维遗物，大幅提升战力！", 'final_cp_cache': 10000
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

# ==============================================================================
# 🎨 [ SDE TCG 02 ] 史诗级卡游 UI 渲染底座 (纯静态字符串，防 NameError 与格式污染)
# ==============================================================================
CSS_BLOCK = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Orbitron:wght@400;500;700;900&family=Fira+Code:wght@400;600&display=swap');
:root { color-scheme: dark; }
[data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
.block-container { padding-top: 2rem !important; padding-bottom: 4rem !important; max-width: 1400px !important; margin: 0 auto; overflow-x: hidden; }
html, body, .stApp { background-color: #030712 !important; font-family: 'Noto Sans SC', sans-serif !important; color: #f8fafc !important; overflow-x: hidden; }
[data-testid="stAppViewContainer"]::before { content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, rgba(0, 243, 255, 0.03) 0%, rgba(3, 7, 18, 1) 70%); pointer-events: none; z-index: 0; }
[data-testid="stAppViewContainer"]::after { content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02)); background-size: 100% 3px, 3px 100%; z-index: 99999; pointer-events: none; opacity: 0.3; }
.stMarkdown, p, span, h2, h3, h4, li, label { color: #f8fafc !important; }
[data-testid="stProgress"] > div > div > div { background: linear-gradient(90deg, #00f3ff, #a855f7) !important; box-shadow: 0 0 15px rgba(168,85,247,0.8); }
.hero-title { font-size: clamp(26px, 5vw, 46px) !important; font-weight: 900 !important; text-align: center; color: #ffffff !important; letter-spacing: 4px; margin-bottom: 5px; margin-top: 15px; text-shadow: 0 0 20px rgba(0,243,255,0.7), 0 0 40px rgba(0,243,255,0.3); text-transform: uppercase; font-family: 'Orbitron', sans-serif;}
div[data-testid="stForm"] { max-width: 600px; margin: 0 auto; border: none !important; background: transparent !important;}
div[data-testid="stTextInput"] > div > div > input { background-color: rgba(4, 9, 20, 0.9) !important; color: #00f3ff !important; font-family: 'Orbitron', monospace !important; border: 1px solid rgba(0,243,255,0.5) !important; border-radius: 8px !important; text-align: center; font-size: clamp(16px, 4vw, 18px) !important; font-weight: bold !important; letter-spacing: 2px; box-shadow: inset 0 0 20px rgba(0,243,255,0.1) !important; height: 56px !important;}
div.stButton > button { background: linear-gradient(135deg, #0f172a 0%, #040914 100%) !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; border-left: 4px solid rgba(0, 243, 255, 0.6) !important; border-radius: 8px !important; min-height: 60px !important; width: 100% !important; box-shadow: 0 4px 15px rgba(0,0,0,0.6) !important; transition: all 0.2s ease !important; position: relative; overflow: hidden; }
div.stButton > button p { color: #ffffff !important; font-weight: bold !important; white-space: normal !important;}
div.stButton > button:hover { border-color: #00f3ff !important; box-shadow: 0 0 25px rgba(0,243,255,0.4) !important; transform: translateX(5px) !important; }
div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #00f3ff, #a855f7) !important; border: none !important; text-align: center !important; }
div.stButton > button[data-testid="baseButton-primary"] p { color: #010308 !important; font-weight: 900 !important; letter-spacing: 2px !important; font-family: 'Orbitron', sans-serif !important;}
[data-testid="stTabs"] button { color: #64748b !important; font-family: 'Noto Sans SC', sans-serif !important; font-weight: 900 !important; font-size: clamp(13px, 3vw, 16px) !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #ffd700 !important; border-bottom-color: #ffd700 !important; border-bottom-width: 4px !important; text-shadow: 0 0 20px rgba(255,215,0,0.6); }
[data-testid="stExpander"] { background: rgba(5, 10, 20, 0.9) !important; border: 1px solid rgba(244, 63, 94, 0.5) !important; border-radius: 8px !important; }
.tcg-card-container { perspective: 1500px; width: 100%; margin-bottom: 30px; display: flex; justify-content: center; z-index: 50; position: relative; }
.tcg-card { width: 100%; max-width: 480px; position: relative; transform-style: preserve-3d; transition: transform 0.5s; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.9); background: #0b1120; overflow: hidden; }
.tcg-card:hover { transform: rotateY(8deg) rotateX(-5deg) translateY(-10px) scale(1.02); }
.tcg-card::after { content: ""; position: absolute; inset: 0; background: linear-gradient(125deg, transparent 20%, rgba(255,255,255,0.4) 40%, rgba(255,215,0,0.5) 50%, rgba(0,243,255,0.4) 60%, transparent 80%); background-size: 250% 250%; background-position: 100% 100%; mix-blend-mode: color-dodge; pointer-events: none; transition: background-position 0.8s ease; z-index: 20; opacity: 0; }
.tcg-card:hover::after { background-position: 0% 0%; opacity: 1; }
.tcg-mbti { font-family: 'Orbitron', sans-serif !important; font-size: clamp(65px, 12vw, 90px); font-weight: 900; color: #ffffff !important; line-height: 1; letter-spacing: 8px; margin: 10px 0; position: relative; z-index: 5; }
.hud-box { background: rgba(5,10,20,0.8); border: 1px solid #334155; border-radius: 8px; padding: 15px; margin-bottom: 15px; font-family: 'Orbitron', monospace; font-size: 12px; }
.hud-title { color: #94a3b8; font-size: 10px; margin-bottom: 5px; font-weight: bold; }
.hud-val { color: #00f3ff; font-size: 18px; font-weight: bold; }
.order-row { display: flex; justify-content: space-between; margin-bottom: 10px; color: #10b981; border-bottom: 1px dashed rgba(16,185,129,0.2); padding-bottom: 6px; font-family: 'Fira Code', monospace; font-size: 13px; animation: flash-row 2s infinite alternate; }
@keyframes flash-row { 0% { opacity: 0.6; } 100% { opacity: 1; text-shadow: 0 0 10px rgba(16,185,129,0.9); } }
</style>
"""
st.markdown(CSS_BLOCK.replace('\n', ''), unsafe_allow_html=True)

# 🧬 Web3 级 SVG 矩阵指纹 (纯 HTML 构建，防格式化污染)
def get_identicon_html(hash_str, color):
    cells = "".join([f'<div style="background: {color if int(hash_str[(i // 5 * 3 + (i % 5 if i % 5 < 3 else 4 - i % 5)) % len(hash_str)], 16) % 2 == 0 else "transparent"}; box-shadow: 0 0 8px {color}; border-radius: 2px;"></div>' for i in range(25)])
    return f'<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 2px; width: 55px; height: 55px; background: rgba(0,0,0,0.8); padding: 5px; border-radius: 8px; border: 2px solid {color}; box-shadow: 0 0 20px {color}88;">{cells}</div>'

# ==============================================================================
# 🧠 [ SDE TCG 03 ] 题库全量无损归位 (40 题完整保留)
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

# 🚨 18 维卡游级属性字典 (完全硬编码，杜绝遗漏)
mbti_details = {
    "INTJ": {"role": "首席数据架构师", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 1.2%", "base_hash": 9850, "desc": "数据要素底座的“造物主”，致力于为错综复杂的数字经济构建严密的底层制度与逻辑规则。", "tags": ["顶层设计", "逻辑闭环", "制度自信"], "partner": "ENTJ", "partner_advice": "将战略落地全权交由 ENTJ 推进，把 INTP 作为高维模型的逻辑验算机。", "tasks": ["主导 SDE 核心确权底层逻辑架构设计", "重构下一代高并发撮合交易引擎逻辑"], "black_swan": "过度追求底层架构完美闭环。面临突发政策转向时，系统极易因过于重型而无法敏捷掉头。", "patch": "在构建宏大的交易规则体系时，请适当为前台业务预留“沙盒容错”空间。", "skills": ["【被动】全知视界", "【法术】底层规则解构", "【领域】绝对秩序统御"], "base_roi": 1.45, "volatility": 0.20, "market_style": "宏观架构对冲与长期趋势跟踪策略", "evolution_path": ["L1 架构规划官", "L2 核心规则主理人"], "ultimate_evolution": "【绝对算力主宰】掌控数据产品的终极业务定价权"},
    "INTP": {"role": "量化风控专家", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 3.1%", "base_hash": 9620, "desc": "穿透数据迷雾，寻找复杂业务表象下的底层逻辑漏洞与确权定价模型的最优解。", "tags": ["深度解构", "模型驱动", "极客思维"], "partner": "INTJ", "partner_advice": "依托 INTJ 将您的理论模型锚定在现实业务框架内，并借助 ENTP 寻找商业变现出口。", "tasks": ["研发基于特征因子的数据资产动态定价算法", "建立实时数据异常交易嗅探与阻断模型"], "black_swan": "陷入“分析瘫痪”。在需要极速拍板的确权灰度地带，过度追求模型最优解往往导致商机流失。", "patch": "尝试将您极其高维的理论模型降维封装，让算法模型转化为生产力。", "skills": ["【被动】多维特征抽取", "【法术】零日漏洞嗅探", "【秘技】量子坍缩推演"], "base_roi": 1.60, "volatility": 0.45, "market_style": "高频统计套利与多因子量化模型", "evolution_path": ["L1 风控分析师", "L2 模型主理人"], "ultimate_evolution": "【全知算法先知】构建百分百无损的跨网底层风控引擎"},
    "ISTJ": {"role": "合规审查主理官", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 11.6%", "base_hash": 8850, "desc": "SDE 底层防线的守夜人，您的评估本身就是安全、严谨与业务零失误的代名词。", "tags": ["绝对合规", "程序正义", "风险兜底"], "partner": "ESTJ", "partner_advice": "配合 ESTJ 建立坚不可摧的业务推进流水线，由 ISFJ 负责兜底后勤细节。", "tasks": ["主导头部数商“数据资源入表”全链路审计", "设计业务合同与智能合约的合规映射SOP"], "black_swan": "过度依赖既有 SOP。面临无先例创新业务时，容易因“无库可查”产生本能的排斥与误杀。", "patch": "在死守数据合规红线的同时，面对狂飙突进的创新产品，试着用“如何让它合规地上架”来指导业务。", "skills": ["【被动】绝对法典映射", "【护盾】程序正义壁垒", "【反击】致命风险阻断"], "base_roi": 1.15, "volatility": 0.10, "market_style": "绝对风险厌恶与固收类稳健策略", "evolution_path": ["L1 审查风控官", "L2 规则执行官"], "ultimate_evolution": "【绝对防御堡垒】全国一体化数据市场要素流转网络最终守门人"},
    "ESTJ": {"role": "核心业务统筹官", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 8.7%", "base_hash": 9500, "desc": "无可争议的推进器，擅长将国家宏观政策拆解为团队可绝对执行的 KPI 矩阵。", "tags": ["强效统帅", "结果导向", "流程大师"], "partner": "ISTJ", "partner_advice": "让 ISTJ 担任您的品控质检员，在突发高并发危机时，直接将排障指挥权临时移交给 ISTP。", "tasks": ["发起并统筹 SDE 年度交易额破局百亿攻坚战", "强力调度跨部门资源打通确权交易清算堵点"], "black_swan": "KPI压倒一切导致“团队算力过载”。易忽视一线团队的情绪阈值，引发内耗。", "patch": "在下发高压任务指令时，适度向团队释放“情绪价值”。", "skills": ["【被动】战略降维拆解", "【战吼】全域资源狂暴", "【光环】铁腕意志压制"], "base_roi": 1.35, "volatility": 0.25, "market_style": "动量突破与大容量核心资产配置", "evolution_path": ["L1 战区指挥官", "L2 跨域推进者"], "ultimate_evolution": "【全域秩序引擎】宏观数据业务推进的心脏中枢"},
    "INFJ": {"role": "产业生态智囊", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 0.9%", "base_hash": 9200, "desc": "具备极强的跨频段共情能力，能精准预判数据流转对未来实体经济产生的深远变革。", "tags": ["远见卓识", "使命驱动", "战略前瞻"], "partner": "ENFJ", "partner_advice": "将您的远见卓识交由 ENFJ 在核心圈层构建共识，让 ENFP 作为布道火种。", "tasks": ["规划 SDE 未来五年在实体经济的数据赋能版图", "发起“数据向善”及社会公益数据要素流通倡议"], "black_swan": "强烈的战略直觉若缺乏硬核量化数据支撑，极易被贴上“不切实际”标签。", "patch": "学会用精确的财务测算、合规条文来锚定您的宏大产业愿景。", "skills": ["【被动】未来脉络洞视", "【光环】跨频灵魂共振", "【法术】精神信仰织网"], "base_roi": 1.55, "volatility": 0.35, "market_style": "宏观周期预判与长线价值发现", "evolution_path": ["L1 行业分析师", "L2 战略规划官"], "ultimate_evolution": "【全域生态先知】主导数字经济时代的底层精神共识"},
    "INFP": {"role": "生态价值主张官", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 4.4%", "base_hash": 8650, "desc": "冷酷数据背后的灵魂捕捉者，擅长在机械的交易网络中注入引人共鸣的生态文化。", "tags": ["价值感召", "组织粘合", "品牌定调"], "partner": "ENFJ", "partner_advice": "依托 ENFJ 的手腕在跨部门博弈中为您护航，联合 ISFP 将抽象的文化具象化。", "tasks": ["重塑 SDE 在数据交易领域的全球品牌叙事", "实施内部文化与跨部门协作协同凝聚力工程"], "black_swan": "在冷酷的算力与预算博弈中，容易因厌恶冲突而退缩，导致核心价值观无法落地。", "patch": "学会熟练利用预算工具和业务导向来捍卫您的核心价值主张。", "skills": ["【被动】无形文化塑形", "【法术】直击灵魂叙事", "【光环】隐性品牌暴击"], "base_roi": 1.25, "volatility": 0.30, "market_style": "ESG 价值投资与利基市场长尾策略", "evolution_path": ["L1 体验叙事者", "L2 品牌调性官"], "ultimate_evolution": "【灵魂共振奇核】赋予极客冷数据极其昂贵的品牌溢价"},
    "ENTJ": {"role": "战略开拓领军人", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 1.8%", "base_hash": 9900, "desc": "天生的矩阵建设者，在数据跨境、公共数据授权等探索区中展现极强的破局能力。", "tags": ["开疆拓土", "战略铁腕", "极致破局"], "partner": "INTJ", "partner_advice": "冲锋时将后背交给 INTJ 进行战略兜底，遇到底层技术阻击时呼叫 ISTP。", "tasks": ["主导“公共数据授权运营”省级破冰与资源抢占", "制定并执行跨链互认及全国数据大市场吞并战略"], "black_swan": "极速吞并外部资源时极易因忽视底层合规红线而触发监管熔断。", "patch": "在极速开疆拓土时，请时刻保持与合规团队的数据同步。", "skills": ["【被动】绝对铁腕破局", "【战技】全域版图吞并", "【奥义】维度打击风暴"], "base_roi": 1.70, "volatility": 0.55, "market_style": "杠杆并购、特殊机会与高举高打", "evolution_path": ["L1 开拓先锋", "L2 战区统帅"], "ultimate_evolution": "【无界版图霸主】全国一体化数据市场的超级统帅"},
    "ENTP": {"role": "模式创新顾问", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 3.2%", "base_hash": 9400, "desc": "传统交易规则的敏锐挑战者，致力于通过跨界思维寻找下一代数据要素流转范式。", "tags": ["范式重构", "逻辑激辩", "思维跳跃"], "partner": "INTP", "partner_advice": "把天马行空的狂野点子丢给 INTP 进行逻辑降维，并指挥 ESTP 去市场上快速收割。", "tasks": ["研发首个基于 Web3 的新型数据要素凭证", "在监管沙盒内主导蓝海型数字产品变现测试"], "black_swan": "无限发散思维导致的交付烂尾。极易沦为纯粹的纸上谈兵。", "patch": "适当收敛发散思维，选择一个极具潜力的创新点深度闭环。", "skills": ["【被动】旧有范式重塑", "【法术】跨界降维骇入", "【光环】次元逻辑破壁"], "base_roi": 1.65, "volatility": 0.60, "market_style": "风险套利、期权重组与颠覆性投资", "evolution_path": ["L1 沙盒破坏者", "L2 跨界重组官"], "ultimate_evolution": "【范式秩序破坏者】亲手定义下个十年的交易元规则"},
    "ENFJ": {"role": "数商生态总监", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 2.5%", "base_hash": 9350, "desc": "数据交易所的枢纽中心，能通过卓越的共识构建能力将多方利益竞争者聚拢为盟友。", "tags": ["关系枢纽", "温情领导力", "利益协同"], "partner": "INFJ", "partner_advice": "汲取 INFJ 的深度产业洞察作为布道弹药，并由 ESFJ 转化为客情跟进单。", "tasks": ["构建辐射全国的 SDE 头部数商与第三方服务联盟", "维稳数据要素多边市场，调解核心生态伙伴冲突"], "black_swan": "对生态伙伴过度包容。处理违规事件时容易被“人情”裹挟。", "patch": "大胆引入客观的量化算法与智能合约刚性指标，确保生态和谐。", "skills": ["【被动】绝对共识结盟", "【光环】极客温情统御", "【战技】利益杠杆平衡"], "base_roi": 1.40, "volatility": 0.25, "market_style": "庞大资产池宏观调配与网络效应增强", "evolution_path": ["L1 渠道统筹", "L2 联盟主理人"], "ultimate_evolution": "【共识引力波】垄断全国超头数据商的绝对心智"},
    "ENFP": {"role": "平台资源布道大使", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 8.1%", "base_hash": 8900, "desc": "充满感染力的生态火苗，让每一场路演与推介都变成数据要素市场的狂热共识。", "tags": ["无限创意", "跨界纽带", "高频驱动"], "partner": "INFJ", "partner_advice": "在创意发散即将失控时，务必听从 INFJ 的战略纠偏。", "tasks": ["领衔 SDE 全国核心城市业务路演与生态宣发大循环", "策划并主持面向千家数商的“数据赋能创新工坊”"], "black_swan": "路演现场火热但无法转化为 CRM 里的真实入驻率。", "patch": "引入严密的商机日程表与里程碑管理，转化为可追踪漏斗。", "skills": ["【被动】群体情绪煽动", "【法术】全域流量黑洞", "【光环】异构资源嫁接"], "base_roi": 1.40, "volatility": 0.40, "market_style": "高波动趋势追逐与注意力经济炒作", "evolution_path": ["L1 宣发先锋官", "L2 流量矩阵中枢"], "ultimate_evolution": "【无界传播基站】把控国家全域要素市场的流量高地"},
    "ISFJ": {"role": "清结算运营中枢", "tier": "R", "tier_color": "#3b82f6", "rarity": "Top 13.8%", "base_hash": 8200, "desc": "最坚韧的底层支点，通过极致纠错与细节控场支撑起整个平台的专业信誉与高吞吐。", "tags": ["极致支撑", "服务巅峰", "高可用节点"], "partner": "ESFJ", "partner_advice": "将对外的复杂客情交由 ESFJ 抵挡，您只需与 ISTJ 打造坚不可摧的后方堡垒。", "tasks": ["保障全天候撮合及大额资金清结算体系 0 宕机", "极速响应并闭环处理生态节点与数商的底层工单"], "black_swan": "默默承受过载的技术债。可能在交易洪峰期因人工审核量爆表而崩溃。", "patch": "尝试主动提出冗余流程的优化提案。", "skills": ["【被动】极限并发支撑", "【法术】毫米级量子纠错", "【护盾】最后绝对防线"], "base_roi": 1.10, "volatility": 0.08, "market_style": "极低回撤避险与无风险极致套利策略", "evolution_path": ["L1 运营专员", "L2 平台质检官"], "ultimate_evolution": "【绝对永动节点】维持交易所生命线的最终坚盾"},
    "ESFJ": {"role": "政企商务枢纽", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 12.3%", "base_hash": 8750, "desc": "超级连接器，擅长经营多维度的外部政企生态关系，是前线业务部门的最强润滑剂。", "tags": ["协作典范", "客情控制", "社会化支撑"], "partner": "ISFJ", "partner_advice": "把繁杂的合同流转放心抛给 ISFJ，遇到合规红线立刻请 ESTJ 回绝。", "tasks": ["高频维护国家部委及地方大数据局的核心 G 端客情", "统筹落地具有全国影响力的年度数据要素高峰论坛"], "black_swan": "过度满足多方诉求导致的边界失守，签下偏离平台底线的协议。", "patch": "建立更独立的合规风险过滤网。", "skills": ["【被动】政企超级链接", "【光环】社会化缓冲巨网", "【法术】多方负载均衡"], "base_roi": 1.20, "volatility": 0.15, "market_style": "庞大资金盘稳健配置与政企引导基金模式", "evolution_path": ["L1 商务专员", "L2 政企主理"], "ultimate_evolution": "【政企超导桥梁】构筑不可替代的 G 端业务护城河"},
    "ISTP": {"role": "平台风控与排障专家", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 5.4%", "base_hash": 8950, "desc": "数据底座的实干派，只对事实和逻辑代码负责，是系统面临大并发技术故障时的定海神针。", "tags": ["极简实干", "故障排查", "硬核运维"], "partner": "ESTP", "partner_advice": "当 ESTP 在前线疯狂接单导致系统过载时，由您负责底层扩容。", "tasks": ["执行 SDE 核心交易链路的灾备拉起与物理级排障", "在不影响前台撮合的前提下执行底层架构高危热更新"], "black_swan": "过度依赖个人的“极客直觉”排障，一旦休假离线会导致系统应急瘫痪。", "patch": "将底层排查经验沉淀为可视化的《应急响应标准手册》。", "skills": ["【被动】致命物理拔线", "【法术】量子黑盒破解", "【光环】超体极客直觉"], "base_roi": 1.35, "volatility": 0.35, "market_style": "黑天鹅事件驱动、困境反转与系统级技术套利", "evolution_path": ["L1 底层架构师", "L2 灾备指挥官"], "ultimate_evolution": "【底层代码幽灵】掌控国家要素机房的绝对生命力"},
    "ISFP": {"role": "资产交互体验官", "tier": "R", "tier_color": "#3b82f6", "rarity": "Top 8.8%", "base_hash": 8150, "desc": "赋予枯燥数据以美学权重，致力于提升数据产品在终端大屏展示时的绝对视觉专业质感。", "tags": ["审美溢价", "感官叙事", "体验极致"], "partner": "ESFP", "partner_advice": "将美学产出交由 ESFP 在各大峰会上高调发布。", "tasks": ["重构 SDE 实时交易大盘的动态数据全息视觉渲染", "主导面向数商终端的 UI/UX 操作流敏捷体验升级"], "black_swan": "设计出极其炫酷的大屏，却完全脱离了数据确权撮合的核心商业逻辑。", "patch": "适度增加对核心确权流转逻辑和底层交易协议的理解。", "skills": ["【被动】沉浸感官叙事", "【法术】低维美学重构", "【光环】绝对心流捕获"], "base_roi": 1.18, "volatility": 0.22, "market_style": "艺术品级别非标资产与另类情感投资估值", "evolution_path": ["L1 UI视觉专员", "L2 交互总监"], "ultimate_evolution": "【感官具象师】以一己之力拉升数据产品百倍视觉溢价"},
    "ESTP": {"role": "前沿敏捷先锋", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 4.3%", "base_hash": 8800, "desc": "数据流通一线的敏锐猎手，能极快捕捉到瞬息万变的市场红利与应用空间的套利机会。", "tags": ["市场直觉", "敏捷收割", "实战专家"], "partner": "ISTP", "partner_advice": "尽情在市场前线厮杀套利，让 ISTP 为您搭建最稳固的技术跳板。", "tasks": ["敏锐收割新政策出台后的第一波“短期数据流通红利”", "针对区域内竞所的市场抢夺发起极速实战反制突击"], "black_swan": "倾向于利用捷径绕过繁琐的合规防火墙，一旦溯源出瑕疵将面临毁灭性反噬。", "patch": "在展现高效行动力促成交易时，务必将前置合规审查纳入操作流程中。", "skills": ["【被动】毫秒瞬时收割", "【战技】全图火力覆盖", "【光环】血腥红利嗅探"], "base_roi": 1.50, "volatility": 0.50, "market_style": "超高频日内交易与极限突发利好嗜血收割", "evolution_path": ["L1 突击交易员", "L2 战地狼王"], "ultimate_evolution": "【极速套利猎手】全网数据交易套利空间的绝杀狙击者"},
    "ESFP": {"role": "官方品牌发声信标", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 9.9%", "base_hash": 8300, "desc": "交易所的前台形象窗口，天生具备将复杂的政策解码为大众传播话术的超级天赋。", "tags": ["全域表现", "舆情响应", "公关信标"], "partner": "ISFP", "partner_advice": "用极具感染力的表现为 ISFP 的视觉产品带货，并与 ENFP 联手策划掀起全网狂潮的路演。", "tasks": ["在全网引爆 SDE 最新明星数据产品的展会级宣发流量", "冲在第一线对冲平台突发的负面市场舆情并进行柔性公关"], "black_swan": "对外宣发时极易出现“用词越界”，引发监管舆情风险。", "patch": "花时间深潜研究数据要素的底层逻辑与政策红头文件。", "skills": ["【被动】全域舆论控场", "【光环】情绪频率调控", "【奥义】暴走危机降维"], "base_roi": 1.35, "volatility": 0.38, "market_style": "舆论狂热驱动、社交媒体共振与情绪面交易", "evolution_path": ["L1 品牌代言", "L2 首席发言人"], "ultimate_evolution": "【极速情绪信标】左右资本市场情绪波动的首席发声端"}
}

# 🏰 TCG 阵营定义 (安全字典)
def get_faction_info(mbti_code):
    if "NT" in mbti_code: return {"name": "赛博真理会 (NT)", "element": "⚡ 量子", "color": "#ffd700"}
    if "NF" in mbti_code: return {"name": "以太灵能网 (NF)", "element": "✨ 灵能", "color": "#a855f7"}
    if "SJ" in mbti_code: return {"name": "绝对秩序阵线 (SJ)", "element": "🛡️ 钢核", "color": "#10b981"}
    if "SP" in mbti_code: return {"name": "混沌游侠公会 (SP)", "element": "🔥 炎脉", "color": "#ff003c"}
    return {"name": "无界佣兵", "element": "🌌 暗物质", "color": "#ffffff"}

# 🎁 圣遗物盲盒卡池 (Relic Pool) - 物理隔离，彻底解决 KeyError
RELICS_POOL = [
    {"name": "【UR】中本聪的创世U盘", "rarity": "UR", "cp": 30000, "desc": "无视合规红线，全属性巨幅飙升", "color": "#ff003c"},
    {"name": "【UR】V神的破碎怀表", "rarity": "UR", "cp": 25000, "desc": "回溯智能合约状态，掌控时间流动", "color": "#ff003c"},
    {"name": "【SSR】破壁者的金库密钥", "rarity": "SSR", "cp": 12000, "desc": "撮合交易时，自动剥夺对手15%利润", "color": "#ffd700"},
    {"name": "【SSR】统帅的暴走号角", "rarity": "SSR", "cp": 11500, "desc": "同盟阵列全员战力进入狂热状态", "color": "#ffd700"},
    {"name": "【SSR】量子裁决天平", "rarity": "SSR", "cp": 10000, "desc": "强制引发风控熔断，无视一切黑天鹅", "color": "#ffd700"},
    {"name": "【SR】数据局长的不锈钢杯", "rarity": "SR", "cp": 5000, "desc": "在合规风暴中保持绝对的冷静", "color": "#a855f7"},
    {"name": "【SR】极客的机械义眼", "rarity": "SR", "cp": 4500, "desc": "底层代码纠错与漏洞嗅探效率+300%", "color": "#a855f7"},
    {"name": "【SR】布道者的炽热火种", "rarity": "SR", "cp": 4000, "desc": "瞬间点燃全网要素市场的 FOMO 情绪", "color": "#a855f7"},
    {"name": "【R】满是 Bug 的旧键盘", "rarity": "R", "cp": 1500, "desc": "虽然旧了，但敲击的段落感依然清脆", "color": "#3b82f6"},
    {"name": "【R】特氟龙防粘平底锅", "rarity": "R", "cp": 1200, "desc": "完美反弹一次本不属于你的线上事故", "color": "#3b82f6"},
    {"name": "【R】发黄的古老运维手册", "rarity": "R", "cp": 1000, "desc": "隐约记录着上古机房的强制重启指令", "color": "#3b82f6"}
]

# 🤝 协同羁绊与算法
def calculate_synergy(m1, m2):
    diff = sum(1 for a, b in zip(m1, m2) if a != b)
    if diff == 0: return 92, "【绝对镜像】回路高度一致，沟通0延迟，但需警惕盲区重叠。"
    elif diff == 1: return 98, "【黄金羁绊】核心逻辑高度一致且具备极佳互补，SDE最强双打组合！"
    elif diff == 2: return 85, "【灰度容错】视角差异带来火花，能打磨出更抗风险的战术闭环。"
    elif diff == 3: return 65, "【高频摩擦】底层通信壁垒极大，需要引入第三方作为战术缓冲。"
    else: return 99, "【阴阳反转】代码完全相反！日常极度痛苦，但若背靠背能实现全图包抄！"

def generate_alpha_curve(base_roi, volatility, seed):
    rng = np.random.RandomState(seed) 
    days = [f"T+{i}" for i in range(1, 31)] 
    roi = [100.0]
    for _ in range(29): roi.append(max(30.0, roi[-1] + (base_roi - 1.0) * 8 + rng.normal(0, volatility * 25)))
    return days, roi

def generate_bids(hash_int):
    rng = np.random.RandomState(hash_int)
    companies = ["0xAI_Core", "ByteMatrix", "G-Cloud", "Web3_Unicorn", "FinTech_Giant"]
    bids = []
    for _ in range(4):
        comp = rng.choice(companies)
        size = rng.randint(10, 99) * 1000
        premium = round(rng.uniform(5.5, 35.5), 1)
        bids.append("<div style='display:flex; justify-content:space-between; margin-bottom:10px; color:#10b981; border-bottom:1px dashed rgba(16,185,129,0.2); padding-bottom:6px; font-family:\"Fira Code\", monospace; font-size:13px; animation: flash-row 2s infinite alternate;'><span style='width:40%; text-align:left;'>" + comp + "</span><span style='width:30%; text-align:center;'>" + str(size) + "</span><span style='width:30%; text-align:right;'>+" + str(premium) + "%</span></div>")
    return "".join(bids)

def get_market_depth_html(hash_int):
    rng = np.random.RandomState(hash_int)
    bids = sorted([rng.uniform(0.1, 0.9) for _ in range(18)])
    asks = sorted([rng.uniform(0.1, 0.9) for _ in range(18)], reverse=True)
    b_html = "".join(["<div style='flex:1; background:linear-gradient(to top, rgba(16,185,129,0.1), rgba(16,185,129,0.8)); height:" + str(b*100) + "%; border-top:1px solid #10b981; margin-right:1px; border-radius:2px 2px 0 0;'></div>" for b in bids])
    a_html = "".join(["<div style='flex:1; background:linear-gradient(to top, rgba(244,63,94,0.1), rgba(244,63,94,0.8)); height:" + str(a*100) + "%; border-top:1px solid #f43f5e; margin-left:1px; border-radius:2px 2px 0 0;'></div>" for a in asks])
    spread = str(round(rng.uniform(0.01, 0.05), 4))
    return "<div style='display:flex; height: 80px; align-items:flex-end; width:100%; margin-bottom:15px; border-bottom: 1px solid #334155; padding-bottom:5px;'><div style='flex:1; display:flex; align-items:flex-end; height:100%; padding-right:5px;'>" + b_html + "</div><div style='width:2px; height:100%; background:#94a3b8; margin:0 2px;'></div><div style='flex:1; display:flex; align-items:flex-end; height:100%; padding-left:5px;'>" + a_html + "</div></div><div style='display:flex; justify-content:space-between; font-size:10px; color:#94a3b8; font-family:monospace; margin-bottom:20px;'><span>BIDS VOL</span><span style='color:#00f3ff; font-weight:bold;'>SPREAD: " + spread + "</span><span>ASKS VOL</span></div>"

# 🌌 3D 认知拓扑星图算法 (满血找回，绝对安全)
def get_3d_topology(val_E, val_I, val_S, val_N, val_T, val_F, mbti_code, tier_color, hash_int):
    rng = np.random.RandomState(hash_int)
    f3d = go.Figure()
    f3d.add_trace(go.Scatter3d(x=rng.randint(-100,100,80), y=rng.randint(-100,100,80), z=rng.randint(-100,100,80), mode='markers', marker=dict(size=3, color='#334155', opacity=0.5), hoverinfo='none'))
    x_v = val_E if val_E > val_I else -val_I
    y_v = val_S if val_S > val_N else -val_N
    z_v = val_T if val_T > val_F else -val_F
    f3d.add_trace(go.Scatter3d(x=[x_v], y=[y_v], z=[z_v], mode='markers+text', text=[mbti_code], textposition="top center", marker=dict(size=14, color=tier_color, symbol='diamond', line=dict(color='#fff', width=2)), textfont=dict(color=tier_color, size=16, family="Orbitron", weight="bold")))
    f3d.update_layout(scene=dict(xaxis_title='E/I', yaxis_title='N/S', zaxis_title='T/F', xaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b", showticklabels=False), yaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b", showticklabels=False), zaxis=dict(backgroundcolor="#020617", gridcolor="#1e293b", showticklabels=False)), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=350, showlegend=False)
    return f3d

# ==============================================================================
# 🎮 [ SDE V11 ] 卡游动作回调函数 (Action Callbacks)
# ==============================================================================
def draw_relic_callback():
    if st.session_state.tokens >= 1000:
        st.session_state.tokens -= 1000
        roll = random.random()
        if roll < 0.05: r = random.choice([x for x in RELICS_POOL if x['rarity']=='UR'])
        elif roll < 0.20: r = random.choice([x for x in RELICS_POOL if x['rarity']=='SSR'])
        elif roll < 0.60: r = random.choice([x for x in RELICS_POOL if x['rarity']=='SR'])
        else: r = random.choice([x for x in RELICS_POOL if x['rarity']=='R'])
        
        # 深拷贝并赋予独立 ID
        r_copy = copy.deepcopy(r)
        r_copy['uid'] = f"rel_{int(time.time()*1000)}_{random.randint(0,999)}"
        st.session_state.inventory.insert(0, r_copy)
        st.session_state.gacha_msg = f"🎉 神经元接驳成功！获得 {r_copy['rarity']} 级圣物：<b style='color:{r_copy['color']};'>{r_copy['name']}</b>"
    else:
        st.session_state.gacha_msg = "<span style='color:#f43f5e;'>❌ 资金不足！需要 1,000 $SDE。</span>"

def equip_relic_callback(uid):
    for r in st.session_state.inventory:
        if r['uid'] == uid:
            # 检查是否已装备，如果已装备则卸下
            if any(eq['uid'] == uid for eq in st.session_state.equipped_relics):
                st.session_state.equipped_relics = [eq for eq in st.session_state.equipped_relics if eq['uid'] != uid]
            else:
                if len(st.session_state.equipped_relics) < 3:
                    st.session_state.equipped_relics.append(r)
                else:
                    st.session_state.equipped_relics.pop(0)
                    st.session_state.equipped_relics.append(r)
            break

def attack_boss_callback():
    if st.session_state.stamina < 10:
        st.session_state.combat_logs.insert(0, "❌ <span style='color:#f43f5e;'>体力不足，无法执行讨伐！需要 10 体力。</span>")
        return
    st.session_state.stamina -= 10
    cp = st.session_state.get('final_cp_cache', 10000)
    is_crit = random.random() < 0.25
    dmg = int(cp * random.uniform(0.8, 1.2) * (2.0 if is_crit else 1.0) / 10)
    st.session_state.boss_hp -= dmg
    crit_tag = "<b style='color:#ff003c;'>[CRITICAL STRIKE]</b> " if is_crit else ""
    st.session_state.combat_logs.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] ⚔️ {crit_tag}对【数据孤岛】造成了 <b style='color:#ffd700;'>{dmg:,}</b> 点伤害！")
    
    drop = int(dmg / 5)
    st.session_state.tokens += drop
    st.session_state.exp += 20
    
    if st.session_state.boss_hp <= 0:
        st.session_state.combat_logs.insert(0, "🏆 <b style='color:#10b981;'>[WORLD FIRST] 利维坦已被击破！全服发放奖励 50,000 $SDE！</b>")
        st.session_state.tokens += 50000
        st.session_state.boss_hp = 99999999
        
    if st.session_state.exp >= st.session_state.level * 100:
        st.session_state.exp -= st.session_state.level * 100
        st.session_state.level += 1
        st.session_state.combat_logs.insert(0, f"🌟 <b style='color:#a855f7;'>升级！当前等级: Lv.{st.session_state.level}，战力获得了提升！</b>")

def pvp_battle_callback(target_faction):
    if st.session_state.stamina < 15:
        st.session_state.pvp_logs.insert(0, "❌ <span style='color:#f43f5e;'>体力不足，无法进入竞技场！需要 15 体力。</span>")
        return
    st.session_state.stamina -= 15
    cp = st.session_state.get('final_cp_cache', 10000)
    enemy_cp = int(cp * random.uniform(0.7, 1.4))
    st.session_state.pvp_logs.insert(0, f"=====================")
    st.session_state.pvp_logs.insert(0, f"⚔️ 遭遇敌对阵营: {target_faction} (敌方战力: {enemy_cp:,})")
    if cp >= enemy_cp:
        loot = int(enemy_cp * random.uniform(0.05, 0.15))
        st.session_state.pvp_logs.insert(0, f"🏆 <b style='color:#10b981;'>胜利！算力碾压对手！掠夺了 {loot:,} $SDE！</b>")
        st.session_state.tokens += loot
        st.session_state.exp += 50
    else:
        st.session_state.pvp_logs.insert(0, f"💀 <b style='color:#ff003c;'>败北... 遭到降维打击，护盾破裂。</b>")
        st.session_state.exp += 10
        
    if st.session_state.exp >= st.session_state.level * 100:
        st.session_state.exp -= st.session_state.level * 100
        st.session_state.level += 1
        st.session_state.pvp_logs.insert(0, f"🌟 <b style='color:#a855f7;'>升级！当前等级: Lv.{st.session_state.level}</b>")

# ==============================================================================
# 🖥️ [ SDE V11 ] 塔台级路由与全息仪表盘渲染
# ==============================================================================
if not st.session_state.started:
    st.markdown("<div style='margin-top:50px;'></div>", unsafe_allow_html=True)
    
    if not st.session_state.boot_played:
        BOOT_CSS = """<style>.sys-boot-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #030712; z-index: 9999999; display: flex; justify-content: center; align-items: center; flex-direction: column; animation: sys-boot-fade 1.5s 2.2s cubic-bezier(0.8, 0, 0.2, 1) forwards; pointer-events: none; }.sys-boot-logo { color: #00f3ff; font-family: 'Orbitron', monospace; font-size: 24px; font-weight: 900; letter-spacing: 4px; overflow: hidden; border-right: 3px solid #00f3ff; white-space: nowrap; animation: typing-boot 0.8s steps(20, end) forwards, blink-boot 0.4s step-end infinite; margin-bottom: 15px; }.sys-boot-bar-bg { width: 300px; height: 2px; background: rgba(0,243,255,0.1); position: relative; }.sys-boot-bar-fill { position: absolute; top: 0; left: 0; height: 100%; background: #00f3ff; box-shadow: 0 0 15px #00f3ff; animation: load-boot 1.8s ease-out forwards; }.sys-boot-logs { margin-top: 15px; font-family: 'Fira Code', monospace; font-size: 10px; color: #10b981; opacity: 0.8; height: 45px; overflow: hidden; width: 300px; text-align: left; line-height: 15px; }.log-line { animation: log-scroll 1.8s steps(10, end) forwards; transform: translateY(45px); }@keyframes typing-boot { from { width: 0; } to { width: 300px; } }@keyframes blink-boot { 50% { border-color: transparent; } }@keyframes load-boot { 0% { width: 0%; } 10% { width: 30%; } 40% { width: 40%; } 60% { width: 80%; } 100% { width: 100%; } }@keyframes sys-boot-fade { to { opacity: 0; visibility: hidden; } }@keyframes log-scroll { 100% { transform: translateY(-100px); } }</style>"""
        HTML_BOOT = BOOT_CSS.replace('\n', '') + """<div class="sys-boot-overlay"><div class="sys-boot-logo">SDE_TCG_V11.0</div><div class="sys-boot-bar-bg"><div class="sys-boot-bar-fill"></div></div><div class="sys-boot-logs"><div class="log-line">[OK] Booting GOD MODE Engine...<br>[OK] Connecting to Ledger...<br>[OK] Decrypting 18-dim Matrix...<br>[OK] Mounting Gacha Module...<br>[OK] Loading Raid Boss Assets...<br>[OK] Bypassing Security Firewall...<br>[OK] Handshake Established.</div></div></div>"""
        st.markdown(HTML_BOOT, unsafe_allow_html=True)
        st.session_state.boot_played = True

    with center_container():
        HTML_TITLE = """<div style="text-align: center; margin-bottom: 20px;"><div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:14px; letter-spacing:8px; margin-bottom:10px;">SHANGHAI DATA EXCHANGE</div><h1 class="hero-title" data-text="职场元宇宙 V11">职场元宇宙 V11</h1><div style="color:#a855f7; font-family:'Orbitron', sans-serif; font-size:13px; font-weight:900; letter-spacing:6px; margin-bottom:30px; margin-top:5px;">GOD_MODE_METAVERSE</div></div>"""
        st.markdown(HTML_TITLE.replace('\n', ''), unsafe_allow_html=True)

        HTML_TERM = """<div style="background: rgba(8, 15, 30, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: clamp(15px, 4vw, 25px); border-radius: 8px; font-family: 'Fira Code', monospace; font-size: clamp(12px, 3vw, 14px); color: #e2e8f0; box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px;"><div style="color:#94a3b8; margin-bottom:5px;">[SYSTEM] Securing root connection... <span style="color:#10b981;">[ESTABLISHED]</span></div><div style="color:#94a3b8;">[KERNEL] Loading 40-Node Matrix V11.0... <span style="color:#10b981;">[READY]</span></div><div style="margin-top:15px; font-family: 'Noto Sans SC', sans-serif; line-height: 1.8; color:#fff;"><b>数据要素价值释放的纪元已经降临。</b><br>本终端将全方位扫描您的职场决策链路。<br>您的物理能力将被<b>「全息要素化」</b>，系统将为您解封一张独一无二的<b>高阶职场算力实体卡牌 (SBT)</b>，并开启属于您的深潜远征！</div></div>"""
        st.markdown(HTML_TERM.replace('\n', ''), unsafe_allow_html=True)

        with st.form(key="login_form", border=False):
            st.markdown("<div style='color:#ffd700; font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:bold; margin-bottom:8px; text-align:center;'>▼ 挂载节点代号 (MOUNT_NODE) ▼</div>", unsafe_allow_html=True)
            st.text_input("", key="login_input", placeholder="输入您的职场代号", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            st.form_submit_button("▶ 开启神经元校准并抽卡 (PULL CARD)", on_click=start_assessment_callback, type="primary", use_container_width=True)

elif st.session_state.calculating:
    with center_container():
        st.markdown("<h2 class='hero-title' data-text='[ ZK-PROOF UNSEALING... ]' style='font-size:clamp(20px, 4vw, 28px) !important; margin-top:50px; text-align:center; display:block;'>[ ZK-PROOF UNSEALING... ]</h2>", unsafe_allow_html=True)
        mint_box = st.empty()
        h_logs = ""
        phases = ["[SYNCING EVM]", "[EXTRACTING]", "[ZK-PROOF]", "[MINTING CARDS]"]
        for i in range(12):
            fake_hash = hashlib.sha256(str(random.random()).encode()).hexdigest().upper()
            h_logs = f"<span style='color:#94a3b8;'>{phases[i % 4]}</span> <span style='color:#ffd700;'>0x{fake_hash[:24]}...</span> <span style='color:#10b981;'>[OK]</span><br>" + h_logs
            mint_box.markdown(f"<div style='background:#000; border:1px solid #334155; border-left:4px solid #00f3ff; padding:20px; border-radius:8px; font-family:monospace; font-size:13px; height:250px; overflow:hidden; color:#4ade80;'>{h_logs}</div>".replace('\n', ''), unsafe_allow_html=True)
            time.sleep(0.15)
        st.session_state.calculating = False; st.rerun()

elif st.session_state.current_q < len(questions):
    # 🕹️ 游戏化侧边栏 (HUD)
    with st.sidebar:
        st.markdown("<div style='text-align:center; font-family:Orbitron; font-size:20px; font-weight:900; color:#ffd700; margin-bottom:20px;'>SDE V11.0 HUD</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:rgba(5,10,20,0.8); border:1px solid #334155; border-radius:8px; padding:15px; margin-bottom:15px; font-family:Orbitron;'><div style='color:#94a3b8; font-size:10px; margin-bottom:5px; font-weight:bold;'>[ NODE IDENTIFIER ]</div><div style='color:#fff; font-size:16px; font-weight:bold;'>{st.session_state.user_alias}</div></div>", unsafe_allow_html=True)
        st.markdown("<div style='background:rgba(5,10,20,0.8); border:1px solid #334155; border-radius:8px; padding:15px; margin-bottom:15px; font-family:Orbitron;'><div style='color:#94a3b8; font-size:10px; margin-bottom:5px; font-weight:bold;'>[ SYSTEM SYNC ]</div><div style='color:#10b981; font-size:16px; font-weight:bold; animation: blink 1s infinite;'>IN PROGRESS...</div></div>", unsafe_allow_html=True)
        
    with center_container():
        q_data = questions[st.session_state.current_q]
        module_name = {"E": "外联输出网络", "S": "颗粒实务穿透", "T": "客观量化护甲", "J": "秩序架构锚定"}.get(q_data['dim'])
        dynamic_hash = hashlib.sha256(f"BLOCK_{st.session_state.current_q}_{q_data['q']}".encode()).hexdigest()[:10].upper()
        
        st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
        progress_val = (st.session_state.current_q + 1) / len(questions)
        st.progress(progress_val)
        st.markdown(f"<div style='text-align:right; font-family:Orbitron, monospace; color:#ffd700; font-size:12px; margin-top:5px; font-weight:bold;'>SYNC RATE: {int(progress_val*100)}%</div>", unsafe_allow_html=True)
        
        HTML_Q = f"""<div style="background: rgba(10, 15, 25, 0.9); border: 2px solid rgba(0, 243, 255, 0.4); border-radius: 12px; padding: clamp(20px, 4vw, 30px); box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 20px rgba(0, 243, 255, 0.05); margin-top: 20px; margin-bottom: 30px;"><div style="display:flex; justify-content:space-between; font-family:monospace; color:#00f3ff; font-size:11px; margin-bottom:15px; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom:10px;"><span style="font-family:'Orbitron', sans-serif;">MOD: {module_name}</span><span style="font-family:'Orbitron', sans-serif;">HASH: 0x{dynamic_hash}</span></div><div style="font-size: clamp(15px, 4vw, 18px); color: #ffffff !important; line-height: 1.8; font-weight: 700;">{q_data['q']}</div></div>"""
        st.markdown(HTML_Q.replace('\n', ''), unsafe_allow_html=True)
        
        opts = [("🚫 强制阻断 (完全背离直觉)", 1), ("⚠️ 弱态耦合 (极少采用)", 2), ("⚖️ 视境判定 (看情况而定)", 3), ("🤝 逻辑握手 (常用决策流)", 4), ("🔒 绝对锁定 (完美复刻思维)", 5)]
        for text, val in opts: st.button(text, type="secondary", key=f"q_{st.session_state.current_q}_{val}", on_click=answer_callback, args=(val, q_data['dim']))

else:
    # ==========================
    # TCG 核心数据结算与属性计算
    # ==========================
    res = st.session_state.total_scores
    mbti = ("E" if res.get("E", 0) >= 0 else "I") + ("S" if res.get("S", 0) >= 0 else "N") + ("T" if res.get("T", 0) >= 0 else "F") + ("J" if res.get("J", 0) >= 0 else "P")
    data = mbti_details.get(mbti, mbti_details["INTJ"])
    faction_data = get_faction_info(mbti)
    
    tier_level = data.get('tier', 'SR')
    tier_color = data.get('tier_color', '#a855f7')
    role_name = data.get('role', '未知节点')
    safe_alias_final = st.session_state.user_alias.upper()
    
    # 💥 SSR 盲盒碎屏抽卡仪式 (物理分离 CSS 防错)
    if not st.session_state.anim_played: 
        st.balloons()
        glow_color = "#ff003c" if tier_level == "UR" else "#ffd700" if tier_level == "SSR" else "#00f3ff"
        GACHA_CSS = """<style>.gacha-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(3,7,18,0.98); z-index: 999999; display: flex; justify-content: center; align-items: center; flex-direction: column; animation: cyber-fadeout 3.5s cubic-bezier(0.8, 0, 0.2, 1) forwards; pointer-events: none; backdrop-filter: blur(8px); }.gacha-cube { width: 80px; height: 80px; border: 4px solid #fff; box-shadow: 0 0 20px #fff, inset 0 0 20px #fff; transform: rotate(45deg); animation: cube-shake 2s ease-in forwards, cube-burst 0.5s 2s forwards; position: relative; }.gacha-cube::after { content:''; position: absolute; top:0; left:0; width:100%; height:100%; background: VAR_GLOW; opacity:0; animation: cube-glow 2s forwards; }.gacha-text { font-family: 'Orbitron', sans-serif; font-size: clamp(24px, 5vw, 64px); font-weight: 900; color: #fff; letter-spacing: 12px; opacity: 0; animation: pop-in 1.5s 2s cubic-bezier(0.1, 0.8, 0.3, 1) forwards; position: relative; z-index: 2; margin-top: 60px; text-transform: uppercase; text-shadow: 0 0 40px VAR_GLOW, 0 0 80px VAR_GLOW; }@keyframes cube-shake { 0% { transform: rotate(45deg) scale(1); } 80% { transform: rotate(405deg) scale(1.2); border-color: VAR_GLOW; box-shadow: 0 0 40px VAR_GLOW; } 100% { transform: rotate(405deg) scale(0.1); opacity: 0; } }@keyframes cube-glow { 80% { opacity: 0.8; } 100% { opacity: 1; } }@keyframes cube-burst { 0% { transform: scale(0.1); opacity: 1; box-shadow: 0 0 100px 50px VAR_GLOW; } 100% { transform: scale(15); opacity: 0; box-shadow: 0 0 0 0 transparent; } }@keyframes pop-in { 0% { transform: scale(0.5); opacity: 0; } 40% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(1); opacity: 1; } }@keyframes cyber-fadeout { 0%, 85% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }</style>"""
        HTML_EMP = GACHA_CSS.replace("VAR_GLOW", glow_color).replace('\n', '') + f"""<div class="gacha-overlay"><div class="gacha-cube"></div><div class="gacha-text">{tier_level} CARD UNLOCKED</div></div>"""
        st.markdown(HTML_EMP, unsafe_allow_html=True)
        st.session_state.anim_played = True
        
    extremes = sum(abs(v) for v in res.values())
    if extremes > 16: card_prefix = "【极端的】"
    elif res.get('E', 0) > 3: card_prefix = "【狂热的】"
    elif res.get('I', 0) > 3: card_prefix = "【深潜的】"
    elif res.get('T', 0) > 3: card_prefix = "【冷酷的】"
    elif res.get('J', 0) > 3: card_prefix = "【秩序的】"
    elif res.get('P', 0) > 3: card_prefix = "【混沌的】"
    else: card_prefix = "【觉醒的】"
    full_title = f"{card_prefix}{role_name}"
    
    def get_intensity(score): return int(max(0, min(100, 50 + (score * 2.5))))
    val_E, val_I = get_intensity(res.get("E", 0)), 100 - get_intensity(res.get("E", 0))
    val_S, val_N = get_intensity(res.get("S", 0)), 100 - get_intensity(res.get("S", 0))
    val_T, val_F = get_intensity(res.get("T", 0)), 100 - get_intensity(res.get("T", 0))
    val_J, val_P = get_intensity(res.get("J", 0)), 100 - get_intensity(res.get("J", 0))

    categories = ['输出(E)', '精准(S)', '护甲(T)', '秩序(J)', '隐匿(I)', '视界(N)', '共情(F)', '敏捷(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]

    p_score, s_score = -res.get("J", 0), res.get("S", 0)
    risk_score = int(max(5, min(95, 50 + (p_score * 1.5) - (s_score * 1.5))))
    if risk_score < 35: r_tag, r_color = "绝对合规防线", "#10b981"
    elif risk_score < 65: r_tag, r_color = "动态灰度平衡", "#ffd700"
    else: r_tag, r_color = "无界极限破局", "#ff003c"

    time_taken = max(1.0, st.session_state.end_time - st.session_state.start_time)
    
    # 🔐 资产防篡改物理锁：仅在完成瞬间生成一次
    if "asset_minted" not in st.session_state or st.session_state.asset_minted.get("version") != VERSION:
        h_code = hashlib.sha256(f"{safe_alias_final}{mbti}{time_taken}{VERSION}".encode()).hexdigest().upper()
        h_int = int(h_code[:8], 16)
        
        avg_q_time = time_taken / len(questions)
        dec_index = int(min(99, max(35, 100 - (max(0, avg_q_time - 2.5) * 5))))
        base_cp = int(data.get('base_hash', 8000) * (1 + (extremes/80.0)*0.4) * (0.8 + (dec_index/100.0)*0.5) * (0.9 + (h_int % 200)/1000.0) * 10000)
        
        # 初始资源下发
        st.session_state.tokens += 10000 
        
        st.session_state.asset_minted = {
            "version": VERSION,
            "hash_code": h_code,
            "block_height": f"V11-{(int(time.time()) % 1000000):06d}",
            "time_str": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "token_id": int(hashlib.md5(f"{safe_alias_final}{time_taken}".encode()).hexdigest()[:8], 16),
            "contract_addr": "0x" + hashlib.sha256(f"contract_{mbti}_{h_int}".encode()).hexdigest()[:38],
            "base_cp": base_cp,
            "pct_beat": round(min(99.9, max(50.0, 60 + (dec_index * 0.3) + ((extremes/80.0) * 20))), 1)
        }
        
    asset = st.session_state.asset_minted
    hash_code = asset["hash_code"]
    block_height = asset["block_height"]
    current_time_str = asset["time_str"]
    token_id = asset["token_id"]
    contract_addr = asset["contract_addr"]
    base_cp = asset["base_cp"]
    pct_beat = asset["pct_beat"]
    h_int = int(hash_code[:8], 16)
    
    # 动态获取当前最终战力 (带等级与圣遗物加成)
    relic_cp_total = sum([r.get('cp', 0) for r in st.session_state.equipped_relics])
    level_mult = 1.0 + (st.session_state.level - 1) * 0.05
    final_cp = int((base_cp + relic_cp_total) * level_mult)
    st.session_state.final_cp_cache = final_cp
    
    valuation_str = f"{final_cp:,}"
    pct_beat_final = min(99.9, pct_beat + (relic_cp_total/200000))

    svg_icon = get_identicon_html(hash_code, tier_color)

    # 🕹️ 游戏化左侧栏 (HUD)
    with st.sidebar:
        st.markdown("<div style='text-align:center; font-family:Orbitron; font-size:20px; font-weight:900; color:#ffd700; margin-bottom:20px;'>TCG HUD V11</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-box'><div class='hud-title'>[ NODE ALIAS ]</div><div class='hud-val' style='color:#fff;'>{safe_alias_final}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-box'><div class='hud-title'>[ FACTION ]</div><div class='hud-val' style='color:{faction_data['color']}; font-family:\"Noto Sans SC\"; font-size:14px;'>{faction_data['name']}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-box'><div class='hud-title'>[ NODE LEVEL ]</div><div class='hud-val' style='color:#a855f7;'>Lv. {st.session_state.level}</div><div style='background:rgba(255,255,255,0.1); height:4px; margin-top:5px;'><div style='background:#a855f7; width:{min(100, st.session_state.exp / (st.session_state.level * 100) * 100)}%; height:100%;'></div></div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-box'><div class='hud-title'>[ STAMINA ]</div><div class='hud-val' style='color:#10b981;'>{st.session_state.stamina} / 120</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-box'><div class='hud-title'>[ $SDE BALANCE ]</div><div class='hud-val' style='color:#ffd700;'>{st.session_state.tokens:,} 🪙</div></div>", unsafe_allow_html=True)
        
        if st.button("🛌 冥想休息 (消耗 500 SDE 恢复 20 体力)", use_container_width=True):
            if st.session_state.tokens >= 500:
                st.session_state.tokens -= 500
                st.session_state.stamina = min(120, st.session_state.stamina + 20)
                st.rerun()

    # =========================================================================
    # 📱【第一排：卡牌主界面与双轨羁绊沙盘】
    # =========================================================================
    HTML_BANNER = f"""<div style="background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(10,15,30,0.9)); border: 1px solid #10b981; border-radius: 8px; padding: 15px 25px; margin-bottom: 25px; font-family: 'Orbitron', monospace; box-shadow: 0 0 20px rgba(16,185,129,0.2);"><div style="color: #10b981; font-size: 14px; font-weight: bold; border-bottom: 1px dashed #10b981; padding-bottom: 10px; margin-bottom: 12px; display:flex; align-items:center;"><span style="font-size:20px; margin-right:10px;">🏆</span> <span>SDE HOLO-CARD MINTED [ GOD_MODE ]</span></div><div style="font-size: 12px; color: #94a3b8; line-height: 1.8; display:flex; flex-wrap: wrap; justify-content: space-between; gap: 10px;"><div><div><span style="color:#e2e8f0;">BLOCK HEIGHT:</span> {block_height}</div><div><span style="color:#e2e8f0;">CONTRACT:</span> {contract_addr[:20]}...</div></div><div style="text-align: left;"><div><span style="color:#e2e8f0;">TOKEN ID:</span> #{token_id}</div><div><span style="color:#e2e8f0;">TIMESTAMP:</span> {current_time_str}</div></div></div></div>"""
    st.markdown(HTML_BANNER.replace('\n', ''), unsafe_allow_html=True)

    col_top_l, col_top_r = st.columns([1.1, 1.3], gap="large")

    with col_top_l:
        tags_html_web = "".join([f"<span style='background:rgba(255, 215, 0, 0.1); color:#ffd700 !important; border:1px solid rgba(255,215,0,0.4); padding:6px 14px; border-radius:6px; font-size:13px; font-weight:900; margin:4px; display:inline-block; font-family:\"Noto Sans SC\"; box-shadow: 0 0 10px rgba(255,215,0,0.1);'>{t}</span>" for t in data.get('tags', [])])
        skills_html_web = "".join([f"<div style='background:linear-gradient(90deg, rgba(168,85,247,0.3), rgba(168,85,247,0.05)); border:1px solid rgba(168,85,247,0.5); border-left:4px solid #a855f7; padding:8px 12px; border-radius:6px; font-size:13px; color:#e9d5ff; font-weight:bold; margin-bottom:8px; box-shadow: 0 0 15px rgba(168,85,247,0.1); text-align:left;'>{s}</div>" for s in data.get('skills', [])])
        
        relics_html_web = "".join([f"<span style='display:inline-block; background:rgba(255,255,255,0.1); border:1px solid {r['color']}; color:{r['color']}; padding:4px 8px; border-radius:4px; font-size:10px; margin:3px; font-weight:bold;'>{r['name']}</span>" for r in st.session_state.equipped_relics])
        if not relics_html_web: relics_html_web = "<span style='color:#64748b; font-size:11px;'>[ 未装备任何圣遗物 ]</span>"

        # 💎 悬浮光剑边框 3D 实体卡牌
        CARD_CSS = """<style>.tcg-card-container { perspective: 1500px; width: 100%; margin-bottom: 30px; display: flex; justify-content: center; z-index: 50; position: relative; }.tcg-card { width: 100%; max-width: 480px; position: relative; transform-style: preserve-3d; transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1); border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.9), 0 0 40px rgba(0,243,255,0.2); background: #0b1120; border: 2px solid VAR_TIER; overflow: hidden; }.tcg-card:hover { transform: rotateY(8deg) rotateX(-5deg) translateY(-10px) scale(1.02); box-shadow: -20px 40px 80px rgba(0,0,0,0.9), 0 0 60px VAR_TIER88; }.tcg-card::after { content: ""; position: absolute; inset: 0; background: linear-gradient(125deg, transparent 20%, rgba(255,255,255,0.4) 40%, rgba(255,215,0,0.5) 50%, rgba(0,243,255,0.4) 60%, transparent 80%); background-size: 250% 250%; background-position: 100% 100%; mix-blend-mode: color-dodge; pointer-events: none; transition: background-position 0.8s ease; z-index: 20; opacity: 0; }.tcg-card:hover::after { background-position: 0% 0%; opacity: 1; }.card-content { position: relative; z-index: 2; padding: clamp(25px, 6vw, 40px) clamp(20px, 5vw, 30px); text-align: center; }.card-header-bg { position: absolute; top: 0; left: 0; width: 100%; height: 160px; background: linear-gradient(180deg, VAR_TIER55 0%, transparent 100%); z-index: 1; border-bottom: 1px solid rgba(255,255,255,0.05); }.tcg-mbti { font-family: 'Orbitron', sans-serif !important; font-size: clamp(65px, 12vw, 90px); font-weight: 900; color: #ffffff !important; line-height: 1; letter-spacing: 8px; text-shadow: 0 0 40px VAR_TIER, 0 5px 0px #000; margin: 10px 0; position: relative; z-index: 5; }.tcg-role { font-size: clamp(20px, 5vw, 24px); font-weight: 900; color: #ffd700 !important; margin: 10px 0 25px 0; letter-spacing: 3px; position: relative; z-index: 5; text-shadow: 0 0 20px rgba(255,215,0,0.5); }.tcg-rarity-badge { position: absolute; top: 25px; right: -50px; background: linear-gradient(90deg, #ffd700, #ff8c00); color: #000; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 14px; padding: 6px 55px; transform: rotate(45deg); z-index: 15; letter-spacing: 3px; box-shadow: 0 5px 20px rgba(255,215,0,0.8); border: 1px solid #fff; }.tcg-stats-box { display: flex; justify-content: space-between; gap: 15px; margin-bottom: 25px; position: relative; z-index: 5; }.tcg-stat-item { flex: 1; background: rgba(0,0,0,0.7); border: 1px solid rgba(0,243,255,0.4); border-radius: 10px; padding: 15px 10px; box-shadow: inset 0 0 20px rgba(0,243,255,0.1); backdrop-filter: blur(5px); }.tcg-stat-title { font-size: 11px; color: #94a3b8; font-family: 'Orbitron', monospace; margin-bottom: 8px; letter-spacing: 1px; }.tcg-stat-val { font-size: clamp(22px, 5vw, 26px); color: #00f3ff; font-weight: 900; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 15px rgba(0,243,255,0.8); }</style>"""
        HTML_CARD = CARD_CSS.replace("VAR_TIER", tier_color).replace('\n', '') + f"""<div class="tcg-card-container"><div class="tcg-card"><div class="card-header-bg"></div><div class="card-content"><div class="tcg-rarity-badge">{tier_level}</div><div style="position:relative; z-index:5; display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom:10px;"><div style="font-family:'Orbitron', monospace; font-size:11px; color:#94a3b8; letter-spacing:4px;">LV.{st.session_state.level} AWAKENED</div><div style="font-size:12px; font-weight:bold; color:#fff; text-shadow: 0 0 5px #fff;">{faction_data['element']}</div></div><div style="position:relative; z-index:5; display:flex; justify-content:center; align-items:center; gap:15px; margin-bottom:5px;">{svg_icon}<div style="color:#ffffff; font-family:'Orbitron', monospace; font-size:20px; font-weight:bold; letter-spacing:2px; text-shadow: 0 0 10px rgba(255,255,255,0.5);">{safe_alias_final}</div></div><div class="tcg-mbti">{mbti}</div><div style="position:relative; z-index:5; text-align:center;font-size:12px;color:#94a3b8;margin-bottom:10px; font-family:'Orbitron';">RARITY: <span style="color:{tier_color};font-weight:bold;font-size:16px; text-shadow: 0 0 10px {tier_color};">{data.get('rarity', 'Top 5%')}</span></div><div style="position:relative; z-index:5; display:flex; justify-content:center; gap:10px; margin-bottom:10px;"><span style="background:rgba(255,255,255,0.1); border:1px solid #94a3b8; padding:3px 10px; border-radius:15px; font-size:10px; font-weight:bold;">{faction_data['name']}</span></div><div class="tcg-role">【 {full_title} 】</div><div class="tcg-stats-box"><div class="tcg-stat-item"><div class="tcg-stat-title">COMBAT POWER</div><div class="tcg-stat-val" style="color:#ffd700;">{valuation_str}</div></div><div class="tcg-stat-item"><div class="tcg-stat-title">PERCENTILE</div><div class="tcg-stat-val">TOP {100 - pct_beat_final:.1f}%</div></div></div><div style="position:relative; z-index:5; margin-bottom:20px;">{tags_html_web}</div><div style="position:relative; z-index:5; width:100%;"><div style="font-size:11px; color:#a855f7; margin-bottom:10px; font-family:'Orbitron'; letter-spacing:2px; font-weight:bold; text-align:left; border-bottom:1px dashed #a855f7; padding-bottom:5px;">[ ABILITY MOVES ]</div>{skills_html_web}</div><div style="position:relative; z-index:5; border-top:1px dashed #334155; padding-top:15px; margin-top:20px;"><div style="font-size:10px; color:#10b981; font-weight:bold; margin-bottom:8px;">[ EQUIPPED RELICS ]</div>{relics_html_web}</div></div></div></div>"""
        st.markdown(HTML_CARD, unsafe_allow_html=True)

    with col_top_r:
        # 🎴 三卡构筑阵列 (Triple Deck Builder)
        st.markdown("<div style='background:rgba(10, 15, 25, 0.8); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:clamp(15px, 4vw, 25px); box-shadow:inset 0 0 20px rgba(0,0,0,0.5); margin-bottom:20px;'><h4 style='color:#3b82f6 !important; border-left:4px solid #3b82f6; padding-left:10px; font-weight:900; margin-bottom:15px;'>🎴 三卡小队构筑阵列 (DECK BUILDER)</h4><div style='font-size:13px; color:#94a3b8; margin-bottom:15px;'>选择两名同盟，系统将进行三轨雷达重叠与羁绊共鸣测算：</div>", unsafe_allow_html=True)
        options_list = list(mbti_details.keys())
        format_func = lambda x: f"{x} - {mbti_details[x]['role']}"
        col_s1, col_s2 = st.columns(2)
        with col_s1: pmbti1 = st.selectbox("🎯 同盟 1:", options=options_list, index=options_list.index("ESTJ"), format_func=format_func, label_visibility="collapsed")
        with col_s2: 
            p2_idx = options_list.index(data.get('partner', 'ENTJ')[:4]) if data.get('partner', 'ENTJ')[:4] in options_list else 0
            pmbti2 = st.selectbox("🎯 同盟 2:", options=options_list, index=p2_idx, format_func=format_func, label_visibility="collapsed")
        
        sc1, sd1 = calculate_synergy(mbti, pmbti1); sc2, sd2 = calculate_synergy(mbti, pmbti2)
        total_sc = int((sc1 + sc2) / 2)
        sc_color = "#ffd700" if total_sc >= 90 else "#00f3ff" if total_sc >= 80 else "#a855f7"
        
        # 🛰️ 极客三轨重叠雷达引擎
        v1_E = 85 if 'E' in pmbti1 else 15; v2_E = 85 if 'E' in pmbti2 else 15
        v1_S = 85 if 'S' in pmbti1 else 15; v2_S = 85 if 'S' in pmbti2 else 15
        v1_T = 85 if 'T' in pmbti1 else 15; v2_T = 85 if 'T' in pmbti2 else 15
        v1_J = 85 if 'J' in pmbti1 else 15; v2_J = 85 if 'J' in pmbti2 else 15
        target_values = [(v1_E+v2_E)/2, (v1_S+v2_S)/2, (v1_T+v2_T)/2, (v1_J+v2_J)/2, 100-(v1_E+v2_E)/2, 100-(v1_S+v2_S)/2, 100-(v1_T+v2_T)/2, 100-(v1_J+v2_J)/2]

        fig_syn = go.Figure()
        fig_syn.add_trace(go.Scatterpolar(r=target_values + [target_values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(168, 85, 247, 0.15)', line=dict(color='rgba(168, 85, 247, 0.8)', width=2, dash='dash'), name='小队平均阵型'))
        fig_syn.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.3)', line=dict(color='#00f3ff', width=3), name='本体 (我)'))
        fig_syn.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC", color='#e2e8f0', size=10))), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#fff")), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=25, r=25, t=10, b=20), height=280)
        st.plotly_chart(fig_syn, use_container_width=True, config={'displayModeBar': False}, theme=None)

        if total_sc >= 90:
            HTML_SYN = f"""<style>.link-skill-active {{ background: linear-gradient(90deg, rgba(255,215,0,0.1), rgba(255,215,0,0.4), rgba(255,215,0,0.1)); border: 2px solid #ffd700; box-shadow: 0 0 30px rgba(255,215,0,0.8), inset 0 0 20px rgba(255,215,0,0.5); animation: pulse-link 1s infinite alternate; border-radius: 12px; padding: 25px; text-align: center; margin-top: 10px;}} @keyframes pulse-link {{ 0% {{ transform: scale(1); }} 100% {{ transform: scale(1.02); box-shadow: 0 0 50px rgba(255,215,0,1); }} }}</style><div class="link-skill-active"><div style="font-family:'Orbitron'; color:#ffd700; font-size:12px; font-weight:bold; margin-bottom:10px; letter-spacing: 4px;">⚡ TRIPLE LINK ACTIVATED ⚡</div><div style="font-family:'Orbitron'; font-size:65px; font-weight:900; color:#fff; text-shadow:0 0 35px rgba(255,215,0,0.8); margin-bottom:15px;">{total_sc}%</div><div style="color:#e2e8f0; font-size:15px; font-weight:bold; line-height:1.7;">终极完美小队！弥补了一切短板！</div></div>"""
        else:
            HTML_SYN = f"""<div style="background: rgba(0,0,0,0.5); border: 1px solid {sc_color}66; border-left: 4px solid {sc_color}; padding: 25px; border-radius: 8px; margin-top:10px; text-align:center; box-shadow: 0 0 30px {sc_color}22;"><div style="font-family:'Orbitron'; color:{sc_color}; font-size:12px; font-weight:bold; margin-bottom:10px; letter-spacing: 3px;">[ TEAM RESONANCE ]</div><div style="font-family:'Orbitron'; font-size:55px; font-weight:900; color:#fff; text-shadow:0 0 35px {sc_color}99; margin-bottom:15px;">{total_sc}%</div><div style="color:#e2e8f0; font-size:14px; font-weight:bold; line-height:1.7;">系统评级：该小队在应对复杂项目时存在一定挑战。</div></div>"""
        st.markdown(HTML_SYN.replace('\n', ' '), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # 📱【第二排：全图表深潜区 (单雷达 + 双向对抗槽 + 风险血量 + 3D拓扑)】满血回归！
    # =========================================================================
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    col_mid_l, col_mid_r = st.columns([1.1, 1.3], gap="large")
    
    with col_mid_l:
        st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🕸️ 本机单体战力雷达阵列</h4>", unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', line=dict(color='rgba(0, 243, 255, 0.3)', width=8), hoverinfo='none'))
        fig_radar.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=3), marker=dict(color='#ff003c', size=6, symbol='diamond')))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC", color='#e2e8f0', size=11), linecolor='rgba(255,255,255,0.1)', gridcolor='rgba(255,255,255,0.1)')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=15, r=15, t=20, b=20), height=300)
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        st.markdown("<h4 style='color:#a855f7 !important; border-left:4px solid #a855f7; padding-left:10px; font-weight:900;'>⚔️ 底层核心对抗能量槽</h4>", unsafe_allow_html=True)
        HTML_BARS = f"""<div style="background:rgba(10,15,25,0.9); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:30px 25px; margin-top:10px; margin-bottom: 20px; box-shadow:inset 0 0 20px rgba(0,0,0,0.8);"><div style="font-size:clamp(11px, 2.5vw, 13px); color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;"><span>外联输出 (E) {val_E}%</span><span style="color:#94a3b8;">深潜隐匿 (I) {val_I}%</span></div><div style="background:rgba(255,255,255,0.05); border-radius:4px; height:10px; margin:8px 0 20px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"><div style="position:absolute; top:0; left:0; height:100%; border-radius:4px; width:{val_E}%; background:linear-gradient(90deg, transparent, #00f3ff); box-shadow:0 0 10px #00f3ff;"></div></div><div style="font-size:clamp(11px, 2.5vw, 13px); color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;"><span>颗粒实勘 (S) {val_S}%</span><span style="color:#94a3b8;">宏观前瞻 (N) {val_N}%</span></div><div style="background:rgba(255,255,255,0.05); border-radius:4px; height:10px; margin:8px 0 20px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"><div style="position:absolute; top:0; left:0; height:100%; border-radius:4px; width:{val_S}%; background:linear-gradient(90deg, transparent, #a855f7); box-shadow:0 0 10px #a855f7;"></div></div><div style="font-size:clamp(11px, 2.5vw, 13px); color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;"><span>量化护甲 (T) {val_T}%</span><span style="color:#94a3b8;">生态共情 (F) {val_F}%</span></div><div style="background:rgba(255,255,255,0.05); border-radius:4px; height:10px; margin:8px 0 20px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"><div style="position:absolute; top:0; left:0; height:100%; border-radius:4px; width:{val_T}%; background:linear-gradient(90deg, transparent, #3b82f6); box-shadow:0 0 10px #3b82f6;"></div></div><div style="font-size:clamp(11px, 2.5vw, 13px); color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;"><span>秩序架构 (J) {val_J}%</span><span style="color:#94a3b8;">敏捷演进 (P) {val_P}%</span></div><div style="background:rgba(255,255,255,0.05); border-radius:4px; height:10px; margin:8px 0 0 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"><div style="position:absolute; top:0; left:0; height:100%; border-radius:4px; width:{val_J}%; background:linear-gradient(90deg, transparent, #10b981); box-shadow:0 0 10px #10b981;"></div></div></div>"""
        st.markdown(HTML_BARS.replace('\n', ''), unsafe_allow_html=True)

    with col_mid_r:
        st.markdown("<h4 style='color:#ff003c !important; border-left:4px solid #ff003c; padding-left:10px; font-weight:900;'>🎛️ 风险抵抗生命值 (HP)</h4>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-size:16px; font-weight:bold; color:{r_color}; font-family:Noto Sans SC; margin-top: 5px;'>防线特性：{r_tag}</div>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=risk_score, number={'suffix': " HP", 'font': {'family': 'Orbitron', 'color': r_color, 'size': 40}}, gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155"}, 'bar': {'color': r_color}, 'bgcolor': "rgba(255,255,255,0.05)", 'steps': [{'range': [0, 35], 'color': "rgba(16, 185, 129, 0.15)"}, {'range': [35, 65], 'color': "rgba(255, 215, 0, 0.15)"}, {'range': [65, 100], 'color': "rgba(244, 63, 94, 0.15)"}]}))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#94a3b8"}, height=200, margin=dict(l=30, r=30, t=10, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False}, theme=None)
        
        st.markdown("<h4 style='color:#a855f7 !important; border-left:4px solid #a855f7; padding-left:10px; font-weight:900; margin-top:15px;'>🌌 3D 认知拓扑星图 (可拖拽)</h4>", unsafe_allow_html=True)
        st.plotly_chart(get_3d_topology(val_E, val_I, val_S, val_N, val_T, val_F, mbti, tier_color, h_int), use_container_width=True, config={'displayModeBar': False}, theme=None)

    # =========================================================================
    # 📱【第三排：赛博魔典深潜面板 (Tabs)】新增神级 TCG 专属玩法！
    # =========================================================================
    st.markdown("<h4 style='color:#ffd700 !important; border-left:4px solid #ffd700; padding-left:10px; font-weight:900; margin-top:30px; margin-bottom:15px;'>🗄️ 赛博魔典档案与 TCG 战区 (GRIMOIRE)</h4><div style='text-align:right; font-size:12px; color:#94a3b8; margin-bottom:10px; opacity:0.8;'>👉 手机端可左右滑动切换面板</div>", unsafe_allow_html=True)
    t_boss, t_pvp, t_relic, t_mkt, t_bids, t_evo, t_sol = st.tabs(["🐉 讨伐首领", "⚔️ 竞技对决", "🎰 圣物盲盒", "📉 战力沙盘", "📊 撮合盘口", "🤖 AI 神谕", "💻 铸造合约"])
    
    with t_boss:
        # 🐉 神级特性 1：世界 Boss 讨伐战
        st.markdown("<div style='font-family:\"Orbitron\", sans-serif; font-size:14px; font-weight:bold; color:#ff003c; margin-bottom:10px; border-bottom:1px dashed #ff003c; padding-bottom:8px; margin-top:15px;'>/// WORLD BOSS RAID SIMULATION</div><div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>目标：<b>Lv.99 数据孤岛·利维坦</b><br>机制：利用战力击破护盾！每次攻击有概率触发真实伤害暴击，打怪将掉落代币与海量经验！</div>", unsafe_allow_html=True)
        boss_hp_pct = max(0, st.session_state.boss_hp / 10000000.0 * 100)
        st.markdown(f"""<div style="background:rgba(0,0,0,0.8); border:2px solid #ff003c; padding:20px; border-radius:8px; text-align:center; box-shadow: inset 0 0 30px rgba(255,0,60,0.15);"><div style="font-size:40px; margin-bottom:10px;">👾</div><div style="color:#ff003c; font-weight:900; font-family:'Orbitron'; font-size:20px; margin-bottom:10px;">LV.99 DATA SILO LEVIATHAN</div><div style="background:#334155; height:15px; border-radius:10px; overflow:hidden; margin-bottom:10px;"><div style="background:#ff003c; width:{boss_hp_pct}%; height:100%; transition:width 0.3s;"></div></div><div style="color:#fff; font-family:'Orbitron';">{int(st.session_state.boss_hp):,} / 10,000,000 HP</div></div>""".replace('\n', ''), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.boss_hp > 0:
            st.button("⚔️ 消耗 10 体力发起量子打击 (ATTACK!)", on_click=attack_boss_callback, type="primary", use_container_width=True)
        else:
            st.success("🎉 讨伐成功！数据孤岛已被您彻底击碎！全网算力节点感谢您的贡献！")
            
        if st.session_state.combat_logs:
            st.markdown("<div style='background:#050505; border:1px solid #334155; padding:15px; border-radius:8px; height:180px; overflow-y:auto; font-family:\"Noto Sans SC\", sans-serif; font-size:13px; color:#e2e8f0; margin-top:20px; box-shadow:inset 0 0 15px rgba(0,0,0,0.8); line-height: 1.6;'>" + "<br><br>".join(st.session_state.combat_logs[:15]) + "</div>", unsafe_allow_html=True)

    with t_pvp:
        # ⚔️ 神级特性 2：PVP 竞技场沙盘
        st.markdown("<div style='font-family:\"Orbitron\", sans-serif; font-size:14px; font-weight:bold; color:#f43f5e; margin-bottom:10px; border-bottom:1px dashed #f43f5e; padding-bottom:8px; margin-top:15px;'>/// PVP ARENA SIMULATION</div><div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>选择目标阵营发起算力突击，胜利可掠夺代币并获取大量经验！</div>", unsafe_allow_html=True)
        target_faction = st.selectbox("🎯 锁定目标阵营:", ["【赛博真理会】", "【以太灵网】", "【秩序裁决所】", "【混沌游侠】"], label_visibility="collapsed")
        st.button("⚔️ 消耗 15 体力发起突击 (BATTLE)", on_click=pvp_battle_callback, args=(target_faction,), use_container_width=True)
        if st.session_state.pvp_logs:
            st.markdown("<div style='background:#050505; border:1px solid #334155; padding:15px; border-radius:8px; height:180px; overflow-y:auto; font-family:\"Noto Sans SC\", sans-serif; font-size:13px; color:#e2e8f0; margin-top:20px; box-shadow:inset 0 0 15px rgba(0,0,0,0.8); line-height: 1.6;'>" + "<br>".join(st.session_state.pvp_logs[:20]) + "</div>", unsafe_allow_html=True)

    with t_relic:
        # 🎰 神级特性 3：完全免疫 KeyError 的圣物盲盒系统！
        st.markdown("<div style='font-family:\"Orbitron\", sans-serif; font-size:14px; font-weight:bold; color:#ffd700; margin-bottom:10px; border-bottom:1px dashed #ffd700; padding-bottom:8px; margin-top:15px;'>/// RELIC GACHA SHOP</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>每次抽取消耗 1,000 $SDE。抽取更高级的遗物可大幅飙升您的战力估值！当前持有：<b style='color:#ffd700; font-size:16px; font-family:Orbitron;'>{st.session_state.tokens:,} 🪙</b></div>", unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns([1, 1.2])
        with col_g1:
            st.button("🎲 抽取 1 次 (PULL x1)", on_click=draw_relic_callback, use_container_width=True)
            st.markdown(f"<div style='margin-top:15px; padding:15px; background:rgba(255,215,0,0.1); border:1px solid rgba(255,215,0,0.4); border-radius:8px; font-size:13px; font-weight:bold; text-align:center;'>{st.session_state.gacha_msg}</div>", unsafe_allow_html=True)
        with col_g2:
            st.markdown("<h5 style='color:#00f3ff; margin-bottom:10px;'>🎒 我的武装库 (最多佩戴 3 件):</h5>", unsafe_allow_html=True)
            if not st.session_state.inventory:
                st.markdown("<div style='color:#64748b; font-size:13px; text-align:center; padding:20px; border:1px dashed #334155; border-radius:8px;'>空空如也，快去打怪或竞技场赚取代币抽卡吧！</div>", unsafe_allow_html=True)
            else:
                for r in st.session_state.inventory:
                    is_eq = any(eq['uid'] == r['uid'] for eq in st.session_state.equipped_relics)
                    bg = "rgba(16,185,129,0.2)" if is_eq else "rgba(255,255,255,0.05)"
                    btn_txt = "卸下" if is_eq else "装备"
                    r_color = r['color']
                    
                    r_col1, r_col2 = st.columns([3, 1])
                    with r_col1:
                        st.markdown(f"""<div style="border-left: 4px solid {r_color}; background: {bg}; padding: 10px; margin-bottom: 5px; border-radius: 0 6px 6px 0;"><div style="display:flex; justify-content:space-between; margin-bottom:5px;"><b style="color:{r_color}; font-size:14px;">{r['name']}</b><span style="color:#10b981; font-weight:bold; font-family:Orbitron; font-size:12px;">+{r['cp']:,} CP</span></div><div style="color:#94a3b8; font-size:11px;">{r['desc']}</div></div>""".replace('\n', ''), unsafe_allow_html=True)
                    with r_col2:
                        st.button(btn_txt, key=f"eq_{r['uid']}", on_click=equip_relic_callback, args=(r['uid'],), use_container_width=True)

    with t_mkt:
        st.markdown(f"<div style='font-family:\"Orbitron\", sans-serif; font-size:14px; font-weight:bold; color:#ffd700; margin-bottom:10px; border-bottom:1px dashed #ffd700; padding-bottom:8px; margin-top:15px;'>/// 30-DAY COMBAT SIMULATION</div><div style='font-size:14px; color:#e2e8f0; margin-bottom:10px;'>基于高斯随机游走与标准差推演的战力走势：<br><span style='color:#ffd700; font-weight:bold; font-size:15px;'>【 {data.get('market_style', '')} 】</span></div>", unsafe_allow_html=True)
        std_dev = np.std(roi_arr)
        upper_band = [val + std_dev * 1.5 for val in roi_arr]; lower_band = [val - std_dev * 1.5 for val in roi_arr]
        fig_roi = go.Figure()
        lc = "#10b981" if roi_arr[-1] >= 100 else "#ff003c"
        fig_roi.add_trace(go.Scatter(x=d_arr + d_arr[::-1], y=upper_band + lower_band[::-1], fill='toself', fillcolor='rgba(255,255,255,0.05)', line=dict(color='rgba(255,255,255,0)'), hoverinfo="skip", showlegend=False))
        fig_roi.add_trace(go.Scatter(x=d_arr, y=roi_arr, mode='lines', line=dict(color=lc, width=3), name="Combat Power"))
        fig_roi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='Power Level'), showlegend=False)
        st.plotly_chart(fig_roi, use_container_width=True, config={'displayModeBar': False}, theme=None)

    with t_bids:
        # 💎 完美修复 NameError 的深度订单墙 (完全分离 CSS 和 F-String 括号)
        st.markdown("<div style='font-family:\"Orbitron\", sans-serif; font-size:14px; font-weight:bold; color:#3b82f6; margin-bottom:10px; border-bottom:1px dashed #3b82f6; padding-bottom:8px; margin-top:15px;'>/// LIVE MARKET DEPTH & BIDS [SDE/USDT]</div><div style='font-size:12px; color:#94a3b8; margin-bottom:15px;'>系统正在全网广播您的算力凭证，以下为各大机构实时模拟撮合竞价：</div>", unsafe_allow_html=True)
        HTML_BIDS = f"""<div style="background: #050505; border: 1px solid #334155; border-radius: 8px; padding: 20px; font-family: 'Fira Code', monospace; font-size: 12px; color: #94a3b8; box-shadow: inset 0 0 20px rgba(0,0,0,0.8);">{get_market_depth_html(h_int)}<div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #334155; padding-bottom: 12px; margin-bottom: 15px; color: #e2e8f0; font-weight: bold; font-size: 11px; letter-spacing: 1px;"><span style="width:40%;">[INSTITUTION]</span><span style="width:30%; text-align:center;">[BID_SIZE]</span><span style="width:30%; text-align:right;">[PREMIUM]</span></div>{bids_html}<div style="text-align: center; margin-top: 15px; font-size: 10px; color: #3b82f6; animation: blink 1.5s infinite;">● WAITING FOR NEW BIDS...</div></div>"""
        st.markdown(HTML_BIDS.replace('\n', ''), unsafe_allow_html=True)

    with t_evo:
        ORACLE_CSS = """<style>.oracle-box { background: #050505; border: 1px solid #334155; border-left: 4px solid #a855f7; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: inset 0 0 20px rgba(0,0,0,0.8); font-family: 'Fira Code', monospace; font-size: 12px; }.oracle-hdr { color: #a855f7; font-size: 11px; margin-bottom: 15px; border-bottom: 1px dashed #334155; padding-bottom: 8px; letter-spacing: 1px; font-weight: bold; }.oracle-line { overflow: hidden; white-space: nowrap; width: 0; display: block; margin-bottom: 8px; color: #10b981; animation: o-type 0.8s steps(40, end) forwards; border-right: 2px solid #10b981; }.oracle-line:nth-child(2) { animation-delay: 0.2s; }.oracle-line:nth-child(3) { animation-delay: 1.2s; }.oracle-line:nth-child(4) { animation-delay: 2.2s; }.oracle-line:nth-child(5) { animation-delay: 3.2s; color: #e2e8f0; border-right: none;}.oracle-line-fade { display: block; margin-top: 15px; color: #94a3b8; opacity: 0; animation: o-fade 1s 4.2s forwards; line-height: 1.8; }@keyframes o-type { 99% { border-color: #10b981; } 100% { width: 100%; border-color: transparent; } }@keyframes o-fade { to { opacity: 1; } }</style>"""
        HTML_ORACLE = ORACLE_CSS.replace('\n', '') + f"""<div class="oracle-box"><div class="oracle-hdr">[AI_ORACLE_V10] QUANTUM DIAGNOSTIC ACTIVE...</div><span class="oracle-line">> Extracting Node [ {safe_alias_final} ] Weights... [OK]</span><span class="oracle-line">> Bypassing SDE Firewall... [SUCCESS]</span><span class="oracle-line">> Decrypting Matrix Topology... [OK]</span><span class="oracle-line">> Node Classified As: <span style="color:#ffd700; font-weight:bold;">{mbti}</span></span><span class="oracle-line-fade">> ULTIMATE EVOLUTION PREDICTION: <br><span style="color:#00f3ff; font-size:14px; font-weight:bold;">{data.get('ultimate_evolution', '')}</span></span></div>"""
        st.markdown(HTML_ORACLE, unsafe_allow_html=True)
        with st.expander("⚠️ 绝密防线：SDE 史诗级黑天鹅宕机推演"):
            HTML_SWAN = f"""<div style="padding: 5px 10px; font-size: 14px; color: #cbd5e1; line-height: 1.7;"><div style="color: #ff003c; font-weight: 900; margin-bottom: 5px; font-size:15px; text-shadow: 0 0 5px #ff003c;">[ 致命崩溃盲点 ]</div><div style="margin-bottom: 15px;">{data.get('black_swan', '')}</div><div style="color: #10b981; font-weight: 900; margin-bottom: 5px; font-size:15px; text-shadow: 0 0 5px #10b981;">[ 官方热修复补丁 ]</div><div>{data.get('patch', '')}</div></div>"""
            st.markdown(HTML_SWAN.replace('\n', ''), unsafe_allow_html=True)

    with t_sol:
        st.markdown("<div style='font-family:\"Orbitron\", sans-serif; font-size:14px; font-weight:bold; color:#10b981; margin-bottom:10px; border-bottom:1px dashed #10b981; padding-bottom:8px; margin-top:15px;'>/// SOLIDITY SMART CONTRACT MINT LOG</div><div style='font-size:12px; color:#94a3b8; margin-bottom:10px;'>系统已自动为您生成专属的以太坊 ERC721 确权智能合约源码。</div>", unsafe_allow_html=True)
        code_block = f"// SPDX-License-Identifier: MIT\npragma solidity ^0.8.20;\nimport \"@sde-network/contracts/token/ERC721.sol\";\n\ncontract SDE_Card_Registry_V10 is ERC721 {{\n    struct CardStats {{\n        string matrix_id;\n        uint256 combat_power;\n        uint8 decisiveness;\n        string rarity_tier;\n    }}\n    \n    mapping(uint256 => CardStats) public deck;\n    \n    constructor() ERC721(\"SDE_TCG_V10\", \"SDETCG\") {{}}\n\n    // MINTED_TO: {safe_alias_final}\n    // BLOCK_HEIGHT: {block_height}\n    // CONTRACT_ADDR: {contract_addr}\n    \n    function executeMint() public {{\n        uint256 tokenId = {token_id};\n        deck[tokenId] = CardStats(\"{mbti}\", {final_cp}, {decisiveness}, \"{tier_level}\");\n        _mint(msg.sender, tokenId);\n    }}\n}}"
        safe_code = html.escape(code_block).replace('\n', '<br>')
        HTML_SOLIDITY = f"""<div style="background: #050505; border-radius: 8px; border: 1px solid #334155; border-left: 4px solid #10b981; width: 100%; box-sizing: border-box; box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(0,243,255,0.05); margin-top: 15px; margin-bottom: 20px; overflow: hidden;"><div style="background: #0f172a; padding: 10px 15px; display: flex; align-items: center; border-bottom: 1px solid #334155;"><div style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f56; margin-right: 8px;"></div><div style="width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e; margin-right: 8px;"></div><div style="width: 12px; height: 12px; border-radius: 50%; background: #27c93f; margin-right: 15px;"></div><div style="color: #94a3b8; font-size: 11px; font-family: 'Fira Code', monospace; letter-spacing: 1px;">SDE_Smart_Contract.sol</div></div><div style="padding: 15px; overflow-x: hidden;"><div style="margin: 0; font-family: 'Fira Code', monospace; font-size: 12px; color: #10b981 !important; line-height: 1.6; background: transparent; border: none; user-select: all; -webkit-user-select: all; cursor: text; word-break: break-all;">{safe_code}</div></div></div>"""
        st.markdown(HTML_SOLIDITY.replace('\n', ''), unsafe_allow_html=True)
        st.markdown("<div style='font-family:\"Orbitron\", sans-serif; font-size:14px; font-weight:bold; color:#f43f5e; margin-bottom:15px; border-bottom:1px dashed #f43f5e; padding-bottom:8px; margin-top:20px;'>/// TOP SECRET BOUNTIES (悬赏任务)</div>", unsafe_allow_html=True)
        tasks_html = "".join([f"<div style='border-left: 4px solid #f43f5e; padding-left: 15px; margin-bottom: 12px; background: rgba(244,63,94,0.05); padding-top: 10px; padding-bottom: 10px; border-radius: 0 4px 4px 0;'><span style='color:#e2e8f0; font-size:14px; font-weight:bold;'>{t}</span></div>" for t in data.get('tasks', [])])
        st.markdown(f"<div style='margin-bottom: 10px;'>{tasks_html}</div>".replace('\n', ''), unsafe_allow_html=True)


    # =========================================================================
    # 💠 4. 【沉底提取中心】终极可见即所得防死锁海报！
    # =========================================================================
    st.markdown("<h4 style='color:#00f3ff !important; border-left:5px solid #00f3ff; padding-left:12px; font-weight:900; margin-top:40px; margin-bottom:20px;'>💠 评级卡砖提取终端 (MINT)</h4>", unsafe_allow_html=True)
    t_img, t_txt, t_json = st.tabs(["📸 PSA 全息防伪海报 (防白屏)", "📝 纯文本通讯协议 (一键复制)", "📥 极客 JSON 底包档案"])

    with t_img:
        # 🚨 颠覆式更新：不再隐藏等渲染，直接排版原生 HTML！用户可以直接用手机系统截图！百分百防死锁！
        st.markdown("<div style='font-size:13px; color:#10b981; margin-bottom:15px; line-height:1.7;'>已为您直接展示【可见即所得】高清卡砖。您可以点击下方按钮生成图片，<b style='color:#ffd700; font-size:15px;'>如果无反应，请直接使用手机系统截屏保存！</b>绝对不再死锁！</div>", unsafe_allow_html=True)
        
        tags_html_poster = "".join([f"<span style='background:rgba(255,215,0,0.1); border:1px solid rgba(255,215,0,0.5); padding:4px 8px; border-radius:4px; font-size:11px; color:#ffd700; font-weight:bold; margin:3px; display:inline-block;'>{t}</span>" for t in data.get('tags', [])])
        skills_html_poster = "".join([f"<div style='background:rgba(168,85,247,0.1); border:1px solid rgba(168,85,247,0.6); border-left:3px solid #a855f7; padding:6px 10px; border-radius:4px; font-size:11px; color:#e9d5ff; font-weight:bold; margin-bottom:5px; text-align:left;'>{s}</div>" for s in data.get('skills', [])])
        
        random.seed(h_int)
        gradient_stops = []
        for p in range(0, 100, int(random.uniform(2, 6))): 
            gradient_stops.append(f"rgba(0,243,255,0.7) {p}%, rgba(0,243,255,0.7) {p+1}%, transparent {p+1}%, transparent {p+2}%")
        barcode_css = "linear-gradient(90deg, " + ", ".join(gradient_stops) + ")"

        POSTER_HTML = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
body {{ margin: 0; padding: 10px 0; background: transparent !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #fff; overflow-x: hidden; text-align: center; }}
.capture-box {{ width: 320px; background-color: #010308; padding: 15px; border-radius: 12px; border: 3px solid #cbd5e1; box-shadow: 0 0 25px rgba(0, 243, 255, 0.4); position: relative; overflow: hidden; margin: 0 auto; text-align: left; box-sizing: border-box; }}
.cyber-grid {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(0deg, rgba(0,243,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.05) 1px, transparent 1px); background-size: 25px 25px; z-index: 0; pointer-events:none;}}
.psa-header {{ background: #ef4444; padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #b91c1c; margin-bottom: 15px; position: relative; z-index: 2; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);}}
.psa-grade {{ font-size: 28px; font-weight: 900; color: #fff; line-height: 1; font-family: Impact, sans-serif; }}
.psa-desc {{ font-size: 10px; color: #fecaca; text-align: right; font-weight: bold; line-height: 1.2; text-transform: uppercase; }}
.inner-card {{ background: rgba(10,15,30,0.95); border: 2px solid rgba(255,215,0,0.4); border-radius: 8px; padding: 20px 15px; position: relative; z-index: 2; overflow: hidden;}}
.hd {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom: 10px; margin-bottom: 15px; }}
.nm {{ text-align: center; font-size: 18px; font-weight: 900; letter-spacing: 2px; margin-bottom: 5px; color: #fff; text-transform: uppercase; }}
.mb {{ font-size: 52px; font-weight: 900; color: #ffd700; line-height: 1; text-align: center; text-shadow: 0 0 30px rgba(255,215,0,0.6); margin-bottom: 5px; letter-spacing: 4px; font-family: Impact, sans-serif; }}
.rl {{ text-align: center; font-size: 13px; font-weight: 900; color: #00f3ff; margin-bottom: 15px; letter-spacing: 2px; }}
.vb {{ display:flex; justify-content:space-between; text-align:center; background:rgba(0,0,0,0.8); border:1px solid rgba(255,215,0,0.4); padding:10px; border-radius:8px; margin-bottom: 15px; gap: 5px; }}
.ft {{ text-align: center; color: #64748b; font-size: 8px; padding-top: 10px; line-height: 1.6; font-family: monospace; position: relative; z-index: 2; margin-top: 10px;}}
.stat-row {{ display: flex; align-items: center; margin-bottom: 8px; font-size: 10px; font-weight: bold; justify-content: space-between; }}
.sbc {{ background: rgba(255,255,255,0.05); border-radius: 3px; height: 5px; width: 130px; position: relative; overflow: hidden; margin: 0 6px; }}
.sbf {{ position: absolute; left: 0; top: 0; height: 100%; }}
.action-btn {{ background: linear-gradient(90deg, #10b981, #059669); color: #fff; border: none; padding: 15px 30px; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; box-shadow: 0 5px 15px rgba(16,185,129,0.4); margin-top: 20px; text-transform: uppercase; width: 320px; transition: all 0.2s ease;}} 
#result-img {{ display: none; width: 320px; border-radius: 12px; margin: 0 auto; box-shadow: 0 0 30px rgba(16,185,129,0.6); margin-top: 20px; }}
.success-msg {{ display: none; color: #10b981; font-weight: bold; margin-top: 15px; font-size: 14px; background: rgba(16,185,129,0.1); padding: 10px; border-radius: 6px; border: 1px solid #10b981; width: 320px; margin: 15px auto 0 auto; box-sizing: border-box; }}
</style>
</head>
<body>
<div id="html-card">
    <div class="capture-box" id="capture-target">
        <div class="cyber-grid"></div>
        <div class="psa-header">
            <div>
                <div style="font-size:12px; font-weight:900; color:#fff; letter-spacing:1px; margin-bottom:2px;">SDE AUTHENTICATED</div>
                <div style="font-size:9px; color:#fca5a5; font-family:monospace;">CERT: {hash_code[:10]}</div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <div class="psa-desc">GEM<br>MINT</div>
                <div class="psa-grade">10</div>
            </div>
        </div>
        <div class="inner-card">
            <div style="position: absolute; top: 15px; right: -35px; background: {tier_color}; color: #000; font-weight: 900; font-size: 10px; padding: 3px 35px; transform: rotate(45deg); z-index: 10; letter-spacing: 2px; box-shadow: 0 0 15px {tier_color}88;">{tier_level}</div>
            <div class="hd">
                <div style="font-size:13px;font-weight:900; color:#00f3ff; letter-spacing:1px;">GENESIS TCG</div>
                <div style="font-size:9px;color:#94a3b8; font-weight:bold;">2026 EDITION</div>
            </div>
            <div style="font-size:9px;color:#94a3b8;text-align:center;margin-bottom:5px;">NODE IDENTIFIER</div>
            <div class="nm">{full_title}</div>
            <div class="mb">{mbti}</div>
            <div style="text-align:center;font-size:10px;color:#94a3b8;margin-bottom:15px; font-weight:bold;">RARITY: <span style="color:{tier_color};font-size:12px;">{data.get('rarity', 'Top 5%')}</span></div>
            <div class="rl">【 {role_name} 】</div>
            <div class="vb">
                <div style="flex:1;"><div style="font-size:9px;color:#94a3b8;margin-bottom:5px;">COMBAT POWER</div><div style="font-size:16px;color:#ffd700;font-weight:900;">{final_cp:,}</div></div>
                <div style="border-left:1px dashed rgba(255,255,255,0.3);"></div>
                <div style="flex:1;"><div style="font-size:9px;color:#94a3b8;margin-bottom:5px;">PERCENTILE</div><div style="font-size:16px;color:#00f3ff;font-weight:900;">TOP {100-pct_beat_final:.1f}%</div></div>
            </div>
            <div style="text-align:center; margin-bottom:12px;"><div style="font-size:10px; color:#a855f7; margin-bottom:6px; font-weight:bold;">[ ABILITY MOVES ]</div>{skills_html_poster}</div>
            <div style="text-align:center; margin-bottom:15px;">{tags_html_poster}</div>
            <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 12px 10px; margin-bottom: 10px;">
                <div style="font-size: 8px; color: #00f3ff; text-align: center; margin-bottom: 8px; font-family: monospace;">/// BASE STATS ///</div>
                <div class="stat-row"><span style="color:#e2e8f0; width:35px;">输出</span><div class="sbc"><div class="sbf" style="width:{val_E}%; background:#00f3ff;"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">隐匿</span></div>
                <div class="stat-row"><span style="color:#e2e8f0; width:35px;">精准</span><div class="sbc"><div class="sbf" style="width:{val_S}%; background:#a855f7;"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">视界</span></div>
                <div class="stat-row"><span style="color:#e2e8f0; width:35px;">护甲</span><div class="sbc"><div class="sbf" style="width:{val_T}%; background:#3b82f6;"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">光环</span></div>
                <div class="stat-row" style="margin-bottom:0;"><span style="color:#e2e8f0; width:35px;">秩序</span><div class="sbc"><div class="sbf" style="width:{val_J}%; background:#10b981;"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">敏捷</span></div>
            </div>
        </div>
        <div class="ft">
            <div style="width: 90%; height: 20px; margin: 0 auto 8px auto; background: {barcode_css};"></div>
            <div style="margin-bottom:2px;font-weight:bold;">SDE CYBER-NODE TCG V10.0</div>
            <div style="color:#475569;">© {COPYRIGHT} | ID: #{token_id}</div>
        </div>
    </div>
    <button class="action-btn" id="btn-render" onclick="execRender()">📸 点击生成纯净图片版</button>
</div>
<img id="result-img" alt="SDE Matrix Slab" title="长按保存或分享" />
<div id="success-msg" class="success-msg">✅ <b>图片压制成功！</b><br>👆 手机端请长按上方图片保存发圈。</div>
<script>
function execRender() {{
    var btn = document.getElementById('btn-render');
    btn.innerHTML = "⏳ 正在压制，请稍候...";
    btn.style.opacity = "0.7";
    if(typeof html2canvas === 'undefined') {{
        btn.innerHTML = "❌ 环境不支持，请直接手机系统截屏";
        btn.style.opacity = "1";
        return;
    }}
    setTimeout(function() {{
        html2canvas(document.getElementById('capture-target'), {{ scale: 2, backgroundColor: '#010308', useCORS: true, logging: false }}).then(function(canvas) {{
            document.getElementById('result-img').src = canvas.toDataURL('image/png');
            document.getElementById('result-img').style.display = 'block';
            document.getElementById('html-card').style.display = 'none';
            document.getElementById('success-msg').style.display = 'block';
        }}).catch(function(e) {{
            btn.innerHTML = "❌ 生成失败，请直接手机截屏";
            btn.style.opacity = "1";
        }});
    }}, 200);
}}
</script>
</body>
</html>
"""
        st.components.v1.html(POSTER_HTML.replace('\n', ''), height=950)

    with t_txt:
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:10px; margin-top:10px;'>👇 长按下方文本框，可一键全选并复制纯文字名片：</div>", unsafe_allow_html=True)
        relics_text = "、".join([r['name'] for r in st.session_state.equipped_relics]) if st.session_state.equipped_relics else "无"
        share_card = f"""【SDE 职场元宇宙 · TCG 创世卡牌】
=================================
👤 节点代号：{safe_alias_final}
💎 战力估值：{final_cp:,} CP
🧬 核心架构：{mbti} ({role_name})
👑 卡牌稀有度：{tier_level} ({data.get('rarity', 'Top 5%')})
⚡️ 算力击败：全球 TOP {100 - pct_beat_final:.1f}%
⚔️ 专属遗物：{relics_text}
🚀 终极演进：{data.get('ultimate_evolution', '')}
🎯 核心指令：{data.get('tasks', ['无'])[0]}
⚖️ 风控偏好：{r_tag}
=================================
🌐 2026 寻找你的羁绊连携节点！
🔗 [Token ID: #{token_id} | Hash: 0x{hash_code[:8]}]"""
        
        # 🚨 终极液态排版：手机端自动换行，一键可全选！
        safe_share = html.escape(share_card).replace('\n', '<br>')
        HTML_TXT = f"""<div style="background-color: #050505 !important; border: 1px solid #334155 !important; border-left: 4px solid #00f3ff !important; border-radius: 8px; padding: 20px; overflow-x: hidden; margin-bottom: 20px; margin-top: 10px; box-shadow: inset 0 0 20px rgba(0,0,0,0.8); user-select: all; -webkit-user-select: all;"><div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 13px; color: #e2e8f0 !important; line-height: 1.7; word-break: break-all; word-wrap: break-word; cursor: text;">{safe_share}</div></div>"""
        st.markdown(HTML_TXT.replace('\n', ''), unsafe_allow_html=True)

    with t_json:
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:15px; margin-top:10px;'>💾 高管/极客视角：导出您的原生底层 JSON 结构树归档：</div>", unsafe_allow_html=True)
        export_data = {
            "version": VERSION,
            "node_alias": safe_alias_final, 
            "card_title": full_title,
            "matrix_id": mbti, 
            "faction": faction_data,
            "role": role_name, 
            "tier": tier_level, 
            "global_rarity": data.get('rarity', ''),
            "soulbound_token": {
                "contract": contract_addr,
                "token_id": token_id,
                "hash_signature": hash_code,
                "block_height": block_height
            },
            "combat_power_cp": final_cp, 
            "global_percentile": pct_beat_final,
            "metrics": {"E_I": val_E, "S_N": val_S, "T_F": val_T, "J_P": val_J},
            "unlocked_skills": data.get('skills', []),
            "equipped_relics": st.session_state.equipped_relics,
            "relics_inventory": st.session_state.inventory,
            "assigned_tasks": data.get('tasks', []), 
            "fatal_vulnerability": data.get('black_swan', ''), 
            "patch_protocol": data.get('patch', ''),
            "ultimate_evolution": data.get('ultimate_evolution', ''),
            "timestamp": current_time_str
        }
        json_str = json.dumps(export_data, indent=4, ensure_ascii=False)
        st.download_button(label="📥 立即下载节点加密档案 (.JSON)", data=json_str, file_name=f"SDE_TCG_{safe_alias_final}.json", mime="application/json", use_container_width=True)

    def reset_system():
        st.session_state.clear()

    with center_container():
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("☢️ 销毁当前节点痕迹并重启 (WIPE_AND_REBOOT)", type="primary", use_container_width=True):
            reset_system()
            st.rerun()

# =========================================================================
# 🛑 [ SDE TCG 07 ] 赛博呼吸专属版权区
# =========================================================================
HTML_FOOTER = f"""<div style="text-align:center; margin-top:80px; margin-bottom:40px; position:relative; z-index:10;"><div style="color:#00f3ff !important; font-family:'Orbitron', monospace; font-size:10px; opacity:0.3; letter-spacing:6px; margin-bottom:8px;">POWERED BY SDE DATA ELEMENT KERNEL</div><div style="color:#00f3ff !important; font-family:'Orbitron', monospace; font-size:10px; opacity:0.2; letter-spacing:3px; margin-bottom:30px;">SYSTEM VERSION: {VERSION}</div><div class="copyright-niliu">© 2026 版权归属 · <b style="font-family:'Orbitron', sans-serif; letter-spacing: 4px;">{COPYRIGHT}</b></div></div>"""
st.markdown(HTML_FOOTER.replace('\n', ''), unsafe_allow_html=True)
# ================================= EOF ==================================
