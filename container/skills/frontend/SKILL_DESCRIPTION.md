# Frontend Development (Senior Frontend)

## Overview

The Frontend Development skill provides comprehensive tools and frameworks for building modern, performant web applications using React, Next.js, TypeScript, and TailwindCSS. This skill enables frontend engineers to create scalable component architectures, optimize bundle sizes, implement best practices for performance, and deliver exceptional user experiences. It combines component generation, bundle analysis, and performance optimization with deep expertise in React patterns and Next.js features.

## Who Should Use This Skill

- **Frontend Engineers** building modern web applications
- **Senior Frontend Developers** architecting UI systems
- **React Developers** specializing in React and Next.js
- **UI Engineers** implementing design systems
- **Tech Leads** establishing frontend standards
- **Fullstack Engineers** working on the frontend layer
- **Performance Engineers** optimizing web performance
- **Engineering Managers** ensuring frontend quality

## Purpose and Use Cases

Use this skill when you need to:
- Build React components with best practices
- Optimize Next.js applications for performance
- Implement responsive and accessible UIs
- Create reusable component libraries
- Optimize bundle sizes and load times
- Implement state management patterns
- Build server-side rendered applications
- Optimize for Core Web Vitals
- Implement code splitting strategies
- Create performant animations
- Build progressive web apps (PWAs)
- Implement design systems

**Keywords that trigger this skill:** React, Next.js, frontend, TypeScript, TailwindCSS, components, performance optimization, bundle size, state management, responsive design, accessibility, web vitals

## What's Included

### Component Generator

**Component Templates:**
- **Basic Component** - Simple functional component
- **Form Component** - with validation and submission
- **Data Display Component** - tables, lists, cards
- **Layout Component** - navigation, headers, footers
- **Page Component** - Next.js page with data fetching
- **API Route** - Next.js API endpoint
- **Hook** - Custom React hook
- **Context Provider** - React context with provider

**Generation Features:**
```bash
# Generate React component
python scripts/component_generator.py UserProfile \
  --type functional \
  --with-typescript \
  --with-tests \
  --with-storybook \
  --styling tailwind

# Generate form component
python scripts/component_generator.py ContactForm \
  --type form \
  --validation zod \
  --with-react-hook-form

# Generate Next.js page
python scripts/component_generator.py Dashboard \
  --type page \
  --data-fetching server-side \
  --with-layout

# Generate custom hook
python scripts/component_generator.py useAuth \
  --type hook \
  --with-tests
```

**Generated Component Structure:**
```typescript
// components/UserProfile/UserProfile.tsx
import { FC } from 'react';
import { UserProfileProps } from './UserProfile.types';
import styles from './UserProfile.module.css';

export const UserProfile: FC<UserProfileProps> = ({ user, onEdit }) => {
  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={onEdit}>Edit Profile</button>
    </div>
  );
};

// components/UserProfile/UserProfile.types.ts
export interface UserProfileProps {
  user: {
    name: string;
    email: string;
  };
  onEdit: () => void;
}

// components/UserProfile/UserProfile.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('renders user information', () => {
    const user = { name: 'John Doe', email: 'john@example.com' };
    render(<UserProfile user={user} onEdit={() => {}} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', () => {
    const onEdit = jest.fn();
    const user = { name: 'John Doe', email: 'john@example.com' };
    render(<UserProfile user={user} onEdit={onEdit} />);

    fireEvent.click(screen.getByText('Edit Profile'));
    expect(onEdit).toHaveBeenCalled();
  });
});

// components/UserProfile/index.ts
export { UserProfile } from './UserProfile';
export type { UserProfileProps } from './UserProfile.types';
```

### Bundle Analyzer

**Analysis Capabilities:**
- Bundle size analysis by route
- Dependency size breakdown
- Tree-shaking effectiveness
- Code splitting opportunities
- Duplicate dependencies detection
- Third-party library impact
- CSS bundle analysis
- Image optimization opportunities
- Font loading analysis

