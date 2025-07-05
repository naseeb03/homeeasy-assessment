# Sales Performance Analysis API

A comprehensive backend system that uses Large Language Models (LLM) to analyze sales data and provide intelligent feedback on both individual sales representatives and overall team performance.

## 🚀 Features

- **Individual Sales Rep Analysis**: Get detailed performance insights for specific sales representatives
- **Team Performance Summary**: Comprehensive analysis of overall sales team performance
- **Trend Analysis & Forecasting**: Identify sales trends and forecast future performance
- **AI-Powered Insights**: Leverage Google's Gemini AI for intelligent analysis and recommendations
- **RESTful API**: Clean, well-documented API endpoints
- **Comprehensive Data Processing**: Support for CSV data with flexible data ingestion

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │ Data Analysis   │    │   LLM Service   │
│   (main.py)     │◄──►│   Service       │◄──►│  (Gemini AI)    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        
         ▼                        ▼                        
┌─────────────────┐    ┌─────────────────┐              
│   API Endpoints │    │   Data Loader   │              
│   - /api/rep_*  │    │   (CSV/JSON)    │              
│   - /api/team_* │    │                 │              
│   - /api/perf_* │    │                 │              
└─────────────────┘    └─────────────────┘              
```

## 📋 Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)
- Google Gemini API key

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd homeeasy
```

### 2. Set up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory with your Gemini API key:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Data Setup

Place your CSV file named `sales_performance_data.csv` in the root directory. The system expects the following columns:

- `employee_id`, `employee_name`
- `lead_taken`, `tours_booked`, `applications`
- `revenue_confirmed`, `revenue_pending`, `revenue_runrate`
- `avg_deal_value_30_days`, `avg_close_rate_30_days`
- Daily activity columns: `mon_text`, `tue_text`, etc.

## 🚀 Running the Application

### Start the Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the application
python main.py
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

### Development Mode

The server runs in development mode by default with auto-reload enabled. Any changes to the code will automatically restart the server.

## 📚 API Documentation

### Core Endpoints

#### 1. Individual Sales Representative Performance Analysis

**GET** `/api/rep_performance`

Get detailed performance analysis for a specific sales representative.

**Parameters:**
- `rep_id` (integer, required): Employee ID of the sales representative

**Example:**
```bash
curl -X GET "http://localhost:8000/api/rep_performance?rep_id=183"
```

**Response:**
```json
{
  "employee_id": 183,
  "employee_name": "Camilla Ali",
  "performance_metrics": {
    "current_performance": {
      "conversion_rate": 0.25,
      "revenue_per_lead": 1200.50,
      "activity_score": 85.0,
      "pipeline_health": {...}
    },
    "historical_trends": {...}
  },
  "llm_analysis": "Detailed AI-generated analysis...",
  "historical_records": 12,
  "last_updated": "2022-07-26"
}
```

#### 2. Overall Sales Team Performance Summary

**GET** `/api/team_performance`

Get comprehensive team performance analysis.

**Example:**
```bash
curl -X GET "http://localhost:8000/api/team_performance"
```

**Response:**
```json
{
  "team_metrics": {
    "overview": {
      "total_employees": 25,
      "total_leads": 15420,
      "total_tours": 8930,
      "total_applications": 3470,
      "total_confirmed_revenue": 2450000,
      "total_pending_revenue": 890000
    },
    "averages": {...},
    "top_performers": {...}
  },
  "llm_analysis": "Team performance insights...",
  "total_records": 2536,
  "unique_employees": 25
}
```

#### 3. Sales Performance Trends and Forecasting

**GET** `/api/performance_trends`

Analyze sales trends and get forecasting insights.

**Parameters:**
- `time_period` (string, optional): "monthly" or "quarterly" (default: "monthly")

**Example:**
```bash
curl -X GET "http://localhost:8000/api/performance_trends?time_period=monthly"
```

### Helper Endpoints

#### Get Available Employees

**GET** `/api/employees`

Returns list of all employees with their IDs.

#### Search Employees

**GET** `/api/employees/search?query=John`

Search employees by name.

#### Data Statistics

**GET** `/api/data/stats`

Get basic statistics about the loaded data.

#### Health Check

**GET** `/health`

Check API and service health status.

## 🔧 Testing with API Tools

### Using cURL

