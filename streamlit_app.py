import streamlit as st
import random
from datetime import date

# ページの設定
st.set_page_config(page_title="バースデー占い", page_icon="🔮")

# タイトルと説明
st.title("🔮 今日のバースデー占い")
st.write("生年月日を入力して、今日の運勢を占ってみましょう！")

# 入力フォーム
with st.sidebar:
    st.header("あなたの情報")
    birthday = st.date_input("生年月日を選択してください", value=date(2000, 1, 1))
    submit_btn = st.button("占う！")

# 占いデータの定義
fortunes = ["絶好調！何事もうまくいく日です。", "安定した運気。自分磨きに最適です。", 
            "少し注意が必要な日。慎重に行動しましょう。", "新しい発見がある予感！", 
            "周りの人に感謝すると運気が上がります。"]
love_fortunes = ["積極的なアプローチが吉。", "聞き手に回ると好感度アップ。", 
                 "自分を信じて真っ直ぐに進んで。", "新しい出会いのチャンスがあるかも。"]
colors = ["レッド", "ブルー", "イエロー", "グリーン", "ピンク", "ゴールド", "パープル", "オレンジ"]

# 占いのロジック
if submit_btn:
    # 今日の日付と誕生日を組み合わせて乱数のシードを固定
    # これにより、同じ誕生日の人はその日一日中、同じ結果が表示されます
    seed_value = int(birthday.strftime('%Y%m%d')) + int(date.today().strftime('%Y%m%d'))
    random.seed(seed_value)

    # ランダムに結果を選択
    today_fortune = random.choice(fortunes)
    today_love = random.choice(love_fortunes)
    lucky_color = random.choice(colors)
    luck_score = random.randint(1, 5)

    # 結果の表示
    st.divider()
    st.header(f"✨ {date.today().strftime('%Y/%m/%d')} の運勢")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("総合運")
        st.write("⭐" * luck_score)
        st.info(today_fortune)
        
    with col2:
        st.subheader("恋愛運")
        st.write(today_love)

    st.subheader("ラッキーカラー")
    st.markdown(f"🎨 今日のあなたの色は **{lucky_color}** です！")

    # お祝い演出
    if luck_score == 5:
        st.balloons()
else:
    st.info("左のサイドバーから生年月日を入力して「占う！」ボタンを押してください。")
