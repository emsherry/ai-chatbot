import React from 'react';
import { Box, Typography, Avatar } from '@mui/material';
import { styled } from '@mui/material/styles';
import { keyframes } from '@emotion/react';

const pulse = keyframes`
  0%, 60%, 100% {
    transform: scale(1);
    opacity: 0.7;
  }
  30% {
    transform: scale(1.2);
    opacity: 1;
  }
`;

const TypingContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(1),
  padding: theme.spacing(1, 2),
  marginBottom: theme.spacing(2),
  alignSelf: 'flex-start',
}));

const Dot = styled('span')(({ theme }) => ({
  width: 8,
  height: 8,
  borderRadius: '50%',
  backgroundColor: theme.palette.primary.main,
  animation: `${pulse} 1.4s infinite ease-in-out`,
  '&:nth-of-type(1)': {
    animationDelay: '-0.32s',
  },
  '&:nth-of-type(2)': {
    animationDelay: '-0.16s',
  },
  '&:nth-of-type(3)': {
    animationDelay: '0s',
  },
}));

const I2CAvatar = styled(Avatar)(({ theme }) => ({
  backgroundColor: '#1976d2',
  color: '#ffffff',
  fontWeight: 'bold',
  width: 32,
  height: 32,
  fontSize: '0.75rem',
}));

interface TypingIndicatorProps {
  isVisible: boolean;
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ isVisible }) => {
  if (!isVisible) return null;

  return (
    <TypingContainer>
      <I2CAvatar>I2C</I2CAvatar>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          <Dot />
          <Dot />
          <Dot />
        </Box>
        <Typography variant="body2" color="text.secondary">
          I2C AI is typing...
        </Typography>
      </Box>
    </TypingContainer>
  );
};

export default TypingIndicator;
