"""
庭锋装饰集团·AI语音工坊 — 多员工AI语音合成工具
"""

import streamlit as st

st.set_page_config(page_title="庭锋装饰集团·AI语音工坊", page_icon="🏗️", layout="centered")

# ── 从 URL 恢复配置 ──
try:
    qp = st.query_params
    saved_key = qp.get("key", "")
    saved_slots = []
    for i in range(1, 6):
        saved_slots.append({
            "name": qp.get(f"name{i}", ""),
            "voice": qp.get(f"voice{i}", ""),
        })
except Exception:
    saved_key = ""
    saved_slots = [{"name": "", "voice": ""} for _ in range(5)]

# ── 庭锋品牌色系 ──
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
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#85c1e9;text-align:center'>🏗️ 庭锋装饰集团·AI语音工坊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aab7c4;margin-bottom:30px'>5位员工专属声音 · 输入文字即合成语音</p>", unsafe_allow_html=True)

# ====== 第一步：配置 ======
with st.expander("⚙️ 第一步：配置（填一次即可）", expanded=(not saved_key)):
    api_key = st.text_input("阿里云百炼 API-Key", type="password", value=saved_key,
        placeholder="sk-xxxxxxxxxxxxxxxx",
        help="整个公司共用一个 API-Key，由管理员统一填写。")

    st.markdown("[🔑 去获取阿里云API KEY](https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key)")

    st.markdown("---")
    st.markdown("<p style='color:#85c1e9;font-weight:600'>👥 员工声音配置（5个槽位）</p>", unsafe_allow_html=True)
    st.caption("每位员工填写姓名和对应的复刻音色ID，不用的槽位留空即可。")

    st.markdown("[🎙️ 去获取声音复刻ID](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_experience_center/voice?currentTab=voiceTts&primary=cloning&secondary=clone)")

    slots = []
    for i in range(5):
        with st.container():
            st.markdown(f"<div class='employee-card'><h4>声音 {i+1}</h4>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("员工姓名", key=f"slot_name_{i}",
                    value=saved_slots[i]["name"],
                    placeholder=f"如：张经理",
                    label_visibility="collapsed")
            with c2:
                voice = st.text_input("音色ID", key=f"slot_voice_{i}",
                    value=saved_slots[i]["voice"],
                    placeholder="cosyvoice-v3.5-plus-bailian-xxxxxxxx",
                    label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
            slots.append({"name": name, "voice": voice})

    if st.button("💾 保存全部配置", use_container_width=True):
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
st.markdown("<h3 style='color:#85c1e9'>👤 第二步：选择员工声音</h3>", unsafe_allow_html=True)

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

# ====== 第三步：合成 ======
st.markdown("<h3 style='color:#85c1e9'>📝 第三步：语音合成</h3>", unsafe_allow_html=True)

text = st.text_area("输入要合成的文字", height=180,
    value=st.session_state.get("template_text", ""),
    placeholder="在这里输入你想说的话，或者点击下方模板快速填充...",
    max_chars=2000)
st.caption(f"{len(text)} / 2000 字")

# 快捷模板（庭锋装饰场景）
st.caption("💡 快捷模板（点击自动填入）：")
templates = {
    "📞 装修咨询": "您好，这里是庭锋装饰集团。感谢您的来电，请问有什么可以帮您的？我们提供免费量房、方案设计和预算报价服务。",
    "🏠 开工通知": "您好，我是庭锋装饰的项目经理。您家的装修工程将于下周一正式开工，届时我会提前到现场做开工准备，请您放心。",
    "📋 进度汇报": "您好，您家的装修目前水电改造已完成，下一步是木工进场。预计工期还有30天，我会每周向您汇报进度。",
    "🎉 竣工交付": "恭喜您，您家的装修工程已全面竣工！我们已经完成了全屋保洁，请您抽时间来验收。有任何问题随时联系我。",
    "💼 客户回访": "您好，我是庭锋装饰的客服。想了解一下您入住后的体验如何，对我们装修质量和服务是否满意？",
    "📢 品牌宣传": "庭锋装饰集团，专注品质家装二十年。自有施工团队，绝不转包，材料透明，报价实在。让每一位客户住得放心。",
    "🎙️ 自我介绍": "大家好，我是庭锋装饰集团的设计师。我擅长现代简约和新中式风格，已经为上百位客户打造了理想的家。",
}
cols = st.columns(4)
for idx, (label, sample) in enumerate(templates.items()):
    with cols[idx % 4]:
        if st.button(label, key=f"tmpl_{idx}", use_container_width=True):
            st.session_state["template_text"] = sample
            st.rerun()

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
                        st.markdown("<h3 style='color:#85c1e9'>🔊 合成结果</h3>", unsafe_allow_html=True)
                        st.markdown(f"<div class='audio-box'>"
                            f"<span class='pill'>👤 {selected_name}</span>"
                            f"<span class='pill'>语速 {speed}x</span>"
                            f"<span class='pill'>{len(text)} 字</span>"
                            f"<span class='pill'>{audio_size:.0f} KB</span>"
                            f"</div>", unsafe_allow_html=True)
                        st.audio(audio, format="audio/mp3")
                        safe_name = selected_name.replace("/", "-").replace("\\", "-")
                        st.download_button("📥 下载到手机", data=audio,
                            file_name=f"庭锋_{safe_name}.mp3",
                            mime="audio/mpeg", use_container_width=True)
                        st.toast("合成完成！", icon="✅")
            except Exception as e:
                st.error(f"合成失败：{e}")

# ====== 使用说明 ======
with st.expander("📖 使用说明"):
    st.markdown("**管理员首次设置**")
    st.markdown("1. 填写阿里云百炼 API-Key（公司共用一个）")
    st.markdown("2. 在「声音1~5」填好每位员工的姓名和音色ID")
    st.markdown("3. 点击「保存全部配置」")
    st.markdown("4. 把带参数的链接分发给员工（或员工直接打开已保存的页面）")
    st.markdown("")
    st.markdown("**员工日常使用**")
    st.markdown("1. 在下拉框选择自己的名字")
    st.markdown("2. 输入要合成的文字（或点击快捷模板）")
    st.markdown("3. 调整语速，点击「开始合成」")
    st.markdown("4. 试听满意后点「下载到手机」")
    st.markdown("")
    st.markdown("**关于声音复刻**")
    st.markdown("每位员工的声音需先在阿里云百炼控制台完成复刻训练（免费），拿到音色ID后填入对应槽位即可使用。")
    st.markdown("")
    st.markdown("如遇到合成失败或任何问题，请联系 **润锋 13307871670**。")

# ====== 成本明细（演示用） ======
with st.expander("💰 成本明细", expanded=False):
    st.markdown("""
    <style>
    .cost-table { width: 100%; border-collapse: collapse; margin: 10px 0; }
    .cost-table th { background: rgba(41,128,185,.15); color: #85c1e9; padding: 10px; text-align: left; border-bottom: 1px solid rgba(255,255,255,.1); }
    .cost-table td { padding: 10px; border-bottom: 1px solid rgba(255,255,255,.06); color: #d5dde5; }
    .cost-total { font-size: 18px; font-weight: 800; color: #85c1e9; text-align: right; padding: 14px; }
    .cost-discount { color: #e74c3c; font-weight: 700; }
    .cost-final { font-size: 24px; font-weight: 900; color: #2ecc71; text-align: right; padding: 14px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### 庭锋装饰集团 · AI语音工坊成本明细")
    st.caption("以下为阿里云官方收费 + 润锋技术服务费合计")

    st.markdown("""
    <table class="cost-table">
    <tr><th>成本项</th><th>明细</th><th style="text-align:right">金额</th></tr>
    <tr><td>阿里云声音复刻训练</td><td>5位员工 × 每人10分钟样本 + AI模型训练</td><td style="text-align:right">¥1,000</td></tr>
    <tr><td>音色调试 & 验证</td><td>每人测试合成、微调参数、确保自然度</td><td style="text-align:right">¥300</td></tr>
    <tr><td>装修行业模板定制</td><td>咨询/开工/进度/回访/品牌宣传等7个场景</td><td style="text-align:right">¥500</td></tr>
    <tr><td>云端服务器部署</td><td>Streamlit Cloud + 域名 + HTTPS</td><td style="text-align:right">¥300</td></tr>
    <tr><td>一年技术维护</td><td>声音模型更新、模板增改、bug修复</td><td style="text-align:right">¥300</td></tr>
    <tr><td>API调用预充值</td><td>阿里云百炼语音合成</td><td style="text-align:right">¥200</td></tr>
    <tr><td colspan="2" class="cost-total">成本合计</td><td class="cost-total">¥2,600</td></tr>
    <tr><td colspan="2" style="text-align:right;color:#e74c3c;font-weight:700">润锋合作方老客户减免</td><td class="cost-discount" style="text-align:right">-¥1</td></tr>
    <tr><td colspan="2" class="cost-final">实收</td><td class="cost-final">¥2,599</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.caption("润锋是平台合作方，开发利润已代为免除。以上仅为阿里云官方服务成本。")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#7f8c8d;font-size:12px;margin-top:30px'>Powered by <b>润锋 AI</b> · 庭锋装饰集团专属语音工坊</p>", unsafe_allow_html=True)
