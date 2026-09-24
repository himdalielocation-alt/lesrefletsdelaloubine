// Menu mobile (burger) — partagé par toutes les pages du site.
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');
const menuIconOpen = document.getElementById('menuIconOpen');
const menuIconClose = document.getElementById('menuIconClose');

if (menuToggle && mobileMenu) {
    function closeMobileMenu() {
        mobileMenu.classList.add('hidden');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.setAttribute('aria-label', 'Ouvrir le menu');
        menuIconOpen.classList.remove('hidden');
        menuIconClose.classList.add('hidden');
    }
    function openMobileMenu() {
        mobileMenu.classList.remove('hidden');
        menuToggle.setAttribute('aria-expanded', 'true');
        menuToggle.setAttribute('aria-label', 'Fermer le menu');
        menuIconOpen.classList.add('hidden');
        menuIconClose.classList.remove('hidden');
    }
    menuToggle.addEventListener('click', () => {
        if (mobileMenu.classList.contains('hidden')) openMobileMenu();
        else closeMobileMenu();
    });
    mobileMenu.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', closeMobileMenu);
    });
}
