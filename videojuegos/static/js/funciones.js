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

// El codigo espera a que la pagina temrine de cargar
$(document).ready(function(){
    $('#id_estado').change(function(e){
        let token = $('[name="csrfmiddlewaretoken"]').val();
        let url = $(this).data('url');
        $.ajax({
            type: 'POST',
            url: url,
            data: {'id_estado':$(this).val(), 'csrfmiddlewaretoken': token},
            success: function(data){
                let html = '';
                $.each(data, function(llave, valor){
                    html+=`<option value="${valor.id}">${valor.nombre}</option>`
                });
                $('#id_municipio').html(html);
            }
        });
    });
});


(function () {
    const typeMap = {
        success: 'success',
        warning: 'warning',
        error: 'danger',
        danger: 'danger',
        info: 'info',
    };

    function buildToast(tipo, mensaje) {
        const container = document.getElementById('app-toast-container');
        if (!container || !window.bootstrap || !window.bootstrap.Toast) {
            return null;
        }
        const baseTipo = (tipo || '').split(' ')[0];
        const color = typeMap[baseTipo] || 'dark';
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-bg-' + color + ' border-0 shadow-sm';
        toast.setAttribute('role', 'status');
        toast.setAttribute('aria-live', 'polite');
        const content = document.createElement('div');
        content.className = 'd-flex align-items-center gap-2';
        const body = document.createElement('div');
        body.className = 'toast-body';
        body.textContent = mensaje;
        const close = document.createElement('button');
        close.type = 'button';
        close.className = 'btn-close btn-close-white me-2 m-auto';
        close.setAttribute('data-bs-dismiss', 'toast');
        close.setAttribute('aria-label', 'Cerrar');
        content.appendChild(body);
        content.appendChild(close);
        toast.appendChild(content);
        container.appendChild(toast);
        return toast;
    }

    window.mostrarToastBootstrap = function (tipo, mensaje) {
        const toast = buildToast(tipo, mensaje);
        if (!toast) {
            return;
        }
        const instance = new bootstrap.Toast(toast, { delay: 3000, autohide: true });
        toast.addEventListener('hidden.bs.toast', function () {
            toast.remove();
        });
        instance.show();
    };

    document.addEventListener('DOMContentLoaded', function () {
        const script = document.getElementById('django-messages-data');
        if (!script) {
            return;
        }
        let items;
        try {
            items = JSON.parse(script.textContent);
        } catch (error) {
            script.remove();
            return;
        }
        script.remove();
        if (!Array.isArray(items)) {
            return;
        }
        items.forEach(function (item) {
            if (!item || !item.text) {
                return;
            }
            window.mostrarToastBootstrap(item.level, item.text);
        });
    });
})();
