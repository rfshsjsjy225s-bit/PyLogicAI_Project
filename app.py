from flask import Flask, render_template, request, jsonify, session
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # لتأمين الجلسات

# تحميل ملف الترجمة
with open('translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

def get_language():
    """تحديد اللغة حسب الجلسة أو المتصفح"""
    if 'lang' in session:
        return session['lang']
    # قراءة لغة المتصفح (ar أو en)
    browser_lang = request.accept_languages.best_match(['ar', 'en'])
    return browser_lang if browser_lang else 'ar'

@app.route('/')
def index():
    lang = get_language()
    return render_template('index.html', t=translations[lang], lang=lang)

@app.route('/set-language/<lang>')
def set_language(lang):
    if lang in ['ar', 'en']:
        session['lang'] = lang
    return jsonify({'status': 'ok'})

# نقطة نهاية API لعرض بيانات الوكالة
@app.route('/api/agency-info')
def agency_info():
    info = {
        "name": "PyLogic AI",
        "slogan": "حيث يلتقي منطق الأكواد بسحر الذكاء",
        "founded": 2025,
        "technologies": ["Python", "Flask", "FastAPI", "TensorFlow", "PyTorch"],
        "services": ["AI-Powered Development", "Full-Stack Solutions", "High-End UI/UX", "Strategic SEO"]
    }
    return jsonify(info)

# نقطة نهاية لتلقي استفسارات العملاء
@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    inquiries_file = 'inquiries.json'
    inquiry = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "email": email,
        "message": message
    }
    try:
        if os.path.exists(inquiries_file):
            with open(inquiries_file, 'r') as f:
                inquiries = json.load(f)
        else:
            inquiries = []
        inquiries.append(inquiry)
        with open(inquiries_file, 'w') as f:
            json.dump(inquiries, f, indent=4, ensure_ascii=False)
        return jsonify({"status": "success", "message": "تم استلام طلبك بنجاح" if get_language() == 'ar' else "Your request has been received"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    from flask import send_from_directory

@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.root_path, 'sitemap.xml')
    app.run(debug=True)