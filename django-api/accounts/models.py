from django.db import models
from uuid import uuid4
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils import timezone
from .OTPSender import OTPSendHandler
from django.db.models.signals import post_save
from mongoDBMS.dbms import ProfileDBMS


"""Override User Class For Add Some Needed Data"""
class User(AbstractUser):
    profile_id = models.CharField(max_length=100, verbose_name='Profile Data Stored In Mongo', null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True, verbose_name='Nationality')


"""
pre save method for create profile document in mongo db
"""
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        """create profile for created user in mongoDB"""
        ProfileDBMS().create_profile(instance)


"""
Override Queryset And Add 'is_valid' Function 
If The Request For OTP Exists And No More Than 2 Minutes Passed is_valid Returns True
"""
class OTPRequestQuerySet(models.QuerySet):
    def is_valid(self, receiver, request_id, password):
        current_time = timezone.now()
        return self.filter(
            receiver=receiver,
            request_id=request_id,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120)
        ).exists()


"""Override Model Manager To Add Some Functions For Model"""
class OTPRequestManager(models.Manager):

    def get_queryset(self):
        return OTPRequestQuerySet(self.model, self._db)

    """If The Request For OTP Exists And No More Than 2 Minutes Passed 'is_valid' Returns True"""
    def is_valid(self, receiver, request_id, password):
        return self.get_queryset().is_valid(receiver, request_id, password)

    """Save OTP Request To DB And Getting Ready OTP Data And Generated OTP Password For Sending To User"""
    def otp_request_handler(self, data):
        otp = self.model(channel=data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        self.__send_otp(otp)
        return otp

    """Pass Created OTP Data For Sending To User"""
    @staticmethod
    def __send_otp(otp):
        OTPSendHandler(otp.password, otp.receiver, otp.channel).send_otp()


"""OTP Requests Table For Saving OTP Requests For Login Or Signup"""
class OTPRequest(models.Model):

    class OTPChannelChoices(models.TextChoices):
        PHONE = 'phone'
        EMAIL = 'email'

    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid4, verbose_name='OTP Request ID')
    channel = models.CharField(max_length=10, choices=OTPChannelChoices.choices, default=OTPChannelChoices.PHONE, verbose_name='Sign in Method')
    receiver = models.CharField(max_length=50, verbose_name='OTP Password Receiver')
    password = models.CharField(max_length=5, default=OTPSendHandler.generate_otp, verbose_name='OTP Password')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='OTP Request Creating Time')

    objects = OTPRequestManager()


