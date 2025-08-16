import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  Box,
  TextField,
  IconButton,
  Typography,
  Fade,
  Alert,
  Chip,
  Zoom,
  Slide,
} from '@mui/material';
import {
  Send as SendIcon,
  ContentCopy as CopyIcon,
  VolumeUp as VolumeIcon,
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import { chatApi, ChatMessage, ChatQueryRequest, ChatQueryResponse } from '../services/api';
import EnhancedMessage from './EnhancedMessage';
import TypingIndicator from './TypingIndicator';
import MessageAvatar from './MessageAvatar';
import GlassContainer from './GlassContainer';
import EnhancedQuickActions from './EnhancedQuickActions';
import '../styles/glassmorphism.css';
import '../styles/enhanced-ui.css';

const ChatContainer = styled(GlassContainer)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  height: '100%',
  maxWidth: '100%',
  margin: '0 auto',
  padding: 0,
  overflow: 'hidden',
  borderRadius: '20px',
  background: 'rgba(255, 255, 255, 0.05)',
  backdropFilter: 'blur(20px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
}));

const MessagesContainer = styled(Box)(({ theme }) => ({
  flex: 1,
  overflowY: 'auto',
  padding: theme.spacing(3),
  background: 'transparent',
  scrollBehavior: 'smooth',
  '&::-webkit-scrollbar': {
    width: '8px',
  },
  '&::-webkit-scrollbar-track': {
    background: 'rgba(0, 0, 0, 0.05)',
    borderRadius: '4px',
  },
  '&::-webkit-scrollbar-thumb': {
    background: 'linear-gradient(135deg, rgba(25, 118, 210, 0.6) 0%, rgba(0, 188, 212, 0.6) 100%)',
    borderRadius: '4px',
  },
}));

const InputContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(2),
  margin: theme.spacing(2),
  marginTop: 0,
  borderRadius: '20px',
  background: 'rgba(255, 255, 255, 0.08)',
  backdropFilter: 'blur(12px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  '&:hover': {
    background: 'rgba(255, 255, 255, 0.12)',
    transform: 'translateY(-1px)',
  },
}));

const ChatUI: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [sources, setSources] = useState<string[]>([]);
  const [confidence, setConfidence] = useState<number>(0);
  const [isOnline, setIsOnline] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message?: string) => {
    const messageToSend = message || inputMessage;
    if (!messageToSend.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: messageToSend.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      const request: ChatQueryRequest = {
        query: userMessage.content,
        conversation_id: conversationId || undefined,
        max_tokens: 500,
        temperature: 0.7,
      };

      const response: ChatQueryResponse = await chatApi.sendMessage(request);
      
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setConversationId(response.conversation_id);
      setSources(response.sources);
      setConfidence(response.confidence);

    } catch (err) {
      setError('Failed to get response. Please try again.');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleCopyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <ChatContainer>
        <MessagesContainer>
          {messages.length === 0 && (
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                color: 'text.secondary',
                textAlign: 'center',
              }}
            >
              <Typography variant="h4" gutterBottom color="primary">
                Welcome to I2C AI Assistant
              </Typography>
              <Typography variant="body1" paragraph>
                Ask me anything about I2C's products, services, or solutions.
              </Typography>
              <EnhancedQuickActions onActionClick={handleSendMessage} />
            </Box>
          )}

          {messages.map((message, index) => (
            <Fade in={true} timeout={500} key={index}>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  mb: 2,
                  flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
                }}
              >
                <MessageAvatar role={message.role} />
                <EnhancedMessage
                  content={message.content}
                  owner={message.role}
                  timestamp={message.timestamp}
                />
              </Box>
            </Fade>
          ))}

          <TypingIndicator isVisible={isLoading} />

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {sources.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" sx={{ mb: 1 }}>
                Sources:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {sources.map((source, index) => (
                  <Chip
                    key={index}
                    label={source}
                    size="small"
                    variant="outlined"
                    color="primary"
                  />
                ))}
              </Box>
            </Box>
          )}

          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputContainer>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder="Ask about I2C products, services, or solutions..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            variant="outlined"
            sx={{
              '& .MuiOutlinedInput-root': {
                border: 'none',
                '& fieldset': {
                  border: 'none',
                },
              },
            }}
          />
          <IconButton
            color="primary"
            onClick={() => handleSendMessage()}
            disabled={isLoading || !inputMessage.trim()}
            sx={{ ml: 1 }}
          >
            <SendIcon />
          </IconButton>
        </InputContainer>
      </ChatContainer>
    </Box>
  );
};

export default ChatUI;
