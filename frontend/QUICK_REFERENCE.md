# Quick Reference: Button & Card Colors

## 🎨 Color System Overview

Your app now has a complete button and card color system with:

### ✅ What's Included

1. **8 Button Variants** (each with 3 states + highlight color)
   - Default (neutral gray)
   - Primary (blue)
   - Secondary (purple)
   - Accent (orange)
   - Success (green)
   - Warning (yellow)
   - Error (red)
   - Ghost (transparent)

2. **Card Colors** (3 states + 6 highlight variants)
   - Normal, Hover, Active states
   - Highlight colors matching each button variant

3. **Auto Dark Mode**
   - All colors adapt to light/dark theme
   - Proper contrast in both modes

## 🚀 Quick Start

### Simple Button Examples

```tsx
// Primary action button
<button className="bg-btn-primary hover:bg-btn-primary-hover text-btn-primary-text px-4 py-2 rounded-lg">
  Save
</button>

// Danger/delete button
<button className="bg-btn-error hover:bg-btn-error-hover text-btn-error-text px-4 py-2 rounded-lg">
  Delete
</button>

// Success button
<button className="bg-btn-success hover:bg-btn-success-hover text-btn-success-text px-4 py-2 rounded-lg">
  Confirm
</button>
```

### Simple Card Examples

```tsx
// Basic card
<div className="bg-card-bg border border-card-border rounded-lg p-4 shadow-card-shadow">
  <h3 className="text-text font-semibold">Title</h3>
  <p className="text-text-muted">Content</p>
</div>

// Interactive card
<div className="
  bg-card-bg hover:bg-card-bg-hover
  border border-card-border hover:border-card-border-hover
  shadow-card-shadow hover:shadow-card-shadow-hover
  rounded-lg p-4 cursor-pointer transition-all
">
  Hover me!
</div>

// Highlighted/selected card
<div className="bg-card-highlight-primary border-2 border-primary rounded-lg p-4">
  Selected item
</div>
```

## 📋 All Available Tailwind Classes

### Button Background Colors
- `bg-btn-default`, `bg-btn-default-hover`, `bg-btn-default-active`
- `bg-btn-primary`, `bg-btn-primary-hover`, `bg-btn-primary-active`
- `bg-btn-secondary`, `bg-btn-secondary-hover`, `bg-btn-secondary-active`
- `bg-btn-accent`, `bg-btn-accent-hover`, `bg-btn-accent-active`
- `bg-btn-success`, `bg-btn-success-hover`, `bg-btn-success-active`
- `bg-btn-warning`, `bg-btn-warning-hover`, `bg-btn-warning-active`
- `bg-btn-error`, `bg-btn-error-hover`, `bg-btn-error-active`
- `bg-btn-ghost`, `bg-btn-ghost-hover`, `bg-btn-ghost-active`

### Button Text Colors
- `text-btn-default-text`
- `text-btn-primary-text`
- `text-btn-secondary-text`
- `text-btn-accent-text`
- `text-btn-success-text`
- `text-btn-warning-text`
- `text-btn-error-text`
- `text-btn-ghost-text`

### Button Highlights (for badges)
- `bg-btn-primary-highlight`
- `bg-btn-secondary-highlight`
- `bg-btn-accent-highlight`
- `bg-btn-success-highlight`
- `bg-btn-warning-highlight`
- `bg-btn-error-highlight`

### Card Colors
- `bg-card-bg`, `bg-card-bg-hover`, `bg-card-bg-active`
- `border-card-border`, `border-card-border-hover`
- `shadow-card-shadow`, `shadow-card-shadow-hover`

### Card Highlights
- `bg-card-highlight-primary`
- `bg-card-highlight-secondary`
- `bg-card-highlight-accent`
- `bg-card-highlight-success`
- `bg-card-highlight-warning`
- `bg-card-highlight-error`

## 🎯 Common Patterns

### Button with Badge
```tsx
<button className="relative bg-btn-primary hover:bg-btn-primary-hover text-btn-primary-text px-4 py-2 rounded-lg">
  Messages
  <span className="absolute -top-2 -right-2 bg-btn-error-highlight text-btn-error-text text-xs px-2 py-1 rounded-full">
    5
  </span>
</button>
```

### Card Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
  <div className="bg-card-bg border border-card-border rounded-lg p-4 hover:shadow-card-shadow-hover transition-all">
    Card 1
  </div>
  <div className="bg-card-bg border border-card-border rounded-lg p-4 hover:shadow-card-shadow-hover transition-all">
    Card 2
  </div>
  <div className="bg-card-bg border border-card-border rounded-lg p-4 hover:shadow-card-shadow-hover transition-all">
    Card 3
  </div>
</div>
```

### Selected State Management
```tsx
function SelectableCard() {
  const [selected, setSelected] = useState(false);
  
  return (
    <div 
      onClick={() => setSelected(!selected)}
      className={`
        rounded-lg p-4 border-2 cursor-pointer transition-all
        ${selected 
          ? 'bg-card-highlight-primary border-primary' 
          : 'bg-card-bg border-card-border hover:bg-card-bg-hover'
        }
      `}
    >
      {selected ? '✓ Selected' : 'Click to select'}
    </div>
  );
}
```

## 🎨 Live Demo

Click the "Show Button & Card Showcase" button in the app to see all variants in action!

## 🔧 Runtime Customization

Change any button or card color at runtime:

```tsx
import { useSettings } from './context/SettingsContext';

function ColorPicker() {
  const { setSetting } = useSettings();
  
  return (
    <input 
      type="color" 
      onChange={(e) => setSetting('btnPrimary', e.target.value)}
      defaultValue="#0ea5e9"
    />
  );
}
```

Changes persist across page reloads via localStorage! 🎉