**Bundle Optimization:**
```bash
# Analyze bundle
python scripts/bundle_analyzer.py /path/to/project \
  --output bundle-report.html

# Find optimization opportunities
python scripts/bundle_analyzer.py /path/to/project \
  --find-duplicates \
  --find-unused \
  --suggest-splits

# Compare bundles
python scripts/bundle_analyzer.py /path/to/project \
  --compare-with baseline.json \
  --threshold 5%
```

**Bundle Report Example:**
```
BUNDLE ANALYSIS REPORT
======================

Total Bundle Size: 487 KB (gzipped)
-----------------------------------

Size Breakdown:
  JavaScript: 342 KB (70%)
  CSS: 89 KB (18%)
  Images: 56 KB (12%)

By Route:
  / (homepage): 245 KB
  /dashboard: 312 KB ⚠️ (exceeds 300 KB)
  /profile: 198 KB
  /settings: 267 KB

Largest Dependencies:
---------------------
1. react-dom: 89 KB
2. @tanstack/react-query: 45 KB
3. date-fns: 34 KB (only 3 functions used - tree-shaking opportunity)
4. lodash: 28 KB (not tree-shakeable - use lodash-es)
5. chart.js: 156 KB ⚠️ (lazy load recommended)

Issues Found:
-------------

[HIGH] Dashboard route exceeds 300 KB
  Route: /dashboard
  Size: 312 KB
  Recommendation: Implement code splitting for ChartComponent (156 KB)
  Potential Savings: 150 KB

[HIGH] Duplicate lodash installations
  Packages: lodash@4.17.21, lodash-es@4.17.21
  Size: 56 KB (28 KB × 2)
  Recommendation: Standardize on lodash-es for tree-shaking

[MEDIUM] date-fns not tree-shaking
  Current: 34 KB (importing entire library)
  Used functions: format, parseISO, differenceInDays
  Recommendation: Import specific functions
  Potential Savings: 28 KB

[MEDIUM] Unused CSS in production
  Unused TailwindCSS classes: 15 KB
  Recommendation: Configure PurgeCSS properly

[LOW] Image optimization opportunities
  5 images > 100 KB without optimization
  Recommendation: Use next/image for automatic optimization
  Potential Savings: 20 KB

Recommendations:
----------------
Priority 1: Lazy load chart.js (saves 150 KB)
Priority 2: Fix duplicate lodash (saves 28 KB)
Priority 3: Tree-shake date-fns (saves 28 KB)
Priority 4: Configure PurgeCSS (saves 15 KB)

Total Potential Savings: 221 KB (45% reduction)
Target Bundle Size: 266 KB
```

### Frontend Scaffolder

**Project Setup:**
```bash
# Initialize React + TypeScript + TailwindCSS project
python scripts/frontend_scaffolder.py init my-app \
  --template react-ts-tailwind \
  --features routing,state-management,forms

# Initialize Next.js App Router project
python scripts/frontend_scaffolder.py init my-nextjs-app \
  --template nextjs-14-app-router \
  --features auth,seo,analytics,pwa

# Add feature to existing project
python scripts/frontend_scaffolder.py feature authentication \
  --with-ui \
  --provider next-auth
```

**Performance Optimization:**
```bash
# Run comprehensive performance audit
python scripts/frontend_scaffolder.py optimize \
  --analyze-bundle \
  --analyze-images \
  --analyze-fonts \
  --lighthouse

# Apply performance optimizations
python scripts/frontend_scaffolder.py optimize \
  --auto-fix \
  --lazy-load-images \
  --optimize-fonts \
  --add-caching
```

## How It Works

### Component Generation Workflow

**Step 1: Define Component Requirements**
```bash
# Interactive component generation
python scripts/component_generator.py --interactive

# Or specify directly
python scripts/component_generator.py ProductCard \
  --type functional \
  --props "product:Product,onAddToCart:Function" \
  --styling tailwind \
  --with-tests \
  --with-storybook
```

