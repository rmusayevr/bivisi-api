import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def send_notification(title, body, data, tokens):
    """
    Send a notification using Firebase Cloud Messaging.

    :param title: Title of the notification
    :param body: Body text of the notification
    :param data: Additional data payload as a dictionary
    :param tokens: List of device tokens to send the notification to
    """
    try:
        # Create the notification message
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,  # Optional additional data as a dictionary
            tokens=tokens,  # List of device tokens
        )

        # Send the message to the specified devices
        response = messaging.send_multicast(message)

        # Log the result
        print(f"Successfully sent message: {response.success_count} messages were sent successfully")
        if response.failure_count > 0:
            print(f"Failed to send {response.failure_count} messages")
            for error in response.responses:
                if not error.success:
                    print(f"Error sending message: {error.exception}")
    except Exception as e:
        print(f"Error sending notification: {e}")
