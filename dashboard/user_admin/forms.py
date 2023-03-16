from django import forms

from dashboard.models.extra import Member


class MemberChangeForm(forms.ModelForm):
    is_student = forms.ChoiceField(choices=[
        (True, "Student"),
        (False, "Student Emas")
    ], label="Studentlik Holati")

    def save(self, commit=True):
        all_value = self.cleaned_data
        self.instance.is_student = True if all_value['is_student'] == 'True' else False
        instance = super().save(commit=commit)
        return instance

    class Meta:
        model = Member
        # fields = '__all__'
        fields = ['pass_serial', 'position', 'is_student']
        labels = {
            "is_student": "Studentlik Holati",
            "position": "Lavozimi",
            "pass_serial": "PassPort Seriyasi",
        }
