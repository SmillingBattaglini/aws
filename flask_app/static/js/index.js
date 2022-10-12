var loginForm = document.getElementById('loginForm');

loginForm.onsubmit = function (event) {
    /* event se refiere al evento que estoy escuchando */
    event.preventDefault(); //Previene el comportamiento por default de mi formulario

    //Obtener los datos del formulario
    var formulario = new FormData(loginForm);
    /*formulario = {
        "email": "elena@codingdojo.com",
        "password": "1234"
    }*/

    fetch('/login', { method: 'POST', body: formulario })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.message == 'correcto') {
                //Todo está correcto y me redirige a dashboard
                window.location.href = "/dashboard";
            } else {
                // var mensajeAlerta = document.getElementById('mensajeAlerta');
                // mensajeAlerta.innerHTML = data.message;

                // //Formato de alerta con colores
                // mensajeAlerta.classList.add('alert');
                // mensajeAlerta.classList.add('alert-danger');
                alert(data.message)
            }
        })
    }