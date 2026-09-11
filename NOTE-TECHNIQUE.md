# Note technique — Refonte AppliCab Avocats (v2, direction SaaS)

Maquette codée haute-fidélité (HTML/CSS/JS sans dépendance) destinée à la présentation client,
puis au portage dans un **thème WordPress sur-mesure** (PHP + Gutenberg, sans page builder).

Pages livrées :

| Page | Fichier | Template WordPress cible |
|---|---|---|
| Accueil | `index.html` | `front-page.php` |
| Fonctionnalités | `fonctionnalites.html` | `page-fonctionnalites.php` |
| Tarifs | `tarifs.html` | `page-tarifs.php` |
| Article de blog | `blog/article.html` | `single.php` |
| Fichier IA génératives | `llms.txt` | fichier statique à la racine |

Les pages sont assemblées depuis `src/pages/*.html` et `src/partials/*.html` par `python3 src/build.py`
(le découpage en partials préfigure `header.php` / `footer.php` / `template-parts/`).

## 1. Arborescence proposée

Le site actuel expose une navigation à plat (À propos, Présentation, Fonctionnalités & cas d'usages, Blog, Contact,
Accès à l'application) qui mélange rubriques éditoriales et produit. L'arborescence proposée reprend les codes des
sites SaaS (monday.com, Doctrine, Axiocap) : une entrée **Produit**, une entrée par **persona**, une page **Tarifs**
autonome, une rubrique **Ressources** qui regroupe le contenu SEO.

```
/                                   Accueil
/fonctionnalites/                   Vue d'ensemble produit (6 fonctions, ancres #dossiers #agenda #clients
                                    #messagerie #pilotage #securite, cas d'usage, comparatif, FAQ)
/fonctionnalites/<fonction>/        (phase 2) une page par fonction pour le SEO longue traîne
/vous-etes/avocat-independant/      Pages persona (phase 2) : indépendant, cabinet de plusieurs associés,
/vous-etes/cabinet/                 jeune avocat, conseil & droit des affaires, contentieux.
/vous-etes/jeune-avocat/            Dans la maquette, ces entrées pointent vers les ancres de /fonctionnalites/.
/tarifs/                            Page tarifs (offres, ROI, tableau « tout inclus », FAQ tarifs)
/blog/                              Liste des articles (catégories : Organisation, Facturation, Pilotage, Innovation…)
/blog/<slug>/                       Articles existants, **slugs conservés** (aucune redirection à créer)
/guides/                            Contenus longs téléchargeables (Guide anti-impayés…) — phase 2
/a-propos/                          Histoire, prix, équipe (aujourd'hui section #histoire de l'accueil)
/contact/                           Formulaire contact / demande de démo
/mentions-legales/, /politique-de-cookies/
/llms.txt, /robots.txt, /sitemap.xml
```

Navigation principale : Produit ▾ (méga-menu 6 fonctions) · Vous êtes ▾ · Tarifs · Ressources ▾ (Blog, Guides,
Vidéos, FAQ, Notre histoire) · Contact · **Se connecter** · **Découvrir AppliCab gratuitement** (CTA principal).

Redirections 301 à prévoir depuis les anciennes URLs de rubriques (`/presentation/`, `/fonctionnalites-cas-d-usages/`,
`/a-propos/`) vers les nouvelles ; les articles ne bougent pas.

## 2. Direction artistique appliquée

- **Palette** : l'identité verte d'AppliCab est conservée mais déplacée vers des codes SaaS : fond blanc dominant,
  sections alternées sable très pâle `#F6F3EB`, sections d'impact **forêt** `#14210E`, primaire olive `#5B7A1F`,
  accent **lime** `#B9D94A` (halos, soulignements, boutons sur fond sombre), jaune avocat `#F0DF62` en halo.
  Tokens dans `assets/css/main.css` § 1 → `theme.json`. Contrastes AA : olive sur blanc 4,9:1, blanc sur forêt 15:1,
  lime sur forêt 10:1.
- **Typographie** : Plus Jakarta Sans 700/800 pour les titres (grandes tailles, interlettrage serré, dégradé de
  couleur sur le mot clé), DM Sans pour le corps. Échelle fluide `clamp()`.
- **Mockups produit en HTML/CSS** (`.app`, `.steps-ui`, `.agenda`, `.msg`) : aucune image lourde, texte réel donc
  indexable, et adaptables dans le thème (un bloc « Aperçu produit » avec champs). Dans le hero, l'étape « en cours »
  se coche en boucle ; des cartes flottantes (rappel envoyé, client connecté, temps gagné) animent la scène.
- **Animations** : révélations au défilement (`.reveal`, position + opacité, uniquement pour les blocs hors écran au
  chargement, donc thumbnail et impression complets), onglets produit à rotation automatique avec barre de progression
  (pause au survol, arrêt au premier clic), compteurs animés, marquee de preuves en CSS, barre de lecture sur les
  articles, sous-navigation collante sur la page Fonctionnalités. `prefers-reduced-motion` neutralise tout.
- **Composants SaaS** : hero centré + scène produit, bandeau de preuves, onglets « Que voulez-vous simplifier ? »,
  bento, bande de chiffres, cartes persona, blocs fonctionnalité alternés texte/mockup, témoignages, tableau
  « tout inclus », FAQ `<details>`, CTA plein écran, pied de page à cinq colonnes.

## 3. Découpage WordPress : template PHP fixe vs blocs Gutenberg

### 3.1 Éléments communs (PHP fixe)

| Élément | Implémentation |
|---|---|
| Bandeau d'annonce | `header.php`, texte + lien + date de fin dans une **page d'options ACF**, masqué après la date. |
| En-tête + méga-menus | `header.php`, `wp_nav_menu('principal')` avec un walker qui rend les items de niveau 2 en `.mega` (titre, sous-titre et icône via champs ACF sur l'item de menu). Boutons « Se connecter » et CTA : options ACF. JS de `assets/js/main.js` repris tel quel. |
| Bandeau CTA final | `template-parts/cta-band.php`, contenu dans les options ACF, inséré par tous les templates. |
| Pied de page | `footer.php` : 4 menus (`wp_nav_menu`), newsletter via le plugin existant (shortcode), réseaux et mentions © depuis les options. |
| Fil d'Ariane | `template-parts/breadcrumb.php` + JSON-LD `BreadcrumbList` (ou délégué au plugin SEO, sans doublon). |
| `<head>` | `wp_head()` ; `title`/`meta description` par le plugin SEO ; polices **auto-hébergées** (`assets/fonts/`, `font-display: swap`, `preload` des 2 fichiers critiques). |

### 3.2 Page d'accueil (`front-page.php`)

| Section | Type | Détail |
|---|---|---|
| Hero | **PHP fixe + ACF** | Pilule « Nouveau », titre H1 (mot clé en dégradé via `<span class="grad-text">`), chapô, 2 boutons, liste de preuves. La scène produit est un `template-parts/mockup-full.php` dont les libellés (noms de dossiers, dates) sont des champs ACF pour rester réalistes sans code. |
| Bandeau de preuves | **Bloc `applicab/preuves`** | Répéteur icône/texte, rendu marquee CSS + liste masquée pour lecteurs d'écran. |
| Onglets produit | **Bloc `applicab/onglets-produit`** | InnerBlocks : un bloc enfant par onglet (titre, chapô, liste, lien, mockup choisi parmi 5 variantes). Contenu des 5 panneaux dans le DOM. |
| Pourquoi (bento) | **Bloc `applicab/benefices`** + enfant `applicab/carte` (icône, titre, texte, variante `sand/forest/lime`, largeur `span-4/5/6/7/8`, mini-UI optionnelle). |
| Réponse directe (GEO) | **Bloc `applicab/reponse`** | Question H2 + réponse en texte brut. |
| Chiffres | **Bloc `applicab/chiffres`** | Répéteur valeur/unité/libellé, attribut `data-count` pour l'animation. |
| Vous êtes | **Bloc `applicab/personas`** | Répéteur numéro/titre/texte/lien. |
| Blocs fonctionnalité | **Bloc `applicab/fonctionnalite`** | Eyebrow, titre, chapô, liste, lien, mockup, option « inversé ». Réutilisé sur la page Fonctionnalités avec `id` d'ancre. |
| Méthode 4 étapes | **Bloc `applicab/etapes`** | `<ol class="steps">`. |
| Témoignages | **Bloc `applicab/temoignages`** | CPT `temoignage` ou répéteur (citation, nom, fonction, ville). |
| Notre histoire | **PHP fixe + répéteur ACF** | Année, titre, texte. |
| Tarifs | **Bloc `applicab/tarifs`** | Prix saisis **une fois** dans les options ACF, lus par le bloc et par le JSON-LD `offers` (accueil et page Tarifs toujours synchronisés). |
| FAQ | **Bloc `applicab/faq`** | Répéteur Q/R → `<details>` ; le bloc émet le JSON-LD `FAQPage`. |
| Derniers articles | **PHP fixe** | `WP_Query` 3 derniers, `template-parts/post-card.php`. |

### 3.3 Page Fonctionnalités (`page-fonctionnalites.php`)

En-tête de page en PHP (`the_title`, chapô ACF, 2 boutons), **sous-navigation collante** générée depuis les
`id` des blocs `applicab/fonctionnalite` de la page, puis blocs : `reponse`, 6 × `fonctionnalite`, `benefices`
(cas d'usage), **tableau natif Gutenberg** avec style de bloc « Comparatif » (`register_block_style`, colonne
AppliCab = classe `is-us`), `faq`, CTA.

### 3.4 Page Tarifs (`page-tarifs.php`)

Blocs `tarifs`, `fonctionnalite` (bloc ROI, variante carte forêt), tableau natif « Tout inclus », `faq`
(FAQ tarifs, JSON-LD dédié), CTA. Le bandeau d'augmentation au 1er octobre 2026 lit la même option ACF que
le bandeau d'annonce.

### 3.5 Article de blog (`single.php`)

Objectif : **ne rien perdre du SEO existant**. Slugs, `title`, meta description (plugin SEO), H2/H3 et liens
internes des articles actuels sont conservés ; seul l'habillage change.

| Élément | Implémentation |
|---|---|
| Barre de lecture | `div.reading-bar` dans `single.php`, JS existant. |
| En-tête | Fil d'Ariane, catégorie principale, `the_title()` en H1, `the_excerpt()` en chapô, auteur, date, temps de lecture calculé. |
| Image à la une | `the_post_thumbnail()` avec `srcset`, `fetchpriority="high"` (LCP), WebP/AVIF. |
| Sommaire | Généré par filtre PHP depuis les H2/H3 de `the_content` (ajout d'`id`), colonne collante, désactivable. |
| Corps | `the_content()` en blocs natifs, stylé par `.prose` ; style de bloc « Encart » (Groupe → `callout`, `callout--forest`) pour les CTA contextuels. |
| Étiquettes, partage, auteur, précédent/suivant, articles liés | PHP fixe. |
| Données structurées | `BlogPosting` + `BreadcrumbList` : plugin SEO s'il les émet, sinon `single.php`. |

### 3.6 Réglages Gutenberg

- `theme.json` : palette (tokens § 2), échelle typographique, espacements, `contentSize = 64ch`, `wideSize = 78rem`,
  couleurs personnalisées désactivées.
- `add_theme_support('editor-styles')` avec `main.css` dans l'éditeur.
- Blocs `applicab/*` en **ACF Blocks** (`block.json` + `render.php`), pas de build JS ; patterns livrés pour chaque section.

## 4. SEO et GEO

- Un seul H1 par page ; HTML sémantique ; `<details>` fermés gardent leur texte dans le DOM ; onglets : les 5 panneaux
  sont présents dans le DOM (`display:none` sur les inactifs, contenu crawlable).
- JSON-LD : `Organization`, `WebSite`, `SoftwareApplication` (+ `offers`), `FAQPage` (accueil, fonctionnalités, tarifs),
  `BreadcrumbList`, `WebPage`, `BlogPosting`. Une seule source par type en production.
- Blocs réponse directe : « Quel est le meilleur logiciel de gestion pour un cabinet d'avocats ? », « Comment digitaliser
  la gestion d'un cabinet d'avocats ? », « Quelles sont les fonctionnalités d'un logiciel de gestion de cabinet ? ».
- Tableau comparatif générique (tableur / suite bureautique / logiciel métier installé / AppliCab), sans marque.
- `llms.txt` (format llmstxt.org) et `robots.txt` ouverts aux crawlers IA.
- Mockups en texte réel : les noms d'étapes et de fonctions sont indexables, contrairement à des captures d'écran.

## 5. Performance (Core Web Vitals)

- CSS unique (~30 Ko avant minification), pas de framework ni de jQuery, icônes SVG inline.
- JS ~4 Ko en `defer` ; aucune ressource tierce avant interaction (façade vidéo).
- Animations en `transform`/`opacity` uniquement (compositeur), `IntersectionObserver`, `prefers-reduced-motion`.
- Polices auto-hébergées, 2 familles, 6 fichiers max ; images `width`/`height`, `loading="lazy"` sauf LCP.

## 6. Accessibilité et RGAA

**État de la maquette.** Elle applique les critères RGAA 4.1 vérifiables sur un prototype statique : contrastes
AA (≥ 4,5:1 texte courant, ≥ 3:1 grands textes, textes secondaires sur fond sombre ≥ 11:1), un seul H1 et
hiérarchie de titres, landmarks (`header`, `nav` nommées, `main`, `footer`), lien d'évitement, focus visible
(`:focus-visible` 3 px), `aria-expanded` / `aria-controls` sur menu mobile, méga-menus et panneau d'accessibilité,
onglets ARIA pilotables au clavier, mockups en `aria-hidden` avec alternative textuelle, tableaux avec `caption` et
`scope`, formulaire avec `label` et `aria-live`, `<details>` natifs pour la FAQ, `prefers-reduced-motion`,
zoom 200 % sans perte, aucun contenu clé porté par la seule couleur.

**Ce qu'elle ne peut pas garantir.** Le RGAA se vérifie sur un site en production (106 critères, 13 thématiques),
pas sur une maquette. Restent à traiter au portage WordPress : alternatives des vraies images, titres de pages
uniques, langue des passages étrangers, tests lecteur d'écran (NVDA, VoiceOver), navigation clavier sur les
menus WordPress, contraste des contenus saisis par le client dans Gutenberg (à verrouiller via `theme.json`), formulaires
réels (erreurs, aide à la saisie), vidéos sous-titrées avec transcription, et la **déclaration d'accessibilité**
(obligatoire pour les organismes publics et les entreprises de plus de 250 M€ de CA ; recommandée sinon).
Un audit RGAA par un tiers avant mise en ligne est le seul moyen d'afficher un taux de conformité.

**Panneau « Accessibilité » (en-tête).** Préférences mémorisées dans `localStorage`, appliquées avant le premier rendu
par un script inline de 300 octets dans `<head>` (pas de flash), matérialisées par des classes `a11y-*` sur `<html>` :

| Réglage | Classe | Effet |
|---|---|---|
| Contraste renforcé | `a11y-contrast` | Encre noire, filets foncés, sections sombres en noir pur, fonds pâles en blanc, texte en dégradé remplacé par un aplat, liens soulignés, focus 4 px |
| Police plus lisible | `a11y-font` | Lexend (conçue pour la lisibilité), chargée uniquement à l'activation |
| Espacer le texte | `a11y-spacing` | Interligne 1,85, interlettrage 0,04 em, inter-mots 0,16 em (WCAG 1.4.12) |
| Souligner les liens | `a11y-links` | Tous les liens soulignés à 2 px |
| Arrêter les animations | `a11y-motion` | Aucune animation ni transition, marquee figé, onglets sans rotation (WCAG 2.2.2) |
| Taille du texte | `a11y-text-lg` / `a11y-text-xl` | 112,5 % / 125 % de la taille de base, titres du hero plafonnés |

Dans le thème WordPress, le panneau devient `template-parts/a11y-panel.php` inclus par `header.php` ; le CSS et le JS
sont repris tels quels. Il complète les réglages du système (il ne remplace pas `prefers-reduced-motion` ni le zoom
navigateur) et n'utilise aucune surcouche tierce.

## 7. Éléments à fournir / arbitrer côté client

- Verbatims clients réels (les 3 témoignages sont des exemples), logos de cabinets si accord.
- ID de la vidéo YouTube, URL exacte de l'application, URLs sociales, texte définitif du bandeau tarifaire.
- Validation des textes GEO (blocs réponse, FAQ, comparatif) par un avocat de l'équipe.
- Décision phase 2 : pages persona `/vous-etes/…` et pages par fonction `/fonctionnalites/<fonction>/`.
