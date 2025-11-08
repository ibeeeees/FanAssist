# FanAssist NBA Props API Backend

A powerful FastAPI backend that leverages AWS Bedrock LLM to analyze NBA player statistics and provide intelligent betting prop recommendations specifically for PrizePicks.

## Features

- 🏀 **NBA Player Stats**: Real-time player statistics from NBA Stats API
- 🤖 **AI-Powered Analysis**: AWS Bedrock (Claude) integration for intelligent prop analysis
- 🎯 **PrizePicks Focus**: Specialized analysis for PrizePicks betting format
- 📊 **Comprehensive Analytics**: Season averages, recent form, and matchup analysis
- 🚀 **Fast API**: High-performance REST API with automatic documentation
- 🔒 **Secure**: Environment-based configuration for AWS credentials

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **LLM Service**: AWS Bedrock (Claude)
- **Data Source**: NBA Stats API
- **Runtime**: Python 3.8+
- **Cloud**: AWS (Bedrock)

## API Endpoints

### Players
- `GET /api/players/search` - Search for NBA players
- `GET /api/players/{player_name}/info` - Get player information
- `GET /api/players/{player_id}/stats/recent` - Get recent game stats
- `GET /api/players/{player_id}/stats/season` - Get season averages

### Props Analysis
- `POST /api/props/analyze` - Analyze multiple PrizePicks props
- `GET /api/props/quick/{player_name}` - Quick single prop analysis
- `GET /api/props/trending` - Get trending props
- `GET /api/props/prop-types` - Available prop types

### General Analysis
- `POST /api/analysis/betting-insights` - Get betting insights
- `GET /api/analysis/market-overview` - NBA market overview
- `GET /api/analysis/recommendations/general` - General betting advice

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd FanAssist/backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your AWS credentials
```

Required environment variables:
```env
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

### 4. Run the Application
```bash
# Development mode with auto-reload
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## AWS Setup

### Prerequisites
1. AWS Account with Bedrock access
2. Enable Claude model in AWS Bedrock console
3. IAM user with Bedrock permissions

### IAM Permissions
Your AWS user needs the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude*"
        }
    ]
}
```

### Supported Models
- `anthropic.claude-3-sonnet-20240229-v1:0` (Recommended)
- `anthropic.claude-3-haiku-20240307-v1:0` (Faster, cheaper)
- `amazon.titan-text-premier-v1:0`

## Usage Examples

### Analyze Multiple Props
```python
import requests

props_data = {
    "props": [
        {
            "player_name": "LeBron James",
            "prop_type": "points",
            "line": 25.5
        },
        {
            "player_name": "Stephen Curry",
            "prop_type": "threes_made",
            "line": 3.5
        }
    ],
    "analysis_depth": "standard"
}

response = requests.post("http://localhost:8000/api/props/analyze", json=props_data)
analysis = response.json()
```

### Quick Player Search
```python
import requests

# Search for players
response = requests.get("http://localhost:8000/api/players/search?query=LeBron")
players = response.json()

# Get player stats
player_id = players[0]["player_id"]
response = requests.get(f"http://localhost:8000/api/players/{player_id}/stats/recent?games=5")
recent_stats = response.json()
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── models/
│   │   └── __init__.py         # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── nba_stats.py        # NBA Stats API service
│   │   ├── aws_bedrock.py      # AWS Bedrock LLM service
│   │   └── prizepicks.py       # PrizePicks analysis service
│   └── routes/
│       ├── __init__.py
│       ├── players.py          # Player endpoints
│       ├── props.py            # Props analysis endpoints
│       └── analysis.py         # General analysis endpoints
├── run.py                      # Application entry point
├── requirements.txt            # Dependencies
├── requirements-dev.txt        # Development dependencies
├── .env.example               # Environment template
├── .gitignore
└── README.md
```

## Development

### Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Run Tests
```bash
pytest
```

### Code Style
```bash
# Format with black (if installed)
black app/

# Lint with flake8 (if installed)
flake8 app/
```

## Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/
COPY run.py .

EXPOSE 8000
CMD ["python", "run.py"]
```

### AWS Lambda
The application can be deployed to AWS Lambda using Mangum:
```bash
pip install mangum
```

## Monitoring and Logging

The application includes structured logging. Logs include:
- Request/response information
- Error tracking
- Performance metrics
- AWS Bedrock API calls

## Rate Limiting and Costs

### NBA Stats API
- Free tier with rate limiting
- Consider caching responses for better performance

### AWS Bedrock
- Pay-per-use pricing
- Claude models: ~$0.01-0.03 per 1K tokens
- Monitor usage in AWS Console

## Disclaimer

This application is for educational and entertainment purposes only. Always:
- Gamble responsibly
- Verify all statistics independently
- Follow local gambling laws and regulations
- Never bet more than you can afford to lose

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Ensure AWS credentials and permissions are correct
4. Verify NBA Stats API connectivity