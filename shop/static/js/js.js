function get_more() {
    let div = document.getElementById("more_model");
    div.style.display = 'block';
    let btn = document.getElementById("show-more-button").style.display = 'none';
    let btn2 = document.getElementById("close-more-button").style.display = 'block';
}

function close_more() {
    let div = document.getElementById("more_model");
    div.style.display = 'none';
    let btn1 = document.getElementById("close-more-button").style.display = 'none';
    let btn2 = document.getElementById("show-more-button").style.display = 'block';
}

function new_price() {
    let c = document.getElementById('elem1').value;
    let price = document.getElementById('price').textContent;
    let new_price = parseInt(price.match(/\d+/))
    if (c > 0) {
        document.getElementById('new_p').innerHTML = new_price * c + " ₽";
    } else {
        document.getElementById('new_p').innerHTML = 0 + " ₽";
    }
}

function unlocked() {
    let btn = document.querySelector(".order-button");
    btn.innerHTML = "Заказать";
    btn.disabled = false;
}

function myFunc() {
    var c = document.getElementById('elem1').value;
    var amount = document.getElementById('elem2').textContent;
    var numEl = parseInt(amount.match(/\d+/))
    let btn = document.querySelector(".order-button");   // выбираем элемент с классом block
    if (c <= 0 || c > numEl) {
        btn.setAttribute('disabled', true);
        btn.innerHTML = "Столько товара нет :(";
    }
}

function minus_amount() {
    let c = document.getElementById('elem1').value;
    new_amount = c - 1;
    if (c > 1) {
        document.getElementById('elem1').value = new_amount;
        new_price();
    }
}

function plus_amount() {
    var c = Number(document.getElementById('elem1').value);
    var new_amount = c + 1;
    document.getElementById('elem1').value = new_amount;
    new_price();
}