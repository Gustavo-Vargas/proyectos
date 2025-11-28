function asignaUsuario(idUsuario, grupos) {
    const campoUsuario = document.getElementById('idUsuario');
    if (campoUsuario && idUsuario) {
        campoUsuario.value = idUsuario;
    }
    
    const seleccionados = grupos
        .split('-')
        .map(valor => valor.trim())
        .filter(Boolean);
    
    if (typeof jQuery !== 'undefined') {
        $('#formGrupos input[type=checkbox]').each(function () {
            const estaSeleccionado = seleccionados.includes($(this).prop('name'));
            $(this).prop('checked', estaSeleccionado);
        });
    } else {
        const checkboxes = document.querySelectorAll('#formGrupos input[type=checkbox]');
        checkboxes.forEach(function(checkbox) {
            const estaSeleccionado = seleccionados.includes(checkbox.name);
            checkbox.checked = estaSeleccionado;
        });
    }
}

function validarFormularioGrupos() {
    const idUsuario = document.getElementById('idUsuario');
    if (!idUsuario || !idUsuario.value || idUsuario.value === '') {
        alert('Error: No se seleccionó un usuario. Por favor, cierra el modal y vuelve a intentar.');
        return false;
    }
    return true;
}
