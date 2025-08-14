import React from 'react';
import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

interface EnhancedTypingIndicatorProps {
  isVisible: boolean;
}

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
  animation: 'pulse 1.4s infinite ease-in-out',
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

const EnhancedTypingIndicator: React.FC<EnhancedTypingIndicatorProps> = ({ isVisible }) => {
  if (!isVisible) return null;

  return (
    <TypingContainer>
      <Box sx={{ display: 'flex', gap: 0.5 }}>
        <Dot />
        <Dot />
        <Dot />
      </Box>
      <Typography variant="body2" color="text.secondary">
        I2C AI is typing...
      </Typography>
    </TypingContainer>
  );
};

export default EnhancedTypingIndicator;
