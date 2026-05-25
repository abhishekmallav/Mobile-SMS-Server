from jnius import autoclass

def send_sms_message(phone_number, message):
    try:
        # Load the Android SmsManager
        SmsManager = autoclass('android.telephony.SmsManager')
        sms_manager = SmsManager.getDefault()
        
        # Send the SMS (destination, scAddress, text, sentIntent, deliveryIntent)
        sms_manager.sendTextMessage(phone_number, None, message, None, None)
        return True, "SMS sent successfully"
    except Exception as e:
        return False, str(e)
