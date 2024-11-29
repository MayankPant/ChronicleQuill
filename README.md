

# ChronicleQuill 🪶  
A lightweight, real-time logging service for microservices, designed to handle high volumes efficiently with a sleek, user-friendly interface.

---

## Features  
- **Real-Time Logging**: View logs in real-time using WebSocket connections.  
- **Service Overview**: Get a summary of total logs and descriptions for each service.  
- **Dynamic Routing**: Navigate seamlessly to specific log viewers for granular monitoring.  
- **Efficient Architecture**: Logs are streamed directly from the backend without being stored in the frontend to manage large data volumes.  
- **Light & Dark Modes**: Switch between themes for a personalized experience.

---

## Technologies Used  
### Frontend  
- **React** (with **TypeScript**)  
- **WebSockets** for real-time updates  
- **Context API** for shared state management  

### Backend  
- **Django**  
- **Message Broker** with fanout exchange (e.g., RabbitMQ) for log distribution  
- **Queue-Based Processing** for scalable and decoupled log management  

---

## Getting Started  

### Prerequisites  
- Node.js  
- Docker  
- RabbitMQ  

### Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/chroniclequill.git
   cd chroniclequill

2. Install dependencies:  
   ```bash
   npm install
   ```

3. Start the development server:  
   ```bash
   npm start
   ```

4. Ensure RabbitMQ and backend services are running. Update WebSocket URLs in the `.env` file if necessary.  

---

## Usage  

1. Launch the application and navigate to the **Dashboard**.  
2. View a summary of all registered services with total log counts.  
3. Click the **View** button to open a real-time log viewer for the desired service.  
4. Use filtering options (if configured) to refine logs by priority, type, or timestamp.

---

## Project Structure  

```plaintext
chroniclequill/
├── public/               # Static assets
├── src/
│   ├── components/       # Reusable UI components
│   ├── context/          # WebSocket Context API setup
│   ├── pages/            # Application pages
│   ├── styles/           # Theming (Light/Dark)
│   └── utils/            # Helper functions
├── .env                  # Environment variables
├── README.md             # Project documentation
└── package.json          # NPM configuration
```

---

## Contributing  

We welcome contributions! To get started:  
1. Fork the repository.  
2. Create a new branch:  
   ```bash
   git checkout -b feature-name
   ```  
3. Commit your changes:  
   ```bash
   git commit -m "Add a feature"
   ```  
4. Push your branch:  
   ```bash
   git push origin feature-name
   ```  
5. Open a Pull Request.  

---

## License  
ChronicleQuill is licensed under the [MIT License](LICENSE).

---

## Acknowledgments  
Special thanks to all contributors who helped shape ChronicleQuill into a powerful logging solution.

---
```

Feel free to customize this to better fit your needs or organization!
