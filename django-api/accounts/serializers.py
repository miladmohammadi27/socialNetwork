from rest_framework import serializers
from .models import OTPRequest

"""Validate OTP Generate Request Information When User Enters His Phone Number Or Email To Sign In"""
class UserRequestOtpGenerateSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False, choices=OTPRequest.OTPChannelChoices.choices)


"""Validate OTP Generate Response"""
class OtpGenerateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['request_id']


"""Validate OTP Verify Request Information When User has Received The OTP And Want To Sign In"""
class UserRequestOtpVerifySerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=64, allow_null=False)
    password = serializers.CharField(max_length=5, allow_null=False)
    receiver = serializers.CharField(max_length=100, allow_null=False)


"""Validate OTP Verify Response To User"""
class OtpVerifyResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
    joined = serializers.BooleanField()