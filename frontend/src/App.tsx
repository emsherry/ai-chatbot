import React from 'react';
import { Container, Box, IconButton, Tooltip } from '@mui/material';
import { styled } from '@mui/material/styles';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import ChatUI from './components/ChatUI';
import { ThemeProvider } from './contexts/ThemeContext';
import { useTheme } from './contexts/ThemeContext';

const MainContainer = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  background: theme.palette.mode === 'dark' 
    ? 'linear-gradient(135deg, #121212 0%, #1e1e1e 100%)'
    : 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
  display: 'flex',
  flexDirection: 'column',
  transition: 'background 0.3s ease',
}));

const Header = styled(Box)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'flex-end',
  alignItems: 'center',
  padding: theme.spacing(2),
  paddingBottom: 0,
}));

const AppContent: React.FC = () => {
  const { darkMode, toggleDarkMode } = useTheme();

  return (
    <MainContainer>
      <Header>
        <Tooltip title={darkMode ? "Switch to light mode" : "Switch to dark mode"}>
          <IconButton 
            onClick={toggleDarkMode}
            sx={{
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
              },
            }}
          >
            {darkMode ? <Brightness7 /> : <Brightness4 />}
          </IconButton>
        </Tooltip>
      </Header>
      
      <Container maxWidth="lg" sx={{ 
        height: 'calc(100vh - 80px)', 
        display: 'flex', 
        flexDirection: 'column',
        px: 2,
        pb: 2,
      }}>
        <ChatUI />
      </Container>
    </MainContainer>
  );
};

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
