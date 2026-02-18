import streamlit as st
import pandas as pd
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="توزيع التكية - لجنة فش فرش الشمالي",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. تنسيقات CSS الاحترافية ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #f0f2f6; }
    
    /* تنسيق الهيدر */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .main-header h1 { margin: 0; font-size: 2.2rem; font-weight: bold; text-shadow: 2px 2px 4px #000000; }
    .dedication { font-size: 1.2rem; color: #ffeb3b; margin-top: 10px; font-weight: bold; }
    .developer { margin-top: 15px; opacity: 0.8; font-size: 0.9rem; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 5px; display: inline-block;}

    /* تنسيق البطاقات */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 5px solid #ddd;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-5px); }
    .metric-value { font-size: 2.5rem; font-weight: bold; color: #333; }
    .metric-label { font-size: 1rem; color: #666; margin-bottom: 5px; }
    
    /* ألوان الحدود العلوية للبطاقات */
    .border-red { border-color: #e74c3c; }
    .border-blue { border-color: #3498db; }
    .border-green { border-color: #2ecc71; }
    .border-orange { border-color: #f39c12; }

    /* تنسيق الفوتر (التذييل) */
    .footer { 
        text-align: center; 
        margin-top: 50px; 
        padding: 30px; 
        background-color: #ffffff;
        border-top: 1px solid #e0e0e0; 
        border-radius: 15px 15px 0 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    .footer p { margin: 5px 0; color: #555; }
    .contact-info { margin-top: 15px; }
    .contact-link { 
        text-decoration: none; 
        margin: 0 10px; 
        font-weight: bold; 
        display: inline-block;
        transition: color 0.3s;
    }
    .whatsapp-link { color: #25D366; }
    .phone-link { color: #1e3c72; }
    .contact-link:hover { opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# --- 3. الهيدر الجديد ---
st.markdown("""
<div class="main-header">
    <h1>🌙 نظام توزيع التكية - لجنة فش فرش الشمالي</h1>
    <div class="dedication">بجهد مبارك من الأخ الفاضل إبراهيم الشاعر (أبو عمر)</div>
    <div class="developer">الإدارة والتطوير: م. عبدالله حميد الصوفي</div>
</div>
""", unsafe_allow_html=True)

# --- 4. القائمة الجانبية (التحكم بالمعايير) ---
st.sidebar.header("⚙️ ضبط معايير التوزيع")
st.sidebar.markdown("قم بتغيير الأرقام أدناه لتحديد من يستحق وجبة، وجبتين، أو ثلاث.")

# --- قسم الوجبتين ---
st.sidebar.markdown("---")
st.sidebar.subheader("1️⃣ فئة الوجبتين (2)")
limit_2_meals = st.sidebar.number_input(
    "يبدأ استحقاق الوجبتين من عدد أفراد:",
    min_value=2, value=7, step=1,
    help="أي عائلة عدد أفرادها يساوي هذا الرقم أو أكثر ستأخذ وجبتين."
)
st.sidebar.info(f"✅ إذن: العائلات من 1 إلى {limit_2_meals - 1} أفراد تأخذ **وجبة واحدة**.")

# --- قسم الـ 3 وجبات ---
st.sidebar.markdown("---")
st.sidebar.subheader("2️⃣ فئة الـ 3 وجبات")
limit_3_meals = st.sidebar.number_input(
    "يبدأ استحقاق الـ 3 وجبات من عدد أفراد:",
    min_value=limit_2_meals + 1, value=11, step=1,
    help="أي عائلة تصل لهذا العدد ستأخذ 3 وجبات."
)
st.sidebar.info(f"✅ إذن: العائلات من {limit_2_meals} إلى {limit_3_meals - 1} أفراد تأخذ **وجبتين**.")
st.sidebar.success(f"🌟 العائلات {limit_3_meals} أفراد فأكثر تأخذ **3 وجبات**.")

# --- قسم الاحتياطي ---
st.sidebar.markdown("---")
st.sidebar.subheader("📦 الاحتياطي")
reserve_meals = st.sidebar.number_input(
    "عدد الوجبات الإضافية (للطوارئ):",
    min_value=0, value=0, step=5
)

st.sidebar.markdown("---")
st.sidebar.markdown("حقوق النشر محفوظة © 2026 \n م. عبدالله حميد الصوفي")

# --- 5. التطبيق الرئيسي ---
uploaded_file = st.file_uploader("📂 قم برفع ملف الإكسل (Excel) هنا", type=['xlsx', 'xls'])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        if 'عدد الافراد' in df.columns:
            
            # دالة الحساب
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

            # الحسابات
            total_meals_families = df['عدد الوجبات المستحقة'].sum()
            grand_total = total_meals_families + reserve_meals
            total_families = len(df)

            # --- عرض البطاقات (Dashboard) ---
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                st.markdown(f"""
                <div class="metric-card border-red">
                    <div class="metric-label">الإجمالي المطلوب (مع الاحتياطي)</div>
                    <div class="metric-value">{grand_total}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                st.markdown(f"""
                <div class="metric-card border-blue">
                    <div class="metric-label">عدد العائلات</div>
                    <div class="metric-value">{total_families}</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="metric-card border-green">
                    <div class="metric-label">وجبات الأهالي فقط</div>
                    <div class="metric-value">{total_meals_families}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with c4:
                 st.markdown(f"""
                <div class="metric-card border-orange">
                    <div class="metric-label">الاحتياطي المضاف</div>
                    <div class="metric-value">{reserve_meals}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 📋 معاينة النتائج:")
            
            # تجهيز الجدول للعرض
            wanted_columns = ['الاسم رباعي', 'رقم الهوية', 'رقم الجوال', 'عدد الافراد', 'عدد الوجبات المستحقة', 'ملاحظات']
            existing_cols = [c for c in wanted_columns if c in df.columns]
            cols = existing_cols + [c for c in df.columns if c not in existing_cols]
            st.dataframe(df[cols].head(10), use_container_width=True)

            # --- التصدير للإكسل ---
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                sheet_name = 'التوزيع النهائي'
                export_cols = [c for c in ['الاسم رباعي', 'رقم الهوية', 'رقم الجوال', 'عدد الافراد', 'عدد الوجبات المستحقة', 'اسم الزوج/ـة', 'رقم هوية الزوج/ـة', 'ملاحظات الحالة', 'اسم مندوب المربع', 'اسم المخيم', 'اسم مندوب المخيم', 'ملاحظات'] if c in df.columns]
                
                df_final = df[export_cols]
                df_final.to_excel(writer, index=False, sheet_name=sheet_name)
                
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                worksheet.right_to_left()
                
                # التنسيقات
                header_fmt = workbook.add_format({'bold': True, 'fg_color': '#2a5298', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
                cell_fmt = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
                
                # تنسيق العناوين
                for col_num, value in enumerate(df_final.columns.values):
                    worksheet.write(0, col_num, value, header_fmt)
                    worksheet.set_column(col_num, col_num, 20)

                # التلوين الشرطي
                try:
                    meal_idx = df_final.columns.get_loc('عدد الوجبات المستحقة')
                    col_char = chr(ord('A') + meal_idx)
                    max_row = len(df_final) + 1
                    
                    # 3 وجبات = أخضر
                    worksheet.conditional_format(f'{col_char}2:{col_char}{max_row}', {'type': 'cell', 'criteria': '>=', 'value': 3, 'format': workbook.add_format({'bg_color': '#c8e6c9', 'font_color': '#006100', 'border': 1, 'align': 'center'})})
                    # 2 وجبة = أصفر
                    worksheet.conditional_format(f'{col_char}2:{col_char}{max_row}', {'type': 'cell', 'criteria': '=', 'value': 2, 'format': workbook.add_format({'bg_color': '#ffeb9c', 'font_color': '#9c6500', 'border': 1, 'align': 'center'})})
                    # 1 وجبة = عادي
                    worksheet.conditional_format(f'{col_char}2:{col_char}{max_row}', {'type': 'cell', 'criteria': '=', 'value': 1, 'format': cell_fmt})
                except:
                    pass

            st.download_button(
                label="📥 تحميل الكشف (Excel) جاهز وملون",
                data=output.getvalue(),
                file_name=f'كشف_توزيع_الشمالي_{grand_total}_وجبة.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        else:
            st.error("⚠️ الملف المرفوع لا يحتوي على عمود 'عدد الافراد'. تأكد من صحة الملف.")

    except Exception as e:
        st.error(f"حدث خطأ: {e}")

# --- الفوتر الجديد مع التواصل ---
st.markdown("""
<div class="footer">
    <p>جميع الحقوق محفوظة للمطور: <b>م. عبدالله حميد الصوفي</b> © 2026</p>
    <p>تم التطوير لخدمة لجنة فش فرش الشمالي</p>
    
    <div class="contact-info">
        <a href="https://wa.me/972567100000" target="_blank" class="contact-link whatsapp-link">
            💬 واتساب: 00972567100000
        </a>
        <span style="color: #ccc;">|</span>
        <a href="tel:0567100000" class="contact-link phone-link">
            📞 جوال: 0567100000
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