```bash
# Test individual performance
curl -X GET "http://localhost:8000/api/rep_performance?rep_id=183"

# Test team performance
curl -X GET "http://localhost:8000/api/team_performance"

# Test trend analysis
curl -X GET "http://localhost:8000/api/performance_trends?time_period=monthly"

# Get employee list
curl -X GET "http://localhost:8000/api/employees"
```

### Using Postman

1. Import the API documentation from `http://localhost:8000/docs`
2. Create a new collection for the Sales Performance API
3. Add the core endpoints:
   - `GET http://localhost:8000/api/rep_performance?rep_id=183`
   - `GET http://localhost:8000/api/team_performance`
   - `GET http://localhost:8000/api/performance_trends?time_period=monthly`

## 🧪 Testing

### Manual Testing

1. **Health Check**: Visit `http://localhost:8000/health`
2. **API Documentation**: Visit `http://localhost:8000/docs`
3. **Test Endpoints**: Use the interactive documentation to test each endpoint

### Example Test Scenarios

1. **Valid Employee Analysis**:
   ```bash
   curl -X GET "http://localhost:8000/api/rep_performance?rep_id=183"
   ```

2. **Invalid Employee ID**:
   ```bash
   curl -X GET "http://localhost:8000/api/rep_performance?rep_id=99999"
   ```

3. **Team Performance**:
   ```bash
   curl -X GET "http://localhost:8000/api/team_performance"
   ```

## 📁 Project Structure

```
homeeasy/
├── main.py                      # FastAPI application
├── data_analysis_service.py     # Data processing and analysis
├── llm_service.py               # Gemini AI integration
├── data_loader.py               # CSV data loading utilities
├── sales_performance_data.csv   # Sales data file
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── README.md                    # This file
└── venv/                        # Virtual environment
```

## 🔍 Key Components

### 1. Data Loader (`data_loader.py`)
- Handles CSV file loading with pandas
- Provides data validation and error handling
- Supports flexible data ingestion

### 2. LLM Service (`llm_service.py`)
- Integrates with Google's Gemini AI
- Generates intelligent analysis and recommendations
- Handles different types of analysis (individual, team, trends)

### 3. Data Analysis Service (`data_analysis_service.py`)
- Processes and analyzes sales data
- Calculates performance metrics and trends
- Interfaces between data and LLM services

### 4. FastAPI Application (`main.py`)
- Provides RESTful API endpoints
- Handles HTTP requests and responses
- Includes comprehensive error handling and logging

## 📊 Data Requirements

The system expects a CSV file with the following structure:

| Column | Description |
|--------|-------------|
| `employee_id` | Unique identifier for each employee |
| `employee_name` | Employee's full name |
| `lead_taken` | Number of leads taken |
| `tours_booked` | Number of tours booked |
| `applications` | Number of applications submitted |
| `revenue_confirmed` | Confirmed revenue amount |
| `revenue_pending` | Pending revenue amount |
| `avg_close_rate_30_days` | 30-day average close rate |
| `mon_text`, `tue_text`, etc. | Daily text activity counts |
| `mon_call`, `tue_call`, etc. | Daily call activity counts |

## 🚨 Error Handling

The API includes comprehensive error handling:

- **404 Not Found**: When employee ID doesn't exist
- **422 Validation Error**: When request parameters are invalid
- **500 Internal Server Error**: For unexpected errors
- **503 Service Unavailable**: When services are not available

## 📈 Performance Considerations

- Data is loaded once at startup for optimal performance
- LLM requests are cached where possible
- Efficient pandas operations for data processing
- Async/await patterns for non-blocking operations

## 🔒 Security Notes

- CORS is enabled for all origins (configure for production)
- API key should be kept secure in environment variables
- Consider rate limiting for production deployment
- Input validation is implemented for all endpoints

## 🚀 Deployment Notes

For production deployment:

1. Set `allow_origins` in CORS middleware to specific domains
2. Use environment variables for all configuration
3. Consider using a production WSGI server like Gunicorn
4. Implement proper logging and monitoring
5. Set up database instead of CSV for larger datasets

## 💡 Future Enhancements

- Database integration for larger datasets
- User authentication and authorization
- Real-time data updates
- Advanced analytics and visualizations
- Export capabilities for reports
- Email notifications for performance alerts

## 📞 Support

For questions or issues:
1. Check the API documentation at `http://localhost:8000/docs`
2. Review the error logs in the console
3. Ensure all dependencies are installed correctly
4. Verify the `.env` file contains the correct API key

## 📝 License

This project is developed as part of a backend development assessment. 