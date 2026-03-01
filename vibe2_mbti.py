import streamlit as st
import streamlit.components.v1 as components
import random
import time
import math
import hashlib
import html
import plotly.graph_objects as go

# --- 1. 页面与全局配置 (沉浸式全屏化) ---
st.set_page_config(
    page_title="SDE 核心人才图谱 | 全息引擎",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 赛博科技级 UI 引擎 (沉浸式去白边，屏蔽默认UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Orbitron:wght@400;500;700;900&display=swap');

    /* 🚨 隐藏 Streamlit 默认的页眉页脚和菜单，实现真全屏 App 体验 */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem; max-width: 650px; }

    /* 终极锁死全局深网背景 */
    html, body, [class*="css"], .stApp { 
        background-color: #030712 !important; 
        font-family: 'Noto Sans SC', sans-serif !important;
        color: #f8fafc !important;
    }
    
    /* 全局 CRT 扫描线与科技网格背景 */
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
        background-size: 100% 3px, 3px 100%;
        z-index: 99999; pointer-events: none; opacity: 0.5;
    }
    [data-testid="stAppViewContainer"] {
        background-image: 
            radial-gradient(circle at 50% 0%, #0f172a 0%, #030712 80%),
            linear-gradient(0deg, rgba(0,243,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px) !important;
        background-size: 100% 100%, 40px 40px, 40px 40px !important;
    }
    
    .stMarkdown, p, span, h2, h3, h4, li, div { color: #f8fafc !important; }
    
    /* 进度条定制 */
    [data-testid="stProgress"] > div > div > div { background-color: #00f3ff !important; box-shadow: 0 0 15px rgba(0,243,255,0.8); }
    
    /* Glitch 故障风主标题 */
    .hero-title { 
        font-size: 38px !important;
        font-weight: 900 !important; text-align: center; 
        color: #ffffff !important; letter-spacing: 4px; margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(0,243,255,0.7), 0 0 40px rgba(0,243,255,0.3);
        position: relative; display: inline-block;
    }
    .hero-title::before, .hero-title::after { content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: transparent; }
    .hero-title::before { left: 2px; text-shadow: -2px 0 #f43f5e; animation: glitch-anim-1 2s infinite linear alternate-reverse; }
    .hero-title::after { left: -2px; text-shadow: 2px 0 #00f3ff; animation: glitch-anim-2 3s infinite linear alternate-reverse; }
    
    @keyframes glitch-anim-1 { 0% { clip-path: inset(20% 0 80% 0); } 20% { clip-path: inset(60% 0 10% 0); } 40% { clip-path: inset(40% 0 50% 0); } 60% { clip-path: inset(80% 0 5% 0); } 80% { clip-path: inset(10% 0 70% 0); } 100% { clip-path: inset(30% 0 20% 0); } }
    @keyframes glitch-anim-2 { 0% { clip-path: inset(10% 0 60% 0); } 20% { clip-path: inset(30% 0 20% 0); } 40% { clip-path: inset(70% 0 10% 0); } 60% { clip-path: inset(20% 0 50% 0); } 80% { clip-path: inset(90% 0 5% 0); } 100% { clip-path: inset(50% 0 30% 0); } }
    
    .hero-subtitle { text-align: center; color: #00f3ff !important; font-size: 13px; letter-spacing: 5px; opacity: 0.9; margin-bottom: 30px; font-family: 'Orbitron', sans-serif !important; font-weight: 700; }
    
    /* 终端缓慢展开自检特效 */
    .terminal-container { background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: 25px; border-radius: 8px; font-family: 'Orbitron', monospace; font-size: 13px; color: #e2e8f0; box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px; }
    .term-line { opacity: 0; margin-bottom: 5px; }
    .term-line:nth-child(1) { animation: scanFade 0.2s 0.2s forwards; }
    .term-line:nth-child(2) { animation: scanFade 0.2s 1.0s forwards; }
    .term-line:nth-child(3) { animation: scanFade 0.2s 1.8s forwards; }
    .term-line-main { opacity: 0; animation: scanFade 0.5s 2.6s forwards; }
    @keyframes scanFade { 0% { opacity: 0; transform: translateX(-10px); filter: blur(2px); } 100% { opacity: 1; transform: translateX(0); filter: blur(0); } }
    .cursor-blink { display: inline-block; width: 8px; height: 16px; background: #00f3ff; animation: blink 1s step-end infinite; vertical-align: middle; margin-left: 5px; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

    /* 输入框与按钮样式 */
    div[data-testid="stTextInput"] > div > div > input { background-color: rgba(2, 6, 23, 0.9) !important; color: #00f3ff !important; font-family: 'Orbitron', monospace !important; border: 1px solid rgba(0,243,255,0.5) !important; border-radius: 6px !important; text-align: center; font-size: 16px !important; font-weight: bold !important; letter-spacing: 2px; box-shadow: inset 0 0 15px rgba(0,243,255,0.1) !important; transition: all 0.3s ease; }
    div[data-testid="stTextInput"] > div > div > input:focus { border-color: #ffd700 !important; box-shadow: 0 0 20px rgba(255,215,0,0.3), inset 0 0 15px rgba(255,215,0,0.1) !important; }

    div.stButton > button { background: #0f172a !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; border-left: 4px solid rgba(0, 243, 255, 0.6) !important; border-radius: 6px !important; min-height: 56px !important; width: 100% !important; padding: 10px 15px !important; text-align: left !important; box-shadow: 0 4px 10px rgba(0,0,0,0.4) !important; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important; }
    div.stButton > button p { color: #ffffff !important; font-size: 15px !important; line-height: 1.5 !important; font-weight: 500 !important; }
    div.stButton > button:hover { background: rgba(0, 243, 255, 0.15) !important; border-color: #00f3ff !important; border-left: 4px solid #00f3ff !important; box-shadow: 0 0 15px rgba(0,243,255,0.3) !important; transform: translateX(3px) !important; }
    div.stButton > button:active { transform: scale(0.98) !important; }
    div.stButton > button[data-testid="baseButton-primary"] { background: linear-gradient(90deg, #00f3ff, #0088ff) !important; border-left: none !important; text-align: center !important; }
    div.stButton > button[data-testid="baseButton-primary"] p { color: #030712 !important; font-weight: 900 !important; font-size: 16px !important; letter-spacing: 1px !important; }
    div.stButton > button[data-testid="baseButton-primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 0 30px rgba(0,243,255,0.6) !important; }
    
    .cli-box { background: #000000; border: 1px solid #334155; border-left: 4px solid #00f3ff; padding: 20px; border-radius: 6px; font-family: 'Orbitron', monospace; font-size: 13px; color: #4ade80; box-shadow: inset 0 0 20px rgba(0,243,255,0.1); margin-top: 50px; text-transform: uppercase; }

    /* 专属 Tabs 标签页 UI 穿透 */
    [data-testid="stTabs"] button { color: #94a3b8 !important; font-family: 'Noto Sans SC', sans-serif !important; font-weight: bold !important; font-size: 15px !important; padding-bottom: 10px !important; }
    [data-testid="stTabs"] button[aria-selected="true"] { color: #00f3ff !important; border-bottom-color: #00f3ff !important; text-shadow: 0 0 10px rgba(0,243,255,0.5); }
    [data-testid="stTabs"] button:hover { color: #ffffff !important; }

    /* 代码块样式修复 */
    [data-testid="stCodeBlock"] { border-radius: 8px !important; margin-top: 10px; }
    [data-testid="stCodeBlock"] > div { background-color: rgba(5, 10, 21, 0.95) !important; border: 1px solid rgba(0, 243, 255, 0.4) !important; border-radius: 8px !important; box-shadow: inset 0 0 20px rgba(0, 243, 255, 0.1) !important; }
    [data-testid="stCodeBlock"] pre, [data-testid="stCodeBlock"] code, [data-testid="stCodeBlock"] span { background-color: transparent !important; color: #e2e8f0 !important; font-family: 'Noto Sans SC', monospace !important; font-size: 13px !important; line-height: 1.6 !important; white-space: pre-wrap !important; text-shadow: none !important; }
    [data-testid="stCodeBlock"] button { background-color: rgba(2, 6, 23, 0.9) !important; border: 1px solid rgba(0, 243, 255, 0.4) !important; border-radius: 4px !important; opacity: 1 !important; transition: all 0.3s ease !important; }
    [data-testid="stCodeBlock"] button:hover { background-color: rgba(0, 243, 255, 0.2) !important; border-color: #00f3ff !important; transform: scale(1.05) !important; }
    [data-testid="stCodeBlock"] button svg { fill: #00f3ff !important; stroke: #00f3ff !important; }

    /* 结算烟花 */
    .firework-center { position: fixed; top: 50%; left: 50%; z-index: 99998; pointer-events: none; font-weight: 900; font-family: 'Orbitron', sans-serif; color: #00f3ff; text-shadow: 0 0 20px #00f3ff, 0 0 30px #ffffff; animation: supernova 1.8s cubic-bezier(0.1, 0.9, 0.2, 1) forwards; will-change: transform, opacity;}
    @keyframes supernova { 0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; } 100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; filter: blur(2px);} }
</style>
""", unsafe_allow_html=True)

def trigger_supernova():
    html_str = ""
    symbols = ["DATA", "SDE", "NODE", "HASH", "ASSET", "SYNC"]
    for _ in range(35): 
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(250, 900)
        tx, ty = distance * math.cos(angle), distance * math.sin(angle)
        scale = random.uniform(1.0, 3.0)
        rot = random.randint(-360, 360)
        delay = random.uniform(0, 0.15)
        text = random.choice(symbols)
        html_str += f'<div class="firework-center" style="--tx:{tx}px; --ty:{ty}px; --s:{scale}; --rot:{rot}deg; animation-delay:{delay}s; font-size:{random.randint(12, 22)}px;">{text}</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 深度定制的 SDE 业务语境题库 ---
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
    {"q": "相比于畅想 2026 年国家级数据大市场的宏伟蓝图，我更关心下个季度的结算系统并发量和撮合效率能否提升。", "dim": "S"},
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

# --- 4. 规范与科技感并存的身份数据库 ---
mbti_details = {
    "INTJ": {"role": "首席数据架构师", "desc": "数据要素底座的“造物主”，致力于为错综复杂的数字经济构建严密的底层制度与逻辑规则。", "tags": ["顶层设计", "逻辑闭环", "制度自信"], "partner": "ENTJ (高效执行统筹) / INTP (极客算法节点)", "advice": "在构建宏大的交易规则体系时，请适当为前台业务预留“沙盒容错”空间；捕获一线的非结构化反馈，能让制度更具生命力。"},
    "INTP": {"role": "量化风控专家", "desc": "穿透数据迷雾，寻找复杂业务表象下的底层逻辑漏洞与确权定价模型的最优解。", "tags": ["深度解构", "模型驱动", "极客思维"], "partner": "INTJ (架构锚定节点) / ENTP (模式发散节点)", "advice": "尝试将您极其高维的理论模型降维封装，形成非技术人员也能看懂的《操作指南》，让优秀的算法模型转化为实际生产力。"},
    "ISTJ": {"role": "合规审查主理官", "desc": "SDE 底层防线的守夜人，您的评估报告本身就是安全、严谨与业务零失误的代名词。", "tags": ["绝对合规", "程序正义", "风险兜底"], "partner": "ESTJ (业务推进节点) / ISFJ (后勤保障节点)", "advice": "在死守数据合规红线的同时，面对狂飙突进的创新产品，试着用“如何让它合规地上架”来指导业务，成为创新的坚实护航者。"},
    "ESTJ": {"role": "核心业务统筹官", "desc": "无可争议的推进器，擅长将国家宏观政策与高层战略拆解为团队可绝对执行的 KPI 矩阵。", "tags": ["强效统帅", "结果导向", "流程大师"], "partner": "ISTJ (合规审查节点) / ISTP (应急排障节点)", "advice": "在下发高压任务指令时，适度向团队释放“情绪价值”。一支具备高信任感的团队，往往比单纯的数字化目标走得更稳健。"},
    "INFJ": {"role": "产业生态智囊", "desc": "具备极强的跨频段共情能力，能精准预判数据流转对未来实体经济产生的深远变革。", "tags": ["远见卓识", "使命驱动", "战略前瞻"], "partner": "ENFJ (共识布道节点) / ENFP (火种传播节点)", "advice": "学会用精确的财务测算、合规条文来锚定您的宏大产业愿景。将“先知直觉”转化为具体的业务政策专报，提升落地的说服力。"},
    "INFP": {"role": "生态价值主张官", "desc": "冷酷数据背后的灵魂捕捉者，擅长在机械的交易网络中注入引人共鸣的生态文化与数字信仰。", "tags": ["价值感召", "组织粘合", "品牌定调"], "partner": "ENFJ (外部护航节点) / ISFP (美学交互节点)", "advice": "在跨部门协同博弈中，学会熟练利用预算工具和业务导向来捍卫您的核心价值主张，将柔性文化转化为硬性的机构资产。"},
    "ENTJ": {"role": "战略开拓领军人", "desc": "天生的矩阵建设者，在数据跨境、公共数据授权等探索区中展现极强的破局与开拓能力。", "tags": ["开疆拓土", "战略铁腕", "极致破局"], "partner": "INTJ (战略智囊节点) / ISTP (技术攻坚节点)", "advice": "在极速开疆拓土时，请时刻保持与中台合规团队的数据同步。有时放慢半拍听听风控预警，能让您避开隐蔽的系统性风险。"},
    "ENTP": {"role": "模式创新顾问", "desc": "传统交易规则的敏锐挑战者，致力于通过跨界思维寻找下一代数据资产流转的范式。", "tags": ["范式重构", "逻辑激辩", "思维跳跃"], "partner": "INTP (逻辑验证节点) / ESTP (市场收割节点)", "advice": "适当收敛发散思维，选择一个极具潜力的创新点（如特定行业的数据凭证），深度闭环跟进至最终交付，用结果验证前瞻。"},
    "ENFJ": {"role": "数商生态总监", "desc": "数据交易所的枢纽中心，能通过卓越的共识构建能力，将多方利益竞争者聚拢为紧密盟友。", "tags": ["关系枢纽", "温情领导力", "利益协同"], "partner": "INFJ (深度研究节点) / ESFJ (落地协同节点)", "advice": "在协调多方利益分配时，大胆引入客观的量化算法与智能合约刚性指标，确保“生态和谐”建立在牢不可破的规则基石之上。"},
    "ENFP": {"role": "平台资源布道大使", "desc": "充满感染力的生态火苗，让每一场路演与推介都变成数据要素市场的狂热共识。", "tags": ["无限创意", "跨界纽带", "高频驱动"], "partner": "INFJ (导航纠偏节点) / INTJ (架构落地节点)", "advice": "引入严密的商机日程表与里程碑管理。将您天马行空的生态创意，转化为可追踪的业务转化漏斗，大幅提升创新的商业核算价值。"},
    "ISFJ": {"role": "清结算运营中枢", "desc": "最坚韧的底层支点，于无声处通过极致纠错与细节控场支撑起整个平台的专业信誉与高吞吐流转。", "tags": ["极致支撑", "服务巅峰", "高可用节点"], "partner": "ESFJ (对外链接节点) / ISTJ (合规审核节点)", "advice": "在完美支撑中后台高速运转之余，尝试主动提出针对现有冗余确权流程的优化提案。您的实操痛点极具价值，应当被赋予更高权重。"},
    "ESFJ": {"role": "政企商务枢纽", "desc": "超级连接器，擅长经营多维度的外部政企生态关系，是前线业务部门的最强润滑剂与负载均衡器。", "tags": ["协作典范", "客情控制", "社会化支撑"], "partner": "ISFJ (精细支持节点) / ESTJ (宏观决策节点)", "advice": "在维护复杂商务生态时，建立更独立的合规风险过滤网。在照顾合作方诉求的同时，保持对机构底线的绝对清醒与坚守。"},
    "ISTP": {"role": "平台风控与排障专家", "desc": "数据底座的实干派，只对事实和逻辑代码负责，是系统面临大并发技术故障或业务危机时的定海神针。", "tags": ["极简实干", "故障排查", "硬核运维"], "partner": "ESTP (前线实战节点) / INTP (算法优化节点)", "advice": "尝试将您极度内隐的底层排查经验，沉淀为可视化的《应急响应标准手册》。打破沟通壁垒，将个体的技术赋能给整个作战团队。"},
    "ISFP": {"role": "资产交互体验官", "desc": "赋予枯燥进制数据以美学权重，致力于提升数字资产在路演与终端大屏展示时的绝对视觉专业质感。", "tags": ["审美溢价", "感官叙事", "体验极致"], "partner": "ESFP (公众表达节点) / INFP (共情叙事节点)", "advice": "在追求终端展示的美学溢价时，适度增加对核心确权流转逻辑和底层交易协议的理解，这会让您的作品拥有直击商业痛点的力量。"},
    "ESTP": {"role": "前沿敏捷先锋", "desc": "数据流通一线的敏锐猎手，能极快捕捉到瞬息万变的市场红利与数据应用空间的商业套利机会。", "tags": ["市场直觉", "敏捷收割", "实战专家"], "partner": "ISTP (底层兜底节点) / ENTJ (战略统筹节点)", "advice": "在捕捉市场瞬时机遇、展现高效行动力促成交易时，务必将前置合规审查纳入操作流程中，为强劲的业务冲刺装上安全的制动阀。"},
    "ESFP": {"role": "官方品牌推广使者", "desc": "交易所的前台形象窗口，天生具备将复杂的《数据二十条》解码为大众传播话术的超级天赋。", "tags": ["全域表现", "舆情响应", "公关信标"], "partner": "ISFP (视觉美学节点) / ENFP (创意破局节点)", "advice": "花时间深潜研究数据要素的底层逻辑与政策红头文件。将您的绝佳表现力建立在扎实的产业根基上，形成无可替代的权威影响力。"}
}

# --- 5. 极速状态机与回调 ---
for key, init_val in [
    ('started', False), ('current_q', 0), ('start_time', None), 
    ('end_time', None), ('calculating', False), ('user_alias', "SDE_NODE"),
    ('total_scores', {"E": 0, "S": 0, "T": 0, "J": 0}), ('firework_played', False)
]:
    if key not in st.session_state: st.session_state[key] = init_val

def start_assessment_callback():
    alias = st.session_state.login_input.strip()
    st.session_state.user_alias = html.escape(alias) if alias else "SDE_NODE"
    st.session_state.started = True
    st.session_state.start_time = time.time()

def answer_callback(val, dim):
    st.session_state.total_scores[dim] += (val - 3)
    st.session_state.current_q += 1
    if st.session_state.current_q >= len(questions):
        st.session_state.end_time = time.time()
        st.session_state.calculating = True

# --- 6. 核心渲染路由引擎 ---
if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 class="hero-title" data-text="上海数据交易所">上海数据交易所</h1><br>
            <h1 class="hero-title" data-text="核心人才全息引擎" style="font-size:32px !important;">核心人才全息引擎</h1>
            <div class="hero-subtitle">▶ SDE MATRIX V1.0_SECURE</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='terminal-container'>
        <div class='term-line'><span style='color:#94a3b8;'>[SYSTEM]</span> Establishing secure connection to SDE Core...</div>
        <div class='term-line'><span style='color:#94a3b8;'>[SYSTEM]</span> Loading Talent Capability Algorithm... <span style='color:#00f3ff;'>[OK]</span></div>
        <div class='term-line'><span style='color:#10b981;'>[COMPLIANCE]</span> Initializing Data Firewall... <span style='color:#00f3ff;'>[OK]</span></div>
        <div class='term-line-main'>
            <span style='color:#ffffff; font-size: 15px; font-family: "Noto Sans SC", sans-serif; line-height: 1.8;'>
            <br><b>2026年是数据要素价值释放的突破之年。</b><br><br>
            在“数据乘数”加速赋能实体经济的当下，合规风控红线与业务场景创新必须同频共振。<br>
            本终端将全方位扫描您的职场决策链路、风控模型与生态协同网络，为您生成独一无二的<b>职场高维数字标识</b>。</span>
            <span class="cursor-blink"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(key="login_form", border=False):
        st.markdown("<div style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:bold; margin-bottom:8px; text-align:center;'>▼ MOUNT NODE ALIAS (输入职场称呼 / 授权代号) ▼</div>", unsafe_allow_html=True)
        st.text_input("", key="login_input", placeholder="例如：Compliance_Wu", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        st.form_submit_button("▶ 授予系统权限并执行深度扫描", on_click=start_assessment_callback, type="primary", use_container_width=True)
    
    st.markdown("<div style='text-align:center; color:#475569; font-size:11px; margin-top:40px; font-family:monospace;'>END-TO-END ENCRYPTED · AUDIT TRAIL ENABLED</div>", unsafe_allow_html=True)

elif st.session_state.calculating:
    st.markdown("<h2 class='hero-title' data-text='[ DECODING MATRIX ]' style='font-size:32px !important; margin-top:50px;'>[ DECODING MATRIX ]</h2>", unsafe_allow_html=True)
    terminal = st.empty()
    logs = [
        f"VERIFYING IDENTITY: {st.session_state.user_alias.upper()}...",
        "EXTRACTING COGNITIVE VECTORS...",
        "QUANTIFYING RISK APPETITE & COMPLIANCE THRESHOLD...",
        "MAPPING TO SDE TALENT TOPOLOGY...",
        "GENERATING UNIQUE DIGITAL IDENTIFIER...",
        "DECRYPTION COMPLETE. INITIALIZING HUD..."
    ]
    log_text = ""
    for line in logs:
        log_text += f"<span style='color:#4ade80;'>[+]</span> {line}<br>"
        terminal.markdown(f"<div class='cli-box'>{log_text}</div>", unsafe_allow_html=True)
        time.sleep(0.35)
    st.session_state.calculating = False
    st.rerun()

elif st.session_state.current_q < len(questions):
    q_data = questions[st.session_state.current_q]
    
    dim_map = {
        "E": "[生态交互] 外部联结协同 vs 内部深潜研判", 
        "S": "[感知落地] 颗粒实务穿透 vs 宏观战略推演", 
        "T": "[量化风控] 客观逻辑刚性 vs 生态人际共情", 
        "J": "[秩序治理] 制度架构锚定 vs 敏捷响应沙盒"
    }
    module_name = dim_map.get(q_data['dim'])
    stable_hash_str = f"BLOCK_{st.session_state.current_q}_{q_data['q']}"
    dynamic_hash = hashlib.sha256(stable_hash_str.encode()).hexdigest()[:10].upper()
    
    st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
    
    progress_val = (st.session_state.current_q + 1) / len(questions)
    st.progress(progress_val)
    st.markdown(f"<div style='text-align:right; font-family:Orbitron, monospace; color:#00f3ff; font-size:12px; margin-top:5px;'>COMPLETION: {int(progress_val*100)}%</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: rgba(2, 6, 23, 0.85); border: 1px solid rgba(0, 243, 255, 0.4); border-radius: 6px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 15px rgba(0, 243, 255, 0.05); margin-top: 15px; margin-bottom: 25px; border-left: 5px solid #00f3ff; backdrop-filter: blur(5px);'>
        <div style='display:flex; justify-content:space-between; font-family:monospace; color:#00f3ff; font-size:12px; margin-bottom:15px; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom:10px;'>
            <span class='orbitron-font'>SYS_MOD: {module_name}</span>
            <span class='orbitron-font'>HASH: 0x{dynamic_hash}</span>
        </div>
        <div style='font-size: 16px; color: #ffffff !important; line-height: 1.7; font-weight: 500;'>
            {q_data['q']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    opts = [
        ("❌ [ 极度排斥 ] 强制阻断：完全背离我的工作直觉", 1),
        ("⚠️ [ 较少符合 ] 弱态耦合：仅在特定场景下采用", 2),
        ("⚖️ [ 中立待定 ] 视境判定：完全视具体业务环境而定", 3),
        ("🤝 [ 比较符合 ] 逻辑握手：是常用的业务决策链路", 4),
        ("🔒 [ 绝对锁定 ] 完美同步：完美复刻核心工作思维", 5)
    ]
    
    for text, val in opts:
        st.button(text, type="secondary", key=f"q_{st.session_state.current_q}_{val}", on_click=answer_callback, args=(val, q_data['dim']))

else:
    if not st.session_state.firework_played:
        trigger_supernova()
        st.session_state.firework_played = True
        
    res = st.session_state.total_scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    data = mbti_details.get(mbti)
    safe_alias_final = st.session_state.user_alias.upper()
    role_name = data['role']
    
    def get_intensity(score): return int(max(15, min(100, 50 + (score / (len(questions)/4) * 50))))
    val_E, val_I = get_intensity(res["E"]), 100 - get_intensity(res["E"])
    val_S, val_N = get_intensity(res["S"]), 100 - get_intensity(res["S"])
    val_T, val_F = get_intensity(res["T"]), 100 - get_intensity(res["T"])
    val_J, val_P = get_intensity(res["J"]), 100 - get_intensity(res["J"])

    p_score = -res.get("J", 0)
    s_score = res.get("S", 0)
    risk_score = int(max(5, min(95, 50 + (p_score * 1.5) - (s_score * 1.5))))
    
    if risk_score < 35: r_tag, r_color, r_desc = "底线合规与安全防线", "#10b981", "运行极其稳健，对合规红线有天然敬畏，适合把守数据存证与资产确权大门，是交易所底层的安全装甲。"
    elif risk_score < 65: r_tag, r_color, r_desc = "动态演进与边界平衡", "#ffd700", "能够在监管锁死与商业吞吐间寻求黄金接口，适合主导跨部门协作与全网业务流转统筹。"
    else: r_tag, r_color, r_desc = "无界扩张与前沿破局", "#f43f5e", "渴望突破陈旧的业务规则枷锁，拥有高爆发性的业务创新实战能力，能快速抢占新兴要素生态阵地。"

    time_taken = st.session_state.end_time - st.session_state.start_time
    hash_code = hashlib.sha256(f"{safe_alias_final}{mbti}{time_taken}".encode()).hexdigest()[:16].upper()

    # =========================================================================
    # ✨ 终极黑科技：引入 Tabs 将功能分为“图片海报”与“文本复制”
    # =========================================================================
    st.markdown("<br><h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>💠 身份密钥与海报提取中心</h4>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📸 生成全息图文海报 (推荐朋友圈)", "📝 提取纯文本格式 (适合群聊)"])

    with tab1:
        random.seed(hash_code)
        gradient_stops = []
        current_pos = 0
        while current_pos < 100:
            width = random.uniform(0.5, 3.0)
            space = random.uniform(0.5, 2.0)
            gradient_stops.append(f"rgba(0,243,255,0.6) {current_pos}%, rgba(0,243,255,0.6) {current_pos + width}%, transparent {current_pos + width}%, transparent {current_pos + width + space}%")
            current_pos += width + space
        barcode_css = "linear-gradient(90deg, " + ", ".join(gradient_stops) + ")"

        tags_html = "".join([f'<div style="background:rgba(0,243,255,0.1); border:1px solid rgba(0,243,255,0.4); padding:4px 8px; border-radius:4px; font-size:12px; color:#00f3ff; font-weight:bold;">{t}</div>' for t in data['tags']])

        html_to_image_script = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
            <style>
                body {{ margin: 0; display: flex; flex-direction: column; align-items: center; background-color: transparent; font-family: 'Noto Sans SC', sans-serif; user-select: none; padding: 10px 0;}}
                
                #capture-box {{
                    width: 340px; background-color: #030712; padding: 30px 25px; border-radius: 16px;
                    border: 1px solid rgba(0, 243, 255, 0.4); box-shadow: 0 0 30px rgba(0, 243, 255, 0.2);
                    position: relative; overflow: hidden; color: #fff; box-sizing: border-box;
                }}
                .cyber-grid {{
                    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                    background-image: linear-gradient(0deg, rgba(0,243,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0,243,255,0.04) 1px, transparent 1px);
                    background-size: 20px 20px; z-index: 0; pointer-events: none;
                }}
                .top-glow {{ position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: linear-gradient(90deg, transparent, #00f3ff, transparent); z-index: 1; }}
                
                .content {{ position: relative; z-index: 2; }}
                .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom: 15px; margin-bottom: 25px; }}
                .logo-text {{ color: #00f3ff; font-family: 'Orbitron', sans-serif; font-size: 15px; font-weight: 900; letter-spacing: 1px; }}
                .sub-logo {{ font-size: 18px; font-weight: 900; margin-top: 5px; letter-spacing: 2px; text-shadow: 0 0 10px rgba(255,255,255,0.2);}}
                .auth-box {{ text-align: right; }}
                .auth-title {{ color: #94a3b8; font-family: 'Orbitron', monospace; font-size: 10px; letter-spacing: 1px; }}
                .auth-hash {{ color: #00f3ff; font-family: 'Orbitron', monospace; font-size: 12px; font-weight: bold; margin-top: 3px; }}
                
                .user-name {{ text-align: center; font-size: 22px; font-weight: 900; letter-spacing: 2px; color: #fff; margin-bottom: 15px; text-transform: uppercase; }}
                .mbti {{ font-family: 'Orbitron', sans-serif; font-size: 68px; font-weight: 900; color: #ffd700; line-height: 1; text-align: center; text-shadow: 0 0 25px rgba(255,215,0,0.6); margin-bottom: 10px; letter-spacing: 4px; }}
                .role {{ text-align: center; font-size: 16px; font-weight: 900; color: #00f3ff; margin-bottom: 25px; letter-spacing: 1px; }}
                
                .tags {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-bottom: 25px; }}
                
                .metrics-box {{ background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 15px; margin-bottom: 25px; }}
                .stat-row {{ display: flex; align-items: center; margin-bottom: 10px; font-size: 11px; font-weight: bold; }}
                .stat-row:last-child {{ margin-bottom: 0; }}
                
                .risk-box {{ border-left: 4px solid {r_color}; background: {r_color}1A; padding: 12px; border-radius: 0 6px 6px 0; margin-bottom: 25px; }}
                .risk-title {{ font-size: 10px; color: #e2e8f0; margin-bottom: 4px; }}
                .risk-val {{ color: {r_color}; font-size: 16px; font-weight: 900; text-shadow: 0 0 10px {r_color}88; }}
                
                .footer {{ text-align: center; color: #64748b; font-family: 'Orbitron', monospace; font-size: 9px; padding-top: 15px; border-top: 1px dashed rgba(255,255,255,0.1); }}
                .barcode {{ width: 85%; height: 25px; margin: 0 auto 10px auto; background: {barcode_css}; }}

                #loading-ui {{ font-family: 'Orbitron', sans-serif; color: #00f3ff; font-size: 13px; text-align: center; padding: 40px; animation: pulse 1s infinite alternate; letter-spacing: 2px; }}
                @keyframes pulse {{ 0% {{ opacity: 1; text-shadow: 0 0 10px #00f3ff; }} 100% {{ opacity: 0.4; text-shadow: none; }} }}
                
                #result-img {{ display: none; width: 100%; max-width: 340px; border-radius: 16px; border: 1px solid rgba(0,243,255,0.5); box-shadow: 0 15px 35px rgba(0,0,0,0.8); pointer-events: auto; -webkit-touch-callout: default; }}
                .hint-box {{ display: none; color: #10b981; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); padding: 12px; border-radius: 6px; font-size: 13px; font-weight: bold; text-align: center; margin-top: 20px; line-height: 1.6; width: 100%; max-width: 340px; box-sizing: border-box; }}
            </style>
        </head>
        <body>
            <div id="render-target" style="position: absolute; left: -9999px;">
                <div id="capture-box">
                    <div class="cyber-grid"></div>
                    <div class="top-glow"></div>
                    <div class="content">
                        <div class="header">
                            <div><div class="logo-text">SDE MATRIX</div><div class="sub-logo">上海数据交易所</div></div>
                            <div class="auth-box"><div class="auth-title">SYS_HASH</div><div class="auth-hash">0x{hash_code[:6]}</div></div>
                        </div>
                        <div style="font-size:10px; color:#94a3b8; text-align:center; font-family:'Orbitron', monospace; margin-bottom:4px;">AUTHORIZED NODE</div>
                        <div class="user-name">{safe_alias_final}</div>
                        <div class="mbti">{mbti}</div>
                        <div class="role">【 {role_name} 】</div>
                        <div class="tags">{tags_html}</div>
                        
                        <div class="metrics-box">
                            <div style="font-family: 'Orbitron', monospace; font-size: 9px; color: #00f3ff; text-align: center; margin-bottom: 12px;">/// CAPABILITY METRICS ///</div>
                            <div class="stat-row"><span style="color:#e2e8f0; width:45px;">生态(E)</span><div style="flex-grow:1; height:6px; background:#1e293b; border-radius:3px; margin:0 10px; position:relative; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{val_E}%; background:#00f3ff; box-shadow:0 0 8px #00f3ff; border-radius:3px;"></div></div><span style="color:#94a3b8; width:45px; text-align:right;">深潜(I)</span></div>
                            <div class="stat-row"><span style="color:#e2e8f0; width:45px;">实勘(S)</span><div style="flex-grow:1; height:6px; background:#1e293b; border-radius:3px; margin:0 10px; position:relative; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{val_S}%; background:#a855f7; box-shadow:0 0 8px #a855f7; border-radius:3px;"></div></div><span style="color:#94a3b8; width:45px; text-align:right;">前瞻(N)</span></div>
                            <div class="stat-row"><span style="color:#e2e8f0; width:45px;">量化(T)</span><div style="flex-grow:1; height:6px; background:#1e293b; border-radius:3px; margin:0 10px; position:relative; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{val_T}%; background:#3b82f6; box-shadow:0 0 8px #3b82f6; border-radius:3px;"></div></div><span style="color:#94a3b8; width:45px; text-align:right;">共情(F)</span></div>
                            <div class="stat-row"><span style="color:#e2e8f0; width:45px;">秩序(J)</span><div style="flex-grow:1; height:6px; background:#1e293b; border-radius:3px; margin:0 10px; position:relative; overflow:hidden;"><div style="position:absolute; left:0; top:0; height:100%; width:{val_J}%; background:#10b981; box-shadow:0 0 8px #10b981; border-radius:3px;"></div></div><span style="color:#94a3b8; width:45px; text-align:right;">敏捷(P)</span></div>
                        </div>
                        
                        <div class="risk-box">
                            <div class="risk-title">风控熔断判定阈值</div>
                            <div class="risk-val">{r_tag}</div>
                        </div>
                        
                        <div class="footer">
                            <div class="barcode"></div>
                            <div style="margin-bottom: 4px;">2026 SDE DATA ELEMENT KERNEL</div>
                            <div>FULL_HASH: 0x{hash_code}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="loading-ui">[ GENERATING HOLOGRAPHIC ID... ]</div>
            <img id="result-img" alt="SDE Matrix Card" title="长按保存或分享" />
            <div id="hint" class="hint-box">✅ 海报压制成功！<br><span style="color:#fff;">👆 手机端请 <b>长按上方图片</b><br>即可「发送给朋友」或「保存到相册」</span></div>

            <script>
                // ✨ 核心移动端修复：废弃不稳定的 document.fonts.ready，采用强力延时渲染
                window.onload = function() {{
                    setTimeout(function() {{
                        const target = document.getElementById('capture-box');
                        html2canvas(target, {{
                            scale: 2, // 降维至2倍图，彻底杜绝手机 Canvas 内存溢出导致白屏
                            backgroundColor: '#030712',
                            useCORS: true,
                            allowTaint: true
                        }}).then(canvas => {{
                            try {{
                                document.getElementById('result-img').src = canvas.toDataURL('image/png');
                                document.getElementById('loading-ui').style.display = 'none';
                                document.getElementById('result-img').style.display = 'block';
                                document.getElementById('hint').style.display = 'block';
                                document.getElementById('render-target').style.display = 'none';
                            }} catch(e) {{
                                document.getElementById('loading-ui').innerHTML = '⚠️ 渲染异常，请直接系统截图保存';
                            }}
                        }}).catch(err => {{
                            document.getElementById('loading-ui').innerHTML = '⚠️ 渲染超时，请直接系统截图保存';
                        }});
                    }}, 1500); // 预留1.5秒充足时间加载字体
                }};
            </script>
        </body>
        </html>
        """
        components.html(html_to_image_script, height=750)

    with tab2:
        st.markdown("<div style='font-size:13px; color:#94a3b8; margin-bottom:10px; margin-top:10px;'>👇 点击下方代码框右上角的 <b style='color:#00f3ff;'>Copy</b> 图标提取纯文本格式：</div>", unsafe_allow_html=True)
        share_card = f"""【上海数据交易所 · 人才全息图谱】
=================================
👤 授权节点：{safe_alias_final}
🧬 核心架构：{mbti} ({role_name})
🎯 赋能标签：{' · '.join(data['tags'])}
⚖️ 风控偏好：{r_tag}
=================================
🌐 2026 数据要素突破之年，寻找你的协同节点！
🔗 [全息链路校验哈希: 0x{hash_code}]"""
        st.code(share_card, language="plaintext")

    categories = ['生态拓展(E)', '实务风控(S)', '逻辑共识(T)', '秩序合规(J)', '节点深潜(I)', '宏观架构(N)', '价值共情(F)', '敏捷演化(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]

    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🕸️ 核心算力拓扑矩阵</h4>", unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.1)', line=dict(color='rgba(0, 243, 255, 0.2)', width=8), hoverinfo='none'))
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=2.5), marker=dict(color='#ff003c', size=6, symbol='diamond')))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC, sans-serif", color='#e2e8f0', size=12), linecolor='rgba(0,243,255,0.2)', gridcolor='rgba(0,243,255,0.15)')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=55, r=55, t=30, b=30), height=350)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<h4 style='color:#10b981 !important; border-left:4px solid #10b981; padding-left:10px; font-weight:900;'>💡 生态网络协同指引</h4>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, rgba(16, 185, 129, 0.08), rgba(0,0,0,0)); border-left: 4px solid #10b981; padding: 20px; border-radius: 4px; font-size: 14px; line-height: 1.7; color: #e2e8f0 !important; border-top: 1px solid rgba(16, 185, 129, 0.3); border-bottom: 1px solid rgba(16, 185, 129, 0.3); box-shadow: 0 5px 20px rgba(0,0,0,0.5); margin: 15px 0 30px 0;'>
        <div style='color: #10b981 !important; font-weight: 900; font-size: 13px; margin-bottom: 8px; font-family: "Orbitron", sans-serif !important; letter-spacing: 2px;'>[ 黄金并网节点 ]</div>
        <div style='margin-bottom:15px; color:#ffffff !important; font-weight:900; font-size:15px;'>{data['partner']}</div>
        <div style='color: #10b981 !important; font-weight: 900; font-size: 13px; margin-bottom: 8px; font-family: "Orbitron", sans-serif !important; letter-spacing: 2px;'>[ 算力超频建议 ]</div>
        <div>{data['advice']}</div>
        <div style='margin-top:15px; border-top:1px dashed rgba(16,185,129,0.3); padding-top:15px; color:#94a3b8; font-size:12px;'>
            {r_desc}
        </div>
    </div>
    """, unsafe_allow_html=True)

    def reset_system():
        st.session_state.started = False
        st.session_state.current_q = 0
        st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
        st.session_state.start_time = None
        st.session_state.end_time = None
        st.session_state.calculating = False
        st.session_state.user_alias = "SDE_NODE"
        st.session_state.firework_played = False

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("⏏ 弹出磁盘并重启矩阵 (SYS_REBOOT)", on_click=reset_system, type="primary", use_container_width=True)

st.markdown("""
    <div style='text-align:center; margin-top:50px; margin-bottom:20px; font-family:\"Orbitron\", monospace; position:relative; z-index:10;'>
        <div style='color:#00f3ff !important; font-size:10px; opacity:0.4; letter-spacing:4px; margin-bottom:5px;'>
            POWERED BY SDE DATA ELEMENT KERNEL
        </div>
        <div style='color:#00f3ff !important; font-size:10px; opacity:0.2; letter-spacing:2px;'>
            SECURE ENTERPRISE BUILD
        </div>
    </div>
""", unsafe_allow_html=True)


