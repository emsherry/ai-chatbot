import React from 'react';
import { Box, Button, Chip, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  HelpOutline as HelpIcon,
  InfoOutlined as InfoIcon,
  ContactSupport as SupportIcon,
  TrendingUp as TrendingIcon,
  AttachMoney as MoneyIcon,
  Security as SecurityIcon,
} from '@mui/icons-material';

const ActionsContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexWrap: 'wrap',
  gap: theme.spacing(1),
  marginTop: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const ActionButton = styled(Button)(({ theme }) => ({
  borderRadius: 20,
  textTransform: 'none',
  fontSize: '0.875rem',
  fontWeight: 500,
  padding: theme.spacing(0.5, 1.5),
  boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
  '&:hover': {
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)',
  },
}));

interface QuickActionsProps {
  onActionClick: (action: string) => void;
}

const QuickActions: React.FC<QuickActionsProps> = ({ onActionClick }) => {
  const actions = [
    {
      label: 'What is I2C?',
      icon: <InfoIcon fontSize="small" />,
      action: 'What is I2C and what services do you provide?',
    },
    {
      label: 'Payment Solutions',
      icon: <MoneyIcon fontSize="small" />,
      action: 'Tell me about I2C payment solutions',
    },
    {
      label: 'Get Started',
      icon: <HelpIcon fontSize="small" />,
      action: 'How can I get started with I2C services?',
    },
    {
      label: 'Security',
      icon: <SecurityIcon fontSize="small" />,
      action: 'What security features does I2C offer?',
    },
    {
      label: 'Support',
      icon: <SupportIcon fontSize="small" />,
      action: 'How can I contact I2C support?',
    },
    {
      label: 'Trending',
      icon: <TrendingIcon fontSize="small" />,
      action: 'What are the latest trends in payment technology?',
    },
  ];

  return (
    <ActionsContainer>
      <Typography variant="subtitle2" sx={{ width: '100%', mb: 1 }}>
        Quick Actions:
      </Typography>
      {actions.map((action, index) => (
        <ActionButton
          key={index}
          variant="outlined"
          size="small"
          startIcon={action.icon}
          onClick={() => onActionClick(action.action)}
        >
          {action.label}
        </ActionButton>
      ))}
    </ActionsContainer>
  );
};

export default QuickActions;
