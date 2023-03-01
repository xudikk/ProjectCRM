from django.db import models
from base.models import StatusModel
from company import Member
from . import PeriodType, PaymentChoice, PaymentType


class Course(StatusModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = "Kurslar"


class Schedule(StatusModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    free = models.BooleanField(default=False, null=False, )
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kundalik Grafik'
        verbose_name_plural = "Grafiklar"


class Group(StatusModel):
    name = models.CharField(max_length=120, blank=False, null=False)
    course = models.ForeignKey(Course, related_name='group_course', blank=True, null=True, on_delete=models.SET_NULL,
                               limit_choices_to={'active_status': 2}, )
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)
    schedule = models.ForeignKey(Schedule, related_name='group_schedule', blank=True, null=True,
                                 on_delete=models.SET_NULL)
    teacher_1 = models.ForeignKey(Member, related_name='O\'qituvchi', blank=False, null=False, on_delete=models.CASCADE,
                                  limit_choices_to={'is_student': False}, )
    teacher_2 = models.ForeignKey(Member, related_name='Assistent', blank=True, null=True, on_delete=models.SET_NULL,
                                  limit_choices_to={'is_student': False}, )
    period_type = models.IntegerField(blank=False, null=False, default=1, choices=PeriodType.CHOICES)
    price_month = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'O`quv Guruh'
        verbose_name_plural = 'Gruppalar'


class GroupStudent(StatusModel):
    student = models.ForeignKey(Member, related_name='group_student', blank=False, null=False,
                                on_delete=models.CASCADE, limit_choices_to={'is_student': True}, )
    group = models.ForeignKey(Group, related_name='groups', blank=False, null=False, on_delete=models.CASCADE)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('student', 'group'),)
        verbose_name = "Guruh Talabasi"
        verbose_name_plural = "Talabalar"

    def __str__(self):
        return f"{self.student}"


class GroupPeriod(models.Model):
    group = models.ForeignKey(Group, related_name='group_months', blank=False, null=False, on_delete=models.CASCADE)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    order_month = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('group', 'start_date', 'end_date'),)
        verbose_name = "Guruh Oyi"
        verbose_name_plural = "Oylar"

    def __str__(self):
        return f"{self.group_id} - {self.start_date}"


class GroupPayment(models.Model):
    period = models.ForeignKey(GroupPeriod, related_name='group_period', blank=False, null=False,
                               on_delete=models.CASCADE)
    student = models.ForeignKey(Member, related_name='group_payment_student', blank=False, null=False,
                                on_delete=models.CASCADE, limit_choices_to={'is_student': True}, )
    payment_date = models.DateField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    payment_type = models.IntegerField(blank=True, null=True, default=1, choices=PaymentType.CHOICES)
    status = models.IntegerField(blank=False, null=False, default=1, choices=PaymentChoice.STATUS_CHOICES)

    class Meta:
        unique_together = (('period', 'student'),)
        verbose_name = "Guruh To`lovlari"
        verbose_name_plural = "Oy to`lovi"

    def __str__(self):
        return f"{self.student_id} - {self.amount}"
