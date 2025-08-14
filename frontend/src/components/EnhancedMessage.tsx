import React from 'react';
import { Paper, Typography, Box } from '@mui/material';
import { styled } from '@mui/material/styles';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useTheme } from '../contexts/ThemeContext';

const MessageBubble = styled(Paper)<{ owner: 'user' | 'assistant' }>(({ theme, owner }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  maxWidth: '70%',
  alignSelf: owner === 'user' ? 'flex-end' : 'flex-start',
  backgroundColor: owner === 'user' ? '#1976d2' : 'background.paper',
  color: owner === 'user' ? '#ffffff' : 'text.primary',
  borderRadius: owner === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
  },
}));

const MarkdownContainer = styled(Box)(({ theme }) => ({
  '& h1, & h2, & h3, & h4, & h5, & h6': {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
    fontWeight: 600,
  },
  '& p': {
    marginBottom: theme.spacing(1),
  },
  '& ul, & ol': {
    marginLeft: theme.spacing(2),
    marginBottom: theme.spacing(1),
  },
  '& li': {
    marginBottom: theme.spacing(0.5),
  },
  '& blockquote': {
    borderLeft: `4px solid ${theme.palette.primary.main}`,
    paddingLeft: theme.spacing(2),
    marginLeft: 0,
    fontStyle: 'italic',
    color: theme.palette.text.secondary,
  },
  '& code': {
    backgroundColor: theme.palette.mode === 'dark' ? '#2d2d2d' : '#f5f5f5',
    padding: '2px 4px',
    borderRadius: '4px',
    fontSize: '0.875em',
  },
  '& pre': {
    backgroundColor: theme.palette.mode === 'dark' ? '#1e1e1e' : '#f8f8f8',
    padding: theme.spacing(2),
    borderRadius: theme.spacing(1),
    overflowX: 'auto',
    margin: theme.spacing(1, 0),
  },
}));

interface EnhancedMessageProps {
  content: string;
  owner: 'user' | 'assistant';
  timestamp?: Date;
}

const EnhancedMessage: React.FC<EnhancedMessageProps> = ({ content, owner, timestamp }) => {
  const { darkMode } = useTheme();

  return (
    <MessageBubble owner={owner}>
      <MarkdownContainer>
        <ReactMarkdown
          components={{
            h1: ({ children }) => <Typography variant="h5" component="h1">{children}</Typography>,
            h2: ({ children }) => <Typography variant="h6" component="h2">{children}</Typography>,
            h3: ({ children }) => <Typography variant="subtitle1" component="h3">{children}</Typography>,
            p: ({ children }) => <Typography variant="body1" component="p">{children}</Typography>,
            ul: ({ children }) => <ul style={{ margin: 0 }}>{children}</ul>,
            ol: ({ children }) => <ol style={{ margin: 0 }}>{children}</ol>,
            li: ({ children }) => <li style={{ marginBottom: '4px' }}>{children}</li>,
            blockquote: ({ children }) => (
              <Box component="blockquote" sx={{ borderLeft: 4, borderColor: 'primary.main', pl: 2, my: 1 }}>
                {children}
              </Box>
            ),
            code: ({ inline, className, children, ...props }: any) => {
              const match = /language-(\w+)/.exec(className || '');
              return !inline && match ? (
                <SyntaxHighlighter
                  style={darkMode ? oneDark : oneLight}
                  language={match[1]}
                  PreTag="div"
                  {...props}
                >
                  {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
          }}
        >
          {content}
        </ReactMarkdown>
      </MarkdownContainer>
      {timestamp && (
        <Typography variant="caption" sx={{ opacity: 0.7, mt: 1 }}>
          {timestamp.toLocaleTimeString()}
        </Typography>
      )}
    </MessageBubble>
  );
};

export default EnhancedMessage;
