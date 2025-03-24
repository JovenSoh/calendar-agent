// src/components/TypingBubble.js
import React from 'react';
import { Paper, Box } from '@mui/material';
import { keyframes } from '@emotion/react';

const bounce = keyframes`
  0%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-8px); }
`;

const TypingBubble = () => {
  const bubbleStyle = {
    backgroundColor: '#e5e5ea',
    padding: '10px 15px',
    borderRadius: '20px',
    alignSelf: 'flex-start', // Bot messages on left
    margin: '5px 0',
    display: 'flex',
  };

  const dotStyle = {
    width: 8,
    height: 8,
    margin: '0 2px',
    backgroundColor: '#000',
    borderRadius: '50%',
    animation: `${bounce} 1.4s infinite ease-in-out both`,
  };

  return (
    <Paper style={bubbleStyle} elevation={2}>
      <Box display="flex">
        <Box style={{ ...dotStyle, animationDelay: '0s' }} />
        <Box style={{ ...dotStyle, animationDelay: '0.2s' }} />
        <Box style={{ ...dotStyle, animationDelay: '0.4s' }} />
      </Box>
    </Paper>
  );
};

export default TypingBubble;
