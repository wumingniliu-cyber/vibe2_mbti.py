import streamlit as st
import time
import random

# --- 1. 页面与官方主题强制配置 ---
st.set_page_config(page_title="SDE 数据要素菁英图谱", page_icon="📊", layout="centered")

# --- 2. 注入 SDE 专属：强制防劫持 CSS & UI 动效 ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    
    .stApp * { color: #1e293b; } /* 强制全局深色字体 */
    
    div.stButton > button {
        height: auto !important; min-height: 100px !important;
        font-size: 15px !important; border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important; background-color: #ffffff !important;
        color: #0f172a !important; transition: all 0.2s ease !important;
        white-space: normal !important; padding: 12px 18px !important;
        text-align: left !important; line-height: 1.6 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    }
    div.stButton > button:hover {
        border-color: #3b82f6 !important; background-color: #eff6ff !important;
        transform: translateY(-2px) !important; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
    }
    
    .result-card {
        padding: 40px 20px; border-radius: 16px; background: #ffffff; 
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border-top: 6px solid #1e3c72; border-bottom: 6px solid #d4af37;
        margin-bottom: 25px; animation: fadeIn 0.8s ease-out;
    }
    .mbti-text { font-size: 85px; font-weight: 900; margin: 0; color: #1e3c72 !important; letter-spacing: 2px; text-shadow: 2px 2px 0px rgba(30,60,114,0.1);}
    .mbti-role { font-size: 24px; font-weight: bold; margin-bottom: 15px; color: #d4af37 !important; }
    
    /* 自定义能量条样式 */
    .bar-container { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; font-size: 14px; font-weight: bold; }
    .bar-bg { flex-grow: 1; height: 12px; background-color: #e2e8f0; border-radius: 6px; margin: 0 15px; overflow: hidden; display: flex;}
    .bar-fill-left { height: 100%; background: linear-gradient(90deg, #3b82f6, #60a5fa); transition: width 1s ease-out;}
    .bar-fill-right { height: 100%; background: linear-gradient(90deg, #f59e0b, #fbbf24); transition: width 1s ease-out;}
    
    .advice-box { padding: 20px; background-color: #ffffff !important; border-radius: 10px; border-left: 5px solid #d4af37; margin-top: 10px; font-size: 14.5px; line-height: 1.7; box-shadow: 0 2px 8px rgba(0,0,0,0.03); color: #334155 !important;}
    
    .share-box { padding: 15px; background-color: #f1f5f9 !important; border-radius: 8px; font-family: monospace; font-size: 13px; color: #475569 !important; border: 1px dashed #cbd5e1; word-break: break-all; }
    
    .effect-666 { position: fixed; font-weight: 900; background: -webkit-linear-gradient(45deg, #1e3c72, #d4af37); -webkit-background-clip: text; -webkit-text-fill-color: transparent; z-index: 9999; animation: floatUp 3s ease-out forwards; pointer-events: none;}
    @keyframes floatUp { 0% { bottom: -10%; opacity: 1; transform: translateY(0) scale(0.5); } 100% { bottom: 110%; opacity: 0; transform: translateY(-100px) scale(1.5); } }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)

def trigger_666_effect():
    html_str = ""
    for _ in range(40): 
        left = random.randint(5, 95)
        delay = random.uniform(0, 1.2)
        size = random.randint(25, 55)
        html_str += f'<div class="effect-666" style="left: {left}%; animation-delay: {delay}s; font-size: {size}px;">666</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 题库区 (保持 32 题 SDE 专属沉浸式题库) ---
questions = [
    {"q": "1. 参加全球数据生态大会，中场休息时你通常会：", "A": ("主动交换名片，和各大数商、第三方机构热聊，越聊越兴奋", "E"), "B": ("找个清静的角落回回工作微信，或者只和同行的熟人交流", "I")},
    {"q": "2. 发现数字资产交易系统的风控规则存在缺陷时，你倾向于：", "A": ("立刻拉一个多部门的紧急碰头会，当面把事情对齐", "E"), "B": ("先梳理好缺陷逻辑和修改建议，发一封详尽的邮件给大家", "I")},
    {"q": "3. 结束了一周高强度跨部门研讨后，周末你更想：", "A": ("约朋友打球、聚餐，在热闹的人间烟火中释放压力", "E"), "B": ("关掉工作手机，一个人在家看书或看电影，享受绝对的独处", "I")},
    {"q": "4. 推动数据要素流通新业务落地，遇到业务部门阻力时，你会：", "A": ("直接走到对方工位上，通过高频、直接的语言沟通解决分歧", "E"), "B": ("通过文字留言或工作群，深思熟虑后再回复对方的质疑", "I")},
    {"q": "5. 对于所内关于“数据资产入表”的头脑风暴会，你的感受是：", "A": ("非常喜欢，别人的发言总能激发我源源不断的灵感", "E"), "B": ("有点耗能，我更喜欢在会前自己先思考出一个完整的框架", "I")},
    {"q": "6. 带领风控合规部进行团队建设时，你通常：", "A": ("主动承担活跃气氛的角色，在众人面前侃侃而谈", "E"), "B": ("做好幕后的统筹和支持，除非被点名，否则尽量不抢风头", "I")},
    {"q": "7. 在所内的 OA 系统或工作大群里，你的活跃度：", "A": ("极高，喜欢发声，经常抛出新话题或参与热烈讨论", "E"), "B": ("潜水为主，只在需要自己明确表态或处理具体事务时才发言", "I")},
    {"q": "8. 面对复杂的合规审查案卷，你更喜欢的办公环境是：", "A": ("开放式、充满交流声、随时可以拉人讨论的氛围", "E"), "B": ("安静、有隔断、没人打扰，能让我进入深度心流状态", "I")},
    {"q": "9. 在起草一份政策专报寻求监管支持时，你最看重：", "A": ("专报中的数据是否准确，法律条文引用是否无误，诉求是否具体可执行", "S"), "B": ("专报是否拔高到了全市乃至国家的数据要素战略高度，立意够不够深远", "N")},
    {"q": "10. 进行数据产权与数据知识产权的对比研究时，你的切入点是：", "A": ("对比现行法律条文的具体字眼，分析两者的确权流程和实操案例", "S"), "B": ("探讨这两种权利在未来数字经济底层架构中的哲学意义和演变趋势", "N")},
    {"q": "11. 评估一个新上架的数据产品时，你第一眼关注：", "A": ("数据来源是否合法，合规字段说明是否清晰，API接口是否稳定", "S"), "B": ("这个产品能组合出什么新玩法，它背后的商业模式有多大想象力", "N")},
    {"q": "12. 你更钦佩哪种交易所的专家：", "A": ("极其严谨务实，能把极其复杂的制度规范逐条落地，不留死角", "S"), "B": ("眼界极度开阔，满脑子都是颠覆性的数据流通新模式和新生态", "N")},
    {"q": "13. 面对国家出台的最新的数据要素指导意见，你会：", "A": ("仔细研读细则，对比旧规，圈出对当前业务有直接影响的条款", "S"), "B": ("思考政策背后的顶层设计逻辑，预判未来三年的行业风口在哪里", "N")},
    {"q": "14. 听取交易系统技术架构重构的汇报时，你容易对什么感到不耐烦：", "A": ("讲了半天概念和宏大愿景，却不告诉我下周到底要开发什么具体功能", "S"), "B": ("陷入了无休止的底层代码细节和微小技术参数里，看不到全局大图", "N")},
    {"q": "15. 解决数字资产交易中的风控“疑难杂症”时，你通常依赖：", "A": ("过往处理类似违规事件的积累经验和现有的制度汇编", "S"), "B": ("敏锐的直觉，尝试跳出既有框架，用全新的视角寻找破局点", "N")},
    {"q": "16. 描述上海数据交易所的愿景，你更喜欢哪种表达：", "A": ("成为日均交易额破百亿、挂牌产品超十万、风控制度最完善的机构", "S"), "B": ("成为全球数据要素流通的神经中枢，重塑数字时代的价值分配体系", "N")},
    {"q": "17. 业务部门为了冲业绩，想上架一款处于合规灰色地带的产品，作为把关人你会：", "A": ("不讲情面，严格按照管理规范和风控底线，坚决一票否决", "T"), "B": ("理解业务团队的压力，尽量帮他们寻找合规的替代方案，婉转驳回", "F")},
    {"q": "18. 在风控团队内部进行项目复盘时，你的侧重点是：", "A": ("剖析流程哪里出了漏洞，责任在谁，如何用制度避免下次再犯", "T"), "B": ("关注大家在项目中的情绪状态，肯定辛勤付出，维护团队和谐", "F")},
    {"q": "19. 发现优秀的同事在操作交易系统时出现违规，你会：", "A": ("公事公办，直接按流程上报并触发警报，维护系统的绝对公正", "T"), "B": ("先私下找他沟通，了解是否事出有因，尽量降低对他的负面影响", "F")},
    {"q": "20. 你认为构建良好“数据生态”的核心基石应该是：", "A": ("冰冷但严密的智能合约、确权规则和惩戒机制", "T"), "B": ("数商之间、政企之间的互信、合作共赢的理念和共识", "F")},
    {"q": "21. 向高管汇报风险控制规则缺陷时，你希望得到的评价是：", "A": ("“逻辑极其严密，数据支撑强悍，无懈可击。”", "T"), "B": ("“非常人性化，充分考虑了各方诉求，极具人情味。”", "F")},
    {"q": "22. 下属因为合规审查失误向你道歉，你脱口而出的是：", "A": ("“别纠结了，赶紧说说你打算怎么补救，下一步的 Action 是什么？”", "T"), "B": ("“没关系，谁都会犯错，你这几天压力太大了，先调整好情绪。”", "F")},
    {"q": "23. 探讨数据资产化对社会的意义时，你更关注：", "A": ("财务审计准则、估值模型和法律权属的清晰界定", "T"), "B": ("数据资产化对普通企业员工的福祉、以及深远的社会伦理影响", "F")},
    {"q": "24. 你认为在职场中最难能可贵的品质是：", "A": ("保持绝对的理智、客观，不被任何情绪裹挟", "T"), "B": ("保持极高的同理心、善良，始终带有人文关怀", "F")},
    {"q": "25. 牵头起草《上海数据交易所合同管理规范》时，你：", "A": ("先拉一个精确到天的甘特图，分配好各部门节点，严格按时间表推进", "J"), "B": ("先写个大致框架，在征求意见的过程中边走边看，随时准备大修大改", "P")},
    {"q": "26. 准备向数据局领导进行专项汇报时，你的状态是：", "A": ("提前几天就定稿汇报材料并反复演练，心无旁骛，确保持续可控", "J"), "B": ("保留到最后一刻再完善细节，随时根据领导的最新关注点灵活调整", "P")},
    {"q": "27. 你电脑里关于“数据产权”的研究资料通常是：", "A": ("层级分明，按年份、政策级别、作者分类得清清楚楚，强迫症福音", "J"), "B": ("全部堆在桌面或一个大文件夹里，靠搜索功能或者惊人的记忆力找东西", "P")},
    {"q": "28. 正在推进数据资产凭证发放业务，突然监管政策风向变了，你：", "A": ("感到非常难受和焦虑，因为这意味着我辛苦做的计划全部作废", "J"), "B": ("觉得反而兴奋，迅速抛弃旧方案，顺应新风向寻找新的突破口", "P")},
    {"q": "29. 结束了一天的数据交易审批离开公司，你的常态是：", "A": ("办公桌收拾得干干净净，明天的待办清单已经列好", "J"), "B": ("桌面上还摊着没看完的文件，随时准备明天无缝衔接继续干", "P")},
    {"q": "30. 排查数字资产交易系统风控规则的缺陷时，你通常：", "A": ("建立详尽的排查矩阵，按部就班地进行全盘扫描，不放过任何死角", "J"), "B": ("凭借直觉和丰富的经验，优先攻击和测试最容易出漏洞的薄弱模块", "P")},
    {"q": "31. 组织高级管理层进行制度研讨会，如果议程突然变动，你：", "A": ("迅速启动备用的 Plan B，确保会议流程不被打乱", "J"), "B": ("随遇而安，甚至即兴发挥，把突发状况变成新的讨论契机", "P")},
    {"q": "32. 在人生的重大选择上，你倾向于：", "A": ("尽早做出决断，一锤定音，然后坚定地朝前走绝不回头", "J"), "B": ("收集极其庞杂的信息，反复权衡，不到最后一刻很难下定决心", "P")}
]

# --- 4. 深度解析库 (融合极深业务绑定与搭档推荐) ---
mbti_profiles = {
    "INTJ": {
        "role": "架构师 | 顶层规则的缔造者",
        "desc": "极度理性，洞察本质。别人看到的是交易数据，你看到的是底层权属与制度的宏大蓝图。",
        "career": "天生的高阶智囊。近期开展数据产权与数据知识产权的深度对比研究，为你起草战略级规范建议提供了极佳弹药。你总能一眼看穿风控规则的逻辑硬伤，构建不可击破的合规护城河。",
        "partner": "最佳业务搭档：ENTJ（帮你强力推进制度落地）",
        "life": "建议设定绝对的“离线时间”，去接触纯物理层面的爱好，比如高强度的器械训练，让大脑强制关机。",
        "love": "智力上的势均力敌是唯一的门槛。当你在为了市局专报熬夜时，你不需要嘘寒问暖，只需要对方能懂你这份事业的战略价值。"
    },
    "INTP": {
        "role": "逻辑学家 | 系统漏洞的清道夫",
        "desc": "极客精神，剖析一切。剥开数据流通的表象，你是那个能重构整个风控逻辑代码的天才。",
        "career": "具备无与伦比的分析能力。极具适合钻研数字资产交易系统风控规则中的隐蔽缺陷。只要给你足够的自由，你能给出令人拍案叫绝的重构方案。",
        "partner": "最佳合规搭档：INTJ（懂你的逻辑，帮你构建体系）",
        "life": "记得按时吃饭，保持环境整洁。偶尔跳出信息茧房，去大自然中感受一下没有逻辑可言的美。",
        "love": "感情对你来说是一个难以用公式计算的难题。你理想的伴侣是能够包容你偶尔的“失联”，并能与你进行高质量精神对话的人。"
    },
    "ISTJ": {
        "role": "物流师 | 合规底线的铁壁垒",
        "desc": "严谨务实，不怒自威。在狂飙突进的数据产业里，你是交易所不可逾越的定海神针。",
        "career": "风控合规部的核心骨干。例如近期牵头起草数据交易所合同管理规范的宣贯，或者排查交易系统风控规则的缺陷，你是团队最坚实、最不可逾越的防线。",
        "partner": "最佳业务搭档：ESTJ（你们组合就是执行力的天花板）",
        "life": "秩序感是你能量的来源。但偶尔的失控未必是坏事，试着在周末来一场没有攻略的自驾游，给紧绷的神经松松绑。",
        "love": "你不擅长甜言蜜语，认为爱情的本质就是契约与责任。陪伴是最长情的告白，靠谱是最顶级的浪漫，你会默默为伴侣提供坚不可摧的后勤保障。"
    },
    "ESTJ": {
        "role": "领航者 | 业务推进的重装机甲",
        "desc": "铁腕执行，结果导向。没有你落不了地的政策，没有你推进不下去的规范。",
        "career": "天生的统帅。在向市局汇报政策，或者在所内跨部门推行合同管理规范时，你能顶住所有的阻力，强势破局。你是让数据要素流通起来的绝对实干家。",
        "partner": "最佳合规搭档：ISTJ（他们能确保你的突进不越红线）",
        "life": "习惯了掌控一切，容易表现出“领导做派”。学会放下身段，陪伴家人时，少讲点大道理，多提供一点情绪价值。",
        "love": "对家庭极具责任感，但也容易强势。试着在伴侣面前卸下在交易所里的铠甲，学会倾听。高质量的爱更是精神上的平等交流。"
    },
    "INFJ": {
        "role": "提倡者 | 数据生态的先知",
        "desc": "洞察人心，高瞻远瞩。你关注的不仅仅是一笔交易，而是它背后的社会价值。",
        "career": "不仅是规则制定者，更是生态布道师。在处理跨部门风控摩擦时，你能敏锐察觉到对方的核心诉求，用极高的情商化解危机，推动顶层制度在人心中落地。",
        "partner": "最佳业务搭档：ENFP（他们的热情能点燃你的深邃蓝图）",
        "life": "必须学会“课题分离”，不要把合规压力带入个人情绪。寻找一个属于自己的心灵避难所，比如冥想或深度阅读。",
        "love": "渴望深邃、直击灵魂的爱恋。理想的爱情是宿命感与共同成长的结合。你的爱温柔而磅礴，但也需要对方能真正读懂你的内心。"
    },
    "INFP": {
        "role": "调停者 | 价值理念的守望者",
        "desc": "内心纯粹，坚守理想。在冰冷的数字资产背后，你始终在寻找人性和温度。",
        "career": "枯燥的条款可能让你窒息，但在起草传递交易所核心价值观的报告时，你会文思泉涌。你适合从事生态培育以及具有社会责任属性的课题探索。",
        "partner": "最佳合规搭档：ENFJ（他们能给你极大的情感支持）",
        "life": "接受“水至清则无鱼”的现实，在合规与业务的灰度中寻找平衡。用艺术或音乐来安置你无处安放的才华。",
        "love": "天生的浪漫主义者，爱情往往伴随着诗意和极强的仪式感。比如专门为爱人 Yushi Han 写一首歌来记录专属的羁绊，用音符标记你们的爱情数据。"
    },
    "ENTJ": {
        "role": "指挥官 | 数据产业的破壁人",
        "desc": "气场全开，雷厉风行。风浪越大你越兴奋，生来就是为了征服复杂的数据商业博弈。",
        "career": "极其适合担任核心团队负责人。在争取重磅政策支持，或是主导顶层数据产权制度改革时，你极具战略眼光，能迅速整合资源，带领团队杀出一条血路。",
        "partner": "最佳业务搭档：INTJ（他们负责底层架构，你负责开疆拓土）",
        "life": "“停不下来”是常态。请强迫自己休息，去尝试壁球或赛车等竞技运动，在非工作领域释放你的征服欲。",
        "love": "追求“强强联合”，希望伴侣是能在事业上给你启发、智力上势均力敌的战友。记得在家里关掉“指挥官模式”，多展现一点柔软和妥协。"
    },
    "ENTP": {
        "role": "辩论家 | 传统规则的颠覆者",
        "desc": "脑洞极大，不破不立。你最讨厌的一句话就是“以前一直都是这么做的”。",
        "career": "数字资产交易风控规则的天然挑战者。总能从不可思议的角度找到制度漏洞并重构。极其适合数据知识产权的前沿探索，只要不干重复性审批，你就是无敌的。",
        "partner": "最佳合规搭档：INTP（你们能一起把系统的底裤看穿）",
        "life": "兴趣像阵风，不要因为三分钟热度自责，广泛涉猎正是灵感源泉。结交不同领域的朋友，跨界的碰撞会让你兴奋不已。",
        "love": "爱情是一场不能无聊的游戏。你需要一个能接住你的各种梗、愿意陪你一起疯的伴侣。你害怕被束缚，高质量的独立空间对关系至关重要。"
    },
    "ENFJ": {
        "role": "主人公 | 交易所的政委",
        "desc": "极具魅力，共情力爆表。你不是在管理团队，你是在点燃他们。",
        "career": "跨部门协同和外部对接的绝佳人选。无论是汇报政策进展，还是调解风控与业务的矛盾，你都能用感染力让各方达成共识，是团队绝对的主心骨。",
        "partner": "最佳业务搭档：INFP（你能完美承接他们的理念并落地）",
        "life": "太习惯于照顾所有人的情绪。请记住：在戴上氧气面罩救别人前，先确保自己呼吸顺畅。你的价值不需要建立在无限度的付出上。",
        "love": "完美的伴侣，能敏锐察觉爱人需求并给予温暖回应。但同样渴望被热烈地爱着。找一个懂得感恩、愿意用实际行动回馈你的人。"
    },
    "ENFP": {
        "role": "竞选者 | 创新生态的火种",
        "desc": "热情洋溢，创意无限。哪里有你，哪里就有数据生态的勃勃生机。",
        "career": "不适合被锁在办公室死磕干瘪的规范。你应该去一线，开拓数商生态。你的热情极具感染力，能轻松撬动海量的外部政企资源。",
        "partner": "最佳合规搭档：INFJ（他们能看懂你天马行空背后的深意）",
        "life": "急需一个靠谱的朋友帮你看好钱包、理清思路，把你的天马行空落地为现实。保持你的好奇心，那是你最珍贵的资产。",
        "love": "容易一头扎进热恋。真正的挑战在于激情退却后的平淡岁月。寻找一个既能陪你疯玩，又能在关键时刻拉住你风筝线的成熟伴侣。"
    },
    "ISFJ": {
        "role": "守卫者 | 后台运营的压舱石",
        "desc": "温和谦逊，细致入微。没有你在后台的死磕，前台的业务根本跑不起来。",
        "career": "合规审查的天然屏障。面对海量确权资料和冗长合同规范，只有你能做到明察秋毫。你极其负责的态度是交易所不可或缺的压舱石。",
        "partner": "最佳业务搭档：ESFJ（你们的组合能把一切安排得明明白白）",
        "life": "你总是那个默默收拾妥当的人，容易受委屈。你的善良必须带点锋芒。今天下班后推掉麻烦事，给自己买一束花。",
        "love": "你的爱如春风化雨，了解伴侣所有的喜好。你渴望一段稳定、忠诚的传统关系。警惕在感情中一味妥协失去自我。"
    },
    "ESFJ": {
        "role": "执政官 | 交易生态的粘合剂",
        "desc": "八面玲珑，热心肠。你能把整个交易所上下左右的关系理得明明白白。",
        "career": "天然的生态运营专家。无论是与市局沟通，还是维系挂牌数商活跃度，你都游刃有余。能敏锐察觉利益相关方诉求，盘活复杂资源。",
        "partner": "最佳合规搭档：ISFJ（你们能确保所有流程顺滑无阻）",
        "life": "极度在乎别人的评价让你活得有些累。尝试摆脱“老好人”标签，建立内在的评价标准。享受哪怕没有人为你点赞的平静时光。",
        "love": "极其顾家，把家庭经营得温馨热闹。但在感情中要警惕“我是为你好”式的过度控制，给伴侣留出足够的呼吸空间。"
    },
    "ISTP": {
        "role": "鉴赏家 | 交易系统的冷酷手术刀",
        "desc": "人狠话不多，实操能力点满。少整虚的，直接看底层数据和代码逻辑。",
        "career": "极度适合处理突发性系统风控危机。当别人在争论时，你已经一头扎进底层规则里修复了引发危机的缺陷。你崇尚“用结果说话”。",
        "partner": "最佳业务搭档：ESTP（你们都是实干派的狠角色）",
        "life": "需要极强的感官刺激来确认存在感。去玩极限运动或者闷头组装复杂的机械模型，这是你疏解高压工作最好的方式。",
        "love": "你觉得爱就是“遇到事了帮你解决”。你可能会通过修好电脑、解决实际困难来表达关心。你需要一个独立、不作不闹的酷伴侣。"
    },
    "ISFP": {
        "role": "探险家 | 数据美学的吟游诗人",
        "desc": "随性自由，极具审美。工作对你而言不仅是打卡，更是表达品味的方式。",
        "career": "在冰冷的交易所里，你是少有的艺术家气质。适合数字资产的创意包装与展示设计。严苛死板的规范会让你窒息，你需要在有美感的工作中发挥天赋。",
        "partner": "最佳合规搭档：ESFP（你们能一起让枯燥的数据充满活力）",
        "life": "极其厌恶冲突，只想守着自己的一亩三分地。把工位或书房布置成一个极具氛围感的空间，点上香薰，远离外界喧嚣。",
        "love": "极其温柔，有着超强的感知力。喜欢顺其自然，讨厌被要求规划五年后的未来。窝在沙发里听一首歌，就是最顶级的浪漫。"
    },
    "ESTP": {
        "role": "企业家 | 数据浪潮的冲浪手",
        "desc": "胆大心细，极其敏锐。在数据变现的风口上，你的嗅觉比谁都灵敏。",
        "career": "数字资产创新交易是你的主场。总能在合规的边缘找到最前沿的商业模式。执行力极强，能在千钧一发之际拍板，是带兵打仗的猛将。",
        "partner": "最佳合规搭档：ISTP（用最快的方式解决系统性阻碍）",
        "life": "永远在追求刺激点。多尝试跨界社交，获取能量。但请务必在合规和财务上给自己留足安全底线。",
        "love": "魅力四射，游刃有余。追求激情和新鲜感。真正的成熟，是懂得在平平淡淡的相伴中，发现不断更新的乐趣。"
    },
    "ESFP": {
        "role": "表演者 | 数据发布会的超级巨星",
        "desc": "天生 C 位，永远热烈。只要有你在，交易所的氛围就绝不会沉闷。",
        "career": "极其适合代表交易所对外发声，如主持大型产品发布会。你的表现力能把枯燥的数据要素讲得生动有趣。死板的幕后审查绝对会毁了你。",
        "partner": "最佳合规搭档：ISFP（你们是极佳的前后台创意组合）",
        "life": "“今朝有酒今朝醉”是你的座右铭。不要为了假装深刻而去读宏大的理论文件。你的快乐和纯粹，本身就是极稀缺的财富。",
        "love": "爱情必须是轰轰烈烈的，喜欢高调秀恩爱。找一个懂得欣赏你的光芒，并愿意陪你把生活折腾得热气腾腾的人。"
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

# --- 6. 核心 UI 渲染 ---
st.title("📈 SDE 专属：核心数据引擎测算")
st.markdown("<p style='color:#64748b; font-size: 14px;'>上海数据交易所团队专属沙盘。请凭第一直觉作答，系统将构建你的能量雷达。</p>", unsafe_allow_html=True)

total_q = len(questions)

if st.session_state.current_q < total_q:
    progress = st.session_state.current_q / total_q
    st.progress(progress)
    st.caption(f"深度扫描中: {st.session_state.current_q + 1} / {total_q}")
    st.markdown("<br>", unsafe_allow_html=True) 
    
    current_item = questions[st.session_state.current_q]
    st.markdown(f"<h4 style='color:#0f172a;'>{current_item['q']}</h4>", unsafe_allow_html=True)
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
    # 核心算法
    mbti_result = ""
    mbti_result += "E" if scores["E"] >= scores["I"] else "I"
    mbti_result += "S" if scores["S"] >= scores["N"] else "N"
    mbti_result += "T" if scores["T"] >= scores["F"] else "F"
    mbti_result += "J" if scores["J"] >= scores["P"] else "P"
    
    profile_data = mbti_profiles.get(mbti_result, mbti_profiles["INTJ"]) 
    
    # 结果大卡片
    st.markdown(f"""
    <div class="result-card">
        <p style="margin:0; font-size: 15px; opacity: 0.8; letter-spacing: 2px; color: #64748b; text-transform: uppercase;">你的合规与业务底层架构</p>
        <p class="mbti-text">{mbti_result}</p>
        <p class="mbti-role">【 {profile_data['role']} 】</p>
        <p style="font-size: 16px; line-height: 1.6; color: #334155;">"{profile_data['desc']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 新增杀手级功能：直观的数据进度面板 ---
    st.markdown("### 📊 灵魂底色数据面板")
    
    def draw_bar(left_label, left_score, right_label, right_score):
        left_pct = (left_score / 8) * 100
        right_pct = (right_score / 8) * 100
        # 平局时颜色平均分配
        st.markdown(f"""
        <div class="bar-container">
            <span style="color:#1e3c72;">{left_label} ({left_score})</span>
            <div class="bar-bg">
                <div class="bar-fill-left" style="width: {left_pct}%;"></div>
                <div class="bar-fill-right" style="width: {right_pct}%;"></div>
            </div>
            <span style="color:#d4af37;">{right_label} ({right_score})</span>
        </div>
        """, unsafe_allow_html=True)

    draw_bar("外向 (E)", scores["E"], "内向 (I)", scores["I"])
    draw_bar("实感 (S)", scores["S"], "直觉 (N)", scores["N"])
    draw_bar("思考 (T)", scores["T"], "情感 (F)", scores["F"])
    draw_bar("判断 (J)", scores["J"], "感知 (P)", scores["P"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 建议区
    st.markdown("### 🧭 你的 SDE 专属进阶指南")
    tab1, tab2, tab3 = st.tabs(["💼 业务与搭档", "🌱 能量与生活", "❤️ 情感与羁绊"])
    
    with tab1:
        st.markdown(f"<div class='advice-box'><b>核心发展：</b><br>{profile_data['career']}<br><br><b>🤝 职场连结：</b><br>{profile_data['partner']}</div>", unsafe_allow_html=True)
    with tab2:
        st.markdown(f"<div class='advice-box'><b>生活赋能：</b><br>{profile_data['life']}</div>", unsafe_allow_html=True)
    with tab3:
        st.markdown(f"<div class='advice-box'><b>情感密码：</b><br>{profile_data['love']}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- 新增杀手级功能：一键生成社交名片 ---
    st.markdown("### 💌 专属社交名片 (点击复制即可分享)")
    share_text = f"我在上海数据交易所专属图谱测出了【{mbti_result} {profile_data['role']}】！\n底层架构：{profile_data['desc']}\n职场搭档：{profile_data['partner'].split('：')[1]}\n快来测测你的业务底色是什么吧！"
    st.markdown(f"<div class='share-box'>{share_text}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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