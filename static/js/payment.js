// Kart numarası girişi için doğrulama
function validateNumber(input) {
    input.value = input.value.replace(/\D/g, ''); // Sadece rakamlara izin ver
    if (input.value.length > 16) {
        input.value = input.value.slice(0, 16); // Maksimum 16 karaktere sınırla
    }
}

// Son kullanma tarihi girişi için doğrulama
function validateExpiry(input) {
    input.value = input.value.replace(/[^0-9\/]/g, ''); // Sadece rakamlar ve '/' karakterlerine izin ver
    if (input.value.length === 2 && !input.value.includes('/')) {
        input.value = input.value + '/'; // Otomatik olarak '/' ekle
    }
    if (input.value.length > 5) {
        input.value = input.value.slice(0, 5); // Maksimum 'MM/YY' formatını sınırla
    }
}

// CVV girişi için doğrulama
function validateCVV(input) {
    input.value = input.value.replace(/\D/g, ''); // Sadece rakamlara izin ver
    if (input.value.length > 3) {
        input.value = input.value.slice(0, 3); // Maksimum 3 karaktere sınırla
    }
}

// Formu kontrol et ve gerekli aksiyonu al
function checkFormCompletion() {
    const number = document.getElementById('number').value;
    const name = document.getElementById('name').value;
    const expiry = document.getElementById('expiry').value;
    const cvv = document.getElementById('cvv').value;

    const form = document.getElementById('card-form');

    if (number && name && expiry && cvv) {
        form.action = '/paymentSuccess'; // Tüm alanlar doluysa formun action'ını /paymentSuccess olarak ayarla
    } else {
        form.removeAttribute('action'); // Eksik alan varsa action'ı kaldır
    }
}

// Form alanlarının her birinde değişiklik olduğunda formu kontrol et
document.getElementById('number').addEventListener('input', checkFormCompletion);
document.getElementById('name').addEventListener('input', checkFormCompletion);
document.getElementById('expiry').addEventListener('input', checkFormCompletion);
document.getElementById('cvv').addEventListener('input', checkFormCompletion);
