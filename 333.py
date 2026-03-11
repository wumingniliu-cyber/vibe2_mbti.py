import streamlit as st
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
# 🌌 [ WARFRAME 01 ] 终焉引擎内核与绝对安全沙盒
# ==============================================================================
VERSION = "42.0_IMMORTAL_OMNIVERSE"
COPYRIGHT = "无名逆流"
SYS_NAME = "职场元宇宙 | 终焉矩阵 V42"

st.set_page_config(page_title=SYS_NAME, page_icon="🩸", layout="wide", initial_sidebar_state="collapsed")

# 绝对物理隔离：纯静态拼接替换所有 f-string 以免疫 NameError/KeyError
def safe_html(text):
    st.markdown(text.replace('\n', ''), unsafe_allow_html=True)

def center_container():
    return st.columns([1, 2, 1])[1]

def init_state():
    defaults = {
        'started': False, 'current_q': 0, 'start_time': None, 'end_time': None,
        'calculating': False, 'user_alias': "SURVIVOR", 
        'total_scores': {"E": 0, "S": 0, "T": 0, "J": 0}, 
        'anim_played': False, 'boot_played': False,
        'tokens': 10000, 
        'dark_matter': 0, 
        'logic_shards': 0, 
        'sanity': 150, 'max_sanity': 150, 'stamina': 150, 'level': 1, 'exp': 0, 
        'ascension_stars': 0, 'ascended': False,
        'boss_hp': 2000000, 'boss_level': 1, 'combat_logs': [], 'pvp_logs': [], 'dispatch_logs': [],
        'inventory': [], 'equipped_relics': [], 'pets': [], 'equipped_pet': None,
        'joined_faction': None, 'equipped_title': "【流浪炮灰】", 'titles_owned': ["【流浪炮灰】"],
        'staked_tokens': 0, 'yield_pool': 0.0, 
        'talent_levels': {"E": 0, "S": 0, "T": 0, "J": 0}, 
        'cyber_augments': [], 'final_cp_cache': 10000, 'turn_count': 1, 
        'achievements': [], 'bounties_claimed': False, 'pity_counter': 0, 
        'weather': "🌑 废土死寂 (无特殊效果)",
        'world_chat': ["<span style='color:#f43f5e;'>[SYS] 终焉引擎 V42.0 已激活。齿轮开始转动。</span>"],
        'gpus': 0, 'tarot_buff': "无", 'despair_level': 0,
        'card_foil': "【标准拉丝工艺】", 'squad': [None, None], 'exchange_rate': 100,
        'forge_msg': "将 3 件同星级未装备圣物融合升阶！", 'gacha_msg': "消耗 1,000 SDE 召唤高维战利品"
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
init_state()

# ==============================================================================
# ⚙️ [ WARFRAME 02 ] 核心闭环生态计算与全局操作回调 (100% 防 NameError)
# ==============================================================================
def start_assessment_callback():
    alias = st.session_state.get("login_input", "").strip()
    st.session_state.user_alias = html.escape(alias) if alias else "SURVIVOR"
    st.session_state.started = True
    st.session_state.start_time = time.time()
    add_chat("新节点 [" + st.session_state.user_alias + "] 强行接入了数据之海。", "#00f3ff")

def answer_callback(val, dim):
    st.session_state.total_scores[dim] += (val - 3)
    st.session_state.current_q += 1
    if st.session_state.current_q >= 40:
        st.session_state.end_time = time.time()
        st.session_state.calculating = True

def get_stat_multipliers():
    base_res = st.session_state.total_scores
    tl = st.session_state.talent_levels
    val_E_raw = base_res.get("E", 0) + tl["E"] * 2
    val_S_raw = base_res.get("S", 0) + tl["S"] * 2
    val_T_raw = base_res.get("T", 0) + tl["T"] * 2
    val_J_raw = base_res.get("J", 0) + tl["J"] * 2
    return {
        "boss_dmg_mult": 1.0 + (max(0, val_E_raw) * 0.05), 
        "pvp_def_mult": 1.0 + (max(0, val_T_raw) * 0.05),  
        "drop_rate_mult": 1.0 + (max(0, val_S_raw) * 0.05),
        "yield_mult": 1.0 + (max(0, val_J_raw) * 0.05),    
        "sanity_resist": max(0, val_T_raw) 
    }

def add_chat(msg, color="#10b981"):
    ts = datetime.now().strftime('%H:%M:%S')
    st.session_state.world_chat.insert(0, "<span style='color:" + color + ";'>[" + ts + "] " + msg + "</span>")
    if len(st.session_state.world_chat) > 30: st.session_state.world_chat.pop()

def unlock_title(title):
    if title not in st.session_state.titles_owned:
        st.session_state.titles_owned.append(title)
        st.session_state.tokens += 3000
        add_chat("[全区广播] 幸存者 " + st.session_state.user_alias + " 夺得了军衔：" + title, "#ffd700")
        st.toast("🏆 获得新军衔：" + title, icon="🏆")

def unlock_achievement(title):
    if title not in st.session_state.achievements:
        st.session_state.achievements.append(title)
        st.session_state.dark_matter += 100 
        st.toast("🏆 解锁绝境成就：" + title + "！奖励 100 暗物质！", icon="🏆")
        add_chat("[深渊快报] 节点 [" + st.session_state.user_alias + "] 达成了创举：" + title, "#ff003c")

def gain_exp(amount):
    if "教皇" in st.session_state.tarot_buff: amount = int(amount * 1.5)
    st.session_state.exp += amount
    req = st.session_state.level * 100
    if st.session_state.exp >= req:
        st.session_state.exp -= req
        st.session_state.level += 1
        st.toast("🌟 阶级跃迁！当前等级 Lv." + str(st.session_state.level), icon="🌟")
        if st.session_state.level == 10: unlock_title("【十级卷王】")
        if st.session_state.level == 30: unlock_title("【无情收割机】")
        if st.session_state.level == 50: unlock_title("【寰宇半神】")

def consume_action_points(stam_cost, san_cost):
    if st.session_state.equipped_pet and "机械哈士奇" in st.session_state.equipped_pet.get('name', ''):
        stam_cost = max(1, int(stam_cost * 0.5))
    if st.session_state.stamina < stam_cost: return False, "❌ 体力不足！"
    
    st.session_state.stamina -= stam_cost
    t_lvl = st.session_state.talent_levels['T']
    real_san_cost = max(1, san_cost - t_lvl)
    st.session_state.sanity = max(0, st.session_state.sanity - real_san_cost)
    return True, "OK"

def tick_turn(*args, **kwargs):
    st.session_state.turn_count += 1
    mults = get_stat_multipliers()
    st.session_state.stamina = min(150, st.session_state.stamina + 2)
    
    if st.session_state.sanity < 50: st.session_state.despair_level = min(100, st.session_state.despair_level + random.randint(3, 8))
    else: st.session_state.despair_level = max(0, st.session_state.despair_level - 1)
    
    if st.session_state.staked_tokens > 0 and st.session_state.despair_level < 80:
        base_yield = 0.0 if "降息浪潮" in st.session_state.weather else random.uniform(0.005, 0.02)
        ascend_bonus = st.session_state.ascension_stars * 0.01
        pet_bonus = 0.01 if st.session_state.equipped_pet and "游隼" in st.session_state.equipped_pet.get('name', '') else 0.0
        st.session_state.yield_pool += st.session_state.staked_tokens * (base_yield + ascend_bonus + pet_bonus) * mults["yield_mult"]
        
    if st.session_state.gpus > 0 and st.session_state.despair_level < 80:
        mining_yield = st.session_state.gpus * random.randint(150, 300) * mults["yield_mult"]
        if "星币" in st.session_state.tarot_buff: mining_yield *= 2
        st.session_state.tokens += int(mining_yield)
        
    st.session_state.exchange_rate = max(50, min(500, int(st.session_state.exchange_rate * random.uniform(0.9, 1.1))))
    
    if random.random() < 0.18:
        weathers = ["⛈️ 量子风暴 (+30%量子系战力)", "🔥 焦土裁员 (+30%炎脉战力)", "✨ 幽灵协议 (+30%灵能战力)", "🛡️ 绝对堡垒 (+30%钢核战力)", "💀 死亡加班 (获取经验翻倍)", "🏦 降息浪潮 (质押利息归零)", "🌑 废土死寂 (无特殊效果)"]
        new_w = random.choice(weathers)
        st.session_state.weather = new_w
        add_chat("[天象警告] 全域气候变更为：" + new_w, "#ff003c")

def equip_title_callback():
    tick_turn()
    st.session_state.equipped_title = st.session_state.title_sel
    st.toast("✅ 已佩戴：" + st.session_state.title_sel)

def claim_yield_callback():
    tick_turn()
    yld = int(st.session_state.yield_pool)
    if yld > 0:
        st.session_state.tokens += yld
        st.session_state.yield_pool = 0.0
        st.toast("✅ 成功提取: " + "{:,}".format(yld) + " $SDE！", icon="💰")

def cb_sleep():
    tick_turn()
    if st.session_state.tokens >= 500:
        st.session_state.tokens -= 500
        st.session_state.stamina = min(150, st.session_state.stamina + 40)
        st.session_state.sanity = min(st.session_state.max_sanity, st.session_state.sanity + 20)
    else: st.toast("战备金不足！", icon="❌")

def cb_purify():
    tick_turn()
    if st.session_state.tokens >= 4000:
        st.session_state.tokens -= 4000
        st.session_state.despair_level = 0
        st.session_state.sanity = st.session_state.max_sanity
        st.toast("精神净化完成，污染已清零！", icon="✨")
    else: st.toast("战备金不足！", icon="❌")

def cb_gacha(pool_type):
    tick_turn()
    cost = 1500 if "数据干旱" in st.session_state.weather else 1000
    if st.session_state.despair_level > 80: cost *= 2
    if st.session_state.tokens >= cost:
        st.session_state.tokens -= cost
        st.session_state.pity_counter += 1
        base_ur = 0.05
        if st.session_state.despair_level > 80: base_ur = 0.00 
        if "命运之轮" in st.session_state.tarot_buff: base_ur += 0.05
        roll = random.random() if st.session_state.pity_counter < 30 else 0.001 
        target_pool = RELICS_POOL if pool_type == "relic" else PETS_POOL
        
        if roll < base_ur: 
            r = random.choice([x for x in target_pool if x['rarity']=='UR'])
            st.session_state.pity_counter = 0
            st.snow()
        elif roll < 0.20: r = random.choice([x for x in target_pool if x['rarity']=='SSR'])
        elif roll < 0.60: r = random.choice([x for x in target_pool if x['rarity']=='SR'])
        else: r = random.choice([x for x in target_pool if x['rarity']=='R'])
        
        if r['rarity'] in ['SSR', 'UR']: st.session_state.pity_counter = 0
            
        r_copy = copy.deepcopy(r)
        r_copy['uid'] = "g_" + str(int(time.time()*1000)) + "_" + str(random.randint(0,999))
        
        if pool_type == "relic": st.session_state.inventory.insert(0, r_copy)
        else: st.session_state.pets.insert(0, r_copy)
            
        st.session_state.gacha_msg = "🎉 捕获成功！获得 " + r_copy['rarity'] + " 级：" + r_copy['name']
        if r['rarity'] in ['SSR', 'UR']: add_chat(st.session_state.user_alias + " 打捞出了 " + r_copy['name'] + "！", r_copy['color'])
        gain_exp(10)
        if r['rarity'] == 'UR': unlock_achievement("【神话之手】")
    else: st.session_state.gacha_msg = "❌ 资金不足！需要 " + str(cost) + " SDE。"

def cb_equip_relic(uid):
    tick_turn()
    for r in st.session_state.inventory:
        if r['uid'] == uid:
            if any(eq['uid'] == uid for eq in st.session_state.equipped_relics):
                st.session_state.equipped_relics = [eq for eq in st.session_state.equipped_relics if eq['uid'] != uid]
            else:
                if len(st.session_state.equipped_relics) < 3: st.session_state.equipped_relics.append(r)
                else: st.session_state.equipped_relics.pop(0); st.session_state.equipped_relics.append(r)
            break

def cb_equip_pet(uid):
    tick_turn()
    for p in st.session_state.pets:
        if p['uid'] == uid:
            if st.session_state.equipped_pet and st.session_state.equipped_pet['uid'] == uid: st.session_state.equipped_pet = None
            else: st.session_state.equipped_pet = p
            break

def cb_dismantle(uid):
    tick_turn()
    for i, r in enumerate(st.session_state.inventory):
        if r['uid'] == uid:
            val = {"UR": 2000, "SSR": 800, "SR": 300, "R": 100}.get(r['rarity'], 100)
            st.session_state.tokens += val
            st.session_state.inventory.pop(i)
            st.toast("♻️ 熔解成功！获得了 " + str(val) + " SDE。", icon="♻️")
            break

def cb_forge(consume_rarity, target_rarity):
    if st.session_state.despair_level > 80 and random.random() < 0.5:
        avail = [r for r in st.session_state.inventory if r['rarity'] == consume_rarity and not any(eq['uid'] == r['uid'] for eq in st.session_state.equipped_relics)]
        if len(avail) >= 3:
            for i in range(3): st.session_state.inventory.remove(avail[i])
        st.session_state.forge_msg = "💥 理智崩溃导致操作失误，熔炉大爆炸，材料全毁！"
        st.toast("💥 熔炉大爆炸！", icon="💥")
        add_chat("节点 " + st.session_state.user_alias + " 精神失常，炸毁了量子熔炉！", "#ff003c")
        return
    tick_turn()
    avail = [r for r in st.session_state.inventory if r['rarity'] == consume_rarity and not any(eq['uid'] == r['uid'] for eq in st.session_state.equipped_relics)]
    if len(avail) >= 3:
        for i in range(3): st.session_state.inventory.remove(avail[i])
        pool = [x for x in RELICS_POOL if x['rarity'] == target_rarity]
        if pool:
            new_r = copy.deepcopy(random.choice(pool))
            new_r['uid'] = "rel_" + str(int(time.time()*1000)) + "_" + str(random.randint(0,999))
            st.session_state.inventory.insert(0, new_r)
            st.session_state.forge_msg = "🔥 锻造成功！获得了：" + new_r['name']
            if target_rarity == "UR": st.snow()
    else: st.session_state.forge_msg = "❌ 材料不足：需要 3 件未装备的 " + consume_rarity + " 级材料！"

def cb_dispatch():
    ok, msg = consume_action_points(20, 5)
    if not ok:
        st.session_state.dispatch_logs.insert(0, msg)
        return
    tick_turn()
    mults = get_stat_multipliers()
    events = [
        ("📡 潜入暗网黑市，发现无主钱包！", "token", 8000),
        ("🛡️ 协助抵抗军拦截了一次攻击！", "exp", 150),
        ("💀 踩中蜜罐陷阱，理智受到精神攻击...", "sanity", -25),
        ("✨ 在数据废墟中挖到了一块逻辑碎片！", "shard", 1),
        ("🤝 与其他流浪节点完成了一次交易。", "token", 4000)
    ]
    ev = random.choice(events)
    if random.random() < (0.05 * mults["drop_rate_mult"]): ev = ("💎 发现隐秘宝库，挖到了高维武装！", "relic", 1)
        
    if ev[1] == "token":
        amt = int(ev[2] * mults["drop_rate_mult"])
        pet_name = st.session_state.equipped_pet.get('name', '') if st.session_state.equipped_pet else ""
        if "寻宝狐" in pet_name: amt = int(amt * 1.5)
        st.session_state.tokens += amt
        tag = " [实勘加成]" if mults["drop_rate_mult"] > 1.0 else ""
        st.session_state.dispatch_logs.insert(0, "[" + datetime.now().strftime('%H:%M:%S') + "] " + ev[0] + " (+" + str(amt) + " SDE)" + tag)
    elif ev[1] == "exp":
        gain_exp(ev[2])
        st.session_state.dispatch_logs.insert(0, "[" + datetime.now().strftime('%H:%M:%S') + "] " + ev[0] + " (+" + str(ev[2]) + " EXP)")
    elif ev[1] == "shard":
        st.session_state.logic_shards += ev[2]
        st.session_state.dispatch_logs.insert(0, "[" + datetime.now().strftime('%H:%M:%S') + "] " + ev[0] + " (逻辑碎片+1)")
    elif ev[1] == "sanity":
        st.session_state.sanity = max(0, st.session_state.sanity + ev[2])
        st.session_state.dispatch_logs.insert(0, "[" + datetime.now().strftime('%H:%M:%S') + "] " + ev[0] + " (SAN " + str(ev[2]) + ")")
    elif ev[1] == "relic":
        r = random.choice([x for x in RELICS_POOL if x['rarity'] in ['SR', 'SSR']])
        r_copy = copy.deepcopy(r); r_copy['uid'] = "rel_" + str(int(time.time()*1000)) + "_" + str(random.randint(0,999))
        st.session_state.inventory.insert(0, r_copy)
        st.session_state.dispatch_logs.insert(0, "[" + datetime.now().strftime('%H:%M:%S') + "] " + ev[0] + " 获得: " + r['name'])

def cb_boss_attack():
    if st.session_state.despair_level >= 100:
        st.session_state.combat_logs.insert(0, "💀 彻底疯狂！你失去了控制能力！")
        return
    ok, msg = consume_action_points(15, 10)
    if not ok:
        st.session_state.combat_logs.insert(0, msg)
        return
    tick_turn()
    mults = get_stat_multipliers()
    cp = st.session_state.get('final_cp_cache', 10000)
    
    # 获取玩家元素
    res = st.session_state.total_scores
    mbti = ("E" if res.get("E", 0) >= 0 else "I") + ("S" if res.get("S", 0) >= 0 else "N") + ("T" if res.get("T", 0) >= 0 else "F") + ("J" if res.get("J", 0) >= 0 else "P")
    faction_data = get_faction_info(mbti)
    player_element = faction_data['element']

    boss_element = ["⚡ 量子", "✨ 灵能", "🛡️ 钢核", "🔥 炎脉"][st.session_state.boss_level % 4]
    element_mult = 1.0
    adv_map = {"⚡ 量子":"🔥 炎脉", "🔥 炎脉":"🛡️ 钢核", "🛡️ 钢核":"✨ 灵能", "✨ 灵能":"⚡ 量子"}
    if adv_map.get(player_element) == boss_element: element_mult = 1.5
    elif adv_map.get(boss_element) == player_element: element_mult = 0.5
    
    s_lvl = st.session_state.talent_levels['S']
    crit_rate = 0.15 + (s_lvl * 0.05)
    is_crit = random.random() < crit_rate
    crit_dmg_mult = 3.5 if (st.session_state.equipped_pet and "量子猫" in st.session_state.equipped_pet.get('name','')) else 2.0
    
    base_dmg = int(cp * random.uniform(0.8, 1.2) * mults['boss_dmg_mult'] * 0.1) 
    if "力量" in st.session_state.tarot_buff: base_dmg *= 2
    dmg = int(base_dmg * (crit_dmg_mult if is_crit else 1.0) * element_mult)
    
    st.session_state.boss_hp -= dmg
    dmg_tag = "{:,}".format(dmg)
    if element_mult > 1.0: dmg_tag += " (克制暴击!)"
    if is_crit: dmg_tag += " CRIT!"
    if mults['boss_dmg_mult'] > 1.0: dmg_tag += " [E属性强化]"
    
    st.session_state.combat_logs.insert(0, "[" + datetime.now().strftime('%H:%M:%S') + "] ⚔️ 造成了 " + dmg_tag + " 伤害！")
    
    dm_drop = int(dmg / 100000)
    if dm_drop > 0: 
        st.session_state.dark_matter += dm_drop
        st.session_state.combat_logs.insert(0, "🔮 掉落了 " + str(dm_drop) + " 个暗物质！")
    
    st.session_state.tokens += int(dmg / 10)
    gain_exp(50)
    if "死亡加班" in st.session_state.weather: gain_exp(50)
    
    if st.session_state.boss_hp <= 0:
        st.session_state.combat_logs.insert(0, "🏆 Lv." + str(st.session_state.boss_level) + " 利维坦被击破！")
        add_chat("捷报！" + st.session_state.user_alias + " 击杀了 Lv." + str(st.session_state.boss_level) + " 利维坦！全服狂欢！", "#ff003c")
        st.session_state.tokens += 100000 * st.session_state.boss_level
        st.session_state.dark_matter += 100 * st.session_state.boss_level
        st.session_state.boss_level += 1
        st.session_state.boss_hp = 2000000 * st.session_state.boss_level

def cb_pvp_battle():
    target_faction = st.session_state.get("pvp_target", "无名阵营")
    if st.session_state.despair_level >= 100:
        st.session_state.pvp_logs.insert(0, "💀 你已经疯了。")
        return
    ok, msg = consume_action_points(15, 10)
    if not ok:
        st.session_state.pvp_logs.insert(0, msg)
        return
    tick_turn()
    cp = st.session_state.get('final_cp_cache', 10000)
    enemy_cp = int(cp * random.uniform(0.7, 1.4))
    
    st.session_state.pvp_logs.insert(0, "=====================")
    st.session_state.pvp_logs.insert(0, "⚔️ 遭遇阵营: " + target_faction + " (敌战力: {:,})".format(enemy_cp))
    if cp >= enemy_cp:
        loot = int(enemy_cp * random.uniform(0.05, 0.15))
        st.session_state.pvp_logs.insert(0, "🏆 胜利！算力碾压对手！掠夺了 {:,} $SDE！".format(loot))
        st.session_state.tokens += loot
        st.session_state.dark_matter += random.randint(1, 5)
        gain_exp(60)
    else:
        loss = int(cp * random.uniform(0.01, 0.05))
        if st.session_state.equipped_pet and "机械猎犬" in st.session_state.equipped_pet.get('name',''):
            loss = int(loss * 0.5)
            st.session_state.pvp_logs.insert(0, "🐾 [猎犬] 护主，抵挡了 50% 损失！")
        st.session_state.tokens = max(0, st.session_state.tokens - loss)
        st.session_state.pvp_logs.insert(0, "💀 败北... 遭到降维打击，丢失 {:,} SDE。".format(loss))
        st.session_state.despair_level = min(100, st.session_state.despair_level + 10)
        gain_exp(10)

def cb_talent_up(dim):
    tick_turn()
    cost_sde = 2000 + st.session_state.talent_levels[dim] * 1000
    cost_shards = 1 + st.session_state.talent_levels[dim]
    if st.session_state.tokens >= cost_sde and st.session_state.logic_shards >= cost_shards:
        st.session_state.tokens -= cost_sde
        st.session_state.logic_shards -= cost_shards
        st.session_state.talent_levels[dim] += 1
        st.toast("🧬 " + dim + " 属性飞升！生态乘区强化！", icon="🧬")
    else: st.toast("❌ SDE 或逻辑碎片不足！(碎片需远征获得)", icon="❌")

def cb_upgrade_foil():
    tick_turn()
    foils = ["【标准拉丝工艺】", "【镭射碎冰闪卡】", "【暗黑反转闪卡】", "【创世血腥幻彩】"]
    costs = [0, 500, 1500, 5000]
    current = st.session_state.card_foil
    idx = foils.index(current) if current in foils else 0
    if idx < 3:
        if st.session_state.dark_matter >= costs[idx+1]:
            st.session_state.dark_matter -= costs[idx+1]
            st.session_state.card_foil = foils[idx+1]
            st.toast("✨ 卡面工艺升级成功！战力乘区扩大！"); st.balloons()
            if idx+1 == 3: unlock_achievement("【创世之影】")
        else: st.toast("❌ 暗物质不足！", icon="❌")
    else: st.toast("已达到最高工艺！")

def cb_exchange_buy():
    tick_turn()
    cost = st.session_state.exchange_rate * 10
    if st.session_state.tokens >= cost:
        st.session_state.tokens -= cost
        st.session_state.dark_matter += 10
        st.session_state.exchange_rate = int(st.session_state.exchange_rate * 1.05)
        st.toast("✅ 成功买入 10 暗物质")
    else: st.toast("❌ SDE 不足")

def cb_exchange_sell():
    tick_turn()
    earn = int(st.session_state.exchange_rate * 10 * 0.9)
    if st.session_state.dark_matter >= 10:
        st.session_state.dark_matter -= 10
        st.session_state.tokens += earn
        st.session_state.exchange_rate = max(50, int(st.session_state.exchange_rate * 0.95))
        st.toast("✅ 成功卖出 10 暗物质")
    else: st.toast("❌ 暗物质不足")

def cb_join_faction():
    tick_turn()
    st.session_state.joined_faction = st.session_state.faction_sel
    st.toast("🛡️ 成功加入阵营！", icon="🛡️")

def cb_stake():
    tick_turn()
    amt = 5000
    if st.session_state.tokens >= amt:
        st.session_state.tokens -= amt
        st.session_state.staked_tokens += amt
        st.toast("📥 成功质押 " + str(amt) + " SDE！")
    else: st.toast("❌ 资金不足！")

def cb_buy_stamina():
    tick_turn()
    if st.session_state.tokens >= 2000:
        st.session_state.tokens -= 2000
        st.session_state.stamina = min(150, st.session_state.stamina + 50)
        st.toast("💊 体力恢复 50 点！", icon="🔋")
    else: st.toast("❌ 资金不足！", icon="❌")

def cb_buy_ssr():
    tick_turn()
    if st.session_state.tokens >= 20000:
        st.session_state.tokens -= 20000
        r = random.choice([x for x in RELICS_POOL if x['rarity']=='SSR'])
        r_copy = copy.deepcopy(r); r_copy['uid'] = "rel_" + str(int(time.time()*1000)) + "_" + str(random.randint(0,999))
        st.session_state.inventory.insert(0, r_copy)
        st.toast("📦 走私成功！获得 " + r['name'] + "！", icon="🎁")
    else: st.toast("❌ 资金不足！", icon="❌")

def cb_buy_gpu():
    tick_turn()
    cost = 5000 + (st.session_state.gpus * 3000)
    if st.session_state.tokens >= cost:
        st.session_state.tokens -= cost
        st.session_state.gpus += 1
        st.toast("🖥️ 矿机部署成功！", icon="📈")
    else: st.toast("❌ 资金不足！", icon="❌")

def cb_claim_bounty():
    tick_turn()
    st.session_state.bounties_claimed = True
    st.session_state.tokens += 10000
    gain_exp(200)
    st.toast("🎁 领取悬赏成功！")

def cb_draw_tarot():
    tick_turn()
    if st.session_state.tokens >= 200:
        st.session_state.tokens -= 200
        buffs = ["【力量】讨伐伤害倍增", "【命运之轮】空投极品爆率提升", "【星币】矿机产出翻倍", "【教皇】获取经验+50%"]
        st.session_state.tarot_buff = random.choice(buffs)
        st.toast("🃏 塔罗指引：" + st.session_state.tarot_buff, icon="🃏")
    else: st.toast("❌ 资金不足！", icon="❌")

def cb_buy_augment(aug_id, cost, san_cost):
    tick_turn()
    if st.session_state.tokens >= cost:
        if aug_id not in st.session_state.cyber_augments:
            st.session_state.tokens -= cost
            st.session_state.max_sanity = max(10, st.session_state.max_sanity - san_cost)
            st.session_state.sanity = min(st.session_state.sanity, st.session_state.max_sanity)
            st.session_state.cyber_augments.append(aug_id)
            st.toast("🦾 义体装载成功！战力倍增！", icon="🦾")
            add_chat("警告：" + st.session_state.user_alias + " 进行了非人道的义体改造！", "#ff003c")
        else: st.toast("已拥有此义体！", icon="⚠️")
    else: st.toast("❌ 资金不足！", icon="❌")

def cb_ascend_card():
    tick_turn()
    cost = 100 + (st.session_state.ascension_stars * 50)
    if st.session_state.dark_matter >= cost and st.session_state.ascension_stars < 5:
        st.session_state.dark_matter -= cost
        st.session_state.ascension_stars += 1
        st.toast("🌌 界限突破！战力飙升！", icon="✨")
        if st.session_state.ascension_stars == 5:
            st.session_state.ascended = True; unlock_achievement("【超维神明】"); st.balloons()
    else: st.toast("❌ 暗物质不足！", icon="❌")

def cb_altar_blood():
    tick_turn()
    if st.session_state.sanity > 30:
        st.session_state.sanity -= 30; st.session_state.despair_level += 15 
        gain = random.randint(5, 15); st.session_state.dark_matter += gain
        st.toast("🩸 祭祀成功！获得 " + str(gain) + " 暗物质！污染加深...", icon="🩸")
        add_chat(st.session_state.user_alias + " 进行了禁忌的鲜血祭祀...", "#ff003c")
    else: st.toast("❌ 理智太低，祭祀会死的！", icon="❌")

def cb_altar_trash():
    tick_turn()
    rs = [r for r in st.session_state.inventory if r['rarity'] == "R" and not any(eq['uid'] == r['uid'] for eq in st.session_state.equipped_relics)]
    if rs:
        st.session_state.inventory.remove(rs[0])
        st.session_state.despair_level = max(0, st.session_state.despair_level - 20)
        st.toast("✨ 污染降低 20 点！")
    else: st.toast("没有多余未装备的 R级 废品！")

def cb_casino():
    tick_turn()
    if st.session_state.tokens >= 1000:
        st.session_state.tokens -= 1000
        if random.random() < 0.3:
            st.session_state.tokens += 3500; st.toast("🎰 狂热大奖！赢得 3500 SDE！", icon="🤑")
            add_chat(st.session_state.user_alias + " 在地下赌场赢得了大奖！", "#ffd700")
        else: st.toast("💀 血本无归！", icon="💸")
    else: st.toast("❌ 战备金不足！", icon="❌")

def cb_confirm_squad():
    tick_turn()
    st.session_state.squad = [st.session_state.syn1, st.session_state.syn2]
    st.toast("🤝 战术小队编成确认！")

def reset_system():
    st.session_state.clear()


# ==============================================================================
# 🧠 [ DATA 04 ] 题库与阵营生态图鉴 (硬编码安全注入)
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

mbti_details = {
    "INTJ": {"role": "矩阵架构师", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 1.2%", "base_hash": 9850, "desc": "垄断核心规则的幕后操盘手，在绝境中重写了整个财团的底层代码。", "tags": ["绝对独裁", "逻辑绞肉机", "法则支配"], "partner": "ENTJ", "partner_advice": "将前线指挥权交给 ENTJ，你只需稳居幕后。", "tasks": ["渗透并篡改中心化交易引擎", "建立反追踪的高维逻辑壁垒"], "black_swan": "对完美闭环的执念。当战争规则突然改变时，容易因为僵化而被反噬。", "patch": "在致命逻辑中留下一道后门，允许一线节点的混沌容错。", "skills": ["【被动】全知视界", "【法术】底层规则解构", "【领域】绝对秩序统御"], "base_roi": 1.45, "volatility": 0.20, "market_style": "宏观架构对冲与冷酷收割", "evolution_path": ["L1 架构规划者", "L2 矩阵操盘手"], "ultimate_evolution": "【绝对算力主宰】剥夺一切节点定价权"},
    "INTP": {"role": "深网风控骇客", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 3.1%", "base_hash": 9620, "desc": "穿透财团迷雾，在深网中寻找资本漏洞的极致黑客。", "tags": ["黑盒解构", "模型杀手", "极客暴徒"], "partner": "INTJ", "partner_advice": "依托 INTJ 将你的破坏性代码锚定，避免失控。", "tasks": ["研发针对核心财团的自动剥削算法", "部署实时异动嗅探木马"], "black_swan": "陷入无穷的算力演算中，在需要拔线的瞬间犹豫，导致机房被毁。", "patch": "别管模型优不优了，先拔电源！", "skills": ["【被动】多维特征抽取", "【法术】零日漏洞感染", "【秘技】量子坍缩推演"], "base_roi": 1.60, "volatility": 0.45, "market_style": "高频统计套利与嗜血量化模型", "evolution_path": ["L1 边缘骇客", "L2 深网潜行者"], "ultimate_evolution": "【全知算法先知】构建百分百无损的跨网风控引擎"},
    "ISTJ": {"role": "铁血审查官", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 11.6%", "base_hash": 8850, "desc": "废土中的程序正义者，你的评估就是生与死的分界线。", "tags": ["绝对防线", "铁血程序", "风险斩杀"], "partner": "ESTJ", "partner_advice": "配合 ESTJ 建立最强硬的防线，绞杀一切越界行为。", "tasks": ["主导企业叛逃节点的肃清审计", "锁定一切违背智能合约的行径"], "black_swan": "过于依赖旧世界的SOP。当新神降临时，你手中的法典可能毫无用处。", "patch": "偶尔学会闭上一只眼睛。", "skills": ["【被动】绝对法典加护", "【护盾】重装正义壁垒", "【反击】致命风险处决"], "base_roi": 1.15, "volatility": 0.10, "market_style": "绝对风险厌恶与固收阵地战", "evolution_path": ["L1 审查哨兵", "L2 铁血执行官"], "ultimate_evolution": "【绝对防御堡垒】废土要素流转网络最终守门人"},
    "ESTJ": {"role": "战区统帅", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 8.7%", "base_hash": 9500, "desc": "无可争议的镇压者，擅长将高层的残忍指令拆解为绝对执行的绞肉机。", "tags": ["铁血统帅", "结果导向", "战争机器"], "partner": "ISTJ", "partner_advice": "让 ISTJ 担任你的宪兵队长，在发生叛乱时迅速镇压。", "tasks": ["发起并统筹对敌对财团的百亿级歼灭战", "强力调度跨战区火力网"], "black_swan": "KPI压倒一切导致团队理智值崩溃引发哗变。", "patch": "下达送死指令前，适度释放廉价的情绪价值。", "skills": ["【被动】战略降维打击", "【战吼】全军狂暴冲锋", "【光环】铁腕意志压制"], "base_roi": 1.35, "volatility": 0.25, "market_style": "动量突破与重火力资产倾泻", "evolution_path": ["L1 战区指挥官", "L2 废土推进者"], "ultimate_evolution": "【战争心脏】宏观绞肉机推进的中枢"},
    "INFJ": {"role": "灵能先知", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 0.9%", "base_hash": 9200, "desc": "在冰冷代码中觉醒了人类共情，能预判未来战争走向的隐秘引路人。", "tags": ["虚空远见", "信仰狂热", "灵魂操控"], "partner": "ENFJ", "partner_advice": "将你的救赎愿景交由 ENFJ 在废土中广播，凝聚反抗力量。", "tasks": ["规划废土重建版图", "发起数字向善的最后一次倡议"], "black_swan": "过度悲天悯人，在极度残酷的算力掠夺中容易成为首个被献祭的节点。", "patch": "将你的先知直觉转化为冰冷的财报测算。", "skills": ["【被动】未来因果洞视", "【光环】跨频灵魂尖啸", "【法术】精神信仰奴役"], "base_roi": 1.55, "volatility": 0.35, "market_style": "宏观周期收割与长线价值潜伏", "evolution_path": ["L1 边缘观察者", "L2 灵能布道师"], "ultimate_evolution": "【全域先知】主导数字末日时代的底层精神共识"},
    "INFP": {"role": "游吟灵魂捕手", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 4.4%", "base_hash": 8650, "desc": "在这片被财团统治的废土上，你是唯一还记得“诗与远方”的幻灵。", "tags": ["价值感召", "组织凝胶", "异端定调"], "partner": "ENFJ", "partner_advice": "依托 ENFJ 的手腕在血腥博弈中为你护航。", "tasks": ["重塑反抗军的全球精神叙事", "实施废土营地的内部凝聚力工程"], "black_swan": "在冷酷的火力对决中因厌恶血腥而退缩。", "patch": "学会熟练利用预算与弹药来捍卫你的狂热信仰。", "skills": ["【被动】无形异端塑形", "【法术】直击灵魂低语", "【光环】隐性狂暴注入"], "base_roi": 1.25, "volatility": 0.30, "market_style": "另类信仰投资与利基长尾剥削", "evolution_path": ["L1 幻象叙事者", "L2 灵魂共振官"], "ultimate_evolution": "【灵魂共振核】赋予数据昂贵信仰溢价"},
    "ENTJ": {"role": "军阀霸主", "tier": "UR", "tier_color": "#ff003c", "rarity": "Top 1.8%", "base_hash": 9900, "desc": "天生的帝国建设者，在数据丛林法则中展现极强的暴力吞并能力。", "tags": ["全图开疆", "战略暴君", "降维碾压"], "partner": "INTJ", "partner_advice": "冲锋时把后背交给 INTJ，遇到底层装甲呼叫 ISTP 爆破。", "tasks": ["主导省级资源抢占与大清洗", "执行跨链互认大统一吞并战"], "black_swan": "狂飙突进时无视红线，被超级财团的轨道炮锁定熔断。", "patch": "放慢半拍，听听风控官的哀嚎，留点活口。", "skills": ["【被动】绝对暴君破局", "【战技】全域版图吞并", "【奥义】维度降级风暴"], "base_roi": 1.70, "volatility": 0.55, "market_style": "极高杠杆并购与特殊机会强吃", "evolution_path": ["L1 开拓先锋", "L2 战区统帅"], "ultimate_evolution": "【无界帝国霸主】全国市场的唯一暴君"},
    "ENTP": {"role": "混沌诡术师", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 3.2%", "base_hash": 9400, "desc": "旧秩序的践踏者，致力于通过跨界思维寻找资本漏洞的狂徒。", "tags": ["范式爆破", "诡辩狂人", "维度跳跃"], "partner": "INTP", "partner_advice": "把狂野的图纸丢给 INTP 降维，指挥 ESTP 去前线强拆。", "tasks": ["研发不可追溯的暗网凭证", "在监管盲区主导蓝海变现测试"], "black_swan": "无限发散导致交付烂尾，挖了坑不填直接跑路。", "patch": "收敛疯狂，选一个极具杀伤力的点深度引爆。", "skills": ["【被动】旧日秩序撕裂", "【法术】跨界降维骇入", "【光环】次元逻辑崩坏"], "base_roi": 1.65, "volatility": 0.60, "market_style": "高风险套利与颠覆性灾难做空", "evolution_path": ["L1 沙盒破坏者", "L2 跨界重组官"], "ultimate_evolution": "【秩序粉碎者】亲手书写下一个纪元"},
    "ENFJ": {"role": "黑市大主教", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 2.5%", "base_hash": 9350, "desc": "地下黑市的无冕之王，能通过恐怖的共识构建能力将佣兵聚拢为敢死队。", "tags": ["关系毒枭", "温情洗脑", "利益操盘"], "partner": "INFJ", "partner_advice": "汲取 INFJ 的深渊洞察作为弹药，由 ESFJ 转化为血契跟进单。", "tasks": ["构建辐射全网的非法服务联盟", "调解核心黑帮冲突"], "black_swan": "对盟友过度包容，处理叛徒时容易被虚假人情裹挟。", "patch": "引入无情的智能合约刚性处决指标。", "skills": ["【被动】绝对狂热结盟", "【光环】极客温情统御", "【战技】利益杠杆操盘"], "base_roi": 1.40, "volatility": 0.25, "market_style": "庞大资产池宏观操控与网络挟持", "evolution_path": ["L1 渠道统筹", "L2 联盟主理人"], "ultimate_evolution": "【引力黑洞】垄断全国巨头的绝对心智"},
    "ENFP": {"role": "废土布道者", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 8.1%", "base_hash": 8900, "desc": "充满感染力的暴乱火种，让每一场推介都变成市场崩溃的狂欢。", "tags": ["无限创意", "跨界煽动", "高频驱动"], "partner": "INFJ", "partner_advice": "在发散即将引发自爆时，务必听从 INFJ 的强行纠偏。", "tasks": ["领衔全网核心战区业务扫荡大循环", "主持面向千人的洗脑创新工坊"], "black_swan": "现场火热但无法转化为真实弹药，导致商业价值破产。", "patch": "引入严密的商机漏斗，把狂热变现为杀伤力。", "skills": ["【被动】群体狂热煽动", "【法术】全域流量吞噬", "【光环】异构资源强融"], "base_roi": 1.40, "volatility": 0.40, "market_style": "高波动狂热追逐与注意力收割", "evolution_path": ["L1 宣发先锋官", "L2 流量矩阵中枢"], "ultimate_evolution": "【无界基站】把控全域要素的流量高地"},
    "ISFJ": {"role": "避难所铁壁", "tier": "R", "tier_color": "#3b82f6", "rarity": "Top 13.8%", "base_hash": 8200, "desc": "最坚韧的底层肉盾，通过极致的损管控制支撑起整个军团的存活。", "tags": ["极限损管", "绝对防线", "不死肉盾"], "partner": "ESFJ", "partner_advice": "将外部战火交由 ESFJ 抵挡，您只需与 ISTJ 铸造叹息之墙。", "tasks": ["保障高压大额资金清算 0 宕机", "极速处理前线濒死的救援工单"], "black_swan": "默默承受过载的火力。可能在交易洪峰期因装甲爆表而阵亡。", "patch": "学会主动抗命，抛弃不必要的冗余防御。", "skills": ["【被动】极限装甲并发", "【法术】毫米级断肢重生", "【护盾】最后叹息之墙"], "base_roi": 1.10, "volatility": 0.08, "market_style": "极低回撤避险与无风险倒把策略", "evolution_path": ["L1 营地卫士", "L2 堡垒主管"], "ultimate_evolution": "【永动核心】维持军团生命线的最终坚盾"},
    "ESFJ": {"role": "八面玲珑掮客", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 12.3%", "base_hash": 8750, "desc": "超级连接器，游走在各大财团与反抗军之间，是阵地战的最强润滑剂。", "tags": ["协作掮客", "情报控制", "社会缓冲"], "partner": "ISFJ", "partner_advice": "在外长袖善舞时，把后勤安全交给 ISFJ。", "tasks": ["高频维护各方巨头的核心机密情报", "统筹地下黑市的资源调配大会"], "black_swan": "过度满足多方导致底线失守，签下丧权辱国的投降协议。", "patch": "建立独立的风控过滤网，谁敢越界就开枪。", "skills": ["【被动】政企超级链接", "【光环】社会化缓冲护盾", "【法术】多方仇恨均衡"], "base_roi": 1.20, "volatility": 0.15, "market_style": "庞大资金盘吸血与引导基金空手套白狼", "evolution_path": ["L1 见习掮客", "L2 黑市巨头"], "ultimate_evolution": "【政企超导桥梁】构筑不可替代的情报网护城河"},
    "ISTP": {"role": "暗夜拔线刺客", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 5.4%", "base_hash": 8950, "desc": "只对杀戮逻辑负责的幽灵，面对崩溃拔线即是真理。", "tags": ["物理切断", "硬核排爆", "极客杀手"], "partner": "ESTP", "partner_advice": "当 ESTP 在前线引来暴走仇恨时，由您负责底层直接拔线。", "tasks": ["执行核心设施的灾备抢修与物理破坏", "在炮火中执行机甲热更新"], "black_swan": "独狼作风。一旦陷入包围圈且通讯切断，极易被集火秒杀。", "patch": "将排雷经验写成防呆手册扔给炮灰。", "skills": ["【被动】致命物理拔线", "【法术】量子黑盒引爆", "【光环】超体极客杀意"], "base_roi": 1.35, "volatility": 0.35, "market_style": "黑天鹅事件狙击、困境反转与暴力破解", "evolution_path": ["L1 独狼猎兵", "L2 灾备指挥官"], "ultimate_evolution": "【代码幽灵】掌控国家机房的物理生命力"},
    "ISFP": {"role": "幻象编织者", "tier": "R", "tier_color": "#3b82f6", "rarity": "Top 8.8%", "base_hash": 8150, "desc": "在血腥战争中，用致幻的美学神经毒素瓦解敌人的战意。", "tags": ["视觉致幻", "感官剥夺", "体验巅峰"], "partner": "ESFP", "partner_advice": "将幻象炸弹交由 ESFP 在广场上引爆。", "tasks": ["重构敌方作战大盘的动态致幻渲染", "主导视觉洗脑体验升级"], "black_swan": "造出极其炫酷但无法击穿护甲的烟雾弹。", "patch": "在幻境中加入致命的木马负荷。", "skills": ["【被动】沉浸感官叙事", "【法术】低维美学抹杀", "【光环】心流深渊捕获"], "base_roi": 1.18, "volatility": 0.22, "market_style": "高奢非标资产与情绪致幻投资估值", "evolution_path": ["L1 幻觉特工", "L2 视觉暴君"], "ultimate_evolution": "【感官具象师】以一己之力拉升百倍幻象溢价"},
    "ESTP": {"role": "嗜血狂徒", "tier": "SSR", "tier_color": "#ffd700", "rarity": "Top 4.3%", "base_hash": 8800, "desc": "战线最前沿的敏锐猎手，能在枪林弹雨中嗅到暴利的机会。", "tags": ["野性直觉", "极速割喉", "实战暴徒"], "partner": "ISTP", "partner_advice": "尽情在前线厮杀，让 ISTP 为您提供最稳固的火力掩护。", "tasks": ["敏锐收割财团崩溃后的第一波物资红利", "针对敌对阵营发起极速闪电斩首"], "black_swan": "为了极速抢人头，踩中高爆地雷区，遭到毁灭性反噬。", "patch": "冲锋前先扔个探测器。", "skills": ["【被动】毫秒瞬时割喉", "【战技】全图火力覆盖", "【光环】血腥红利嗅探"], "base_roi": 1.50, "volatility": 0.50, "market_style": "超高频日内白刃战与极限突发利好嗜血收割", "evolution_path": ["L1 突击兵", "L2 战地狼王"], "ultimate_evolution": "【极速套利猎手】全网废土套利空间的绝杀狙击者"},
    "ESFP": {"role": "末日偶像", "tier": "SR", "tier_color": "#a855f7", "rarity": "Top 9.9%", "base_hash": 8300, "desc": "各大阵营争夺的前台形象窗口，一言一行足以左右全网军心。", "tags": ["全域魅惑", "舆情控制", "精神广播"], "partner": "ISFP", "partner_advice": "穿上 ISFP 为你打造的战袍，去前线开一场鼓舞士气的演唱会。", "tasks": ["在全网引爆最新型机甲的展会级宣发", "冲在第一线安抚溃败士兵的情绪"], "black_swan": "对外宣发时大嘴巴泄露了基地的坐标，引发灭顶之灾。", "patch": "把稿子背熟，不要即兴发挥。", "skills": ["【被动】全域舆论脑控", "【光环】情绪频率劫持", "【奥义】暴走危机降维"], "base_roi": 1.35, "volatility": 0.38, "market_style": "狂热粉丝驱动、社交网络暴动与情绪面收割", "evolution_path": ["L1 战地记者", "L2 精神领袖"], "ultimate_evolution": "【极速情绪信标】左右资本市场波动的首席发声端"}
}

def get_faction_info(mbti_code):
    if "NT" in mbti_code: return {"name": "硅基抵抗军", "element": "⚡ 量子", "color": "#00f3ff"}
    if "NF" in mbti_code: return {"name": "幽能清道夫", "element": "✨ 灵能", "color": "#a855f7"}
    if "SJ" in mbti_code: return {"name": "秩序裁决所", "element": "🛡️ 钢核", "color": "#10b981"}
    if "SP" in mbti_code: return {"name": "混沌暴徒", "element": "🔥 炎脉", "color": "#ff003c"}
    return {"name": "无界流浪者", "element": "🌌 暗物质", "color": "#ffffff"}

RELICS_POOL = [
    {"name": "【UR】中本聪的创世U盘", "rarity": "UR", "cp": 50000, "desc": "全属性巨幅飙升", "color": "#ff003c"},
    {"name": "【UR】V神的破碎怀表", "rarity": "UR", "cp": 45000, "desc": "掌控时间流动", "color": "#ff003c"},
    {"name": "【UR】奥本海默的密匙", "rarity": "UR", "cp": 48000, "desc": "核爆级战力加成", "color": "#ff003c"},
    {"name": "【SSR】破壁者的金库密钥", "rarity": "SSR", "cp": 20000, "desc": "剥夺对手利润", "color": "#ffd700"},
    {"name": "【SSR】统帅的暴走号角", "rarity": "SSR", "cp": 18000, "desc": "全员进入狂热状态", "color": "#ffd700"},
    {"name": "【SSR】量子裁决天平", "rarity": "SSR", "cp": 19000, "desc": "无视一切黑天鹅", "color": "#ffd700"},
    {"name": "【SR】局长的不锈钢杯", "rarity": "SR", "cp": 8000, "desc": "保持绝对冷血", "color": "#a855f7"},
    {"name": "【SR】极客的机械义眼", "rarity": "SR", "cp": 7500, "desc": "漏洞嗅探效率飙升", "color": "#a855f7"},
    {"name": "【SR】布道者的炽热火种", "rarity": "SR", "cp": 7000, "desc": "点燃市场 FOMO 情绪", "color": "#a855f7"},
    {"name": "【R】满是 Bug 的旧键盘", "rarity": "R", "cp": 3000, "desc": "敲击段落感清脆", "color": "#3b82f6"},
    {"name": "【R】特氟龙防粘平底锅", "rarity": "R", "cp": 2500, "desc": "完美反弹线上事故", "color": "#3b82f6"}
]

PETS_POOL = [
    {"name": "【UR】虚空量子猫", "rarity": "UR", "cp": 35000, "desc": "薛定谔的梦魇 | 核心暴击伤害飙升至 350%", "color": "#ff003c"},
    {"name": "【SSR】机械哈士奇", "rarity": "SSR", "cp": 25000, "desc": "绝对护主 | 行动体力消耗减半！", "color": "#ffd700"},
    {"name": "【SR】摸鱼寻宝狐", "rarity": "SR", "cp": 10000, "desc": "嗅觉灵敏 | 暗网远征掉落代币增加 50%", "color": "#a855f7"},
    {"name": "【R】电子监听游隼", "rarity": "R", "cp": 3000, "desc": "侦查增强 | 避风港质押挖矿附加额外利息", "color": "#3b82f6"}
]

CYBER_AUGMENTS = [
    {"id": "aug_spine", "name": "【反内卷神经切断器】", "cost": 100, "cp_mult": 1.15, "san_cost": 20, "desc": "物理改造：全战力 +15% / 永久扣除20理智上限"},
    {"id": "aug_heart", "name": "【聚变抗压心脏】", "cost": 300, "cp_mult": 1.30, "san_cost": 40, "desc": "物理改造：全战力 +30% / 永久扣除40理智上限"},
    {"id": "aug_eye",   "name": "【高维全视机械眼】", "cost": 800, "cp_mult": 1.50, "san_cost": 70, "desc": "物理改造：全战力 +50% / 永久扣除70理智上限"}
]

# ==============================================================================
# 🖥️ [ UI 07 ] 塔台级路由与全息渲染 (内联消除一切断层)
# ==============================================================================
if not st.session_state.started:
    safe_html("<div style='margin-top:50px;'></div>")
    if not st.session_state.boot_played:
        BOOT_CSS = "<style>.sys-boot-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #030408; z-index: 9999999; display: flex; justify-content: center; align-items: center; flex-direction: column; animation: sys-boot-fade 1.5s 2.2s cubic-bezier(0.8, 0, 0.2, 1) forwards; pointer-events: none; }.sys-boot-logo { color: #00f3ff; font-family: 'Orbitron', monospace; font-size: 24px; font-weight: 900; letter-spacing: 4px; overflow: hidden; border-right: 3px solid #00f3ff; white-space: nowrap; animation: typing-boot 0.8s steps(20, end) forwards, blink-boot 0.4s step-end infinite; margin-bottom: 15px; text-shadow: 0 0 20px #00f3ff; }.sys-boot-bar-bg { width: 300px; height: 2px; background: rgba(0,243,255,0.2); position: relative; }.sys-boot-bar-fill { position: absolute; top: 0; left: 0; height: 100%; background: #00f3ff; box-shadow: 0 0 15px #00f3ff; animation: load-boot 1.8s ease-out forwards; }.sys-boot-logs { margin-top: 15px; font-family: 'Fira Code', monospace; font-size: 10px; color: #10b981; opacity: 0.8; height: 45px; overflow: hidden; width: 300px; text-align: left; line-height: 15px; }.log-line { animation: log-scroll 1.8s steps(10, end) forwards; transform: translateY(45px); }@keyframes typing-boot { from { width: 0; } to { width: 300px; } }@keyframes blink-boot { 50% { border-color: transparent; } }@keyframes load-boot { 0% { width: 0%; } 10% { width: 30%; } 40% { width: 40%; } 60% { width: 80%; } 100% { width: 100%; } }@keyframes sys-boot-fade { to { opacity: 0; visibility: hidden; } }@keyframes log-scroll { 100% { transform: translateY(-100px); } }</style>"
        safe_html(BOOT_CSS.replace('\n', '') + "<div class=\"sys-boot-overlay\"><div class=\"sys-boot-logo\">OMNIVERSE_CORE_V42</div><div class=\"sys-boot-bar-bg\"><div class=\"sys-boot-bar-fill\"></div></div><div class=\"sys-boot-logs\"><div class=\"log-line\">[SYS] Booting Ecosystem Fusion...<br>[SYS] Connecting to Global Matrix...<br>[SYS] Linking Talent Nodes...<br>[SYS] Spawning War Pets...<br>[OK] Handshake Established.</div></div></div>")
        st.session_state.boot_played = True

    with center_container():
        safe_html("<div style=\"text-align: center; margin-bottom: 20px;\"><div style=\"color:#00f3ff; font-family:'Orbitron', monospace; font-size:14px; letter-spacing:8px; margin-bottom:10px;\">SHANGHAI DATA EXCHANGE</div><h1 class=\"hero-title\" data-text=\"终极纪元 V42\">终极纪元 V42</h1><div style=\"color:#a855f7; font-family:'Orbitron', sans-serif; font-size:13px; font-weight:900; letter-spacing:6px; margin-bottom:30px; margin-top:5px;\">IMMORTAL_GOD_MODE</div></div>")
        safe_html("<div style=\"background: rgba(4, 9, 20, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: clamp(15px, 4vw, 25px); border-radius: 8px; font-family: 'Fira Code', monospace; font-size: clamp(12px, 3vw, 14px); color: #e2e8f0; box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 30px;\"><div style=\"color:#10b981; margin-bottom:5px;\">[SYSTEM] Securing root connection... <span style=\"color:#00f3ff;\">[CONNECTED]</span></div><div style=\"color:#10b981;\">[KERNEL] Loading Ecosystem Matrix V42... <span style=\"color:#00f3ff;\">[READY]</span></div><div style=\"margin-top:15px; font-family: 'Noto Sans SC', sans-serif; line-height: 1.8; color:#fff;\"><b>万物互联的职场生态纪元已经降临。</b><br>一切行为皆有因果。天赋、宠物、污染度与天气将形成紧密的齿轮效应。<br>系统将为您空投一张独一无二的<b>高阶职场算力实体卡牌 (SBT)</b>，努力活下去吧！</div></div>")
        with st.form(key="login_form", border=False):
            safe_html("<div style='color:#00f3ff; font-family:\"Orbitron\", sans-serif; font-size:12px; font-weight:bold; margin-bottom:8px; text-align:center;'>▼ 登记神经元代号 (MOUNT_NODE) ▼</div>")
            st.text_input("", key="login_input", placeholder="输入您的职场代号", label_visibility="collapsed")
            safe_html("<br>")
            st.form_submit_button("▶ 开启神经元接驳并呼叫空投", on_click=start_assessment_callback, type="primary", use_container_width=True)

elif st.session_state.calculating:
    with center_container():
        safe_html("<h2 class='hero-title' data-text='[ ZK-PROOF UNSEALING... ]' style='font-size:clamp(20px, 4vw, 28px) !important; margin-top:50px; text-align:center; display:block; color:#00f3ff !important;'>[ ZK-PROOF UNSEALING... ]</h2>")
        mint_box = st.empty()
        phases = ["[SYNCING EVM]", "[EXTRACTING DATA]", "[ZK-PROOF]", "[WEAPONIZING CARDS]"]
        h_logs = ""
        for i in range(12):
            fake_hash = hashlib.sha256(str(random.random()).encode()).hexdigest().upper()
            h_logs = "<span style='color:#94a3b8;'>" + phases[i % 4] + "</span> <span style='color:#00f3ff;'>0x" + fake_hash[:24] + "...</span> <span style='color:#10b981;'>[OK]</span><br>" + h_logs
            mint_box.markdown("<div style='background:#030408; border:1px solid #002233; border-left:4px solid #00f3ff; padding:20px; border-radius:8px; font-family:monospace; font-size:13px; height:250px; overflow:hidden; color:#10b981; box-shadow: inset 0 0 20px rgba(0,243,255,0.1);'>" + h_logs + "</div>", unsafe_allow_html=True)
            time.sleep(0.15)
        st.session_state.calculating = False; st.rerun()

elif st.session_state.current_q < len(questions):
    with st.sidebar:
        safe_html("<div style='text-align:center; font-family:Orbitron; font-size:20px; font-weight:900; color:#00f3ff; margin-bottom:20px; text-shadow: 0 0 10px #00f3ff;'>ECO HUD</div>")
        safe_html("<div class='hud-box'><div class='hud-title'>[ SURVIVOR ID ]</div><div class='hud-val' style='color:#fff;'>" + st.session_state.user_alias + "</div></div>")
        safe_html("<div class='hud-box'><div class='hud-title'>[ SYSTEM SYNC ]</div><div class='hud-val' style='color:#10b981; animation: blink 1s infinite;'>IN PROGRESS...</div></div>")
        
    with center_container():
        q_data = questions[st.session_state.current_q]
        module_name = {"E": "外联生态网络", "S": "颗粒实务穿透", "T": "量化护甲屏障", "J": "秩序规则锚定"}.get(q_data['dim'])
        dynamic_hash = hashlib.sha256(("BLOCK_" + str(st.session_state.current_q) + "_" + q_data['q']).encode()).hexdigest()[:10].upper()
        
        safe_html("<div style='padding-top:10px;'></div>")
        progress_val = (st.session_state.current_q + 1) / len(questions)
        st.progress(progress_val)
        safe_html("<div style='text-align:right; font-family:Orbitron, monospace; color:#00f3ff; font-size:12px; margin-top:5px; font-weight:bold;'>SYNC RATE: " + str(int(progress_val*100)) + "%</div>")
        
        safe_html("<div style=\"background: rgba(4, 9, 20, 0.9); border: 2px solid rgba(0, 243, 255, 0.4); border-radius: 12px; padding: clamp(20px, 4vw, 30px); box-shadow: 0 10px 30px rgba(0,0,0,0.9), inset 0 0 30px rgba(0, 243, 255, 0.1); margin-top: 20px; margin-bottom: 30px;\"><div style=\"display:flex; justify-content:space-between; font-family:monospace; color:#00f3ff; font-size:11px; margin-bottom:15px; border-bottom: 1px dashed rgba(0,243,255,0.3); padding-bottom:10px;\"><span style=\"font-family:'Orbitron', sans-serif;\">MOD: " + module_name + "</span><span style=\"font-family:'Orbitron', sans-serif;\">HASH: 0x" + dynamic_hash + "</span></div><div style=\"font-size: clamp(15px, 4vw, 18px); color: #ffffff !important; line-height: 1.8; font-weight: 700;\">" + q_data['q'] + "</div></div>")
        
        opts = [("🚫 强制阻断 (找死)", 1), ("⚠️ 战术规避 (抗拒)", 2), ("⚖️ 视境判定 (看情况保命)", 3), ("🤝 残酷执行 (常用)", 4), ("🔒 绝对信仰 (死忠)", 5)]
        for text, val in opts: 
            st.button(text, key="q_" + str(st.session_state.current_q) + "_" + str(val), on_click=answer_callback, args=(val, q_data['dim']), use_container_width=True)

else:
    # ==========================
    # V42 终极生态大一统演算与渲染
    # ==========================
    res = st.session_state.total_scores
    mbti = ("E" if res.get("E", 0) >= 0 else "I") + ("S" if res.get("S", 0) >= 0 else "N") + ("T" if res.get("T", 0) >= 0 else "F") + ("J" if res.get("J", 0) >= 0 else "P")
    data = mbti_details.get(mbti, mbti_details["INTJ"])
    faction_data = get_faction_info(mbti)
    
    tier_level = "MR" if st.session_state.ascended else data.get('tier', 'SR')
    tier_color = "#00f3ff" if st.session_state.ascended else data.get('tier_color', '#a855f7')
    border_color = "#ffffff" if st.session_state.ascended else data.get('tier_color', '#a855f7')
    role_name = data.get('role', '未知节点')
    safe_alias_final = st.session_state.user_alias.upper()
    
    if not st.session_state.anim_played: 
        st.balloons()
        glow_color = "#ffffff" if st.session_state.ascended else ("#ff003c" if tier_level == "UR" else ("#ffd700" if tier_level == "SSR" else "#00f3ff"))
        GACHA_CSS = "<style>.gacha-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(3,4,8,0.98); z-index: 999999; display: flex; justify-content: center; align-items: center; flex-direction: column; animation: cyber-fadeout 3.5s cubic-bezier(0.8, 0, 0.2, 1) forwards; pointer-events: none; backdrop-filter: blur(8px); }.gacha-cube { width: 80px; height: 80px; border: 4px solid #fff; box-shadow: 0 0 20px #fff, inset 0 0 20px #fff; transform: rotate(45deg); animation: cube-shake 2s ease-in forwards, cube-burst 0.5s 2s forwards; position: relative; }.gacha-cube::after { content:''; position: absolute; top:0; left:0; width:100%; height:100%; background: " + glow_color + "; opacity:0; animation: cube-glow 2s forwards; }.gacha-text { font-family: 'Orbitron', sans-serif; font-size: clamp(24px, 5vw, 64px); font-weight: 900; color: #fff; letter-spacing: 12px; opacity: 0; animation: pop-in 1.5s 2s cubic-bezier(0.1, 0.8, 0.3, 1) forwards; position: relative; z-index: 2; margin-top: 60px; text-transform: uppercase; text-shadow: 0 0 40px " + glow_color + ", 0 0 80px " + glow_color + "; }@keyframes cube-shake { 0% { transform: rotate(45deg) scale(1); } 80% { transform: rotate(405deg) scale(1.2); border-color: " + glow_color + "; box-shadow: 0 0 40px " + glow_color + "; } 100% { transform: rotate(405deg) scale(0.1); opacity: 0; } }@keyframes cube-glow { 80% { opacity: 0.8; } 100% { opacity: 1; } }@keyframes cube-burst { 0% { transform: scale(0.1); opacity: 1; box-shadow: 0 0 100px 50px " + glow_color + "; } 100% { transform: scale(15); opacity: 0; box-shadow: 0 0 0 0 transparent; } }@keyframes pop-in { 0% { transform: scale(0.5); opacity: 0; } 40% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(1); opacity: 1; } }@keyframes cyber-fadeout { 0%, 85% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }</style>"
        safe_html(GACHA_CSS + "<div class='gacha-overlay'><div class='gacha-cube'></div><div class='gacha-text'>ECOSYSTEM LINKED<br>" + tier_level + " UNLOCKED</div></div>")
        st.session_state.anim_played = True
        
    full_title = st.session_state.equipped_title + " " + role_name
    
    def get_intensity(score): return int(max(0, min(100, 50 + (score * 2.5))))
    val_E = get_intensity(res.get("E", 0)); val_I = 100 - val_E
    val_S = get_intensity(res.get("S", 0)); val_N = 100 - val_S
    val_T = get_intensity(res.get("T", 0)); val_F = 100 - val_T
    val_J = get_intensity(res.get("J", 0)); val_P = 100 - val_J

    categories = ['输出(E)', '精准(S)', '护甲(T)', '秩序(J)', '隐匿(I)', '视界(N)', '共情(F)', '敏捷(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]

    p_score = -res.get("J", 0); s_score = res.get("S", 0)
    risk_score = int(max(5, min(95, 50 + (p_score * 1.5) - (s_score * 1.5))))
    if risk_score < 35: r_tag, r_color = "城墙级绝对防线", "#10b981"
    elif risk_score < 65: r_tag, r_color = "动态灰度平衡", "#ffd700"
    else: r_tag, r_color = "疯狗级极限破局", "#ff003c"

    time_taken = max(1.0, st.session_state.end_time - st.session_state.start_time)
    h_code_gen = hashlib.sha256((safe_alias_final + mbti + str(time_taken) + VERSION).encode()).hexdigest().upper()
    h_int_gen = int(h_code_gen[:8], 16)
    
    if "asset_minted" not in st.session_state or st.session_state.asset_minted.get("version") != VERSION:
        avg_q_time = time_taken / len(questions)
        dec_index = int(min(99, max(35, 100 - (max(0, avg_q_time - 2.5) * 5))))
        extremity_score = sum(abs(v) for v in res.values()) / 80.0
        random_factor = 0.9 + (h_int_gen % 200) / 1000.0
        
        computed_base_cp = int(data.get('base_hash', 8000) * (1 + extremity_score * 0.4) * (0.8 + (dec_index/100.0) * 0.5) * random_factor * 10000)
        computed_pct_beat = round(min(99.9, max(50.0, 60 + (dec_index * 0.3) + (extremity_score * 20))), 1)
        d_arr_gen, roi_arr_gen = generate_alpha_curve(data.get('base_roi', 1.35), data.get('volatility', 0.35), int(h_code_gen[:6], 16))
        
        st.session_state.asset_minted = {
            "version": VERSION,
            "hash_code": h_code_gen,
            "mbti": mbti,
            "block_height": "V42-" + str((int(time.time()) % 1000000)).zfill(6),
            "time_str": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "token_id": int(hashlib.md5((safe_alias_final + str(time_taken)).encode()).hexdigest()[:8], 16),
            "contract_addr": "0x" + hashlib.sha256(("contract_" + mbti + "_" + str(h_int_gen)).encode()).hexdigest()[:38],
            "base_cp": computed_base_cp,
            "pct_beat": computed_pct_beat,
            "d_arr": d_arr_gen,
            "roi_arr": roi_arr_gen,
            "bids_html": generate_bids(h_int_gen),
            "decisiveness": dec_index
        }
        
    asset = st.session_state.asset_minted
    hash_code = asset["hash_code"]
    block_height = asset["block_height"]
    current_time_str = asset["time_str"]
    token_id = asset["token_id"]
    contract_addr = asset["contract_addr"]
    base_cp = asset["base_cp"]
    pct_beat = asset["pct_beat"]
    d_arr = asset["d_arr"]
    roi_arr = asset["roi_arr"]
    bids_html = asset["bids_html"]
    card_foil = st.session_state.card_foil
    h_int = int(hash_code[:8], 16)
    
    # === 寰宇级战力结算算法 ===
    sys_mults = get_stat_multipliers()
    
    relic_cp_total = sum([r.get('cp', 0) for r in st.session_state.equipped_relics])
    pet_cp_total = st.session_state.equipped_pet.get('cp', 0) if st.session_state.equipped_pet else 0
    
    ur_count = sum(1 for r in st.session_state.equipped_relics if r['rarity'] == 'UR')
    if ur_count >= 3: set_bonus_cp = 200000
    elif ur_count >= 2: set_bonus_cp = 50000
    else: set_bonus_cp = 0
    
    talent_cp_total = sum(st.session_state.talent_levels.values()) * 5000
    lvl_m = 1.0 + (st.session_state.level - 1) * 0.05
    asc_m = 1.0 + (st.session_state.ascension_stars * 0.25)
    
    aug_m = 1.0
    aug_html_str = ""
    for aug in CYBER_AUGMENTS:
        if aug['id'] in st.session_state.cyber_augments:
            aug_m *= aug['cp_mult']
            aug_html_str += "<span style='display:inline-block; font-size:10px; color:#ff003c; border:1px solid #ff003c; background:rgba(255,0,60,0.1); padding:2px 5px; margin-right:5px; border-radius:2px; margin-bottom:5px;'>🦾 " + aug['name'] + "</span>"

    foil_mult = 1.0
    if "碎冰" in card_foil: foil_mult = 1.1
    elif "反转" in card_foil: foil_mult = 1.25
    elif "幻彩" in card_foil: foil_mult = 1.5

    squad_mult = 1.0
    if st.session_state.squad[0] and st.session_state.squad[1]:
        squad_mult = 1.2
        f1 = get_faction_info(st.session_state.squad[0])
        f2 = get_faction_info(st.session_state.squad[1])
        if faction_data['element'] == f1['element'] == f2['element']:
            squad_mult = 1.5 
    
    despair_m = 1.0
    despair_buff_str = ""
    if st.session_state.despair_level > 80:
        despair_m = 0.5 
        despair_buff_str = "<div style='color:#ff003c; font-size:10px; font-weight:bold; margin-top:5px; animation:blink 0.5s infinite;'>💀 基因崩溃: 战力强制减半 (-50%)</div>"
    elif st.session_state.despair_level >= 40:
        despair_m = 1.2
        despair_buff_str = "<div style='color:#ffd700; font-size:10px; font-weight:bold; margin-top:5px;'>🔥 绝境狂暴: 战力极度虚高 (+20%)</div>"

    raw_cp = (base_cp + relic_cp_total + pet_cp_total + talent_cp_total + set_bonus_cp) * lvl_m * asc_m * aug_m * foil_mult * squad_mult * despair_m
    
    faction_mult = 1.0
    faction_buff_str = ""
    if st.session_state.joined_faction and st.session_state.joined_faction in faction_data['name']:
        faction_mult = 1.1
        faction_buff_str = "<div style='color:#10b981; font-size:10px; font-weight:bold; margin-top:5px;'>🛡️ 阵营本命觉醒: ACTIVE (+10% CP)</div>"

    weather_mult = 1.0
    weather_buff_str = ""
    if ("量子" in st.session_state.weather and "量子" in faction_data['element']) or \
       ("灵能" in st.session_state.weather and "灵能" in faction_data['element']) or \
       ("钢核" in st.session_state.weather and "钢核" in faction_data['element']) or \
       ("炎脉" in st.session_state.weather and "炎脉" in faction_data['element']):
        weather_mult = 1.3
        weather_buff_str = "<div style='color:#ffd700; font-size:10px; font-weight:bold; margin-top:5px; animation:blink 1.5s infinite;'>⛈️ 天象极速共鸣: ACTIVE (+30% CP)</div>"

    final_cp = int(raw_cp * faction_mult * weather_mult)
    st.session_state.final_cp_cache = final_cp
    
    rank_name, rank_color = get_rank_tier(final_cp)
    valuation_str = "{:,}".format(final_cp)
    pct_beat_final = min(99.99, pct_beat + (st.session_state.level * 0.1) + (st.session_state.ascension_stars * 1.5))
    
    svg_icon = get_identicon_html(hash_code, border_color)
    stars_html = "".join(["★" for _ in range(st.session_state.ascension_stars)])
    stars_display = "<span style='color:#ffd700; margin-left:10px; font-size:18px;'>" + stars_html + "</span>" if stars_html else ""

    # =========================================================================
    # 🕹️ 左侧 HUD (寰宇仪表盘)
    # =========================================================================
    with st.sidebar:
        safe_html("<div style='text-align:center; font-family:Orbitron; font-size:20px; font-weight:900; color:#00f3ff; margin-bottom:20px;'>ECO HUD V42</div>")
        safe_html("<div class='hud-box'><div class='hud-title'>SURVIVAL DAY [" + str(st.session_state.turn_count) + "] - 环境状况</div><div style='color:#ffd700; font-size:12px; font-weight:bold;'>" + st.session_state.weather + "</div></div>")
        
        despair_color = "#10b981" if st.session_state.despair_level < 40 else ("#ffd700" if st.session_state.despair_level < 80 else "#ff003c")
        despair_text = "理智尚存 (0-39)" if st.session_state.despair_level < 40 else ("绝境边缘 (战力+20%)" if st.session_state.despair_level < 80 else "基因崩溃 (战力减半/熔炉易爆)")
        safe_html("<div class='hud-box' style='border-color:" + despair_color + ";'><div class='hud-title' style='color:" + despair_color + ";'>[ DESPAIR (污染度): " + str(st.session_state.despair_level) + "% ]</div><div style='color:" + despair_color + "; font-size:11px; font-weight:bold;'>" + despair_text + "</div><div style='background:rgba(255,255,255,0.1); height:4px; margin-top:5px;'><div style='background:" + despair_color + "; width:" + str(st.session_state.despair_level) + "%; height:100%; transition: width 0.5s;'></div></div></div>")

        idx = st.session_state.titles_owned.index(st.session_state.equipped_title) if st.session_state.equipped_title in st.session_state.titles_owned else 0
        st.selectbox("佩戴军衔:", st.session_state.titles_owned, index=idx, key="title_sel", label_visibility="collapsed", on_change=equip_title_callback)

        safe_html("<div class='hud-box'><div class='hud-title'>[ ALIAS ]</div><div class='hud-val' style='color:#fff;'>" + safe_alias_final + stars_display + "</div></div>")
        safe_html("<div class='hud-box' style='margin-top:15px;'><div class='hud-title'>[ WAR TIER ]</div><div class='hud-val' style='color:" + rank_color + "; font-size:16px;'>" + rank_name + "</div></div>")
        safe_html("<div class='hud-box'><div class='hud-title'>[ LEVEL ]</div><div class='hud-val' style='color:#a855f7;'>Lv. " + str(st.session_state.level) + "</div><div style='background:rgba(255,255,255,0.1); height:4px; margin-top:5px;'><div style='background:#a855f7; width:" + str(min(100, st.session_state.exp / (st.session_state.level * 100) * 100)) + "%; height:100%;'></div></div></div>")
        
        stam_color = "#10b981" if st.session_state.stamina > 30 else "#ff003c"
        safe_html("<div class='hud-box'><div class='hud-title'>[ STAMINA (体力) ]</div><div class='hud-val' style='color:" + stam_color + ";'>" + str(st.session_state.stamina) + " / 150</div></div>")
        
        sanity_color = "#00f3ff" if st.session_state.sanity > 50 else "#ff003c"
        safe_html("<div class='hud-box'><div class='hud-title'>[ SAN (理智) ]</div><div class='hud-val' style='color:" + sanity_color + ";'>" + str(st.session_state.sanity) + " / " + str(st.session_state.max_sanity) + "</div></div>")
        
        gpu_str = " (+" + str(int(st.session_state.gpus * 150 * sys_mults['yield_mult'])) + "/回合)" if st.session_state.gpus > 0 else ""
        safe_html("<div class='hud-box'><div class='hud-title'>[ WAR FUNDS (SDE 战备金) ]</div><div class='hud-val' style='color:#ffd700;'>" + "{:,}".format(int(st.session_state.tokens)) + " 🪙</div><div style='font-size:9px; color:#10b981; margin-top:5px;'>矿机: " + str(st.session_state.gpus) + " 台" + gpu_str + "</div></div>")
        
        safe_html("<div class='hud-box' style='border-color:#a855f7;'><div class='hud-title' style='color:#a855f7;'>[ PREMIUM ASSETS ]</div><div style='color:#fff; font-size:12px; font-weight:bold; margin-bottom:4px;'>🌑 暗物质: " + "{:,}".format(st.session_state.dark_matter) + "</div><div style='color:#fff; font-size:12px; font-weight:bold;'>💠 逻辑碎片: " + "{:,}".format(st.session_state.logic_shards) + "</div></div>")
        
        ach_html = "".join(["<span class='achieve-badge'>" + a + "</span>" for a in st.session_state.achievements])
        if ach_html: safe_html("<div class='hud-box'><div class='hud-title'>[ ACHIEVEMENTS ]</div><div>" + ach_html + "</div></div>")
        
        if st.session_state.staked_tokens > 0:
            safe_html("<div class='hud-box' style='border-color:#3b82f6;'><div class='hud-title' style='color:#3b82f6;'>[ LAUNDERED POOL ]</div><div class='hud-val' style='color:#00f3ff; font-size:14px;'>+ " + "{:,}".format(int(st.session_state.yield_pool)) + " 🪙</div></div>")
            st.button("📤 提取洗白资金", on_click=claim_yield_callback, use_container_width=True)
            
        c_act1, c_act2 = st.columns(2)
        with c_act1: st.button("🛌 休眠(500)", on_click=cb_sleep, use_container_width=True)
        with c_act2: st.button("🚿 净化(4k)", on_click=cb_purify, use_container_width=True)
            
        safe_html("<div style='font-family:Orbitron; font-size:11px; font-weight:bold; color:#00f3ff; margin-top:30px; margin-bottom:10px; border-bottom:1px solid #334155; padding-bottom:5px;'>/// WORLD CHAT ///</div>")
        safe_html("<div style='font-family:\"Noto Sans SC\", sans-serif; font-size:11px; line-height:1.6; max-height: 250px; overflow-y: hidden;'>" + "<br>".join(st.session_state.world_chat[:20]) + "</div>")

    # =========================================================================
    # 📱【主面板 13 大主控终端】
    # =========================================================================
    safe_html("<div style='background: linear-gradient(135deg, rgba(0,243,255,0.1), rgba(10,15,30,0.9)); border: 1px solid #00f3ff; border-radius: 8px; padding: 15px 25px; margin-bottom: 25px; font-family: \"Orbitron\", monospace; box-shadow: 0 0 20px rgba(0,243,255,0.2);'><div style='color: #00f3ff; font-size: 14px; font-weight: bold; border-bottom: 1px dashed #00f3ff; padding-bottom: 10px; margin-bottom: 12px;'>🏆 ECOSYSTEM CARD MINTED [ FUSION MODE ]</div><div style='font-size: 12px; color: #94a3b8; display:flex; justify-content: space-between;'><div>BLOCK: " + block_height + "</div><div>ID: #" + str(token_id) + "</div></div><div style='margin-top:10px; font-size:11px; color:#10b981; font-family:\"Noto Sans SC\";'>【核心法则】远征得碎片 -> 升级天赋 -> 打怪得暗物质 -> 提升星级工艺 -> 暴增战力掠夺全网！</div></div>")

    t_dash, t_combat, t_dispatch, t_growth, t_gacha, t_inv, t_aug, t_econ, t_altar, t_syn, t_data, t_oracle, t_mint = st.tabs([
        "🖥️ 战地大盘", "⚔️ 征战深渊(产暗物质)", "🗺️ 暗网远征(产碎片)", "🧬 潜能突破", "🎰 黑箱召唤", "🎒 军火行囊", "🦾 义体改造", 
        "🏦 黑市帝国", "🩸 禁忌祭坛", "🤝 战术小队", "📊 战场态势", "🤖 神谕降临", "📸 抽离卡砖"
    ])

    with t_dash:
        safe_html("<div class='eco-glance' style='background: linear-gradient(180deg, rgba(4,9,20,0.9), rgba(3,4,8,0.9)); border: 1px solid rgba(0,243,255,0.4); border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: inset 0 0 30px rgba(0,243,255,0.1);'><div style='color:#00f3ff; font-family:Orbitron; font-weight:bold; border-bottom:1px dashed #00f3ff; padding-bottom:10px; margin-bottom:10px;'>/// ECOSYSTEM RESONANCE ENGINE ///</div><div style='font-size:14px; color:#e2e8f0; line-height:1.8;'><b>生态战力演算流：</b><br>基础算力 (" + "{:,}".format(base_cp) + ") + 军火加成 (" + "{:,}".format(relic_cp_total) + ") + 宠物加成 (" + "{:,}".format(pet_cp_total) + ") + 天赋加成 (" + "{:,}".format(talent_cp_total) + ") + 套装共鸣 (" + "{:,}".format(set_bonus_cp) + ")<br>✖️ 等级 (" + str(round(lvl_m,2)) + ") ✖️ 星级 (" + str(round(asc_m,2)) + ") ✖️ 义体 (" + str(round(aug_m,2)) + ") ✖️ 污染 (" + str(round(despair_m,2)) + ") ✖️ 工艺 (" + str(round(foil_mult,2)) + ") ✖️ 小队 (" + str(round(squad_mult,2)) + ") ✖️ 阵营 (" + str(round(faction_mult,2)) + ") ✖️ 天象 (" + str(round(weather_mult,2)) + ")<br>🟰 <b>最终战力：<span style='color:#ffd700; font-size:20px;'>" + "{:,}".format(final_cp) + " CP</span></b></div></div>")
        
        col_l, col_m, col_r = st.columns([1.2, 1.1, 1.1], gap="medium")
        with col_l:
            tags_html_web = "".join(["<span style='background:rgba(0, 243, 255, 0.1); color:#00f3ff !important; border:1px solid rgba(0,243,255,0.4); padding:6px 14px; border-radius:2px; font-size:13px; font-weight:900; margin:4px; display:inline-block; font-family:\"Noto Sans SC\";'>" + t + "</span>" for t in data.get('tags', [])])
            skills_html_web = "".join(["<div style='background:linear-gradient(90deg, rgba(0,243,255,0.2), transparent); border:1px solid rgba(0,243,255,0.5); border-left:4px solid #00f3ff; padding:8px 12px; border-radius:2px; font-size:13px; color:#fff; font-weight:bold; margin-bottom:8px; text-align:left;'>" + s + "</div>" for s in data.get('skills', [])])
            tier_bg = tier_color if st.session_state.ascended else tier_color + "55"
            
            foil_css = ""
            if "碎冰" in card_foil: foil_css = "background: linear-gradient(125deg, transparent 20%, rgba(255,255,255,0.8) 40%, rgba(0,243,255,0.8) 50%, rgba(168,85,247,0.8) 60%, transparent 80%); mix-blend-mode: color-dodge;"
            elif "反转" in card_foil: foil_css = "background: linear-gradient(125deg, transparent 20%, rgba(0,0,0,0.9) 40%, rgba(255,0,60,0.8) 50%, rgba(0,0,0,0.9) 60%, transparent 80%); mix-blend-mode: multiply;"
            elif "幻彩" in card_foil: foil_css = "background: linear-gradient(125deg, transparent 20%, rgba(255,215,0,0.8) 40%, rgba(255,255,255,0.9) 50%, rgba(0,243,255,0.8) 60%, transparent 80%); mix-blend-mode: overlay;"
            else: foil_css = "background: linear-gradient(125deg, transparent 20%, rgba(255,255,255,0.2) 40%, rgba(0,243,255,0.5) 50%, rgba(0,0,0,0.4) 60%, transparent 80%); mix-blend-mode: color-dodge;"
            
            set_bonus_html = "<div style='margin-top:10px; font-size:11px; color:#ffd700; font-weight:bold; animation: blink 1.5s infinite;'>🔥 [UR套装共鸣] 触发！战力极其膨胀！</div>" if set_bonus_cp > 0 else ""
            squad_bonus_html = "<div style='margin-top:5px; font-size:11px; color:#00f3ff; font-weight:bold;'>🤝 [小队阵列] 激活战力倍率！</div>" if squad_mult > 1.0 else ""
            
            CARD_CSS = "<style>.tcg-card-container { perspective: 1500px; width: 100%; margin-bottom: 20px; display: flex; justify-content: center; z-index: 50; position: relative; }.tcg-card { width: 100%; max-width: 480px; position: relative; transform-style: preserve-3d; transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1); border-radius: 8px; box-shadow: 0 30px 60px rgba(0,0,0,0.9), 0 0 40px rgba(0,243,255,0.2); background: #0b0505; border: 2px solid " + border_color + "; overflow: hidden; }.tcg-card:hover { transform: rotateY(8deg) rotateX(-5deg) translateY(-10px) scale(1.02); box-shadow: -20px 40px 80px rgba(0,0,0,0.9), 0 0 60px " + border_color + "88; }.tcg-card::after { content: \"\"; position: absolute; inset: 0; " + foil_css + " background-size: 250% 250%; background-position: 100% 100%; pointer-events: none; transition: background-position 0.8s ease; z-index: 20; opacity: 0; }.tcg-card:hover::after { background-position: 0% 0%; opacity: 1; }.card-content { position: relative; z-index: 2; padding: clamp(25px, 6vw, 40px) clamp(20px, 5vw, 30px); text-align: center; }.card-header-bg { position: absolute; top: 0; left: 0; width: 100%; height: 160px; background: linear-gradient(180deg, " + tier_bg + " 0%, transparent 100%); z-index: 1; border-bottom: 1px solid rgba(255,255,255,0.05); }.tcg-mbti { font-family: 'Orbitron', sans-serif !important; font-size: clamp(65px, 12vw, 90px); font-weight: 900; color: #ffffff !important; line-height: 1; letter-spacing: 8px; text-shadow: 0 0 40px " + border_color + ", 0 5px 0px #000; margin: 10px 0; position: relative; z-index: 5; }.tcg-role { font-size: clamp(20px, 5vw, 24px); font-weight: 900; color: #ffd700 !important; margin: 10px 0 25px 0; letter-spacing: 3px; position: relative; z-index: 5; text-shadow: 0 0 20px rgba(255,215,0,0.5); }.tcg-rarity-badge { position: absolute; top: 25px; right: -50px; background: " + tier_color + "; color: #000; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 14px; padding: 6px 55px; transform: rotate(45deg); z-index: 15; letter-spacing: 3px; box-shadow: 0 5px 20px rgba(0,243,255,0.8); border: 1px solid #fff; }.tcg-stats-box { display: flex; justify-content: space-between; gap: 15px; margin-bottom: 25px; position: relative; z-index: 5; }.tcg-stat-item { flex: 1; background: rgba(0,0,0,0.8); border: 1px solid rgba(0,243,255,0.4); border-radius: 4px; padding: 15px 10px; box-shadow: inset 0 0 20px rgba(0,243,255,0.1); backdrop-filter: blur(5px); }.tcg-stat-title { font-size: 11px; color: #94a3b8; font-family: 'Orbitron', monospace; margin-bottom: 8px; letter-spacing: 1px; }.tcg-stat-val { font-size: clamp(22px, 5vw, 26px); color: #00f3ff; font-weight: 900; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 15px rgba(0,243,255,0.8); }</style>"
            
            HTML_CARD = CARD_CSS.replace('\n', '') + "<div class=\"tcg-card-container\"><div class=\"tcg-card\"><div class=\"card-header-bg\"></div><div class=\"card-content\"><div class=\"tcg-rarity-badge\">" + tier_level + "</div><div style=\"position:relative; z-index:5; display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom:10px;\"><div style=\"font-family:'Orbitron', monospace; font-size:11px; color:#94a3b8; letter-spacing:4px;\">LV." + str(st.session_state.level) + " MERCENARY</div><div style=\"font-size:12px; font-weight:bold; color:" + faction_data['color'] + "; text-shadow: 0 0 5px " + faction_data['color'] + ";\">" + faction_data['element'] + "</div></div><div style=\"position:relative; z-index:5; display:flex; justify-content:center; align-items:center; gap:15px; margin-bottom:5px;\">" + svg_icon + "<div style=\"color:#ffffff; font-family:'Orbitron', monospace; font-size:20px; font-weight:bold; letter-spacing:2px; text-shadow: 0 0 10px rgba(255,255,255,0.5);\">" + safe_alias_final + stars_display + "</div></div><div class=\"tcg-mbti\">" + mbti + "</div><div style=\"position:relative; z-index:5; text-align:center;font-size:12px;color:#94a3b8;margin-bottom:10px; font-family:'Orbitron';\">FOIL: <span style=\"color:" + border_color + ";font-weight:bold;font-size:14px;\">" + card_foil + "</span></div><div style=\"position:relative; z-index:5; display:flex; justify-content:center; gap:10px; margin-bottom:10px;\"><span style=\"background:rgba(255,255,255,0.1); border:1px solid #94a3b8; padding:3px 10px; border-radius:15px; font-size:10px; font-weight:bold;\">" + faction_data['name'] + "</span></div><div class=\"tcg-role\">" + full_title + "</div><div class=\"tcg-stats-box\"><div class=\"tcg-stat-item\"><div class=\"tcg-stat-title\">COMBAT POWER</div><div class=\"tcg-stat-val\" style=\"color:#ffd700;\">" + "{:,}".format(final_cp) + "</div></div><div class=\"tcg-stat-item\"><div class=\"tcg-stat-title\">SURVIVAL RATE</div><div class=\"tcg-stat-val\">TOP " + "{:.1f}".format(100-pct_beat_final) + "%</div></div></div><div style=\"position:relative; z-index:5; margin-bottom:15px;\">" + aug_html_str + "</div><div style=\"position:relative; z-index:5; margin-bottom:20px;\">" + tags_html_web + "</div><div style=\"position:relative; z-index:5; width:100%;\"><div style=\"font-size:11px; color:#00f3ff; margin-bottom:10px; font-family:'Orbitron'; letter-spacing:2px; font-weight:bold; text-align:left; border-bottom:1px dashed #00f3ff; padding-bottom:5px;\">[ CORE PROTOCOLS ]</div>" + skills_html_web + faction_buff_str + weather_buff_str + despair_buff_str + squad_bonus_html + set_bonus_html + "</div></div></div></div>"
            safe_html(HTML_CARD)

        with col_m:
            safe_html("<h4 style='color:#00f3ff !important; border-left:4px solid #00f3ff; padding-left:10px; font-weight:900;'>🕸️ 六维战力雷达</h4>")
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.15)', line=dict(color='rgba(0, 243, 255, 0.4)', width=8), hoverinfo='none'))
            fig_radar.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=3), marker=dict(color='#ff003c', size=6, symbol='diamond')))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC", color='#e2e8f0', size=11))), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=15, r=15, t=10, b=20), height=300)
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
            
            safe_html("<h4 style='color:#ff003c !important; border-left:4px solid #ff003c; padding-left:10px; font-weight:900;'>🎛️ 风险抵抗阈值</h4>")
            fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=risk_score, number={'suffix': " HP", 'font': {'family': 'Orbitron', 'color': r_color, 'size': 36}}, gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#330011"}, 'bar': {'color': r_color}, 'bgcolor': "rgba(0,243,255,0.05)", 'steps': [{'range': [0, 35], 'color': "rgba(16, 185, 129, 0.15)"}, {'range': [35, 65], 'color': "rgba(255, 215, 0, 0.15)"}, {'range': [65, 100], 'color': "rgba(255, 0, 60, 0.25)"}]}))
            fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#94a3b8"}, height=200, margin=dict(l=30, r=30, t=10, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        with col_r:
            safe_html("<h4 style='color:#a855f7 !important; border-left:4px solid #a855f7; padding-left:10px; font-weight:900;'>⚔️ 对抗能量槽</h4>")
            HTML_BARS = "<div style=\"background:rgba(10,5,5,0.9); border:1px solid rgba(0,243,255,0.2); border-radius:4px; padding:20px; box-shadow:inset 0 0 20px rgba(0,0,0,0.8);\"><div style=\"font-size:11px; color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;\"><span>外联 (E) " + str(val_E) + "%</span><span style=\"color:#94a3b8;\">深潜 (I) " + str(val_I) + "%</span></div><div style=\"background:rgba(255,255,255,0.05); border-radius:2px; height:8px; margin:8px 0 15px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);\"><div style=\"position:absolute; top:0; left:0; height:100%; border-radius:2px; width:" + str(val_E) + "%; background:linear-gradient(90deg, transparent, #00f3ff);\"></div></div><div style=\"font-size:11px; color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;\"><span>实勘 (S) " + str(val_S) + "%</span><span style=\"color:#94a3b8;\">前瞻 (N) " + str(val_N) + "%</span></div><div style=\"background:rgba(255,255,255,0.05); border-radius:2px; height:8px; margin:8px 0 15px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);\"><div style=\"position:absolute; top:0; left:0; height:100%; border-radius:2px; width:" + str(val_S) + "%; background:linear-gradient(90deg, transparent, #a855f7);\"></div></div><div style=\"font-size:11px; color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;\"><span>护甲 (T) " + str(val_T) + "%</span><span style=\"color:#94a3b8;\">共情 (F) " + str(val_F) + "%</span></div><div style=\"background:rgba(255,255,255,0.05); border-radius:2px; height:8px; margin:8px 0 15px 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);\"><div style=\"position:absolute; top:0; left:0; height:100%; border-radius:2px; width:" + str(val_T) + "%; background:linear-gradient(90deg, transparent, #3b82f6);\"></div></div><div style=\"font-size:11px; color:#e2e8f0; font-family:'Orbitron', sans-serif; display:flex; justify-content:space-between; font-weight:bold;\"><span>秩序 (J) " + str(val_J) + "%</span><span style=\"color:#94a3b8;\">敏捷 (P) " + str(val_P) + "%</span></div><div style=\"background:rgba(255,255,255,0.05); border-radius:2px; height:8px; margin:8px 0 0 0; position:relative; overflow:hidden; border:1px solid rgba(255,255,255,0.1);\"><div style=\"position:absolute; top:0; left:0; height:100%; border-radius:2px; width:" + str(val_J) + "%; background:linear-gradient(90deg, transparent, #10b981);\"></div></div></div>"
            safe_html(HTML_BARS)
            
            safe_html("<h4 style='color:#ffd700 !important; border-left:4px solid #ffd700; padding-left:10px; font-weight:900; margin-top:15px;'>🌌 3D 废土星图</h4>")
            st.plotly_chart(get_3d_topology(val_E, val_I, val_S, val_N, val_T, val_F, mbti, tier_color, h_int), use_container_width=True, config={'displayModeBar': False})

    with t_combat:
        c_tc1, c_tc2 = st.columns(2)
        with c_tc1:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#ff003c; margin-bottom:10px; border-bottom:1px dashed #ff003c; padding-bottom:8px;'>/// MEGA-CORP RAID (产出暗物质)</div>")
            boss_max_hp = 2000000 * st.session_state.boss_level
            boss_hp_pct = max(0, st.session_state.boss_hp / boss_max_hp * 100)
            boss_element = ["⚡ 量子", "✨ 灵能", "🛡️ 钢核", "🔥 炎脉"][st.session_state.boss_level % 4]
            boss_name = ["P0级连环线上事故", "毁灭级降本增效风暴", "跨部门背刺利维坦", "史诗级黑客入侵勒索"][st.session_state.boss_level % 4]
            
            safe_html("<div style=\"background:rgba(0,0,0,0.8); border:2px solid #ff003c; padding:20px; border-radius:4px; text-align:center; box-shadow: inset 0 0 30px rgba(255,0,60,0.15);\"><div style=\"font-size:40px; margin-bottom:10px;\">🏢</div><div style=\"color:#ff003c; font-weight:900; font-family:'Orbitron'; font-size:20px; margin-bottom:5px;\">LV." + str(st.session_state.boss_level) + " " + boss_name + "</div><div style=\"font-size:12px; color:#fff; font-weight:bold; margin-bottom:10px;\">弱点检测：防线呈现 " + boss_element + " 特性</div><div style=\"background:#334155; height:15px; border-radius:2px; overflow:hidden; margin-bottom:10px;\"><div style=\"background:#ff003c; width:" + str(boss_hp_pct) + "%; height:100%; transition:width 0.3s;\"></div></div><div style=\"color:#fff; font-family:'Orbitron';\">" + "{:,}".format(int(st.session_state.boss_hp)) + " HP</div></div>")
            safe_html("<br>")
            if st.session_state.boss_hp > 0:
                cost_b = 7 if (st.session_state.equipped_pet and "机械哈士奇" in st.session_state.equipped_pet.get('name','')) else 15
                st.button("⚔️ 消耗 " + str(cost_b) + " 体力引爆火力 (受 E 值加成)", on_click=cb_boss_attack, type="primary", use_container_width=True)
            if st.session_state.combat_logs:
                safe_html("<div style='background:#050505; border:1px solid #334155; padding:15px; border-radius:4px; height:180px; overflow-y:auto; font-size:13px; color:#e2e8f0; margin-top:20px; box-shadow:inset 0 0 15px rgba(0,0,0,0.8); line-height: 1.7;'>" + "<br><br>".join(st.session_state.combat_logs[:15]) + "</div>")
        with c_tc2:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#f43f5e; margin-bottom:10px; border-bottom:1px dashed #f43f5e; padding-bottom:8px;'>/// PVP ARENA (零和博弈)</div>")
            st.selectbox("🎯 锁定敌对派系:", ["硅基抵抗军", "幽能清道夫", "秩序裁决所", "混沌暴徒"], key="pvp_target", label_visibility="collapsed")
            cost_p = 7 if (st.session_state.equipped_pet and "机械哈士奇" in st.session_state.equipped_pet.get('name','')) else 15
            st.button("⚔️ 消耗 " + str(cost_p) + " 体力发起突袭 (受 T 值加成)", on_click=cb_pvp_battle, use_container_width=True)
            if st.session_state.pvp_logs:
                safe_html("<div style='background:#050505; border:1px solid #334155; padding:15px; border-radius:4px; height:180px; overflow-y:auto; font-size:13px; color:#e2e8f0; margin-top:20px; box-shadow:inset 0 0 15px rgba(0,0,0,0.8); line-height: 1.7;'>" + "<br>".join(st.session_state.pvp_logs[:20]) + "</div>")

    with t_dispatch:
        safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#00f3ff; margin-bottom:10px; border-bottom:1px dashed #00f3ff; padding-bottom:8px;'>/// WASTELAND DISPATCH (产出逻辑碎片)</div>")
        safe_html("<div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>派遣进入暗网拾荒，高概率产出升级天赋树必备的【逻辑碎片】。受 S 值掉落加成。</div>")
        cost_d = 10 if (st.session_state.equipped_pet and "机械哈士奇" in st.session_state.equipped_pet.get('name','')) else 20
        st.button("🛸 消耗 " + str(cost_d) + " 体力进入暗网拾荒", on_click=cb_dispatch, use_container_width=True)
        if st.session_state.dispatch_logs:
            safe_html("<div style='background:#050505; border:1px solid #334155; padding:15px; border-radius:4px; height:200px; overflow-y:auto; font-size:13px; color:#e2e8f0; margin-top:20px; box-shadow:inset 0 0 15px rgba(0,0,0,0.8); line-height: 1.7;'>" + "<br><br>".join(st.session_state.dispatch_logs[:15]) + "</div>")

    with t_growth:
        col_gr1, col_gr2, col_gr3 = st.columns(3)
        with col_gr1:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#00f3ff; margin-bottom:10px; border-bottom:1px dashed #00f3ff; padding-bottom:8px;'>/// CARD ASCENSION (星级突破)</div><div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>消耗稀有的【暗物质】升星！每次突破全属性战力提升 25%！</div>")
            cost_dm = 100 + (st.session_state.ascension_stars * 50)
            safe_html("<div style='text-align:center; padding:10px; background:rgba(0,0,0,0.5); border:1px solid #334155; border-radius:4px; margin-bottom:10px;'><div style='font-size:14px; color:#fff; font-weight:bold; margin-bottom:5px;'>当前星级：" + str(st.session_state.ascension_stars) + " 星</div><div style='font-size:11px; color:#94a3b8;'>需要：<b style='color:#a855f7; font-size:14px;'>" + str(cost_dm) + "</b> 🌑 暗物质</div></div>")
            if st.session_state.ascension_stars < 5: 
                st.button("🌌 突破界限 (ASCEND)", on_click=cb_ascend_card, type="primary", use_container_width=True)
            else: safe_html("<div style='text-align:center; padding:10px; font-size:16px; font-weight:bold; color:#fff; text-shadow:0 0 10px #00f3ff;'>✨ MAX ASCENSION ✨</div>")
        with col_gr2:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#a855f7; margin-bottom:10px; border-bottom:1px dashed #a855f7; padding-bottom:8px;'>/// GENE TALENT (消耗逻辑碎片)</div><div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>升级不仅永久加成战力，更能提升四大生态乘区的倍率！</div>")
            tl = st.session_state.talent_levels
            c_e, c_s = st.columns(2); c_t, c_j = st.columns(2)
            with c_e: 
                cost_sde = 2000 + tl['E'] * 1000; cost_shard = 1 + tl['E']
                st.button("升 E [Lv" + str(tl['E']) + "]\n" + str(cost_sde) + "币/" + str(cost_shard) + "碎", key="up_e", on_click=cb_talent_up, args=("E",), use_container_width=True)
            with c_s: 
                cost_sde = 2000 + tl['S'] * 1000; cost_shard = 1 + tl['S']
                st.button("升 S [Lv" + str(tl['S']) + "]\n" + str(cost_sde) + "币/" + str(cost_shard) + "碎", key="up_s", on_click=cb_talent_up, args=("S",), use_container_width=True)
            with c_t: 
                cost_sde = 2000 + tl['T'] * 1000; cost_shard = 1 + tl['T']
                st.button("升 T [Lv" + str(tl['T']) + "]\n" + str(cost_sde) + "币/" + str(cost_shard) + "碎", key="up_t", on_click=cb_talent_up, args=("T",), use_container_width=True)
            with c_j: 
                cost_sde = 2000 + tl['J'] * 1000; cost_shard = 1 + tl['J']
                st.button("升 J [Lv" + str(tl['J']) + "]\n" + str(cost_sde) + "币/" + str(cost_shard) + "碎", key="up_j", on_click=cb_talent_up, args=("J",), use_container_width=True)
        with col_gr3:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#ffd700; margin-bottom:10px; border-bottom:1px dashed #ffd700; padding-bottom:8px;'>/// FOIL UPGRADE (幻彩重铸)</div><div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>消耗暗物质重铸卡面材质，扩大全局战力乘区！</div>")
            foils = ["【标准拉丝工艺】", "【镭射碎冰闪卡】", "【暗黑反转闪卡】", "【创世血腥幻彩】"]
            costs = [0, 500, 1500, 5000]
            current = st.session_state.card_foil
            try: idx = foils.index(current)
            except: idx = 0
            safe_html("<div style='text-align:center; padding:10px; background:rgba(0,0,0,0.5); border:1px solid #334155; border-radius:4px; margin-bottom:10px;'><div style='font-size:12px; color:#fff; font-weight:bold; margin-bottom:5px;'>当前：<span style='color:#ffd700;'>" + current + "</span></div>")
            if idx < 3:
                cost_f = costs[idx+1]
                safe_html("<div style='font-size:11px; color:#94a3b8;'>升级需要：<b style='color:#a855f7;'>" + str(cost_f) + "</b> 🌑 暗物质</div></div>")
                st.button("✨ 重铸卡面材质", on_click=cb_upgrade_foil, type="primary", use_container_width=True)
            else:
                safe_html("</div><div style='text-align:center; padding:10px; font-size:16px; font-weight:bold; color:#fff; text-shadow:0 0 10px #ffd700;'>✨ 巅峰工艺达成 ✨</div>")

    with t_gacha:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            safe_html("<div style='font-family:Orbitron; font-size:16px; font-weight:bold; color:#ffd700; margin-bottom:10px; border-bottom:1px dashed #ffd700; padding-bottom:8px;'>/// WEAPON BANNER (黑市空投)</div>")
            if st.session_state.pity_counter > 0:
                safe_html("<div style='color:#ff003c; font-size:11px; margin-bottom:5px; font-weight:bold;'>再打捞 " + str(30 - st.session_state.pity_counter) + " 次必出神话级！</div>")
            st.button("🎲 呼叫空投军火 (消耗 SDE)", on_click=cb_gacha, args=("relic",), use_container_width=True)
            
            safe_html("<div style='font-family:Orbitron; font-size:16px; font-weight:bold; color:#00f3ff; margin-bottom:10px; border-bottom:1px dashed #00f3ff; padding-bottom:8px; margin-top:20px;'>/// CYBER TAROT (命运占卜)</div>")
            st.button("🃏 占卜今日运势 (消耗 200 SDE)", on_click=cb_draw_tarot, use_container_width=True)
            safe_html("<div style='margin-top:20px; padding:15px; background:rgba(255,0,60,0.1); border:1px solid rgba(255,0,60,0.4); border-radius:4px; font-size:14px; font-weight:bold; text-align:center; color:#ff003c;'>" + st.session_state.gacha_msg + "</div>")
        
        with col_g2:
            safe_html("<div style='font-family:Orbitron; font-size:16px; font-weight:bold; color:#a855f7; margin-bottom:10px; border-bottom:1px dashed #a855f7; padding-bottom:8px;'>/// PET BANNER (伴生机甲)</div>")
            st.button("🐾 抽取伴生机甲 (消耗 SDE)", on_click=cb_gacha, args=("pet",), use_container_width=True)

    with t_inv:
        safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#ff8c00; margin-bottom:10px; border-bottom:1px dashed #ff8c00; padding-bottom:8px;'>/// QUANTUM FORGE (量子熔炉)</div>")
        if st.session_state.despair_level > 80:
            safe_html("<div style='color:#ff003c; font-size:12px; font-weight:bold; animation:blink 1.5s infinite;'>⚠️ 警告：污染超载，融合有 50% 概率发生大爆炸导致材料全毁！</div>")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1: st.button("🔥 融合 3 件 R 级", on_click=cb_forge, args=("R", "SR"), use_container_width=True)
        with col_f2: st.button("🔥 融合 3 件 SR 级", on_click=cb_forge, args=("SR", "SSR"), use_container_width=True)
        with col_f3: st.button("🔥 融合 3 件 SSR 级", on_click=cb_forge, args=("SSR", "UR"), use_container_width=True)
        safe_html("<div style='margin-top:10px; margin-bottom:20px; font-size:12px; color:#ff8c00; text-align:center;'>" + st.session_state.forge_msg + "</div>")
        
        safe_html("<h5 style='color:#ff003c;'>🎒 我的武装库 (最多装备 3 件武器 + 1 只机甲)：</h5>")
        if not st.session_state.inventory and not st.session_state.pets:
            safe_html("<div style='color:#64748b; font-size:13px; text-align:center; padding:20px; border:1px dashed #334155; border-radius:4px;'>空空如也，快去空投区抽卡吧！</div>")
        else:
            for r in st.session_state.inventory:
                is_eq = any(eq['uid'] == r['uid'] for eq in st.session_state.equipped_relics)
                bg = "rgba(255,0,60,0.2)" if is_eq else "rgba(255,255,255,0.05)"
                btn_txt = "卸下" if is_eq else "装备"
                r_col1, r_col2, r_col3 = st.columns([3, 1, 1])
                with r_col1:
                    safe_html("<div style=\"border-left: 4px solid " + r['color'] + "; background: " + bg + "; padding: 10px; margin-bottom: 5px; border-radius: 0 4px 4px 0;\"><div style=\"display:flex; justify-content:space-between; margin-bottom:5px;\"><b style=\"color:" + r['color'] + "; font-size:14px;\">[武装] " + r['name'] + "</b><span style=\"color:#ff003c; font-weight:bold; font-family:Orbitron; font-size:12px;\">+" + "{:,}".format(r['cp']) + " CP</span></div><div style=\"color:#94a3b8; font-size:11px;\">" + r['desc'] + "</div></div>")
                with r_col2: st.button(btn_txt, key="eq_"+r['uid'], on_click=cb_equip_relic, args=(r['uid'],), use_container_width=True)
                with r_col3:
                    if not is_eq: st.button("拆解", key="ds_"+r['uid'], on_click=cb_dismantle, args=(r['uid'],), use_container_width=True)
            for p in st.session_state.pets:
                is_eq = st.session_state.equipped_pet and st.session_state.equipped_pet['uid'] == p['uid']
                bg = "rgba(255,0,60,0.2)" if is_eq else "rgba(255,255,255,0.05)"
                btn_txt = "待机" if is_eq else "出战"
                p_col1, p_col2 = st.columns([3, 2])
                with p_col1:
                    safe_html("<div style=\"border-left: 4px solid " + p['color'] + "; background: " + bg + "; padding: 10px; margin-bottom: 5px; border-radius: 0 4px 4px 0;\"><div style=\"display:flex; justify-content:space-between; margin-bottom:5px;\"><b style=\"color:" + p['color'] + "; font-size:14px;\">[伴生] " + p['name'] + "</b><span style=\"color:#ff003c; font-weight:bold; font-family:Orbitron; font-size:12px;\">+" + "{:,}".format(p['cp']) + " CP</span></div><div style=\"color:#94a3b8; font-size:11px;\">" + p['desc'] + "</div></div>")
                with p_col2: st.button(btn_txt, key="eq_"+p['uid'], on_click=cb_equip_pet, args=(p['uid'],), use_container_width=True)

    with t_aug:
        safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#ff003c; margin-bottom:10px; border-bottom:1px dashed #ff003c; padding-bottom:8px;'>/// CYBERNETIC AUGMENTATION CLINIC</div>")
        safe_html("<div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>血肉苦弱，机械飞升。花费巨额战备金与<b style='color:#ff003c;'>永久理智上限</b>进行肉体改造，获得不可逆的倍率加成！</div>")
        for aug in CYBER_AUGMENTS:
            has_aug = aug['id'] in st.session_state.cyber_augments
            a_col1, a_col2 = st.columns([3, 1])
            with a_col1:
                bg = "rgba(255,0,60,0.15)" if has_aug else "rgba(0,0,0,0.5)"
                border = "border-left: 4px solid #ff003c;" if has_aug else "border-left: 4px solid #334155;"
                safe_html("<div style='background:" + bg + "; " + border + " padding:15px; border-radius:4px; margin-bottom:10px;'><div style='display:flex; justify-content:space-between;'><b style='color:#fff;'>" + aug['name'] + "</b><span style='color:#ffd700; font-family:Orbitron;'>成本: " + "{:,}".format(aug['cost']) + " 币</span></div><div style='color:#ff003c; font-size:12px; margin-top:5px;'>" + aug['desc'] + "</div></div>")
            with a_col2:
                if has_aug: st.button("已安装", key="aug_"+aug['id'], disabled=True, use_container_width=True)
                else: st.button("安装义体", key="aug_"+aug['id'], on_click=cb_buy_augment, args=(aug['id'], aug['cost'], aug['san_cost']), use_container_width=True)

    with t_econ:
        c_te1, c_te2, c_te3 = st.tabs(["🏦 避风港质押", "🛒 动态外汇大盘", "📜 军令状"])
        with c_te1:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#3b82f6; margin-bottom:10px; border-bottom:1px dashed #3b82f6; padding-bottom:8px;'>/// OFFSHORE STAKING POOL (复利)</div><div style='font-size:13px; color:#e2e8f0; margin-bottom:15px;'>将 $SDE 转移至海外避风港。你在终端的<b>每一次行动</b>都会产生复利！(受 J 值加成)</div>")
            c_st1, c_st2 = st.columns(2)
            with c_st1:
                safe_html("<div style='background:rgba(0,0,0,0.6); border:1px solid #334155; border-radius:8px; padding:20px; margin-bottom:15px;'><div style='color:#94a3b8; font-size:11px; margin-bottom:5px;'>已洗白金额 (SDE)</div><div style='color:#00f3ff; font-size:24px; font-family:Orbitron; font-weight:bold;'>" + "{:,}".format(int(st.session_state.staked_tokens)) + " 🪙</div></div>")
                st.button("📥 转移 5,000 $SDE", on_click=cb_stake, use_container_width=True)
            with c_st2:
                safe_html("<div style='background:rgba(0,0,0,0.6); border:1px solid #334155; border-radius:8px; padding:20px; margin-bottom:15px;'><div style='color:#94a3b8; font-size:11px; margin-bottom:5px;'>未提取收益</div><div style='color:#10b981; font-size:24px; font-family:Orbitron; font-weight:bold;'>+ " + "{:,}".format(int(st.session_state.yield_pool)) + " SDE</div></div>")
                st.button("📤 提取全部利息", on_click=claim_yield_callback, type="primary", use_container_width=True)
        with c_te2:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#a855f7; margin-bottom:10px; border-bottom:1px dashed #a855f7; padding-bottom:8px;'>/// DARK MATTER EXCHANGE (暗物质外汇)</div>")
            safe_html("<div style='background:rgba(0,0,0,0.6); border:1px solid #a855f7; border-radius:8px; padding:15px; margin-bottom:15px; text-align:center;'><div style='color:#94a3b8; font-size:11px;'>实时汇率 (SDE / 1 暗物质)</div><div style='color:#a855f7; font-size:28px; font-weight:bold; font-family:Orbitron;'>" + str(st.session_state.exchange_rate) + "</div></div>")
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                cost_ex = st.session_state.exchange_rate * 10
                st.button("📉 买入 10 暗物质 (" + str(cost_ex) + " SDE)", on_click=cb_exchange_buy, use_container_width=True)
            with col_ex2:
                earn_ex = int(st.session_state.exchange_rate * 10 * 0.9)
                st.button("📈 卖出 10 暗物质 (得 " + str(earn_ex) + " SDE)", on_click=cb_exchange_sell, use_container_width=True)
                
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#f43f5e; margin-bottom:10px; border-bottom:1px dashed #f43f5e; padding-bottom:8px; margin-top:20px;'>/// BLACK MARKET</div>")
            col_sm1, col_sm2 = st.columns(2)
            with col_sm1: 
                st.button("💊 购买神经安定剂 (+50体力 | 2k SDE)", on_click=cb_buy_stamina, use_container_width=True)
                st.button("📦 走私交易：必得 SSR (2w SDE)", on_click=cb_buy_ssr, use_container_width=True)
            with col_sm2:
                gpu_cost = 5000 + (st.session_state.gpus * 3000)
                st.button("🖥️ 部署僵尸矿机 (消耗 " + "{:,}".format(gpu_cost) + " SDE)", on_click=cb_buy_gpu, use_container_width=True)
                safe_html("<div style='margin-top:5px; color:#10b981; font-size:11px;'>矿机会在每次生态循环中自动产币！受 J 值加成！</div>")
        with c_te3:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#10b981; margin-bottom:10px; border-bottom:1px dashed #10b981; padding-bottom:8px;'>/// DAILY BOUNTIES</div>")
            if not st.session_state.bounties_claimed:
                safe_html("<div style='background:rgba(16,185,129,0.1); border-left:4px solid #10b981; padding:15px; border-radius:4px; margin-bottom:15px;'><b style='color:#10b981;'>【日常】活下来，并激活节点</b><br><span style='font-size:12px; color:#94a3b8;'>奖励：10,000 SDE + 200 EXP</span></div>")
                st.button("🎁 领取悬赏奖励", on_click=cb_claim_bounty, use_container_width=True)
            else: st.success("✅ 今日悬赏已全部完成！")

    with t_altar:
        col_al1, col_al2 = st.columns(2)
        with col_al1:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#ff003c; margin-bottom:10px; border-bottom:1px dashed #ff003c; padding-bottom:8px;'>/// BLOOD SACRIFICE (鲜血祭祀)</div><div style='font-size:12px; color:#e2e8f0; margin-bottom:15px;'>用理智换取暴利，或去赌场梭哈！</div>")
            st.button("🩸 献祭 30 理智 换取 暗物质", on_click=cb_altar_blood, use_container_width=True)
            st.button("🗑️ 献祭 1 件 R级武装 降低 20 污染", on_click=cb_altar_trash, use_container_width=True)

        with col_al2:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#ffd700; margin-bottom:10px; border-bottom:1px dashed #ffd700; padding-bottom:8px;'>/// CYBER CASINO (地下赌局)</div><div style='font-size:12px; color:#e2e8f0; margin-bottom:15px;'>消耗 1000 SDE，30% 概率赢得 3500 SDE。</div>")
            st.button("🎰 赛博赌盘 (消耗 1000 SDE)", on_click=cb_casino, use_container_width=True)

    with t_syn:
        safe_html("<div style='background:rgba(10, 2, 4, 0.8); border:1px solid rgba(255,0,60,0.2); border-radius:12px; padding:clamp(15px, 4vw, 25px); box-shadow:inset 0 0 20px rgba(0,0,0,0.5);'><h4 style='color:#3b82f6 !important; border-left:4px solid #3b82f6; padding-left:10px; font-weight:900; margin-bottom:15px;'>🎴 三卡小队实体编成 (SQUAD BUILDER)</h4><div style='font-size:13px; color:#94a3b8; margin-bottom:15px;'>在绝境中招募两名实体盟友！编成后所有队员共享 20% 战力加成，若三人同属同一元素，将引发【元素共鸣】，全体战力暴增 50%！</div>")
        options_list = list(mbti_details.keys())
        format_func = lambda x: f"{x} - {mbti_details[x]['role']}"
        col_s1, col_s2, col_s3 = st.columns([2, 2, 1])
        
        idx1 = options_list.index(st.session_state.squad[0]) if st.session_state.squad[0] else options_list.index("ESTJ")
        idx2 = options_list.index(st.session_state.squad[1]) if st.session_state.squad[1] else options_list.index("INTJ")
        
        with col_s1: st.selectbox("🎯 战术小队成员 1:", options=options_list, index=idx1, format_func=format_func, key="syn1", label_visibility="collapsed")
        with col_s2: st.selectbox("🎯 战术小队成员 2:", options=options_list, index=idx2, format_func=format_func, key="syn2", label_visibility="collapsed")
        with col_s3: st.button("✅ 确认编队", on_click=cb_confirm_squad, use_container_width=True)
        
        curr_m1 = st.session_state.squad[0] if st.session_state.squad[0] else st.session_state.syn1
        curr_m2 = st.session_state.squad[1] if st.session_state.squad[1] else st.session_state.syn2
        
        sc1, sd1 = calculate_synergy(mbti, curr_m1); sc2, sd2 = calculate_synergy(mbti, curr_m2)
        total_sc = int((sc1 + sc2) / 2)
        fac1 = get_faction_info(curr_m1); fac2 = get_faction_info(curr_m2)
        tri_element = (faction_data['element'] == fac1['element'] == fac2['element'])
        if tri_element: total_sc = min(150, total_sc + 30)
        sc_color = "#ff003c" if tri_element else ("#ffd700" if total_sc >= 90 else ("#00f3ff" if total_sc >= 80 else "#a855f7"))
        
        v1_E = 85 if 'E' in curr_m1 else 15; v2_E = 85 if 'E' in curr_m2 else 15
        v1_S = 85 if 'S' in curr_m1 else 15; v2_S = 85 if 'S' in curr_m2 else 15
        v1_T = 85 if 'T' in curr_m1 else 15; v2_T = 85 if 'T' in curr_m2 else 15
        v1_J = 85 if 'J' in curr_m1 else 15; v2_J = 85 if 'J' in curr_m2 else 15
        target_values = [(v1_E+v2_E)/2, (v1_S+v2_S)/2, (v1_T+v2_T)/2, (v1_J+v2_J)/2, 100-(v1_E+v2_E)/2, 100-(v1_S+v2_S)/2, 100-(v1_T+v2_T)/2, 100-(v1_J+v2_J)/2]

        fig_syn = go.Figure()
        fig_syn.add_trace(go.Scatterpolar(r=target_values + [target_values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(168, 85, 247, 0.15)', line=dict(color='rgba(168, 85, 247, 0.8)', width=2, dash='dash'), name='小队平均阵型'))
        fig_syn.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(255, 0, 60, 0.3)', line=dict(color='#ff003c', width=3), name='本机节点'))
        fig_syn.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(family="Noto Sans SC", color='#e2e8f0', size=10))), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#fff")), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=25, r=25, t=10, b=20), height=320)
        st.plotly_chart(fig_syn, use_container_width=True, config={'displayModeBar': False})

        if st.session_state.squad[0]:
            if tri_element:
                safe_html("<style>.link-skill-active { background: linear-gradient(90deg, rgba(255,0,60,0.1), rgba(255,0,60,0.4), rgba(255,0,60,0.1)); border: 2px solid #ff003c; box-shadow: 0 0 30px rgba(255,0,60,0.8), inset 0 0 20px rgba(255,0,60,0.5); animation: pulse-link 1s infinite alternate; border-radius: 12px; padding: 25px; text-align: center; margin-top: 10px;} @keyframes pulse-link { 0% { transform: scale(1); } 100% { transform: scale(1.02); box-shadow: 0 0 50px rgba(255,0,60,1); } }</style><div class=\"link-skill-active\"><div style=\"font-family:'Orbitron'; color:#ff003c; font-size:12px; font-weight:bold; margin-bottom:10px; letter-spacing: 4px;\">💥 " + faction_data['element'] + " 军团共鸣大爆发 💥</div><div style=\"font-family:'Orbitron'; font-size:65px; font-weight:900; color:#fff; text-shadow:0 0 35px #ff003c; margin-bottom:15px;\">" + str(total_sc) + "%</div><div style=\"color:#e2e8f0; font-size:15px; font-weight:bold; line-height:1.7;\">神级羁绊！已为您带来 50% 战力乘区扩大！</div></div>")
            else:
                safe_html("<div style=\"background: rgba(0,0,0,0.5); border: 1px solid " + sc_color + "66; border-left: 4px solid " + sc_color + "; padding: 25px; border-radius: 8px; margin-top:10px; text-align:center; box-shadow: 0 0 30px " + sc_color + "22;\"><div style=\"font-family:'Orbitron'; color:" + sc_color + "; font-size:12px; font-weight:bold; margin-bottom:10px; letter-spacing: 3px;\">[ TEAM RESONANCE ]</div><div style=\"font-family:'Orbitron'; font-size:55px; font-weight:900; color:#fff; text-shadow:0 0 35px " + sc_color + "99; margin-bottom:15px;\">" + str(total_sc) + "%</div><div style=\"color:#e2e8f0; font-size:14px; font-weight:bold; line-height:1.7;\">已激活普通编队，获得 20% 战力加成。</div></div>")
        safe_html("</div>")

    with t_data:
        c_td1, c_td2, c_td3, c_td6, c_td7 = st.tabs(["🛡️ 军团阵营", "📉 走势压测", "📊 黑市盘口", "🏆 生还者榜", "🟩 战损热力"])
        with c_td1:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#10b981; margin-bottom:10px; border-bottom:1px dashed #10b981; padding-bottom:8px;'>/// FACTION GUILD</div>")
            if not st.session_state.joined_faction:
                st.selectbox("宣誓效忠的阵营 (若匹配核心将获10%战力增幅):", ["硅基抵抗军 (量子)", "幽能清道夫 (灵能)", "秩序裁决所 (钢核)", "混沌暴徒 (炎脉)"], key="faction_sel")
                st.button("🛡️ 宣誓效忠 (不可更改)", on_click=cb_join_faction)
            else:
                safe_html("<div style='text-align:center; padding:20px; background:rgba(0,0,0,0.5); border:1px solid #10b981; border-radius:8px;'><div style='color:#10b981; font-weight:bold; font-size:18px;'>已加入：[" + st.session_state.joined_faction + "]</div><div style='color:#e2e8f0; font-size:13px; margin-top:10px;'>享受该阵营的专属被动增益。</div></div>")
        with c_td2:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#ffd700; margin-bottom:10px; border-bottom:1px dashed #ffd700; padding-bottom:8px;'>/// 30-DAY COMBAT SIMULATION</div><div style='font-size:14px; color:#e2e8f0; margin-bottom:10px;'>基于高斯随机游走与标准差推演：<br><span style='color:#ffd700; font-weight:bold; font-size:15px;'>【 " + data.get('market_style', '') + " 】</span></div>")
            std_dev = np.std(roi_arr); upper_band = [val + std_dev * 1.5 for val in roi_arr]; lower_band = [val - std_dev * 1.5 for val in roi_arr]
            fig_roi = go.Figure()
            lc = "#10b981" if roi_arr[-1] >= 100 else "#ff003c"
            fig_roi.add_trace(go.Scatter(x=d_arr + d_arr[::-1], y=upper_band + lower_band[::-1], fill='toself', fillcolor='rgba(255,255,255,0.05)', line=dict(color='rgba(255,255,255,0)'), hoverinfo="skip", showlegend=False))
            fig_roi.add_trace(go.Scatter(x=d_arr, y=roi_arr, mode='lines', line=dict(color=lc, width=3), name="Combat Power"))
            fig_roi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'), showlegend=False)
            st.plotly_chart(fig_roi, use_container_width=True, config={'displayModeBar': False})
        with c_td3:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#3b82f6; margin-bottom:10px; border-bottom:1px dashed #3b82f6; padding-bottom:8px;'>/// LIVE MARKET DEPTH & BIDS</div>")
            HTML_BIDS = "<div style=\"background: #050205; border: 1px solid #330011; border-radius: 8px; padding: 20px; font-family: 'Fira Code', monospace; font-size: 12px; color: #94a3b8; box-shadow: inset 0 0 20px rgba(255,0,60,0.2);\">" + get_market_depth_html(h_int) + "<div style=\"display: flex; justify-content: space-between; border-bottom: 1px dashed #330011; padding-bottom: 12px; margin-bottom: 15px; color: #e2e8f0; font-weight: bold; font-size: 11px; letter-spacing: 1px;\"><span style=\"width:40%;\">[INSTITUTION]</span><span style=\"width:30%; text-align:center;\">[BID_SIZE]</span><span style=\"width:30%; text-align:right;\">[PREMIUM]</span></div>" + bids_html + "<div style=\"text-align: center; margin-top: 15px; font-size: 10px; color: #ff003c; animation: blink 1.5s infinite;\">● WAITING FOR NEW BIDS...</div></div>"
            safe_html(HTML_BIDS)
        with c_td6:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#ffd700; margin-bottom:10px; border-bottom:1px dashed #ffd700; padding-bottom:8px;'>/// GLOBAL SURVIVOR LEADERBOARD</div>")
            HTML_RANK = "<div style=\"background:#050205; border:1px solid #330011; border-radius:8px; padding:15px; font-family:'Orbitron', monospace; font-size:12px;\"><div style=\"display:flex; justify-content:space-between; color:#ffd700; margin-bottom:10px; border-bottom:1px dashed #330011; padding-bottom:5px;\"><span>RANK</span><span>NODE_ID</span><span>CP</span></div><div style=\"display:flex; justify-content:space-between; color:#e2e8f0; margin-bottom:8px;\"><span>#1</span><span>0xAI_GHOST</span><span>199,500,000</span></div><div style=\"display:flex; justify-content:space-between; color:#e2e8f0; margin-bottom:8px;\"><span>#2</span><span style=\"color:#ff003c; font-weight:bold;\">" + safe_alias_final + " (YOU)</span><span style=\"color:#ff003c; font-weight:bold;\">" + "{:,}".format(final_cp) + "</span></div><div style=\"display:flex; justify-content:space-between; color:#e2e8f0; margin-bottom:8px;\"><span>#3</span><span>BYTE_SAMURAI</span><span>8,250,000</span></div></div>"
            safe_html(HTML_RANK)
        with c_td7:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#10b981; margin-bottom:10px; border-bottom:1px dashed #10b981; padding-bottom:8px;'>/// DAMAGE HEATMAP (战损分布)</div>")
            safe_html(get_heatmap_html(h_int))

    with t_oracle:
        ORACLE_CSS = "<style>.oracle-box { background: #050205; border: 1px solid #330011; border-left: 4px solid #ff003c; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: inset 0 0 20px rgba(255,0,60,0.2); font-family: 'Fira Code', monospace; font-size: 12px; }.oracle-hdr { color: #ff003c; font-size: 11px; margin-bottom: 15px; border-bottom: 1px dashed #330011; padding-bottom: 8px; letter-spacing: 1px; font-weight: bold; }.oracle-line { overflow: hidden; white-space: nowrap; width: 0; display: block; margin-bottom: 8px; color: #ff8c00; animation: o-type 0.8s steps(40, end) forwards; border-right: 2px solid #ff8c00; }.oracle-line:nth-child(2) { animation-delay: 0.2s; }.oracle-line:nth-child(3) { animation-delay: 1.2s; }.oracle-line:nth-child(4) { animation-delay: 2.2s; }.oracle-line:nth-child(5) { animation-delay: 3.2s; color: #e2e8f0; border-right: none;}.oracle-line-fade { display: block; margin-top: 15px; color: #94a3b8; opacity: 0; animation: o-fade 1s 4.2s forwards; line-height: 1.8; }@keyframes o-type { 99% { border-color: #ff8c00; } 100% { width: 100%; border-color: transparent; } }@keyframes o-fade { to { opacity: 1; } }</style>"
        HTML_ORACLE = ORACLE_CSS.replace('\n', '') + "<div class=\"oracle-box\"><div class=\"oracle-hdr\">[AI_ORACLE_V42] SURVIVAL DIAGNOSTIC...</div><span class=\"oracle-line\">> Extracting Node [ " + safe_alias_final + " ] Weights... [OK]</span><span class=\"oracle-line\">> Bypassing Meatspace Firewall... [SUCCESS]</span><span class=\"oracle-line\">> Decrypting Matrix... [OK]</span><span class=\"oracle-line\">> Node Classified As: <span style=\"color:#ffd700; font-weight:bold;\">" + mbti + "</span></span><span class=\"oracle-line-fade\">> ULTIMATE EVOLUTION PREDICTION: <br><span style=\"color:#ff003c; font-size:14px; font-weight:bold;\">" + data.get('ultimate_evolution', '') + "</span></span></div>"
        safe_html(HTML_ORACLE)
        
        evo_path = data.get('evolution_path', ["L1 见习炮灰", "L2 核心兵器"])
        safe_html("<div style=\"margin-top:15px; margin-bottom:15px; border-left:3px solid #ff003c; padding-left:15px; background:linear-gradient(90deg, rgba(255,0,60,0.1), transparent); padding-top:10px; padding-bottom:10px; border-radius: 0 6px 6px 0;\"><div style=\"color:#ff003c; font-family:Orbitron; font-size:11px; margin-bottom:2px; letter-spacing:1px;\">PHASE 1 (CURRENT STATE)</div><div style=\"color:#fff; font-weight:bold; font-size:16px;\">" + evo_path[0] + "</div></div><div style=\"margin-bottom:15px; border-left:3px solid #ffd700; padding-left:15px; background:linear-gradient(90deg, rgba(255,215,0,0.1), transparent); padding-top:10px; padding-bottom:10px; border-radius: 0 6px 6px 0; margin-left: 20px;\"><div style=\"color:#ffd700; font-family:Orbitron; font-size:11px; margin-bottom:2px; letter-spacing:1px;\">PHASE 2 (AWAKENING)</div><div style=\"color:#fff; font-weight:bold; font-size:16px;\">" + evo_path[1] + "</div></div>")
        with st.expander("⚠️ 绝密防线：资本利维坦黑天鹅推演"):
            safe_html("<div style=\"padding: 5px 10px; font-size: 14px; color: #cbd5e1; line-height: 1.7;\"><div style=\"color: #ff003c; font-weight: 900; margin-bottom: 5px; font-size:15px; text-shadow: 0 0 5px #ff003c;\">[ 致命崩溃盲点 ]</div><div style=\"margin-bottom: 15px;\">" + data.get('black_swan', '') + "</div><div style=\"color: #10b981; font-weight: 900; margin-bottom: 5px; font-size:15px; text-shadow: 0 0 5px #10b981;\">[ 官方热修复补丁 ]</div><div>" + data.get('patch', '') + "</div></div>")

    # ---------------- 15. 卡砖提取 (防死锁海报) ----------------
    with t_mint:
        tm1, tm2, tm3, tm4 = st.tabs(["📸 PSA 实体卡砖 (防死锁)", "📝 纯文本通讯协议", "💻 智能合约", "📥 极客 JSON"])
        with tm1:
            safe_html("<div style='font-size:13px; color:#10b981; margin-bottom:15px; line-height:1.7;'>已为您展示【可见即所得】高清卡砖。点击下方按钮生成图片，<b style='color:#ff003c; font-size:15px;'>如果受环境限制无反应，请直接使用手机系统截屏保存！</b>绝对不再死锁！</div>")
            
            tags_html_poster = "".join(["<span style='background:rgba(255,215,0,0.1); border:1px solid rgba(255,215,0,0.5); padding:4px 8px; border-radius:2px; font-size:11px; color:#ffd700; font-weight:bold; margin:3px; display:inline-block;'>" + t + "</span>" for t in data.get('tags', [])])
            skills_html_poster = "".join(["<div style='background:rgba(255,0,60,0.1); border:1px solid rgba(255,0,60,0.6); border-left:3px solid #ff003c; padding:6px 10px; border-radius:2px; font-size:11px; color:#fca5a5; font-weight:bold; margin-bottom:5px; text-align:left;'>" + s + "</div>" for s in data.get('skills', [])])
            
            random.seed(h_int)
            gradient_stops = []
            for p in range(0, 100, int(random.uniform(2, 6))): 
                gradient_stops.append("rgba(255,0,60,0.4) " + str(p) + "%, rgba(255,0,60,0.4) " + str(p+1) + "%, transparent " + str(p+1) + "%, transparent " + str(p+2) + "%")
            barcode_css = "linear-gradient(90deg, " + ", ".join(gradient_stops) + ")"
            
            relics_text = "、".join([r['name'][:6] for r in st.session_state.equipped_relics]) if st.session_state.equipped_relics else "裸装上阵"
            pet_text = st.session_state.equipped_pet['name'] if st.session_state.equipped_pet else "无伴生兽"

            POSTER_CSS = (
                '<style>body { margin: 0; padding: 10px 0; background: transparent !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #fff; overflow-x: hidden; text-align: center; } '
                '.capture-box { width: 320px; background-color: #050205; padding: 15px; border-radius: 12px; border: 3px solid #cbd5e1; box-shadow: 0 0 25px rgba(255, 0, 60, 0.4); position: relative; overflow: hidden; margin: 0 auto; text-align: left; box-sizing: border-box; } '
                '.cyber-grid { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: linear-gradient(0deg, rgba(255,0,60,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,0,60,0.05) 1px, transparent 1px); background-size: 25px 25px; z-index: 0; pointer-events:none;} '
                '.psa-header { background: #990024; padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #ff003c; margin-bottom: 15px; position: relative; z-index: 2; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);} '
                '.psa-grade { font-size: 28px; font-weight: 900; color: #fff; line-height: 1; font-family: Impact, sans-serif; } '
                '.psa-desc { font-size: 10px; color: #fecaca; text-align: right; font-weight: bold; line-height: 1.2; text-transform: uppercase; } '
                '.inner-card { background: rgba(20,5,10,0.95); border: 2px solid rgba(255,0,60,0.4); border-radius: 8px; padding: 20px 15px; position: relative; z-index: 2; overflow: hidden;} '
                '.hd { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed rgba(255,0,60,0.3); padding-bottom: 10px; margin-bottom: 15px; } '
                '.nm { text-align: center; font-size: 18px; font-weight: 900; letter-spacing: 2px; margin-bottom: 5px; color: #fff; text-transform: uppercase; } '
                '.mb { font-size: 46px; font-weight: 900; color: #ffd700; line-height: 1; text-align: center; text-shadow: 0 0 30px rgba(255,215,0,0.6); margin-bottom: 5px; letter-spacing: 4px; font-family: Impact, sans-serif; } '
                '.rl { text-align: center; font-size: 13px; font-weight: 900; color: #ff003c; margin-bottom: 15px; letter-spacing: 2px; } '
                '.vb { display:flex; justify-content:space-between; text-align:center; background:rgba(0,0,0,0.8); border:1px solid rgba(255,0,60,0.4); padding:10px; border-radius:8px; margin-bottom: 15px; gap: 5px; } '
                '.ft { text-align: center; color: #64748b; font-size: 8px; padding-top: 10px; line-height: 1.6; font-family: monospace; position: relative; z-index: 2; margin-top: 10px;} '
                '.stat-row { display: flex; align-items: center; margin-bottom: 8px; font-size: 10px; font-weight: bold; justify-content: space-between; } '
                '.sbc { background: rgba(255,255,255,0.05); border-radius: 3px; height: 5px; width: 130px; position: relative; overflow: hidden; margin: 0 6px; } '
                '.sbf { position: absolute; left: 0; top: 0; height: 100%; } '
                '.action-btn { background: linear-gradient(90deg, #ff003c, #9f1239); color: #fff; border: none; padding: 15px 30px; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; box-shadow: 0 5px 15px rgba(255,0,60,0.4); margin-top: 20px; text-transform: uppercase; width: 320px; transition: all 0.2s ease;} '
                '#result-img { display: none; width: 320px; border-radius: 12px; margin: 0 auto; box-shadow: 0 0 30px rgba(255,0,60,0.6); margin-top: 20px; border: 2px solid #ff003c; } '
                '.success-msg { display: none; color: #10b981; font-weight: bold; margin-top: 15px; font-size: 14px; background: rgba(16,185,129,0.1); padding: 10px; border-radius: 6px; border: 1px solid #10b981; width: 320px; margin: 15px auto 0 auto; box-sizing: border-box; }</style>'
            )

            HTML_POSTER_BODY = (
                '<div id="html-card"><div class="capture-box" id="capture-target">'
                '<div class="cyber-grid"></div><div class="psa-header"><div>'
                '<div style="font-size:12px; font-weight:900; color:#fff; letter-spacing:1px; margin-bottom:2px;">SDE AUTHENTICATED</div>'
                '<div style="font-size:9px; color:#fca5a5; font-family:monospace;">CERT: ' + hash_code[:10] + '</div></div>'
                '<div style="display:flex; align-items:center; gap:10px;"><div class="psa-desc">WAR<br>ZONE</div><div class="psa-grade">10</div></div></div>'
                '<div class="inner-card"><div style="position: absolute; top: 15px; right: -35px; background: ' + tier_color + '; color: #000; font-weight: 900; font-size: 10px; padding: 3px 35px; transform: rotate(45deg); z-index: 10; letter-spacing: 2px; box-shadow: 0 0 15px ' + border_color + '88;">' + tier_level + '</div>'
                '<div class="hd"><div style="font-size:13px;font-weight:900; color:#ff003c; letter-spacing:1px;">DESPERATE TCG</div>'
                '<div style="font-size:9px;color:#94a3b8; font-weight:bold;">LV.' + str(st.session_state.level) + ' EDITION</div></div>'
                '<div style="font-size:9px;color:#94a3b8;text-align:center;margin-bottom:5px;">MERCENARY ID</div>'
                '<div class="nm">' + full_title + '</div><div class="mb">' + mbti + '</div>'
                '<div style="text-align:center;font-size:10px;color:#94a3b8;margin-bottom:15px; font-weight:bold;">RARITY: <span style="color:' + border_color + ';font-size:12px;">' + data.get('rarity', 'Top 5%') + '</span></div>'
                '<div class="rl">【 ' + role_name + ' 】</div>'
                '<div class="vb"><div style="flex:1;"><div style="font-size:9px;color:#94a3b8;margin-bottom:5px;">COMBAT POWER</div><div style="font-size:16px;color:#ffd700;font-weight:900;">' + "{:,}".format(final_cp) + '</div></div>'
                '<div style="border-left:1px dashed rgba(255,0,60,0.3);"></div>'
                '<div style="flex:1;"><div style="font-size:9px;color:#94a3b8;margin-bottom:5px;">SURVIVAL RATE</div><div style="font-size:16px;color:#ff003c;font-weight:900;">TOP ' + "{:.1f}".format(100-pct_beat_final) + '%</div></div></div>'
                '<div style="text-align:center; margin-bottom:12px;"><div style="font-size:10px; color:#ff003c; margin-bottom:6px; font-weight:bold;">[ ABILITY MOVES ]</div>' + skills_html_poster + '</div>'
                '<div style="text-align:center; margin-bottom:15px;">' + tags_html_poster + '</div>'
                '<div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(255,0,60,0.2); border-radius: 8px; padding: 12px 10px; margin-bottom: 10px;">'
                '<div style="font-size: 8px; color: #ff003c; text-align: center; margin-bottom: 8px; font-family: monospace;">/// BASE STATS ///</div>'
                '<div class="stat-row"><span style="color:#e2e8f0; width:35px;">输出</span><div class="sbc"><div class="sbf" style="width:' + str(val_E) + '%; background:#ff003c;"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">隐匿</span></div>'
                '<div class="stat-row"><span style="color:#e2e8f0; width:35px;">精准</span><div class="sbc"><div class="sbf" style="width:' + str(val_S) + '%; background:#a855f7;"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">视界</span></div>'
                '<div class="stat-row"><span style="color:#e2e8f0; width:35px;">护甲</span><div class="sbc"><div class="sbf" style="width:' + str(val_T) + '%; background:#3b82f6;"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">光环</span></div>'
                '<div class="stat-row" style="margin-bottom:0;"><span style="color:#e2e8f0; width:35px;">秩序</span><div class="sbc"><div class="sbf" style="width:' + str(val_J) + '%; background:#10b981;"></div></div><span style="color:#94a3b8; width:35px; text-align:right;">敏捷</span></div></div>'
                '<div style="font-size:11px; font-weight:bold; color:#10b981; text-align:center; border-top:1px dashed #330011; padding-top:10px;">军火：<span style="color:#ffd700;">' + relics_text + '</span></div>'
                '<div style="font-size:11px; font-weight:bold; color:#00f3ff; text-align:center; margin-top:5px;">机甲：<span style="color:#ffd700;">' + pet_text + '</span></div></div>'
                '<div class="ft"><div style="width: 90%; height: 20px; margin: 0 auto 8px auto; background: ' + barcode_css + ';"></div>'
                '<div style="margin-bottom:2px;font-weight:bold;">SDE WARFRAME TCG V42.0</div><div style="color:#475569;">© ' + COPYRIGHT + ' | ID: #' + str(token_id) + '</div></div></div>'
                '<button class="action-btn" id="btn-render" onclick="execRender()">📸 点击生成纯净图片版</button></div>'
                '<img id="result-img" alt="SDE Matrix Slab" title="长按保存或分享" />'
                '<div id="success-msg" class="success-msg">✅ <b>图片压制成功！</b><br>👆 手机端请长按上方图片保存发圈。</div>'
            )

            JS_SCRIPT = (
                '<script>function execRender() { var btn = document.getElementById("btn-render"); btn.innerHTML = "⏳ 正在压制，请稍候..."; btn.style.opacity = "0.7"; '
                'if(typeof html2canvas === "undefined") { btn.innerHTML = "❌ 环境不支持，请直接手机系统截屏"; btn.style.opacity = "1"; return; } '
                'setTimeout(function() { html2canvas(document.getElementById("capture-target"), { scale: 2, backgroundColor: "#050205", useCORS: true, logging: false }).then(function(canvas) { '
                'document.getElementById("result-img").src = canvas.toDataURL("image/png"); document.getElementById("result-img").style.display = "block"; document.getElementById("html-card").style.display = "none"; document.getElementById("success-msg").style.display = "block"; '
                '}).catch(function(e) { btn.innerHTML = "❌ 生成失败，请直接手机系统截屏"; btn.style.opacity = "1"; }); }, 200); }</script>'
            )

            final_html = "<!DOCTYPE html><html><head><meta charset='utf-8'><script src='https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js'></script>" + POSTER_CSS + "</head><body>" + HTML_POSTER_BODY + JS_SCRIPT + "</body></html>"
            st.components.v1.html(final_html.replace('\n', ''), height=1050)

        with tm2:
            safe_html("<div style='font-size:13px; color:#94a3b8; margin-bottom:10px; margin-top:10px;'>👇 长按下方文本框，可一键全选并复制纯文字名片：</div>")
            relics_str_txt = "、".join([r['name'] for r in st.session_state.equipped_relics]) if st.session_state.equipped_relics else "无"
            pet_str_txt = st.session_state.equipped_pet.get('name', '') if st.session_state.equipped_pet else "无"
            faction_str_txt = st.session_state.joined_faction if st.session_state.joined_faction else "无界流浪佣兵"
            
            share_card = f"""【SDE 职场元宇宙：不朽神明 V42】
=================================
👤 幸存者代号：{safe_alias_final}
🎖️ 史诗军衔：{st.session_state.equipped_title}
💎 战力估值：{final_cp:,} CP (Lv.{st.session_state.level})
🧬 核心架构：{mbti} ({role_name})
🛡️ 所属阵营：{faction_str_txt}
👑 生存段位：{rank_name}
⚡️ 存活率击败：全球 TOP {100 - pct_beat_final:.1f}%
⚔️ 专属武装：{relics_str_txt}
🐾 伴生机甲：{pet_str_txt}
🎴 卡面工艺：{card_foil}
🚀 终极演进：{data.get('ultimate_evolution', '')}
=================================
🌐 2026 齿轮转动，万物同调。
🔗 [Token ID: #{token_id} | Hash: 0x{hash_code[:8]}]"""
            
            safe_share = html.escape(share_card).replace('\n', '<br>')
            HTML_TXT = """<div style="background-color: #050505 !important; border: 1px solid #334155 !important; border-left: 4px solid #ff003c !important; border-radius: 8px; padding: 20px; overflow-x: hidden; margin-bottom: 20px; margin-top: 10px; box-shadow: inset 0 0 20px rgba(255,0,60,0.2); user-select: all; -webkit-user-select: all;"><div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 13px; color: #e2e8f0 !important; line-height: 1.7; word-break: break-all; word-wrap: break-word; cursor: text;">""" + safe_share + """</div></div>"""
            safe_html(HTML_TXT)
            
        with tm3:
            safe_html("<div style='font-family:Orbitron; font-size:14px; font-weight:bold; color:#10b981; margin-bottom:10px; border-bottom:1px dashed #10b981; padding-bottom:8px; margin-top:15px;'>/// SOLIDITY SMART CONTRACT</div>")
            code_block = "// SPDX-License-Identifier: MIT\npragma solidity ^0.8.20;\nimport \"@sde-network/contracts/token/ERC721.sol\";\n\ncontract SDE_Card_Registry_V42 is ERC721 {\n    struct CardStats {\n        string matrix_id;\n        uint256 combat_power;\n        uint8 level;\n        uint8 ascension_stars;\n    }\n    \n    mapping(uint256 => CardStats) public deck;\n    \n    constructor() ERC721(\"SDE_WAR_V42\", \"SDEWAR\") {}\n\n    // MINTED_TO: " + safe_alias_final + "\n    // BLOCK_HEIGHT: " + block_height + "\n    // CONTRACT_ADDR: " + contract_addr + "\n    \n    function executeMint() public {\n        uint256 tokenId = " + str(token_id) + ";\n        deck[tokenId] = CardStats(\"" + mbti + "\", " + str(final_cp) + ", " + str(st.session_state.level) + ", " + str(st.session_state.ascension_stars) + ");\n        _mint(msg.sender, tokenId);\n    }\n}"
            safe_code = html.escape(code_block).replace('\n', '<br>')
            HTML_SOLIDITY = "<div style=\"background: #050505; border-radius: 8px; border: 1px solid #334155; border-left: 4px solid #10b981; width: 100%; box-sizing: border-box; box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(0,243,255,0.05); margin-top: 15px; margin-bottom: 20px; overflow: hidden;\"><div style=\"background: #14050a; padding: 10px 15px; display: flex; align-items: center; border-bottom: 1px solid #330011;\"><div style=\"width: 12px; height: 12px; border-radius: 50%; background: #ff5f56; margin-right: 8px;\"></div><div style=\"width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e; margin-right: 8px;\"></div><div style=\"width: 12px; height: 12px; border-radius: 50%; background: #27c93f; margin-right: 15px;\"></div><div style=\"color: #94a3b8; font-size: 11px; font-family: 'Fira Code', monospace; letter-spacing: 1px;\">SDE_Smart_Contract.sol</div></div><div style=\"padding: 15px; overflow-x: hidden;\"><div style=\"margin: 0; font-family: 'Fira Code', monospace; font-size: 12px; color: #10b981 !important; line-height: 1.6; background: transparent; border: none; user-select: all; -webkit-user-select: all; cursor: text; word-break: break-all;\">" + safe_code + "</div></div></div>"
            safe_html(HTML_SOLIDITY)

        with tm4:
            safe_html("<div style='font-size:13px; color:#94a3b8; margin-bottom:15px; margin-top:10px;'>💾 幸存者视角：导出您的原生底层 JSON 结构树归档：</div>")
            export_data = {
                "version": VERSION,
                "node_alias": safe_alias_final, 
                "equipped_title": st.session_state.equipped_title,
                "card_title": full_title,
                "rank_tier": rank_name,
                "matrix_id": mbti, 
                "faction": faction_data,
                "joined_guild": st.session_state.joined_faction,
                "role": role_name, 
                "tier": tier_level, 
                "foil_variant": card_foil,
                "ascension_stars": st.session_state.ascension_stars,
                "soulbound_token": {
                    "contract": contract_addr,
                    "token_id": token_id,
                    "hash_signature": hash_code,
                    "block_height": block_height
                },
                "war_stats": {
                    "level": st.session_state.level,
                    "exp": st.session_state.exp,
                    "san_points": st.session_state.sanity,
                    "despair_level": st.session_state.despair_level,
                    "tokens_sde": st.session_state.tokens,
                    "dark_matter": st.session_state.dark_matter,
                    "logic_shards": st.session_state.logic_shards,
                    "combat_power_cp": final_cp, 
                    "cyber_augments": st.session_state.cyber_augments,
                    "talent_tree": st.session_state.talent_levels,
                    "active_tarot_buff": st.session_state.tarot_buff,
                    "mining_rigs": st.session_state.gpus,
                    "squad_members": st.session_state.squad
                },
                "metrics": {"E_I": val_E, "S_N": val_S, "T_F": val_T, "J_P": val_J},
                "equipped_relics": st.session_state.equipped_relics,
                "equipped_pet": st.session_state.equipped_pet,
                "ultimate_evolution": data.get('ultimate_evolution', ''),
                "timestamp": current_time_str
            }
            json_str = json.dumps(export_data, indent=4, ensure_ascii=False)
            st.download_button(label="📥 立即下载节点加密档案 (.JSON)", data=json_str, file_name=f"SDE_OMNIVERSE_{safe_alias_final}.json", mime="application/json", use_container_width=True)

    c_e1, c_btn, c_e2 = st.columns([1, 2, 1])
    with c_btn:
        safe_html("<br>")
        st.button("☢️ 强制格式化神经元并重置世界 (WIPE_AND_REBOOT)", on_click=reset_system, type="primary", use_container_width=True)

# =========================================================================
# 🛑 [ OMNIVERSE 08 ] 赛博呼吸专属版权区
# =========================================================================
HTML_FOOTER = """<div style="text-align:center; margin-top:80px; margin-bottom:40px; position:relative; z-index:10;"><div style="color:#ff003c !important; font-family:'Orbitron', monospace; font-size:10px; opacity:0.3; letter-spacing:6px; margin-bottom:8px;">POWERED BY ULTIMATE ECOSYSTEM ENGINE</div><div style="color:#ff003c !important; font-family:'Orbitron', monospace; font-size:10px; opacity:0.2; letter-spacing:3px; margin-bottom:30px;">SYSTEM VERSION: """ + VERSION + """</div><div style="display: inline-block; padding: 12px 40px; border-radius: 50px; font-size: 13px; font-family: 'Noto Sans SC', sans-serif; letter-spacing: 3px; color: #ff003c; font-weight: 900; background: rgba(255,0,60,0.05); border: 1px solid rgba(255,0,60,0.3); box-shadow: 0 0 20px rgba(255,0,60,0.15);">© 2026 版权归属 · <b style="font-family:'Orbitron', sans-serif; letter-spacing: 4px;">""" + COPYRIGHT + """</b></div></div>"""
safe_html(HTML_FOOTER)
# ================================= EOF ==================================
