// src/components/Chat.js
import React, { useState } from 'react';
import { Box, TextField, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ChatBubble from './ChatBubble';
import TypingBubble from './TypingBubble';

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        'Welcome to our appointment booking chat! I can help you book appointments in **15-minute timeslots**. You can ask me to *book*, *list*, or *cancel* appointments. How can I assist you today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  // Adjust the URL if your backend is running elsewhere.
  const backendUrl = 'http://localhost:8000/api/chat';

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { role: 'user', content: input.trim() };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: updatedMessages }),
      });
      const data = await response.json();
      if (data.reply) {
        const replyMessage = { role: 'assistant', content: data.reply };
        setMessages(prev => [...prev, replyMessage]);
      } else if (data.error) {
        const errorMessage = { role: 'assistant', content: 'Error: ' + data.error };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = { role: 'assistant', content: 'Error: ' + error.message };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      height="90vh"
      sx={{
        maxWidth: 480,       // Portrait-friendly width
        margin: '0 auto',    // Center horizontally
        py: 4,               // Vertical padding
        px: 2,               // Horizontal padding
      }}
    >
      {/* Chat messages container */}
      <Box flex={1} overflow="auto" mb={2} sx={{ py: 2 }}>
        {messages.map((msg, index) => (
          <ChatBubble key={index} message={msg.content} role={msg.role} />
        ))}
        {loading && <TypingBubble />}
      </Box>
      {/* Message input area */}
      <Box display="flex">
        <TextField
          variant="outlined"
          placeholder="Type a message..."
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <IconButton color="primary" onClick={sendMessage} disabled={loading}>
          <SendIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default Chat;
