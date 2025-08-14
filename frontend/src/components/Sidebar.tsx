import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
  IconButton,
} from '@mui/material';
import {
  History as HistoryIcon,
  Dashboard as DashboardIcon,
  Settings as SettingsIcon,
  Help as HelpIcon,
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';

const drawerWidth = 280;

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    boxSizing: 'border-box',
    backgroundColor: '#f8f9fa',
    borderRight: '1px solid #e0e0e0',
  },
}));

const SidebarHeader = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  backgroundColor: '#1976d2',
  color: '#ffffff',
}));

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon /> },
    { text: 'Conversation History', icon: <HistoryIcon /> },
    { text: 'Settings', icon: <SettingsIcon /> },
    { text: 'Help & Support', icon: <HelpIcon /> },
  ];

  return (
    <StyledDrawer
      variant="temporary"
      anchor="left"
      open={open}
      onClose={onClose}
      ModalProps={{
        keepMounted: true,
      }}
    >
      <SidebarHeader>
        <Typography variant="h6" noWrap>
          I2C AI Assistant
        </Typography>
        <Typography variant="body2" sx={{ opacity: 0.8 }}>
          Navigation
        </Typography>
      </SidebarHeader>
      
      <Divider />
      
      <List>
        {menuItems.map((item, index) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton>
              <ListItemIcon sx={{ color: '#1976d2' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      
      <Divider />
      
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Recent Conversations
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Your conversation history will appear here
        </Typography>
      </Box>
    </StyledDrawer>
  );
};

export default Sidebar;
