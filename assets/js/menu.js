// Menu mobile (burger) — partagé par toutes les pages du site.
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');
const menuIconOpen = document.getElementById('menuIconOpen');
const menuIconClose = document.getElementById('menuIconClose');

if (menuToggle && mobileMenu) {
    // Libellés lus depuis des attributs data-* (traduits par page/langue dans
    // templates/includes/header.{lang}.html) plutôt que codés en dur ici,
    // puisque ce script est partagé par les 3 langues du site.
    const labelOpen = menuToggle.getAttribute('data-label-open') || 'Ouvrir le menu';
    const labelClose = menuToggle.getAttribute('data-label-close') || 'Fermer le menu';
    function closeMobileMenu() {
        mobileMenu.classList.add('hidden');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.setAttribute('aria-label', labelOpen);
        menuIconOpen.classList.remove('hidden');
        menuIconClose.classList.add('hidden');
    }
    function openMobileMenu() {
        mobileMenu.classList.remove('hidden');
        menuToggle.setAttribute('aria-expanded', 'true');
        menuToggle.setAttribute('aria-label', labelClose);
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
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
            closeMobileMenu();
            menuToggle.focus();
        }
    });
}