**Step 2: Generated Component**
```typescript
// components/ProductCard/ProductCard.tsx
import { FC } from 'react';
import { ProductCardProps } from './ProductCard.types';
import { Button } from '@/components/ui/Button';
import { formatCurrency } from '@/lib/utils';

export const ProductCard: FC<ProductCardProps> = ({ product, onAddToCart }) => {
  return (
    <div className="rounded-lg border border-gray-200 p-4 shadow-sm hover:shadow-md transition-shadow">
      <img
        src={product.imageUrl}
        alt={product.name}
        className="w-full h-48 object-cover rounded-md mb-4"
      />
      <h3 className="text-lg font-semibold mb-2">{product.name}</h3>
      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
        {product.description}
      </p>
      <div className="flex items-center justify-between">
        <span className="text-xl font-bold text-gray-900">
          {formatCurrency(product.price)}
        </span>
        <Button onClick={() => onAddToCart(product)}>Add to Cart</Button>
      </div>
    </div>
  );
};

// components/ProductCard/ProductCard.types.ts
export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
}

export interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
}

// components/ProductCard/ProductCard.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ProductCard } from './ProductCard';

const meta: Meta<typeof ProductCard> = {
  title: 'Components/ProductCard',
  component: ProductCard,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof ProductCard>;

export const Default: Story = {
  args: {
    product: {
      id: '1',
      name: 'Wireless Headphones',
      description: 'High-quality wireless headphones with noise cancellation',
      price: 99.99,
      imageUrl: 'https://example.com/headphones.jpg',
    },
    onAddToCart: (product) => console.log('Add to cart:', product),
  },
};

export const LongDescription: Story = {
  args: {
    product: {
      id: '2',
      name: 'Smart Watch',
      description:
        'Advanced smart watch with health tracking, GPS, and long battery life. Perfect for fitness enthusiasts and tech lovers alike.',
      price: 299.99,
      imageUrl: 'https://example.com/watch.jpg',
    },
    onAddToCart: (product) => console.log('Add to cart:', product),
  },
};
```

### Bundle Optimization Workflow

**Step 1: Analyze Current Bundle**
```bash
# Generate bundle analysis
python scripts/bundle_analyzer.py /path/to/project \
  --output bundle-report.html \
  --save-baseline baseline.json
```

**Step 2: Identify Optimization Opportunities**
```
OPTIMIZATION OPPORTUNITIES
==========================

Quick Wins (High Impact, Low Effort):
--------------------------------------

1. Lazy Load Chart Component (Impact: 150 KB saved)
   Current: import Chart from 'chart.js'
   Replace with:
     const Chart = dynamic(() => import('chart.js'), {
       loading: () => <p>Loading chart...</p>,
       ssr: false
     })

2. Use lodash-es instead of lodash (Impact: 28 KB saved)
   Current: import { debounce } from 'lodash'
   Replace with: import debounce from 'lodash-es/debounce'

3. Tree-shake date-fns (Impact: 28 KB saved)
   Current: import * as dateFns from 'date-fns'
   Replace with: import { format, parseISO } from 'date-fns'

4. Enable PurgeCSS (Impact: 15 KB saved)
   Add to tailwind.config.js:
     content: ['./src/**/*.{js,jsx,ts,tsx}']

Medium Effort (High Impact):
-----------------------------

5. Implement Route-Based Code Splitting (Impact: 80 KB saved)
   Split dashboard, admin, and analytics routes

6. Optimize Image Loading (Impact: 45 KB saved)
   Convert images to WebP, implement lazy loading

Total Quick Wins: 221 KB savings (4 hours of work)
Total With Medium Effort: 346 KB savings (2 days of work)
```

**Step 3: Apply Optimizations**
```bash
# Apply automated fixes
python scripts/bundle_analyzer.py /path/to/project \
  --auto-fix \
  --optimize imports,images,css

# Verify improvements
python scripts/bundle_analyzer.py /path/to/project \
  --compare-with baseline.json
```

**Step 4: Measure Impact**
```
OPTIMIZATION RESULTS
====================

Before: 487 KB (gzipped)
After: 266 KB (gzipped)
Reduction: 221 KB (45%)

Core Web Vitals Impact:
  LCP: 2.8s → 1.6s (43% faster)
  FCP: 1.4s → 0.9s (36% faster)
  TBT: 320ms → 180ms (44% faster)

Performance Score:
  Before: 72/100
  After: 91/100
  Improvement: +19 points

Lighthouse Metrics:
  ✓ All metrics in "Good" range
  ✓ No high-priority issues
  ✓ PWA ready
```

