export const sendMessageToRasa = async (message, setMessages, setIsTyping, setInputText)=> {
    try {
      // Api para obtener la respuesta de rasa
      // Update UI to show user message
      setMessages(prevMessages => [...prevMessages, { text: message, sender: 'user' }]);
  
      // Indicate chatbot is typing
      setIsTyping(true);
  
      // Prepare data for Rasa API call
      const rasaUrl = 'http://localhost:5005/webhooks/rest/webhook'; 
      const body = JSON.stringify({ message });
  
      // Send message to Rasa server
      const responsePromise = fetch(rasaUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body,
      });

      // promesa, si no devuelve la respuesta rasa despues de 6 segundos arrojara error
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => {
          reject(new Error('Rasa response timed out (took more than 6 seconds)'));
        }, 6000); 
      });

    // Wait for either the response or the timeout
    const response = await Promise.race([responsePromise, timeoutPromise]);
  
      // Check response status
      if (!response.ok) {
        throw new Error(`Rasa API error: ${response.status}`); // Throw error with specific message
      }
  
      const data = await response.json();
      
      // Check if Rasa returned an empty array
      if (Array.isArray(data) && data.length === 0) {
      throw new Error('Rasa returned an empty response');
      }
  
      // Update UI with bot messages
      setMessages(prevMessages => [...prevMessages, ...data.map(item => ({ text: item.text, sender: 'bot' }))]);
  
     
  
    } catch (error) {
      console.error('Error sending message to Rasa:', error);
      setMessages(prevMessages => [...prevMessages, { text: 'Oops! Something went wrong.', sender: 'bot' }]);
    }
    finally {
      // Indicate chatbot has finished typing
      setIsTyping(false);
       // Clear user input field
      setInputText('');
    }
  };
  