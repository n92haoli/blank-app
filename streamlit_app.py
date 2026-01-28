import streamlit as st
import random
from datetime import date
from st_supabase_connection import SupabaseConnection

# ページの設定
st.set_page_config(page_title="バースデー占い", page_icon="🔮")

# --- Supabase 接続の初期化 ---
# .streamlit/secrets.toml の情報を自動で読み込みます
conn = st.connection("supabase", type=SupabaseConnection)

st.title("🔮 今日のバースデー占い")

# メイン画面に入力項目を配置
st.subheader("あなたの生年月日を教えてください")

# 3つのカラムに分けて、年・月・日を数字で入力
col_y, col_m, col_d = st.columns(3)

with col_y:
    year = st.number_input("年", min_value=1900, max_value=2026, value=2000)
with col_m:
    month = st.number_input("月", min_value=1, max_value=12, value=1)
with col_d:
    day = st.number_input("日", min_value=1, max_value=31, value=1)

# ボタンを中央付近に配置
submit_btn = st.button("✨ 今日の運勢を占う ✨", use_container_width=True)

# 占いデータ
fortunes = ["絶好調！", "安定しています", "慎重に！", "新しい発見あり", "感謝を忘れずに"]
love_fortunes = ["積極性が吉", "聞き上手になって", "自分を信じて", "出会いの予感"]
colors = ["レッド", "ブルー", "イエロー", "グリーン", "ピンク", "ゴールド", "パープル", "オレンジ"]

if submit_btn:
    try:
        # 入力された数値が正しい日付かチェック（例：2月31日などはエラーにする）
        input_birthday = date(year, month, day)
        
        # 乱数のシード設定
        seed_value = int(input_birthday.strftime('%Y%m%d')) + int(date.today().strftime('%Y%m%d'))
        random.seed(seed_value)

        # 結果を生成
        today_fortune = random.choice(fortunes)
        today_love = random.choice(love_fortunes)
        lucky_color = random.choice(colors)
        luck_score = random.randint(1, 5)

        # --- Supabase への保存処理 (改良ポイント) ---
        new_data = {
            "birthday": input_birthday.isoformat(),
            "fortune": today_fortune,
            "luck_score": luck_score
        }
        conn.table("fortune_history").insert(new_data).execute()

        # 表示
        st.divider()
        st.success(f"結果が出ました！ （占った日: {date.today().strftime('%Y/%m/%d')}）")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric(label="運勢スコア", value=f"{luck_score} / 5")
            st.info(f"**総合運:** {today_fortune}")
        with c2:
            st.write("**恋愛運**")
            st.write(today_love)
            st.write(f"**ラッキーカラー:** {lucky_color}")

        if luck_score == 5:
            st.balloons()

    except ValueError:
        st.error("正しい日付を入力してください（例：存在しない日などは占えません）")
# --- 履歴の表示部分 (追加機能) ---
st.divider()
st.subheader("📜 最近の占い履歴")

# Supabase からデータを取得 (最新の10件)
try:
    res = conn.table("fortune_history").select("*").order("created_at", desc=True).limit(10).execute()
    if res.data:
        # 取得したデータを表形式で表示
        st.table(res.data)
    else:
        st.write("履歴はまだありません。")
except Exception as e:
    st.error("履歴の読み込みに失敗しました。RLSの設定やテーブル名を確認してください。")
