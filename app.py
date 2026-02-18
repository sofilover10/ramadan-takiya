# --- 6. الفوتر المحدث (تصميم احترافي) ---
st.markdown("---")

footer_html = """
<style>
    /* حاوية الفوتر */
    .footer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* بطاقة المطور */
    .dev-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        text-align: center;
        width: 100%;
        max-width: 700px;
        border: 1px solid #eee;
    }
    
    .dev-title {
        color: #1e3c72;
        font-family: 'Cairo', sans-serif;
        font-weight: 700;
        margin-bottom: 5px;
        font-size: 1.3rem;
    }
    
    .dev-subtitle {
        color: #777;
        font-size: 0.9rem;
        margin-bottom: 25px;
    }
    
    /* أزرار التواصل */
    .contact-buttons {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .btn-contact {
        display: flex;
        align-items: center;
        padding: 12px 25px;
        border-radius: 50px;
        text-decoration: none !important;
        color: white !important;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .btn-contact:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    }
    
    .btn-whatsapp {
        background: linear-gradient(45deg, #25D366, #128C7E);
    }
    
    .btn-phone {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
    }
    
    .icon { margin-left: 10px; font-size: 1.2rem; }
</style>

<div class="footer-container">
    <div class="dev-card">
        <h3 class="dev-title">جميع الحقوق محفوظة للمطور: م. عبدالله حميد الصوفي © 2026</h3>
        <p class="dev-subtitle">تم التطوير لخدمة لجنة فش فرش الشمالي</p>
        
        <div class="contact-buttons">
            <a href="https://wa.me/972567100000" target="_blank" class="btn-contact btn-whatsapp">
                <span class="icon">💬</span> تواصل واتساب
            </a>
            
            <a href="tel:0567100000" class="btn-contact btn-phone">
                <span class="icon">📞</span> اتصال هاتفي
            </a>
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