### Performance Optimization Workflow

**Step 1: Run Lighthouse Audit**
```bash
python scripts/frontend_scaffolder.py audit \
  --url https://staging.example.com \
  --output lighthouse-report.html
```

**Step 2: Review Performance Metrics**
```
LIGHTHOUSE PERFORMANCE AUDIT
==============================

Performance Score: 78/100 (Needs Improvement)

Core Web Vitals:
----------------
LCP (Largest Contentful Paint): 3.2s ⚠️ (target: < 2.5s)
FID (First Input Delay): 85ms ✓ (target: < 100ms)
CLS (Cumulative Layout Shift): 0.18 ⚠️ (target: < 0.1)

Other Metrics:
--------------
FCP (First Contentful Paint): 1.8s (target: < 1.8s) ✓
TTI (Time to Interactive): 4.5s ⚠️ (target: < 3.8s)
TBT (Total Blocking Time): 450ms ⚠️ (target: < 200ms)
Speed Index: 3.1s (target: < 3.4s) ✓

Issues Found:
-------------

[HIGH] Large Render-Blocking Resources
  - main.js: 342 KB (blocks for 1.2s)
  - styles.css: 89 KB (blocks for 0.4s)
  Recommendation: Code split, inline critical CSS

[HIGH] Cumulative Layout Shift (CLS)
  Elements shifting: Product images, navbar
  Recommendation: Add width/height to images, reserve space for navbar

[MEDIUM] Unused JavaScript
  - 156 KB of unused code shipped
  Recommendation: Tree-shake dependencies, code split

[MEDIUM] Unoptimized Images
  - 8 images not using modern formats (WebP/AVIF)
  - Total potential savings: 120 KB
  Recommendation: Use next/image or responsive images

[LOW] Missing Cache Headers
  - Static assets not cached efficiently
  Recommendation: Add cache headers for JS, CSS, images

Optimization Plan:
------------------
Week 1:
  - Add width/height to all images (fixes CLS)
  - Implement code splitting for routes
  - Inline critical CSS

Week 2:
  - Convert images to WebP
  - Implement lazy loading for below-fold content
  - Add cache headers

Expected Performance Score After: 92/100
```

**Step 3: Implement Optimizations**
```typescript
// Before: Regular import
import Chart from 'chart.js';

// After: Dynamic import
const Chart = dynamic(() => import('chart.js'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});

// Before: No image optimization
<img src="/product.jpg" alt="Product" />

// After: Next.js Image component
<Image
  src="/product.jpg"
  alt="Product"
  width={400}
  height={300}
  loading="lazy"
  placeholder="blur"
/>

// Before: All CSS loaded
import './styles.css';

// After: CSS Modules with critical CSS extraction
import styles from './Component.module.css';
```

## Technical Details

### React Patterns

**Component Composition:**
```typescript
// Higher-Order Component (HOC)
export const withAuth = <P extends object>(
  Component: React.ComponentType<P>
) => {
  return (props: P) => {
    const { user } = useAuth();
    if (!user) return <LoginPage />;
    return <Component {...props} />;
  };
};

// Render Props
export const DataFetcher = ({ render, url }) => {
  const { data, loading, error } = useFetch(url);
  return render({ data, loading, error });
};

// Compound Components
export const Tabs = ({ children }) => {
  const [activeTab, setActiveTab] = useState(0);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
};
Tabs.Tab = TabComponent;
Tabs.Panel = PanelComponent;
```

### Next.js App Router Features

**Server Components:**
```typescript
// app/dashboard/page.tsx (Server Component)
async function Dashboard() {
  const data = await fetchDashboardData();

  return (
    <div>
      <h1>Dashboard</h1>
      <ClientChart data={data} />
    </div>
  );
}

// Client Component for interactivity
'use client';
function ClientChart({ data }) {
  return <Chart data={data} />;
}
```

**Streaming with Suspense:**
```typescript
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<SkeletonChart />}>
        <SlowDataComponent />
      </Suspense>
      <Suspense fallback={<SkeletonTable />}>
        <SlowTableComponent />
      </Suspense>
    </div>
  );
}
```

