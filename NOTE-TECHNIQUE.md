# Note technique — Refonte AppliCab Avocats

Maquette codée haute-fidélité (HTML/CSS/JS sans dépendance) destinée à la présentation client,
puis au portage dans un **thème WordPress sur-mesure** (PHP + Gutenberg, sans page builder).

Pages livrées :

| Page | Fichier | Template WordPress cible |
|---|---|---|
| Accueil | `index.html` | `front-page.php` |
| Fonctionnalités & tarifs | `fonctionnalites-tarifs.html` | `page-fonctionnalites.php` (ou `page.php` + blocs) |
| Article de blog | `blog/article.html` | `single.php` |
| Fichier IA génératives | `llms.txt` | fichier statique à la racine (ou route `rewrite` WP) |

## 1. Direction artistique appliquée

- **Palette** conservée du site actuel et resserrée en tokens (`assets/css/main.css`, section 1) :
  sable `#F1ECE2`, brun titre `#46392E`, olive `#5B7A1F`, olive profond `#3D5516`, vert clair `#A9C24A`,
  jaune avocat `#DCCB4F` (accent rare), terre cuite `#A4492F` (illustration uniquement).
  Tous les couples texte/fond utilisés respectent le niveau AA (olive sur blanc : 4,9:1 ; blanc sur olive profond : 9,8:1).
- **Typographie** : Martel 700/800 pour les titres (continuité avec le serif actuel, échelle plus affirmée),
  Poppins 400/500/600 pour le corps. Échelle fluide via `clamp()`.
- **Grilles** : bento 12 colonnes (`.bento`, `.span-*`), en-têtes de section asymétriques (`.section-head--split`),
  frise horizontale, tableau comparatif, FAQ en `<details>` natifs.
- **Micro-interactions** : en-tête collant avec ombre au défilement, liens fléchés, léger décalage vertical à
  l'apparition (jamais d'opacité 0 : le contenu reste lisible sans JS et pour les crawlers), `prefers-reduced-motion` respecté.
- Supprimé par rapport à Divi : ombres portées lourdes, dégradés génériques, icônes par défaut, sliders JS, CSS inline massif.

## 2. Découpage WordPress : template PHP fixe vs blocs Gutenberg

### 2.1 Éléments communs (PHP fixe)

| Élément | Implémentation |
|---|---|
| Bandeau d'annonce | `header.php`, texte + lien + date de fin dans un **groupe d'options ACF** (`options page`), masqué automatiquement après la date. |
| En-tête + navigation | `header.php`, `wp_nav_menu('principal')`, bouton CTA = dernier item du menu avec la classe `nav-cta` (walker ou filtre `nav_menu_css_class`). Le bouton mobile et le JS de `assets/js/main.js` sont repris tels quels. |
| Bandeau CTA final | `template-parts/cta-band.php`, contenu (titre, texte, 2 boutons) dans les **options ACF**, réutilisé sur toutes les pages. |
| Pied de page | `footer.php` : 3 zones de menus (`wp_nav_menu`), formulaire newsletter branché sur le plugin existant (MailPoet/Brevo) via shortcode, mentions © dynamiques. |
| Fil d'Ariane | `template-parts/breadcrumb.php` + JSON-LD `BreadcrumbList` généré en PHP (ou délégué à Yoast/Rank Math si déjà en place — **ne pas dupliquer**). |
| `<head>` | `wp_head()` ; `title`/`meta description` gérés par le plugin SEO déjà utilisé sur les articles ; polices **auto-hébergées** dans `assets/fonts/` avec `font-display: swap` et `<link rel="preload">` sur les 2 fichiers critiques. |

### 2.2 Page d'accueil (`front-page.php`)

| Section de la maquette | Type | Détail |
|---|---|---|
| Hero | **PHP fixe + ACF** | Champs : surtitre, titre (H1, avec `<em>` sur la partie mise en avant), chapô, 2 boutons, liste de preuves, badge récompense. La mascotte est un SVG inline dans le template. |
| Chiffres clés | **Bloc réutilisable `applicab/kpis`** (ACF Block) | Répéteur valeur/libellé, 2 à 4 items, rendu `<dl class="kpis">`. |
| Réponse directe (GEO) | **Bloc `applicab/reponse`** | Une question (H2) + une réponse courte en texte brut. Rendu `.answer`. Réutilisable sur toute page. |
| Présentation (bento) | **Bloc `applicab/benefices`** | InnerBlocks avec un bloc enfant `applicab/carte` (icône, titre, texte, liste, lien, variante de couleur, largeur `span-5/7`). |
| Fonctionnalités + vidéo | **Bloc `applicab/fonctionnalites-apercu`** | Liste à coches (bloc liste natif stylé) + **façade vidéo** : champ « ID YouTube », l'iframe n'est injectée qu'au clic (CWV). |
| Méthode en 4 étapes | **Bloc `applicab/etapes`** | Répéteur titre/texte, rendu `<ol class="steps">` numéroté par CSS. |
| Cas d'usage | **Bloc `applicab/cas-usage`** | Même bloc enfant `applicab/carte` sur fond sombre (`.section--dark`). |
| Notre histoire | **PHP fixe + ACF répéteur** (année, titre, texte, `is_now`) | Rendu `<ol class="timeline">` ; remplace le slider Divi. |
| Tarifs | **Bloc `applicab/tarifs`** | Les prix sont saisis **une seule fois** dans les options ACF et lus par le bloc (accueil et page tarifs toujours synchronisés) ; le même champ alimente le JSON-LD `offers`. |
| FAQ | **Bloc `applicab/faq`** | Répéteur question/réponse, rendu `<details>` natifs (texte dans le DOM). Le bloc **génère lui-même le JSON-LD `FAQPage`** à partir de ses champs. |
| Derniers articles | **PHP fixe** | `WP_Query` 3 derniers articles, `template-parts/post-card.php`. |

