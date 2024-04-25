document.addEventListener('DOMContentLoaded', function() {
    const createProjectBtn = document.getElementById('create-project-btn');

    createProjectBtn.addEventListener('click', function() {
        const projectName = document.getElementById('project-name').value;
        const contributors = Array.from(document.querySelectorAll('.contributor-input')).map(input => input.value);


        fetch('/create_project', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ projectName, contributors })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            alert("Project created successfully!")
        });
    });

    const addContributorBtn = document.getElementById('add-contributor-btn');

    addContributorBtn.addEventListener('click', function() {
        const contributorsContainer = document.querySelector('.contributors');
        const newContributorInput = document.createElement('input');
        newContributorInput.type = 'text';
        newContributorInput.classList.add('contributor-input');
        contributorsContainer.appendChild(newContributorInput);

        newContributorInput.style.marginBottom = '10px';
    });

    const showProjectsBtn = document.getElementById('show-projects-btn');

    showProjectsBtn.addEventListener('click', function() {
        window.location.href = '/view_projects';
    });
});
