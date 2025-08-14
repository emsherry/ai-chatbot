import React, { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  IconButton,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  SmartToy as AIIcon,
  Info as InfoIcon,
  HelpOutline as HelpIcon,
  AttachMoney as MoneyIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';
import { useTheme } from '../contexts/ThemeContext';

const QuickActionsContainer = styled(Box)(({ theme }) => ({
  position: 'relative',
  margin: theme.spacing(2, 0),
  padding: theme.spacing(2),
  borderRadius: '20px',
  background: theme.palette.mode === 'dark'
    ? 'rgba(0, 0, 0, 0.3)'
    : 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(255, 255, 255, 0.2)'}`,
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
  transition: 'all 0.3s ease',
}));

interface EnhancedQuickActionsProps {
  onActionClick: (action: string, type?: string, metadata?: any) => void;
}

const EnhancedQuickActions: React.FC<EnhancedQuickActionsProps> = ({
  onActionClick,
}) => {
  const actions = [
    {
      id: 'what-is-i2c',
      title: 'About I2C',
      icon: <InfoIcon />,
      action: 'What is I2C and what services do you provide?',
    },
    {
      id: 'get-started',
      title: 'Get Started',
      icon: <HelpIcon />,
      action: 'How can I get started with I2C services?',
    },
    {
      id: 'payment-solutions',
      title: 'Payment Solutions',
      icon: <MoneyIcon />,
      action: 'Tell me about I2C payment solutions',
    },
    {
      id: 'security-features',
      title: 'Security Features',
      icon: <SecurityIcon />,
      action: 'What security features does I2C offer?',
    },
  ];

  return (
    <QuickActionsContainer>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          AI Quick Actions
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        {actions.map((action) => (
          <Button
            key={action.id}
            variant="outlined"
            size="small"
            startIcon={action.icon}
            onClick={() => onActionClick(action.action)}
            sx={{
              borderRadius: 3,
              textTransform: 'none',
              fontSize: '0.875rem',
            }}
          >
            {action.title}
          </Button>
        ))}
      </Box>
    </QuickActionsContainer>
  );
};

export default EnhancedQuickActions;
