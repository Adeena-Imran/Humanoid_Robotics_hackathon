import React, { useState } from 'react';

// Define the expected structure of your API response
interface ChatbotResponse {
  response: string;
  // Add other fields from your RagChatResponse schema if needed:
  // sources?: SourceReference[];
  // citations?: Citation[];
}

function ChatbotIntegration() {
  const [query, setQuery] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setResponse('');
    setError(null);

    try {
      const apiResponse = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: query,
          query_type: 'explanation',
          session_id: 'unique-session-id-for-user',
        }),
      });

      if (!apiResponse.ok) {
        const errorData = await apiResponse.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${apiResponse.status}`
        );
      }

      const data: ChatbotResponse = await apiResponse.json();
      setResponse(data.response || 'No response received.');
    } catch (err: any) {
      console.error('Error fetching from RAG chatbot:', err);
      setError(`Failed to fetch response: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Ask the RAG Chatbot</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Enter your question about humanoid robotics..."
          style={{ width: '80%', padding: '8px', marginRight: '10px' }}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {response && (
        <div>
          <h3>Chatbot Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default ChatbotIntegration;
