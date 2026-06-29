// Register JS
const registerForm = document.getElementById('registerForm');

if (registerForm) {
    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        if (data.password !== data.password2) {
            alert("Passwords do not match");
            return;
        }

        const payload = {
            email: data.email,
            username: data.username,
            first_name: data.first_name,
            last_name: data.last_name,
            role: data.role,
            phone_number: data.phone_number,
            password: data.password
        };

        try {
            const response = await fetch('/auth/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                alert("Registration successful!");
                window.location.href = '/auth/login-page';
            } else {
                const errorData = await response.json();
                alert(errorData.detail || "Registration failed");
            }
        } catch (error) {
            console.error(error);
            alert("An error occurred while registering.");
        }
    });
}