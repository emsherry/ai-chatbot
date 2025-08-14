# I2C AI Chatbot

An intelligent chatbot for i2cinc.com that scrapes website content and provides AI-powered responses to customer queries.

## 🚀 Features

- **Web Scraping**: Automatically scrapes and indexes content from i2cinc.com
- **AI-Powered Responses**: Uses advanced language models to provide intelligent answers
- **Real-time Chat**: Interactive chat interface with typing indicators and quick actions
- **Vector Search**: Efficient semantic search using ChromaDB for document retrieval
- **Production Ready**: Built with FastAPI backend and React frontend for scalability

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI**: Modern, fast Python web framework
- **ChromaDB**: Vector database for semantic search
- **LangChain**: Framework for building LLM applications
- **BeautifulSoup**: Web scraping capabilities
- **Pydantic**: Data validation using Python type hints

### Frontend (React)
- **React**: Modern UI framework with TypeScript
- **Axios**: HTTP client for API communication
- **Glassmorphism**: Modern UI design with glass effects
- **Responsive Design**: Works on desktop and mobile devices

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- pip (Python package manager)
- npm (Node package manager)

## 🛠️ Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 Running the Application

### Development Mode

1. Start the backend server:
```bash
cd backend
python run.py
```

2. In a new terminal, start the frontend:
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### Production Mode

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Start the backend in production mode:
```bash
cd backend
python run.py
```

## 📊 API Endpoints

### Chat Endpoints
- `POST /api/v1/chat/query` - Send a chat message
- `GET /api/v1/chat/health` - Health check for chat service

### Scrape Endpoints
- `POST /api/v1/scrape` - Manually trigger website scraping

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# API Configuration
APP_NAME=I2C AI Chatbot
ENVIRONMENT=development
API_V1_PREFIX=/api/v1

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]

# Scraping
BASE_URL=https://i2cinc.com
MAX_SCRAPE_PAGES=50
SCRAPE_DELAY=1

# Vector Store
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=i2c_documents

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

#### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Deployment

### Docker Deployment
```bash
docker-compose up --build
```

### Cloud Deployment
- **Heroku**: Follow the deployment guide in `DEPLOYMENT_GUIDE.md`
- **AWS**: Use AWS Elastic Beanstalk or EC2
- **Vercel**: Deploy frontend directly from GitHub
- **Render**: Deploy backend and frontend separately

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- i2cinc.com for providing the content
- FastAPI team for the excellent framework
- React team for the frontend library
