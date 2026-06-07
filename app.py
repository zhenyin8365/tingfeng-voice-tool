"""
庭锋顺锋·AI语音工坊 — 翁大锋旗下庭锋装饰集团 + 那隆顺锋家私 多员工AI语音合成工具
"""

import streamlit as st

st.set_page_config(page_title="庭锋顺锋·AI语音工坊", page_icon="🏗️", layout="centered")

SLOT_COUNT = 6
AGNES_KEY = "sk-SfAuFKTIGg8WCkhwRYgVZGhSNazYLgrSbI4dYWrSBsM2RrCK"

# ── 从 URL 恢复配置 ──
try:
    qp = st.query_params
    saved_key = qp.get("key", "")
    saved_slots = []
    for i in range(1, SLOT_COUNT + 1):
        saved_slots.append({
            "name": qp.get(f"name{i}", ""),
            "voice": qp.get(f"voice{i}", ""),
        })
except Exception:
    saved_key = ""
    saved_slots = [{"name": "", "voice": ""} for _ in range(SLOT_COUNT)]

# ── 品牌色系 ──
st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(135deg, #1a5276, #2980b9) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    padding: 12px 24px !important; font-weight: 700 !important; width: 100%;
}
.stButton>button:hover { background: linear-gradient(135deg, #2980b9, #3498db) !important; }
.audio-box {
    background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.1);
    border-radius: 14px; padding: 20px; text-align: center; margin: 16px 0;
}
.pill {
    display: inline-block; background: rgba(41,128,185,.25); color: #85c1e9;
    border-radius: 20px; padding: 4px 14px; font-size: 13px; font-weight: 600; margin: 4px;
}
.employee-card {
    background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.08);
    border-radius: 12px; padding: 14px; margin-bottom: 10px;
}
.employee-card h4 { color: #85c1e9; margin: 0 0 8px 0; }
.dept-tag {
    display: inline-block; background: rgba(41,128,185,.15); color: #85c1e9;
    border-radius: 8px; padding: 2px 10px; font-size: 11px; margin-left: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#85c1e9;text-align:center'>🏗️ 庭锋顺锋·AI语音工坊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aab7c4;margin-bottom:5px'>庭锋装饰集团 · 那隆顺锋家私 | 翁大锋旗下品牌</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aab7c4;margin-bottom:30px'>6位员工专属声音 · 输入文字即合成语音</p>", unsafe_allow_html=True)

# ====== 第一步：配置 ======
with st.expander("第一步：配置（填一次即可）", expanded=(not saved_key)):
    api_key = st.text_input("阿里云百炼 API-Key（语音合成）", type="password", value=saved_key,
        placeholder="sk-xxxxxxxxxxxxxxxx",
        help="用于语音合成，由管理员统一填写。")

    st.markdown("[🔑 去获取阿里云API KEY](https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key)")

    st.markdown("---")
    st.markdown("<p style='color:#85c1e9;font-weight:600'>员工声音配置（6个槽位）</p>", unsafe_allow_html=True)
    st.caption("每位员工填写姓名和对应的复刻音色ID，不用的槽位留空即可。")

    st.markdown("[🎙️ 去获取声音复刻ID](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_experience_center/voice?currentTab=voiceTts&primary=cloning&secondary=clone)")

    slots = []
    for i in range(SLOT_COUNT):
        with st.container():
            tag = "庭锋装饰" if i < 3 else "那隆顺锋"
            st.markdown(f"<div class='employee-card'><h4>声音 {i+1}<span class='dept-tag'>{tag}</span></h4>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("员工姓名", key=f"slot_name_{i}",
                    value=saved_slots[i]["name"],
                    placeholder="如：张经理" if i < 3 else "如：陈经理",
                    label_visibility="collapsed")
            with c2:
                voice = st.text_input("音色ID", key=f"slot_voice_{i}",
                    value=saved_slots[i]["voice"],
                    placeholder="cosyvoice-v3.5-plus-bailian-xxxxxxxx",
                    label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
            slots.append({"name": name, "voice": voice})

    if st.button("保存全部配置", use_container_width=True):
        if not api_key.strip():
            st.error("请先填写 API-Key。")
        else:
            st.query_params["key"] = api_key.strip()
            for i, s in enumerate(slots):
                st.query_params[f"name{i+1}"] = s["name"].strip()
                st.query_params[f"voice{i+1}"] = s["voice"].strip()
            st.rerun()

# ── 检查已配置的员工 ──
configured = [(s["name"].strip(), s["voice"].strip()) for s in slots if s["name"].strip() and s["voice"].strip()]

# ====== 第二步：选择员工 ======
st.markdown("<h3 style='color:#85c1e9'>第二步：选择员工声音</h3>", unsafe_allow_html=True)

if not configured:
    st.warning("请先在第一步配置中至少填写一位员工的姓名和音色ID。")
    selected_name = None
    selected_voice = None
else:
    employee_names = [name for name, _ in configured]
    selected_name = st.selectbox("当前使用的声音", employee_names,
        help="选择要用哪位员工的声音进行合成")
    selected_voice = None
    for name, voice in configured:
        if name == selected_name:
            selected_voice = voice
            break

# ====== 第三步：AI文案生成 ======
st.markdown("<h3 style='color:#85c1e9'>第三步：AI文案生成</h3>", unsafe_allow_html=True)
st.caption("点击产品按钮，AI 自动生成一条口播文案，然后直接合成语音。")

ai_products = {
    "🛋️ 沙发": "帮我写一条抖音短视频口播文案，推广一款真皮沙发，突出舒适、耐用、厂家直销价格优惠。字数80字左右，语气亲切自然。",
    "🍵 茶桌": "帮我写一条抖音短视频口播文案，推广一款实木功夫茶桌，突出新中式风格、卯榫工艺、适合客厅书房。字数80字左右，语气亲切自然。",
    "🛏️ 床垫": "帮我写一条抖音短视频口播文案，推广一款乳胶床垫，突出护脊、透气、独立弹簧。字数80字左右，语气亲切自然。",
    "🪑 餐桌": "帮我写一条抖音短视频口播文案，推广一款可伸缩岩板餐桌，突出现代简约、耐刮耐磨、小户型变大桌。字数80字左右，语气亲切自然。",
    "🗄️ 衣柜": "帮我写一条抖音短视频口播文案，推广一款定制整体衣柜，突出收纳空间大、板材环保、免费量尺设计。字数80字左右，语气亲切自然。",
    "🛌 实木床": "帮我写一条抖音短视频口播文案，推广一款白橡木实木大床，突出卯榫结构、承重稳固、进口木材。字数80字左右，语气亲切自然。",
}

cols = st.columns(6)
for idx, (label, prompt) in enumerate(ai_products.items()):
    with cols[idx % 6]:
        if st.button(label, key=f"ai_{idx}", use_container_width=True):
            with st.spinner(f"AI 正在为你生成{label}口播文案..."):
                try:
                    import requests as req
                    ai_resp = req.post(
                        "https://apihub.agnes-ai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {AGNES_KEY}",
                            "Content-Type": "application/json",
                        },
                            json={
                                "model": "agnes-2.0-flash",
                                "messages": [
                                    {"role": "system", "content": "你是一个专业的抖音家具口播文案写手。回复只输出文案本身，不加任何解释、引号或前缀。语气要自然，像朋友推荐。"},
                                    {"role": "user", "content": prompt},
                                ],
                                "max_tokens": 300,
                            },
                            timeout=30,
                        )
                        if ai_resp.status_code == 200:
                            ai_text = ai_resp.json()["choices"][0]["message"]["content"].strip()
                            st.session_state["template_text"] = ai_text
                            st.rerun()
                        else:
                            st.error(f"AI 生成失败：{ai_resp.text[:150]}")
                except Exception as e:
                    st.error(f"AI 生成失败：{e}")

# ====== 第四步：语音合成 ======
st.markdown("<h3 style='color:#85c1e9'>第四步：语音合成</h3>", unsafe_allow_html=True)

text = st.text_area("输入要合成的文字", height=180,
    value=st.session_state.get("template_text", ""),
    placeholder="在这里输入你想说的话，或点击上方 AI 按钮自动生成，或点击下方模板快速填充。",
    max_chars=2000)
st.caption(f"{len(text)} / 2000 字")

# 快捷模板
st.caption("快捷模板（点击自动填入）：")

# ── 庭锋装饰模板 ──
st.markdown("<p style='color:#85c1e9;font-size:13px;margin:4px 0'>庭锋装饰集团</p>", unsafe_allow_html=True)
tf_templates = {
    "📞 装修咨询": "您好，这里是庭锋装饰集团。感谢您的来电，请问有什么可以帮您的？我们提供免费量房、方案设计和预算报价服务。",
    "🏠 开工通知": "您好，我是庭锋装饰的项目经理。您家的装修工程将于下周一正式开工，届时我会提前到现场做开工准备，请您放心。",
    "📋 进度汇报": "您好，您家的装修目前水电改造已完成，下一步是木工进场。预计工期还有30天，我会每周向您汇报进度。",
    "🎉 竣工交付": "恭喜您，您家的装修工程已全面竣工！我们已经完成了全屋保洁，请您抽时间来验收。有任何问题随时联系我。",
    "💼 装修回访": "您好，我是庭锋装饰的客服。想了解一下您入住后的体验如何，对我们装修质量和服务是否满意？",
}
cols = st.columns(5)
for idx, (label, sample) in enumerate(tf_templates.items()):
    with cols[idx % 5]:
        if st.button(label, key=f"tf_{idx}", use_container_width=True):
            st.session_state["template_text"] = sample
            st.rerun()

# ── 那隆顺锋家私模板 ──
st.markdown("<p style='color:#d4a854;font-size:13px;margin:12px 0 4px 0'>那隆顺锋家私</p>", unsafe_allow_html=True)
nl_templates = {
    "🛋️ 家具咨询": "您好，这里是那隆顺锋家私。我们主营实木床、衣柜、沙发、餐桌等全屋家具，厂家直销价格更实惠。请问有什么可以帮您？",
    "📦 订单确认": "您好，您在我们那隆顺锋家私订购的家具已经确认。我们会在48小时内安排生产，预计15天左右完工，届时电话通知您送货。",
    "🚚 送货通知": "您好，您订的家具今天下午送到，请保持电话畅通。我们的师傅会帮忙搬到指定位置并简单安装。",
    "💼 家具回访": "您好，我是那隆顺锋家私的客服。上次买的家具用得还满意吗？有任何质量问题随时联系我们，保修期内免费处理。",
    "🪑 产品介绍": "这款实木大床选用进口白橡木，卯榫结构坚固耐用。配套床头柜和衣柜也可以一起看，全屋配齐更划算。",
}
cols = st.columns(5)
for idx, (label, sample) in enumerate(nl_templates.items()):
    with cols[idx % 5]:
        if st.button(label, key=f"nl_{idx}", use_container_width=True):
            st.session_state["template_text"] = sample
            st.rerun()

# 通用模板
st.markdown("<p style='color:#aab7c4;font-size:13px;margin:12px 0 4px 0'>通用</p>", unsafe_allow_html=True)
common_templates = {
    "📢 品牌宣传": "庭锋装饰集团专注品质家装，那隆顺锋家私厂家直销。翁大锋旗下品牌，真材实料，十年质保。让每一位客户住得放心，用得安心。",
    "🎙️ 自我介绍": "大家好，我是翁大锋，庭锋装饰集团和那隆顺锋家私的创始人。我做装修和家具二十多年，坚持质量第一，服务至上。有任何需求欢迎来找我。",
}
cols = st.columns(4)
for idx, (label, sample) in enumerate(common_templates.items()):
    with cols[idx % 4]:
        if st.button(label, key=f"cm_{idx}", use_container_width=True):
            st.session_state["template_text"] = sample
            st.rerun()

language = st.selectbox("语言",
    options=["普通话", "白话"],
    help="选择合成语音的语言")
lang_hint = "zh" if language == "普通话" else "yue"

col_s1, col_s2 = st.columns(2)
with col_s1:
    speed = st.select_slider("语速", options=[0.8, 1.0, 1.2, 1.3, 1.5], value=1.0)
with col_s2:
    volume = st.slider("音量", min_value=0, max_value=100, value=80)

if st.button("▶ 开始合成", use_container_width=True):
    if not api_key.strip():
        st.error("请先填写 API-Key。")
    elif selected_voice is None:
        st.error("请先选择一位已配置的员工声音。")
    elif not text.strip():
        st.error("请先输入要合成的文字。")
    else:
        with st.spinner(f"正在用 {selected_name} 的声音合成中，请稍候..."):
            try:
                import requests

                resp = requests.post(
                    "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer",
                    headers={
                        "Authorization": f"Bearer {api_key.strip()}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "cosyvoice-v3.5-plus",
                        "input": {
                            "text": text,
                            "voice": selected_voice,
                            "format": "mp3",
                        },
                        "parameters": {
                            "speech_rate": speed,
                            "volume": volume,
                            "language_hints": [lang_hint],
                        },
                    },
                    timeout=60,
                )

                if resp.status_code != 200:
                    st.error(f"合成失败：HTTP {resp.status_code} - {resp.text[:200]}")
                else:
                    result = resp.json()
                    audio_url = result.get("output", {}).get("audio", {}).get("url", "")
                    if not audio_url:
                        st.error(f"未获取到音频链接：{resp.text[:200]}")
                    else:
                        audio_resp = requests.get(audio_url, timeout=30)
                        audio = audio_resp.content
                        audio_size = len(audio) / 1024
                        st.markdown("---")
                        st.markdown("<h3 style='color:#85c1e9'>合成结果</h3>", unsafe_allow_html=True)
                        st.markdown(f"<div class='audio-box'>"
                            f"<span class='pill'>{selected_name}</span>"
                            f"<span class='pill'>语速 {speed}x</span>"
                            f"<span class='pill'>{len(text)} 字</span>"
                            f"<span class='pill'>{audio_size:.0f} KB</span>"
                            f"</div>", unsafe_allow_html=True)
                        st.audio(audio, format="audio/mp3")
                        safe_name = selected_name.replace("/", "-").replace("\\", "-")
                        st.download_button("下载到手机", data=audio,
                            file_name=f"庭锋顺锋_{safe_name}.mp3",
                            mime="audio/mpeg", use_container_width=True)
                        st.toast("合成完成！", icon="✅")
            except Exception as e:
                st.error(f"合成失败：{e}")

# ====== 使用说明 ======
with st.expander("使用说明"):
    st.markdown("**管理员首次设置**")
    st.markdown("1. 填写阿里云百炼 API-Key（两个公司共用一个）")
    st.markdown("2. 声音1~3 填庭锋装饰员工，声音4~6 填那隆顺锋家私员工")
    st.markdown("3. 点击「保存全部配置」")
    st.markdown("4. 把链接发给员工，员工打开网页即可使用")
    st.markdown("")
    st.markdown("**员工日常使用**")
    st.markdown("1. 在下拉框选择自己的名字")
    st.markdown("2. 输入要合成的文字（或点击快捷模板）")
    st.markdown("3. 选择语言、调整语速，点击「开始合成」")
    st.markdown("4. 试听满意后点「下载到手机」")
    st.markdown("")
    st.markdown("**关于声音复刻**")
    st.markdown("每位员工的声音需先在阿里云百炼控制台完成复刻训练（免费），拿到音色ID后填入对应槽位即可使用。")
    st.markdown("")
    st.markdown("如遇到合成失败或任何问题，请联系 **润锋 13307871670**。")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#7f8c8d;font-size:12px;margin-top:30px'>Powered by <b>润锋 AI</b> · 庭锋装饰集团 · 那隆顺锋家私</p>", unsafe_allow_html=True)
