import React, { useState, useEffect, useRef } from 'react';
import { Box, BoxProps } from '@mui/material';
import { styled } from '@mui/material/styles';

interface GlassContainerProps extends BoxProps {
  variant?: 'light' | 'dark';
  blur?: number;
  opacity?: number;
  animated?: boolean;
  floating?: boolean;
  shimmer?: boolean;
}

const StyledGlassContainer = styled(Box, {
  shouldForwardProp: (prop) => 
    prop !== 'variant' && 
    prop !== 'blur' && 
    prop !== 'opacity' && 
    prop !== 'animated' && 
    prop !== 'floating' && 
    prop !== 'shimmer',
})<GlassContainerProps>(({ theme, variant = 'light', blur = 20, opacity = 0.1, animated = false, floating = false, shimmer = false }) => ({
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
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  position: 'relative',
  overflow: 'hidden',
  ...(animated && {
    animation: 'float 6s ease-in-out infinite',
  }),
  ...(floating && {
    animation: 'float 6s ease-in-out infinite',
  }),
  ...(shimmer && {
    '&::before': {
      content: '""',
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: `linear-gradient(
        135deg,
        ${variant === 'light' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(255, 255, 255, 0.05)'} 0%,
        ${variant === 'light' ? 'rgba(255, 255, 255, 0.05)' : 'rgba(255, 255, 255, 0.02)'} 100%
      )`,
      opacity: 0,
      transition: 'opacity 0.3s ease',
    },
    '&:hover::before': {
      opacity: 1,
    },
  }),
  '&::after': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: '-100%',
    width: '100%',
    height: '100%',
    background: `linear-gradient(
      90deg,
      transparent,
      ${variant === 'light' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(255, 255, 255, 0.05)'},
      transparent
    )`,
    transition: 'left 0.5s ease',
  },
  '&:hover::after': {
    left: '100%',
  },
  '&:hover': {
    background: variant === 'light'
      ? `rgba(255, 255, 255, ${opacity + 0.05})`
      : `rgba(0, 0, 0, ${opacity + 0.1})`,
    boxShadow: variant === 'light'
      ? '0 12px 40px rgba(0, 0, 0, 0.15)'
      : '0 12px 40px rgba(0, 0, 0, 0.4)',
    transform: 'translateY(-2px)',
  },
}));

const GlassContainer: React.FC<GlassContainerProps> = ({ 
  children, 
  animated = false,
  floating = false,
  shimmer = false,
  ...props 
}) => {
  const [scrollBlur, setScrollBlur] = useState(20);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => {
      if (containerRef.current) {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const newBlur = Math.min(20 + scrollTop * 0.1, 40);
        setScrollBlur(newBlur);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <StyledGlassContainer 
      ref={containerRef}
      blur={scrollBlur}
      animated={animated}
      floating={floating}
      shimmer={shimmer}
      {...props}
    >
      {children}
    </StyledGlassContainer>
  );
};

export default GlassContainer;