### Performance Optimization Techniques

**Code Splitting:**
```typescript
// Route-based splitting (automatic in Next.js)
import dynamic from 'next/dynamic';

// Component-based splitting
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false,
});

// Library splitting
const Chart = dynamic(() => import('chart.js').then((mod) => mod.Chart), {
  ssr: false,
});
```

**Memoization:**
```typescript
// React.memo for component memoization
export const ExpensiveComponent = React.memo(({ data }) => {
  // Only re-renders if data changes
  return <div>{/* Expensive rendering */}</div>;
});

// useMemo for expensive calculations
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// useCallback for function stability
const handleClick = useCallback(() => {
  console.log('Clicked');
}, []);
```

## Best Practices

### Component Design Best Practices

**Do:**
- Keep components small and focused (single responsibility)
- Use TypeScript for type safety
- Write tests for components
- Use composition over inheritance
- Extract reusable logic into custom hooks
- Use meaningful component and prop names
- Add prop validation
- Document complex components

**Don't:**
- Create god components (too many responsibilities)
- Use index as key in lists
- Mutate props
- Over-optimize prematurely
- Forget accessibility (a11y)
- Skip error boundaries
- Ignore performance metrics

### Performance Best Practices

**Do:**
- Measure before optimizing (use Lighthouse, Web Vitals)
- Implement code splitting
- Lazy load below-the-fold content
- Optimize images (use next/image)
- Use proper caching strategies
- Monitor bundle size
- Implement virtual scrolling for long lists
- Use CDN for static assets

**Don't:**
- Load everything upfront
- Ship large dependencies without tree-shaking
- Ignore Core Web Vitals
- Skip image optimization
- Forget about mobile performance
- Over-use client-side rendering
- Ignore layout shifts

### Accessibility Best Practices

**Do:**
- Use semantic HTML
- Add ARIA labels where needed
- Ensure keyboard navigation
- Provide alt text for images
- Maintain sufficient color contrast
- Support screen readers
- Test with accessibility tools
- Follow WCAG guidelines

**Don't:**
- Rely solely on color for information
- Create keyboard traps
- Use div/span for interactive elements
- Forget focus indicators
- Skip skip-to-content links
- Ignore ARIA best practices

## Integration Points

This skill integrates with:
- **React Frameworks:** React, Next.js, Remix, Gatsby
- **State Management:** Zustand, Redux Toolkit, Jotai, React Query
- **Styling:** TailwindCSS, styled-components, CSS Modules, Sass
- **UI Libraries:** shadcn/ui, Radix UI, Headless UI, Chakra UI
- **Forms:** React Hook Form, Formik, Zod validation
- **Testing:** Jest, React Testing Library, Playwright, Cypress
- **Build Tools:** Vite, Webpack, Turbopack, esbuild
- **Deployment:** Vercel, Netlify, AWS Amplify, Cloudflare Pages

## Common Challenges and Solutions

### Challenge: Large Bundle Sizes
**Solution:** Implement code splitting, tree-shake dependencies, lazy load heavy components, use bundle analyzer, remove unused dependencies, optimize images

### Challenge: Poor Core Web Vitals
**Solution:** Optimize LCP (optimize images, preload critical resources), reduce CLS (reserve space for dynamic content, use consistent image dimensions), improve FID/INP (reduce JavaScript execution, use web workers)

### Challenge: State Management Complexity
**Solution:** Use React Query for server state, Zustand for simple client state, keep state close to where it's used, avoid prop drilling with context, use atomic state management

### Challenge: Slow Re-renders
**Solution:** Use React.memo, useMemo, and useCallback appropriately, avoid creating new objects/arrays in render, use proper key props, implement virtualization for long lists

### Challenge: Accessibility Issues
**Solution:** Use semantic HTML, test with screen readers, implement keyboard navigation, use accessibility linting tools, follow WCAG guidelines, test with real users

### Challenge: Complex Form Validation
**Solution:** Use React Hook Form with Zod schema validation, implement field-level validation, provide clear error messages, use proper HTML5 validation attributes, test edge cases
