import streamlit as st # type: ignore
import pandas as pd # type: ignore
import pickle
import matplotlib.pyplot as plt # type: ignore
import base64

st.set_page_config(
    page_title="Dari.ma — Estimation de prix",
    page_icon="🏠",
    layout="wide"
)

USERS = {
    "admin": "admin123",
    "user1": "maroc2024",
    "user2": "immo2024"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def login_page():
    img = get_base64_image("images/background.jpg")
    st.markdown(f"""
    <style>
    .block-container {{ padding-top: 0 !important; padding-bottom: 0 !important; }}
    .stApp {{
        background-image: url("data:image/jpg;base64,{img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
 .login-card {{
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(1.5px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255,255,255,0.5);
        padding: 1rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }}
    .login-title {{
        font-size: 38px;
        font-weight: 800;
        color: black;
        text-align: center;
        margin-bottom: 6px;
    }}
    .login-subtitle {{
        font-size: 14px;
        color: black;
        text-align: center;
        margin-bottom: 8px;
    }}
    .login-badge {{
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        font-size: 12px;
        color: rgba(255,255,255,0.9);
        margin-top: 12px;
    }}
    .stButton>button {{
        background: rgba(135,206,235,0.9) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        padding: 10px 24px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100% !important;
    }}
    .stButton>button:hover {{
        background: rgba(15,110,86,0.95) !important;
    }}
    div[data-testid="stTextInput"] input {{
        background: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        border-radius: 10px !important;
        color: white !important;
    }}
    div[data-testid="stTextInput"] input::placeholder {{
        color: rgba(255,255,255,0.7) !important;
    }}
   div[data-testid="stVerticalBlockBorderWrapper"] {{
        padding: 0 !important;
        gap: 0 !important;
    }}
    .stTextInput {{
        margin-top: -20px !important;
        margin-bottom: -12.5px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:38vh'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        st.markdown("""
        <div class='login-card'>
            <div class='login-title'>🏠 Dari.ma</div>
            <div class='login-subtitle'>Estimation intelligente de prix immobilier au Maroc</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:3px'></div>", unsafe_allow_html=True)

        username = st.text_input("", placeholder="👤  Nom d'utilisateur", key="user")
        password = st.text_input("", placeholder="🔒  Mot de passe", type="password", key="pass")

        if st.button("Se connecter →"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Identifiants incorrects")

        st.markdown("""
        <div class='login-badge'>
            Comptes de test &nbsp;|&nbsp;
            <b>admin</b> / admin123 &nbsp;·&nbsp;
            <b>user1</b> / maroc2024
        </div>
        """, unsafe_allow_html=True)

def main_app():
    username = st.session_state.username
    st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem !important; }
    .stButton>button {
        background-color: #1D9E75 !important;
        color: white !important;
        border-radius: 8px !important;
        border: 2px solid white !important;
        width: 100% !important;
        font-weight: bold !important;
    }
    .stButton>button:hover { background-color: #0F6E56 !important; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        st.markdown("""
        <div style='background:#1D9E75;padding:8px 16px;border-radius:8px;
        display:inline-block;margin-top:55px;'>
            <span style='color:white;font-size:15px;font-weight:bold'>🏠 Dari.ma</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='margin-top:55px;'>
            <p style='margin:0;font-size:12px;color:#888;'>Connecté en tant que</p>
            <p style='margin:0;font-size:15px;font-weight:bold;color:#1D9E75;'>👤 {username}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='margin-top:48px'></div>", unsafe_allow_html=True)
        if st.button("🚪 Déconnexion"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    st.markdown("<hr style='margin:8px 0 16px 0'>", unsafe_allow_html=True)

    with open("model/xgboost_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model/label_encoders.pkl", "rb") as f:
        encoders = pickle.load(f)

    df = pd.read_csv("data/annonces_propres_selenium.csv")
    prix_m2_ville = df.groupby("ville")["prix"].mean() / df.groupby("ville")["surface"].mean()
    surface_moy_ville = df.groupby("ville")["surface"].mean()

    st.markdown("### Caractéristiques du bien")
    col1, col2, col3 = st.columns(3)
    with col1:
        ville = st.selectbox("Ville", sorted(df["ville"].unique()))
    with col2:
        surface = st.slider("Surface (m²)", 20, 500, 100)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        estimer = st.button("Estimer le prix")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Annonces disponibles", f"{len(df[df['ville']==ville])}")
    with col2:
        st.metric("Prix moyen au m²", f"{prix_m2_ville.get(ville, 0):,.0f} DH")
    with col3:
        st.metric("Surface moyenne", f"{surface_moy_ville.get(ville, 0):,.0f} m²")
    with col4:
        prix_med = df[df["ville"]==ville]["prix"].median()
        st.metric("Prix médian", f"{prix_med:,.0f} DH")

    if estimer:
        try:
            ville_encoded = encoders["ville"].transform([ville])[0]
            pm2 = prix_m2_ville.get(ville, prix_m2_ville.mean())
            surf_ratio = surface / surface_moy_ville.get(ville, surface_moy_ville.mean())
            X = pd.DataFrame(
                [[surface, ville_encoded, pm2, surf_ratio]],
                columns=["surface", "ville_encoded", "prix_m2_ville", "surface_ratio"]
            )
            prix_estime = model.predict(X)[0]

            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.success(f"### Prix estimé\n# {prix_estime:,.0f} DH")
            with col2:
                st.info(f"### Prix au m²\n# {prix_estime/surface:,.0f} DH/m²")
            with col3:
                prix_min = prix_estime * 0.9
                prix_max = prix_estime * 1.1
                st.warning(f"### Fourchette\n{prix_min:,.0f} — {prix_max:,.0f} DH")

            st.markdown("### Annonces similaires")
            similaires = df[
                (df["ville"] == ville) &
                (df["surface"].between(surface * 0.8, surface * 1.2))
            ][["prix", "surface", "ville"]].head(5)
            if len(similaires) > 0:
                st.dataframe(similaires, use_container_width=True)
            else:
                st.info("Pas d'annonces similaires trouvées.")

        except Exception as e:
            st.error(f"Erreur : {e}")

    st.markdown("---")
    st.markdown("### Analyse du marché")
    tab1, tab2, tab3 = st.tabs(["Distribution des prix", "Prix par ville", "Prix vs Surface"])

    with tab1:
        fig, ax = plt.subplots(figsize=(10, 4))
        df_ville = df[df["ville"] == ville]
        ax.hist(df_ville["prix"], bins=30, color="#1D9E75", edgecolor="white")
        ax.axvline(df_ville["prix"].mean(), color="red", linestyle="--",
                   label=f"Moyenne : {df_ville['prix'].mean():,.0f} DH")
        ax.set_title(f"Distribution des prix à {ville}")
        ax.set_xlabel("Prix (DH)")
        ax.set_ylabel("Nombre d'annonces")
        ax.legend()
        st.pyplot(fig)
        plt.close()

    with tab2:
        fig, ax = plt.subplots(figsize=(10, 4))
        prix_moy = df.groupby("ville")["prix"].mean().sort_values()
        colors = ["#1D9E75" if v == ville else "#B4B2A9" for v in prix_moy.index]
        prix_moy.plot(kind="barh", ax=ax, color=colors)
        ax.set_title("Prix moyen par ville")
        ax.set_xlabel("Prix moyen (DH)")
        st.pyplot(fig)
        plt.close()

    with tab3:
        fig, ax = plt.subplots(figsize=(10, 4))
        df_ville = df[df["ville"] == ville]
        ax.scatter(df_ville["surface"], df_ville["prix"], alpha=0.4, color="#D85A30")
        ax.axvline(surface, color="#7F77DD", linestyle="--",
                   label=f"Surface choisie : {surface}m²")
        ax.set_title(f"Prix vs Surface à {ville}")
        ax.set_xlabel("Surface (m²)")
        ax.set_ylabel("Prix (DH)")
        ax.legend()
        st.pyplot(fig)
        plt.close()

if st.session_state.logged_in:
    main_app()
else:
    login_page()