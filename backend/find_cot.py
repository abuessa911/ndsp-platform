import os

KEYWORDS = ["cftc", "cot", "quandl", "read_csv", "fetch_cot", "cot_snapshot"]
IGNORE_DIRS = {'node_modules', 'venv', '.venv', '.git', '__pycache__'}

def search_files(root_dir):
    print("🔍 جاري البحث عن ملفات تغذية بيانات COT...")
    found = []
    for d, dirs, files in os.walk(root_dir):
        dirs[:] = [dir for dir in dirs if dir not in IGNORE_DIRS]
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(d, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read().lower()
                        matches = [k for k in KEYWORDS if k in content]
                        if matches: 
                            found.append((path, matches))
                except: pass
    
    if found:
        print("\n✅ تم العثور على الملفات التالية:")
        for p, m in found: 
            print(f"📁 المسار: {p} | الكلمات الدليلية: {', '.join(m)}")
        print("\n💡 يرجى تزويدي بمحتوى الملف الذي يبدو أنه المزود الرئيسي (مثلاً tdl_data_provider أو ما شابه).")
    else:
        print("\n❌ لم يتم العثور على ملفات سحب بيانات COT في هذا المجلد.")

search_files('.')
