/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/pages/**/*.html',
        './templates/includes/**/*.html',
        './scripts/build_pages.py',
    ],
    theme: {
        extend: {
            colors: {
                'bleu-loubine': 'var(--bleu-loubine)',
                'bleu-estran': 'var(--bleu-estran)',
                'reflet': 'var(--reflet)',
                'ecume': 'var(--ecume)',
                'sable': 'var(--sable)',
                'blanc-coquille': 'var(--blanc-coquille)',
                'dune': 'var(--dune)',
                'encre': 'var(--encre)',
                'encre-douce': 'var(--encre-douce)',
                'nuit': 'var(--nuit)',
                'tamaris': 'var(--tamaris)',
                'tamaris-pale': 'var(--tamaris-pale)',
                'varech': 'var(--varech)',
                'ajonc': 'var(--ajonc)',
                'ecume-nuit': 'var(--ecume-nuit)',
            },
            fontFamily: {
                titre: ['Fraunces Reflets', 'Georgia', 'Times New Roman', 'serif'],
                texte: ['Karla Reflets', 'Helvetica Neue', 'Arial', 'sans-serif'],
            },
            borderRadius: {
                'rayon-sm': '6px',
                'rayon-md': '12px',
                'rayon-lg': '20px',
                'rayon-pilule': '999px',
            },
            boxShadow: {
                posee: 'var(--ombre-posee)',
                relief: 'var(--ombre-relief)',
            },
        },
    },
    plugins: [],
};
