document.getElementById('codeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const code = document.getElementById('code').value;
    
    const payload = {
        username: username,
        password: password,
        code: code
    };
    
    axios.post('<manage>/submission', payload)
        .then(response => {
            console.log('Success:', response);
            alert('Submission successful!');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Submission failed.');
        });
});

