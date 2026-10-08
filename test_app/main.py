from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import json, os

class MyApp(App):
    def build(self):
        # مسار حفظ آمن ومستقل متوافق تماماً مع الـ APK للأندرويد
        self.FILE = os.path.join(self.user_data_dir, "accounts.json")
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.layout.add_widget(Label(text='مدير حساباتي الآمن', font_size=24, size_hint_y=None, height=40))
        
        self.app_name = TextInput(multiline=False, hint_text="اسم التطبيق (مثال: Facebook)")
        self.layout.add_widget(self.app_name)
        
        self.username = TextInput(multiline=False, hint_text="اسم المستخدم أو الإيميل")
        self.layout.add_widget(self.username)
        
        self.password = TextInput(multiline=False, password=True, hint_text="كلمة المرور")
        self.layout.add_widget(self.password)
        
        self.btn_save = Button(text='حفظ الحساب الجديد', background_color=(0, 0.7, 0, 1), size_hint_y=None, height=50)
        self.btn_save.bind(on_press=self.save_account)
        self.layout.add_widget(self.btn_save)
        
        self.layout.add_widget(Label(text='--- البحث عن حساب ---', size_hint_y=None, height=30))
        
        self.search_input = TextInput(multiline=False, hint_text="أدخل اسم التطبيق للبحث عنه")
        self.layout.add_widget(self.search_input)
        
        self.btn_search = Button(text='عرض بيانات الحساب', background_color=(0, 0.5, 1, 1), size_hint_y=None, height=50)
        self.btn_search.bind(on_press=self.search_account)
        self.layout.add_widget(self.btn_search)
        
        self.status_label = Label(text='مرحباً بك', font_size=16, color=(1, 1, 0, 1))
        self.layout.add_widget(self.status_label)
        
        return self.layout

    def save_account(self, instance):
        app = self.app_name.text.strip()
        user = self.username.text.strip()
        pwd = self.password.text.strip()
        
        if not app or not user or not pwd:
            self.status_label.text = "خطأ: يرجى ملء جميع الحقول!"
            return
            
        new_data = {app: {"username": user, "password": pwd}}
        
        if os.path.exists(self.FILE):
            try:
                with open(self.FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except:
                data = {}
        else:
            data = {}
            
        data.update(new_data)
        
        try:
            with open(self.FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.status_label.text = f"تم حفظ حساب {app} بنجاح!"
            self.app_name.text = ""
            self.username.text = ""
            self.password.text = ""
        except:
            self.status_label.text = "فشل الحفظ في ذاكرة التطبيق"

    def search_account(self, instance):
        query = self.search_input.text.strip()
        if not query:
            self.status_label.text = "يرجى كتابة اسم التطبيق للبحث!"
            return
            
        if os.path.exists(self.FILE):
            try:
                with open(self.FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if query in data:
                    user = data[query]["username"]
                    pwd = data[query]["password"]
                    self.status_label.text = f"الحساب: {user}\nكلمة المرور: {pwd}"
                else:
                    self.status_label.text = f"لم يتم العثور على حساب باسم '{query}'"
            except:
                self.status_label.text = "خطأ في قراءة ملف الحسابات"
        else:
            self.status_label.text = "لا يوجد أي حسابات محفوظة بعد!"

if __name__ == '__main__':
    MyApp().run()
