# Kul Setu Backend

A Flask-based backend API for the Kul Setu family tree application with ML-enhanced search capabilities.

## Features

- 🗃️ **PostgreSQL Database**: External database hosted on Render
- 🔍 **ML Search**: TF-IDF vectorization with cosine similarity search
- 👨‍👩‍👧‍👦 **Family Tree**: Complete genealogical data management
- 🌐 **REST API**: Full CRUD operations for family members
- 📊 **CSV Import**: Bulk data loading from tree.csv

## Database Schema

The application uses a comprehensive 36-field schema including:
- **Personal Info**: Person ID, name, gender, ethnicity
- **Relationships**: Mother, father, spouse connections
- **Health Data**: Medical conditions, blood group, physical traits
- **Cultural Info**: Traditions, cuisine, migration history
- **Demographics**: Birth/death dates, location, education

## Quick Start

### 1. Environment Setup
```bash
python setup.py
```

### 2. Database Initialization
```bash
python deploy.py
```

### 3. Start the Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Family Members
- `GET /members` - Get all family members
- `POST /register` - Register new family member
- `GET /member/<id>` - Get specific family member
- `PUT /member/<id>` - Update family member
- `DELETE /member/<id>` - Delete family member

### Search
- `POST /search` - Advanced search with ML similarity
- `GET /search/suggestions` - Get search suggestions

### Family Tree
- `GET /family-lines` - Get all unique family lines
- `GET /family-tree/<family_line_id>` - Get family tree for specific line

## Database Configuration

The application connects to an external PostgreSQL database on Render:

```python
DATABASE_URL = "postgresql://kul_setu_db_user:5xvepfwEtYa0Bzx89vyTiTnUqkJWG437@dpg-d3kjv2ffte5s738ehdh0-a.oregon-postgres.render.com/kul_setu_db"
```

## Development

### Testing Database Connection
```bash
python test_db.py
```

### Manual Database Operations
```python
from app import init_db, load_csv_data

# Initialize database
init_db()

# Load CSV data
load_csv_data()
```

## Dependencies

- Flask - Web framework
- Flask-CORS - Cross-origin requests
- psycopg2-binary - PostgreSQL adapter
- scikit-learn - ML search features
- numpy - Numerical operations
- gunicorn - Production server

## File Structure

```
kul-setu-backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── tree.csv           # Family data (to be imported)
├── setup.py           # Environment setup script
├── deploy.py          # Database deployment script
├── test_db.py         # Database connection test
└── README.md          # This file
```

## ML Search Engine

The backend includes a sophisticated search engine that:

1. **Text Vectorization**: Uses TF-IDF to convert text fields into numerical vectors
2. **Similarity Calculation**: Employs cosine similarity to find matches
3. **Multi-field Search**: Searches across name, location, traditions, and more
4. **Ranking**: Returns results sorted by relevance score

## Production Deployment

### Environment Variables
For production, set the database URL as an environment variable:
```bash
export DATABASE_URL="postgresql://user:pass@host:port/db"
```

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Health Check

The application includes basic health check endpoints:
- `GET /` - Basic server status
- `GET /health` - Database connectivity check

## Error Handling

The API includes comprehensive error handling with appropriate HTTP status codes:
- 200: Success
- 400: Bad request
- 404: Not found
- 500: Internal server error

## Security Notes

- Database credentials are included for demo purposes
- In production, use environment variables for sensitive data
- Consider implementing authentication for write operations
- Add rate limiting for search endpoints

## Support

For issues or questions regarding the backend setup, check:
1. Database connectivity with `python test_db.py`
2. CSV file format matches expected schema
3. All dependencies are installed correctly

## License

This project is part of the Kul Setu family tree application.