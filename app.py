import streamlit as st
import pandas as pd
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="نظام توزيع التكية - مخيم الكرامة",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. التصميم والألوان (CSS الاحترافي) ---
st.markdown("""
<style>
    /* استيراد خط عربي أنيق */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }

    /* خلفية التطبيق */
    .stApp {
        background-color: #f4f6f9;
    }

    /* تنسيق العناوين */
    .main-header {
        text-align: center;
        color: #1e3d59;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border-bottom: 4px solid #ff6e40;
    }
    
    .main-header h1 {
        color: #1e3d59;
        font-weight: 800;
        font-size: 32px;
        margin: 0;
    }
    
    .main-header h3 {
        color: #6c757d;
        font-size: 16px;
        margin-top: 5px;
    }

    /* تنسيق بطاقات الإحصائيات الملونة */
    .stat-card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        transition: transform 0.3s;
        margin-bottom: 10px;
    }
    .stat-card:hover {
        transform: translateY(-5px);
    }
    .stat-card h2 {
        font-size: 36px;
        margin: 0;
        font-weight: bold;
    }
    .stat-card p {
        font-size: 18px;
        margin: 0;
        opacity: 0.9;
    }

    /* ألوان البطاقات */
    .bg-total { background: linear-gradient(135deg, #d32f2f, #ef5350); } /* أحمر للاجمالي */
    .bg-families { background: linear-gradient(135deg, #1976d2, #42a5f5); } /* أزرق للعائلات */
    .bg-meals { background: linear-gradient(135deg, #388e3c, #66bb6a); } /* أخضر للوجبات */
    .bg-reserve { background: linear-gradient(135deg, #fbc02d, #ffeb3b); color: #333 !important; } /* أصفر للاحتياطي */

    /* تذييل الصفحة */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #666;
        font-size: 14px;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. واجهة العرض (Header) ---
st.markdown("""
<div class="main-header">
    <h1>🌙 نظام توزيع التكية - مخيم الكرامة</h1>
    <h3>الإدارة والتطوير: م. عبدالله حميد الصوفي</h3>
</div>
""", unsafe_allow_html=True)

# --- 4. القائمة الجانبية (Sidebar) ---
st.sidebar.markdown("### ⚙️ إعدادات التوزيع")
st.sidebar.info("قم بتعديل المعايير أدناه وسيتم إعادة الحساب فوراً")

# معيار الوجبتين
limit_2_meals = st.sidebar.number_input(
    "👨‍👩‍👧‍👦 يبدأ استحقاق (وجبتين) من عدد أفراد:",
    min_value=1, value=6, step=1,
    help="مثلاً: إذا اخترت 6، فإن أي أسرة عددها 6 أو أكثر ستحصل على وجبتين."
)

# معيار 3 وجبات
limit_3_meals = st.sidebar.number_input(
    "👨‍👩‍👧‍👦‍👦 يبدأ استحقاق (3 وجبات) من عدد أفراد:",
    min_value=limit_2_meals + 1, value=10, step=1,
    help="مثلاً: إذا اخترت 10، فإن أي أسرة عددها 10 أو أكثر ستحصل على 3 وجبات."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📦 المخزون الاحتياطي")
reserve_meals = st.sidebar.number_input(
    "عدد الوجبات الإضافية (احتياطي للمخيم):",
    min_value=0, value=0, step=5
)

# --- 5. معالجة الملف ---
uploaded_file = st.file_uploader("📂 قم برفع ملف الإكسل (Excel) هنا", type=['xlsx', 'xls'])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        if 'عدد الافراد' in df.columns:
            
            # منطق الحساب
            def calculate_meals(row):
                try:
                    size = int(row['عدد الافراد'])
                except:
                    return 1
                
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
            total_families = len(df)

            # --- عرض الإحصائيات ببطاقات ملونة (HTML Custom) ---
            st.markdown("### 📊 ملخص التوزيع:")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card bg-total">
                    <p>🚨 الإجمالي المطلوب</p>
                    <h2>{grand_total}</h2>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="stat-card bg-families">
                    <p>👨‍👩‍👧‍👦 عدد العائلات</p>
                    <h2>{total_families}</h2>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="stat-card bg-meals">
                    <p>🍲 وجبات الأهالي</p>
                    <h2>{total_meals_families}</h2>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                # لون الاحتياطي يختلف إذا كان صفر أو له قيمة
                reserve_bg = "bg-reserve" if reserve_meals > 0 else "bg-families"
                st.markdown(f"""
                <div class="stat-card {reserve_bg}" style="color: #333;">
                    <p>📦 الاحتياطي</p>
                    <h2>{reserve_meals}</h2>
                </div>
                """, unsafe_allow_html=True)

            # عرض المعايير الحالية
            st.caption(f"ℹ️ النظام الحالي: (وجبتين) لمن هم {limit_2_meals} فأكثر | (3 وجبات) لمن هم {limit_3_meals} فأكثر")
            
            st.divider()

            # تجهيز الجدول
            wanted_columns = [
                'الاسم رباعي', 'رقم الهوية', 'رقم الجوال', 'عدد الافراد',
                'عدد الوجبات المستحقة',
                'اسم الزوج/ـة', 'رقم هوية الزوج/ـة', 'ملاحظات الحالة',
                'اسم مندوب المربع', 'اسم المخيم', 'اسم مندوب المخيم', 'ملاحظات'
            ]
            final_cols = [c for c in wanted_columns if c in df.columns]
            df_export = df[final_cols].copy()

            st.write("### 📋 معاينة الجدول:")
            st.dataframe(df_export.head(5), use_container_width=True)

            # --- تصدير الإكسل الملون ---
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                sheet_name = 'كشف التوزيع'
                df_export.to_excel(writer, index=False, sheet_name=sheet_name)
                
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                worksheet.right_to_left()
                
                # التنسيقات
                header_fmt = workbook.add_format({
                    'bold': True, 'fg_color': '#1e3d59', 'font_color': 'white',
                    'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 12
                })
                base_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
                
                # ألوان الخلايا (نفس ألوان الموقع تقريباً)
                fmt_green = workbook.add_format({'bg_color': '#c8e6c9', 'font_color': '#1b5e20', 'border': 1, 'align': 'center'}) # أخضر فاتح
                fmt_orange = workbook.add_format({'bg_color': '#ffcc80', 'font_color': '#e65100', 'border': 1, 'align': 'center'}) # برتقالي فاتح
                
                # تطبيق العناوين وتوسيع الأعمدة
                for col_num, value in enumerate(df_export.columns.values):
                    worksheet.write(0, col_num, value, header_fmt)
                    worksheet.set_column(col_num, col_num, 20)

                # التلوين الشرطي
                try:
                    meal_col_idx = df_export.columns.get_loc('عدد الوجبات المستحقة')
                    col_letter = chr(ord('A') + meal_col_idx)
                    max_row = len(df_export) + 1
                    
                    # 3 وجبات = أخضر
                    worksheet.conditional_format(f'{col_letter}2:{col_letter}{max_row}', {
                        'type': 'cell', 'criteria': '>=', 'value': 3, 'format': fmt_green
                    })
                    # وجبتين = برتقالي
                    worksheet.conditional_format(f'{col_letter}2:{col_letter}{max_row}', {
                        'type': 'cell', 'criteria': '=', 'value': 2, 'format': fmt_orange
                    })
                    # وجبة واحدة = عادي
                    worksheet.conditional_format(f'{col_letter}2:{col_letter}{max_row}', {
                        'type': 'cell', 'criteria': '=', 'value': 1, 'format': base_fmt
                    })
                except:
                    pass

            st.download_button(
                label="📥 تحميل الكشف النهائي (Excel ملون وجاهز)",
                data=output.getvalue(),
                file_name=f'توزيع_الكرامة_{grand_total}_وجبة.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        else:
            st.error("⚠️ الملف لا يحتوي على عمود 'عدد الافراد'.")

    except Exception as e:
        st.error(f"حدث خطأ: {e}")

# Footer
st.markdown("""
<div class="footer">
    تم تطوير النظام لتسهيل خدمة أهلنا في مخيم الكرامة (أرض الشاعر) <br>
    <b>جميع الحقوق محفوظة للمطور: م. عبدالله حميد الصوفي © 2026</b>
</div>
""", unsafe_allow_html=True)
