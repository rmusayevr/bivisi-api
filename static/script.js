// Connect to the WebSocket server
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNTQ5OTA4LCJpYXQiOjE3MjI5NDUxMDgsImp0aSI6ImVmN2FkYjQzZTc3YTQ0OTFhMmMyNmQyYzc2NGNiMmQ2IiwidXNlcl9pZCI6MiwidXNlcm5hbWUiOiJhZG1pbjEifQ.nIdg5EiF7xZpXbS4NTnYahCc97filKqJAM57Z5EGk_A';
const socket = new WebSocket(`wss://bivisibackend.store/ws/notifications/?token=${token}`); // Replace with your actual URL

// Function to handle WebSocket messages
function handleWebSocketMessage(event) {
    const data = JSON.parse(event.data);
    console.log('Message from server:', data);

    // Display the notification
    displayNotification(data);
}

// Function to display notifications in the UI
function displayNotification(data) {
    const { message, notification_type } = data;
    const notificationList = document.getElementById('notificationList');
    
    const listItem = document.createElement('li');
    listItem.textContent = `Type: ${notification_type}, Message: ${message}`;
    notificationList.appendChild(listItem);
}

// Event handlers for WebSocket
socket.onopen = function(event) {
    console.log('WebSocket is open now.');
};

socket.onmessage = handleWebSocketMessage;

socket.onerror = function(error) {
    console.error('WebSocket Error:', error);
};

socket.onclose = function(event) {
    console.log('WebSocket is closed now.');
};

// Function to send subscription request
function subscribeUser() {
    const userId = document.getElementById('userIdInput').value;
    if (userId) {
        // Send a subscription request to the server
        fetch(`https://bivisibackend.store/api/user/toggle_subscribe/${userId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(), // Ensure CSRF token is included if CSRF protection is enabled
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
                notification_type: 'Subscribe'
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Subscription response:', data);
            const testMessage = {
                message: 'Subscription test message',
                notification_type: 'Subscribe'
            };
            socket.send(JSON.stringify(testMessage));
        })
        .catch(error => {
            console.error('Subscription error:', error);
        });
    }
}

// Function to get CSRF token (for Django)
function getCsrfToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^;]*)/);
    return cookieValue ? cookieValue[1] : '';
}

// Attach event listener to the subscribe button
document.getElementById('subscribeButton').addEventListener('click', subscribeUser);
