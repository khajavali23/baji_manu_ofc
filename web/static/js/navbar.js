document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("mobileMenuToggle");
    const nav = document.getElementById("nav");

    if (toggle && nav) {
        toggle.addEventListener("click", function () {

            // Toggle menu
            nav.classList.toggle("show");

            // Optional: toggle active state
            toggle.classList.toggle("active");

        });
    }

});


document.querySelectorAll('.nav-item.dropdown').forEach(function (item) {
    item.addEventListener('mouseenter', function () {
        let menu = this.querySelector('.dropdown-menu');
        if (menu) menu.classList.add('show');
    });

    item.addEventListener('mouseleave', function () {
        let menu = this.querySelector('.dropdown-menu');
        if (menu) menu.classList.remove('show');
    });
});


