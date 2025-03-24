// src/components/TypingBubble.js
import React from 'react';
import { Paper, Box } from '@mui/material';
import { keyframes } from '@emotion/react';

const bounce = keyframes`
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-8px);
  }
`;

const TypingBubble = () => {
  return (
    <Paper
      elevation={2}
      sx={{
        backgroundColor: '#e5e5ea',
        padding: '10px 15px',
        borderRadius: '20px',
        alignSelf: 'flex-start',
        margin: '5px 0',
        display: 'inline-flex',
        maxWidth: '80%',
        overflow: 'visible',  // allow the dots to bounce visibly
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        {[0, 0.2, 0.4].map((delay, index) => (
          <Box
            key={index}
            sx={{
              width: 8,
              height: 8,
              margin: '0 2px',
              backgroundColor: '#000',
              borderRadius: '50%',
              animation: `${bounce} 1.4s infinite ease-in-out both`,
              animationDelay: `${delay}s`,
            }}
          />
        ))}
      </Box>
    </Paper>
  );
};

export default TypingBubble;
