from django import forms
from django.forms import DateInput, TimeInput

from base import GenderChoice
from dashboard.models.extra import Position, Member
from geo.models import District


class DatePicker(DateInput):
    template_name = "widgets/datepicker.html"


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'status']
        labels = {
            "title": 'Название',
            "status": 'Статус',
        }


class EmployeeForm(forms.ModelForm):
    gender = forms.ChoiceField(required=True, label='Jins', choices=GenderChoice.CHOICES)

    birthday = forms.DateField(
        help_text="Tug'ilgan kuni",
        required=True,
        label="Tug'ilgan kuni",
        widget=DatePicker,
    )

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        self.fields['region'].initial = None
        self.fields['district'].queryset = self.district_queryset()

    def district_queryset(self):
        if self.instance.pk is None:
            return District.objects.all()

        print(self.instance.region_id)
        return District.objects.filter(region_id=self.instance.region_id)

    def save(self, commit=True):
        all_value = self.cleaned_data
        self.instance.gender = True if all_value['gender'] == 1 else False
        instance = super().save(commit=commit)
        return instance

    class Meta:
        model = Member
        fields = '__all__'
        # exclude = ['join_date', 'is_student']
        labels = {
            "firstname": "Ism",
            "lastname": "Familiya",
            "middlename": "Otasini ismi",
            "birthday": "Tug‘ilgan kun",
            "gender": "Jisni",
            "address": "Manzil",
            "pass_serial": "Passport ma'lumoti",
            "position": "Lavozim",
            "region": "Viloyat/shahar",
            "district": "Tuman",
        }


class StudentForm(forms.ModelForm):
    gender = forms.ChoiceField(required=True, label='Jins', choices=[
        (True, "Erkak"),
        (False, "Ayol"),
    ])
    nickname = forms.SlugField(required=False, label='Nick name')

    birthday = forms.DateField(
        help_text="YYYY-MM-DD",
        required=True,
        label="Tug'ilgan kuni",
        widget=DatePicker,
    )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields['region'].initial = None
        self.fields['district'].queryset = self.district_queryset()
        self.fields['nickname'].initial = self.get_nick()

    def district_queryset(self):
        if self.instance.pk is None:
            return District.objects.all()

        return District.objects.filter(region_id=self.instance.region_id)

    def get_nick(self):
        if self.instance.pk is None:
            return None

        return self.instance.user.nickname

    def save(self, commit=True):
        all_value = self.cleaned_data
        print(type(all_value['gender']))
        self.instance.gender = True if all_value['gender'] == 'True' else False
        instance = super().save(commit=commit)
        return instance

    class Meta:
        model = Member
        # fields = '__all__'
        exclude = ['position', 'is_student']
        labels = {
            "firstname": "Ism",
            "lastname": "Familiya",
            "middlename": "Otasini ismi",
            "birthday": "Tug‘ilgan kun",
            "gender": "Jisni",
            "pass_serial": "Passport ma'lumoti",
            "region": "Viloyat/shahar",
            "district": "Tuman",
        }
