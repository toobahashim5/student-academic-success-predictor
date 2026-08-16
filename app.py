import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Academic Success Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. DESIGN SYSTEM
#    Direction: academic transcript / diploma. Navy + brass-gold on
#    parchment, serif display type for gravitas, thin gold rules
#    instead of boxed "card soup". The result reads like an official
#    record entry rather than a generic dashboard widget.
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    :root {
        --ink:        #16213E;
        --ink-light:  #253863;
        --parchment:  #FAF7F0;
        --gold:       #B8935F;
        --gold-light: #E8D5B7;
        --charcoal:   #2B2B2B;
        --muted:      #6B6458;
        --pass-green: #2F5233;
        --fail-maroon:#8B2635;
    }

    .stApp { background-color: var(--parchment); }

    /* ---- Letterhead header ---- */
    .letterhead {
        background: var(--ink);
        margin: -1rem -1rem 2rem -1rem;
        padding: 2.4rem 3rem 1.6rem 3rem;
        border-bottom: 4px solid var(--gold);
    }
    .letterhead .eyebrow {
        color: var(--gold-light);
        font-size: 0.72rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .letterhead h1 {
        font-family: 'Playfair Display', serif;
        color: #FFFFFF;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.15;
    }
    .letterhead p {
        color: #C9CEDD;
        font-size: 0.98rem;
        margin-top: 0.6rem;
        max-width: 640px;
    }

    /* ---- Section headers: editorial, not boxed ---- */
    .section-eyebrow {
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 700;
        color: var(--gold);
        margin-bottom: 0.15rem;
        margin-top: 1.6rem;
    }
    .section-heading {
        font-family: 'Playfair Display', serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 0.7rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--gold-light);
    }

    /* ---- Inputs: quieten Streamlit defaults, add hover/focus states ---- */
    div[data-baseweb="select"] > div {
        border-radius: 4px !important;
        border-color: #DCD3C2 !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 1px var(--gold);
    }
    div[data-baseweb="select"][aria-expanded="true"] > div {
        border-color: var(--ink) !important;
        box-shadow: 0 0 0 1px var(--ink);
    }
    /* dropdown option list */
    ul[role="listbox"] li:hover {
        background-color: var(--gold-light) !important;
        color: var(--ink) !important;
    }
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: var(--gold) !important;
        color: #FFFFFF !important;
    }
    .stNumberInput input {
        border-radius: 4px !important;
        border-color: #DCD3C2 !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .stNumberInput input:hover {
        border-color: var(--gold) !important;
    }
    .stNumberInput input:focus {
        border-color: var(--ink) !important;
        box-shadow: 0 0 0 1px var(--ink) !important;
    }
    /* Slider: override Streamlit's default red accent with navy */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: var(--ink) !important;
        border-color: var(--ink) !important;
        box-shadow: none !important;
        transition: transform 0.15s ease;
    }
    div[data-testid="stSlider"] div[role="slider"]:hover,
    div[data-testid="stSlider"] div[role="slider"]:focus {
        transform: scale(1.15);
        box-shadow: 0 0 0 0.2rem rgba(22, 33, 62, 0.25) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
        background-color: var(--ink) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div {
        background-color: var(--gold-light) !important;
    }
    div[data-testid="stThumbValue"] {
        color: var(--ink) !important;
        font-weight: 600;
    }
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {
        color: var(--muted) !important;
    }

    /* Generic Streamlit red-accent focus rings (inputs/select/buttons) -> navy */
    *:focus {
        outline-color: var(--ink) !important;
    }
    div[data-baseweb="select"]:focus-within > div,
    div[data-baseweb="base-input"]:focus-within {
        border-color: var(--ink) !important;
        box-shadow: 0 0 0 1px var(--ink) !important;
    }
    label { color: var(--charcoal) !important; font-weight: 500 !important; }

    /* ---- Predict button: seal-like, small caps, deliberate ---- */
    div.stButton > button {
        background: var(--ink);
        color: var(--gold-light);
        font-weight: 600;
        font-size: 0.92rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.85rem 0;
        border-radius: 4px;
        border: 1px solid var(--gold);
        width: 100%;
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button:hover {
        background: var(--ink-light);
        border-color: var(--gold-light);
        color: #FFFFFF;
        box-shadow: 0 2px 10px rgba(22, 33, 62, 0.25);
    }

    /* ---- Summary strip (pre-submit recap) ---- */
    .summary-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 2.2rem;
        background: #FFFFFF;
        border: 1px solid var(--gold-light);
        border-left: 4px solid var(--gold);
        border-radius: 4px;
        padding: 1rem 1.4rem;
        margin-bottom: 1.4rem;
    }
    .summary-item .label {
        font-size: 0.68rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--muted);
        font-weight: 600;
    }
    .summary-item .value {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--ink);
    }

    /* ---- Result: certificate panel ---- */
    .cert-panel {
        background: #FFFFFF;
        border: 1px solid var(--gold-light);
        border-radius: 6px;
        padding: 2.2rem 2rem;
        margin-top: 1.6rem;
        text-align: center;
        position: relative;
    }
    .cert-panel::before, .cert-panel::after {
        content: "";
        position: absolute;
        left: 1.1rem; right: 1.1rem;
        height: 1px;
        background: var(--gold-light);
    }
    .cert-panel::before { top: 0.65rem; }
    .cert-panel::after { bottom: 0.65rem; }
    .cert-eyebrow {
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--muted);
        font-weight: 600;
        margin-bottom: 0.6rem;
    }
    .cert-grade {
        font-family: 'Playfair Display', serif;
        font-size: 4.2rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .cert-caption {
        font-size: 0.88rem;
        color: var(--muted);
    }

    /* ---- Data tables ---- */
    div[data-testid="stTable"] table, .stDataFrame {
        border: 1px solid var(--gold-light) !important;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "student_grade_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "preprocessor.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
FEATURES_PATH = BASE_DIR / "selected_features.pkl"


# ============================================================
# 4. LOAD MACHINE LEARNING COMPONENTS
# ============================================================

@st.cache_resource
def load_components():
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    scaler = joblib.load(SCALER_PATH)
    selected_features = joblib.load(FEATURES_PATH)
    return model, preprocessor, scaler, selected_features


try:
    model, preprocessor, scaler, selected_features = load_components()
except Exception as error:
    st.error("Unable to load the Machine Learning model files.")
    st.exception(error)
    st.stop()


# ============================================================
# 5. SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        "<div style='font-family:Playfair Display, serif; font-size:1.2rem; "
        "font-weight:700; color:#16213E;'>Record Notes</div>",
        unsafe_allow_html=True
    )
    st.write(
        "This tool estimates a student's **HSSC-II grade** from academic, "
        "attendance, and family-background records using a trained "
        "Random Forest model."
    )
    st.divider()
    st.markdown("**Grade scale**  \nA-ONE · A · B · C · D · Fail")
    st.divider()
    st.caption(
        "This is a decision-support estimate, not an official record or "
        "a substitute for teacher judgment."
    )


# ============================================================
# 6. LETTERHEAD
# ============================================================

st.markdown("""
<div class="letterhead">
    <div class="eyebrow">Academic Records &middot; Prediction Tool</div>
    <h1>🎓 Student Academic Success Predictor</h1>
    <p>Enter the student's academic, attendance, demographic, and educational
    background information to estimate the expected HSSC-II grade.</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 7. STUDENT INFORMATION
# ============================================================

st.markdown('<div class="section-eyebrow">Section I</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">👤 Student Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["Female", "Male"])
with col2:
    school_type = st.selectbox("School Type", ["Public", "Private"])


# ============================================================
# 8. ACADEMIC INFORMATION
# ============================================================

st.markdown('<div class="section-eyebrow">Section II</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">📚 Academic Information</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    ssc_i_marks = st.number_input("SSC-I Marks", min_value=0.0, max_value=1000.0, value=500.0, step=1.0)
with col2:
    ssc_ii_marks = st.number_input("SSC-II Marks", min_value=0.0, max_value=1000.0, value=500.0, step=1.0)
with col3:
    hssc_i_marks = st.number_input("HSSC-I Marks", min_value=0.0, max_value=1000.0, value=500.0, step=1.0)


# ============================================================
# 9. ATTENDANCE AND ACADEMIC HISTORY
# ============================================================

st.markdown('<div class="section-eyebrow">Section III</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">📊 Attendance &amp; Academic History</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    attendance_rate = st.slider("Attendance Rate (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
with col2:
    previous_failures = st.number_input("Previous Failures", min_value=0, max_value=10, value=0, step=1)


# ============================================================
# 10. FAMILY EDUCATIONAL BACKGROUND
# ============================================================

st.markdown('<div class="section-eyebrow">Section IV</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">🏫 Family Educational Background</div>', unsafe_allow_html=True)

parent_education = st.selectbox(
    "Parent Education Level",
    ["High School", "Bachelor", "Master", "Primary", "Other"]
)


# ============================================================
# 11. PRE-SUBMIT SUMMARY STRIP
# ============================================================

st.markdown('<div class="section-eyebrow">Review</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">📋 Student Information Summary</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="summary-strip">
    <div class="summary-item"><div class="label">Gender</div><div class="value">{gender}</div></div>
    <div class="summary-item"><div class="label">School Type</div><div class="value">{school_type}</div></div>
    <div class="summary-item"><div class="label">Attendance</div><div class="value">{attendance_rate:.0f}%</div></div>
    <div class="summary-item"><div class="label">Previous Failures</div><div class="value">{previous_failures}</div></div>
    <div class="summary-item"><div class="label">Parent Education</div><div class="value">{parent_education}</div></div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 12. PREDICTION
# ============================================================

predict_button = st.button("Predict Academic Grade")

# (color, caption) per grade — deliberately restrained: only
# pass/borderline/fail read as distinct colors, not one hue per grade.
GRADE_STYLES = {
    "A-ONE": ("#2F5233", "Outstanding performance"),
    "A":     ("#2F5233", "Strong performance"),
    "B":     ("#8A6D1F", "Solid, above-average performance"),
    "C":     ("#8A6D1F", "Average performance"),
    "D":     ("#8B2635", "Below-average — at risk"),
    "Fail":  ("#8B2635", "At risk — needs intervention"),
}

if predict_button:

    input_data = pd.DataFrame({
        "SSC_I_Marks": [ssc_i_marks],
        "Previous_Failures": [previous_failures],
        "Attendance_Rate": [attendance_rate],
        "Gender": [gender],
        "HSSC_I_Marks": [hssc_i_marks],
        "SSC_II_Marks": [ssc_ii_marks],
        "School_Type": [school_type],
        "Parent_Education_Level": [parent_education]
    })

    try:
        processed_data = preprocessor.transform(input_data)
        processed_data = pd.DataFrame(processed_data, columns=preprocessor.get_feature_names_out())
        processed_data = processed_data[selected_features]
        processed_data = scaler.transform(processed_data)

        prediction = model.predict(processed_data)[0]
        text_color, caption = GRADE_STYLES.get(prediction, ("#16213E", ""))

        # ---- Prediction Result ----
        st.markdown('<div class="section-eyebrow">Result</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🎯 Prediction Result</div>', unsafe_allow_html=True)
        st.markdown(
            f'''
            <div class="cert-panel">
                <div class="cert-eyebrow">Predicted HSSC-II Grade</div>
                <div class="cert-grade" style="color:{text_color};">{prediction}</div>
                <div class="cert-caption">{caption}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
        st.info(f"The Random Forest model predicts grade **{prediction}** for this student.")

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(processed_data)[0]
            classes = model.classes_
            proba_df = pd.DataFrame({"Grade": classes, "Probability (%)": (proba * 100).round(2)}).sort_values(
                "Probability (%)", ascending=False
            ).reset_index(drop=True)

            top_prob = proba_df.iloc[0]

            # ---- Prediction Confidence ----
            st.markdown('<div class="section-eyebrow">Model Certainty</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">📈 Prediction Confidence</div>', unsafe_allow_html=True)

            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown(
                    f'''<div class="summary-item">
                        <div class="label">Most Likely Grade</div>
                        <div class="value">{top_prob['Grade']}</div>
                    </div>
                    <div class="summary-item" style="margin-top:0.8rem;">
                        <div class="label">Probability</div>
                        <div class="value">{top_prob['Probability (%)']}%</div>
                    </div>''',
                    unsafe_allow_html=True
                )
            with c2:
                st.bar_chart(proba_df.set_index("Grade"), color="#16213E", height=260)

            # ---- Detailed Probability Table ----
            st.markdown('<div class="section-eyebrow">Breakdown</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">🔢 Detailed Probability</div>', unsafe_allow_html=True)
            st.dataframe(proba_df, use_container_width=True, hide_index=True)

        # ---- Input Data Used for Prediction ----
        st.markdown('<div class="section-eyebrow">Reference</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📄 Input Data Used for Prediction</div>', unsafe_allow_html=True)
        display_input = input_data.T.reset_index()
        display_input.columns = ["Field", "Value"]
        st.dataframe(display_input, use_container_width=True, hide_index=True)

    except Exception as error:
        st.error("An error occurred while processing the prediction.")
        st.exception(error)


# ============================================================
# 13. FOOTER
# ============================================================

st.write("")
st.markdown(
    "<hr style='border-color:#E8D5B7; margin-top:2rem;'>"
    "<div style='color:#6B6458; font-size:0.8rem; padding-top:0.4rem;'>"
    "Student Academic Success Prediction System &middot; Machine Learning Project"
    "</div>",
    unsafe_allow_html=True
)