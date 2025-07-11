import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

# Config de la page
st.set_page_config(
    page_title="Analyse Airbnb avec DuckDB",
    page_icon="🏡",
    layout="wide"
)

# Airbnb style : logo, fond, boutons
st.markdown("""
    <style>
    .main {
        background-color: #fff5f7;
    }
    header, footer {
        visibility: hidden;
    }
    .stButton>button {
        color: white;
        background-color: #FF5A5F;
        border: none;
        padding: 0.5em 1em;
        border-radius: 8px;
    }
    h1, h2, h3, .stMetricValue {
        color: #FF5A5F;
    }
    img.airbnb-logo {
        max-height: 60px;
        margin-bottom: 10px;
    }
    </style>

    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_Bélo.svg/1024px-Airbnb_Logo_Bélo.svg.png" class="airbnb-logo" />
""", unsafe_allow_html=True)

# TITRE
st.title("🏠 Analyse Airbnb avec DuckDB")
st.subheader("📁 Importer un fichier CSV")

# UPLOADER CSV
uploaded_file = st.file_uploader("Glissez ou cliquez pour importer un fichier .csv", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, low_memory=False)

        # Nettoyage colonnes
        df.columns = [col.strip() for col in df.columns]
        df.rename(columns=lambda x: x.lower().replace(" ", "_"), inplace=True)

        # Conversion des champs prix et dispo
        if 'price' in df.columns:
            df['price'] = df['price'].astype(str).str.replace(r'[^0-9.]', '', regex=True)
            df['price'] = pd.to_numeric(df['price'], errors='coerce')

        if 'availability_365' in df.columns:
            df['availability_365'] = pd.to_numeric(df['availability_365'], errors='coerce')

        # --- 🔍 FILTRES ---
        if 'neighbourhood_group' in df.columns:
            quartiers = df['neighbourhood_group'].dropna().unique().tolist()
            quartiers.sort()
            quartier_selection = st.multiselect("📍 Filtrer par quartier", quartiers, default=quartiers)
            df = df[df['neighbourhood_group'].isin(quartier_selection)]

        if 'room_type' in df.columns:
            room_types = df['room_type'].dropna().unique().tolist()
            room_types.sort()
            type_selection = st.multiselect("🏘️ Type de logement", room_types, default=room_types)
            df = df[df['room_type'].isin(type_selection)]

        prix_max = st.slider("💸 Prix maximum", 0, int(df['price'].max()), 500)
        df = df[df['price'] <= prix_max]

        st.success("✅ Données filtrées")
        st.dataframe(df.head())

        # --- DuckDB ---
        con = duckdb.connect()
        con.register("airbnb", df)

        # KPI 1
        nb_total = con.execute("SELECT COUNT(*) FROM airbnb").fetchone()[0]

        # KPI 2
        kpi2 = con.execute("""
            SELECT room_type, ROUND(AVG(price), 2) AS prix_moyen
            FROM airbnb
            WHERE price IS NOT NULL
            GROUP BY room_type
        """).df()

        # KPI 3
        kpi3 = con.execute("""
            SELECT neighbourhood_group AS quartier, COUNT(*) AS nb_logements
            FROM airbnb
            GROUP BY quartier
            ORDER BY nb_logements DESC
        """).df()

        # KPI 4
        dispo = con.execute("""
            SELECT ROUND(AVG(availability_365), 2) AS dispo_moyenne
            FROM airbnb
            WHERE availability_365 IS NOT NULL
        """).fetchone()[0]

        # --- Affichage des KPI ---
        st.markdown("### 🔢 Nombre total de logements")
        st.metric("Total", nb_total)

        st.markdown("### 💰 Prix moyen par type de logement")
        st.dataframe(kpi2)

        st.markdown("### 🌍 Répartition par quartier")
        st.dataframe(kpi3)

        st.markdown("### 📆 Disponibilité moyenne sur l'année")
        st.metric("Jours", dispo)

        # --- GRAPHIQUES ---
        st.markdown("## 📊 Visualisations")

        # 1. Histogramme des prix
        fig1, ax1 = plt.subplots()
        sns.histplot(df['price'], bins=50, ax=ax1)
        ax1.set_title("Distribution des prix")
        ax1.set_xlabel("Prix ($)")
        ax1.set_ylabel("Fréquence")
        st.pyplot(fig1)

        # 2. Camembert des types de logements
        fig2, ax2 = plt.subplots()
        kpi2.set_index("room_type").plot.pie(y="prix_moyen", autopct='%1.1f%%', ax=ax2)
        ax2.set_ylabel("")
        ax2.set_title("Répartition des prix moyens")
        st.pyplot(fig2)

        # 3. Barplot quartiers
        fig3, ax3 = plt.subplots()
        sns.barplot(x='quartier', y='nb_logements', data=kpi3, ax=ax3)
        ax3.set_title("Nombre de logements par quartier")
        ax3.tick_params(axis='x', rotation=45)
        st.pyplot(fig3)

        # 4. Disponibilité moyenne
        fig4, ax4 = plt.subplots()
        ax4.bar(["Disponibilité Moyenne"], [dispo], color="#FF5A5F")
        ax4.set_ylabel("Jours")
        ax4.set_title("📆 Disponibilité moyenne (365 jours)")
        st.pyplot(fig4)

    except Exception as e:
        st.error(f"❌ Erreur : {e}")