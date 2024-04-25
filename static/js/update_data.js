document.addEventListener('DOMContentLoaded', function() {
    const saveBtn = document.getElementById('save-profile-btn');

    saveBtn.addEventListener('click', function() {
        const name = document.getElementById('name').value;
        const age = document.getElementById('age').value;
        const location = document.getElementById('location').value;
        const birthday = document.getElementById('birthday').value;
        const summary = document.getElementById('summary').value;

        const data = {
            name: name,
            age: age,
            location: location,
            birthday: birthday,
            summary: summary
        };

        fetch('/update_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                alert("Profile updated succesfully!");
            } else {
                alert("Profile update failed.");
            }
        })
        .catch(error => {
            alert("Profile update failed.");
        });
    });
});
