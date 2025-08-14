import React, { useState } from 'react';
import { Box, IconButton, Tooltip, Fade } from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  ThumbUp,
  ThumbDown,
  Favorite,
  EmojiEmotions,
  Lightbulb,
} from '@mui/icons-material';

interface MessageReactionsProps {
  messageId: string;
  onReaction?: (reaction: string) => void;
  reactions?: { [key: string]: number };
}

const ReactionsContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  gap: theme.spacing(0.5),
  marginTop: theme.spacing(1),
  opacity: 0.7,
  transition: 'opacity 0.2s ease',
  '&:hover': {
    opacity: 1,
  },
}));

const ReactionButton = styled(IconButton)(({ theme }) => ({
  padding: theme.spacing(0.5),
  fontSize: '1rem',
  color: theme.palette.text.secondary,
  transition: 'all 0.2s ease',
  '&:hover': {
    transform: 'scale(1.2)',
  },
  '&.active': {
    color: theme.palette.primary.main,
    transform: 'scale(1.1)',
  },
}));

const reactionIcons = {
  like: ThumbUp,
  dislike: ThumbDown,
  love: Favorite,
  funny: EmojiEmotions,
  insightful: Lightbulb,
};

const reactionLabels = {
  like: 'Like',
  dislike: 'Dislike',
  love: 'Love',
  funny: 'Funny',
  insightful: 'Insightful',
};

const MessageReactions: React.FC<MessageReactionsProps> = ({
  messageId,
  onReaction,
  reactions = {},
}) => {
  const [userReactions, setUserReactions] = useState<Set<string>>(new Set());

  const handleReaction = (reaction: string) => {
    const newReactions = new Set(userReactions);
    if (newReactions.has(reaction)) {
      newReactions.delete(reaction);
    } else {
      newReactions.add(reaction);
    }
    setUserReactions(newReactions);
    onReaction?.(reaction);
  };

  return (
    <ReactionsContainer>
      {Object.entries(reactionIcons).map(([key, Icon]) => (
        <Fade in={true} timeout={300} key={key}>
          <Tooltip title={reactionLabels[key as keyof typeof reactionLabels]} arrow>
            <ReactionButton
              onClick={() => handleReaction(key)}
              className={userReactions.has(key) ? 'active' : ''}
              size="small"
            >
              <Icon fontSize="small" />
            </ReactionButton>
          </Tooltip>
        </Fade>
      ))}
    </ReactionsContainer>
  );
};

export default MessageReactions;
