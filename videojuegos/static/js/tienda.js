document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".articulo-selector").forEach(function (selector) {
    selector.addEventListener("click", function () {
      var target = document.getElementById(this.dataset.target);
      if (target) {
        target.src = this.dataset.src;
      }
    });
  });

  document.querySelectorAll(".quantity-control").forEach(function (control) {
    var input = control.querySelector(".cantidad-input");
    var display = control.querySelector(".quantity-display");
    var buttons = control.querySelectorAll(".quantity-btn");
    if (!input || !display || buttons.length === 0) {
      return;
    }
    var stock = parseInt(input.dataset.stock, 10);
    if (isNaN(stock)) {
      stock = 0;
    }
    var min = parseInt(input.dataset.min, 10);
    if (isNaN(min) || min < 1) {
      min = 1;
    }
    var value = parseInt(input.value, 10);
    if (isNaN(value)) {
      value = min;
    }

    var decrementBtn = control.querySelector('.quantity-btn[data-step="-1"]');
    var incrementBtn = control.querySelector('.quantity-btn[data-step="1"]');

    if (stock <= 0) {
      sync(0);
      if (incrementBtn) {
        incrementBtn.disabled = true;
      }
      if (decrementBtn) {
        decrementBtn.disabled = true;
      }
      return;
    }

    if (value < min) {
      value = min;
    } else if (value > stock) {
      value = stock;
    }
    sync(value);

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        var step = parseInt(button.dataset.step, 10) || 0;
        var next = value + step;
        if (step > 0 && value >= stock) {
          notify("warning", "Solo hay " + stock + " unidades disponibles.");
          return;
        }
        if (step < 0 && value <= min) {
          notify("warning", "Debes solicitar al menos " + min + " unidad.");
          return;
        }
        next = Math.max(min, Math.min(stock, next));
        sync(next);
      });
    });

    control.addEventListener("submit", function (event) {
      if (value < min) {
        event.preventDefault();
        sync(min);
        notify("warning", "Debes solicitar al menos " + min + " unidad.");
        return;
      }
      if (value > stock) {
        event.preventDefault();
        sync(stock);
        notify("warning", "Solo hay " + stock + " unidades disponibles.");
      }
    });

    function sync(nuevoValor) {
      value = nuevoValor;
      input.value = value;
      display.textContent = value;
    }
  });

  function notify(tipo, mensaje) {
    if (typeof window.mostrarToastBootstrap === "function") {
      window.mostrarToastBootstrap(tipo, mensaje);
    } else {
      console.warn(mensaje);
    }
  }
});
