module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'react', 'react-hooks'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended'
  ],
  env: {
    browser: true,
    node: true,
    es2021: true,
  },
  rules: {
    // Turn off for React 17+ JSX transform
    'react/react-in-jsx-scope': 'off',
    // Allow @ts-ignore comments
    '@typescript-eslint/ban-ts-comment': 'off',
    'react/prop-types': 'off',
    '@typescript-eslint/no-unused-vars': ['warn', { 'argsIgnorePattern': '^_', 'varsIgnorePattern': '^_' }],
    // Add more custom rules here if needed
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
