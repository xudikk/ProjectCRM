from django import forms

from dashboard.models.extra import Interested


class EnrollForm(forms.ModelForm):
    class Meta:
        model = Interested
        # fields = '__all__'
        exclude = ['view', 'contacted']
        labels = {
            "name": "To'lliq ism Familiyangiz",
            "phone": "Telefon raqam",
            "telegram": "Telegram username",
            "extra_contact": "Qo'shimcha bog'lanish uchun manba",
            'additional': "Qiziqishingiz haqida qisqacha"
        }