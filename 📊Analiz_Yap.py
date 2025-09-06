import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai
import tempfile
import os
import json
from datetime import datetime, timedelta
import pandas_ta as ta  # <-- YENİ EKLENDİ
from plotly.subplots import make_subplots # <-- YENİ EKLENDİ



genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

MODEL_NAME = "gemini-1.5-flash" # Model adını güncelledim
gen_model = genai.GenerativeModel(model_name=MODEL_NAME)


st.set_page_config(page_title="Trader AI", page_icon=":guardsman:", layout="wide")
st.title("Yapay Zeka Destekli Teknik Hisse Analizi :guardsman:")
st.sidebar.header("Konfigürasyonlar")


tickers_input = st.sidebar.text_input("Hisse Sembollerini Giriniz (virgül ile ayırarak)", "ASELS.IS, BIMAS.IS, EREGL.IS, FROTO.IS, GARAN.IS, HALKB.IS")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]


end_date_default = datetime.today()
start_date_default = end_date_default - timedelta(days=120)
start_date = st.sidebar.date_input("Başlangıç Tarihi", value=start_date_default)
end_date = st.sidebar.date_input("Bitiş Tarihi", value=end_date_default)

st.sidebar.subheader("Teknik Göstergeler")
indicators = st.sidebar.multiselect(
    "Teknik İndikatörleri Seçin",
    options=["20-Day SMA", "20-Day EMA", "RSI", "MACD", "20-Day Bollinger Bands"],
    default=["20-Day SMA", "20-Day EMA"]
)


# YUKARIDAKİ ESKİ BLOK YERİNE BUNU YAPIŞTIRIN
if st.sidebar.button("Veriyi Çek"):
    if tickers:
        # Adım 1: Tüm hisseleri tek bir API çağrısıyla, verimli bir şekilde indir.
        # yfinance, sütunları ('Close', 'ASELS.IS') gibi bir MultiIndex olarak döndürür.
        all_data = yf.download(tickers, start=start_date, end=end_date)

        if not all_data.empty:
            stock_data = {}
            # Adım 2: Ana DataFrame'i her bir hisse senedi için döngüde ayır.
            for ticker in tickers:
                # Sadece mevcut 'ticker'a ait sütunları seçiyoruz.
                # Örn: Sadece ('Open', 'ASELS.IS'), ('Close', 'ASELS.IS') vb.
                # .dropna() ile o hissenin işlem görmediği (NaN) günler temizlenir.
                
                # yfinance'in tekil ve çoğul indirme için kullandığı farklı formatları yönetiyoruz
                if len(tickers) > 1:
                    # MultiIndex'ten veri çekme
                    ticker_data = all_data.loc[:, (slice(None), ticker)]
                    ticker_data.columns = ticker_data.columns.droplevel(1) # Sadece 'Open', 'High' kalsın
                else:
                    # Tek hisse indirildiğinde MultiIndex olmaz
                    ticker_data = all_data

                if not ticker_data.empty:
                    stock_data[ticker] = ticker_data.dropna(how='all')
                else:
                    st.warning(f"{ticker} için belirtilen tarih aralığında veri bulunamadı.")

            st.session_state["stock_data"] = stock_data
            if stock_data:
                st.success("Veri başarıyla çekildi: " + ", ".join(stock_data.keys()))
            else:
                st.error("Belirtilen aralıkta hiçbir hisse için veri bulunamadı.")
        else:
            st.error("Belirtilen semboller için hiçbir veri indirilemedi.")
    else:
        st.warning("Lütfen analiz için en az bir hisse sembolü girin.")


