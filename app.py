import streamlit as st
import pandas as pd
import io

# --- 1. إعدادات الصفحة والتصميم العام ---
st.set_page_config(
    page_title="نظام توزيع التكية - مخيم الكرامة",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم (CSS) ليكون احترافياً
st.markdown("""
    <style>
    /* استيراد خط تجريبي جميل للعناوين */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl; /* اتجاه النص للعربية */
    }
    
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 1px 1px 2px #d1d1d1;
    }
    
    .sub-title {
        text-align: center;
        color: #555;
        font-size: 18px;
        margin-bottom: 25px;
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #333;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #ddd;
    }
    
    /* تنسيق الجداول */
    .stDataFrame { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# --- 2. واجهة العرض الرئيسية ---
st.markdown('<div class="main-title">🌙 نظام توزيع التكية - مخيم الكرامة</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">الإدارة والتطوير: م. عبدالله حميد الصوفي</div>', unsafe_allow_html=True)

# --- 3. القائمة الجانبية (Sidebar) ---
st.sidebar.markdown("### ⚙️ لوحة التحكم والمعايير")
st.sidebar.info("تحكم هنا في شروط توزيع الوجبات حسب حجم الأسرة")

# مدخلات المعايير
limit_2_meals = st.sidebar.number_input(
    "عدد الأفراد لاستحقاق وجبتين (2):",
    min_value=1, value=6, step=1
)

limit_3_meals = st.sidebar.number_input(
    "عدد الأفراد لاستحقاق 3 وجبات:",
    min_value=limit_2_meals + 1, value=10, step=1
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📦 احتياطي الطوارئ")
reserve_meals = st.sidebar.number_input(
    "وجبات إضافية (احتياطي للمخيم):",
    min_value=0, value=0, step=5
)

st.sidebar.markdown("---")
st.sidebar.markdown("###### حقوق النشر محفوظة © 2026 \n م. عبدالله حميد الصوفي")

# --- 4. معالجة الملف ---
uploaded_file = st.file_uploader("📂 اسحب وأفلت ملف الإكسل هنا (تأكد من وجود عمود 'عدد الافراد')", type=['xlsx', 'xls'])

if uploaded_file:
    try:
        # قراءة الملف
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip() # تنظيف أسماء الأعمدة

        if 'عدد الافراد' in df.columns:
            
            # --- المنطق الحسابي ---
            def calculate_meals(row):
                try:
                    size = int(row['عدد الافراد'])
                except:
                    return 1 # القيمة الافتراضية عند الخطأ
                
                if size >= limit_3_meals:
                    return 3
                elif size >= limit_2_meals:
                    return 2
                else:
                    return 1

            df['عدد الوجبات المستحقة'] = df.apply(calculate_meals, axis=1)

            # الإحصائيات
            total_meals_families = df['عدد الوجبات المستحقة'].sum()
            grand_total = total_meals_families + reserve_meals
            
            # عرض الإحصائيات في بطاقات جميلة
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📌 إجمالي المطلوب (مع الاحتياطي)", f"{grand_total}", delta=f"{reserve_meals} احتياطي")
            col2.metric("🍲 وجبات العائلات فقط", f"{total_meals_families}")
            col3.metric("👨‍👩‍👧‍👦 عدد العائلات", f"{len(df)}")
            col4.metric("📊 نظام التوزيع", f"2 بدءاً من {limit_2_meals} | 3 بدءاً من {limit_3_meals}")

            st.divider()

            # تحديد الأعمدة المطلوبة للعرض والتصدير
            wanted_columns = [
                'الاسم رباعي', 'رقم الهوية', 'رقم الجوال', 'عدد الافراد',
                'عدد الوجبات المستحقة', # العمود الجديد
                'اسم الزوج/ـة', 'رقم هوية الزوج/ـة', 'ملاحظات الحالة',
                'اسم مندوب المربع', 'اسم المخيم', 'اسم مندوب المخيم', 'ملاحظات'
            ]
            final_cols = [c for c in wanted_columns if c in df.columns]
            df_export = df[final_cols].copy()

            st.write("### 📋 معاينة البيانات بعد المعالجة:")
            st.dataframe(df_export.head(5), use_container_width=True)

            # --- 5. إنشاء ملف الإكسل الملون والذكي ---
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                sheet_name = 'توزيع الوجبات'
                df_export.to_excel(writer, index=False, sheet_name=sheet_name)
                
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                
                # تفعيل اتجاه اليمين لليسار (مهم جداً للعربي)
                worksheet.right_to_left()
                
                # تنسيقات الألوان (Styles)
                header_fmt = workbook.add_format({
                    'bold': True, 'fg_color': '#284f85', 'font_color': 'white',
                    'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 12
                })
                
                base_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
                
                # ألوان الوجبات (Conditional Formatting Colors)
                fmt_green = workbook.add_format({'bg_color': '#c6efce', 'font_color': '#006100', 'border': 1}) # للـ 3 وجبات
                fmt_yellow = workbook.add_format({'bg_color': '#ffeb9c', 'font_color': '#9c5700', 'border': 1}) # للوجبتين
                fmt_normal = workbook.add_format({'border': 1, 'align': 'center'}) # للوجبة الواحدة

                # تطبيق تنسيق العناوين وتوسيع الأعمدة
                for col_num, value in enumerate(df_export.columns.values):
                    worksheet.write(0, col_num, value, header_fmt)
                    worksheet.set_column(col_num, col_num, 20) # عرض العمود

                # معرفة رقم عمود "عدد الوجبات المستحقة" لتلوينه
                # الحرف المقابل للعمود (A=0, B=1, etc.)
                try:
                    meal_col_idx = df_export.columns.get_loc('عدد الوجبات المستحقة')
                    # تحويل الرقم لحرف (مثلاً 4 -> E)
                    col_letter = chr(ord('A') + meal_col_idx)
                    
                    # عدد الصفوف
                    max_row = len(df_export) + 1
                    
                    # تطبيق التلوين الشرطي
                    # 1. إذا كان الرقم 3 -> لون أخضر
                    worksheet.conditional_format(f'{col_letter}2:{col_letter}{max_row}', {
                        'type': 'cell', 'criteria': '>=', 'value': 3, 'format': fmt_green
                    })
                    # 2. إذا كان الرقم 2 -> لون أصفر
                    worksheet.conditional_format(f'{col_letter}2:{col_letter}{max_row}', {
                        'type': 'cell', 'criteria': '=', 'value': 2, 'format': fmt_yellow
                    })
                    # 3. الباقي عادي
                    worksheet.conditional_format(f'{col_letter}2:{col_letter}{max_row}', {
                        'type': 'cell', 'criteria': '=', 'value': 1, 'format': base_fmt
                    })
                except:
                    pass # تجاوز التلوين في حال حدوث خطأ بسيط

            # --- زر التحميل النهائي ---
            st.download_button(
                label="📥 تحميل الكشف النهائي (Excel ملون وجاهز)",
                data=output.getvalue(),
                file_name=f'كشف_توزيع_الكرامة_{grand_total}_وجبة.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        else:
            st.error("⚠️ خطأ: لم يتم العثور على عمود باسم 'عدد الافراد' في الملف.")

    except Exception as e:
        st.error(f"حدث خطأ غير متوقع: {e}")

# --- تذييل الصفحة ---
st.markdown("""
<div class="footer">
    تم تطوير النظام لتسهيل خدمة أهلنا في مخيم الكرامة (أرض الشاعر) <br>
    <b>جميع الحقوق محفوظة للمطور: م. عبدالله حميد الصوفي © 2026</b>
</div>
""", unsafe_allow_html=True)
