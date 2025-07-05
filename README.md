# Sales Performance Analysis API

A backend system that analyzes sales data using Large Language Models (LLM) to provide intelligent insights on individual sales representatives and overall team performance.

## Project Overview

This API processes sales performance data from CSV files and generates AI-powered analysis and recommendations using Google's Gemini AI. It provides three main endpoints for analyzing sales data at different levels - individual representatives, team-wide performance, and performance trends over time.

## API Endpoints

### 1. Individual Sales Representative Performance Analysis
**`GET /api/rep_performance?rep_id={employee_id}`**

Analyzes performance data for a specific sales representative and provides:
- Current performance metrics (conversion rates, activity scores, pipeline health)
- Historical performance trends
- AI-generated analysis with actionable recommendations

### 2. Overall Sales Team Performance Summary  
**`GET /api/team_performance`**

Provides comprehensive team-wide analysis including:
- Team overview metrics (total leads, revenue, applications)
- Performance averages and conversion metrics
- Top performer identification
- AI-generated team performance insights and recommendations

### 3. Sales Performance Trends and Forecasting
**`GET /api/performance_trends?time_period={monthly|quarterly}`**

Analyzes sales trends over specified time periods and provides:
- Revenue and lead generation trends
- Growth metrics and forecasting
- Pipeline health assessment
- AI-generated trend analysis and future predictions

## Architecture Overview

The system follows a layered architecture with the following components:

- **FastAPI Application** - Handles HTTP requests and API routing
- **Data Analysis Service** - Processes sales data and calculates performance metrics
- **LLM Service** - Integrates with Google Gemini AI for intelligent analysis
- **Data Loader** - Handles CSV file loading and data validation

## Technologies Used

- **Backend Framework**: FastAPI
- **Data Processing**: Pandas, NumPy
- **AI/LLM**: Google Gemini AI (gemini-1.5-flash)
- **Server**: Uvicorn
- **Data Format**: CSV
- **Language**: Python 3.8+

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Add Gemini API key to `.env` file: `GEMINI_API_KEY=your_key_here`
3. Place sales data CSV file in root directory as `sales_performance_data.csv`
4. Run server: `./run.sh` or `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

API documentation available at: `http://localhost:8000/docs` 