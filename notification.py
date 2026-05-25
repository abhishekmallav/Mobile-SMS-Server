from kivy.utils import platform

def show_server_notification(ip_text):
    if platform != 'android':
        return
    try:
        from jnius import autoclass, cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Context = autoclass('android.content.Context')
        Intent = autoclass('android.content.Intent')
        PendingIntent = autoclass('android.app.PendingIntent')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        BuildVERSION = autoclass('android.os.Build$VERSION')
        String = autoclass('java.lang.String')
        
        context = PythonActivity.mActivity.getApplicationContext()
        notification_manager = cast(
            'android.app.NotificationManager',
            context.getSystemService(Context.NOTIFICATION_SERVICE)
        )

        channel_id = String('sms_server_channel')
        
        if BuildVERSION.SDK_INT >= 26:
            channelName = String('SMS Server Status')
            channel = NotificationChannel(
                channel_id,
                channelName,
                NotificationManager.IMPORTANCE_LOW
            )
            notification_manager.createNotificationChannel(channel)

        intent = Intent(context, PythonActivity)
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP)
        
        # FLAG_IMMUTABLE is required for Android 12+ (API 31)
        FLAG_IMMUTABLE = 67108864 # PendingIntent.FLAG_IMMUTABLE
        pending_intent = PendingIntent.getActivity(
            context, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT | FLAG_IMMUTABLE
        )

        builder = NotificationBuilder(context)
        if BuildVERSION.SDK_INT >= 26:
            builder = NotificationBuilder(context, channel_id)

        icon_id = context.getApplicationInfo().icon
        
        builder.setContentTitle(String("Server is running"))
        builder.setContentText(String(ip_text))
        builder.setContentIntent(pending_intent)
        builder.setSmallIcon(icon_id)
        builder.setOngoing(True)

        notification = builder.build()
        notification_manager.notify(1, notification)
    except Exception as e:
        print(f"Notification Error: {e}")

def hide_server_notification():
    if platform != 'android':
        return
    try:
        from jnius import autoclass, cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Context = autoclass('android.content.Context')
        context = PythonActivity.mActivity.getApplicationContext()
        notification_manager = cast(
            'android.app.NotificationManager',
            context.getSystemService(Context.NOTIFICATION_SERVICE)
        )
        notification_manager.cancel(1)
    except Exception as e:
        print(f"Cancel Notification Error: {e}")