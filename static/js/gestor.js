function eliminarGasto(idGasto){

    if (!confirm("Estas Seguro que quieres eliminar este gasto?")){
        return;
    }

    fetch(`/delete/${idGasto}`,{
        method: 'POST',
        headers: {
            'Content-type' :'application/json'
        }
    })
    .then((response) => response.json())
    .then((data) => {
        if(data.status==="success"){
            const fila = document.getElementById(`fila-${idGasto}`);
            if(fila){
                fila.remove();
                console.log("Gasto Eliminado Correctamente: ");
            }
        }else{
            alert("Error al eliminar: " + data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}

function agregarGasto() {
    const descripcion = document.getElementById('descripcion').value;
    const categoria = document.getElementById('categoria').value;
    const monto = document.getElementById('monto').value;

    if(!descripcion || !categoria || !monto){
        alert("Por favor, llena todos los campos");
        return;
    }

    const gastoData = {
        descripcion: descripcion,
        categoria: categoria,
        monto: monto
    };

    console.log("Enviando datos:", gastoData);

    fetch("/gastos", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(gastoData)
    })
    .then(response => {
        if (!response.ok) throw new Error("Error en el servidor");
        return response.json();
    })
    .then(data => {
        console.log("Respuesta de Flask:", data);
        if(data.status === "success") {
            const tabla = document.getElementById("cuerpo-tabla") || document.getElementById("tabla-gastos");
            
            if(!tabla){
                window.location.reload();
                return;
            }
            const nuevaFila = document.createElement("tr"); 
            nuevaFila.id = `fila-${data.gasto.id}`;

            nuevaFila.innerHTML = `
                <td>${data.gasto.descripcion}</td>
                <td>${data.gasto.categoria}</td>
                <td>${data.gasto.monto}</td>
                <td>${data.gasto.fecha}</td>
                <td>
                    <a class="botonEditar" href="/edit/${data.gasto.id}">Edit</a>
                    <button class="botonEliminar" onclick="eliminarGasto(${data.gasto.id})">Delete</button>
                </td>
            `;

            const cuerpoTabla = tabla.querySelector("tbody") || tabla;
            cuerpoTabla.appendChild(nuevaFila);

            document.getElementById('descripcion').value = "";
            document.getElementById('categoria').value = "";
            document.getElementById('monto').value = "";
        }
    })
    .catch(err => {
        console.error("Error en Fetch:", err);
        alert("No se pudo agregar el gasto. Revisa la consola.");
    });
}