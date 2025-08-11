const minusBtn = document.getElementById('button-minus');
const plusBtn = document.getElementById('button-plus');
const quantityInput = document.getElementById('quantity-input');

minusBtn.addEventListener('click', function () {
    let currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }
});

plusBtn.addEventListener('click', function () {
    let currentValue = parseInt(quantityInput.value);
    quantityInput.value = currentValue + 1;
});