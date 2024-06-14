document.getElementById('submissionForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const code = document.getElementById('code').value;

    try {
        const response = await axios.post('http://127.0.0.1:8000/submission', {
            username: username,
            password: password,
            code: code
        });

        if (response.status === 200) {
            alert('Code submitted successfully. Reservation ID: ' + response.data.id);
        }
    } catch (error) {
        console.error('Error submitting code:', error);
        alert('Error submitting code. Please try again.');
    }
});

