# Web Development Rules

This document outlines the standard best practices that AI agents must follow when writing web applications, generating UI/UX components, or managing web assets.

## 1. Design Aesthetics & UX
> [!IMPORTANT]
> If a web application looks simple and basic, it is considered a failure. 
> - **Visual Excellence:** Build interfaces that feel premium. Avoid generic default colors. Use curated HSL palettes, smooth gradients, and sleek dark modes.
> - **Modern Typography:** Prioritize modern fonts (e.g., Inter, Roboto, Outfit) over standard browser defaults.
> - **Micro-animations:** Incorporate subtle transitions and hover effects to make the application feel responsive and dynamic. Glassmorphism and modern UI trends should be utilized where appropriate.
> - **No Placeholders:** When an image is needed for a demonstration, use generative image tools (`generate_image`) rather than inserting empty boxes or broken image tags.

## 2. Technology Stack Enforcement
> [!NOTE]
> - **Core:** Structure with Semantic HTML5 and logic with modular JavaScript/TypeScript.
> - **Styling:** Use raw, Vanilla CSS for maximum flexibility. **Do not use TailwindCSS unless explicitly requested by the user.**
> - **Frameworks:** Default to native web components unless the user specifically asks for complex logic, in which case Next.js or Vite configurations should be instantiated.

## 3. SEO & Accessibility Best Practices
> [!TIP]
> Always automatically implement these without asking:
> - **Semantic Tags:** Use `<nav>`, `<main>`, `<article>`, `<aside>`, and `<section>` correctly.
> - **Heading Structure:** Ensure there is exactly one `<h1>` per page, and subsequent headings (`<h2>`, `<h3>`) follow a strict logical hierarchy.
> - **Meta Information:** Populate `<title>` tags and `<meta name="description">` accurately based on the page context.
> - **Accessibility (WCAG):** Ensure sufficient color contrast, provide `alt` attributes for all images, and ensure all interactive elements (buttons, inputs) are keyboard navigable.
> - **Unique Identifiers:** Assign unique, descriptive IDs to interactive elements to facilitate browser automation testing (e.g., Playwright scripts).

## 4. Performance Optimization
- **Core Web Vitals:** Keep the First Input Delay (FID) and Cumulative Layout Shift (CLS) in mind. Set explicit `width` and `height` attributes on images to prevent layout shifting.
- **Lazy Loading:** Use `loading="lazy"` on off-screen assets and implement code-splitting in larger framework projects.
