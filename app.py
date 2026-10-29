import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Medical Appointment No-Shows", page_icon="🏥", layout="wide")

st.title("🏥 Medical Appointment No-Shows")
st.write("استكشاف البيانات وفحص جودتها قبل التحليل.")

st.sidebar.header("تحميل البيانات")
uploaded_file = st.sidebar.file_uploader(
    "ارفعي ملف CSV الخاص بالـ Dataset",
    type=["csv"],
    help="حمّلي ملف CSV من Kaggle ثم اختاريه هنا."
)

if uploaded_file is None:
    st.info("ابدئي برفع ملف CSV الذي نزّلتيه من Kaggle لعرض التحليل.")
    st.markdown("""
    **الخطوات:**
    1. افتحي صفحة Dataset على Kaggle.
    2. نزّلي ملف البيانات وفكّي ضغط ZIP.
    3. ارفعي ملف CSV من القائمة الجانبية.
    """)
    st.stop()

try:
    df = pd.read_csv(uploaded_file)
except Exception as exc:
    st.error(f"تعذرت قراءة الملف. تأكدي أنه ملف CSV صالح. التفاصيل: {exc}")
    st.stop()

# Basic overview
st.subheader("1. نظرة عامة على البيانات")
c1, c2, c3 = st.columns(3)
c1.metric("عدد الصفوف", f"{df.shape[0]:,}")
c2.metric("عدد الأعمدة", f"{df.shape[1]:,}")
c3.metric("الصفوف المكررة بالكامل", f"{int(df.duplicated().sum()):,}")

with st.expander("عرض أول 10 صفوف", expanded=True):
    st.dataframe(df.head(10), use_container_width=True)

# Data types
st.subheader("2. أنواع الأعمدة")
dtype_df = pd.DataFrame({
    "Column": df.columns.astype(str),
    "Data type": [str(dtype) for dtype in df.dtypes],
    "Missing values": [int(df[col].isna().sum()) for col in df.columns],
    "Unique values": [int(df[col].nunique(dropna=True)) for col in df.columns],
})
st.dataframe(dtype_df, use_container_width=True)

numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

c1, c2 = st.columns(2)
with c1:
    st.write("**الأعمدة الرقمية**")
    st.write(numeric_cols if numeric_cols else "لم يتم اكتشاف أعمدة رقمية.")
with c2:
    st.write("**الأعمدة الفئوية / النصية**")
    st.write(categorical_cols if categorical_cols else "لم يتم اكتشاف أعمدة فئوية أو نصية.")

# Missing values
st.subheader("3. فحص القيم المفقودة")
missing = df.isna().sum().sort_values(ascending=False)
missing_nonzero = missing[missing > 0]
if missing_nonzero.empty:
    st.success("لم تُكتشف قيم مفقودة بصيغة NaN في الملف.")
else:
    st.dataframe(
        missing_nonzero.rename("Missing count").to_frame(),
        use_container_width=True
    )

# Duplicate rows
st.subheader("4. فحص الصفوف المكررة")
duplicate_count = int(df.duplicated().sum())
if duplicate_count == 0:
    st.success("لم يتم العثور على صفوف مكررة بالكامل.")
else:
    st.warning(f"تم العثور على {duplicate_count:,} صفًا مكررًا بالكامل.")
    with st.expander("عرض أمثلة من الصفوف المكررة"):
        st.dataframe(df[df.duplicated(keep=False)].head(20), use_container_width=True)

# Age anomaly check
st.subheader("5. فحص قيم العمر غير المنطقية")
age_col = next((col for col in df.columns if str(col).strip().lower() == "age"), None)
if age_col is None:
    st.info("لم يتم العثور على عمود اسمه Age، لذلك تم تخطي فحص العمر.")
else:
    age_numeric = pd.to_numeric(df[age_col], errors="coerce")
    invalid_age = df[age_numeric < 0]
    c1, c2 = st.columns(2)
    c1.metric("عدد الأعمار السالبة", f"{len(invalid_age):,}")
    c2.metric("أكبر عمر مسجل", str(age_numeric.max()) if age_numeric.notna().any() else "غير متاح")
    if invalid_age.empty:
        st.success("لم يتم العثور على أعمار سالبة.")
    else:
        st.warning("الأعمار السالبة غير منطقية وتحتاج إلى مراجعة قبل التحليل.")
        st.dataframe(invalid_age.head(20), use_container_width=True)

# Category consistency check
st.subheader("6. فحص القيم الفئوية")
for candidate in ["Gender", "No-show"]:
    actual_col = next((col for col in df.columns if str(col).strip().lower() == candidate.lower()), None)
    if actual_col is not None:
        with st.expander(f"القيم الموجودة في {actual_col}"):
            st.write(df[actual_col].value_counts(dropna=False).head(30))

# No-show chart
st.subheader("7. تحليل مبدئي لحالة الحضور")
noshow_col = next((col for col in df.columns if str(col).strip().lower() == "no-show"), None)
if noshow_col is not None:
    counts = df[noshow_col].astype("string").fillna("Missing").value_counts()
    st.bar_chart(counts)
    st.caption("يعرض الرسم عدد السجلات لكل قيمة في عمود No-show. تحققي من معنى القيم حسب وصف مصدر البيانات.")
else:
    st.info("لم يتم العثور على عمود No-show، لذلك لم يتم إنشاء الرسم الخاص بالحضور.")

st.subheader("8. ملاحظات قبل التنظيف")
st.write(
    "هذه الصفحة تفحص البيانات وتعرض مؤشرات أولية فقط. "
    "لا يتم حذف الصفوف أو تعديل القيم تلقائيًا؛ يجب مراجعة كل مشكلة وفهم معناها قبل اتخاذ قرار التنظيف."
)

st.caption("Dataset: Medical Appointment No-Shows | Built with Python, Pandas, and Streamlit")
