from random import randint

"""
This Class Handles The OTP Send For Login Or Signup Based On Preferred Login Method(Phone or Email)
"""
class OTPSendHandler:
    def __init__(self, otp_password, otp_receiver, otp_channel):
        self.otp_password = otp_password
        self.otp_receiver = otp_receiver
        self.otp_channel = otp_channel

    def __send_otp_sms(self):
        print('[!!!!!!!!!!!!!!]Sending SMS To {} : Your Password Is {}'.format(self.otp_receiver, self.otp_password))

    def __send_otp_email(self):
        print('[!!!!!!!!!!!!!!]Sending Email To {} : Your Password Is {}'.format(self.otp_receiver, self.otp_password))

    def send_otp(self):
        if self.otp_channel == 'phone':
            self.__send_otp_sms()

        if self.otp_channel == 'email':
            self.__send_otp_email()

    @staticmethod
    def generate_otp():
        return randint(10000, 99999)