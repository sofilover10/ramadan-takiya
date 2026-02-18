import streamlit as st
import pandas as pd
import io

# إعداد الصفحة
st.set_page_config(page_title="توزيع التكية - فش فرش", layout="wide")

# العنوان والشعار
st.title("🌙 نظام توزيع التكية - مخيمات فش فرش الشمالي")
st.write("---")

# دالة الحساب (القاعدة: أقل من 5 = 1، 5 وأكثر = 2)
def calculate_meals(members):
    try:
        # تحويل القيمة لرقم والتأكد منها
        val = float(members)
        if val < 5:
            return 1
        else:
            return 2
    except:
        return 0

# رفع الملف
uploaded_file = st.file_uploader("📂 قم برفع ملف الإكسل (Excel أو CSV) هنا:", type=['xlsx', 'csv', 'xls'])

if uploaded_file is not None:
    try:
        # قراءة الملف
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # تنظيف أسماء الأعمدة لإزالة المسافات الزائدة
        df.columns = df.columns.str.strip()

        # البحث عن عمود عدد الأفراد (قد يختلف الاسم قليلًا)
        possible_names = ['عدد الافراد', 'عدد الأفراد', 'عدد افراد الأسرة', 'عدد أفراد الأسرة']
        col_name = None
        for name in possible_names:
            if name in df.columns:
                col_name = name
                break
        
        if col_name:
            # الحساب
            df['عدد الوجبات المستحقة'] = df[col_name].apply(calculate_meals)

            # عرض النتائج
            st.success("✅ تم الحساب بنجاح!")
            
            # إحصائيات سريعة
            total_families = len(df)
            total_meals = df['عدد الوجبات المستحقة'].sum()
            
            c1, c2 = st.columns(2)
            c1.metric("عدد العائلات", total_families)
            c2.metric("مجموع الوجبات المطلوبة", f"{total_meals} وجبة")

            # عرض الجدول
            st.dataframe(df)

            # زر التحميل
            output = io.BytesIO()
            # حفظ كملف Excel
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            
            st.download_button(
                label="📥 تحميل الملف جاهز مع الوجبات (Excel)",
                data=output.getvalue(),
                file_name=f"توزيع_رمضان_{uploaded_file.name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("⚠️ لم يتم العثور على عمود باسم 'عدد الافراد'. تأكد من اسم العمود في الملف.")

    except Exception as e:
        st.error(f"حدث خطأ: {e}")
