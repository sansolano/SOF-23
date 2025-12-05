
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const alertBox = document.getElementById('alert');
    const btnLogin = document.getElementById('btnLogin');

    btnLogin.disabled = true;
    btnLogin.textContent = 'Iniciando sesión...';

    try {
        const response = await fetch(`http://localhost:3000/login/${email}/${password}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.status === "success") {
            localStorage.setItem('user', email);

            alertBox.className = 'alert alert-success';
            alertBox.textContent = data.message;
            alertBox.style.display = 'block';

            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        alertBox.className = 'alert alert-error';
        alertBox.textContent = error.message;
        alertBox.style.display = 'block';

        btnLogin.disabled = false;
        btnLogin.textContent = 'Ingresar';
    }
});

document.getElementById('registerLink').addEventListener('click', async (e) => {
    e.preventDefault();

    const email = prompt("Ingresa tu usuario/correo:");
    const password = prompt("Ingresa tu contraseña:");

    if (!email || !password) return;

    try {
        const response = await fetch(`http://localhost:3000/register/${email}/${password}`, {
            method: 'PUT'
        });

        const data = await response.json();

        if (data.status === "success") {
            alert("Registro exitoso. Ahora puedes iniciar sesión.");
        } else {
            alert("Error: " + data.message);
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
});