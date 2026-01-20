import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Sayfa konfigürasyonu
st.set_page_config(page_title="Film Oylama Dashboard", layout="wide")

def stil_enjekte_et():
    """Uygulama genelinde kullanılacak minimal CSS düzenlemelerini tanımlar."""
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                min-width: 280px;
                max-width: 320px;
            }
            [data-testid="stMetric"] {
                background-color: rgba(255, 255, 255, 0.05);
                padding: 15px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

def veri_yukle():
    """Belirtilen yerel dosya yolundan CSV verisini yükler."""
    dosya_yolu = "data/filmler.csv"
    
    if os.path.exists(dosya_yolu):
        try:
            return pd.read_csv(dosya_yolu)
        except Exception as e:
            st.error(f"Dosya okuma hatası: {str(e)}")
            return None
    else:
        st.error(f"Kritik Hata: Veri dosyası bulunamadı.")
        st.info(f"Lütfen projenin kök dizininde '{dosya_yolu}' dosyasının mevcut olduğundan emin olunuz.")
        return None

def kolon_tespit_et(df):
    """Kolonları analiz eder ve veri tiplerini normalize eder."""
    tespit_edilenler = {
        'puan': next((c for c in df.columns if any(a in c.lower() for a in ['rating', 'puan'])), None),
        'yil': next((c for c in df.columns if any(a in c.lower() for a in ['year', 'yıl'])), None),
        'tur': next((c for c in df.columns if any(a in c.lower() for a in ['genre', 'tür'])), None),
        'isim': next((c for c in df.columns if any(a in c.lower() for a in ['title', 'isim', 'ad'])), df.columns[0])
    }

    for anahtar in ['puan', 'yil']:
        kolon_adi = tespit_edilenler[anahtar]
        if kolon_adi:
            df[kolon_adi] = pd.to_numeric(df[kolon_adi], errors='coerce')
    
    kritik_kolonlar = [tespit_edilenler[k] for k in ['puan', 'yil'] if tespit_edilenler[k]]
    if kritik_kolonlar:
        df.dropna(subset=kritik_kolonlar, inplace=True)
        
    return tespit_edilenler, df

def sidebar_filtreleri(df, kolonlar):
    """Filtreleme bileşenlerini yönetir."""
    f_df = df.copy()
    st.sidebar.subheader("Analiz Filtreleri")
    
    if kolonlar['puan']:
        min_v, max_v = float(df[kolonlar['puan']].min()), float(df[kolonlar['puan']].max())
        secilen_puan = st.sidebar.slider("Puan Aralığı", min_v, max_v, (min_v, max_v))
        f_df = f_df[(f_df[kolonlar['puan']] >= secilen_puan[0]) & (f_df[kolonlar['puan']] <= secilen_puan[1])]
    
    if kolonlar['yil']:
        min_y, max_y = int(df[kolonlar['yil']].min()), int(df[kolonlar['yil']].max())
        secilen_yil = st.sidebar.slider("Yıl Aralığı", min_y, max_y, (min_y, max_y))
        f_df = f_df[(f_df[kolonlar['yil']] >= secilen_yil[0]) & (f_df[kolonlar['yil']] <= secilen_yil[1])]
        
    if kolonlar['tur']:
        tur_serisi = df[kolonlar['tur']].fillna("Bilinmiyor").astype(str)
        tekil_turler = sorted(list(set([t.strip() for satır in tur_serisi for t in satır.split(',') if t.strip()])))
        secilen_turler = st.sidebar.multiselect("Film Türleri", tekil_turler)
        if secilen_turler:
            maske = f_df[kolonlar['tur']].astype(str).apply(lambda x: any(t in x for t in secilen_turler))
            f_df = f_df[maske]
            
    return f_df

def dashboard_grafikleri(df, kolonlar):
    """İstenilen görsel analiz grafiklerini oluşturur."""
    if df.empty:
        return

    # 1. Puan Dağılımı Grafiği
    if kolonlar['puan']:
        st.subheader("Puan Dağılımı")
        fig_hist = px.histogram(
            df, 
            x=kolonlar['puan'], 
            nbins=20, 
            labels={kolonlar['puan']: 'Puan'},
            template="plotly_dark"
        )
        fig_hist.update_layout(bargap=0.1)
        st.plotly_chart(fig_hist, use_container_width=True)

    col1, col2 = st.columns(2)

    # 2. Yıllara Göre Ortalama Puan Grafiği
    if kolonlar['yil'] and kolonlar['puan']:
        with col1:
            st.subheader("Yıllara Göre Filmlerin benden aldığı puanların ortalaması")
            yil_gruplu = df.groupby(kolonlar['yil'])[kolonlar['puan']].mean().reset_index()
            fig_yil = px.line(
                yil_gruplu, 
                x=kolonlar['yil'], 
                y=kolonlar['puan'], 
                markers=True,
                labels={kolonlar['yil']: 'Yıl', kolonlar['puan']: 'Ortalama Puan'},
                template="plotly_dark"
            )
            st.plotly_chart(fig_yil, use_container_width=True)

    # 3. Türlere Göre Ortalama Puan Grafiği
    if kolonlar['tur'] and kolonlar['puan']:
        with col2:
            st.subheader("Türlere Göre Ortalama Puanlar")
            tur_df = df.copy()
            tur_df[kolonlar['tur']] = tur_df[kolonlar['tur']].fillna("").astype(str)
            tur_df['gecici_tur'] = tur_df[kolonlar['tur']].str.split(',')
            tur_df = tur_df.explode('gecici_tur')
            tur_df['gecici_tur'] = tur_df['gecici_tur'].str.strip()
            
            tur_df = tur_df[tur_df['gecici_tur'] != ""]
            
            tur_gruplu = tur_df.groupby('gecici_tur')[kolonlar['puan']].mean().reset_index()
            tur_gruplu = tur_gruplu.sort_values(by=kolonlar['puan'], ascending=False)
            
            fig_tur = px.bar(
                tur_gruplu, 
                x='gecici_tur', 
                y=kolonlar['puan'],
                labels={'gecici_tur': 'Tür', kolonlar['puan']: 'Ortalama Puan'},
                template="plotly_dark"
            )
            st.plotly_chart(fig_tur, use_container_width=True)

def dashboard_metrikleri(df, kolonlar):
    """Genel istatistiksel verileri sunar."""
    if kolonlar['puan'] and not df.empty:
        ort_puan = df[kolonlar['puan']].mean()
        st.metric(label="Filtrelenmiş Veri Ortalama Puanı", value=f"{ort_puan:.2f}")

def dashboard_tablolar(df, kolonlar):
    """Sıralı listeleri ve ham veriyi sunar."""
    if kolonlar['puan'] and not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("En yüksek oy verdiğim filmler")
                st.table(df.sort_values(by=kolonlar['puan'], ascending=False).head(10)[[kolonlar['isim'], kolonlar['puan']]])
        with c2:
            with st.container(border=True):
                st.subheader("En beğenmediklerim")
                st.table(df.sort_values(by=kolonlar['puan'], ascending=True).head(10)[[kolonlar['isim'], kolonlar['puan']]])
            
    st.markdown("---")
    st.subheader("Film Listem")
    st.dataframe(df, use_container_width=True, hide_index=True)

def main():
    """Uygulama ana akış kontrolü."""
    stil_enjekte_et()
    st.title("Film Oylama Analitik Paneli")
    st.markdown("_Veri seti üzerinden dinamik filtreleme ve görsel analiz arayüzü._")
    st.markdown("---")
    
    ham_df = veri_yukle()
    if ham_df is not None:
        # Yüklenen film sayısı bildirimi
        st.success(f"Toplam {len(ham_df)} adet film veritabanından başarıyla yüklendi.")
        
        kolon_bilgisi, temiz_df = kolon_tespit_et(ham_df)
        sonuc_df = sidebar_filtreleri(temiz_df, kolon_bilgisi)
        
        # Filtreleme sonucu durum bildirimi
        if sonuc_df.empty:
            st.warning("Seçilen filtre kriterlerine uygun film bulunamadı. Lütfen filtreleri gevşetiniz.")
        else:
            st.info(f"Şu an filtrelenmiş {len(sonuc_df)} adet film görüntüleniyor.")
            
            # --- CSV İNDİRME BUTONU ---
            st.sidebar.markdown("---")
            csv_data = sonuc_df.to_csv(index=False).encode('utf-8')
            st.sidebar.download_button(
                label="📥 Filtrelenmiş Veriyi İndir",
                data=csv_data,
                file_name="filtered_movies.csv",
                mime="text/csv",
                help="Mevcut filtreleme sonuçlarını CSV dosyası olarak bilgisayarınıza indirir."
            )
            # --------------------------
            
            dashboard_metrikleri(sonuc_df, kolon_bilgisi)
            dashboard_grafikleri(sonuc_df, kolon_bilgisi)
            st.write("") 
            dashboard_tablolar(sonuc_df, kolon_bilgisi)
    else:
        # Dosya bulunamadığı için veri_yukle fonksiyonu zaten hata mesajı bastı.
        # Burada ekstra bir şey yapmaya gerek yok, akış durur.
        pass

if __name__ == "__main__":
    main()