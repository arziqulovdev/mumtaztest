# forms.py
from django import forms
from .models import Test

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'summary', 'public', 'time']
        labels = {
            'name': 'Test nomi',
            'summary': 'Qisqacha tavsif',
            'public': "Testni ommaga ko'rsatish",
            'time': 'Vaqt (soat)',
        }
        help_texts = {
            'name': 'Test nomini kiriting, 100 belgidan oshmasligi kerak.',
            'summary': 'Test haqida qisqacha tushuntirish (300 belgigacha).',
            'public': "Agar ushbu katakcha belgilanmagan bo'lsa, test faqat maxsus kod orqali kiriladi.",
            'time': 'Test uchun ajratilgan vaqtni kiriting (soatlarda).',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Matematika asoslari'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Test haqida qisqacha...'}),
            'public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Vaqtni kiriting'}),
        }
