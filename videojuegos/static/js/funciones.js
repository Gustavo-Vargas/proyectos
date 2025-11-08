function asignaUsuario(idUsuario, grupos) {
    document.getElementById('idUsuario').value = idUsuario;
    const seleccionados = grupos
        .split('-')
        .map(valor => valor.trim())
        .filter(Boolean);
    $('#formGrupos input[type=checkbox]').each(function () {
        const estaSeleccionado = seleccionados.includes($(this).prop('name'));
        $(this).prop('checked', estaSeleccionado);
    });
}
