window.addEventListener("scroll", function () {

    const button = document.getElementById("wm-back-to-top");
    const section2 = document.getElementById("section2");
    const section3 = document.getElementById("section3");

    const section2Position = section2.offsetTop;
    const section3Position = section3.offsetTop;

    // وقتی از سکشن سوم رد شد
    if (window.scrollY > section3Position) {
        button.classList.add("show");
    }
    // وقتی به سکشن‌های بالاتر از سکشن دوم برگشت
    else if (window.scrollY < section2Position) {
        button.classList.remove("show");
    }
});

AOS.init({
    duration: 1000, // مدت زمان انیمیشن
    easing: 'ease-in-out', // نوع انیمیشن
    once: true, // انیمیشن فقط یک بار اجرا شود
});

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const header = document.querySelector('header');    
    const closeMenu = document.querySelector('.menu-close');

    menuToggle.addEventListener('click', function() {
        if (mobileMenu.classList.contains('open')) {
            mobileMenu.classList.remove('open');
        } else {
            mobileMenu.classList.add('open');
        }
    });

    closeMenu.addEventListener('click', function() {
        mobileMenu.classList.remove('open');
    });

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // افزودن قابلیت دارک مود و لایت مود
    const themeToggleButton = document.getElementById("theme-toggle-button");

    // بررسی تم ذخیره‌شده در لوکال استوریج
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        document.body.classList.toggle("dark-mode", savedTheme === "dark");
    }

    themeToggleButton.addEventListener("click", function () {
        const isDarkMode = document.body.classList.toggle("dark-mode");

        // ذخیره تم انتخاب‌شده در لوکال استوریج
        localStorage.setItem("theme", isDarkMode ? "dark" : "light");
    });
    
    document.addEventListener('DOMContentLoaded', function () {
        const themeToggleButton = document.getElementById("theme-toggle-button");
        const themeIcon = document.getElementById("theme-icon");
    
        // بررسی تم ذخیره‌شده در لوکال استوریج
        const savedTheme = localStorage.getItem("theme");
        if (savedTheme) {
            document.body.classList.toggle("dark-mode", savedTheme === "dark");
            themeIcon.classList.toggle("fa-moon", savedTheme === "dark");
            themeIcon.classList.toggle("fa-sun", savedTheme !== "dark");
        }
    
        themeToggleButton.addEventListener("click", function () {
            const isDarkMode = document.body.classList.toggle("dark-mode");
    
            // تغییر آیکون
            themeIcon.classList.toggle("fa-sun", !isDarkMode);
            themeIcon.classList.toggle("fa-moon", isDarkMode);
    
            // ذخیره تم انتخاب‌شده در لوکال استوریج
            localStorage.setItem("theme", isDarkMode ? "dark" : "light");
        });
    });
    
});

