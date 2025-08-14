import React from 'react';
import { Box, BoxProps } from '@mui/material';
import { styled } from '@mui/material/styles';

interface GlassContainerProps extends BoxProps {
  variant?: 'light' | 'dark';
  blur?: number;
  opacity?: number;
}

const StyledGlassContainer = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'variant' && prop !== 'blur' && prop !== 'opacity',
})<GlassContainerProps>(({ theme, variant = 'light', blur = 20, opacity = 0.1 }) => ({
  background: variant === 'light' 
    ? `rgba(255, 255, 255, ${opacity})`
    : `rgba(0, 0, 0, ${opacity})`,
  backdropFilter: `blur(${blur}px)`,
  WebkitBackdropFilter: `blur(${blur}px)`,
  border: `1px solid ${variant === 'light' 
    ? 'rgba(255, 255, 255, 0.2)' 
    : 'rgba(255, 255, 255, 0.1)'}`,
  borderRadius: 16,
  boxShadow: variant === 'light'
    ? '0 8px 32px rgba(0, 0, 0, 0.1)'
    : '0 8px 32px rgba(0, 0, 0, 0.3)',
  transition: 'all 0.3s ease',
  '&:hover': {
    background: variant === 'light'
      ? `rgba(255, 255, 255, ${opacity + 0.05})`
      : `rgba(0, 0, 0, ${opacity + 0.1})`,
    boxShadow: variant === 'light'
      ? '0 12px 40px rgba(0, 0, 0, 0.15)'
      : '0 12px 40px rgba(0, 0, 0, 0.4)',
  },
}));

const GlassContainer: React.FC<GlassContainerProps> = ({ children, ...props }) => {
  return (
    <StyledGlassContainer {...props}>
      {children}
    </StyledGlassContainer>
  );
};

export default GlassContainer;
