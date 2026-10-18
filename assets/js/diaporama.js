// Diaporama des photos du logement (accueil, 3 langues).
// Le balisage (photos, boutons, libellés traduits) est généré par scripts/build_pages.py ;
// sans ce script, les photos restent consultables en faisant défiler au doigt.
// Défilement automatique lent (5 s), en pause au survol, au focus clavier, quand le
// diaporama n'est pas visible, et désactivé si le visiteur limite les animations.
// Toute navigation manuelle (flèches, points, balayage, clavier) arrête le défilement automatique.
(function () {
    'use strict';
    var DELAI = 5000;
    var reduit = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    document.querySelectorAll('.diaporama').forEach(function (racine) {
        var piste = racine.querySelector('.diaporama-piste');
        var diapos = Array.prototype.slice.call(racine.querySelectorAll('.diaporama-diapo'));
        var points = Array.prototype.slice.call(racine.querySelectorAll('.diaporama-points button'));
        var btnPause = racine.querySelector('.diaporama-pause');
        var total = diapos.length;
        if (!piste || total === 0) return;

        racine.classList.add('diaporama-actif');
        if (total < 2) { racine.classList.add('diaporama-seule'); return; }

        var courant = 0;
        var auto = !reduit;          // le visiteur n'a pas mis en pause / navigué lui-même
        var survol = false;
        var focus = false;
        var visible = true;
        var minuteur = null;

        function indexAffiche() {
            return Math.round(piste.scrollLeft / Math.max(piste.clientWidth, 1));
        }

        function majIndicateurs() {
            points.forEach(function (p, i) {
                if (i === courant) p.setAttribute('aria-current', 'true');
                else p.removeAttribute('aria-current');
            });
        }

        function aller(i, douceur) {
            courant = (i + total) % total;
            piste.scrollTo({ left: courant * piste.clientWidth, behavior: (douceur && !reduit) ? 'smooth' : 'auto' });
            majIndicateurs();
        }

        function majPause() {
            if (!btnPause) return;
            var label = auto ? racine.getAttribute('data-libelle-pause') : racine.getAttribute('data-libelle-lecture');
            btnPause.setAttribute('aria-label', label);
            btnPause.setAttribute('title', label);
            btnPause.querySelector('.icone-pause').style.display = auto ? '' : 'none';
            btnPause.querySelector('.icone-lecture').style.display = auto ? 'none' : '';
            // Annonce des changements de photo aux lecteurs d'écran seulement hors défilement automatique.
            piste.setAttribute('aria-live', auto ? 'off' : 'polite');
        }

        function planifier() {
            clearInterval(minuteur);
            minuteur = null;
            if (auto && !survol && !focus && visible && !document.hidden) {
                minuteur = setInterval(function () { aller(courant + 1, true); }, DELAI);
            }
        }

        function arreterAuto() {
            if (auto) { auto = false; majPause(); }
            planifier();
        }

        racine.querySelector('.diaporama-prec').addEventListener('click', function () { arreterAuto(); aller(courant - 1, true); });
        racine.querySelector('.diaporama-suiv').addEventListener('click', function () { arreterAuto(); aller(courant + 1, true); });
        points.forEach(function (p, i) {
            p.addEventListener('click', function () { arreterAuto(); aller(i, true); });
        });
        if (btnPause) {
            btnPause.addEventListener('click', function () {
                auto = !auto;
                majPause();
                planifier();
            });
        }

        piste.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowLeft') { e.preventDefault(); arreterAuto(); aller(courant - 1, true); }
            if (e.key === 'ArrowRight') { e.preventDefault(); arreterAuto(); aller(courant + 1, true); }
        });

        // Balayage au doigt : le défilement natif fait le travail, on suit la photo affichée.
        piste.addEventListener('touchstart', arreterAuto, { passive: true });
        piste.addEventListener('wheel', function (e) { if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) arreterAuto(); }, { passive: true });
        var attente = null;
        piste.addEventListener('scroll', function () {
            clearTimeout(attente);
            attente = setTimeout(function () {
                var i = indexAffiche();
                if (i !== courant) { courant = i; majIndicateurs(); }
            }, 80);
        }, { passive: true });

        racine.addEventListener('mouseenter', function () { survol = true; planifier(); });
        racine.addEventListener('mouseleave', function () { survol = false; planifier(); });
        racine.addEventListener('focusin', function () { focus = true; planifier(); });
        racine.addEventListener('focusout', function (e) {
            if (!racine.contains(e.relatedTarget)) { focus = false; planifier(); }
        });
        document.addEventListener('visibilitychange', planifier);
        if ('IntersectionObserver' in window) {
            new IntersectionObserver(function (entrees) {
                visible = entrees[0].isIntersecting;
                planifier();
            }, { threshold: 0.4 }).observe(racine);
        }
        window.addEventListener('resize', function () { aller(courant, false); });

        majIndicateurs();
        majPause();
        planifier();
    });
})();