### 2.3 Page Fonctionnalités & tarifs (`page-fonctionnalites.php` ou `page.php`)

Tout le contenu est composé avec les blocs ci-dessus + :

| Section | Type |
|---|---|
| En-tête de page (H1, chapô, boutons) | PHP fixe (`the_title`, champ ACF « chapô ») |
| Grille des 6 fonctionnalités | Bloc `applicab/fonctionnalite` (enfant de `applicab/benefices`), avec ancre `id` par carte pour le maillage interne |
| Tableau comparatif | **Bloc tableau natif Gutenberg** + style de bloc « Comparatif » (`register_block_style`) ; la colonne AppliCab reçoit la classe `is-us` via la classe CSS additionnelle du bloc. Aucun contenu en image. |
| Tarifs, FAQ, CTA | Blocs `applicab/tarifs`, `applicab/faq`, part `cta-band` |

### 2.4 Article de blog (`single.php`)

Objectif : **ne rien perdre du SEO existant**. Les articles actuels sont conservés tels quels (même slug, même `title`,
même meta description via le plugin SEO, mêmes H2/H3, mêmes liens internes). Seul l'habillage change.

| Élément | Implémentation |
|---|---|
| En-tête | PHP fixe : fil d'Ariane, catégorie principale, `the_title()` en H1, `the_excerpt()` en chapô, auteur, `the_date()`, temps de lecture calculé (`str_word_count / 200`). |
| Image à la une | `the_post_thumbnail()` avec `sizes`/`srcset` natifs, `loading="eager"` + `fetchpriority="high"` (image LCP), formats WebP/AVIF via `add_theme_support` + plugin d'optimisation. |
| Sommaire | Généré automatiquement à partir des H2/H3 de `the_content` (filtre PHP ajoutant des `id` + liste), affiché en colonne collante. Désactivable par case ACF. |
| Corps | `the_content()` : blocs natifs (paragraphe, titres, listes, citation, tableau, image). Styles dans `.prose`. Un **style de bloc « Encart »** sur le bloc Groupe (`callout`, `callout--olive`) pour les CTA contextuels. |
| Étiquettes, partage, auteur, précédent/suivant | PHP fixe (`the_tags`, `get_the_author_meta`, `previous_post_link`). |
| Articles liés | `WP_Query` même catégorie, 3 items. |
| Données structurées | `BlogPosting` + `BreadcrumbList` : déléguées au plugin SEO s'il les émet déjà, sinon générées dans `single.php` sur le modèle du prototype. |

### 2.5 Gutenberg : réglages du thème

- `theme.json` : palette (tokens de la section 1), échelle typographique, espacements, `layout.contentSize = 62ch`,
  `wideSize = 76rem`, désactivation des couleurs/dégradés personnalisés pour garder la charte.
- `functions.php` : `add_theme_support('editor-styles')` avec `main.css` chargé dans l'éditeur pour un WYSIWYG fidèle.
- Blocs `applicab/*` déclarés en **ACF Blocks** (`block.json` + `render.php`), ce qui évite un build JS et reste éditable
  par le client. Ils sont marqués `"reusable": true` là où le contenu se répète (tarifs, FAQ, CTA).
- Patterns (`register_block_pattern`) livrés : « Section présentation », « Section fonctionnalités », « FAQ », « Comparatif ».

## 3. SEO et GEO

- Un seul H1 par page, hiérarchie H2/H3 logique, HTML sémantique (`header`, `nav`, `main`, `article`, `section`, `footer`).
- JSON-LD présent dans le prototype : `Organization`, `WebSite`, `SoftwareApplication` (+ `offers` 59 € / 39 €),
  `FAQPage`, `BreadcrumbList`, `WebPage`, `BlogPosting`. En production, **une seule source** par type (thème ou plugin SEO).
- Blocs « réponse directe » (`.answer`) en texte brut, réponses FAQ autonomes et citables, tableau comparatif en HTML.
- Aucun contenu clé derrière du JS : les `<details>` fermés gardent leur texte dans le DOM.
- `llms.txt` à la racine (format llmstxt.org) ; `robots.txt` ouvert aux crawlers IA (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)
  sauf décision contraire du client.
- Sitemap XML : celui du plugin SEO existant.

## 4. Performance (Core Web Vitals)

- CSS unique (~20 Ko avant minification), pas de framework, pas de jQuery, pas de police icônes (SVG inline).
- JS de 2 Ko chargé en `defer` ; façade vidéo : aucune ressource YouTube avant le clic.
- Polices auto-hébergées, `font-display: swap`, 2 graisses Martel + 4 Poppins maximum.
- Images : `width`/`height` déclarés, `loading="lazy"` sauf image LCP, WebP/AVIF, `srcset`.
- Aucun CSS inline généré par un builder ; `wp_enqueue_style` avec version hash pour le cache.

## 5. Accessibilité

- Contrastes AA, focus visible (`:focus-visible` bleu à fort contraste), lien d'évitement, `aria-current`, `aria-expanded` sur le menu,
  libellés sur toutes les icônes sociales, tableau avec `caption`/`scope`, formulaire avec `label` et message `aria-live`.
- Navigation clavier complète ; `prefers-reduced-motion` neutralise les transitions.

## 6. Éléments à fournir / arbitrer côté client

- ID de la vidéo YouTube de présentation ; URL exacte d'accès à l'application ; URLs des réseaux sociaux.
- Validation des textes GEO (blocs réponse, FAQ, comparatif) par un avocat de l'équipe.
- Photo d'illustration des articles (remplace les placeholders SVG).
- Confirmation de l'augmentation tarifaire au 1er octobre 2026 pour le bandeau.
