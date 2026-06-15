---
name: Calm Urgency Transit System
colors:
  surface: '#fcf8fa'
  surface-dim: '#dcd9db'
  surface-bright: '#fcf8fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f5'
  surface-container: '#f0edef'
  surface-container-high: '#eae7e9'
  surface-container-highest: '#e4e2e4'
  on-surface: '#1b1b1d'
  on-surface-variant: '#45464d'
  inverse-surface: '#303032'
  inverse-on-surface: '#f3f0f2'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#0058be'
  on-secondary: '#ffffff'
  secondary-container: '#2170e4'
  on-secondary-container: '#fefcff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#25005a'
  on-tertiary-container: '#9863ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#eaddff'
  tertiary-fixed-dim: '#d2bbff'
  on-tertiary-fixed: '#25005a'
  on-tertiary-fixed-variant: '#5a00c6'
  background: '#fcf8fa'
  on-background: '#1b1b1d'
  surface-variant: '#e4e2e4'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 12px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-margin: 16px
  gutter: 12px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style

The design system is built on the philosophy of **Calm Urgency**. In a chaotic transit environment like Chennai, the UI must provide a sense of control and clarity while facilitating rapid decision-making. The aesthetic is **Corporate Modern with a High-Contrast Edge**, prioritizing legibility and cognitive load reduction.

The target audience ranges from daily commuters on the CMRL Metro to tourists navigating the MTC bus network. The UI evokes a premium, reliable, and functional emotional response through deep colors and structured layouts. Visual weight is used strategically to highlight the "Fastest" or "Cheapest" routes, ensuring users can glance, decide, and move.

## Colors

This design system utilizes a high-contrast palette to differentiate between transit modes and trip priorities. 

- **Primary & Accent:** Deep Navy (#0F172A) provides a professional foundation, while Electric Blue (#3B82F6) acts as the primary action color.
- **Mood Palettes:** Used exclusively for route recommendation cards. The background colors are ultra-light (50-100 weight) to ensure black text remains accessible while the accent colors provide a clear visual "tag."
- **Transit Identities:** These are immutable colors associated with specific transport types in Chennai, used for line identifiers, icons, and route polyline maps.

## Typography

The typography system relies on **Inter** for its exceptional legibility and systematic weight distribution. 

- **Hierarchy:** Headlines use a semi-bold weight (600) to stand out against dense map data. Body text remains at 400 for long-form information (like safety instructions).
- **Tamil Fallback:** For all multilingual interfaces, Noto Sans Tamil must be used, ensuring it matches the vertical alignment and optical weight of Inter.
- **Micro-copy:** Labels (sm/md) are used for "Time to Arrival" and "Platform Numbers," requiring a medium weight (500) to ensure clarity even at small scales.

## Layout & Spacing

This design system follows a **4px grid** for strict mathematical alignment. 

- **Grid Model:** A 12-column fluid grid is used for desktop/tablet, while a 4-column layout is used for mobile. 
- **Margins:** A standard 16px side margin is maintained across mobile devices to prevent content from touching the screen edges.
- **Journey Legs:** Vertical spacing between transit legs in a route overview should be 12px (3 units) to imply a connected path without overcrowding.

## Elevation & Depth

The system uses **Tonal Layers** rather than heavy shadows to maintain a "flat but deep" feel.

- **Base Layer:** The map or background remains at elevation 0.
- **Surface Cards:** Route cards use a 1px border (#E2E8F0) with no shadow, keeping the interface clean and scannable.
- **Floating Elements:** Only high-priority interactive elements, such as the "Locate Me" button or the bottom navigation bar, receive a subtle ambient shadow (Blur 8px, Y-offset 4px, Opacity 0.05).
- **Overlays:** Full-screen modals or search sheets use a backdrop blur (8px) to maintain the context of the user's location on the map.

## Shapes

The shape language is sophisticated and varied to distinguish between different content types.

- **Standard Elements:** Buttons and inputs use a base 8px (0.5rem) radius.
- **Information Containers:** Mood-based route cards use a 16px radius to feel friendly and approachable. 
- **Connectors:** Journey leg segments use a 12px radius, creating a softer flow for transit step visualizations.
- **Badges:** All chips and status indicators use a fully rounded (pill-shaped) 99px radius to distinguish them from interactive buttons.

## Components

- **Buttons:** Primary buttons are Solid Deep Navy (#0F172A) with white text. Secondary buttons use a transparent background with an Electric Blue border.
- **Mood Cards:** These are the centerpiece. They use the Mood Palette colors (e.g., Emerald for Cheapest). The header should contain the mood label in a `label-sm` badge, with the price and duration in `headline-md`.
- **Journey Leg List:** Vertical connectors using the Transit Identity colors. Each node in the list should be an icon representing the mode (Bus, Metro, etc.).
- **Input Fields:** Search bars should be prominent, with a 1px border and a 16px corner radius. The focus state uses an Electric Blue 2px ring.
- **Chips:** Used for transit filters (e.g., "A/C Only," "Direct"). Unselected: Gray bg; Selected: Electric Blue bg with white text.
- **Icons:** Use **Tabler Icons (Outline)** at a 2px stroke width. Icons for transit modes should be encased in a circular container using the specific mode's color.