# React Builder (Artifacts Builder)

## Overview

The React Builder skill provides a complete suite of tools for creating elaborate, multi-component HTML artifacts using modern frontend technologies. It enables the creation of complex web applications with React 18, TypeScript, Tailwind CSS, and shadcn/ui components, all bundled into a single shareable HTML file.

## Who Should Use This Skill

- **Developers** building complex interactive web tools and applications
- **Product Teams** creating sophisticated prototypes or internal tools
- **UI/UX Designers** needing production-quality component implementations
- **Technical Teams** requiring multi-page applications with state management and routing

## Purpose and Use Cases

Use this skill when you need to:
- Build complex artifacts requiring multiple components and state management
- Create applications that need routing between different views
- Implement sophisticated UI with shadcn/ui component library (40+ pre-installed components)
- Develop interactive tools with TypeScript for type safety
- Bundle complete applications into a single distributable HTML file

**Note:** This skill is NOT for simple single-file HTML/JSX artifacts. Use it only when complexity demands proper component architecture and modern tooling.

## What's Included

### Complete Modern Stack

**Core Technologies:**
- **React 18** - Latest React with concurrent features
- **TypeScript** - Type-safe development
- **Vite** - Fast development server and build tool
- **Parcel** - HTML bundler for single-file output
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - 40+ pre-installed premium components

**Pre-configured Features:**
- Path aliases (@/) for clean imports
- Node 18+ compatibility
- Optimized build pipeline
- Single HTML bundle output

### shadcn/ui Components Library

Access to 40+ professionally designed, accessible components including:
- Buttons, Cards, Dialogs, Dropdowns
- Forms, Inputs, Select menus
- Tables, Tabs, Tooltips
- Navigation, Sidebar, Breadcrumbs
- Charts, Progress indicators
- And many more...

### Development Workflow

**Initialization Script:**
```bash
bash scripts/init-artifact.sh <project-name>
```
Creates a complete project structure with all dependencies configured

**Bundle Script:**
```bash
bash scripts/bundle-artifact.sh
```
Compiles the entire application into a single `bundle.html` file

## How It Works

### Step-by-Step Workflow

**1. Initialize Project**
```bash
bash scripts/init-artifact.sh my-app
```
- Creates project directory structure
- Installs React 18, TypeScript, Vite, Tailwind CSS
- Pre-installs all 40+ shadcn/ui components
- Configures path aliases and build tools

**2. Develop Your Application**
- Edit the generated code in the project directory
- Use TypeScript for type safety
- Import shadcn/ui components from `@/components/ui`
- Style with Tailwind CSS utility classes
- Add routing, state management, and complex logic as needed

**3. Bundle for Distribution**
```bash
bash scripts/bundle-artifact.sh
```
- Builds the complete application
- Bundles everything into a single HTML file
- Output: `bundle.html` in the project directory

**4. Share the Artifact**
- Present the `bundle.html` file to the user
- File is completely self-contained
- Works in any modern web browser
- No server or installation required

**5. Optional Testing**
- Test the artifact in a browser
- Verify all components and interactions work
- Ensure responsive design functions properly

### Project Structure

After initialization, you'll have:
```
project-name/
├── src/
│   ├── components/
│   │   └── ui/          # 40+ shadcn/ui components
│   ├── App.tsx          # Main application component
│   └── main.tsx         # Entry point
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

## Technical Details

### Capabilities

**Complex State Management:**
- React hooks (useState, useEffect, useContext, etc.)
- Custom hooks for shared logic
- State management libraries if needed

**Routing:**
- Client-side routing for multi-page applications
- React Router or similar routing solutions

**Component Architecture:**
- Modular, reusable components
- Component composition and inheritance
- Type-safe props with TypeScript

**Styling:**
- Tailwind CSS utility classes
- Responsive design utilities
- Custom theme configuration
- Dark mode support

### System Requirements

- Node.js 18 or higher
- Modern terminal/command line access
- Sufficient disk space for node_modules

### Performance Considerations

- Bundle size is minimized through tree-shaking
- Vite provides fast HMR (Hot Module Replacement) during development
- Parcel creates optimized production bundles
- All dependencies are bundled, so no external requests needed

## When to Use vs. When NOT to Use

### ✅ Use This Skill When:
- Building complex multi-component applications
- Need routing between different views
- Require state management across components
- Want to use shadcn/ui's professional components
- Building interactive tools with sophisticated logic
- Type safety is important (TypeScript)

### ❌ Do NOT Use This Skill When:
- Creating simple single-file HTML/JSX artifacts
- Building basic static pages
- Simple visualizations or demos
- Quick prototypes without complex interactions

For simple artifacts, use regular HTML/JSX with inline JavaScript instead.

## Best Practices

- Use TypeScript's type system to prevent runtime errors
- Leverage shadcn/ui components instead of building from scratch
- Organize components logically in the src/components directory
- Use Tailwind CSS utilities for consistent styling
- Test the bundle.html thoroughly before sharing
- Keep components modular and reusable
- Follow React best practices for hooks and lifecycle
- Use path aliases (@/) for cleaner imports