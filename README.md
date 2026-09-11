# AppliCab Avocats — maquette de refonte (v2, direction SaaS)

Prototype codé haute-fidélité (HTML/CSS/JS, aucune dépendance) de la refonte du site
[applicab-avocats.com](https://applicab-avocats.com/), en vue d'un thème WordPress sur-mesure compatible Gutenberg.

## Pages

- `index.html` — accueil (hero + scène produit animée, preuves, onglets, bento, chiffres, personas, méthode, témoignages, histoire, tarifs, FAQ, blog)
- `fonctionnalites.html` — six fonctions détaillées, cas d'usage, comparatif, FAQ
- `tarifs.html` — offres, retour sur investissement, tableau « tout inclus », FAQ tarifs
- `blog/article.html` — template d'article (barre de lecture, sommaire collant, prose, articles liés)
- `llms.txt` — résumé du site pour les crawlers d'IA générative

## Ouvrir la maquette

```
python3 -m http.server 8080
```

puis http://localhost:8080/.

## Modifier

Les pages sont générées depuis `src/pages/` et `src/partials/` (en-tête, pied de page, CTA, mockups, JSON-LD) :

```
python3 src/build.py
```

## Portage WordPress

Voir `NOTE-TECHNIQUE.md` : arborescence proposée, découpage en templates PHP et blocs Gutenberg, SEO/GEO, performance, accessibilité.
