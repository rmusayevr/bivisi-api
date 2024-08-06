import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def send_notification(title, body, token):
    """
    Send a notification using Firebase Cloud Messaging.

    :param title: Title of the notification
    :param body: Body text of the notification
    :param data: Additional data payload as a dictionary
    :param tokens: List of device tokens to send the notification to
    """
    try:
        # Create the notification message
        notification = messaging.Notification(
            title=title,
            body=body
        )

        # Create APNs config with default sound
        apns_config = messaging.APNSConfig(
            aps=messaging.Aps(
                sound='default'
            )
        )

        # Create Android config with high priority and default sound
        android_notification = messaging.AndroidNotification(
            sound='default',
            channel_id='high_importance_channel'
        )
        android_config = messaging.AndroidConfig(
            notification=android_notification,
            priority='high'
        )

        # Build the message
        message = messaging.Message(
            notification=notification,
            token=token,
            apns=apns_config,
            android=android_config
        )

        # Send the message
        response = messaging.send(message)
        result = {'success': True, 'response': response}
        return result

    except FirebaseError as e:
        # Handle Firebase-specific errors
        return {'success': False, 'error': str(e)}

    except Exception as e:
        # Handle other unexpected errors
        return {'success': False, 'error': str(e)}
