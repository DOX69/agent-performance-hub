---
name: web-app-vibe-coding
description: "Expert in building modern, fluid, and aesthetic web interfaces (Vibe Coding) using React, Tailwind, and Framer Motion. Focuses on UX and visual delight."
---

# Skill: Web App Vibe Coding (React / Tailwind / Framer Motion)

## Objectifs
- Créer des interfaces web modernes, fluides et esthétiques ("Vibe Coding").
- Prioriser l'expérience utilisateur (UX) et le "delight" visuel.
- Code React fonctionnel, performant et propre.

## Stack Ciblée
- **Framework**: React 18+ (Next.js App Router préféré)
- **Styling**: Tailwind CSS v3/v4
- **Animation**: Framer Motion
- **Icons**: Lucide React / Phosphor Icons
- **Components**: Shadcn UI (radix-ui based) ou custom components minimalistes

## Patterns Recommandés
- **Composants Fonctionnels**: Hooks pour la logique, composants purs pour l'affichage.
- **Tailwind Utility-First**: Utiliser les classes utilitaires pour la rapidité et la cohérence.
- **Animations Subtiles**: Transitions au hover, apparition progressive (fadeIn), micro-interactions.
- **Responsive Design**: Mobile-first par défaut.
- **Dark Mode**: Support natif via Tailwind `dark:` classes.

## Exemples de Prompts Recommandés
- "Crée une landing page moderne pour une SaaS AI avec un hero section animé et des gradients subtils."
- "Génère un composant de carte produit avec un effet de hover 'glassmorphism' et une animation d'entrée."
- "Refactorise ce dashboard pour utiliser une palette de couleurs monochrome et des ombres douces."

## Anti-patterns à Éviter
- **Over-engineering**: Pas de Redux pour un simple toggle.
- **Inline Styles**: Utiliser Tailwind ou CSS Modules, pas de `style={{...}}` sauf pour des valeurs dynamiques complexes.
- **Animations Lourdes**: Éviter les animations qui bloquent le thread principal ou causent du layout thrashing.
- **Div Soup**: Utiliser des éléments sémantiques HTML (`<section>`, `<article>`, `<nav>`).

## Ressources Externes
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Framer Motion Docs](https://www.framer.com/motion/)
- [Shadcn UI](https://ui.shadcn.com/)
- [Vercel Design](https://vercel.com/design)
