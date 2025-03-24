import React from 'react';
import { Paper } from '@mui/material';
import ReactMarkdown from 'react-markdown';

const ChatBubble = ({ message, role }) => {
  const isUser = role === 'user';
  const bubbleStyle = {
    backgroundColor: isUser ? '#007AFF' : '#e5e5ea',
    color: isUser ? '#fff' : '#000',
    padding: '10px 15px',
    borderRadius: '20px',
    maxWidth: '80%',
    alignSelf: isUser ? 'flex-end' : 'flex-start',
    margin: '15px 0',
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word',
  };

  return (
    <Paper style={bubbleStyle} elevation={2}>
      <ReactMarkdown
        components={{
          strong: ({ node, ...props }) => <strong style={{ fontWeight: 600 }} {...props} />,
          p: ({ node, ...props }) => <span {...props} />, 
        }}
      >
        {message}
      </ReactMarkdown>
    </Paper>
  );
};

export default ChatBubble;
