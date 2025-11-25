# Material Design 3 Component Reference

This document provides detailed specifications for common Material Design 3 components.

## Table of Contents

- [Buttons](#buttons)
- [Cards](#cards)
- [Text Fields](#text-fields)
- [Chips](#chips)
- [Dialogs](#dialogs)
- [FAB (Floating Action Button)](#fab-floating-action-button)
- [Navigation Components](#navigation-components)
- [Lists](#lists)
- [Switches & Checkboxes](#switches--checkboxes)

---

## Buttons

### Button Types

1. **Filled Button** - High emphasis
2. **Outlined Button** - Medium emphasis
3. **Text Button** - Low emphasis
4. **Elevated Button** - Alternative high emphasis
5. **Tonal Button** - Medium-low emphasis

### Filled Button Specifications

```
Height: 40dp
Padding: 24dp horizontal
Corner Radius: Full (9999px)
Typography: Label Large (14px/500)
Elevation: 0dp (rest), 1dp (hover)
State Layer Opacity:
  - Hover: 8%
  - Focus: 12%
  - Pressed: 12%
  - Disabled: Container 12%, Label 38%
```

### Outlined Button

```css
.md-button-outlined {
  background-color: transparent;
  border: 1px solid var(--md-sys-color-outline);
  border-radius: var(--md-shape-corner-full);
  color: var(--md-sys-color-primary);
  padding: 10px 24px;
  min-height: 40px;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.1px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.md-button-outlined:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: var(--md-sys-color-primary);
  opacity: 0.08;
  border-radius: inherit;
}

.md-button-outlined:disabled {
  border-color: rgba(var(--md-sys-color-on-surface-rgb), 0.12);
  color: rgba(var(--md-sys-color-on-surface-rgb), 0.38);
}
```

### Text Button

```css
.md-button-text {
  background-color: transparent;
  border: none;
  border-radius: var(--md-shape-corner-full);
  color: var(--md-sys-color-primary);
  padding: 10px 12px;
  min-height: 40px;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.1px;
  cursor: pointer;
  position: relative;
}

.md-button-text:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: var(--md-sys-color-primary);
  opacity: 0.08;
  border-radius: inherit;
}
```

### Icon Button

```css
.md-icon-button {
  width: 48px;
  height: 48px;
  border: none;
  background: transparent;
  border-radius: var(--md-shape-corner-full);
  color: var(--md-sys-color-on-surface-variant);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
}

.md-icon-button:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: var(--md-sys-color-on-surface-variant);
  opacity: 0.08;
  border-radius: inherit;
}
```

---

## Cards

### Card Types

1. **Elevated Card** - Resting elevation with shadow
2. **Filled Card** - No shadow, filled background
3. **Outlined Card** - Border, no shadow

### Elevated Card Specifications

```
Corner Radius: 12dp (medium)
Elevation: 1dp (rest), 2dp (hover), 1dp (dragged)
Padding: 16dp
Min Width: 200dp
Surface Tint: Primary color at elevation opacity
```

### Card Anatomy

```html
<div class="md-card">
  <div class="md-card-media">
    <!-- Image or video -->
  </div>
  <div class="md-card-content">
    <h3 class="md-card-title">Title</h3>
    <p class="md-card-subtitle">Subtitle</p>
    <p class="md-card-supporting-text">Description text</p>
  </div>
  <div class="md-card-actions">
    <button class="md-button-text">Action 1</button>
    <button class="md-button-text">Action 2</button>
  </div>
</div>
```

### Filled Card

```css
.md-card-filled {
  background-color: var(--md-sys-color-surface-container-highest);
  border-radius: var(--md-shape-corner-medium);
  padding: 16px;
  color: var(--md-sys-color-on-surface);
}
```

### Outlined Card

```css
.md-card-outlined {
  background-color: var(--md-sys-color-surface);
  border: 1px solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-shape-corner-medium);
  padding: 16px;
  color: var(--md-sys-color-on-surface);
}
```

---

## Text Fields

### Text Field Types

1. **Filled** - Default, prominent
2. **Outlined** - Clearer separation

### Filled Text Field Specifications

```
Height: 56dp (single line)
Corner Radius: 4dp (top only)
Typography: Body Large (16px/400) for input
           Body Small (12px/400) for label
Padding: 16dp horizontal, 8dp top, 8dp bottom
Active Indicator: 1dp (rest), 2dp (focus)
```

### Outlined Text Field

```css
.md-text-field-outlined {
  position: relative;
  border: 1px solid var(--md-sys-color-outline);
  border-radius: var(--md-shape-corner-extra-small);
  padding: 16px;
  background-color: transparent;
}

.md-text-field-outlined:focus-within {
  border-width: 2px;
  border-color: var(--md-sys-color-primary);
  padding: 15px; /* Compensate for border width */
}

.md-text-field-outlined .md-text-field-label {
  position: absolute;
  top: -8px;
  left: 12px;
  background-color: var(--md-sys-color-surface);
  padding: 0 4px;
  color: var(--md-sys-color-on-surface-variant);
  font-size: 12px;
}

.md-text-field-outlined:focus-within .md-text-field-label {
  color: var(--md-sys-color-primary);
}
```

### Text Field with Helper Text

```html
<div class="md-text-field-container">
  <div class="md-text-field-filled">
    <label for="email" class="md-text-field-label">Email</label>
    <input
      type="email"
      id="email"
      class="md-text-field-input"
      aria-describedby="email-helper"
    >
    <div class="md-text-field-active-indicator"></div>
  </div>
  <span id="email-helper" class="md-text-field-supporting-text">
    Enter your email address
  </span>
</div>
```

```css
.md-text-field-supporting-text {
  display: block;
  margin-top: 4px;
  padding: 0 16px;
  color: var(--md-sys-color-on-surface-variant);
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.4px;
}

.md-text-field-container.error .md-text-field-supporting-text {
  color: var(--md-sys-color-error);
}
```

---

## Chips

### Chip Types

1. **Assist Chip** - Suggestions or actions
2. **Filter Chip** - Toggleable filters
3. **Input Chip** - User-entered content
4. **Suggestion Chip** - Recommended content

### Assist Chip Specifications

```
Height: 32dp
Corner Radius: 8dp (small)
Padding: 8dp horizontal (with icon), 16dp (text only)
Typography: Label Large (14px/500)
Elevation: 0dp (flat) or 1dp (elevated variant)
```

### Filter Chip (Selected State)

```css
.md-chip-filter {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 32px;
  padding: 0 16px;
  border-radius: var(--md-shape-corner-small);
  border: 1px solid var(--md-sys-color-outline);
  background-color: transparent;
  color: var(--md-sys-color-on-surface-variant);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.1px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.md-chip-filter:hover {
  background-color: rgba(var(--md-sys-color-on-surface-variant-rgb), 0.08);
}

.md-chip-filter.selected {
  background-color: var(--md-sys-color-secondary-container);
  border-color: transparent;
  color: var(--md-sys-color-on-secondary-container);
}

.md-chip-filter.selected::before {
  content: '✓';
  display: inline-block;
  width: 18px;
  height: 18px;
}
```

### Input Chip with Remove

```html
<div class="md-chip-input">
  <span class="md-chip-label">Chip text</span>
  <button class="md-chip-remove" aria-label="Remove">
    <svg width="18" height="18">
      <path d="M6 6L12 12M12 6L6 12" stroke="currentColor" stroke-width="2"/>
    </svg>
  </button>
</div>
```

---

## Dialogs

### Dialog Specifications

```
Corner Radius: 28dp (extra-large)
Elevation: 3dp
Min Width: 280dp
Max Width: 560dp
Padding: 24dp
Surface Tint: Primary
```

### Full-width Dialog (Mobile)

```html
<div class="md-dialog-scrim">
  <div class="md-dialog" role="dialog" aria-labelledby="dialog-title">
    <div class="md-dialog-header">
      <h2 id="dialog-title" class="md-dialog-title">Dialog Title</h2>
      <button class="md-icon-button" aria-label="Close">
        <svg>...</svg>
      </button>
    </div>
    <div class="md-dialog-content">
      <p>Dialog content goes here.</p>
    </div>
    <div class="md-dialog-actions">
      <button class="md-button-text">Cancel</button>
      <button class="md-button-filled">Confirm</button>
    </div>
  </div>
</div>
```

```css
.md-dialog-scrim {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.32);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.md-dialog {
  background-color: var(--md-sys-color-surface-container-high);
  border-radius: var(--md-shape-corner-extra-large);
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.3),
              0px 4px 8px 3px rgba(0, 0, 0, 0.15);
  padding: 24px;
  min-width: 280px;
  max-width: 560px;
  max-height: 90vh;
  overflow: auto;
}

.md-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.md-dialog-title {
  font-size: 24px;
  line-height: 32px;
  font-weight: 400;
  color: var(--md-sys-color-on-surface);
}

.md-dialog-content {
  color: var(--md-sys-color-on-surface-variant);
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.25px;
  margin-bottom: 24px;
}

.md-dialog-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
```

---

## FAB (Floating Action Button)

### FAB Types

1. **FAB** - Standard size
2. **Small FAB** - Compact size
3. **Large FAB** - Prominent size
4. **Extended FAB** - With text label

### FAB Specifications

```
Size: 56x56dp (standard), 40x40dp (small), 96x96dp (large)
Corner Radius: 16dp (large), 12dp (medium), 12dp (small)
Elevation: 3dp (rest), 4dp (hover)
Icon Size: 24dp
Surface Tint: Primary
```

### Standard FAB

```css
.md-fab {
  width: 56px;
  height: 56px;
  border-radius: var(--md-shape-corner-large);
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.3),
              0px 4px 8px 3px rgba(0, 0, 0, 0.15);
  transition: box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.md-fab:hover {
  box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.3),
              0px 6px 10px 4px rgba(0, 0, 0, 0.15);
}

.md-fab svg {
  width: 24px;
  height: 24px;
}
```

### Extended FAB

```html
<button class="md-fab-extended">
  <svg width="24" height="24">...</svg>
  <span>Create</span>
</button>
```

```css
.md-fab-extended {
  height: 56px;
  padding: 0 16px;
  border-radius: var(--md-shape-corner-large);
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  border: none;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.3),
              0px 4px 8px 3px rgba(0, 0, 0, 0.15);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.1px;
}
```

---

## Navigation Components

### Bottom Navigation Bar

```
Height: 80dp
Item Width: Min 80dp, Max 168dp
Typography: Label Medium (12px/500)
Icon Size: 24dp
Active Indicator: 32dp wide, 16dp tall pill shape
```

```css
.md-bottom-nav {
  display: flex;
  height: 80px;
  background-color: var(--md-sys-color-surface-container);
  border-top: 1px solid var(--md-sys-color-outline-variant);
}

.md-bottom-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: transparent;
  border: none;
  color: var(--md-sys-color-on-surface-variant);
  cursor: pointer;
  position: relative;
  min-width: 80px;
  max-width: 168px;
}

.md-bottom-nav-item.active {
  color: var(--md-sys-color-on-secondary-container);
}

.md-bottom-nav-item.active::before {
  content: '';
  position: absolute;
  top: 12px;
  width: 64px;
  height: 32px;
  background-color: var(--md-sys-color-secondary-container);
  border-radius: 16px;
  z-index: -1;
}

.md-bottom-nav-icon {
  width: 24px;
  height: 24px;
}

.md-bottom-nav-label {
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.5px;
}
```

### Navigation Rail (Tablet)

```
Width: 80dp
Item Height: 56dp
Typography: Label Medium (12px/500)
Icon Size: 24dp
```

```css
.md-nav-rail {
  width: 80px;
  background-color: var(--md-sys-color-surface-container);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0;
  gap: 12px;
}

.md-nav-rail-item {
  width: 56px;
  height: 56px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: transparent;
  border: none;
  border-radius: var(--md-shape-corner-large);
  color: var(--md-sys-color-on-surface-variant);
  cursor: pointer;
  position: relative;
}

.md-nav-rail-item.active {
  background-color: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}
```

### Navigation Drawer (Desktop)

```
Width: 360dp (standard), 256dp (modal)
Surface: Surface Container Low
Item Height: 56dp
```

```css
.md-nav-drawer {
  width: 360px;
  background-color: var(--md-sys-color-surface-container-low);
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 12px;
  overflow-y: auto;
}

.md-nav-drawer-item {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 56px;
  padding: 0 16px;
  border-radius: var(--md-shape-corner-full);
  background: transparent;
  border: none;
  color: var(--md-sys-color-on-surface-variant);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.1px;
  cursor: pointer;
  text-align: left;
}

.md-nav-drawer-item:hover {
  background-color: rgba(var(--md-sys-color-on-surface-variant-rgb), 0.08);
}

.md-nav-drawer-item.active {
  background-color: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}
```

---

## Lists

### List Item Specifications

```
Height: 56dp (one-line), 72dp (two-line), 88dp (three-line)
Padding: 16dp horizontal
Leading/Trailing Element: 24dp or 56dp width
Typography: Body Large (16px) for primary text
           Body Medium (14px) for secondary text
```

### One-line List Item

```html
<ul class="md-list">
  <li class="md-list-item">
    <div class="md-list-item-leading">
      <svg width="24" height="24">...</svg>
    </div>
    <div class="md-list-item-content">
      <span class="md-list-item-label">List item</span>
    </div>
  </li>
</ul>
```

```css
.md-list {
  list-style: none;
  padding: 8px 0;
  margin: 0;
}

.md-list-item {
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 56px;
  padding: 8px 16px;
  cursor: pointer;
  position: relative;
}

.md-list-item:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: var(--md-sys-color-on-surface);
  opacity: 0.08;
}

.md-list-item-leading {
  width: 24px;
  height: 24px;
  color: var(--md-sys-color-on-surface-variant);
}

.md-list-item-label {
  color: var(--md-sys-color-on-surface);
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.5px;
}
```

### Two-line List Item

```html
<li class="md-list-item md-list-item-two-line">
  <div class="md-list-item-leading">
    <img src="avatar.jpg" alt="" class="md-avatar">
  </div>
  <div class="md-list-item-content">
    <span class="md-list-item-label">Primary text</span>
    <span class="md-list-item-supporting-text">Secondary text</span>
  </div>
  <div class="md-list-item-trailing">
    <span class="md-body-small">12:30</span>
  </div>
</li>
```

```css
.md-list-item-two-line {
  min-height: 72px;
  align-items: flex-start;
  padding: 12px 16px;
}

.md-list-item-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.md-list-item-supporting-text {
  color: var(--md-sys-color-on-surface-variant);
  font-size: 14px;
  line-height: 20px;
  letter-spacing: 0.25px;
}

.md-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
```

---

## Switches & Checkboxes

### Switch Specifications

```
Track Width: 52dp
Track Height: 32dp
Handle Diameter: 16dp (unselected), 24dp (selected)
Corner Radius: Full
```

```css
.md-switch {
  position: relative;
  display: inline-block;
  width: 52px;
  height: 32px;
}

.md-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.md-switch-track {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--md-sys-color-surface-container-highest);
  border: 2px solid var(--md-sys-color-outline);
  border-radius: 16px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.md-switch-handle {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 8px;
  bottom: 8px;
  background-color: var(--md-sys-color-outline);
  border-radius: 50%;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

input:checked + .md-switch-track {
  background-color: var(--md-sys-color-primary);
  border-color: transparent;
}

input:checked + .md-switch-track .md-switch-handle {
  transform: translateX(20px);
  width: 24px;
  height: 24px;
  bottom: 4px;
  background-color: var(--md-sys-color-on-primary);
}
```

### Checkbox

```css
.md-checkbox {
  position: relative;
  width: 18px;
  height: 18px;
}

.md-checkbox input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.md-checkbox-box {
  position: absolute;
  top: 0;
  left: 0;
  height: 18px;
  width: 18px;
  border: 2px solid var(--md-sys-color-on-surface-variant);
  border-radius: 2px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.md-checkbox input:checked ~ .md-checkbox-box {
  background-color: var(--md-sys-color-primary);
  border-color: var(--md-sys-color-primary);
}

.md-checkbox-checkmark {
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid var(--md-sys-color-on-primary);
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.md-checkbox input:checked ~ .md-checkbox-box .md-checkbox-checkmark {
  display: block;
}
```

---

## Additional Component Notes

### Snackbar

```
Height: 48dp (single line), 68dp+ (multi-line)
Width: 344dp (mobile), min 344dp (desktop)
Corner Radius: 4dp
Elevation: 6dp
Duration: 4-10 seconds
```

### Tooltip

```
Corner Radius: 4dp
Padding: 4dp 8dp
Typography: Body Small (12px)
Background: Inverse Surface
Color: Inverse On-Surface
```

### Progress Indicators

**Linear:**
- Height: 4dp
- Corner Radius: 2dp (full)

**Circular:**
- Stroke Width: 4dp
- Size: 48dp (default), 24dp (small)

---

**Reference**: All specifications are from [Material Design 3 Guidelines](https://m3.material.io/components).
