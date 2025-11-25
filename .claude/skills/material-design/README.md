# Material Design Skill

A comprehensive Claude Code skill for implementing Google Material Design 3 (Material You) components and patterns.

## Skill Structure

```
material-design/
├── SKILL.md                          # Main skill file with instructions
├── README.md                         # This file
├── reference.md                      # Detailed component specifications
├── examples/                         # Ready-to-use HTML examples
│   ├── layout-app-bar.html          # Top app bar with FAB
│   ├── form-material-inputs.html    # Form with text fields and validation
│   ├── card-grid.html               # Responsive card grid layout
│   └── bottom-navigation.html       # Bottom navigation with tabs
└── templates/                        # Reusable CSS templates
    ├── button-variants.css          # All button types (filled, outlined, text, etc.)
    └── design-tokens.css            # Complete MD3 design tokens (colors, typography, etc.)
```

## What This Skill Does

This skill helps you:
- **Build Material Design 3 components** from scratch
- **Implement Material You theming** with dynamic colors
- **Follow accessibility guidelines** (WCAG 2.1 AA)
- **Create responsive layouts** for mobile, tablet, and desktop
- **Apply proper motion and animations** with Material easing curves
- **Use semantic design tokens** for consistent styling

## When It Activates

Claude will automatically use this skill when you mention:
- Material Design, Material UI, MUI, Material 3, Material You
- Component names: buttons, cards, text fields, FAB, navigation
- Design concepts: elevation, color system, typography, theming
- Frameworks: React (MUI), Vue (Vuetify), Android Material Components

## Quick Start

### Example 1: Create a Material Button

**Prompt:** "Create a Material Design filled button"

**Result:** Claude will provide HTML + CSS for a properly styled Material Design 3 button with:
- Correct colors, typography, and shape
- State layers (hover, focus, pressed)
- Accessibility attributes
- Disabled state

### Example 2: Build a Form

**Prompt:** "Create a Material Design form with email and password fields"

**Result:** Claude will generate a complete form with:
- Filled or outlined text fields
- Floating labels
- Helper text and error states
- Proper validation and ARIA attributes

### Example 3: Setup a Theme

**Prompt:** "Setup Material Design 3 color tokens for my app"

**Result:** Claude will provide:
- CSS custom properties for all color roles
- Light and dark theme support
- Dynamic color generation guidance
- Usage examples

## Resources

### Examples
All examples are in the `examples/` directory. Open them in a browser to see live Material Design 3 components.

### Templates
Use templates in `templates/` as starting points:
- `design-tokens.css` - Copy into your project for instant Material Design 3 theming
- `button-variants.css` - All button types ready to use

### Reference
See `reference.md` for detailed specifications:
- Component measurements (height, padding, radius)
- State layer opacities
- Typography scale
- Elevation levels
- Navigation patterns

## Supported Frameworks

This skill provides implementations for:
- **Vanilla HTML/CSS**: Copy-paste ready code
- **React (MUI)**: Using Material-UI components
- **Vue (Vuetify)**: Using Vuetify 3+
- **Android**: Material Components for Android

## Design Token Coverage

Complete Material Design 3 tokens included:
- ✅ Colors (Primary, Secondary, Tertiary, Error, Surface variants)
- ✅ Typography (Display, Headline, Title, Body, Label scales)
- ✅ Shape (Corner radius tokens)
- ✅ Elevation (5 levels with proper shadows)
- ✅ Motion (Duration and easing curves)
- ✅ State layers (Hover, focus, pressed opacities)

## Official Material Design Resources

- [Material Design 3 Guidelines](https://m3.material.io/)
- [Material Theme Builder](https://m3.material.io/theme-builder)
- [Material Design Icons](https://fonts.google.com/icons)
- [Figma Material 3 Kit](https://www.figma.com/community/file/1035203688168086460)

## Tips for Using This Skill

1. **Be specific about framework**: Mention if you're using React/MUI, Vue/Vuetify, or vanilla HTML/CSS
2. **Ask for examples**: Request to see the example files for reference
3. **Customize colors**: Provide your brand color and Claude will generate a full Material Design 3 palette
4. **Check accessibility**: Claude will automatically ensure WCAG 2.1 AA compliance
5. **Request variations**: Ask for different component variants (filled, outlined, text buttons, etc.)

## License

This skill provides guidance and templates based on publicly available Material Design 3 specifications from Google.