if "stock_data" in st.session_state and st.session_state["stock_data"]:

    # ==============================================================================
    # ANALİZ FONKSİYONU - TAMAMEN YENİLENDİ
    # ==============================================================================
    def analyze_ticker(ticker, data):
        # --- 1. Göstergeleri pandas_ta ile hesapla ---
        data.ta.sma(length=20, append=True)
        data.ta.ema(length=20, append=True)
        data.ta.rsi(append=True)
        data.ta.macd(append=True)
        data.ta.bbands(length=20, append=True)

        # --- 2. Alt Grafikleri (Subplots) Oluştur ---
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.6, 0.2, 0.2]
        )

        # --- 3. Ana Fiyat Grafiğini (Candlestick) Ekle ---
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Candlestick"
        ), row=1, col=1)

        # --- 4. Seçilen Göstergeleri İlgili Grafiklere Ekle ---
        def add_indicator_to_plot(indicator):
            if indicator == "20-Day SMA" and 'SMA_20' in data.columns:
                fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], mode='lines', name='20-Day SMA'), row=1, col=1)

            elif indicator == "20-Day EMA" and 'EMA_20' in data.columns:
                fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], mode='lines', name='20-Day EMA'), row=1, col=1)

            elif indicator == "20-Day Bollinger Bands":
                if 'BBL_20_2.0' in data.columns and 'BBU_20_2.0' in data.columns:
                    fig.add_trace(go.Scatter(x=data.index, y=data['BBU_20_2.0'], mode='lines', name='BB Upper', line={'color': 'gray', 'dash': 'dash'}), row=1, col=1)
                    fig.add_trace(go.Scatter(x=data.index, y=data['BBL_20_2.0'], mode='lines', name='BB Lower', line={'color': 'gray', 'dash': 'dash'}, fill='tonexty', fillcolor='rgba(128,128,128,0.1)'), row=1, col=1)

            elif indicator == "RSI" and 'RSI_14' in data.columns:
                fig.add_trace(go.Scatter(x=data.index, y=data['RSI_14'], mode='lines', name='RSI'), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

            elif indicator == "MACD":
                if 'MACD_12_26_9' in data.columns and 'MACDs_12_26_9' in data.columns:
                    fig.add_trace(go.Scatter(x=data.index, y=data['MACD_12_26_9'], mode='lines', name='MACD', line={'color': 'blue'}), row=3, col=1)
                    fig.add_trace(go.Scatter(x=data.index, y=data['MACDs_12_26_9'], mode='lines', name='Signal', line={'color': 'orange'}), row=3, col=1)
                    # Histogram ile ilgili satırlar tamamen silindi.
        for ind in indicators:
            add_indicator_to_plot(ind)

        fig.update_layout(
            title_text=f'{ticker} Teknik Analiz Grafiği',
            xaxis_rangeslider_visible=False,
            yaxis1_title="Fiyat",
            yaxis2_title="RSI",
            yaxis3_title="MACD",
            legend_title="Göstergeler"
        )
        
        # --- 5. Grafik Görüntüsünü Oluşturma ve AI Analizi ---
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            fig.write_image(tmpfile.name, width=1200, height=800)
            tmpfile_path = tmpfile.name
        with open(tmpfile_path, "rb") as f:
            image_bytes = f.read()
        os.remove(tmpfile_path)

        image_part = {
            "data": image_bytes,
            "mime_type": "image/png"
        }

        analysis_prompt = (
            f"You are a Stock Trader specialist in Technical Analysis at a top financial institution."
            f"Analyze the stock data for {ticker} based on its candlestick chart and the displayed technical indicators (RSI and MACD might be in subplots below the main chart)."
            f"Provide a detailed justification for your analysis, explain what patterns, signals, and trends you observe."
            f"Then, based solely on the chart, provide a recommendation from the following options:"
            f"1. Strong Buy, 2. Buy, 3. Weak Buy, 4. Hold, 5. Weak Sell, 6. Sell, 7. Strong Sell"
            f"Return your output in Turkish Language as a JSON object with two keys: 'action' and 'justification'."
        )

        contents = [
            {"role": "user", "parts": [analysis_prompt, image_part]}
        ]
        
        try:
            response = gen_model.generate_content(contents=contents)
            result_text = response.text
            json_start_index = result_text.find('{')
            json_end_index = result_text.rfind('}') + 1
            if json_start_index != -1 and json_end_index > json_start_index:
                json_str = result_text[json_start_index:json_end_index]
                result_json = json.loads(json_str)
            else:
                raise ValueError("Yapay zekadan geçerli bir JSON yanıtı alınamadı.")
        except Exception as e:
            st.error(f"{ticker} için analiz yapılırken hata oluştu: {e}")
            result_json = {"action": "Hata", "justification": f"Analiz sırasında bir hata meydana geldi: {str(e)}"}

        return fig, result_json

    # ==============================================================================
    # SEKMELERİ OLUŞTURMA VE GÖSTERME
    # ==============================================================================
    tab_names = ["Genel Özet"] + list(st.session_state["stock_data"].keys())
    tabs = st.tabs(tab_names)

    overall_results = []

    for i, ticker in enumerate(st.session_state["stock_data"]):
        data = st.session_state["stock_data"][ticker]
        fig, result_json = analyze_ticker(ticker, data)
        overall_results.append({"Hisse": ticker, "Öneri": result_json.get("action", "N/A")})

        with tabs[i + 1]:
            st.subheader(f"{ticker} İçin Teknik Analiz")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader(f"Yapay Zeka Değerlendirmesi: **{result_json.get('action', 'Belirtilmedi')}**")
            st.write("**Detaylı Gerekçe:**")
            st.info(result_json.get("justification", "Gerekçe bulunamadı."))

    with tabs[0]:
        st.subheader("Genel Yapılandırılmış Öneri")
        overall_df = pd.DataFrame(overall_results)
        st.table(overall_df)
else:
    st.info("Hisse senedi sembollerini girin ve analize başlamak için 'Veriyi Çek' butonuna tıklayın.")