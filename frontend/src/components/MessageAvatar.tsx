import React from 'react';
import { Avatar, Badge, Box } from '@mui/material';
import { styled } from '@mui/material/styles';
import { Person, SmartToy } from '@mui/icons-material';

interface MessageAvatarProps {
  role: 'user' | 'assistant';
  size?: 'small' | 'medium' | 'large';
  isOnline?: boolean;
}

const StyledAvatar = styled(Avatar, {
  shouldForwardProp: (prop) => prop !== 'role' && prop !== 'size',
})<{ role: string; size: string }>(({ theme, role, size }) => ({
  background: role === 'user'
    ? 'linear-gradient(135deg, #1976d2, #1565c0)'
    : 'linear-gradient(135deg, #00bcd4, #0097a7)',
  width: size === 'small' ? 32 : size === 'medium' ? 40 : 48,
  height: size === 'small' ? 32 : size === 'medium' ? 40 : 48,
  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
  border: `2px solid ${role === 'user' ? '#1976d2' : '#00bcd4'}`,
}));

const OnlineBadge = styled(Badge)(({ theme }) => ({
  '& .MuiBadge-badge': {
    backgroundColor: '#4caf50',
    color: '#4caf50',
    boxShadow: `0 0 0 2px ${theme.palette.background.paper}`,
    '&::after': {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      borderRadius: '50%',
      animation: 'ripple 1.2s infinite ease-in-out',
      border: '1px solid currentColor',
      content: '""',
    },
  },
  '@keyframes ripple': {
    '0%': {
      transform: 'scale(.8)',
      opacity: 1,
    },
    '100%': {
      transform: 'scale(2.4)',
      opacity: 0,
    },
  },
}));

const MessageAvatar: React.FC<MessageAvatarProps> = ({ 
  role, 
  size = 'medium', 
  isOnline = true 
}) => {
  const icon = role === 'user' ? <Person /> : <SmartToy />;
  
  return (
    <Box sx={{ position: 'relative' }}>
      {role === 'assistant' && isOnline ? (
        <OnlineBadge
          overlap="circular"
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          variant="dot"
        >
          <StyledAvatar role={role} size={size}>
            {icon}
          </StyledAvatar>
        </OnlineBadge>
      ) : (
        <StyledAvatar role={role} size={size}>
          {icon}
        </StyledAvatar>
      )}
    </Box>
  );
};

export default MessageAvatar;
