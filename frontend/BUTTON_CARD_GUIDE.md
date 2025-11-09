# Button & Card Color System Guide

This guide shows you how to use all the button and card colors with their different states.

## 📦 Available Button Variants

Each button variant has 4 states: **normal**, **hover**, **active**, and **highlight** (for badges/indicators).

### Usage with Tailwind Classes

```tsx
// Primary Button
<button className="bg-btn-primary hover:bg-btn-primary-hover active:bg-btn-primary-active text-btn-primary-text">
  Primary Action
</button>

// Secondary Button
<button className="bg-btn-secondary hover:bg-btn-secondary-hover active:bg-btn-secondary-active text-btn-secondary-text">
  Secondary Action
</button>

// Accent Button
<button className="bg-btn-accent hover:bg-btn-accent-hover active:bg-btn-accent-active text-btn-accent-text">
  Accent Action
</button>

// Success Button
<button className="bg-btn-success hover:bg-btn-success-hover active:bg-btn-success-active text-btn-success-text">
  Success Action
</button>

// Warning Button
<button className="bg-btn-warning hover:bg-btn-warning-hover active:bg-btn-warning-active text-btn-warning-text">
  Warning Action
</button>

// Error/Danger Button
<button className="bg-btn-error hover:bg-btn-error-hover active:bg-btn-error-active text-btn-error-text">
  Delete
</button>

// Default/Neutral Button
<button className="bg-btn-default hover:bg-btn-default-hover active:bg-btn-default-active text-btn-default-text">
  Cancel
</button>

// Ghost Button (transparent)
<button className="bg-btn-ghost hover:bg-btn-ghost-hover active:bg-btn-ghost-active text-btn-ghost-text border border-btn-ghost-border">
  Ghost Button
</button>
```

### Usage with Inline Styles (for dynamic buttons)

```tsx
<button
  style={{
    backgroundColor: 'var(--btn-primary)',
    color: 'var(--btn-primary-text)'
  }}
  onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--btn-primary-hover)'}
  onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'var(--btn-primary)'}
>
  Hover Me
</button>
```

## 🏷️ Highlight/Badge Colors

Each button variant has a corresponding highlight color for badges, indicators, or notifications:

```tsx
// Badge using primary highlight
<span className="bg-btn-primary-highlight text-btn-primary-text px-2 py-1 rounded text-xs">
  New
</span>

// Notification dot
<span className="w-2 h-2 rounded-full bg-btn-error-highlight" />
```

## 🎴 Card Colors

Cards have 3 states: **normal**, **hover**, and **active** (clicked/selected).

### Basic Card

```tsx
<div className="bg-card-bg border border-card-border rounded-lg p-4 shadow-card-shadow">
  <h3 className="text-text font-semibold">Card Title</h3>
  <p className="text-text-muted">Card content</p>
</div>
```

### Interactive Card (with hover)

```tsx
<div className="
  bg-card-bg 
  hover:bg-card-bg-hover 
  border border-card-border 
  hover:border-card-border-hover 
  rounded-lg p-4 
  shadow-card-shadow 
  hover:shadow-card-shadow-hover
  transition-all duration-200
  cursor-pointer
">
  <h3 className="text-text font-semibold">Hover Me</h3>
  <p className="text-text-muted">I change on hover!</p>
</div>
```

### Selected/Highlighted Cards

Use highlight backgrounds when a card is selected or in a special state:

```tsx
// Primary highlighted card
<div className="bg-card-highlight-primary border-2 border-primary rounded-lg p-4">
  <h3 className="text-text font-semibold">Selected Card</h3>
</div>

// Success highlighted card
<div className="bg-card-highlight-success border-2 border-success rounded-lg p-4">
  <h3 className="text-text font-semibold">Success State</h3>
</div>

// Error highlighted card
<div className="bg-card-highlight-error border-2 border-error rounded-lg p-4">
  <h3 className="text-text font-semibold">Error State</h3>
</div>
```

## 🎨 All Available CSS Variables

### Buttons
| Variant | Normal | Hover | Active | Text | Highlight |
|---------|--------|-------|--------|------|-----------|
| Default | `--btn-default` | `--btn-default-hover` | `--btn-default-active` | `--btn-default-text` | - |
| Primary | `--btn-primary` | `--btn-primary-hover` | `--btn-primary-active` | `--btn-primary-text` | `--btn-primary-highlight` |
| Secondary | `--btn-secondary` | `--btn-secondary-hover` | `--btn-secondary-active` | `--btn-secondary-text` | `--btn-secondary-highlight` |
| Accent | `--btn-accent` | `--btn-accent-hover` | `--btn-accent-active` | `--btn-accent-text` | `--btn-accent-highlight` |
| Success | `--btn-success` | `--btn-success-hover` | `--btn-success-active` | `--btn-success-text` | `--btn-success-highlight` |
| Warning | `--btn-warning` | `--btn-warning-hover` | `--btn-warning-active` | `--btn-warning-text` | `--btn-warning-highlight` |
| Error | `--btn-error` | `--btn-error-hover` | `--btn-error-active` | `--btn-error-text` | `--btn-error-highlight` |
| Ghost | `--btn-ghost` | `--btn-ghost-hover` | `--btn-ghost-active` | `--btn-ghost-text` | - |

### Cards
| Property | Variable |
|----------|----------|
| Background | `--card-bg` |
| Background (hover) | `--card-bg-hover` |
| Background (active) | `--card-bg-active` |
| Border | `--card-border` |
| Border (hover) | `--card-border-hover` |
| Shadow | `--card-shadow` |
| Shadow (hover) | `--card-shadow-hover` |

### Card Highlights
| Type | Variable |
|------|----------|
| Primary | `--card-highlight-primary` |
| Secondary | `--card-highlight-secondary` |
| Accent | `--card-highlight-accent` |
| Success | `--card-highlight-success` |
| Warning | `--card-highlight-warning` |
| Error | `--card-highlight-error` |

## 🌓 Dark Mode

All button and card colors automatically adjust when `.dark` class is present on the `<html>` element. The colors are optimized for both light and dark themes with proper contrast ratios.

## 🎯 Best Practices

1. **Button Hierarchy**: Use Primary for main actions, Secondary for supporting actions, Default for cancel/neutral
2. **Consistent States**: Always include hover states for interactive elements
3. **Card Selection**: Use highlight backgrounds + border color change to show selection
4. **Accessibility**: All color combinations maintain WCAG AA contrast ratios
5. **Transitions**: Add `transition-all duration-200` for smooth state changes

## 🔧 Customization

Change button/card colors at runtime using the `useSettings()` hook:

```tsx
import { useSettings } from './context/SettingsContext';

function CustomizeButton() {
  const { setSetting } = useSettings();
  
  return (
    <input 
      type="color" 
      onChange={(e) => setSetting('btnPrimary', e.target.value)}
    />
  );
}
```

This updates the CSS variable `--btn-primary` dynamically!
