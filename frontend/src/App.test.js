import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

test('renders loading indicator initially', () => {
  const { getByText } = render(<App />);
  const loadingElement = getByText(/Loading/i);
  expect(loadingElement).toBeInTheDocument();
});
