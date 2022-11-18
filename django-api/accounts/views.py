from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from .models import OTPRequest


class OTPView(APIView):
    """
    User Sends A Request For Sign In, And Generate OTP, The Request Must Include:
      1- receiver : phone number or email address for receiving OTP
      2- channel : sign in method(phone or Email)
    """
    def get(self, request):
        """Validating User Request Information For Generate OTP With Phone Or Email"""
        serializer = serializers.UserRequestOtpGenerateSerializer(data=request.query_params)
        if serializer.is_valid():
            user_otp_request_info: dict = serializer.validated_data
            try:
                """
                Pass User's Data To OTP Handler For:
                 1- Create OTP
                 2- Save Generated Password With Request ID And Receiver(Phone Or Email) In DB
                 3- Send OTP For User To Sign In With It
                """
                created_otp_info: OTPRequest = OTPRequest.objects.otp_request_handler(user_otp_request_info)
                return Response(data=serializers.OtpGenerateResponseSerializer(created_otp_info).data, status=status.HTTP_200_OK)
            except Exception as error:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=error)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self, request):
        """
        User Has Received OTP With Email Or Phone Now User Have To
        Send Verification Information Of OTP That Should Contain
        These Information In Request Body:
          1- receiver : phone number or email address that was entered in OTP generate stage
          2- request_id : was sent in response of OTP generate stage
          3- password : OTP that was generate sent to phone or mail of user in OTP generate stage
        """
        serializer = serializers.UserRequestOtpVerifySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            """If OTP Exist On DB And Not Been Expired"""
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                """Check User Is New User And Want Signup  Or Is Not New User And Want To Login"""
                User = get_user_model()
                query = User.objects.filter(username=data['receiver'])

                if query.exists():
                    """Is Not New User --> Just Send Authentication Token """
                    joined: bool = False
                    user = query.first()
                else:
                    """Is New User --> Create New User And Then Send Authentication Token """
                    joined: bool = True
                    user = User.objects.create(username=data['receiver'])

                refresh = RefreshToken.for_user(user)

                login_data = serializers.OtpVerifyResponseSerializer({
                    'refresh': str(refresh),
                    'token': str(refresh.access_token),
                    'joined': joined
                }).data

                return Response(
                    data=login_data,
                    status=status.HTTP_200_OK
                )

            else:
                """If OTP Not Exist On DB Or Has Been Expired --> Raise Error"""
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={"message": "OTP Has Expired Or IS Not Correct"})

        else:
            """If Information For OTP Verify Was Not Valid"""
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)