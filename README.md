# AppliCab Avocats — maquette de refonte

Prototype codé haute-fidélité (HTML/CSS/JS, aucune dépendance) de la refonte du site
[applicab-avocats.com](https://applicab-avocats.com/), en vue d'un thème WordPress sur-mesure compatible Gutenberg.

## Pages

- `index.html` — page d'accueil
- `fonctionnalites-tarifs.html` — fonctionnalités, cas d'usage, comparatif, tarifs, FAQ
- `blog/article.html` — template d'article de blog
- `llms.txt` — résumé du site pour les crawlers d'IA générative

## Ouvrir la maquette

Ouvrir `index.html` dans un navigateur, ou servir le dossier :

```
python3 -m http.server 8080
```

puis http://localhost:8080/.

## Portage WordPress

Voir `NOTE-TECHNIQUE.md` : découpage en templates PHP et blocs Gutenberg réutilisables, SEO/GEO, performance, accessibilité.
