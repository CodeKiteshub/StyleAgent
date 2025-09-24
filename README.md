# StyleAgent - AI-Powered Fashion Styling Platform

StyleAgent is a cutting-edge fashion recommendation system that combines computer vision, natural language processing, and retrieval-augmented generation (RAG) to provide personalized outfit recommendations and styling advice.

## 🌟 Features

### Core Functionality
- **AI-Powered Chat Interface**: Multi-turn conversations with an AI fashion consultant
- **Image Analysis**: Advanced computer vision for body type detection, pose analysis, and clothing recognition
- **Personalized Recommendations**: RAG-based outfit suggestions using vector similarity search
- **Trend Analysis**: Real-time fashion trend tracking and social media integration
- **User Profiles**: Comprehensive user management with preferences and history

### Technical Highlights
- **FastAPI Backend**: High-performance async API with automatic documentation
- **SQLAlchemy ORM**: Robust database modeling with relationship management
- **Vector Search**: Pinecone integration for semantic outfit matching
- **Computer Vision**: MediaPipe and OpenCV for pose detection and image analysis
- **AI Integration**: OpenAI GPT models for conversational AI and content generation
- **Authentication**: JWT-based secure authentication with refresh tokens

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite by default)
- Redis (optional, for caching)
- OpenAI API key
- Pinecone account (for vector search)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/styleagent.git
   cd styleagent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the application**
   ```bash
   cd backend
   python main.py
   ```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## 📁 Project Structure

```
styleagent/
├── backend/
│   ├── api/
│   │   └── routes/          # API endpoint definitions
│   │       ├── auth.py      # Authentication endpoints
│   │       ├── chat.py      # Chat conversation endpoints
│   │       ├── image.py     # Image analysis endpoints
│   │       ├── recommendations.py  # Outfit recommendation endpoints
│   │       └── users.py     # User management endpoints
│   ├── models/              # SQLAlchemy database models
│   │   ├── conversation.py  # Chat conversation models
│   │   ├── image_analysis.py # Image analysis models
│   │   ├── outfit.py        # Outfit and recommendation models
│   │   └── user.py          # User authentication models
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── chat.py          # Chat API schemas
│   │   ├── image.py         # Image analysis schemas
│   │   ├── recommendations.py # Recommendation schemas
│   │   └── user.py          # User management schemas
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py  # Authentication logic
│   │   ├── chat_service.py  # Chat conversation logic
│   │   ├── image_service.py # Image processing logic
│   │   ├── rag_service.py   # RAG recommendation logic
│   │   ├── trend_service.py # Trend analysis logic
│   │   └── user_service.py  # User management logic
│   ├── config.py            # Application configuration
│   ├── database.py          # Database connection setup
│   └── main.py              # FastAPI application entry point
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Database
DATABASE_URL=sqlite:///./styleagent.db

# Authentication
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services
OPENAI_API_KEY=your-openai-key
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=your-pinecone-env

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your-email
SMTP_PASSWORD=your-password
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - User logout

### Chat Endpoints
- `POST /api/chat/start` - Start new conversation
- `POST /api/chat/message` - Send message in conversation
- `GET /api/chat/conversations` - List user conversations
- `GET /api/chat/conversations/{id}` - Get conversation history

### Image Analysis Endpoints
- `POST /api/image/analyze` - Analyze uploaded image
- `GET /api/image/analysis/{id}` - Get analysis results
- `GET /api/image/analyses` - List user analyses

### Recommendation Endpoints
- `POST /api/recommendations/generate` - Generate outfit recommendations
- `POST /api/recommendations/similar` - Find similar outfits
- `GET /api/recommendations/trending` - Get trending outfits
- `GET /api/recommendations/feed` - Personalized outfit feed

### User Management Endpoints
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `PUT /api/users/preferences` - Update user preferences

## 🤖 AI Features

### Conversational AI
- Multi-turn fashion consultations
- Context-aware responses
- Personalized styling advice
- Budget and occasion-specific recommendations

### Computer Vision
- Body type detection and analysis
- Pose estimation for fit assessment
- Clothing item recognition
- Color palette extraction
- Style attribute classification

### Recommendation Engine
- Vector-based similarity search
- User preference learning
- Trend-aware suggestions
- Social media integration
- Collaborative filtering

## 🔒 Security Features

- JWT-based authentication with refresh tokens
- Password hashing with bcrypt
- Email verification system
- Rate limiting protection
- Input validation and sanitization
- CORS configuration
- SQL injection prevention

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=backend
```

## 🚀 Deployment

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t styleagent .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 --env-file .env styleagent
   ```

### Production Considerations

- Use PostgreSQL for production database
- Set up Redis for caching and sessions
- Configure proper CORS origins
- Use environment-specific secrets
- Set up monitoring and logging
- Configure reverse proxy (nginx)
- Enable HTTPS with SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models and embeddings
- Pinecone for vector database services
- MediaPipe for computer vision capabilities
- FastAPI for the excellent web framework
- The open-source community for various libraries and tools

## 📞 Support

For support, email support@styleagent.com or join our Discord community.

---

**StyleAgent** - Revolutionizing fashion with AI 🎨✨