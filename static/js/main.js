function generarMatrices(){

    let tam = document.getElementById("tamMatriz").value;
    tam = parseInt(tam);

    localStorage.setItem("tamMatriz", tam);

    let estado = document.getElementById("estadoBox");

    if(isNaN(tam) || tam < 2 || tam > 12){

        estado.className = "estadoBox estadoError";
        estado.innerHTML = '<i class="bi bi-x-circle"></i> El tamaño debe estar entre 2 y 12.';

        return;
    }

    crearTabla("tablaFlujo", "flujo", tam);
    crearTabla("tablaDistancia", "distancia", tam);

    document.getElementById("matricesArea").classList.remove("d-none");

    estado.className = "estadoBox estadoCorrecto";
    estado.innerHTML = '<i class="bi bi-check-circle"></i> Matrices generadas correctamente. Completa los valores faltantes.';
}


function crearTabla(contenedor, tipo, tam){

    let caja = document.getElementById(contenedor);

    let texto = "";

    texto += '<table class="matrix-table">';

    texto += '<thead>';

    texto += '<tr>';

    texto += '<th></th>';

    for(let j = 1; j <= tam; j++){

        texto += `<th>${j}</th>`;

    }

    texto += '</tr>';

    texto += '</thead>';

    texto += '<tbody>';

    for(let i = 1; i <= tam; i++){

        texto += '<tr>';

        texto += `<th>${i}</th>`;

        for(let j = 1; j <= tam; j++){

            if(i == j){

                texto += `
                    <td>
                        <input type="text" value="0" class="matrix-input matrix-diagonal" disabled>
                    </td>
                `;

            }else{

                texto += `
                    <td>
                        <input type="text" class="matrix-input" data-tipo="${tipo}" oninput="validarCelda(this)">
                    </td>
                `;

            }

        }

        texto += '</tr>';

    }

    texto += '</tbody>';

    texto += '</table>';

    caja.innerHTML = texto;
}


function validarCelda(campo){

    let valor = campo.value.trim();

    if(valor === ""){

        campo.classList.remove("matrix-invalid");
        return;

    }

    if(isNaN(valor) || Number(valor) < 0){

        campo.classList.add("matrix-invalid");

    }else{

        campo.classList.remove("matrix-invalid");

    }
}


function validarMatrices(){

    let campos = document.querySelectorAll(".matrix-input:not(.matrix-diagonal)");

    let vacios = 0;
    let errores = 0;

    for(let i = 0; i < campos.length; i++){

        let valor = campos[i].value.trim();

        if(valor === ""){

            vacios++;

        }else if(isNaN(valor) || Number(valor) < 0){

            errores++;

        }

    }

    let estado = document.getElementById("estadoBox");

    if(errores > 0){

        estado.className = "estadoBox estadoError";
        estado.innerHTML = `<i class="bi bi-x-circle"></i> Hay ${errores} dato(s) inválido(s). Solo se permiten números positivos o cero.`;
        setTimeout(function(){
    window.location.href = "/solucion-inicial";
}, 800);

    }else if(vacios > 0){

        estado.className = "estadoBox estadoAdvertencia";
        estado.innerHTML = `<i class="bi bi-exclamation-triangle"></i> Faltan ${vacios} celda(s) por completar.`;

    }else{

    obtenerMatrices();

    estado.className = "estadoBox estadoCorrecto";

    estado.innerHTML =
    '<i class="bi bi-check-circle"></i> Las matrices están completas y listas para continuar.';

    setTimeout(function(){

        window.location.href =
        "/solucion-inicial";

    }, 700);

}
}
function continuarNuevaInstancia(){

    let construccion = document.querySelector('input[name="construccion"]:checked').value;

    localStorage.setItem("metodoConstruccion", construccion);

    if(construccion === "mayores_flujos"){
        window.location.href = "/matrices-mayores-flujos";
    }

    if(construccion === "aleatorizada"){
        window.location.href = "/matrices-aleatorizada";
    }
}

document.addEventListener("change", function(event){

    if(event.target.name === "construccion"){

        let opciones = document.querySelectorAll('input[name="construccion"]');

        opciones.forEach(function(opcion){
            opcion.closest(".opcionHeuristica").classList.remove("seleccionada");
        });

        event.target.closest(".opcionHeuristica").classList.add("seleccionada");
    }

    if(event.target.name === "mejora"){

        let opciones = document.querySelectorAll('input[name="mejora"]');

        opciones.forEach(function(opcion){
            opcion.closest(".opcionHeuristica").classList.remove("seleccionada");
        });

        event.target.closest(".opcionHeuristica").classList.add("seleccionada");
    }

});
const botonTema = document.getElementById("themeToggle");

if(botonTema){

    botonTema.addEventListener("click", function(){

        document.body.classList.toggle("darkMode");

        if(document.body.classList.contains("darkMode")){
            localStorage.setItem("tema", "oscuro");
        }else{
            localStorage.setItem("tema", "claro");
        }

    });

}

if(localStorage.getItem("tema") === "oscuro"){
    document.body.classList.add("darkMode");
}

if(localStorage.getItem("tema") === "oscuro"){
    document.body.classList.add("darkMode");
}
function obtenerMatrices(){

    let flujo = [];
    let distancia = [];

    let filasFlujo =
        document.querySelectorAll("#tablaFlujo tbody tr");

    let filasDistancia =
        document.querySelectorAll("#tablaDistancia tbody tr");

    filasFlujo.forEach(function(fila){

        let renglon = [];

        let celdas = fila.querySelectorAll("input");

        celdas.forEach(function(celda){

            renglon.push(Number(celda.value));

        });

        flujo.push(renglon);

    });

    filasDistancia.forEach(function(fila){

        let renglon = [];

        let celdas = fila.querySelectorAll("input");

        celdas.forEach(function(celda){

            renglon.push(Number(celda.value));

        });

        distancia.push(renglon);

    });

    localStorage.setItem(
        "matrizFlujo",
        JSON.stringify(flujo)
    );

    localStorage.setItem(
        "matrizDistancia",
        JSON.stringify(distancia)
    );

}
function continuarResultados(){

    let mejora = document.querySelector('input[name="mejora"]:checked').value;

    localStorage.setItem("metodoMejora", mejora);

    window.location.href = "/resultados";

}