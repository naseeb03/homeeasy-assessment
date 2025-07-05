import pandas as pd
from typing import Dict, Any, Optional
from data_loader import load_sales_data
from llm_service import LLMService
import numpy as np
from datetime import datetime, timedelta

class DataAnalysisService:
    def __init__(self):
        """Initialize the data analysis service."""
        self.llm_service = LLMService()
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load the sales performance data."""
        try:
            self.data = load_sales_data()
            print(f"Data loaded successfully: {len(self.data)} records")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = pd.DataFrame()
    
    def get_employee_data(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """
        Get employee data by ID.
        
        Args:
            employee_id: Employee ID to search for
            
        Returns:
            Dictionary containing employee data or None if not found
        """
        if self.data is None or self.data.empty:
            return None
        
        employee_records = self.data[self.data['employee_id'] == employee_id]
        if employee_records.empty:
            return None
        
        # Get the most recent record for the employee
        latest_record = employee_records.iloc[-1]
        return latest_record.to_dict()
    
    def get_employee_performance_analysis(self, employee_id: int) -> Dict[str, Any]:
        """
        Get comprehensive performance analysis for a specific employee.
        
        Args:
            employee_id: Employee ID to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        employee_data = self.get_employee_data(employee_id)
        if not employee_data:
            return {
                "error": f"Employee with ID {employee_id} not found",
                "employee_id": employee_id
            }
        
        # Get historical data for the employee
        historical_data = self.data[self.data['employee_id'] == employee_id]
        
        # Calculate additional metrics
        performance_metrics = self._calculate_employee_metrics(employee_data, historical_data)
        
        # Generate LLM analysis
        llm_analysis = self.llm_service.analyze_individual_performance(employee_data)
        
        return {
            "employee_id": employee_id,
            "employee_name": employee_data.get('employee_name', 'Unknown'),
            "performance_metrics": performance_metrics,
            "llm_analysis": llm_analysis,
            "historical_records": len(historical_data),
            "last_updated": employee_data.get('dated', 'Unknown')
        }
    
    def get_team_performance_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive team performance analysis.
        
        Returns:
            Dictionary containing team analysis results
        """
        if self.data is None or self.data.empty:
            return {"error": "No data available for analysis"}
        
        # Calculate team metrics
        team_metrics = self._calculate_team_metrics()
        
        # Generate LLM analysis
        llm_analysis = self.llm_service.analyze_team_performance(self.data)
        
        return {
            "team_metrics": team_metrics,
            "llm_analysis": llm_analysis,
            "total_records": len(self.data),
            "unique_employees": self.data['employee_id'].nunique(),
            "analysis_date": datetime.now().isoformat()
        }
    
    def get_performance_trends(self, time_period: str = "monthly") -> Dict[str, Any]:
        """
        Get performance trends and forecasting analysis.
        
        Args:
            time_period: Time period for analysis (monthly, quarterly)
            
        Returns:
            Dictionary containing trend analysis
        """
        if self.data is None or self.data.empty:
            return {"error": "No data available for analysis"}
        
        # Calculate trend metrics
        trend_metrics = self._calculate_trend_metrics(time_period)
        
        # Generate LLM analysis
        llm_analysis = self.llm_service.analyze_performance_trends(self.data, time_period)
        
        return {
            "time_period": time_period,
            "trend_metrics": trend_metrics,
            "llm_analysis": llm_analysis,
            "analysis_date": datetime.now().isoformat()
        }
    
    def _calculate_employee_metrics(self, employee_data: Dict[str, Any], historical_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate additional metrics for an employee."""
        metrics = {
            "current_performance": {
                "conversion_rate": employee_data.get('apps_per_lead', 0),
                "revenue_per_lead": employee_data.get('revenue_confirmed', 0) / max(employee_data.get('lead_taken', 1), 1),
                "activity_score": self._calculate_activity_score(employee_data),
                "pipeline_health": self._calculate_pipeline_health(employee_data)
            },
            "historical_trends": {
                "total_records": len(historical_data),
                "avg_monthly_revenue": historical_data['revenue_confirmed'].mean(),
                "avg_monthly_leads": historical_data['lead_taken'].mean(),
                "performance_consistency": historical_data['revenue_confirmed'].std() / max(historical_data['revenue_confirmed'].mean(), 1)
            }
        }
        
        return metrics
    
    def _calculate_team_metrics(self) -> Dict[str, Any]:
        """Calculate comprehensive team metrics."""
        metrics = {
            "overview": {
                "total_employees": self.data['employee_id'].nunique(),
                "total_leads": int(self.data['lead_taken'].sum()),
                "total_tours": int(self.data['tours_booked'].sum()),
                "total_applications": int(self.data['applications'].sum()),
                "total_confirmed_revenue": int(self.data['revenue_confirmed'].sum()),
                "total_pending_revenue": int(self.data['revenue_pending'].sum())
            },
            "averages": {
                "avg_leads_per_employee": float(self.data['lead_taken'].mean()),
                "avg_revenue_per_employee": float(self.data['revenue_confirmed'].mean()),
                "avg_close_rate": float(self.data['avg_close_rate_30_days'].mean()),
                "avg_deal_value": float(self.data['avg_deal_value_30_days'].mean())
            },
            "conversion_metrics": {
                "team_tours_per_lead": float(self.data['tours_per_lead'].mean()),
                "team_apps_per_tour": float(self.data['apps_per_tour'].mean()),
                "team_apps_per_lead": float(self.data['apps_per_lead'].mean())
            },
            "top_performers": {
                "highest_revenue": self._get_top_performer('revenue_confirmed'),
                "highest_leads": self._get_top_performer('lead_taken'),
                "highest_applications": self._get_top_performer('applications'),
                "highest_close_rate": self._get_top_performer('avg_close_rate_30_days')
            }
        }
        
        return metrics
    
    def _calculate_trend_metrics(self, time_period: str) -> Dict[str, Any]:
        """Calculate trend-based metrics."""
        # Convert date columns
        data_copy = self.data.copy()
        data_copy['dated'] = pd.to_datetime(data_copy['dated'])
        
        # Calculate time-based groupings
        if time_period == "monthly":
            grouped = data_copy.groupby(data_copy['dated'].dt.to_period('M'))
        else:  # quarterly
            grouped = data_copy.groupby(data_copy['dated'].dt.to_period('Q'))
        
        trends = {
            "revenue_trend": grouped['revenue_confirmed'].sum().to_dict(),
            "lead_trend": grouped['lead_taken'].sum().to_dict(),
            "application_trend": grouped['applications'].sum().to_dict(),
            "close_rate_trend": grouped['avg_close_rate_30_days'].mean().to_dict()
        }
        
        # Convert Period objects to strings for JSON serialization
        for key, value in trends.items():
            trends[key] = {str(k): v for k, v in value.items()}
        
        # Calculate growth rates
        revenue_values = list(grouped['revenue_confirmed'].sum().values)
        if len(revenue_values) > 1:
            recent_growth = ((revenue_values[-1] - revenue_values[-2]) / max(revenue_values[-2], 1)) * 100
        else:
            recent_growth = 0
        
        metrics = {
            "trends": trends,
            "growth_metrics": {
                "recent_revenue_growth": float(recent_growth),
                "total_periods": len(revenue_values),
                "avg_period_revenue": float(np.mean(revenue_values)) if revenue_values else 0
            },
            "pipeline_metrics": {
                "total_pipeline_tours": int(self.data['tours_in_pipeline'].sum()),
                "total_pending_revenue": int(self.data['revenue_pending'].sum()),
                "avg_deal_value": float(self.data['avg_deal_value_30_days'].mean())
            }
        }
        
        return metrics
    
    def _calculate_activity_score(self, employee_data: Dict[str, Any]) -> float:
        """Calculate employee activity score based on daily activities."""
        total_texts = sum([
            employee_data.get(f'{day}_text', 0) 
            for day in ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun']
        ])
        total_calls = sum([
            employee_data.get(f'{day}_call', 0) 
            for day in ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun']
        ])
        
        # Weighted score (calls are worth more than texts)
        activity_score = (total_texts * 1) + (total_calls * 2)
        return float(activity_score)
    
    def _calculate_pipeline_health(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate pipeline health metrics."""
        total_tours = employee_data.get('tours_in_pipeline', 0) + employee_data.get('tours_scheduled', 0)
        cancelled_rate = employee_data.get('tours_cancelled', 0) / max(total_tours, 1)
        
        return {
            "pipeline_tours": employee_data.get('tours_in_pipeline', 0),
            "scheduled_tours": employee_data.get('tours_scheduled', 0),
            "cancelled_rate": float(cancelled_rate),
            "pending_revenue": employee_data.get('revenue_pending', 0)
        }
    
    def _get_top_performer(self, metric: str) -> Dict[str, Any]:
        """Get top performer for a specific metric."""
        if self.data is None or self.data.empty:
            return {"name": "Unknown", "value": 0, "employee_id": 0}
        
        top_performer = self.data.loc[self.data[metric].idxmax()]
        return {
            "name": top_performer.get('employee_name', 'Unknown'),
            "value": float(top_performer[metric]),
            "employee_id": int(top_performer['employee_id'])
        }
    
 