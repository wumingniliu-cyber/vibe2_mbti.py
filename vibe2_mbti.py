import streamlit as st
import random
import time
import math
import hashlib
import html
import plotly.graph_objects as go

# --- 1. 页面与全局配置 ---
st.set_page_config(
    page_title="SDE 核心人才算力引擎 | MATRIX",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 赛博朋克级 UI 引擎 (包含 Glitch 与 终端自检特效) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Orbitron:wght@400;500;700;900&display=swap');

    /* 1. 终极锁死全局深网背景 */
    html, body, [class*="css"], .stApp { 
        background-color: #030712 !important; 
        font-family: 'Noto Sans SC', sans-serif !important;
        color: #f8fafc !important;
    }
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: transparent !important;
    }
    
    /* 2. 全局 CRT 扫描线与星网背景 (赛博质感核心) */
    [data-testid="stAppViewContainer"]::after {
        content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
        background-size: 100% 3px, 3px 100%;
        z-index: 99999; pointer-events: none; opacity: 0.6;
    }
    [data-testid="stAppViewContainer"] {
        background-image: 
            radial-gradient(circle at 50% 0%, #0f172a 0%, #030712 80%),
            linear-gradient(0deg, rgba(0,243,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px) !important;
        background-size: 100% 100%, 40px 40px, 40px 40px !important;
    }
    .stMarkdown, p, span, h2, h3, h4, li, div { color: #f8fafc !important; }
    
    /* 3. 进度条赛博化接管 */
    [data-testid="stProgress"] > div > div > div {
        background-color: #00f3ff !important;
        box-shadow: 0 0 15px rgba(0,243,255,0.8);
    }
    
    /* 4. Glitch 故障风主标题 */
    .hero-title { 
        font-size: 42px !important; font-weight: 900 !important; text-align: center; 
        color: #ffffff !important; letter-spacing: 4px; margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(0,243,255,0.8), 0 0 40px rgba(0,243,255,0.4);
        position: relative; display: inline-block;
    }
    .hero-title::before, .hero-title::after {
        content: attr(data-text); position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: transparent;
    }
    .hero-title::before { left: 2px; text-shadow: -2px 0 #f43f5e; animation: glitch-anim-1 2s infinite linear alternate-reverse; }
    .hero-title::after { left: -2px; text-shadow: 2px 0 #00f3ff; animation: glitch-anim-2 3s infinite linear alternate-reverse; }
    
    @keyframes glitch-anim-1 { 0% { clip-path: inset(20% 0 80% 0); } 20% { clip-path: inset(60% 0 10% 0); } 40% { clip-path: inset(40% 0 50% 0); } 60% { clip-path: inset(80% 0 5% 0); } 80% { clip-path: inset(10% 0 70% 0); } 100% { clip-path: inset(30% 0 20% 0); } }
    @keyframes glitch-anim-2 { 0% { clip-path: inset(10% 0 60% 0); } 20% { clip-path: inset(30% 0 20% 0); } 40% { clip-path: inset(70% 0 10% 0); } 60% { clip-path: inset(20% 0 50% 0); } 80% { clip-path: inset(90% 0 5% 0); } 100% { clip-path: inset(50% 0 30% 0); } }
    
    .hero-subtitle { text-align: center; color: #00f3ff !important; font-size: 13px; letter-spacing: 6px; opacity: 0.9; margin-bottom: 30px; font-family: 'Orbitron', sans-serif !important; font-weight: 700; }
    
    /* 5. 终端缓慢展开自检特效 (Terminal Boot) */
    .terminal-container {
        background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: 25px; 
        border-radius: 12px; font-family: 'Orbitron', monospace; font-size: 14px; color: #e2e8f0; 
        box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px;
    }
    .term-line { opacity: 0; margin-bottom: 5px; }
    .term-line:nth-child(1) { animation: scanFade 0.2s 0.2s forwards; }
    .term-line:nth-child(2) { animation: scanFade 0.2s 1.0s forwards; }
    .term-line:nth-child(3) { animation: scanFade 0.2s 1.8s forwards; }
    .term-line-main { opacity: 0; animation: scanFade 0.5s 2.6s forwards; }
    @keyframes scanFade { 0% { opacity: 0; transform: translateX(-10px); filter: blur(2px); } 100% { opacity: 1; transform: translateX(0); filter: blur(0); } }
    
    /* 闪烁光标 */
    .cursor-blink { display: inline-block; width: 8px; height: 16px; background: #00f3ff; animation: blink 1s step-end infinite; vertical-align: middle; margin-left: 5px; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

    /* 黑客风输入框 */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: rgba(2, 6, 23, 0.9) !important;
        color: #00f3ff !important; font-family: 'Orbitron', monospace !important;
        border: 1px solid rgba(0,243,255,0.5) !important; border-radius: 8px !important;
        text-align: center; font-size: 18px !important; font-weight: bold !important; letter-spacing: 2px;
        box-shadow: inset 0 0 15px rgba(0,243,255,0.1) !important; transition: all 0.3s ease;
    }
    div[data-testid="stTextInput"] > div > div > input:focus {
        border-color: #ffd700 !important; box-shadow: 0 0 20px rgba(255,215,0,0.4), inset 0 0 15px rgba(255,215,0,0.2) !important;
    }

    /* 6. 选项按钮深度穿透 */
    div.stButton > button {
        background: #0f172a !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; 
        border-left: 4px solid rgba(0, 243, 255, 0.6) !important; border-radius: 8px !important; 
        min-height: 60px !important; width: 100% !important; padding: 12px 15px !important; text-align: left !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.6) !important; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button p { color: #ffffff !important; font-size: 15px !important; line-height: 1.5 !important; font-weight: 500 !important; }
    div.stButton > button:hover { 
        background: rgba(0, 243, 255, 0.15) !important; border-color: #00f3ff !important; border-left: 4px solid #00f3ff !important; 
        box-shadow: 0 0 20px rgba(0,243,255,0.3) !important; transform: translateX(4px) !important; 
    }
    div.stButton > button:active { transform: scale(0.98) !important; }

    /* 启动按钮颜色特异化 */
    div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #00f3ff, #0088ff) !important; border-left: none !important; text-align: center !important;
    }
    div.stButton > button[data-testid="baseButton-primary"] p { color: #030712 !important; font-weight: 900 !important; font-size: 16px !important; letter-spacing: 2px !important; }
    div.stButton > button[data-testid="baseButton-primary"]:hover { transform: translateY(-2px) scale(1.02) !important; box-shadow: 0 0 40px rgba(0,243,255,0.8) !important; }
    
    /* 7. 结果视窗与终端日志 */
    .result-card {
        padding: 40px 25px; border-radius: 16px; background: rgba(11, 17, 32, 0.95) !important; 
        border: 1px solid rgba(255,215,0,0.3); border-top: 6px solid #ffd700; 
        text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.8); margin-bottom: 30px;
    }
    .mbti-code { font-family: 'Orbitron', sans-serif !important; font-size: 80px; font-weight: 900; color: #ffd700 !important; line-height: 1.1; letter-spacing: 4px; text-shadow: 0 0 35px rgba(255,215,0,0.6); margin: 0;}
    .cli-box {
        background: #000000; border: 1px solid #334155; border-left: 4px solid #00f3ff;
        padding: 20px; border-radius: 8px; font-family: 'Orbitron', monospace; font-size: 13px;
        color: #4ade80; box-shadow: inset 0 0 20px rgba(0,243,255,0.1); margin-top: 50px; text-transform: uppercase;
    }

    /* 8. 性能优化版结算烟花 */
    .firework-center { position: fixed; top: 50%; left: 50%; z-index: 99998; pointer-events: none; font-weight: 900; font-family: 'Orbitron', sans-serif; color: #00f3ff; text-shadow: 0 0 20px #00f3ff, 0 0 40px #ffffff; animation: supernova 1.8s cubic-bezier(0.1, 0.9, 0.2, 1) forwards; will-change: transform, opacity;}
    @keyframes supernova { 0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; } 100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; filter: blur(2px);} }
</style>
""", unsafe_allow_html=True)

def trigger_supernova():
    html_str = ""
    symbols = ["1", "0", "SYS", "NODE", "HASH", "SYNC"]
    for _ in range(40): 
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(300, 1000)
        tx, ty = distance * math.cos(angle), distance * math.sin(angle)
        scale = random.uniform(1.0, 3.5)
        rot = random.randint(-360, 360)
        delay = random.uniform(0, 0.15)
        text = random.choice(symbols)
        html_str += f'<div class="firework-center" style="--tx:{tx}px; --ty:{ty}px; --s:{scale}; --rot:{rot}deg; animation-delay:{delay}s; font-size:{random.randint(14, 26)}px;">{text}</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 题库核心层 (消除 40 魔术数字自适应长短) ---
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

# --- 4. 赛博化画像数据库 ---
mbti_details = {
    "INTJ": {"role": "首席系统架构师", "desc": "数据要素世界的“造物主”，致力于构建严密的底层网络公理体系。", "tags": ["逻辑闭环", "顶层架构", "系统自信"], "partner": "ENTJ (强效执行节点) / INTP (极客算法节点)", "advice": "在构建宏大的底层规则架构时，请适当为业务部门预留“沙盒容错”空间；捕获一线的非结构化数据流，能让系统更具生命力。"},
    "INTP": {"role": "风控算法极客", "desc": "穿透数据迷雾，寻找复杂业务表象下的底层逻辑漏洞与算力平衡。", "tags": ["黑客思维", "算法驱动", "极致解构"], "partner": "INTJ (架构锚定节点) / ENTP (协议发散节点)", "advice": "尝试将你极其高维的理论模型降维封装，形成非技术节点也能读取的操作协议，让算力转化为具体的生产力。"},
    "ISTJ": {"role": "底层协议审查官", "desc": "数据流转的守夜人，你的标识本身就是安全、严谨、零失误的代名词。", "tags": ["绝对合规", "程序正义", "数据护法"], "partner": "ESTJ (指令推进节点) / ISFJ (存储保障节点)", "advice": "在死守数据合规防火墙的同时，面对狂飙突进的创新协议，试着用“如何安全桥接”来指导业务，成为创新的护航者。"},
    "ESTJ": {"role": "核心进程统帅", "desc": "无可争议的算力推进器，擅长将复杂的上层指令转化为绝对可执行的KPI模块。", "tags": ["强类型执行", "结果导向", "进程控制"], "partner": "ISTJ (协议审查节点) / ISTP (故障兜底节点)", "advice": "在下发高压任务指令时，适度向节点池释放“情绪奖励”。一个具备高容错和信任感的网络，比单纯的跑分目标更稳健。"},
    "INFJ": {"role": "生态进化先知", "desc": "具备极强的跨频段共情能力，能精准预判数据流转对未来文明产生的降维变革。", "tags": ["远见卓识", "底层使命", "人文波段"], "partner": "ENFJ (共识布道节点) / ENFP (火种广播节点)", "advice": "学会用精确的量化参数、合规协议来锚定你的宏大网络愿景。将“先知直觉”编译为具体的执行代码，提升物理层的说服力。"},
    "INFP": {"role": "共识价值主张官", "desc": "冷酷数据背后的灵魂捕捉者，擅长在机械网络中注入引人共鸣的数字信仰。", "tags": ["协议感召", "价值重塑", "网络粘合"], "partner": "ENFJ (外部护航节点) / ISFP (交互美学节点)", "advice": "在跨域算力博弈中，学会熟练调用“预算函数”和“转化漏斗”来捍卫你的核心价值，将柔性代码转化为硬性资产。"},
    "ENTJ": {"role": "域外拓荒领军人", "desc": "天生的矩阵建设者，在数据资源化的未授权区中展现极强的强制并网能力。", "tags": ["跨域吞噬", "战略铁腕", "极速成交"], "partner": "INTJ (算法智囊节点) / ISTP (底层攻坚节点)", "advice": "在极速扩展域外节点时，请时刻保持与中台风控引擎的数据握手。偶尔降频倾听合规警报，能避开隐蔽的系统级崩溃。"},
    "ENTP": {"role": "零日漏洞探索者", "desc": "交易规则的敏锐挑战者，致力于通过跨界思维寻找下一代资源流转协议范式。", "tags": ["模式重写", "溢出测试", "思维跳变"], "partner": "INTP (底层验证节点) / ESTP (前线收割节点)", "advice": "适当收敛你的无限递归思维，选择一个极具潜力的创新接口（如特定凭证），深度闭环跟进至最终交付，用编译结果验证前瞻。"},
    "ENFJ": {"role": "全域生态调度官", "desc": "网络的魅力枢纽，能通过卓越的协议协商能力，将不同频段的竞争方聚拢为集群。", "tags": ["集群控制", "温情指令", "利益协定"], "partner": "INFJ (深度嗅探节点) / ESFJ (局域协同节点)", "advice": "在分配算力与利益配额时，大胆引入不可篡改的智能合约与刚性指针，确保“生态和谐”建立在牢不可破的底层代码之上。"},
    "ENFP": {"role": "跨链资源大使", "desc": "充满感染力的生态脉冲，让每一场物理路演都转变为数据要素市场的狂热共识。", "tags": ["无限频段", "跨链纽带", "高频驱动"], "partner": "INFJ (导航纠偏节点) / INTJ (底层挂载节点)", "advice": "引入严密的日志追踪与时间戳管理。将你天马行空的脉冲信号，转化为可溯源的转化链路，大幅提升创新的商业估值。"},
    "ISFJ": {"role": "高级守备进程", "desc": "最坚韧的底层存储器，于无声处通过极致纠错支撑起整个算力集群的稳定运行。", "tags": ["绝对利他", "吞吐巅峰", "高可用节点"], "partner": "ESFJ (外部桥接节点) / ISTJ (协议审核节点)", "advice": "在完美支撑主线程高速运转之余，尝试向管理员提交针对冗余死循环的优化补丁。你的底层实操日志极具价值，应当被提权。"},
    "ESFJ": {"role": "前线桥接主管", "desc": "超级网关，擅长经营多维度的外部握手协议，是前线业务请求的最强负载均衡器。", "tags": ["高并发协作", "细粒度控制", "社会化路由"], "partner": "ISFJ (精细存储节点) / ESTJ (宏观调度节点)", "advice": "在维持复杂的外部网络心跳时，建立更强硬的拦截防火墙，在响应外部请求的同时，保持对本地核心底线的绝对清醒。"},
    "ISTP": {"role": "危机熔断极客", "desc": "只对二进制事实和底层堆栈负责，是系统面临毁灭性拥堵或崩溃时的定海神针。", "tags": ["极简执行", "熔断直觉", "硬核堆栈"], "partner": "ESTP (实战突击节点) / INTP (算法重构节点)", "advice": "尝试将你极度内隐的故障排除脚本，沉淀为可视化的系统白皮书。打破接口调用壁垒，将个体的技术权限赋能给整个网络集群。"},
    "ISFP": {"role": "全息交互设计师", "desc": "赋予枯燥进制数据以美学权重，致力于提升数字资产在终端渲染时的绝对视觉压制。", "tags": ["审美溢价", "感官渲染", "独立纯粹"], "partner": "ESFP (公域广播节点) / INFP (共情叙事节点)", "advice": "在追求终端渲染的美学溢价时，适度挂载对核心业务逻辑和底层交易协议的读取权限，这会让你的UI拥有直击商业痛点的穿透力。"},
    "ESTP": {"role": "红蓝对抗突击手", "desc": "数据流转的敏锐猎手，能极快捕捉到瞬息万变的算力红利与资源套利空间。", "tags": ["物理直觉", "零和博弈", "高频收割"], "partner": "ISTP (底层兜底节点) / ENTJ (矩阵统筹节点)", "advice": "在捕捉瞬时算力爆发、展现高效抢占动作时，务必将前置合规审查写入你的自动化脚本中，为强劲的业务冲刺装上安全制动阀。"},
    "ESFP": {"role": "外网广播代言人", "desc": "矩阵物理层形象代理，天生具备将极客协议降维解码为大众传播频段的转码天赋。", "tags": ["全域广播", "即时响应", "快乐信标"], "partner": "ISFP (视觉渲染节点) / ENFP (创意脉冲节点)", "advice": "花时间深潜读取数据要素的核心库与政策文件。将你的绝佳广播穿透力挂载于扎实的产业根基上，形成系统级不可剥夺的权威权重。"}
}

# --- 5. 无闪烁状态机与事件回调 (工程化极速响应) ---
for key, init_val in [
    ('started', False), ('current_q', 0), ('start_time', None), 
    ('end_time', None), ('calculating', False), ('user_alias', "SDE_NODE"),
    ('total_scores', {"E": 0, "S": 0, "T": 0, "J": 0}), ('firework_played', False)
]:
    if key not in st.session_state: st.session_state[key] = init_val

def start_assessment_callback():
    """回车登录绑定的原子回调，自带防 XSS"""
    alias = st.session_state.login_input.strip()
    st.session_state.user_alias = html.escape(alias) if alias else "SDE_NODE"
    st.session_state.started = True
    st.session_state.start_time = time.time()

def answer_callback(val, dim):
    """按钮事件回调：杜绝 rerun 导致的闪屏与连点 BUG"""
    st.session_state.total_scores[dim] += (val - 3)
    st.session_state.current_q += 1
    if st.session_state.current_q >= len(questions):
        st.session_state.end_time = time.time()
        st.session_state.calculating = True

# --- 6. 核心渲染路由引擎 ---
if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 震撼的 Glitch 故障重影标题
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 class="hero-title" data-text="上海数据交易所">上海数据交易所</h1><br>
            <h1 class="hero-title" data-text="算力图谱全息引擎" style="font-size:32px !important;">算力图谱全息引擎</h1>
            <div class="hero-subtitle">▶ SDE MATRIX V26.0_SECURE</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 纯正的赛博终端逐字开机揭秘特效
    st.markdown("""
    <div class='terminal-container'>
        <div class='term-line'><span style='color:#94a3b8;'>[SYSTEM]</span> Establishing secure neural-link to SDE Core...</div>
        <div class='term-line'><span style='color:#94a3b8;'>[SYSTEM]</span> Loading Capability Matrix Algorithm... <span style='color:#00f3ff;'>[OK]</span></div>
        <div class='term-line'><span style='color:#10b981;'>[AUDIT]</span> Initializing Data Compliance Firewall... <span style='color:#00f3ff;'>[OK]</span></div>
        <div class='term-line-main'>
            <span style='color:#ffffff; font-size: 15px; font-family: "Noto Sans SC", sans-serif; line-height: 1.8;'>
            <br><b>2026年是数据要素价值释放的突破之年。</b><br><br>
            在“数据乘数”加速赋能实体经济的当下，合规红线与业务创新必须同频共振。<br>
            本全息终端将深度扫描您的底层能力架构、风控决策树与生态协同网络，为您生成独一无二的职场物理算力标识。</span>
            <span class="cursor-blink"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 采用 st.form，完美支持用户按下 回车键 (Enter) 登录提交
    with st.form(key="login_form", border=False):
        st.markdown("<div style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:bold; margin-bottom:5px; text-align:center;'>▼ MOUNT NODE ALIAS (挂载节点授权代号) ▼</div>", unsafe_allow_html=True)
        st.text_input("", key="login_input", placeholder="e.g. Director_Wu", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        st.form_submit_button("▶ 授予系统权限并执行深度扫描", on_click=start_assessment_callback, type="primary", use_container_width=True)
    
    st.markdown("<div style='text-align:center; color:#475569; font-size:11px; margin-top:40px; font-family:monospace;'>END-TO-END ENCRYPTED · AUDIT TRAIL ENABLED</div>", unsafe_allow_html=True)

elif st.session_state.calculating:
    # 终端黑客解码页
    st.markdown("<h2 class='hero-title' data-text='[ SYSTEM DECODING ]' style='font-size:32px !important; margin-top:50px;'>[ SYSTEM DECODING ]</h2>", unsafe_allow_html=True)
    terminal = st.empty()
    
    logs = [
        f"VERIFYING NODE: {st.session_state.user_alias.upper()}...",
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
    
    # 全新升级的赛博科幻维度分类
    dim_map = {
        "E": "[通信链路] 外部泛化传播 vs 内网深潜运算", 
        "S": "[感知雷达] 底层颗粒实勘 vs 宏观拓扑推演", 
        "T": "[算力引擎] 冰冷逻辑刚性 vs 生态价值共情", 
        "J": "[治理架构] 秩序刚性锁定 vs 动态混沌沙盒"
    }
    module_name = dim_map.get(q_data['dim'], "特征算力提取 (CORE_EXTRACTION)")
    
    # 修复 Hash 随重绘跳变：采用绑定题目内容的稳定种子生成哈希
    stable_hash_str = f"BLOCK_{st.session_state.current_q}_{q_data['q']}"
    dynamic_hash = hashlib.sha256(stable_hash_str.encode()).hexdigest()[:10].upper()
    
    st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
    
    progress_val = (st.session_state.current_q + 1) / len(questions)
    st.progress(progress_val)
    st.markdown(f"<div style='text-align:right; font-family:Orbitron, monospace; color:#00f3ff; font-size:12px; margin-top:5px;'>SYS_MEM_ALLOC: {int(progress_val*100)}%</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: rgba(2, 6, 23, 0.85); border: 1px solid rgba(0, 243, 255, 0.4); border-radius: 4px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 15px rgba(0, 243, 255, 0.05); margin-top: 15px; margin-bottom: 25px; border-left: 5px solid #00f3ff; backdrop-filter: blur(5px);'>
        <div style='display:flex; justify-content:space-between; font-family:monospace; color:#00f3ff; font-size:12px; margin-bottom:15px; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom:10px;'>
            <span class='orbitron-font'>▶ SYS_MOD: {module_name}</span>
            <span class='orbitron-font'>HASH: 0x{dynamic_hash}</span>
        </div>
        <div style='font-size: 17px; color: #ffffff !important; line-height: 1.6; font-weight: 500;'>
            {q_data['q']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 深度契合矩阵黑客语境的进程级选项文案
    opts = [
        ("❌ [ ERR_REJECT ] 强制阻断 / 完全背离底层直觉", 1),
        ("⚠️ [ LOW_SYNC ] 弱态耦合 / 偏离常规执行轨道", 2),
        ("⏳ [ SYS_AWAIT ] 线程挂起 / 视动态环境变量而定", 3),
        ("🔗 [ HIGH_SYNC ] 逻辑共振 / 高度拟合主决策树", 4),
        ("🔒 [ SYS_LOCK ] 绝对同步 / 强制锁死为最高优先级", 5)
    ]
    
    # 采用 on_click 模式，彻底告别由于 st.rerun() 造成的按钮闪跳和误触
    for text, val in opts:
        st.button(
            text, 
            type="secondary", 
            key=f"q_{st.session_state.current_q}_{val}",
            on_click=answer_callback,
            args=(val, q_data['dim'])
        )

else:
    # 状态锁：确保烟花只播放一次，避免用户悬停图表时触发 Streamlit 重绘导致烟花重放
    if not st.session_state.firework_played:
        trigger_supernova()
        st.session_state.firework_played = True
        
    res = st.session_state.total_scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    data = mbti_details.get(mbti)
    safe_alias_final = st.session_state.user_alias.upper()
    
    st.markdown(f"""
    <div class="result-card">
        <div class="orbitron-font" style="font-size:13px; color:#94a3b8; letter-spacing:4px; margin-bottom:15px;">MATRIX DECODED SUCCESSFULLY</div>
        <div style="color:#00f3ff; font-family:'Orbitron', monospace; font-size:13px; margin-bottom:5px; border-bottom:1px dashed #334155; padding-bottom:10px; display:inline-block;">AUTH_NODE: {safe_alias_final}</div>
        <div class="mbti-code" style="margin-top:10px;">{mbti}</div>
        <div class="mbti-post">【 {data['role']} 】</div>
        <div style="color:#e2e8f0 !important; font-size:14px; line-height:1.8; margin-bottom:25px; font-weight:400; text-align:left; padding:0 10px;">{data['desc']}</div>
        <div>
            {" ".join([f'<span style="background:rgba(0, 243, 255, 0.1); color:#00f3ff !important; border:1px solid rgba(0,243,255,0.4); padding:5px 12px; border-radius:4px; font-size:12px; font-weight:700; margin:4px; display:inline-block; font-family:\'Noto Sans SC\', sans-serif;">{t}</span>' for t in data['tags']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🕸️ 核心算力拓扑矩阵</h4>", unsafe_allow_html=True)
    def get_intensity(score): return max(15, min(100, 50 + (score / (len(questions)/4) * 50)))
    val_E, val_I = get_intensity(res["E"]), 100 - get_intensity(res["E"])
    val_S, val_N = get_intensity(res["S"]), 100 - get_intensity(res["S"])
    val_T, val_F = get_intensity(res["T"]), 100 - get_intensity(res["T"])
    val_J, val_P = get_intensity(res["J"]), 100 - get_intensity(res["J"])
    
    # 图表也替换为赛博风表述
    categories = ['外网辐射(E)', '颗粒实勘(S)', '刚性算法(T)', '秩序引擎(J)', '内网深潜(I)', '拓扑推演(N)', '生态共情(F)', '混沌沙盒(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.1)', line=dict(color='rgba(0, 243, 255, 0.2)', width=8), hoverinfo='none'))
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=2.5), marker=dict(color='#ff003c', size=6, symbol='diamond')))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC, sans-serif", color='#e2e8f0', size=12), linecolor='rgba(0,243,255,0.2)', gridcolor='rgba(0,243,255,0.15)')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=40, r=40, t=20, b=20), height=300)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🎛️ 风险过载阈值仪</h4>", unsafe_allow_html=True)
    p_score = -res.get("J", 0)
    s_score = res.get("S", 0)
    risk_score = max(5, min(95, 50 + (p_score * 1.5) - (s_score * 1.5)))
    
    if risk_score < 35: r_tag, r_color, r_desc = "绝对合规与物理装甲", "#10b981", "运行极其稳健，对协议红线有天然敬畏，适合把守数据存证大门，是系统的物理装甲。"
    elif risk_score < 65: r_tag, r_color, r_desc = "动态演进与边界平衡", "#ffd700", "能够在监管锁死与商业吞吐间寻求黄金接口，适合主导跨协议数据路由与全网算力统筹。"
    else: r_tag, r_color, r_desc = "无界扩张与零日突破", "#f43f5e", "渴望绕过陈旧的系统进程，拥有高爆发性的破坏重组算力，能快速抢占域外节点。"
    
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=risk_score, number={'suffix': "%", 'font': {'family': 'Orbitron, sans-serif', 'color': r_color, 'size': 38}}, title={'text': f"<span style='color:{r_color}; font-size:15px; font-family:Noto Sans SC; font-weight:bold;'>{r_tag}</span>"}, gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155"}, 'bar': {'color': r_color}, 'bgcolor': "rgba(255,255,255,0.05)", 'steps': [{'range': [0, 35], 'color': "rgba(16, 185, 129, 0.15)"}, {'range': [35, 65], 'color': "rgba(255, 215, 0, 0.15)"}, {'range': [65, 100], 'color': "rgba(244, 63, 94, 0.15)"}]}))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#94a3b8"}, height=240, margin=dict(l=20, r=20, t=30, b=0))
    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"<div style='color:#cbd5e1 !important; font-size:13px; text-align:center; margin-top:-20px; margin-bottom:25px; padding:0 10px; line-height:1.6;'>{r_desc}</div>", unsafe_allow_html=True)

    st.markdown("<h4 style='color:#10b981 !important; border-left:4px solid #10b981; padding-left:10px; font-weight:900;'>💡 集群网络挂载指南</h4>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: linear-gradient(145deg, rgba(16, 185, 129, 0.08), rgba(0,0,0,0)); border-left: 4px solid #10b981; padding: 20px; border-radius: 4px; font-size: 14px; line-height: 1.7; color: #e2e8f0 !important; border-top: 1px solid rgba(16, 185, 129, 0.3); border-bottom: 1px solid rgba(16, 185, 129, 0.3); box-shadow: 0 5px 20px rgba(0,0,0,0.5); margin: 15px 0 30px 0;'>
        <div style='color: #10b981 !important; font-weight: 900; font-size: 13px; margin-bottom: 8px; font-family: "Orbitron", sans-serif !important; letter-spacing: 2px;'>[ 黄金并网节点 ]</div>
        <div style='margin-bottom:15px; color:#ffffff !important; font-weight:900; font-size:15px;'>{data['partner']}</div>
        <div style='color: #10b981 !important; font-weight: 900; font-size: 13px; margin-bottom: 8px; font-family: "Orbitron", sans-serif !important; letter-spacing: 2px;'>[ 算力超频补丁 ]</div>
        <div>{data['advice']}</div>
    </div>
    """, unsafe_allow_html=True)

    time_taken = st.session_state.end_time - st.session_state.start_time
    st.markdown("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>💠 专属神经公钥下发</h4>", unsafe_allow_html=True)
    hash_code = hashlib.sha256(f"{safe_alias_final}{mbti}{time_taken}".encode()).hexdigest()[:16].upper()
    
    share_card = f"""【SDE MATRIX 核心算力链路解析】
=================================
◈ 挂载节点：{safe_alias_final}
◈ 协议序列：{mbti} ({data['role'].split(' / ')[0]})
◈ 核心指令：{' · '.join(data['tags'])}
◈ 熔断阈值：{r_tag}
=================================
链上校验码：0x{hash_code}
(解码底层物理逻辑，驱动数据要素未来)"""
    
    st.markdown(f"<div style='background:rgba(0,0,0,0.6); padding:20px; border-radius:4px; font-family:\"Noto Sans SC\", monospace; font-size:13px; color:#ffffff !important; border:1px solid #00f3ff; box-shadow:0 0 20px rgba(0,243,255,0.1) inset; white-space:pre-wrap; line-height:1.6;'>{share_card}</div>", unsafe_allow_html=True)
    st.caption("☝️ 点击右上方复制图标，发至局域网（微信）寻找你的协同节点。")

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
            POWERED BY DATA ELEMENT KERNEL
        </div>
        <div style='color:#00f3ff !important; font-size:10px; opacity:0.2; letter-spacing:2px;'>
            GITHUB RELEASE SECURE BUILD
        </div>
    </div>
""", unsafe_allow_html=True)
