document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Получаем данные формы
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    const email = data.email.trim();

    // Строгая проверка email (обязательно должна быть точка и домен)
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address (e.g., example@gmail.com or example@mail.ru)");
        return; // Остановка отправки
    }

    // Проверка телефона (минимум 10 цифр)
    const phonePattern = /^[0-9]{10,}$/;
    if (!phonePattern.test(data.phone)) {
        alert("Please enter a valid phone number (at least 10 digits)");
        return;
    }

    // Проверка имени (не пустое)
    if (!data.firstname || data.firstname.trim() === '') {
        alert("Please enter your first name");
        return;
    }

    // Отправка данных
    fetch('/api/contacts', {
        method: 'POST',
        body: JSON.stringify({
            firstname: data.firstname,
            phone: data.phone,
            email: email
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server error: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('result').innerHTML = data.message || "Success!";
        alert("Thank you for contacting us! We'll get back to you soon.");
        this.reset(); // Очистка формы
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = 
            error.message.includes('Server error') ? 
            "Server error. Please try later." : 
            "An error occurred. Please check your data.";
    });
});