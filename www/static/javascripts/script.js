// Функция для валидации email
function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const domainPart = email.split('@')[1];
    const commonTlds = ['com', 'net', 'org', 'ru', 'ua', 'by', 'kz', 'uk', 'de', 'fr', 'it', 'es', 'io', 'co'];
    const tld = domainPart?.split('.')?.pop();
    
    return emailPattern.test(email) && commonTlds.includes(tld);
}

// Отправка формы тура
function submitTourRequest() {
    const firstName = document.getElementById("first-name")?.value.trim();
    const lastName = document.getElementById("last-name")?.value.trim();
    const email = document.getElementById("email")?.value.trim();
    const phone = document.getElementById("phone")?.value.trim();

    if (!firstName || !lastName || !email || !phone) {
        alert("Please fill in all fields.");
        return false;
    }

    if (!validateEmail(email)) {
        alert("Please enter a valid email address (e.g., example@gmail.com).");
        return false;
    }

    const phonePattern = /^[0-9]{10,}$/;
    if (!phonePattern.test(phone)) {
        alert("Please enter a valid phone number (at least 10 digits).");
        return false;
    }

    alert("Form submitted successfully!");
    return true;
}

// Подписка
function subscribe() {
    const name = document.getElementById("name")?.value.trim();
    const email = document.getElementById("email")?.value.trim();
    const phone = document.getElementById("phone")?.value.trim();

    if (!name || !email || !phone) {
        alert("Please fill in all fields.");
        return false;
    }

    if (!validateEmail(email)) {
        alert("Please enter a valid email address (e.g., example@mail.ru).");
        return false;
    }

    const phonePattern = /^[0-9]{10,}$/;
    if (!phonePattern.test(phone)) {
        alert("Please enter a valid phone number (at least 10 digits).");
        return false;
    }

    alert("Thank you for subscribing! We'll contact you soon.");
    return true;
}

// Переключение текста
function toggleText(elementId) {
    const textElement = document.getElementById(elementId);
    if (!textElement) return;
    
    const headerElement = textElement.previousElementSibling;
    textElement.classList.toggle('show');
    headerElement?.classList.toggle('active');
}

// Изменение текста логотипа
function changeLogoText(text) {
    const logo = document.getElementById("logo-text");
    if (logo) logo.innerText = text;
}

// Обработчик прокрутки
function handleScroll() {
    // Кнопка "Наверх"
    const backToTopButton = document.querySelector('.back-to-top');
    if (backToTopButton) {
        backToTopButton.style.display = (window.scrollY > 300) ? 'flex' : 'none';
    }

    // Анимация карточек
    const cards = document.querySelectorAll('.card');
    const triggerBottom = window.innerHeight / 5 * 4;
    
    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;
        if (cardTop < triggerBottom) {
            card.classList.add('show');
        } else {
            card.classList.remove('show');
        }
    });

    // Эффект для навигации
    const nav = document.querySelector('nav');
    if (nav) {
        nav.classList.toggle('scrolled', window.scrollY > 50);
    }
}

// Плавная прокрутка вверх
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Инициализация всех обработчиков событий
document.addEventListener('DOMContentLoaded', function() {
    // Обработчик прокрутки
    window.addEventListener('scroll', handleScroll);
    
    // Кнопка "Наверх"
    const backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', scrollToTop);
    }
    
    // Другие инициализации при необходимости
});