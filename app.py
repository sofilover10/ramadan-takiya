import streamlit as st
import pandas as pd
import io

# 1. تحسين الشكل الخارجي وإعدادات الصفحة
st.set_page_config(
    page_title="نظام توزيع التكية",
    page_icon="🌙",
    layout="wide"
)

# عنوان التطبيق في المنتصف
st.markdown("<h1 style='text-align: center; color: #2e7bcf;'>🌙 نظام توزيع التكية - إدارة الوجبات</h1>", unsafe_allow_html=True)
st.markdown("---")

# 2. القائمة الجانبية (Sidebar) للتحكم في المعايير
st.sidebar.header("⚙️ إعدادات التوزيع")
st.sidebar.write("تحكم هنا في عدد الأفراد لكل فئة:")

# تحديد الحد الأدنى للوجبتين (أنت تختار الرقم)
limit_2_meals = st.sidebar.number_input(
    "عدد الأفراد لاستحقاق وجبتين (2):",
    min_value=1,
    value=6,  # القيمة الافتراضية
    help="أي عائلة عدد أفرادها يساوي أو أكبر من هذا الرقم ستحصل على وجبتين"
)

# تحديد الحد الأدنى لـ 3 وجبات (أنت تختار الرقم)
limit_3_meals = st.sidebar.number_input(
    "عدد الأفراد لاستحقاق 3 وجبات:",
    min_value=1,
    value=10, # القيمة الافتراضية
    help="أي عائلة عدد أفرادها يساوي أو أكبر من هذا الرقم ستحصل على 3 وجبات"
)

# رفع الملف
uploaded_file = st.file_uploader("📂 قم برفع ملف الإكسل (يجب أن يحتوي على عمود 'عدد الافراد')", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # قراءة الملف
        df = pd.read_excel(uploaded_file)
        
        # التأكد من وجود عمود عدد الأفراد
        if 'عدد الافراد' in df.columns:
            
            # --- 3. المنطق الجديد للحساب بناءً على اختيارك ---
            def calculate_meals(row):
                family_size = row['عدد الافراد']
                
                # التعامل مع القيم الفارغة أو غير الرقمية
                try:
                    family_size = int(family_size)
                except:
                    return 0 # إذا كان الرقم خطأ يرجع 0
                
                # تطبيق المعايير التي اخترتها في القائمة الجانبية
                if family_size >= limit_3_meals:
                    return 3
                elif family_size >= limit_2_meals:
                    return 2
                else:
                    return 1

            # تطبيق الدالة
            df['عدد الوجبات المستحقة'] = df.apply(calculate_meals, axis=1)
            
            # --- عرض الإحصائيات بشكل جميل ---
            total_meals = df['عدد الوجبات المستحقة'].sum()
            total_families = len(df)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("إجمالي الوجبات المطلوبة", f"{total_meals} وجبة")
            col2.metric("عدد العائلات", f"{total_families} عائلة")
            col3.metric("معيار الوجبتين", f"من {limit_2_meals} أفراد فأكثر")

            st.success("✅ تم الحساب بنجاح!")
            
            # عرض الجدول
            st.dataframe(df)
            
            # --- 4. التحضير للتحميل (Excel Report) ---
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='توزيع الوجبات')
                
                # تنسيق الملف ليظهر بشكل جميل عند الفتح
                workbook = writer.book
                worksheet = writer.sheets['توزيع الوجبات']
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',
                    'border': 1
                })
                # تطبيق التنسيق على الأعمدة
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    worksheet.set_column(col_num, col_num, 15) # توسيع الأعمدة

            processed_data = output.getvalue()
            
            st.download_button(
                label="📥 تحميل التقرير (Excel جاهز للطباعة)",
                data=processed_data,
                file_name=f'تقرير_توزيع_الوجبات_{total_meals}_وجبة.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        else:
            st.error("⚠️ عذراً، الملف لا يحتوي على عمود باسم 'عدد الافراد'. تأكد من كتابة الاسم بدقة.")
            
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

# تذييل الصفحة
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>تم التطوير للمساعدة في أعمال الخير</p>", unsafe_allow_html=True)
