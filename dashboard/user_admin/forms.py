from django import forms

from dashboard.models.extra import Member, Course, Group, GroupStudent
from dashboard.student.forms import DatePicker


class MemberChangeForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[
        (1, 'Chiqib ketgan'),
        (2, 'Faol'),
        (3, 'Mavjud emas'),
        (4, 'Yangi qo`shilmoqchi')
    ], label="Studentlik Holati")
    permission = forms.ChoiceField(choices=[
        (0, "Yangi qo'shilgan"),
        (1, "O'quvchi"),
        (2, "Mentor"),
    ], label="A'zoning ruxsatlari")

    def __init__(self, *args, **kwargs):
        super(MemberChangeForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['permission'].initial = self.instance.permission
            self.fields['status'].initial = self.instance.status

    def save(self, commit=True):
        all_value = self.cleaned_data
        self.instance.status = 1 if all_value['status'] == '1' else 2 if all_value['status'] == '2' else 3 if all_value[
                                                                                                                  'status'] == '3' else 4
        self.instance.permission = 1 if all_value['permission'] == '1' else 2 if all_value['permission'] == '2' else 0
        instance = super().save(commit=commit)
        return instance

    class Meta:
        model = Member
        # fields = '__all__'
        fields = ['position', 'is_student']
        labels = {
            "status": "Holati",
            "position": "Lavozimi",
            "permission": "A'zoning ruxsatlari",
        }


class GrStForm(forms.ModelForm):
    start_date = forms.DateField(
        required=True,
        label="O\'uqvchi qachondan qo\'shildi",
        widget=DatePicker,
    )

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group')
        super().__init__(*args, **kwargs)
        self.fields['group'].initial = group

    class Meta:
        model = GroupStudent
        fields = '__all__'
        labels = {
            "group": "Guruhni tanlang",
            "student": 'O\'quvchini tanlang',
            "start_date": 'O\'uqvchi qachondan qo\'shildi',
        }

    def save(self, commit=True):
        instance = super(GrStForm, self).save(commit=commit)
        return instance


class PasswordForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=Member.objects.filter(is_student=True),
        label="Kerakli Foydalanuchini tanlang",
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Yangi parolni kiriting",
        required=True
    )
    re_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Parolni boshqatdan kiriting",
        required=True
    )


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

        labels = {
            "name": "Kurs Nomi",
            "mentor": "Kursi o'tuvchi Mentor",
        }
