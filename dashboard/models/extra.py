from django.db import models
from django.utils import timezone

from base.models import StatusModel
from dashboard import PositionChoice, MemberChoice
from geo.models import Region, District
from user.models import User


class Otp(models.Model):
    key = models.CharField(max_length=512)
    mobile = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)
    extra = models.JSONField(default={})
    is_verified = models.BooleanField(default=False)
    step = models.CharField(max_length=25)
    by = models.IntegerField(choices=[
        (1, "By Register"),
        (2, "By Login"),
    ])

    created = models.DateTimeField(auto_now=False, default=timezone.now, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        if self.tries >= 3:
            self.is_expired = True
        return super(Otp, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.key}-{self.mobile}"


class Position(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    status = models.SmallIntegerField(choices=PositionChoice.STATUS_CHOICES, default=2, null=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"


class Member(models.Model):
    firstname = models.CharField(max_length=30, blank=False, null=False)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    middlename = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    birthday = models.DateField(auto_now=False)
    gender = models.BooleanField(verbose_name="Jinsi", default=True, null=False, choices=[
        (True, "Erkak"),
        (False, "Ayol"),
    ])
    is_student = models.BooleanField(default=True, null=False, )

    join_date = models.DateField(auto_now=False, auto_now_add=True, blank=False, null=False)
    pass_serial = models.CharField(max_length=30, blank=True, null=True)
    position = models.ForeignKey(Position, related_name='position', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.SmallIntegerField(choices=MemberChoice.STATUS_CHOICES, default=2, null=False, blank=True)
    permission = models.SmallIntegerField(choices=[
        (0, "Yangi qo'shilgan"),
        (1, "O'quvchi"),
        (2, "Mentor"),
        (3, "Admin"),
    ], default=0, null=True, blank=True)
    region = models.ForeignKey(Region, related_name='member_region', null=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(District, related_name='member_district', null=True,
                                 on_delete=models.SET_NULL)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = 'Xodim va a`zo'
        verbose_name_plural = "Xodimlar va A`zolar"


class Profile(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False, )
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    description = models.CharField(max_length=800, blank=True, null=True, )
    phone_number = models.CharField(max_length=20, blank=True, null=True, )
    logo = models.ImageField(upload_to="logos", blank=True, null=True)
    lat = models.DecimalField("Latitude", max_digits=18, decimal_places=12, blank=True, null=True)
    lng = models.DecimalField("Longitude", max_digits=18, decimal_places=12, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True, )
    region = models.ForeignKey(
        Region, related_name='company_region', null=True, blank=True,
        on_delete=models.SET_NULL)

    district = models.ForeignKey(
        District, related_name='company_district', null=True, blank=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.title


class Course(models.Model):
    name = models.CharField("Kurs Turi", max_length=50, null=False, blank=False)
    mentor = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="course_mentor",
                               limit_choices_to={'is_student': False}
                               )

    def __str__(self):
        return f"{self.name} | Mentor: {self.mentor} "

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "Courses"


class Group(models.Model):
    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="course")
    duration = models.CharField("Kurs Davomiyligi", max_length=128, default="6 oy")
    status = models.SmallIntegerField(default=0, choices=[
        (1, "Boshlanmoqda"),
        (2, "Davom Qilyabdi"),
        (3, "Guruh Yopilgan"),
    ])

    def __str__(self):
        return f"Name : {self.name} | Course: {self.course} | Duration: {self.duration}"


class GroupStudent(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True,
                                limit_choices_to={"is_student": True})
    start_date = models.DateField(verbose_name="O'quvchi guruhga qo'shilgan sana", blank=False, null=False)
    end_date = models.DateField(verbose_name="O'quvchi guruhdan chiqqan sana", blank=True, null=True)

    class Meta:
        unique_together = (('student', 'group'),)
        verbose_name = "Guruh Talabasi"
        verbose_name_plural = "Talabalar"

    def __str__(self):
        return f"{self.student}"


class Interested(models.Model):
    name = models.CharField(verbose_name="Ism Familiya", max_length=128, null=False, blank=False)
    phone = models.CharField("Telefon raqam", max_length=20, null=False, blank=False)
    telegram = models.CharField("Telegram username", null=True, blank=True, max_length=70)
    extra_contact = models.CharField("Qo'shimcha Contact", null=True, blank=True, max_length=256)
    additional = models.TextField("Qiziqishingiz haqida qisqacha", null=True, blank=True)
    view = models.BooleanField(default=False)
    contacted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Yangi Yozilmoqchi"
        verbose_name_plural = "Kursga Yozilmoqchi bo'lganlar"

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.contacted} "


