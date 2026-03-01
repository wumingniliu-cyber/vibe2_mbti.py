import streamlit as st
import random
import time
import math
import hashlib
import html  # 用于防范 XSS 攻击
import plotly.graph_objects as go
# 已经彻底移除了无用的 pandas 依赖，提升冷启动速度

# --- 1. 页面与全局配置 ---
st.set_page_config(
    page_title="SDE 核心人才资产引擎",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 绝对防御级 UI 与赛博动效注入 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Orbitron:wght@400;500;700;900&display=swap');

    /* 终极锁死全局背景 */
    html, body, [class*="css"], .stApp { 
        background-color: #030712 !important; 
        font-family: 'Noto Sans SC', sans-serif !important;
        color: #f8fafc !important;
    }
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: transparent !important;
    }
    [data-testid="stAppViewContainer"] {
        background-image: 
            radial-gradient(circle at 50% 0%, #0f172a 0%, #030712 80%),
            linear-gradient(0deg, rgba(0,243,255,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,243,255,0.02) 1px, transparent 1px) !important;
        background-size: 100% 100%, 30px 30px, 30px 30px !important;
    }
    .stMarkdown, p, span, h2, h3, h4, li, div { color: #f8fafc !important; }
    
    /* 丝滑转场动画 */
    [data-testid="stAppViewBlockContainer"] { animation: smoothFadeIn 0.5s cubic-bezier(0.22, 1, 0.36, 1); }
    @keyframes smoothFadeIn { 0% { opacity: 0; transform: translateY(10px); filter: blur(2px); } 100% { opacity: 1; transform: translateY(0); filter: blur(0); } }
    
    /* 标题高定光感 */
    .hero-title { 
        font-size: 38px !important; font-weight: 900 !important; text-align: center; 
        color: #ffffff !important; letter-spacing: 3px; margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(0,243,255,0.8), 0 0 40px rgba(0,243,255,0.4);
    }
    .hero-subtitle { text-align: center; color: #00f3ff !important; font-size: 13px; letter-spacing: 6px; opacity: 0.9; margin-bottom: 30px; font-family: 'Orbitron', sans-serif !important; font-weight: 700; }

    /* 赛博风输入框 */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: rgba(2, 6, 23, 0.9) !important; color: #00f3ff !important; font-family: 'Orbitron', monospace !important;
        border: 1px solid rgba(0,243,255,0.5) !important; border-radius: 8px !important;
        text-align: center; font-size: 18px !important; font-weight: bold !important; letter-spacing: 2px;
        box-shadow: inset 0 0 15px rgba(0,243,255,0.1) !important;
    }
    div[data-testid="stTextInput"] > div > div > input:focus { border-color: #ffd700 !important; box-shadow: 0 0 20px rgba(255,215,0,0.3), inset 0 0 15px rgba(255,215,0,0.2) !important; }

    /* 靶向接管选项按钮 */
    div.stButton > button {
        background: #0f172a !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; border-left: 4px solid rgba(0, 243, 255, 0.6) !important;
        border-radius: 8px !important; min-height: 60px !important; width: 100% !important; padding: 12px 15px !important; text-align: left !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.6) !important; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button p, div.stButton > button span { color: #ffffff !important; font-size: 15px !important; line-height: 1.5 !important; white-space: normal !important; font-weight: 500 !important; }
    div.stButton > button:hover { background: rgba(0, 243, 255, 0.15) !important; border-color: #00f3ff !important; border-left: 4px solid #00f3ff !important; box-shadow: 0 0 20px rgba(0,243,255,0.3) !important; transform: translateX(4px) !important; }
    div.stButton > button:active { transform: scale(0.98) !important; }

    /* 启动与重启的 Primary 按钮 */
    div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #00f3ff, #0088ff) !important; border-left: none !important; text-align: center !important;
    }
    div.stButton > button[data-testid="baseButton-primary"] p { color: #030712 !important; font-weight: 900 !important; font-size: 16px !important; letter-spacing: 2px !important; }
    div.stButton > button[data-testid="baseButton-primary"]:hover { transform: translateY(-2px) scale(1.02) !important; box-shadow: 0 0 40px rgba(0,243,255,0.8) !important; }
    
    /* ✨ txt建议落实：彻底接管进度条，实现赛博风发光 */
    [data-testid="stProgress"] > div > div > div {
        background-color: #00f3ff !important;
        box-shadow: 0 0 10px rgba(0,243,255,0.6) !important;
    }

    /* 结果视窗 */
    .result-card {
        padding: 40px 25px; border-radius: 16px; background: rgba(11, 17, 32, 0.95) !important; 
        border: 1px solid rgba(255,215,0,0.3); border-top: 6px solid #ffd700; 
        text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.8); margin-bottom: 30px;
    }
    .mbti-code { font-family: 'Orbitron', sans-serif !important; font-size: 80px; font-weight: 900; color: #ffd700 !important; line-height: 1.1; letter-spacing: 4px; text-shadow: 0 0 35px rgba(255,215,0,0.6); margin: 0;}
    
    /* 专属终端控制台 */
    .cli-box {
        background: #000000; border: 1px solid #334155; border-left: 4px solid #00f3ff;
        padding: 20px; border-radius: 8px; font-family: 'Orbitron', monospace; font-size: 13px;
        color: #4ade80; box-shadow: inset 0 0 20px rgba(0,243,255,0.1); margin-top: 50px;
    }
    .orbitron-font { font-family: 'Orbitron', sans-serif !important; font-weight: 700; color: #00f3ff; }

    /* 性能优化版烟花 */
    .firework-center { position: fixed; top: 50%; left: 50%; z-index: 99999; pointer-events: none; font-weight: 900; font-family: 'Orbitron', sans-serif; color: #00f3ff; text-shadow: 0 0 20px #00f3ff, 0 0 40px #ffffff; animation: supernova 1.8s cubic-bezier(0.1, 0.9, 0.2, 1) forwards; will-change: transform, opacity;}
    @keyframes supernova { 0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; } 100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; } }
</style>
""", unsafe_allow_html=True)

def trigger_supernova():
    html_str = ""
    symbols = ["1", "0", "DATA", "NODE", "SDE"]
    for _ in range(40): 
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(300, 1000)
        tx, ty = distance * math.cos(angle), distance * math.sin(angle)
        scale = random.uniform(1.0, 3.0)
        rot = random.randint(-360, 360)
        delay = random.uniform(0, 0.15)
        text = random.choice(symbols)
        html_str += f'<div class="firework-center" style="--tx:{tx}px; --ty:{ty}px; --s:{scale}; --rot:{rot}deg; animation-delay:{delay}s; font-size:{random.randint(18, 28)}px;">{text}</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 题库核心引擎 (如需分离，可挪至 data.py) ---
questions = [
    {"q": "面对数商生态中各方利益的博弈冲突，我倾向于亲自到现场进行高频次的调解与游说。", "dim": "E"},
    {"q": "代表交易所进行政策咨询时，我享受通过专业表达输出机构影响力的过程。", "dim": "E"},
    {"q": "相比审阅合同，我更擅长通过“头脑风暴”快速萃取业务协同方案。", "dim": "E"},
    {"q": "我习惯于维护庞大的人脉网络，并定期主动激活其中的潜在业务价值。", "dim": "E"},
    {"q": "处理突发声誉风险时，我倾向于迅速发声而非长时间闭门研判。", "dim": "E"},
    {"q": "在大型业务路演中，我发现自己能激发出比独处时更多的创新灵感。", "dim": "E"},
    {"q": "新政策出台后，我会第一时间在专业群组发起讨论而非独自研读。", "dim": "E"},
    {"q": "面对跨部门协作壁垒，我倾向于用非正式的社交手段来打破僵局。", "dim": "E"},
    {"q": "我能适应高强度的商务谈判频率，并从中获得极大的成就感。", "dim": "E"},
    {"q": "在推行规则时，我坚信“现场宣贯”的效果远优于“文件下发”。", "dim": "E"},
    {"q": "即使是宏大的项目，我也会先死磕会计科目调整的每一个底层逻辑。", "dim": "S"},
    {"q": "我更信任成交曲线和合规存证等量化数据，而非定性的趋势预判。", "dim": "S"},
    {"q": "面对新名词（如隐私计算），我首先关注其具体的技术落地路径。", "dim": "S"},
    {"q": "我认为交易所的核心任务是把确权、存证、结算动作做到零差错。", "dim": "S"},
    {"q": "撰写报告时，我习惯于堆叠详实的事实证据，而非过多的战略隐喻。", "dim": "S"},
    {"q": "相比于预测十年规划，我更关心下个季度的结算效率如何提升。", "dim": "S"},
    {"q": "成熟的交易所应当像精密机器，规则的稳定性优于频繁的创新。", "dim": "S"},
    {"q": "在法律文本面前，我总能敏锐捕捉到导致实操失败的措辞隐患。", "dim": "S"},
    {"q": "我偏好有明确时间节点的阶段性产出，即使只是流程的微小改良。", "dim": "S"},
    {"q": "对于审核上架，我倾向于依赖标准清单而非主观的价值评估。", "dim": "S"},
    {"q": "即使影响交易额，我也会关停任何存在合规瑕疵的高收益项目。", "dim": "T"},
    {"q": "评估数商信用时，我只看客观履约数据，不看行业内的情感口碑。", "dim": "T"},
    {"q": "交易所职责应当职责分明、冷酷高效，过度人情味会损伤公平。", "dim": "T"},
    {"q": "面对跨部门争议，我倾向于寻找逻辑最优解，而非寻求情感平衡。", "dim": "T"},
    {"q": "当下属工作出现失误，我会直接指出逻辑谬误，认为这是最高效的。", "dim": "T"},
    {"q": "我倾向于通过智能合约等技术手段替代人工审核，确保绝对公平。", "dim": "T"},
    {"q": "在收益分配中，我坚信“贡献度量化”应绝对优于“生态扶持”。", "dim": "T"},
    {"q": "面对不合理的业务要求，我会列举逻辑障碍回绝，而非婉转迁就。", "dim": "T"},
    {"q": "合规官应当像法官一样理智，不被外界的业务热潮所干扰。", "dim": "T"},
    {"q": "处理投诉时，我关注问题的本质技术原因，而非投诉者的情绪。", "dim": "T"},
    {"q": "我会为重大项目建立多级倒排计划，并极其反感进度失去控制。", "dim": "J"},
    {"q": "我的云盘文件夹拥有严密的分类逻辑，索引缺失会让我感到不适。", "dim": "J"},
    {"q": "如果没有形成明确的决议和责任人，我会认为这场会议是失败的。", "dim": "J"},
    {"q": "我倾向于在项目初期锁定所有需求，对中途变卦持排斥态度。", "dim": "J"},
    {"q": "即便再忙碌，我也坚持每日进行工作复盘并更新待办任务清单。", "dim": "J"},
    {"q": "交易所运营应当“重制度设计、轻即兴发挥”，哪怕牺牲反应速度。", "dim": "J"},
    {"q": "我几乎从不拖延，因为待办清单的存在会带给我无形的心理压力。", "dim": "J"},
    {"q": "我更喜欢节奏稳定、可预测的环境，而非每天处理突发任务。", "dim": "J"},
    {"q": "为了确保最终交付质量，我会提前预留出至少20%的缓冲时间。", "dim": "J"},
    {"q": "面对多线任务，我必须先梳理优先级并获得确认，才能安心执行。", "dim": "J"}
]

# --- 4. 组织节点画像数据库 ---
mbti_details = {
    "INTJ": {"role": "首席制度架构师", "desc": "数据要素世界的“造物主”，致力于构建严密的数据治理公理体系。", "tags": ["逻辑闭环", "顶层设计", "制度自信"], "partner": "ENTJ (强效执行节点) / INTP (极客算法节点)", "advice": "在构建宏大的底层规则架构时，请适当为业务部门预留“沙盒容错”空间；倾听一线的非结构化反馈，能让制度更具生命力。"},
    "INTP": {"role": "风控模型专家", "desc": "穿透迷雾，寻找业务背后底层的逻辑漏洞与算力平衡。", "tags": ["黑客思维", "算法驱动", "极致解构"], "partner": "INTJ (框架锚定节点) / ENTP (模式发散节点)", "advice": "尝试将你极其高维的理论模型降维封装，形成非技术人员也能看懂的业务操作手册，让优秀的逻辑转化为具体的生产力。"},
    "ISTJ": {"role": "首席合规审查官", "desc": "交易所的守夜人，你的名字本身就是安全、严谨、零失误的代名词。", "tags": ["绝对合规", "程序正义", "数据护法"], "partner": "ESTJ (业务推进节点) / ISFJ (后勤保障节点)", "advice": "在死守数据合规底线的同时，面对狂飙突进的创新产品，试着用“如何让它合规地上架”来指导业务，成为创新的护航者。"},
    "ESTJ": {"role": "业务统筹总监", "desc": "无可争议的项目推进器，擅长将复杂的国家政策转化为可落地的KPI体系。", "tags": ["统帅力", "结果主义", "流程大师"], "partner": "ISTJ (品控审查节点) / ISTP (危机拆弹节点)", "advice": "在推进高压任务时，适度向团队释放情绪价值。一支拥有高凝聚力和信任感的团队，往往比单纯的数字化目标走得更稳健。"},
    "INFJ": {"role": "产业生态智库", "desc": "具备极强的行业共情能力，能精准预判数据流通对未来文明产生的变革。", "tags": ["远见卓识", "使命驱动", "人文视角"], "partner": "ENFJ (共识布道节点) / ENFP (火种传播节点)", "advice": "学会用精确的财务数据、合规条文来锚定你的宏大产业愿景。将“先知感知”转化为具体的业务政策专报，提升落地的说服力。"},
    "INFP": {"role": "品牌价值主张官", "desc": "数据背后的灵魂捕捉者，擅长构建不仅专业而且动人的数商生态故事。", "tags": ["感召力", "价值观构建", "组织粘合"], "partner": "ENFJ (外部护航节点) / ISFP (美学交互节点)", "advice": "在跨部门协同博弈中，学会熟练利用预算工具和业务导向来捍卫你的核心价值主张，将柔性文化转化为硬性的机构资产。"},
    "ENTJ": {"role": "市场开拓领军人", "desc": "天生的建设者，在数据资源化、产品化的无人区中展现极强的破局能力。", "tags": ["开疆拓土", "战略铁腕", "极速成交"], "partner": "INTJ (战略智囊节点) / ISTP (技术攻坚节点)", "advice": "在极速开疆拓土时，请时刻保持与中台合规团队的数据同步。有时放慢半拍听听风控建议，能让你避开隐蔽的系统性风险。"},
    "ENTP": {"role": "产品创新顾问", "desc": "交易规则的敏锐挑战者，致力于通过跨界思维寻找下一代交易范式。", "tags": ["模式创新", "辩才无碍", "思维跳变"], "partner": "INTP (逻辑验证节点) / ESTP (市场收割节点)", "advice": "适当收敛发散思维，选择一个极具潜力的创新点（如特定数据产权凭证），深度闭环跟进至最终交付，用结果验证你的前瞻性。"},
    "ENFJ": {"role": "数商生态总监", "desc": "数交所的魅力中心，能通过卓越的共识构建能力，将竞争方聚拢为盟友。", "tags": ["关系枢纽", "温情领导力", "利益协调"], "partner": "INFJ (深度研究节点) / ESFJ (落地协同节点)", "advice": "在协调多方利益分配时，大胆引入客观的量化算法与刚性指标，确保“生态和谐”建立在牢不可破的规则基石之上。"},
    "ENFP": {"role": "资源链接大使", "desc": "充满感染力的生态火苗，让每一场路演都变成数据要素市场的信仰共识。", "tags": ["无限创意", "跨界纽带", "热情驱动"], "partner": "INFJ (导航纠偏节点) / INTJ (架构落地节点)", "advice": "引入严密的日程表与里程碑管理。将你天马行空的生态创意，转化为可追踪的业务转化漏斗，大幅提升创新的商业核算价值。"},
    "ISFJ": {"role": "高级行政主管", "desc": "最坚韧的底层支点，于无声处通过极致细节支撑起整个平台的专业信誉。", "tags": ["利他主义", "执行力巅峰", "运营专家"], "partner": "ESFJ (对外链接节点) / ISTJ (品控审核节点)", "advice": "在完美支撑中后台高速运转之余，尝试主动提出针对现有冗余流程的优化提案。你的实操经验极具价值，应当被更多人看见。"},
    "ESFJ": {"role": "商务关系主管", "desc": "超级连接器，擅长经营多维度的商务关系，是前台业务的最强润滑剂。", "tags": ["协作典范", "细节控制", "社会化支撑"], "partner": "ISFJ (精细支持节点) / ESTJ (宏观决策节点)", "advice": "在维护复杂商务生态时，建立更独立的风险评估过滤网，在照顾合作方诉求的同时，保持对业务底线的绝对清醒。"},
    "ISTP": {"role": "危机管理专家", "desc": "数据底座的实干极客，只对事实和逻辑负责，是突发故障时的定海神针。", "tags": ["极简实干", "危机直觉", "技术硬核"], "partner": "ESTP (前线实战节点) / INTP (算法优化节点)", "advice": "尝试将你极度内隐的危机处理经验，沉淀为可视化的预案文档。打破技术沟通壁垒，将个人的技术赋能给整个团队系统。"},
    "ISFP": {"role": "视觉交互设计专家", "desc": "赋予枯燥数据以美学价值，致力于提升资产评估与路演的颜值与专业质感。", "tags": ["审美溢价", "感官叙事", "独立纯粹"], "partner": "ESFP (公众表达节点) / INFP (共情叙事节点)", "advice": "在追求数字展示的美学溢价时，适度增加对核心业务逻辑和底层交易规则的理解，这会让你的作品拥有直击商业痛点的力量。"},
    "ESTP": {"role": "大客户成交官", "desc": "数据交易的敏锐猎手，能极快捕捉到瞬息万变的市场红利与应用空间。", "tags": ["现场感", "博弈高手", "结果收割"], "partner": "ISTP (底层兜底节点) / ENTJ (战略统筹节点)", "advice": "在捕捉市场瞬时机遇、展现高效行动力时，务必将前置合规审查纳入你的操作雷达之内，为强劲的业务冲刺装上安全的制动阀。"},
    "ESFP": {"role": "公共关系大使", "desc": "交易所形象代言人，天生具备将复杂的业务逻辑转化为大众传播话术的天赋。", "tags": ["表现力", "当下主义", "快乐源泉"], "partner": "ISFP (视觉美学节点) / ENFP (创意破局节点)", "advice": "花时间深潜研究数据要素的底层逻辑与政策文件。将你的绝佳表现力建立在扎实的产业根基上，形成无可替代的权威影响力。"}
}

# --- 5. 核心状态机管理 ---
if 'started' not in st.session_state: st.session_state.started = False
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'total_scores' not in st.session_state: st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'end_time' not in st.session_state: st.session_state.end_time = None
if 'calculating' not in st.session_state: st.session_state.calculating = False
if 'user_alias' not in st.session_state: st.session_state.user_alias = "SDE_NODE"
# ✨ txt建议落实：防止烟花无限重播的锁
if 'firework_played' not in st.session_state: st.session_state.firework_played = False

# ✨ txt建议落实：使用官方原生 on_click 回调函数，彻底解决答题闪烁和点击冲突
def answer_clicked(val, dim):
    st.session_state.total_scores[dim] += (val - 3)
    st.session_state.current_q += 1
    # ✨ txt建议落实：消灭魔法数字 40，使用 len(questions)
    if st.session_state.current_q == len(questions):
        st.session_state.end_time = time.time()
        st.session_state.calculating = True

# --- 6. 渲染引擎 ---
if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title'>上海数据交易所<br>人才图谱全息引擎</h1>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>▶ SDE MATRIX V23.0_GENESIS</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: 25px; border-radius: 12px; font-family: monospace; font-size: 14px; color: #e2e8f0; box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px;'>
        <span style='color:#94a3b8;'>[SYSTEM]</span> Establishing secure connection to SDE Core...<br>
        <span style='color:#94a3b8;'>[SYSTEM]</span> Loading Capability Matrix Algorithm... <span style='color:#00f3ff;'>[OK]</span><br>
        <span style='color:#10b981;'>[AUDIT]</span> Initializing Compliance & Risk Framework... <span style='color:#00f3ff;'>[OK]</span><br><br>
        <span style='color:#ffffff; font-size: 15px; font-family: "Noto Sans SC", sans-serif; line-height: 1.8;'><b>2026年是数据要素价值释放的突破之年。</b>在“数据乘数”加速赋能实体经济的当下，合规红线与业务创新必须同频共振。<br><br>本全息终端将深度解析您的底层能力架构、风控决策模型与生态协同潜能，为您生成专属的职场能力数字标识。</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ✨ txt建议落实：采用 st.form 表单，支持回车键无缝登录
    with st.form(key="login_form", border=False):
        st.markdown("<div style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:bold; margin-bottom:5px;'>▶ ENTER NODE ALIAS (输入授权代号/姓名):</div>", unsafe_allow_html=True)
        input_alias = st.text_input("", placeholder="e.g. Director_Wu", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 提交表单时触发
        if st.form_submit_button("▶ 授予系统权限并启动扫描", type="primary", use_container_width=True):
            # 防 XSS 注入并保存名字
            st.session_state.user_alias = html.escape(input_alias.strip()) if input_alias.strip() else "SDE_NODE"
            st.session_state.started = True
            st.session_state.start_time = time.time()
            st.rerun()
    
    st.markdown("<div style='text-align:center; color:#475569; font-size:11px; margin-top:20px; font-family:monospace;'>END-TO-END ENCRYPTED · AUDIT TRAIL ENABLED</div>", unsafe_allow_html=True)

# ✨ txt建议落实：消灭魔法数字
elif st.session_state.current_q < len(questions):
    q_data = questions[st.session_state.current_q]
    dim_map = {"E": "生态链路拓扑 (ECO_TOPOLOGY)", "S": "要素颗粒解析 (ASSET_GRANULARITY)", "T": "合规风控共识 (RISK_CONSENSUS)", "J": "演化秩序引擎 (EVOLUTION_GOVERNANCE)"}
    module_name = dim_map.get(q_data['dim'], "特征算力提取 (CORE_EXTRACTION)")
    
    # ✨ txt建议落实：摒弃 time.time()，采用静态题号生成 Hash，彻底消除 Hash 闪烁
    dynamic_hash = hashlib.sha256(f"BLOCK_{st.session_state.current_q}_{q_data['q']}".encode()).hexdigest()[:10].upper()
    
    st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q + 1) / len(questions))
    
    st.markdown(f"""
    <div style='background: rgba(2, 6, 23, 0.8); border: 1px solid rgba(0, 243, 255, 0.4); border-radius: 12px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 15px rgba(0, 243, 255, 0.05); margin-top: 15px; margin-bottom: 25px; border-left: 5px solid #00f3ff;'>
        <div style='display:flex; justify-content:space-between; font-family:monospace; color:#00f3ff; font-size:12px; margin-bottom:15px; border-bottom: 1px solid rgba(0,243,255,0.2); padding-bottom:10px;'>
            <span class='orbitron-font'>▶ MODULE: {module_name}</span>
            <span class='orbitron-font'>BLOCK: 0x{dynamic_hash}</span>
        </div>
        <div style='font-size: 17px; color: #ffffff !important; line-height: 1.6; font-weight: 500;'>
            {q_data['q']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    opts = [
        ("[ 00% ] 拒绝指令：完全背离业务直觉", 1),
        ("[ 25% ] 偏离轨道：较不符合执行习惯", 2),
        ("[ 50% ] 待定挂起：视具体交易场景而定", 3),
        ("[ 75% ] 拟合特征：比较符合决策链路", 4),
        ("[ 100% ] 强制锁定：完全复刻底层逻辑", 5)
    ]
    
    for text, val in opts:
        # ✨ txt建议落实：采用 on_click 原生回调，不再在循环内写 st.rerun()
        st.button(
            text, 
            type="secondary", 
            key=f"q_{st.session_state.current_q}_{val}",
            on_click=answer_clicked,
            args=(val, q_data['dim'])
        )

elif st.session_state.calculating:
    st.markdown("<h2 style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; letter-spacing:4px; text-shadow:0 0 15px rgba(0,243,255,0.8); text-align:center; margin-top:50px;'>[ SYSTEM DECODING ]</h2>", unsafe_allow_html=True)
    terminal = st.empty()
    logs = [
        f"VERIFYING NODE: {st.session_state.user_alias}...",
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

else:
    # ✨ txt建议落实：防烟花重播锁发挥作用
    if not st.session_state.firework_played:
        trigger_supernova()
        st.session_state.firework_played = True
    
    res = st.session_state.total_scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    data = mbti_details.get(mbti)
    
    st.markdown(f"""
    <div class="result-card">
        <div class="orbitron-font" style="font-size:13px; color:#94a3b8; letter-spacing:4px; margin-bottom:15px;">MATRIX DECODED SUCCESSFULLY</div>
        <div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:13px; margin-bottom:5px; border-bottom:1px dashed #334155; padding-bottom:10px; display:inline-block;">AUTH_NODE: {st.session_state.user_alias}</div>
        <div class="mbti-code" style="margin-top:10px;">{mbti}</div>
        <div class="mbti-post">【 {data['role']} 】</div>
        <div style="color:#e2e8f0 !important; font-size:15px; line-height:1.8; margin-bottom:25px; font-weight:400;">{data['desc']}</div>
        <div>
            {" ".join([f'<span style="background:#1e293b; color:#00f3ff !important; border:1px solid #00f3ff; padding:5px 12px; border-radius:6px; font-size:12px; font-weight:700; margin:4px; display:inline-block; font-family:\'Noto Sans SC\', sans-serif;">{t}</span>' for t in data['tags']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🕸️ 核心能力拓扑矩阵</h4>", unsafe_allow_html=True)
    def get_intensity(score): return max(15, min(100, 50 + (score / 20 * 50)))
    val_E, val_I = get_intensity(res["E"]), 100 - get_intensity(res["E"])
    val_S, val_N = get_intensity(res["S"]), 100 - get_intensity(res["S"])
    val_T, val_F = get_intensity(res["T"]), 100 - get_intensity(res["T"])
    val_J, val_P = get_intensity(res["J"]), 100 - get_intensity(res["J"])
    categories = ['外向(E)', '实务(S)', '理性(T)', '秩序(J)', '内向(I)', '直觉(N)', '感性(F)', '灵活(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.1)', line=dict(color='rgba(0, 243, 255, 0.2)', width=8), hoverinfo='none'))
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=2.5), marker=dict(color='#ffd700', size=6, symbol='diamond')))
    
    fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC, sans-serif", color='#e2e8f0', size=13), linecolor='rgba(0,243,255,0.2)', gridcolor='rgba(0,243,255,0.15)')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=35, r=35, t=20, b=20), height=300)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🎛️ 业务风控与决策仪表</h4>", unsafe_allow_html=True)
    p_score = -res.get("J", 0) 
    s_score = res.get("S", 0)
    risk_score = max(5, min(95, 50 + (p_score * 1.5) - (s_score * 1.5)))
    
    if risk_score < 35: r_tag, r_color, r_desc = "绝对合规与风控导向", "#4ade80", "行事极度稳健，对合规红线有天然敬畏，适合把守数据存证与风控大门，是交易所的底层装甲。"
    elif risk_score < 65: r_tag, r_color, r_desc = "动态创新与合规平衡", "#ffd700", "能够在监管框架与商业诉求间寻求最优解，适合主导数据产品架构与跨部门业务统筹。"
    else: r_tag, r_color, r_desc = "极致扩张与前沿开拓", "#f43f5e", "渴望打破旧有规则限制，拥有极强破坏性创新力，能快速抢占新兴生态阵地（需强力风控后台匹配）。"
    
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=risk_score, number={'suffix': "%", 'font': {'family': 'Orbitron, sans-serif', 'color': r_color, 'size': 38}}, title={'text': f"<span style='color:{r_color}; font-size:15px; font-family:Noto Sans SC;'>{r_tag}</span>"}, gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155"}, 'bar': {'color': r_color}, 'bgcolor': "rgba(255,255,255,0.05)", 'steps': [{'range': [0, 35], 'color': "rgba(74, 222, 128, 0.15)"}, {'range': [35, 65], 'color': "rgba(255, 215, 0, 0.15)"}, {'range': [65, 100], 'color': "rgba(244, 63, 94, 0.15)"}]}))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#94a3b8"}, height=240, margin=dict(l=20, r=20, t=30, b=0))
    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"<div style='color:#e2e8f0 !important; font-size:13px; text-align:center; margin-top:-20px; margin-bottom:25px; padding:0 10px;'>{r_desc}</div>", unsafe_allow_html=True)

    st.markdown("<h4 style='color:#10b981 !important; border-left:4px solid #10b981; padding-left:10px; font-weight:900;'>💡 组织生态赋能指南</h4>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, rgba(16, 185, 129, 0.08), rgba(0,0,0,0)); border-left: 4px solid #10b981; padding: 20px; border-radius: 8px; font-size: 14px; line-height: 1.7; color: #e2e8f0 !important; border-top: 1px solid rgba(16, 185, 129, 0.3); border-bottom: 1px solid rgba(16, 185, 129, 0.3); box-shadow: 0 5px 20px rgba(0,0,0,0.5); margin: 15px 0 30px 0;'>
        <div style='color: #34d399 !important; font-weight: 900; font-size: 13px; margin-bottom: 8px; font-family: "Orbitron", sans-serif !important; letter-spacing: 1px;'>[ 黄金生态协作节点 ]</div>
        <div style='margin-bottom:15px; color:#ffffff !important; font-weight:900; font-size:15px;'>{data['partner']}</div>
        <div style='color: #34d399 !important; font-weight: 900; font-size: 13px; margin-bottom: 8px; font-family: "Orbitron", sans-serif !important; letter-spacing: 1px;'>[ 高阶算力提升指令 ]</div>
        <div>{data['advice']}</div>
    </div>
    """, unsafe_allow_html=True)

    time_taken = st.session_state.end_time - st.session_state.start_time
    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>💠 专属职场数字标识</h4>", unsafe_allow_html=True)
    hash_code = hashlib.sha256(f"{st.session_state.user_alias}{mbti}{time_taken}".encode()).hexdigest()[:12].upper()
    share_card = f"""【SDE 人才能力图谱解析报告】
============================
◈ 授权节点：{st.session_state.user_alias}
◈ 特征序列：{mbti} ({data['role'].split(' / ')[0]})
◈ 核心素质：{' · '.join(data['tags'])}
◈ 决策偏好：{r_tag}
============================
全息校验码：0x{hash_code}
（解码职场潜能，驱动要素未来）"""
    st.markdown(f"<div style='background:#050a15; padding:20px; border-radius:8px; font-family:\"Noto Sans SC\", monospace; font-size:13px; color:#ffffff !important; border:1px solid #00f3ff; box-shadow:0 0 20px rgba(0,243,255,0.15); white-space:pre-wrap; line-height:1.6;'>{share_card}</div>", unsafe_allow_html=True)
    
    st.caption("☝️ 点击右上方复制按钮，或长按文本区发至微信分享你的专属图谱。")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("重启引擎系统 RESET()", type="primary", use_container_width=True):
        st.session_state.started = False
        st.session_state.current_q = 0
        st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
        st.session_state.start_time = None
        st.session_state.end_time = None
        st.session_state.calculating = False
        st.session_state.firework_played = False
        st.session_state.user_alias = "SDE_NODE"
        st.rerun()

st.markdown("""
    <div style='text-align:center; margin-top:50px; margin-bottom:20px; font-family:\"Orbitron\", monospace;'>
        <div style='color:#00f3ff !important; font-size:10px; opacity:0.5; letter-spacing:2px; margin-bottom:5px;'>
            POWERED BY DATA ELEMENT ENGINE
        </div>
        <div style='color:#ffd700 !important; font-size:12px; font-weight:900; letter-spacing:3px; text-shadow:0 0 15px rgba(255,215,0,0.6);'>
            © 版权归属无名逆流所有
        </div>
    </div>
""", unsafe_allow_html=True)
