import React, { createContext, useContext, useEffect, useState } from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { i2cTheme } from '../theme';
import { createTheme } from '@mui/material/styles';
import { i2cColors } from '../theme';

interface ThemeContextType {
  darkMode: boolean;
  toggleDarkMode: () => void;
  autoTheme: boolean;
  toggleAutoTheme: () => void;
  highContrast: boolean;
  toggleHighContrast: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
  darkMode: false,
  toggleDarkMode: () => {},
  autoTheme: false,
  toggleAutoTheme: () => {},
  highContrast: false,
  toggleHighContrast: () => {},
});

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : false;
  });

  const [autoTheme, setAutoTheme] = useState(() => {
    const saved = localStorage.getItem('autoTheme');
    return saved ? JSON.parse(saved) : false;
  });

  const [highContrast, setHighContrast] = useState(() => {
    const saved = localStorage.getItem('highContrast');
    return saved ? JSON.parse(saved) : false;
  });

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const toggleAutoTheme = () => {
    setAutoTheme(!autoTheme);
  };

  const toggleHighContrast = () => {
    setHighContrast(!highContrast);
  };

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  useEffect(() => {
    localStorage.setItem('autoTheme', JSON.stringify(autoTheme));
  }, [autoTheme]);

  useEffect(() => {
    localStorage.setItem('highContrast', JSON.stringify(highContrast));
  }, [highContrast]);

  useEffect(() => {
    if (autoTheme) {
      const hour = new Date().getHours();
      const isNight = hour < 6 || hour >= 18;
      setDarkMode(isNight);
    }
  }, [autoTheme]);

  useEffect(() => {
    if (autoTheme) {
      const interval = setInterval(() => {
        const hour = new Date().getHours();
        const isNight = hour < 6 || hour >= 18;
        setDarkMode(isNight);
      }, 60000); // Check every minute
      return () => clearInterval(interval);
    }
  }, [autoTheme]);

  const theme = createTheme({
    ...i2cTheme,
    palette: {
      ...i2cTheme.palette,
      mode: darkMode ? 'dark' : 'light',
      primary: {
        ...i2cColors.primary,
        ...(highContrast && {
          main: '#0066cc',
          light: '#3385ff',
          dark: '#004499',
        }),
      },
      secondary: {
        ...i2cColors.secondary,
        ...(highContrast && {
          main: '#00b3b3',
          light: '#33c6c6',
          dark: '#008080',
        }),
      },
      background: {
        default: darkMode ? '#121212' : '#f5f7fa',
        paper: darkMode ? '#1e1e1e' : '#ffffff',
        ...(highContrast && {
          default: darkMode ? '#000000' : '#ffffff',
          paper: darkMode ? '#1a1a1a' : '#f5f5f5',
        }),
      },
      text: {
        primary: darkMode ? '#ffffff' : '#333333',
        secondary: darkMode ? '#b3b3b3' : '#666666',
        ...(highContrast && {
          primary: darkMode ? '#ffffff' : '#000000',
          secondary: darkMode ? '#cccccc' : '#333333',
        }),
      },
    },
    components: {
      ...i2cTheme.components,
      MuiCssBaseline: {
        styleOverrides: {
          body: {
            backgroundColor: darkMode ? '#121212' : '#f5f7fa',
            backgroundImage: darkMode 
              ? 'linear-gradient(135deg, #121212 0%, #1e1e1e 100%)'
              : 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            ...(highContrast && {
              backgroundImage: darkMode 
                ? 'linear-gradient(135deg, #000000 0%, #1a1a1a 100%)'
                : 'linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%)',
            }),
          },
        },
      },
    },
  });

  return (
    <ThemeContext.Provider value={{ 
      darkMode, 
      toggleDarkMode, 
      autoTheme, 
      toggleAutoTheme,
      highContrast,
      toggleHighContrast 
    }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};
