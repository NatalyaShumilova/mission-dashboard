import React from 'react';
import { render, screen } from '@testing-library/react';
import ErrorMessage from './ErrorMessage';

describe('ErrorMessage', () => {
  test('renders error message with default title', () => {
    render(<ErrorMessage message="Something went wrong" />);
    
    expect(screen.getByText('Error')).toBeInTheDocument();
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
  });

  test('renders error message with custom title', () => {
    render(<ErrorMessage title="Custom Error" message="Custom message" />);
    
    expect(screen.getByText('Custom Error')).toBeInTheDocument();
    expect(screen.getByText('Custom message')).toBeInTheDocument();
  });
});
