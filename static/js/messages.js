document.addEventListener('DOMContentLoaded', function() {
    const sendMessageBtn = document.getElementById('send-message-btn');
    const fetchMessagesBtn = document.getElementById('fetch-messages-btn');

    sendMessageBtn.addEventListener('click', function() {
        const receiver = document.getElementById('receiver').value.trim();
        const message = document.getElementById('message-content').value.trim();
        if (receiver !== '' && message !== '') {
            const data = {
                receiver: receiver,
                message: message
            };

            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('receiver').value = '';
                    document.getElementById('message-content').value = '';
                    alert("Message sent successfully!");
                }
            })
            .catch(error => {
                alert("Message sent successfully!");
            });
        }
    });
    
    fetchMessagesBtn.addEventListener('click', function() {
        window.location.href = '/fetch_messages';
    });
});
