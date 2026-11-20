import { defineShikiSetup } from '@slidev/types'

// Juraci's deck shows code light-on-dark (#191919 boxes) on white and black
// slides alike, so both schemes use the same dark theme.
export default defineShikiSetup(() => ({
  themes: { dark: 'github-dark-default', light: 'github-dark-default' },
}))
