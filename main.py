from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from data_analysis_service import DataAnalysisService
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sales Performance Analysis API",
    description="A comprehensive API for analyzing sales team performance using AI-powered insights",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data analysis service
try:
    analysis_service = DataAnalysisService()
    logger.info("Data analysis service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize data analysis service: {e}")
    analysis_service = None

# Pydantic models
class EmployeePerformanceResponse(BaseModel):
    employee_id: int
    employee_name: str
    performance_metrics: Dict[str, Any]
    llm_analysis: str
    historical_records: int
    last_updated: str

class TeamPerformanceResponse(BaseModel):
    team_metrics: Dict[str, Any]
    llm_analysis: str
    total_records: int
    unique_employees: int
    analysis_date: str

class TrendAnalysisResponse(BaseModel):
    time_period: str
    trend_metrics: Dict[str, Any]
    llm_analysis: str
    analysis_date: str



class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str

# Root endpoint
@app.get("/")
async def root():
    """API status."""
    return {"message": "Sales Performance Analysis API", "status": "running"}



# 1. Individual Sales Representative Performance Analysis
@app.get("/api/rep_performance", 
         response_model=EmployeePerformanceResponse,
         summary="Get Individual Sales Rep Performance Analysis")
async def get_rep_performance(
    rep_id: int = Query(..., description="Unique identifier for the sales representative", ge=1)
):
    """
    Returns detailed performance analysis and feedback for the specified sales representative.
    
    - **rep_id**: The unique employee ID of the sales representative
    - Returns comprehensive performance metrics and AI-generated insights
    """
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Data analysis service not available")
    
    try:
        logger.info(f"Analyzing performance for employee ID: {rep_id}")
        result = analysis_service.get_employee_performance_analysis(rep_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing rep performance: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 2. Overall Sales Team Performance Summary
@app.get("/api/team_performance", 
         response_model=TeamPerformanceResponse,
         summary="Get Overall Sales Team Performance Summary")
async def get_team_performance():
    """
    Provides a comprehensive summary of the sales team's overall performance.
    
    - Returns team-wide metrics, top performers, and AI-generated insights
    - Includes conversion rates, revenue metrics, and performance distribution
    """
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Data analysis service not available")
    
    try:
        logger.info("Analyzing team performance")
        result = analysis_service.get_team_performance_analysis()
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing team performance: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# 3. Sales Performance Trends and Forecasting
@app.get("/api/performance_trends", 
         response_model=TrendAnalysisResponse,
         summary="Get Sales Performance Trends and Forecasting")
async def get_performance_trends(
    time_period: str = Query(
        "monthly", 
        description="Time period for analysis (monthly, quarterly)", 
        regex="^(monthly|quarterly)$"
    )
):
    """
    Analyzes sales data over the specified time period to identify trends and forecast future performance.
    
    - **time_period**: Analysis period - either "monthly" or "quarterly"
    - Returns trend analysis, growth metrics, and AI-generated forecasting insights
    """
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Data analysis service not available")
    
    try:
        logger.info(f"Analyzing performance trends for period: {time_period}")
        result = analysis_service.get_performance_trends(time_period)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing performance trends: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error="Not Found",
            detail=str(exc.detail) if hasattr(exc, 'detail') else "Resource not found",
            timestamp=datetime.now().isoformat()
        ).dict()
    )

@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail=str(exc.detail) if hasattr(exc, 'detail') else "An unexpected error occurred",
            timestamp=datetime.now().isoformat()
        ).dict()
    )

# Development server
if __name__ == "__main__":
    print("Starting Sales Performance Analysis API...")
    print("API Documentation available at: http://localhost:8000/docs")
    print("Alternative documentation at: http://localhost:8000/redoc")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
