import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def send_notification(title, body, token):
    """
    Send a notification using Firebase Cloud Messaging.
    """
    try:
        notification = messaging.Notification(
            title=title,
            body=body
        )
        
        apns_config = messaging.APNSConfig(
            headers={
                "apns-priority": "10"
            },
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound='default',
                ),
            ),
        )

        android_notification = messaging.AndroidNotification(
            sound="default",
            channel_id="high_importance_channel"
        )
        android_config = messaging.AndroidConfig(
            notification=android_notification,
            priority="high"
        )

        message = messaging.Message(
            notification=notification,
            token=token,
            apns=apns_config,
            android=android_config
        )

        response = messaging.send(message)
        return {"success": True, "response": response}

    except FirebaseError as e:
        return {"success": False, "error": str(e)}

    except Exception as e:
        return {"success": False, "error": str(e)}
