var loginForm = document.getElementById('loginForm');

loginForm.onsubmit = function (event) {
    /*event se refiere al evento que estoy escuchando*/ 
    event.preventDefault(); //Previene el comportamineto por default de mi formulario

    //obtener los datos del formulario

    var formulario = new FormData(loginForm);
    /*formulario = diccionario : {
        "email": "elena@detroya.com",
        "password": 1234    }*/

    fetch('/login', {method:'POST', body: formulario})
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data.message == 'correcto'){
            window.location.href = "/dashboard";
        } else {
            var mensajeAlerta = document.getElementById('mensajeAlerta');
            mensajeAlerta.innerHTML = data.message;

            //formato de alerta con colores
            mensajeAlerta.classList.add('alert');
            mensajeAlerta.classList.add('alert-danger')
        }
    })

}