import streamlit as st
import time
import random

# --- 1. 页面与官方主题强制配置 ---
st.set_page_config(page_title="SDE 数据要素菁英图谱", page_icon="📊", layout="centered")

# --- 2. 注入 SDE 专属：高对比度 & 强制亮色主题 CSS ---
st.markdown("""
<style>
    /* 强制锁定亮色主题背景，防止手机深色模式干扰导致字看不清 */
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    
    /* 强制所有文本为深色 */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp span, .stApp div {
        color: #1e293b !important;
    }
    
    /* 选项按钮：自适应高度，强化点击反馈，删除 height 参数改用 CSS 模拟 */
    div.stButton > button {
        height: auto !important; min-height: 100px !important;
        font-size: 15px !important; border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important; background-color: #ffffff !important;
        color: #0f172a !important; transition: all 0.2s ease !important;
        white-space: normal !important; padding: 15px 20px !important;
        text-align: left !important; line-height: 1.6 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    div.stButton > button:hover {
        border-color: #1e3c72 !important; background-color: #eff6ff !important;
        transform: translateY(-2px) !important; box-shadow: 0 4px 12px rgba(30, 60, 114, 0.15) !important;
    }
    
    /* 结果大卡片：白底金边，极致清晰 */
    .result-card {
        padding: 40px 20px; border-radius: 20px; background: #ffffff; 
        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border-top: 6px solid #1e3c72; border-bottom: 6px solid #d4af37;
        margin-bottom: 25px; animation: fadeIn 0.8s ease-out;
    }
    .mbti-text { font-size: 80px; font-weight: 900; margin: 0; color: #1e3c72 !important; letter-spacing: 2px; }
    .mbti-role { font-size: 26px; font-weight: bold; margin-bottom: 10px; color: #d4af37 !important; }
    
    /* 能量条样式 */
    .bar-container { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; font-size: 14px; font-weight: bold; }
    .bar-bg { flex-grow: 1; height: 12px; background-color: #e2e8f0; border-radius: 6px; margin: 0 15px; overflow: hidden; display: flex;}
    .bar-fill-left { height: 100%; background: linear-gradient(90deg, #1e3c72, #3b82f6); }
    .bar-fill-right { height: 100%; background: linear-gradient(90deg, #d4af37, #fbbf24); }
    
    .advice-box { padding: 20px; background-color: #ffffff !important; border-radius: 12px; border-left: 5px solid #d4af37; margin-top: 10px; font-size: 15px; line-height: 1.8; box-shadow: 0 2px 8px rgba(0,0,0,0.04); color: #334155 !important;}
    
    /* 666 特效动画 */
    .effect-666 { position: fixed; font-weight: 900; background: -webkit-linear-gradient(45deg, #1e3c72, #d4af37); -webkit-background-clip: text; -webkit-text-fill-color: transparent; z-index: 9999; animation: floatUp 3s ease-out forwards; pointer-events: none;}
    @keyframes floatUp { 0% { bottom: -10%; opacity: 1; transform: translateY(0) scale(0.5); } 100% { bottom: 110%; opacity: 0; transform: translateY(-100px) scale(1.5); } }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

def trigger_666_effect():
    html_str = ""
    for _ in range(66): 
        left = random.randint(5, 95)
        delay = random.uniform(0, 2.0)
        size = random.randint(25, 70)
        html_str += f'<div class="effect-666" style="left: {left}%; animation-delay: {delay}s; font-size: {size}px;">666</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 32道 SDE 全场景题库 (审计通过版) ---
questions = [
    # E-I 维度 (能量与沟通)
    {"q": "1. 参加数商生态交流会时，你的状态通常是：", "A": ("主动穿梭在各企业代表间，乐于建立新的业务连接", "E"), "B": ("倾向于深度观察，只在遇到真正感兴趣的项目时才切入交流", "I")},
    {"q": "2. 面对跨部门的业务协同（如交易运营与技术对接），你倾向于：", "A": ("直接发起碰头会或线下沟通，通过实时互动解决分歧", "E"), "B": ("先通过文档梳理需求，确保思考周全后再同步", "I")},
    {"q": "3. 结束了一周高强度的数据产品路演活动，周末你如何回血：", "A": ("约上朋友探店或运动，通过社交恢复精力", "E"), "B": ("宅在家中整理思绪，享受安静的私人时间", "I")},
    {"q": "4. 当你在公开场合代表交易所进行业务推介或汇报时：", "A": ("能够迅速进入状态，享受在聚光灯下表达的过程", "E"), "B": ("会做极其充分的幕后准备，认为内容扎实最重要", "I")},
    {"q": "5. 对于“头脑风暴”式的内部讨论会，你的看法是：", "A": ("非常欢迎，即时讨论常能碰撞出意想不到的业务火花", "E"), "B": ("略感疲惫，更习惯于在安静的环境下独立打磨方案", "I")},
    {"q": "6. 在办公室里，你更偏好哪种协作氛围：", "A": ("开放式、随处可见的沟通与共创，信息高度透明", "E"), "B": ("有专注空间的、相互尊重的沉浸式办公", "I")},
    {"q": "7. 当有新数商入驻需要提供引导咨询时：", "A": ("能迅速与对方建立联结，通过热情接待建立第一好感", "E"), "B": ("更倾向于提供专业、冷静的合规指引或操作手册", "I")},
    {"q": "8. 你更喜欢哪种工作方式：", "A": ("多线并行，频繁与不同背景的人交换信息", "E"), "B": ("单点突破，长时间专注于解决一个复杂的业务难题", "I")},

    # S-N 维度 (信息处理与视野)
    {"q": "9. 在评估一个初创数据产品上架时，你首先看重：", "A": ("数据源的真实性、清洗粒度和接口稳定性等技术细节", "S"), "B": ("该产品在产业链中的潜在应用场景和对行业的增量价值", "N")},
    {"q": "10. 研究“数据产权与数据知识产权”时，你的切入点是：", "A": ("现行法律框架下的确权流程、存证证据链等实操环节", "S"), "B": ("两种权利在数据资产价值分配机制中的长远博弈", "N")},
    {"q": "11. 面对海量的数据要素政策文件，你会：", "A": ("圈出其中的具体指标、红线要求和操作细则", "S"), "B": ("挖掘政策背后的导向逻辑，预判未来两年的产业风向", "N")},
    {"q": "12. 你更钦佩哪种类型的职业专家：", "A": ("在合同管理规范或清算结算等领域做到零差错的专业工匠", "S"), "B": ("能提出突破性交易模式，引领行业规则重构的战略极客", "N")},
    {"q": "13. 推进“数据资产入表”业务时，你认为关键在于：", "A": ("会计准则的对标、估值方法的准确性和报表调整", "S"), "B": ("数据资产化对企业估值体系的重塑及其长期意义", "N")},
    {"q": "14. 在进行业务规划时，你倾向于：", "A": ("参考过往成功的交易案例和已验证的运营经验", "S"), "B": ("寻找市场上尚未出现的空白点，尝试前人未竟的创新", "N")},
    {"q": "15. 如果要向市局领导汇报风险控制规则，你认为：", "A": ("清晰的排查矩阵、具体的整改案例和量化指标最有力", "S"), "B": ("风险防控的整体理念、演进路径和安全发展的愿景", "N")},
    {"q": "16. 描述上海数据交易所的愿景，你脑海中的画面是：", "A": ("一个流程标准化、交易合规化、效率极高的基础设施", "S"), "B": ("一个引领全球数字经济规则、释放全社会数据价值的引擎", "N")},

    # T-F 维度 (决策与价值判断)
    {"q": "17. 当业务需求与合规标准发生冲突时，你会：", "A": ("坚持原则与制度，认为合规底线是不可逾越的生命线", "T"), "B": ("寻找动态平衡点，通过合规优化支撑业务的创新诉求", "F")},
    {"q": "18. 在团队复盘会上，你倾向于：", "A": ("直接剖析流程缺陷，指出责任归属，以期最快解决", "T"), "B": ("关注成员状态，肯定大家的付出，在和谐氛围中总结", "F")},
    {"q": "19. 评估一个数商的入驻申请时，你认为最重要的标准是：", "A": ("企业的资质证明、技术能力以及合规记录等硬指标", "T"), "B": ("企业与交易所生态的契合度及对行业的正向影响", "F")},
    {"q": "20. 当你发现系统规则存在缺陷但尚未造成损失时：", "A": ("立刻按程序上报并申请冻结相关操作，即便暂时影响业务", "T"), "B": ("私下联系相关方先做补救，尽量柔性处理", "F")},
    {"q": "21. 给高管汇报时，你希望得到的评价是：", "A": ("“逻辑严密，论证扎实，决策模型非常专业。”", "T"), "B": ("“富有感染力，充分考虑了多方利益，能达成共识。”", "F")},
    {"q": "22. 下属因处理数据资产凭证发放业务失误时，你会：", "A": ("分析失误原因，重构操作手册，确保不再发生", "T"), "B": ("关注对方的抗压状态，给予情感上的疏导", "F")},
    {"q": "23. 讨论“数据红利分配”时，你更关注：", "A": ("收益分配比例的测算、贡献度的量化及合同履约率", "T"), "B": ("分配机制的公平性、对中小微企业的扶持及社会认同", "F")},
    {"q": "24. 你认为交易所职场中最核心的素养是：", "A": ("客观、理性的职业操守，以及对规则的绝对忠诚", "T"), "B": ("理解、共情的协作精神，以及对行业生态的关怀", "F")},

    # J-P 维度 (执行与节奏)
    {"q": "25. 面对一项紧急的政策起草任务：", "A": ("设定严格的倒排时间表，各环节严丝合缝地分阶段完成", "J"), "B": ("保持高度灵活性，随着调研深入动态调整方案重点", "P")},
    {"q": "26. 你的办公习惯更接近：", "A": ("坚持“今日事今日毕”，喜欢清单被逐项划掉的掌控感", "J"), "B": ("习惯于“截止日期（DDL）”前的高产，享受灵感迸发", "P")},
    {"q": "27. 处理交易所的合同管理或归档工作时：", "A": ("遵循严密的目录索引体系，确保任何文档都能快速定位", "J"), "B": ("虽然索引随性，但在需要时总能凭借联想找到材料", "P")},
    {"q": "28. 如果本周的工作议程临时发生了重大调整：", "A": ("会感到焦虑，必须重新调整所有后续安排", "J"), "B": ("觉得很有挑战性，乐于在不确定性中寻找机会点", "P")},
    {"q": "29. 准备向总工汇报技术架构方案前，你通常：", "A": ("反复校对每一个细节，确保内容持续可控、无懈可击", "J"), "B": ("保留一定的开放式话题，准备根据互动即兴发挥", "P")},
    {"q": "30. 对于“交易系统风控规则”的排查工作，你倾向于：", "A": ("建立标准化的排查矩阵，按部就班地进行全盘扫描", "J"), "B": ("凭借丰富的实战直觉，优先测试最容易出漏洞的模块", "P")},
    {"q": "31. 在日常团队管理中，你希望：", "A": ("每个环节都有章可循，工作流程像精密钟表一样运行", "J"), "B": ("鼓励自发性创新，给成员留出弹性的探索空间", "P")},
    {"q": "32. 在人生的重大决策面前：", "A": ("尽早确定目标并关闭其他选项，心无旁骛朝终点跑", "J"), "B": ("尽量保留多种可能性，在不断探索中等待契机", "P")}
]

# --- 4. MBTI 专业解析库 (建议岗位视角) ---
mbti_profiles = {
    "INTJ": {
        "role": "首席战略分析师 / 制度架构师",
        "desc": "极度理性，洞察本质。你不是在处理数据，而是在构建未来的制度文明。",
        "career": "在交易所最适合担任顶层制度规划、合规体系建设等中枢岗位。近期“数据产权与知识产权对比研究”正是你的主战场。",
        "partner": "最佳业务搭档：ENTJ（帮你强力推进蓝图落地）",
        "life": "建议设定强制的“离线时间”，远离政策和文档，通过硬核体能训练让大脑彻底放松。",
        "love": "你追求智力层面的极致共鸣。你对伴侣的最高赞赏是“你懂我的逻辑”。"
    },
    "INTP": {
        "role": "高级技术风控 / 数据产品专家",
        "desc": "天生奇才，解构主义。你能精准拆解任何看似完美的交易逻辑。",
        "career": "适合担任技术风控、数据产品架构优化等岗位。你对“系统规则缺陷”有着天然的嗅觉。",
        "partner": "最佳搭档：INTJ（把你的奇思妙想转化为体系）",
        "life": "记得按时吃饭，别在逻辑迷宫里走丢。偶尔尝试手作（如乐高），能给大脑回血。",
        "love": "感情对你是个黑盒。你理想的伴侣是能包容你偶尔“失联”的独立灵魂。"
    },
    "ISTJ": {
        "role": "合规审查官 / 清算结算专家",
        "desc": "零差错执行者。在数交所，你就是规则和契约的最后防线。",
        "career": "风控合规、合同管理、清算结算的绝对核心。你是栾宏冬局长或刘总工最放心的执行者。",
        "partner": "最佳搭档：ESTJ（你们的组合是执行力的天花板）",
        "life": "秩序感是你的能量，但偶尔的“失控”是最好的解药。去试试没做攻略的即兴旅行吧。",
        "love": "陪伴是最长情的告白。你会默默承包所有家务和琐碎，提供金石般的可靠。"
    },
    "ESTJ": {
        "role": "部门主管 / 业务流程专家",
        "desc": "铁腕推进，使命必达。没有你拿不下的数商，没有你推不动的政策。",
        "career": "适合前台业务开发、大型项目协调或行政管理。你是让数据要素真正“跑起来”的发动机。",
        "partner": "最佳搭档：ISTJ（他们能确保你的突击不越红线）",
        "life": "放过自己，生活不是 KPI。多给伴侣提供情感价值，而不仅仅是解决问题。",
        "love": "家庭对你是责任。试着在爱人面前卸下“总监”身份，展现你柔软的一面。"
    },
    "INFJ": {
        "role": "生态运营官 / 战略研究员",
        "desc": "愿景引领者。你关注的不仅仅是交易，而是数据如何改变社会。",
        "career": "适合战略研究、公共关系或生态运营。你能在跨部门摩擦中用情商和愿景化解冰霜。",
        "partner": "最佳搭档：ENFP（他们的热情能点燃你的深邃蓝图）",
        "life": "学会课题分离。数据交易所的合规压力是公司的，不是你个人的。保护好你的共情力。",
        "love": "渴望宿命般的爱恋。一旦认定，爱得深沉且绝不回头。你需要极高的情感浓度。"
    },
    "INFP": {
        "role": "品牌策划 / 组织文化专家",
        "desc": "温柔的理想主义者。在冰冷的数字面前，你坚信人性才是数据要素的终极注脚。",
        "career": "适合品牌宣贯、企业文化、人文类课题研究。你是让交易所具备温情的关键因子。",
        "partner": "最佳搭档：ENFJ（他们能给你极大的情感支持）",
        "life": "接纳“灰度”。用音乐和写作来安置你无处安放的才华。比如专门为爱人准备一首庆祝羁绊的歌。",
        "love": "你的爱是诗，是歌。你追求的是那种不被世俗定义的、极致纯粹的感情连接。"
    },
    "ENTJ": {
        "role": "首席业务官 / 项目合伙人",
        "desc": "生而为赢。在复杂的数据商业博弈中，你是那个能赢到最后的弈棋者。",
        "career": "适合担任部门负责人、核心项目主理。在争取政策支持时，你的压迫感就是战斗力。",
        "partner": "最佳搭档：INTJ（战略与执行的完美闭环）",
        "life": "尝试竞技体育。把在工作中的征服欲，通过出汗的方式在赛场上宣泄掉。",
        "love": "追求强强联手。你理想的伴侣是那个能在事业上给你启发、精神上势均力敌的战友。"
    },
    "ENTP": {
        "role": "产品创新专家 / 业务开发顾问",
        "desc": "不破不立。你的存在就是为了挑战那些陈旧、不合时宜的交易模式。",
        "career": "适合产品创新、业务开拓。只要不让你干重复性审批，你就是交易所的灵感之眼。",
        "partner": "最佳搭档：INTP（一起把旧系统的底裤看穿）",
        "life": "兴趣广泛是好事，但请找个 ISTJ 帮你理财。别让你的天才Idea因为琐碎细节而夭折。",
        "love": "爱情是智力游戏，也是新鲜感。你需要一个能接住你所有梗并陪你一起疯的人。"
    },
    "ENFJ": {
        "role": "数商关系主管 / 团队协调官",
        "desc": "共情与领导力的化身。你不是在管理，你是在点燃每位数商的激情。",
        "career": "适合数商生态服务、对外协调汇报。你是交易所最闪亮的名片，天生的外交家。",
        "partner": "最佳搭档：INFP（你能完美承接并落地他们的愿景）",
        "life": "停止照顾所有人。学会给自己留一点“自私”的时间，你的能量不是取之不尽的。",
        "love": "你是完美的爱人，能预判伴侣的所有需求。但也渴望被热烈地、具象地爱着。"
    },
    "ENFP": {
        "role": "市场拓展主管 / 创意策划人",
        "desc": "快乐修勾。哪里有你，哪里就有数据要素流通的无限可能性。",
        "career": "适合生态拓展、活动策划。你的热情能轻易撬动海量的外部资源，是业务的助推器。",
        "partner": "最佳搭档：INFJ（他们能看懂你天马行空背后的深意）",
        "life": "找个靠谱的朋友帮你做生活规划。保持你的好奇心，那是你最珍贵的资产。",
        "love": "容易一头扎进热恋，把生活过成电影。你需要一个既能陪你疯，又能拉住你风筝线的爱人。"
    },
    "ISFJ": {
        "role": "高级行政主管 / 运营支持",
        "desc": "温柔的基石。没有你在后台的精准操作，前台的交易就是空中楼阁。",
        "career": "适合合规审查、日常运营、行政事务。你是领导最放心、最省心的工作搭档。",
        "partner": "最佳搭档：ESFJ（你们组合能把一切安排得明明白白）",
        "life": "你的善良要带点锋芒。今天就推掉那个不属于你的麻烦事，给自己买顿大餐。",
        "love": "你的爱如春风化雨。你渴望的是那种细水长流、相濡以沫的传统式温情。"
    },
    "ESFJ": {
        "role": "客户成功主管 / 商务秘书",
        "desc": "人际关系大师。你能把复杂的部门关系和外部客户理得顺顺当当。",
        "career": "适合客服运营、商务支持、行政。你能敏锐察觉利益相关方诉求，是润滑剂。",
        "partner": "最佳搭档：ISFJ（双保守组合，确保业务稳健无虞）",
        "life": "摆脱“认可成瘾”。做一点不需要发朋友圈展示、纯粹让自己开心的事。",
        "love": "极致顾家。你会把伴侣介绍给所有朋友，希望爱情能被全世界见证和祝福。"
    },
    "ISTP": {
        "role": "技术运维专家 / 数据分析师",
        "desc": "硬核实干派。对于不合逻辑的流程，你只会祭出最锋利的重构方案。",
        "career": "适合技术运维、数据分析、危机处理。你是那个在突发状况下最冷静的硬汉。",
        "partner": "最佳搭档：ESTP（双实干组合，效率天花板）",
        "life": "去玩极限运动。通过这种纯粹的感官刺激，来疏解交易所高压的工作节奏。",
        "love": "爱是解决问题。你会修好家里所有的家电，但可能忘了说“我爱你”。"
    },
    "ISFP": {
        "role": "视觉设计师 / 交互体验师",
        "desc": "随性且精致。你致力于让枯燥的数据产品展示变得极具美感。",
        "career": "适合视觉设计、交互体验、品牌创意。你是让数交所展示变得高级的功臣。",
        "partner": "最佳搭档：ESFP（创意双子星，让业务变得有趣）",
        "life": "讨厌冲突。把办公环境布置得温馨惬意，那是你保护自己灵魂的阵地。",
        "love": "你是温柔的爱人。窝在沙发听歌、看电影，就是你最向往的恋爱时刻。"
    },
    "ESTP": {
        "role": "高级业务经理 / 市场开拓专家",
        "desc": "敏锐、果敢。在瞬息万变的市场中，你总是那个最先发现红利的人。",
        "career": "适合市场开拓、高频交易、风险投资。你天生就是吃业务这碗饭的。",
        "partner": "最佳搭档：ISTP（用最快的方式解决业务中的所有障碍）",
        "life": "别让自己停下来。多去接触不同领域的人。但要在合规和财务上留足安全垫。",
        "love": "魅力四射。追求激情，但也需要学会在平淡中找到长久相伴的真谛。"
    },
    "ESFP": {
        "role": "公共关系专家 / 活动主持",
        "desc": "天生耀眼。你是数交所发布会上最能调动气氛的那个人。",
        "career": "适合前台接待、活动主持、公关推广。你的快乐是整个团队的强心针。",
        "partner": "最佳搭档：ISFP（前台展现，后台支持，天作之合）",
        "life": "今朝有酒今朝醉。别去死磕那些无趣的理论，你的纯粹就是你的财富。",
        "love": "爱情必须是轰轰烈烈的。你要秀给全世界看，享受被宠爱的每一秒。"
    }
}

# --- 5. 状态管理 ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

def answer_clicked(dimension):
    st.session_state.scores[dimension] += 1
    st.session_state.current_q += 1

# --- 6. 核心渲染逻辑 ---
st.title("📊 SDE 数据要素菁英图谱")
st.markdown("<p style='color:#1e293b; font-size: 15px;'>专为上海数据交易所团队定制。请根据第一直觉作答。</p>", unsafe_allow_html=True)

total_q = len(questions)

if st.session_state.current_q < total_q:
    progress = st.session_state.current_q / total_q
    st.progress(progress)
    st.caption(f"深度扫描中: {st.session_state.current_q + 1} / {total_q}")
    st.markdown("<br>", unsafe_allow_html=True) 
    
    current_item = questions[st.session_state.current_q]
    st.markdown(f"<h4 style='color:#1e293b;'>{current_item['q']}</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True) 
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(current_item['A'][0], use_container_width=True):
            answer_clicked(current_item['A'][1])
            st.rerun()
    with col2:
        if st.button(current_item['B'][0], use_container_width=True):
            answer_clicked(current_item['B'][1])
            st.rerun()

else:
    st.progress(1.0)
    st.balloons()
    trigger_666_effect() 
    
    scores = st.session_state.scores
    mbti_result = ""
    mbti_result += "E" if scores["E"] >= scores["I"] else "I"
    mbti_result += "S" if scores["S"] >= scores["N"] else "N"
    mbti_result += "T" if scores["T"] >= scores["F"] else "F"
    mbti_result += "J" if scores["J"] >= scores["P"] else "P"
    
    profile_data = mbti_profiles.get(mbti_result, mbti_profiles["INTJ"]) 
    
    st.markdown(f"""
    <div class="result-card">
        <p style="margin:0; font-size: 16px; opacity: 0.8; letter-spacing: 2px; color: #64748b;">你的灵魂核心驱动</p>
        <p class="mbti-text">{mbti_result}</p>
        <p class="mbti-role">【 {profile_data['role']} 】</p>
        <p style="font-size: 16px; color: #334155;">"{profile_data['desc']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 性格能量面板")
    def draw_bar(left_label, left_score, right_label, right_score):
        left_pct = (left_score / 8) * 100
        right_pct = (right_score / 8) * 100
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; margin-bottom:5px; font-weight:bold; font-size:14px; color:#1e293b;'>
            <span>{left_label} ({left_score})</span>
            <span>{right_label} ({right_score})</span>
        </div>
        <div style='height:10px; background-color:#e2e8f0; border-radius:5px; margin-bottom:15px; display:flex; overflow:hidden;'>
            <div style='width:{left_pct}%; background-color:#1e3c72;'></div>
            <div style='width:{right_pct}%; background-color:#d4af37;'></div>
        </div>
        """, unsafe_allow_html=True)

    draw_bar("外向 (E)", scores["E"], "内向 (I)", scores["I"])
    draw_bar("实感 (S)", scores["S"], "直觉 (N)", scores["N"])
    draw_bar("思考 (T)", scores["T"], "情感 (F)", scores["F"])
    draw_bar("判断 (J)", scores["J"], "感知 (P)", scores["P"])
    
    st.markdown("### 🧭 SDE 专属进阶指南")
    tab1, tab2, tab3 = st.tabs(["💼 业务与搭档", "🌱 能量与生活", "❤️ 情感与羁绊"])
    
    with tab1:
        st.markdown(f"<div class='advice-box'><b>建议岗位：</b><br>{profile_data['role']}<br><br><b>核心发展：</b><br>{profile_data['career']}<br><br><b>🤝 职场搭档：</b><br>{profile_data.get('partner','团队核心成员')}</div>", unsafe_allow_html=True)
    with tab2:
        st.markdown(f"<div class='advice-box'><b>生活赋能：</b><br>{profile_data['life']}</div>", unsafe_allow_html=True)
    with tab3:
        st.markdown(f"<div class='advice-box'><b>情感密码：</b><br>{profile_data['love']}</div>", unsafe_allow_html=True)
    
    share_text = f"我在【上海数交所专属图谱】测出了【{mbti_result} {profile_data['role']}】！底色：{profile_data['desc']} 快来测测你的业务原力吧！"
    st.markdown(f"### 💌 专属社交名片\n<div style='padding:15px; background:#ffffff; border-radius:8px; font-family:monospace; font-size:13px; border:1px dashed #cbd5e1; color:#1e293b;'>{share_text}</div>", unsafe_allow_html=True)
    
    if st.button("🔄 重启沙盘测算", use_container_width=True):
        st.session_state.current_q = 0
        st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        st.rerun()

# --- 7. 专属底部署名 ---
st.markdown("""
    <div class="footer">
        Powered by 数据要素核心引擎<br>
        © 版权归属无名逆流所有
    </div>
""", unsafe_allow_html=True)