// import { useState } from "react";
// import { Send } from "lucide-react";
// import { Card, CardContent } from "@mui/material";
// import { Button } from "@mui/material";
// import { TextField } from "@mui/material";

// export default function App() {
//   const [messages, setMessages] = useState([
//     { id: 1, text: "Hello! How can I help you?", sender: "bot" }
//   ]);
//   const [input, setInput] = useState("");

//   const sendMessage = async () => {
//     if (!input.trim()) return;

//     // Send the user's message
//     const newMessage = { id: messages.length + 1, text: input, sender: "user" };
//     setMessages([...messages, newMessage]);
//     setInput("");

//     try {
//       // Make an HTTP request to the backend
//       const response = await fetch("http://127.0.0.1:5000/click", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json"
//         },
//         body: JSON.stringify({ message: input })
//       },
//     console.log(input)
//     );

//       if (response.ok) {
//         console.log(response)
//         const data = await response.json();
//         const botMessage = {
//           id: messages.length + 2,
//           text: data.reply, // Assuming the response has a "reply" field
//           sender: "bot"
//         };
//         setMessages((prevMessages) => [...prevMessages, botMessage]);
//       } else {
//         console.error("Error:", response.statusText);
//       }
//     } catch (error) {
//       console.error("Error:", error);
//     }
//   };

//   return (
//     <div className="flex flex-col h-screen p-4 max-w-md mx-auto">
//       <Card className="flex-1 overflow-y-auto p-4 bg-gray-100 rounded-lg">
//         <CardContent>
//           {messages.map((msg) => (
//             <div
//               key={msg.id}
//               className={`mb-2 text-${msg.sender === "user" ? "right" : "left"}`}
//             >
//               <span
//                 className={`inline-block px-4 py-2 rounded-lg ${
//                   msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-300"
//                 }`}
//               >
//                 {msg.text}
//               </span>
//             </div>
//           ))}
//         </CardContent>
//       </Card>
//       <div className="flex gap-2 mt-4">
//         <TextField
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           placeholder="Type a message..."
//           fullWidth
//         />
//         <Button onClick={sendMessage} variant="contained" color="primary">
//           <Send size={20} />
//         </Button>
//       </div>
//     </div>
//   );
// }

import { useState } from "react";
import { Send } from "lucide-react";
import { Card, CardContent, Button, TextField } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";

export default function ChatApp() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I help you?", sender: "bot", timestamp: "12:00 PM" },
  ]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  const theme = createTheme({
    palette: {
      mode: darkMode ? "dark" : "light",
      primary: {
        main: "#25D366", // WhatsApp green
      },
      secondary: {
        main: "#f50057",
      },
      background: {
        default: darkMode ? "#121212" : "#f5f5f5",
      },
    },
  });

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Send the user's message
    const newMessage = { 
      id: messages.length + 1, 
      text: input, 
      sender: "user", 
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
    };
    setMessages([...messages, newMessage]);
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:5000/click", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          id: messages.length + 2,
          text: data.reply,
          sender: "bot",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } else {
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <div
        className="flex flex-col h-screen p-4 max-w-md mx-auto"
        style={{
          backgroundImage: `url("https://source.unsplash.com/1600x900/?travel")`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Card
          className="flex-1 overflow-y-auto p-4 bg-opacity-70 rounded-lg"
          style={{ maxHeight: "80vh", paddingBottom: "20px", borderRadius: "20px" }}
        >
          <CardContent>
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`mb-2 flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`inline-block px-4 py-2 rounded-lg max-w-xs ${msg.sender === "user" ? "bg-[#25D366] text-white" : "bg-[#f1f1f1] text-black"} `}
                  style={{
                    borderRadius: "20px",
                    animation: "fadeIn 0.5s",
                    marginBottom: "5px",
                  }}
                >
                  {msg.text}
                  <div className="text-xs text-gray-500 mt-1 text-right">{msg.timestamp}</div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
        <div className="flex items-center gap-2 mt-4">
          <TextField
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            fullWidth
            variant="outlined"
            size="small"
            style={{
              backgroundColor: darkMode ? "#333" : "#fff",
              borderRadius: "20px",
              padding: "10px 15px",
              color: darkMode ? "#fff" : "#000",
            }}
          />
          <Button
            onClick={sendMessage}
            variant="contained"
            color="primary"
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "10px",
              borderRadius: "50%",
              minWidth: "50px",
            }}
          >
            <Send size={20} />
          </Button>
        </div>
        <div className="mt-4 text-center">
          <Button
            variant="contained"
            color="secondary"
            onClick={() => setDarkMode(!darkMode)}
            style={{ borderRadius: "20px" }}
          >
            Toggle Dark Mode
          </Button>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        .message-bubble {
          display: inline-block;
          padding: 10px 15px;
          border-radius: 20px;
          max-width: 70%;
          word-wrap: break-word;
        }

        .user-message {
          background-color: #25D366;
          color: white;
          margin-left: auto;
        }

        .bot-message {
          background-color: #f1f1f1;
          color: black;
          margin-right: auto;
        }

        .message-timestamp {
          font-size: 12px;
          color: #999;
          text-align: right;
        }
      `}</style>
    </ThemeProvider>
  );
}
