import time
from fractions import Fraction
import io
import streamlit as st


import streamlit as st

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Al-Fara'id Islamic Inheritance Engine",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =====================================================================
# 1. PAGE CONFIGURATION (MUST BE THE FIRST STREAMLIT COMMAND)
# =====================================================================
st.set_page_config(
    page_title="Islamic Inheritance Calculator",
    page_icon="🕌",
    layout="wide"
)
# 2. HIDE DEVELOPER MENUS & GITHUB SOURCING
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stActionButtonIcon"] {visibility: hidden;}
    .viewerBadge_container__171of {display: none !important;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# 3. INITIALIZE COUNTERS AT ZERO
if "like_count" not in st.session_state:
    st.session_state.like_count = 0
if "love_count" not in st.session_state:
    st.session_state.love_count = 0
if "has_liked" not in st.session_state:
    st.session_state.has_liked = False
if "has_loved" not in st.session_state:
    st.session_state.has_loved = False
# --- 2. Constants and System Maps ---
ALLOWED_HEIRS = [
    "husband", "wife", "son", "daughter", "father", "mother",
    "son_of_son", "daughter_of_son", "grandfather",
    "maternal_grandmother", "paternal_grandmother", "full_brother", "full_sister",
    "paternal_brother", "paternal_sister", "maternal_brother", "maternal_sister",
    "son_of_full_brother", "son_of_paternal_brother", "full_paternal_uncle",
    "paternal_paternal_uncle", "son_of_full_paternal_uncle", "son_of_paternal_paternal_uncle"
]

LANG_MAP = {
    "en": {
        "title": "ISLAMIC INHERITANCE CALCULATOR",
        "estate": "Total Estate Assets Evaluation",
        "calc": "Calculate",
        "err": "Execution Error",
        "inv_amt": "Please provide a valid asset valuation amount greater than zero.",
        "sel_heir": "Select Active Surviving Heirs Below",
        "breakdown": "LEGAL INHERITANCE DISTRIBUTION LEDGER",
        "reset": "Reset System Parameters",
        "heir_header": "Heir Category & Count",
        "share_header": "Fractional Split",
        "pct_header": "Percentage",
        "basis_header": "Legal Basis / Fiqh Justification",
        "another": "← Calculate New Case",
        "download_pdf": "📥 Download Report",
        "case_summary": "💼 Case Summary Matrix",
        "husband": "Husband", "wife": "Wife", "son": "Son", "daughter": "Daughter", "father": "Father",
        "mother": "Mother",
        "son_of_son": "Son of Son", "daughter_of_son": "Daughter of Son", "grandfather": "Paternal Grandfather",
        "maternal_grandmother": "Maternal Grandmother", "paternal_grandmother": "Paternal Grandmother",
        "full_brother": "Full Brother", "full_sister": "Full Sister", "paternal_brother": "Paternal Brother",
        "paternal_sister": "Paternal Sister",
        "maternal_brother": "Maternal Brother (Utterine)", "maternal_sister": "Maternal Sister (Utterine)",
        "son_of_full_brother": "Son of Full Brother",
        "son_of_paternal_brother": "Son of Paternal Brother", "full_paternal_uncle": "Full Paternal Uncle",
        "paternal_paternal_uncle": "Paternal Paternal Uncle",
        "son_of_full_paternal_uncle": "Son of Full Paternal Uncle",
        "son_of_paternal_paternal_uncle": "Son of Paternal Paternal Uncle",
        "muan_tajhiz": "Funeral Expenses (مؤن التجهيز)",
        "huquq": "Debts & Liabilities (الديون والحقوق)",
        "wasiyyah": "Valid Bequests (الوصية)",
        "pre_dist_title": "⚖️ Pre-Distribution Liabilities / الحقوق المتعلقة بالتركة",
        "pre_dist_caption": "These obligations take legal precedence and must be deducted from the gross estate before distributing fixed shares.",
        "net_estate_msg": "Net Distributable Estate",
    },
    "ar": {
        "title": "حاسبة المواريث الإسلامية",
        "estate": "إجمالي قيمة التركة والأصول المادية:",
        "calc": "احسب",
        "inv_amt": "يرجى إدخال قيمة صحيحة للتركة أكبر من الصفر.",
        "sel_heir": "حدد الورثة المستحقين الحاليين أدناه",
        "breakdown": "دفتر توزيع المواريث الشرعي المعتمد",
        "reset": "إعادة ضبط معطيات النظام بالكامل",
        "heir_header": "الوارث وعدد المستحقين",
        "share_header": "الفرض المقدر",
        "pct_header": "النسبة المئوية",
        "basis_header": "السبب والتعليل الفقهي الشرعي",
        "another": "← حساب مسألة فقهية جديدة",
        "download_pdf": "📥 تحميل التقرير",
        "case_summary": "💼 ملخص المسألة المفتوحة",
        "husband": "الزوج", "wife": "الزوجة", "son": "الابن", "daughter": "البنت", "father": "الأب", "mother": "الأم",
        "son_of_son": "ابن الابن", "daughter_of_son": "بنت الابن", "grandfather": "الجد لأب",
        "maternal_grandmother": "الجدة لأم", "paternal_grandmother": "الجدة لأب",
        "full_brother": "الأخ الشقيق", "full_sister": "الأخت الشقيقة", "paternal_brother": "الأخ لأب",
        "paternal_sister": "الأخت لأب",
        "maternal_brother": "الأخ لأم", "maternal_sister": "الأخت لأم", "son_of_full_brother": "ابن الأخ الشقيق",
        "son_of_paternal_brother": "ابن الأخ لأب", "full_paternal_uncle": "العم الشقيق",
        "paternal_paternal_uncle": "العم لأب",
        "son_of_full_paternal_uncle": "ابن العم الشقيق", "son_of_paternal_paternal_uncle": "ابن العم لأب",
        "muan_tajhiz": "مؤن التجهيز",
        "huquq": "الديون والحقوق",
        "wasiyyah": "الوصية الشرعية",
        "pre_dist_title": "⚖️ الحقوق المتعلقة بالتركة",
        "pre_dist_caption": "تستقطع هذه الحقوق والواجبات من التركة أولاً قبل تقسيم السهام على الورثة.",
        "net_estate_msg": "صافي التركة القابلة للقسمة",
    }
}

التعليلات_والشروط = {
    "en": {
        "husband_half": "Husband receives 1/2 because there is a total absence of any surviving child or grandchild.",
        "husband_fourth": "Husband drops to 1/4 due to the presence of one or more surviving children or grandchildren.",
        "wife_fourth": "Wife/Wives receive 1/4 because there is a total absence of any surviving child or grandchild.",
        "wife_eighth": "Wife/Wives drop to 1/8 due to the presence of one or more surviving children or grandchildren.",
        "mother_third": "Mother receives 1/3 because there are no surviving children, no grandchildren, and no multiple siblings.",
        "mother_sixth": "Mother drops to 1/6 due to the presence of surviving children, grandchildren, or multiple siblings.",
        "father_sixth": "Father receives a fixed 1/6 share due to the presence of a surviving male descending child.",
        "father_mix": "Father receives a fixed 1/6 share plus the remainder as a residuary due to the presence of female descending children only.",
        "father_res": "Father takes the remaining assets as a residuary ('Asabah) because there are no descending children.",
        "grandfather_sixth": "Paternal Grandfather receives 1/6 in the absence of the father and presence of male descendants.",
        "grandfather_mix": "Paternal Grandfather receives 1/6 plus the remainder as a residuary in the absence of the father and presence of female descendants.",
        "grandfather_res": "Paternal Grandfather takes the remaining assets as a residuary in the absence of the father and descending children.",
        "son_asabah": "Son(s) inherit as core residuaries ('Asabah), taking remaining assets in a 2:1 ratio over daughters.",
        "daughter_half": "Daughter receives 1/2 as she is an only child with no surviving brothers.",
        "daughter_two_thirds": "Daughters receive 2/3 shared equally because there are multiple daughters and no surviving brothers.",
        "daughter_asabah": "Daughter inherits as a residuary alongside her brother(s) ('Asabah bi-ghayriha) in a 2:1 male-to-female ratio.",
        "son_of_son_asabah": "Son of son inherits as a residuary in the absence of higher male descendants.",
        "daughter_of_son_half": "Daughter of son receives 1/2 as she is an only grandchild with no making-reductive conditions.",
        "daughter_of_son_two_thirds": "Daughters of son receive 2/3 shared equally in the absence of higher descendants.",
        "daughter_of_son_sixth": "Daughter of son receives 1/6 to complete the 2/3 allocation for daughters alongside a single higher daughter.",
        "daughter_of_son_asabah": "Daughter of son inherits as a residuary alongside her male equivalent counter-part.",
        "maternal_grandmother_sixth": "Maternal Grandmother receives 1/6 in the absence of the mother.",
        "paternal_grandmother_sixth": "Paternal Grandmother receives 1/6 in the absence of the mother and father (shared if both grandmothers exist).",
        "uterine_siblings_sixth": "Uterine sibling receives 1/6 as an isolated individual with no blocking ascendants or descendants.",
        "uterine_siblings_third": "Uterine siblings receive 1/3 split equally between sexes because they are multiple.",
        "full_brother_asabah": "Full Brother inherits as a residuary ('Asabah) taking remaining assets.",
        "full_sister_half": "Full Sister receives 1/2 as she is isolated with no blocking or compounding factors.",
        "full_sister_two_thirds": "Full Sisters receive 2/3 shared equally because they are multiple.",
        "full_sister_asabah_bi": "Full Sister inherits as a residuary alongside her brother(s) ('Asabah bi-ghayriha).",
        "full_sister_asabah_ma": "Full Sister inherits as a residuary alongside daughters/granddaughters ('Asabah ma'a ghayriha).",
        "paternal_brother_asabah": "Paternal Brother inherits as a residuary ('Asabah) in the absence of full brothers.",
        "paternal_sister_half": "Paternal Sister receives 1/2 as she is isolated with no higher siblings.",
        "paternal_sister_two_thirds": "Paternal Sisters receive 2/3 shared equally.",
        "paternal_sister_sixth": "Paternal Sister receives 1/6 to complete the 2/3 allocation alongside a single full sister.",
        "paternal_sister_asabah_bi": "Paternal Sister inherits as a residuary alongside paternal brothers.",
        "paternal_sister_asabah_ma": "Paternal Sister inherits as a residuary alongside daughters/granddaughters in the absence of full siblings.",
        "other_asabah": "Inherits remaining assets by order of agnatic proximity ('Asabah).",
        "umariyyah_mother": "Gharawain Case: Mother receives 1/3 of the residue after the spouse's share is deducted.",
        "umariyyah_father": "Gharawain Case: Father takes the remaining residue after the spouse and mother shares.",
        "default": "Inherits standard assignment dictated by the rules of Al-Fara'id."
    },
    "ar": {
        "husband_half": "الزوج يستحق النصف فرضاً لعدم وجود فرع وارث للميت مطلقاً.",
        "husband_fourth": "الزوج ينزل من النصف إلى الربع فرضاً لوجود الفرع الوارث للميت.",
        "wife_fourth": "الزوجة/الزوجات يستحققن الربع فرضاً لعدم وجود فرع وارث للميت مطلقاً.",
        "wife_eighth": "الزوجة/الزوجات ينزلن إلى الثمن فرضاً لوجود الفرع الوارث للميت.",
        "mother_third": "الأم تستحق الثلث فرضاً لعدم وجود فرع وارث ولعدم وجود جمع من الإخوة.",
        "mother_sixth": "الأم تنزل إلى السدس فرضاً لوجود الفرع الوارث أو وجود جمع من الإخوة والأخوات.",
        "father_sixth": "الأب يستحق السدس فرضاً لوجود الفرع الوارث المذكر (الابن أو ابن الابن).",
        "father_mix": "الأب يستحق السدس فرضاً بالإضافة إلى الباقي تعصيباً لوجود فرع وارث مؤنث فقط.",
        "father_res": "الأب يرث بالتعصيب المحض ويأخذ الباقي لعدم وجود فرع وارث للميت.",
        "grandfather_sixth": "الجد لأب يستحق السدس فرضاً عند عدم وجود الأب ووجود فرع وارث مذكر.",
        "grandfather_mix": "الجد لأب يستحق السدس فرضاً والباقي تعصيباً عند عدم وجود الأب ووجود فرع مؤنث فقط.",
        "grandfather_res": "الجد لأب يأخذ الباقي تعصيباً عند عدم وجود الأب والفرع الوارث مطلقاً.",
        "son_asabah": "الابن يرث بالتعصيب كعصبة بالنفس ويأخذ باقي التركة بالكامل بعد الفروض (للذكر مثل حظ الأنثيين).",
        "daughter_half": "البنت تستحق النصف فرضاً لانفرادها عن المعصب والمشارك.",
        "daughter_two_thirds": "البنات يستحققن الثلثين فرضاً للتعدد ولعدم وجود معصب لهن.",
        "daughter_asabah": "البنت ترث بالتعصيب بالغير مع شقيقها، للذكر مثل حظ الأنثيين.",
        "son_of_son_asabah": "ابن الابن يأخذ الباقي تعصيباً عند عدم وجود ابن صلبي أعلى منه.",
        "daughter_of_son_half": "بنت الابن تستحق النصف فرضاً لانفرادها وعدم وجود فرع أعلى أو معصب.",
        "daughter_of_son_two_thirds": "بنات الابن يستحققن الثلثين فرضاً للتعدد وعدم وجود فرع أعلى أو معصب.",
        "daughter_of_son_sixth": "بنت الابن تأخذ السدس فرضاً تكملة للثلثين مع وجود بنت صلبية واحدة أعلى منها.",
        "daughter_of_son_asabah": "بنت الابن ترث بالتعصيب بالغير مع ابن الابن المساوي لها أو الأقل منها إن احتاجت إليه.",
        "maternal_grandmother_sixth": "الجدة لأم تستحق السدس فرضاً لعدم وجود الأم.",
        "paternal_grandmother_sixth": "الجدة لأب تستحق السدس فرضاً لعدم وجود الأم والأب (ويشتركن فيه إن وجدتا معاً).",
        "uterine_siblings_sixth": "الأخ أو الأخت لأم يستحق السدس فرضاً عند الانفراد وعدم وجود الأصل المذكر أو الفرع الوارث.",
        "uterine_siblings_third": "الإخوة لأم يستحقون الثلث فرضاً عند التعدد ويقسم بينهم بالتساوي دون تفضيل للذكر.",
        "full_brother_asabah": "الأخ الشقيق يرث بالتعصيب بالنفس كأقوى العصبات بعد الأبوة والبنوة.",
        "full_sister_half": "الأخت الشقيقة تستحق النصف فرضاً لانفرادها وعدم وجود حاجب أو معصب.",
        "full_sister_two_thirds": "الأخوات الشقيقات يستحققن الثلثين فرضاً عند التعدد وعدم وجود حاجب أو معصب.",
        "full_sister_asabah_bi": "الأخت الشقيقة ترث بالتعصيب بالغير مع الأخ الشقيق (للذكر مثل حظ الأنثيين).",
        "full_sister_asabah_ma": "الأخت الشقيقة ترث عصبة مع الغير مع البنات أو بنات الابن لقوله ﷺ 'اجعلوا الأخوات مع البنات عصبة'.",
        "paternal_brother_asabah": "الأخ لأب يرث بالتعصيب بالنفس عند عدم وجود الأخ الشقيق أو العصبة الأعلى.",
        "paternal_sister_half": "الأخت لأب تستحق النصف فرضاً لانفرادها وعدم وجود شقيق أو شقيقة أو حاجب.",
        "paternal_sister_two_thirds": "الأخوات لأب يستحققن الثلثين فرضاً عند التعدد.",
        "paternal_sister_sixth": "الأخت لأب تأخذ السدس فرضاً تكملة للثلثين مع وجود أخت شقيقة واحدة صلبة.",
        "paternal_sister_asabah_bi": "الأخت لأب ترث بالتعصيب بالغير مع الأخ لأب.",
        "paternal_sister_asabah_ma": "الأخت لأب ترث عصبة مع الغير مع البنات عند عدم وجود الإخوة الأشقاء.",
        "other_asabah": "يستحق الباقي تعصيباً بجهة القرابة والعصوبة الإيجابية وفق ترتيب جهات العصمة.",
        "umariyyah_mother": "المسألة الغراوية: ترث الأم ثلث الباقي بعد فرض الزوج أو الزوجة حتى لا تتعدى نصيب الأب.",
        "umariyyah_father": "المسألة الغراوية: يأخذ الأب الباقي تعصيباً بعد فرض الزوج ونصيب الأم.",
        "default": "يستحق النصيب المقدر له شرعاً بموجب قواعد وأحكام الإرث والتعصيب الفقهية."
    }
}

# --- 3. Session States Initialization ---
if "initial_splash_loaded" not in st.session_state:
    st.session_state.initial_splash_loaded = False
if "calc_splash_trigger" not in st.session_state:
    st.session_state.calc_splash_trigger = False
if "page_view" not in st.session_state:
    st.session_state.page_view = "input"
if "heirs_state" not in st.session_state:
    st.session_state.heirs_state = {n: 0 for n in ALLOWED_HEIRS}

# --- 4. Splashes and Loading Screens ---
if not st.session_state.initial_splash_loaded:
    st.markdown("""
        <style>
        [data-testid="stHeader"], footer {visibility: hidden;}
        .block-container {padding: 0rem; max-width: 100%;}
        .splash-canvas {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #0A1410; display: flex; flex-direction: column;
            justify-content: center; align-items: center; z-index: 999999;
        }
        .ring-wrapper {
            position: relative; width: 140px; height: 140px; margin-bottom: 20px;
            display: flex; justify-content: center; align-items: center;
        }
        .progress-ring-circle {
            stroke: #40916C; stroke-dasharray: 301.6; stroke-dashoffset: 301.6;
            animation: fillProgress 3s linear forwards;
            transform: rotate(-90deg); transform-origin: 50% 50%; stroke-linecap: round;
        }
        @keyframes fillProgress { to { stroke-dashoffset: 0; } }
        .brand-diamond { position: absolute; width: 24px; height: 24px; background-color: #40916C; transform: rotate(45deg); }
        .splash-title { color: #FFFFFF; font-size: 26px; font-weight: 700; letter-spacing: 5px; margin: 5px 0; font-family: 'Inter', sans-serif; }
        .splash-subtitle { color: #94A3B8; font-size: 11px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; font-family: 'Inter', sans-serif; }
        </style>
        <div class="splash-canvas">
            <div class="ring-wrapper">
                <svg width="110" height="110">
                    <circle cx="55" cy="55" r="48" stroke="#10251C" stroke-width="5" fill="transparent" />
                    <circle class="progress-ring-circle" cx="55" cy="55" r="48" stroke-width="5" fill="transparent" />
                </svg>
                <div class="brand-diamond"></div>
            </div>
            <div class="splash-title">AL-FARA'ID</div>
            <div class="splash-subtitle">Secure • Instant • Fiqh Engine</div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3.0)
    st.session_state.initial_splash_loaded = True
    st.rerun()

if st.session_state.calc_splash_trigger:
    st.markdown("""
        <style>
        [data-testid="stHeader"], footer {visibility: hidden;}
        .block-container {padding: 0rem; max-width: 100%;}
        .splash-canvas {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #0A0D14; display: flex; flex-direction: column;
            justify-content: center; align-items: center; z-index: 999999;
        }
        .ring-wrapper {
            position: relative; width: 140px; height: 140px; margin-bottom: 20px;
            display: flex; justify-content: center; align-items: center;
        }
        .progress-ring-circle {
            stroke: #52B788; stroke-dasharray: 301.6; stroke-dashoffset: 301.6;
            animation: fillProgress 2s linear forwards;
            transform: rotate(-90deg); transform-origin: 50% 50%; stroke-linecap: round;
        }
        @keyframes fillProgress { to { stroke-dashoffset: 0; } }
        .brand-diamond { position: absolute; width: 24px; height: 24px; background-color: #52B788; transform: rotate(45deg); }
        .splash-title { color: #FFFFFF; font-size: 24px; font-weight: 700; letter-spacing: 4px; margin: 8px 0; font-family: 'Inter', sans-serif; }
        .splash-subtitle { color: #A3B19B; font-size: 11px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; font-family: 'Inter', sans-serif; }
        </style>
        <div class="splash-canvas">
            <div class="ring-wrapper">
                <svg width="110" height="110">
                    <circle cx="55" cy="55" r="48" stroke="#1A221E" stroke-width="5" fill="transparent" />
                    <circle class="progress-ring-circle" cx="55" cy="55" r="48" stroke-width="5" fill="transparent" />
                </svg>
                <div class="brand-diamond"></div>
            </div>
            <div class="splash-title">RUNNING MATRIX CALCULATIONS</div>
            <div class="splash-subtitle">Applying Asabah & Fard Rules...</div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2.0)
    st.session_state.calc_splash_trigger = False
    st.session_state.page_view = "result"
    st.rerun()

# --- 5. Custom Visual Typography UI Styles ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Inter:wght@400;500;600;700&display=swap');
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
            background-color: #0B0E14; color: #F3F4F6;
        }
        .hero-banner {
            background: linear-gradient(135deg, #0F2E22 0%, #061810 100%);
            padding: 2.5rem; border-radius: 16px; border: 1px solid #1B4D3E; text-align: center; margin-bottom: 2.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }
        .hero-title-ar { font-family: 'Amiri', serif; font-size: 3rem; color: #52B788; margin:0; line-height: 1.2; }
        .hero-title-en { font-size: 1.2rem; font-weight: 600; letter-spacing: 3px; color: #D1D5DB; margin-top:12px; }
        .grid-header { background-color: #121815; border-radius: 8px; padding: 14px; font-weight:600; border:1px solid #22332A; margin-bottom:12px; text-align: center; color: #52B788;}
        .result-row { background-color: #131722; border: 1px solid #22293A; border-radius: 12px; padding: 20px; margin-bottom: 14px; min-height: 95px;}
        .card-container { background-color: #141923; border: 1px solid #232D42; border-radius: 14px; padding: 24px; margin-bottom: 2rem; }
        .heir-entry-box { background-color: #11151E; border: 1px solid #1E2638; border-radius: 10px; padding: 12px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; }
    </style>
""", unsafe_allow_html=True)

# RTL/LTR Handling
lang_code = "en"
sel_c1, sel_c2 = st.columns([5, 1])
with sel_c2:
    lang_sel = st.selectbox("Language / اللغة", ["English", "العربية"], label_visibility="collapsed")
    lang_code = "ar" if lang_sel == "العربية" else "en"
    m = LANG_MAP[lang_code]

if lang_code == "ar":
    st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { direction: rtl; text-align: right; }</style>",
                unsafe_allow_html=True)
else:
    st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { direction: ltr; text-align: left; }</style>",
                unsafe_allow_html=True)


# --- 6. Verified Fiqh Mathematical Inference Engine ---
class Heir:
    def __init__(self, name, count=1):
        self.name = name
        self.count = count
        self.fractional_share = Fraction(0, 1)
        self.individual_cash = 0.0
        self.justification_key = ""


class InheritanceEngine:
    def __init__(self, total, heir_counts):
        self.total = total
        self.raw_counts = heir_counts
        self.h = {}
        self.case_meta = {"gharawain": False}

    def calculate(self):
        # Local counts dictionary matching working state
        hc = {k: v for k, v in self.raw_counts.items() if v > 0}

        # 1. SPECIAL CASE METRICS: Gharawain (Umariyyah Check)
        if set(hc.keys()) == {"husband", "mother", "father"} and hc["husband"] == 1:
            self.h = {k: Heir(k, 1) for k in hc.keys()}
            self.h["husband"].fractional_share = Fraction(1, 2)
            self.h["mother"].fractional_share = Fraction(1, 6)  # 1/3 of remainder (1/2)
            self.h["father"].fractional_share = Fraction(1, 3)  # Asabah remainder
            self.h["husband"].justification_key = "husband_half"
            self.h["mother"].justification_key = "umariyyah_mother"
            self.h["father"].justification_key = "umariyyah_father"
            self.case_meta["gharawain"] = True
            return self._finalize()

        if set(hc.keys()) == {"wife", "mother", "father"}:
            self.h = {k: Heir(k, hc[k]) for k in hc.keys()}
            self.h["wife"].fractional_share = Fraction(1, 4)
            self.h["mother"].fractional_share = Fraction(1, 4)  # 1/3 of remainder (3/4)
            self.h["father"].fractional_share = Fraction(1, 2)  # Asabah remainder
            self.h["wife"].justification_key = "wife_fourth"
            self.h["mother"].justification_key = "umariyyah_mother"
            self.h["father"].justification_key = "umariyyah_father"
            self.case_meta["gharawain"] = True
            return self._finalize()

        # 2. FIQH TOTAL EXCLUSION RULES (HAJB AL-HIRMAN)
        # Descendant exclusions
        if hc.get("son", 0) > 0:
            hc.pop("son_of_son", None)
            hc.pop("daughter_of_son", None)
        if hc.get("son_of_son", 0) > 0 and hc.get("son", 0) == 0:
            # lower descendants omitted for engine scope
            pass

        # Ascendant exclusions
        if hc.get("father", 0) > 0:
            hc.pop("grandfather", None)
            hc.pop("paternal_grandmother", None)
        if hc.get("mother", 0) > 0:
            hc.pop("maternal_grandmother", None)
            hc.pop("paternal_grandmother", None)

        # Siblings and Collateral exclusions
        has_male_desc = (hc.get("son", 0) > 0 or hc.get("son_of_son", 0) > 0)
        has_female_desc = (hc.get("daughter", 0) > 0 or hc.get("daughter_of_son", 0) > 0)
        has_any_desc = has_male_desc or has_female_desc
        has_male_asc = (hc.get("father", 0) > 0 or hc.get("grandfather", 0) > 0)

        # Uterine Siblings are blocked by any descendent or male ascendant
        if has_any_desc or has_male_asc:
            hc.pop("maternal_brother", None)
            hc.pop("maternal_sister", None)

        # Full Siblings are completely blocked by Father, Son, or Son of Son
        if hc.get("father", 0) > 0 or has_male_desc:
            hc.pop("full_brother", None)
            hc.pop("full_sister", None)

        # Paternal Siblings are blocked by Father, Son, Son of Son, Full Brother
        # Paternal Sister is also blocked by multiple Full Sisters unless there is a Paternal Brother
        if hc.get("father", 0) > 0 or has_male_desc or hc.get("full_brother", 0) > 0:
            hc.pop("paternal_brother", None)
            hc.pop("paternal_sister", None)
        if hc.get("full_sister", 0) >= 2 and hc.get("paternal_brother", 0) == 0:
            hc.pop("paternal_sister", None)

        # Distant collaterals (nephews, uncles) blocked by any male sibling/father/son
        block_distant = (hc.get("father", 0) > 0 or has_male_desc or
                         hc.get("full_brother", 0) > 0 or hc.get("paternal_brother", 0) > 0 or
                         hc.get("grandfather", 0) > 0 or
                         (hc.get("full_sister", 0) > 0 and has_female_desc) or
                         (hc.get("paternal_sister", 0) > 0 and has_female_desc))

        if block_distant:
            for k in ["son_of_full_brother", "son_of_paternal_brother", "full_paternal_uncle",
                      "paternal_paternal_uncle", "son_of_full_paternal_uncle", "son_of_paternal_paternal_uncle"]:
                hc.pop(k, None)

        # Reinitialize active working map
        self.h = {k: Heir(k, hc[k]) for k in hc.keys()}

        # 3. FIXED FRACTION ASSIGNMENTS (FARD)
        # Spouses
        if "husband" in self.h:
            self.h["husband"].fractional_share = Fraction(1, 4) if has_any_desc else Fraction(1, 2)
            self.h["husband"].justification_key = "husband_fourth" if has_any_desc else "husband_half"
        if "wife" in self.h:
            self.h["wife"].fractional_share = Fraction(1, 8) if has_any_desc else Fraction(1, 4)
            self.h["wife"].justification_key = "wife_eighth" if has_any_desc else "wife_fourth"

        # Mother
        total_siblings = sum(self.h[k].count for k in ["full_brother", "full_sister", "paternal_brother",
                                                       "paternal_sister", "maternal_brother", "maternal_sister"] if
                             k in self.h)
        if "mother" in self.h:
            cond_mother = has_any_desc or total_siblings >= 2
            self.h["mother"].fractional_share = Fraction(1, 6) if cond_mother else Fraction(1, 3)
            self.h["mother"].justification_key = "mother_sixth" if cond_mother else "mother_third"

        # Grandmothers
        if "maternal_grandmother" in self.h:
            self.h["maternal_grandmother"].fractional_share = Fraction(1, 6)
            self.h["maternal_grandmother"].justification_key = "maternal_grandmother_sixth"
        if "paternal_grandmother" in self.h:
            self.h["paternal_grandmother"].fractional_share = Fraction(1, 6)
            self.h["paternal_grandmother"].justification_key = "paternal_grandmother_sixth"
        if "maternal_grandmother" in self.h and "paternal_grandmother" in self.h:
            self.h["maternal_grandmother"].fractional_share = Fraction(1, 12)
            self.h["paternal_grandmother"].fractional_share = Fraction(1, 12)

        # Father & Paternal Grandfather Fard Base
        if "father" in self.h and has_male_desc:
            self.h["father"].fractional_share = Fraction(1, 6)
            self.h["father"].justification_key = "father_sixth"
        elif "father" in self.h and has_female_desc:
            self.h["father"].fractional_share = Fraction(1, 6)
            self.h["father"].justification_key = "father_mix"

        if "grandfather" in self.h and "father" not in self.h:
            if has_male_desc:
                self.h["grandfather"].fractional_share = Fraction(1, 6)
                self.h["grandfather"].justification_key = "grandfather_sixth"
            elif has_female_desc:
                self.h["grandfather"].fractional_share = Fraction(1, 6)
                self.h["grandfather"].justification_key = "grandfather_mix"

        # Daughters & Granddaughters
        if "daughter" in self.h and "son" not in self.h:
            self.h["daughter"].fractional_share = Fraction(1, 2) if self.h["daughter"].count == 1 else Fraction(2, 3)
            self.h["daughter"].justification_key = "daughter_half" if self.h[
                                                                          "daughter"].count == 1 else "daughter_two_thirds"

        if "daughter_of_son" in self.h and "son" not in self.h and "son_of_son" not in self.h:
            if "daughter" not in self.h:
                self.h["daughter_of_son"].fractional_share = Fraction(1, 2) if self.h[
                                                                                   "daughter_of_son"].count == 1 else Fraction(
                    2, 3)
                self.h["daughter_of_son"].justification_key = "daughter_of_son_half" if self.h[
                                                                                            "daughter_of_son"].count == 1 else "daughter_of_son_two_thirds"
            elif self.h["daughter"].count == 1:
                self.h["daughter_of_son"].fractional_share = Fraction(1, 6)  # Takmilat al-Thuluthayn
                self.h["daughter_of_son"].justification_key = "daughter_of_son_sixth"

        # Uterine Siblings
        ut_count = self.h.get("maternal_brother", Heir("x", 0)).count + self.h.get("maternal_sister",
                                                                                   Heir("x", 0)).count
        if ut_count > 0:
            share_per_ut = Fraction(1, 6) if ut_count == 1 else Fraction(1, 3) / ut_count
            key_ut = "uterine_siblings_sixth" if ut_count == 1 else "uterine_siblings_third"
            if "maternal_brother" in self.h:
                self.h["maternal_brother"].fractional_share = share_per_ut * self.h["maternal_brother"].count
                self.h["maternal_brother"].justification_key = key_ut
            if "maternal_sister" in self.h:
                self.h["maternal_sister"].fractional_share = share_per_ut * self.h["maternal_sister"].count
                self.h["maternal_sister"].justification_key = key_ut

        # Female Collaterals (Sisters)
        if "full_sister" in self.h and "full_brother" not in self.h and not has_male_desc and hc.get("father", 0) == 0:
            if not has_female_desc:
                self.h["full_sister"].fractional_share = Fraction(1, 2) if self.h[
                                                                               "full_sister"].count == 1 else Fraction(
                    2, 3)
                self.h["full_sister"].justification_key = "full_sister_half" if self.h[
                                                                                    "full_sister"].count == 1 else "full_sister_two_thirds"
            else:
                # Asabah Ma'a Ghayriha (Will be calculated below via residue)
                pass

        if "paternal_sister" in self.h and "paternal_brother" not in self.h and "full_brother" not in self.h and not has_male_desc and hc.get(
                "father", 0) == 0:
            if not has_female_desc:
                if "full_sister" not in self.h:
                    self.h["paternal_sister"].fractional_share = Fraction(1, 2) if self.h[
                                                                                       "paternal_sister"].count == 1 else Fraction(
                        2, 3)
                    self.h["paternal_sister"].justification_key = "paternal_sister_half" if self.h[
                                                                                                "paternal_sister"].count == 1 else "paternal_sister_two_thirds"
                elif self.h["full_sister"].count == 1:
                    self.h["paternal_sister"].fractional_share = Fraction(1, 6)
                    self.h["paternal_sister"].justification_key = "paternal_sister_sixth"

        # 4. RESIDUARY INFERENCE CALCULATIONS ('ASABAH)
        allocated_fard = sum(x.fractional_share for x in self.h.values())
        remainder = Fraction(1, 1) - allocated_fard

        if remainder > 0:
            # Class A: Direct Agnatic Descendants (Son & Daughter combo)
            if "son" in self.h:
                total_parts = (self.h["son"].count * 2) + self.h.get("daughter", Heir("d", 0)).count
                self.h["son"].fractional_share += remainder * Fraction(self.h["son"].count * 2, total_parts)
                self.h["son"].justification_key = "son_asabah"
                if "daughter" in self.h:
                    self.h["daughter"].fractional_share += remainder * Fraction(self.h["daughter"].count, total_parts)
                    self.h["daughter"].justification_key = "daughter_asabah"
                remainder = Fraction(0, 1)

            # Class B: Grandchildren combo
            elif "son_of_son" in self.h:
                total_parts = (self.h["son_of_son"].count * 2) + self.h.get("daughter_of_son", Heir("d", 0)).count
                self.h["son_of_son"].fractional_share += remainder * Fraction(self.h["son_of_son"].count * 2,
                                                                              total_parts)
                self.h["son_of_son"].justification_key = "son_of_son_asabah"
                if "daughter_of_son" in self.h:
                    self.h["daughter_of_son"].fractional_share += remainder * Fraction(self.h["daughter_of_son"].count,
                                                                                       total_parts)
                    self.h["daughter_of_son"].justification_key = "daughter_of_son_asabah"
                remainder = Fraction(0, 1)

            # Class C: Fathers / Grandfathers taking remaining
            elif "father" in self.h and not has_male_desc:
                self.h["father"].fractional_share += remainder
                self.h["father"].justification_key = "father_res"
                remainder = Fraction(0, 1)
            elif "grandfather" in self.h and "father" not in self.h and not has_male_desc:
                self.h["grandfather"].fractional_share += remainder
                self.h["grandfather"].justification_key = "grandfather_res"
                remainder = Fraction(0, 1)

            # Class D: Full Siblings / Asabah with Daughters
            elif "full_brother" in self.h or (
                    "full_sister" in self.h and (has_female_desc or "full_brother" in self.h)):
                if "full_brother" in self.h:
                    total_parts = (self.h["full_brother"].count * 2) + self.h.get("full_sister", Heir("s", 0)).count
                    self.h["full_brother"].fractional_share += remainder * Fraction(self.h["full_brother"].count * 2,
                                                                                    total_parts)
                    self.h["full_brother"].justification_key = "full_brother_asabah"
                    if "full_sister" in self.h:
                        self.h["full_sister"].fractional_share += remainder * Fraction(self.h["full_sister"].count,
                                                                                       total_parts)
                        self.h["full_sister"].justification_key = "full_sister_asabah_bi"
                else:
                    # Asabah Ma'a Ghayriha with daughters
                    self.h["full_sister"].fractional_share += remainder
                    self.h["full_sister"].justification_key = "full_sister_asabah_ma"
                remainder = Fraction(0, 1)

            # Class E: Paternal Siblings
            elif "paternal_brother" in self.h or (
                    "paternal_sister" in self.h and (has_female_desc or "paternal_brother" in self.h)):
                if "paternal_brother" in self.h:
                    total_parts = (self.h["paternal_brother"].count * 2) + self.h.get("paternal_sister",
                                                                                      Heir("s", 0)).count
                    self.h["paternal_brother"].fractional_share += remainder * Fraction(
                        self.h["paternal_brother"].count * 2, total_parts)
                    self.h["paternal_brother"].justification_key = "paternal_brother_asabah"
                    if "paternal_sister" in self.h:
                        self.h["paternal_sister"].fractional_share += remainder * Fraction(
                            self.h["paternal_sister"].count, total_parts)
                        self.h["paternal_sister"].justification_key = "paternal_sister_asabah_bi"
                else:
                    self.h["paternal_sister"].fractional_share += remainder
                    self.h["paternal_sister"].justification_key = "paternal_sister_asabah_ma"
                remainder = Fraction(0, 1)

            # Class F: Cascading remaining agnates (Uncles/Nephews)
            else:
                for k in ["son_of_full_brother", "son_of_paternal_brother", "full_paternal_uncle",
                          "paternal_paternal_uncle", "son_of_full_paternal_uncle", "son_of_paternal_paternal_uncle"]:
                    if k in self.h:
                        self.h[k].fractional_share += remainder
                        self.h[k].justification_key = "other_asabah"
                        remainder = Fraction(0, 1)
                        break

        # 5. ANOMALY ADAPTATION MATRIX: AUL & RAD (عول ورد)
        total_shares = sum(x.fractional_share for x in self.h.values())

        # Aul (Proportional reduction for crowded Fard shares over 1.0)
        if total_shares > 1:
            for x in self.h.values():
                x.fractional_share /= total_shares

        # Rad (Return of excess back to Fard heirs excluding Spouses)
        elif total_shares < 1:
            rad_heirs = [x for k, x in self.h.items() if k not in ["husband", "wife"] and x.fractional_share > 0]
            if rad_heirs:
                rad_base = sum(x.fractional_share for x in rad_heirs)
                surplus = Fraction(1, 1) - total_shares
                for x in rad_heirs:
                    x.fractional_share += surplus * (x.fractional_share / rad_base)

        return self._finalize()

    def _finalize(self):
        for x in self.h.values():
            x.individual_cash = (float(x.fractional_share) * self.total) / x.count
            if not x.justification_key:
                x.justification_key = "default"
        return self.h


def generate_pdf_report(engine, total_amount, currency_symbol, lang):
    buffer = io.BytesIO()
    lines = []
    lines.append("=" * 60)
    lines.append("                AL-FARA'ID ISLAMIC INHERITANCE REPORT")
    lines.append("=" * 60)
    lines.append(f"Total Estate Assets Valuation: {currency_symbol} {total_amount:,.2f}")
    lines.append("-" * 60)
    lines.append(f"{'Heir Category (Count)':<30} | {'Share':<8} | {'Percentage':<10} | {'Cash Allocation':<15}")
    lines.append("-" * 60)

    for k, h in engine.h.items():
        heir_label = LANG_MAP[lang].get(k, k)
        pct = float(h.fractional_share) * 100
        line_item = f"{heir_label + ' (x' + str(h.count) + ')':<30} | {str(h.fractional_share):<8} | {pct:.2f}% {' ':<6} | {currency_symbol} {h.individual_cash:,.2f}"
        lines.append(line_item)
        basis_txt = التعليلات_والشروط[lang].get(h.justification_key, التعليلات_والشروط[lang]["default"])
        lines.append(f"   ↳ Fiqh Basis: {basis_txt}")
        lines.append("-" * 50)

    lines.append("=" * 60)
    final_text = "\n".join(lines)
    buffer.write(final_text.encode("utf-8"))
    buffer.seek(0)
    return buffer


# --- 7. Application Control Layout Router ---
if st.session_state.page_view == "input":
    st.markdown(
        f'<div class="hero-banner"><div class="hero-title-ar">المواريث والفرائض</div><div class="hero-title-en">{m["title"]}</div></div>',
        unsafe_allow_html=True)

   with st.container():
        st.markdown(f'<div class="card-container">', unsafe_allow_html=True)
        st.subheader(m["estate"])
        
        # Financial Input Base Split
        fin_c1, fin_c2 = st.columns([1, 4])
        with fin_c1:
            currency = st.selectbox("Currency", ["₦ NGN", "$ USD", "€ EUR", "£ GBP", "SR SAR", "د.إ AED"],
                                    label_visibility="collapsed")
        with fin_c2:
            gross_estate = st.number_input("Gross Valuation Amount", min_value=0.0, step=100.0, value=0.0,
                                         label_visibility="collapsed")
            
        st.write("---")
        st.markdown("#### ⚖️ Pre-Distribution Liabilities / الحقوق المتعلقة بالتركة")
        st.caption("These obligations take legal precedence and must be deducted from the gross estate before distributing fixed shares.")
        
        # Three clean columns for the legal deductions
        ded_c1, ded_c2, ded_c3 = st.columns(3)
        
        with ded_c1:
            tajhiz = st.number_input("Funeral Expenses (مؤن التجهيز)", min_value=0.0, step=50.0, value=0.0)
        with ded_c2:
            debts = st.number_input("Debts & Liabilities (الديون والحقوق)", min_value=0.0, step=50.0, value=0.0)
        with ded_c3:
            wasiyyah_input = st.number_input("Valid Bequests (الوصية)", min_value=0.0, step=50.0, value=0.0)
            
        # Calculate Remaining Net Estate
        pre_wasiyyah_estate = max(0.0, gross_estate - (tajhiz + debts))
        max_wasiyyah_allowed = pre_wasiyyah_estate / 3.0
        
        # Enforce the strict Shariah 1/3 limits on Wasiyyah
        if wasiyyah_input > max_wasiyyah_allowed:
            st.warning(f"⚠️ Wasiyyah exceeds the legal 1/3 limit! Capped at: {currency.split()[-1]} {max_wasiyyah_allowed:,.2f}")
            wasiyyah = max_wasiyyah_allowed
        else:
            wasiyyah = wasiyyah_input
            
        estate_amt = max(0.0, pre_wasiyyah_estate - wasiyyah)
        
        # Dynamic visual output to keep user informed before hitting calculate
        if gross_estate > 0:
            st.info(f"📋 **Net Distributable Estate:** {currency.split()[-1]} {estate_amt:,.2f} *(Gross subtracted by total deductions)*")
            
        st.markdown('</div>', unsafe_allow_html=True)

    st.write(f"### {m['sel_heir']}")

    tab_labels = ["Primary Heirs / الأصول والفروع", "Siblings & Uncles / الإخوة والأعمام"] if lang_code == "en" else [
        "الأصول والفروع والزوجين", "الحواشي (الإخوة والأعمام)"]
    tab1, tab2 = st.tabs(tab_labels)

    with tab1:
        for n in ALLOWED_HEIRS[:11]:
            max_v = 100
            if n in ["husband", "father", "mother", "grandfather"]:
                max_v = 1
            elif n == "wife":
                max_v = 4
            if n == "husband" and st.session_state.heirs_state["wife"] > 0: max_v = 0
            if n == "wife" and st.session_state.heirs_state["husband"] > 0: max_v = 0

            st.markdown(f'<div class="heir-entry-box">', unsafe_allow_html=True)
            row_c1, row_c2 = st.columns([4, 1])
            with row_c1:
                st.markdown(f"<div style='padding-top:4px;'><b>{m.get(n, n.upper())}</b></div>", unsafe_allow_html=True)
            with row_c2:
                st.session_state.heirs_state[n] = st.number_input(
                    label=n, min_value=0, max_value=max_v, value=st.session_state.heirs_state[n], key=f"tab1_{n}",
                    label_visibility="collapsed"
                )
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        for n in ALLOWED_HEIRS[11:]:
            st.markdown(f'<div class="heir-entry-box">', unsafe_allow_html=True)
            row_c1, row_c2 = st.columns([4, 1])
            with row_c1:
                st.markdown(f"<div style='padding-top:4px;'><b>{m.get(n, n.upper())}</b></div>", unsafe_allow_html=True)
            with row_c2:
                st.session_state.heirs_state[n] = st.number_input(
                    label=n, min_value=0, max_value=100, value=st.session_state.heirs_state[n], key=f"tab2_{n}",
                    label_visibility="collapsed"
                )
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    col_btn1, col_btn2 = st.columns([4, 1])
    with col_btn1:
        if st.button(m["calc"], type="primary", use_container_width=True):
            if estate_amt <= 0:
                st.error(m["inv_amt"])
            elif not any(v > 0 for v in st.session_state.heirs_state.values()):
                st.warning(m["sel_heir"])
            else:
                engine = InheritanceEngine(estate_amt, st.session_state.heirs_state)
                engine.calculate()
                st.session_state["cached_engine"] = engine
                st.session_state["cached_val"] = estate_amt
                st.session_state["cached_symbol"] = currency.split()[-1]
                st.session_state.calc_splash_trigger = True
                st.rerun()
    with col_btn2:
        if st.button(m["reset"], type="secondary", use_container_width=True):
            for k in ALLOWED_HEIRS: st.session_state.heirs_state[k] = 0
            st.rerun()

elif st.session_state.page_view == "result":
    eng = st.session_state.get("cached_engine", None)
    cur = st.session_state.get("cached_symbol", "₦")
    val = st.session_state.get("cached_val", 0.0)

    if eng is None:
        st.session_state.page_view = "input"
        st.rerun()

    st.markdown(f"## {m['breakdown']}")

    st.markdown(f'<div class="card-container">', unsafe_allow_html=True)
    st.metric(label=m["case_summary"], value=f"{val:,.2f} {cur}")
    st.markdown('</div>', unsafe_allow_html=True)

    pdf_file = generate_pdf_report(eng, val, cur, lang_code)
    st.download_button(
        label=m["download_pdf"],
        data=pdf_file,
        file_name=f"Faraid_Report_{int(time.time())}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.write("")
    h_col1, h_col2, h_col3, h_col4 = st.columns([3, 1.5, 1.5, 4])
    with h_col1:
        st.markdown(f'<div class="grid-header">{m["heir_header"]}</div>', unsafe_allow_html=True)
    with h_col2:
        st.markdown(f'<div class="grid-header">{m["share_header"]}</div>', unsafe_allow_html=True)
    with h_col3:
        st.markdown(f'<div class="grid-header">{m["pct_header"]}</div>', unsafe_allow_html=True)
    with h_col4:
        st.markdown(f'<div class="grid-header">{m["basis_header"]}</div>', unsafe_allow_html=True)

    for k, h in eng.h.items():
        percentage_val = float(h.fractional_share) * 100
        العقد_الفقهي = التعليلات_والشروط[lang_code].get(h.justification_key, التعليلات_والشروط[lang_code]["default"])

        row_col1, row_col2, row_col3, row_col4 = st.columns([3, 1.5, 1.5, 4])
        with row_col1:
            st.markdown(
                f'<div class="result-row"><b>{m.get(k, k)}</b> <span style="color:#8892B0;">(x{h.count})</span><br/><span style="color:#52B788; font-size:1.15rem; font-weight:700;">{cur} {h.individual_cash:,.2f}</span></div>',
                unsafe_allow_html=True)
        with row_col2:
            st.markdown(
                f'<div class="result-row" style="text-align:center; padding-top:25px;"><span style="font-size:1.25rem; color:#4CC9F0; font-weight:bold;">{h.fractional_share}</span></div>',
                unsafe_allow_html=True)
        with row_col3:
            st.markdown(
                f'<div class="result-row" style="text-align:center; padding-top:25px;"><span style="font-size:1.25rem; color:#FFB703; font-weight:bold;">{percentage_val:.2f}%</span></div>',
                unsafe_allow_html=True)
        with row_col4:
            st.markdown(
                f'<div class="result-row" style="font-size:0.92rem; color:#E2E8F0; line-height:1.4;">{العقد_الفقهي}</div>',
                unsafe_allow_html=True)

    if eng.case_meta["gharawain"]:
        st.markdown("### 📜 Structural Case Insight: The Gharawain Case (المسألة الغراوية)")
        with st.expander("Jurisprudential Analysis Breakdown / التحليل الفقهي الاستثنائي", expanded=True):
            if lang_code == "en":
                st.markdown(
                    "**Historical Origins:** Precedents established by the second Caliph, Umar ibn al-Khattab (R) (Umariyyah).")
            else:
                st.markdown(
                    "**التأصيل الفقهي للمسألة:** تُعرف بـ الغراويتين أو العُمريتين نسبةً لقضاء أمير المؤمنين عمر بن الخطاب رضي الله عنه.")

    st.write("---")
    if st.button(m["another"], type="secondary", use_container_width=True):
        st.session_state.page_view = "input"
        st.rerun()


# =====================================================================
# REACTION SECTION (PLACED AT THE BOTTOM OF THE APPLICATION)
# =====================================================================
st.write("---")
st.markdown("### Did this tool help you? Leave a reaction!")

# ==========================================
# 1. PERMANENT FILE STORAGE SETUP
# ==========================================
import os

LIKE_FILE = "interaction_counts.txt"

def load_counts():
    if os.path.exists(LIKE_FILE):
        try:
            with open(LIKE_FILE, "r") as f:
                lines = f.read().split(",")
                return int(lines[0]), int(lines[1])
        except:
            return 0, 0
    return 0, 0

def save_counts(likes, loves):
    with open(LIKE_FILE, "w") as f:
        f.write(f"{likes},{loves}")

# Initialize session state tracking for the current browser session
if "has_liked" not in st.session_state:
    st.session_state.has_liked = False
if "has_loved" not in st.session_state:
    st.session_state.has_loved = False

# Load the permanent totals from the file
permanent_likes, permanent_loves = load_counts()


# ==========================================
# 2. YOUR ORIGINAL BUTTON LAYOUT (UPDATED)
# ==========================================
col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    if st.button(f"Like ({permanent_likes})", disabled=st.session_state.has_liked, key="like_btn"):
        permanent_likes += 1
        save_counts(permanent_likes, permanent_loves) # Save permanently
        st.session_state.has_liked = True
        st.rerun()

with col2:
    if st.button(f"Love ({permanent_loves})", disabled=st.session_state.has_loved, key="love_btn"):
        permanent_loves += 1
        save_counts(permanent_likes, permanent_loves) # Save permanently
        st.session_state.has_loved = True
        st.rerun()

with col3:
    if st.session_state.has_liked or st.session_state.has_loved:
        st.success("Thank you for your feedback!")

st.write("---")
st.caption("Calculated in adherence to orthodox Islamic jurisprudence matrices.")

# =====================================================================
# SADAQAH JARIYAH / DONATION SECTION
# =====================================================================
st.write("---")
with st.container():
    # Use standard markdown container styling for a professional layout
    st.markdown("""
        <div style="
            background-color: #f4f6f9; 
            padding: 20px; 
            border-radius: 10px; 
            border-left: 5px solid #1e7e34;
            margin-top: 20px;">
            <h3 style="color: #1e7e34; margin-top: 0;">✨ Support as Sadaqah Jariyah</h3>
            <p style="color: #333333; font-size: 15px;">
                If this tool helped you or your family compute your estate shares accurately, 
                please consider supporting its hosting costs and continuous maintenance. 
                Any contribution is a form of continuous charity.
            </p>
        </div>
    """, unsafe_allow_html=True)

    #     # Split layout into two columns
    col_local, col_intl = st.columns(2)
    
    with col_local:
        st.markdown("### 🇳🇬 Inside Nigeria")
        st.write("**Direct Bank Transfer / OPay**")
        st.info("""
        • Bank Name: **OPay**
        • Account Number: **9138080996**
        • Account Name: **AbdulAzeez Hammad Omokunmi**
        """)
        st.caption("You can transfer directly using your local mobile banking app.")

    with col_intl:
        st.markdown("### 🌐 Outside Nigeria (USD / GBP / EUR)")
        st.write("**International Remittance App**")
        st.success("""
        • Wallet Provider: **OPay**
        • Wallet Number: **9138080996**
        • Receiver Name: **AbdulAzeez Hammad Omokunmi**
        """)
        st.caption("Donors abroad can use **Remitly**, **WorldRemit**, or **LemFi** to send funds straight to this OPay wallet. The apps handle currency conversion automatically.")

     


