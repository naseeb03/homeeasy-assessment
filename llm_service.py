import os
import pandas as pd
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self):
        """Initialize the LLM service with Gemini AI."""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_individual_performance(self, employee_data: Dict[str, Any]) -> str:
        """
        Analyze individual sales representative performance using LLM.
        
        Args:
            employee_data: Dictionary containing employee performance metrics
            
        Returns:
            str: LLM-generated analysis and recommendations
        """
        prompt = f"""
        You are a sales performance analyst. Analyze the following sales representative's performance data and provide detailed insights:

        Employee: {employee_data.get('employee_name', 'Unknown')}
        Employee ID: {employee_data.get('employee_id', 'Unknown')}
        
        Performance Metrics:
        - Leads Taken: {employee_data.get('lead_taken', 0)}
        - Tours Booked: {employee_data.get('tours_booked', 0)}
        - Applications: {employee_data.get('applications', 0)}
        - Tours per Lead: {employee_data.get('tours_per_lead', 0):.2f}
        - Apps per Tour: {employee_data.get('apps_per_tour', 0):.2f}
        - Apps per Lead: {employee_data.get('apps_per_lead', 0):.2f}
        
        Revenue Metrics:
        - Revenue Confirmed: ${employee_data.get('revenue_confirmed', 0):,}
        - Revenue Pending: ${employee_data.get('revenue_pending', 0):,}
        - Revenue Runrate: ${employee_data.get('revenue_runrate', 0):,}
        - Estimated Revenue: ${employee_data.get('estimated_revenue', 0):,}
        - Average Deal Value (30 days): ${employee_data.get('avg_deal_value_30_days', 0):,}
        - Average Close Rate (30 days): {employee_data.get('avg_close_rate_30_days', 0):.2f}%
        
        Activity Metrics:
        - Tours in Pipeline: {employee_data.get('tours_in_pipeline', 0)}
        - Tours Scheduled: {employee_data.get('tours_scheduled', 0)}
        - Tours Pending: {employee_data.get('tours_pending', 0)}
        - Tours Cancelled: {employee_data.get('tours_cancelled', 0)}
        
        Daily Activity (Texts/Calls):
        - Monday: {employee_data.get('mon_text', 0)} texts, {employee_data.get('mon_call', 0)} calls
        - Tuesday: {employee_data.get('tue_text', 0)} texts, {employee_data.get('tue_call', 0)} calls
        - Wednesday: {employee_data.get('wed_text', 0)} texts, {employee_data.get('wed_call', 0)} calls
        - Thursday: {employee_data.get('thur_text', 0)} texts, {employee_data.get('thur_call', 0)} calls
        - Friday: {employee_data.get('fri_text', 0)} texts, {employee_data.get('fri_call', 0)} calls
        - Saturday: {employee_data.get('sat_text', 0)} texts, {employee_data.get('sat_call', 0)} calls
        - Sunday: {employee_data.get('sun_text', 0)} texts, {employee_data.get('sun_call', 0)} calls

        Please provide:
        1. Overall performance assessment
        2. Key strengths and areas for improvement
        3. Specific actionable recommendations
        4. Comparison with typical industry benchmarks
        5. Suggested focus areas for the next 30 days

        Format your response in a clear, professional manner with bullet points and sections.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating analysis: {str(e)}"
    
    def analyze_team_performance(self, team_data: pd.DataFrame) -> str:
        """
        Analyze overall team performance using LLM.
        
        Args:
            team_data: DataFrame containing team performance metrics
            
        Returns:
            str: LLM-generated team analysis
        """
        # Calculate team aggregates
        total_leads = team_data['lead_taken'].sum()
        total_tours = team_data['tours_booked'].sum()
        total_applications = team_data['applications'].sum()
        total_confirmed_revenue = team_data['revenue_confirmed'].sum()
        total_pending_revenue = team_data['revenue_pending'].sum()
        avg_close_rate = team_data['avg_close_rate_30_days'].mean()
        
        # Top performers
        top_revenue_performer = team_data.loc[team_data['revenue_confirmed'].idxmax()]
        top_lead_performer = team_data.loc[team_data['lead_taken'].idxmax()]
        
        prompt = f"""
        You are a sales team performance analyst. Analyze the following sales team's overall performance:

        Team Overview:
        - Total Team Members: {len(team_data)}
        - Total Leads Taken: {total_leads:,}
        - Total Tours Booked: {total_tours:,}
        - Total Applications: {total_applications:,}
        - Total Confirmed Revenue: ${total_confirmed_revenue:,}
        - Total Pending Revenue: ${total_pending_revenue:,}
        - Average Team Close Rate: {avg_close_rate:.2f}%

        Performance Distribution:
        - Highest Revenue Generator: {top_revenue_performer['employee_name']} (${top_revenue_performer['revenue_confirmed']:,})
        - Highest Lead Generator: {top_lead_performer['employee_name']} ({top_lead_performer['lead_taken']} leads)
        - Average Revenue per Rep: ${team_data['revenue_confirmed'].mean():,.0f}
        - Average Leads per Rep: {team_data['lead_taken'].mean():.1f}
        - Average Apps per Rep: {team_data['applications'].mean():.1f}

        Conversion Metrics:
        - Team Tours per Lead: {team_data['tours_per_lead'].mean():.2f}
        - Team Apps per Tour: {team_data['apps_per_tour'].mean():.2f}
        - Team Apps per Lead: {team_data['apps_per_lead'].mean():.2f}

        Please provide:
        1. Overall team performance assessment
        2. Key team strengths and challenges
        3. Performance distribution analysis (top performers vs. underperformers)
        4. Team-wide improvement recommendations
        5. Suggested team goals and KPIs for the next quarter
        6. Resource allocation recommendations

        Format your response professionally with clear sections and actionable insights.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating team analysis: {str(e)}"
    
    def analyze_performance_trends(self, team_data: pd.DataFrame, time_period: str = "monthly") -> str:
        """
        Analyze sales performance trends and provide forecasting.
        
        Args:
            team_data: DataFrame containing performance data
            time_period: Time period for analysis (monthly, quarterly)
            
        Returns:
            str: LLM-generated trend analysis and forecasting
        """
        # Convert date columns
        team_data['created'] = pd.to_datetime(team_data['created'])
        team_data['dated'] = pd.to_datetime(team_data['dated'])
        
        # Calculate time-based metrics
        date_range = team_data['dated'].max() - team_data['dated'].min()
        latest_month_data = team_data[team_data['dated'] >= team_data['dated'].max() - timedelta(days=30)]
        
        # Revenue trend analysis
        revenue_trend = team_data.groupby(team_data['dated'].dt.to_period('M'))['revenue_confirmed'].sum()
        lead_trend = team_data.groupby(team_data['dated'].dt.to_period('M'))['lead_taken'].sum()
        
        prompt = f"""
        You are a sales forecasting analyst. Analyze the following sales performance trends and provide forecasting insights:

        Data Overview:
        - Date Range: {date_range.days} days
        - Analysis Period: {time_period}
        - Total Records: {len(team_data)}
        - Latest Month Performance: {len(latest_month_data)} records

        Current Performance Metrics:
        - Current Month Revenue: ${latest_month_data['revenue_confirmed'].sum():,}
        - Current Month Leads: {latest_month_data['lead_taken'].sum():,}
        - Current Month Applications: {latest_month_data['applications'].sum():,}
        - Current Month Average Close Rate: {latest_month_data['avg_close_rate_30_days'].mean():.2f}%

        Trend Indicators:
        - Revenue Runrate: ${team_data['revenue_runrate'].mean():,.0f}
        - Tours in Pipeline: {team_data['tours_in_pipeline'].sum():,}
        - Pending Revenue: ${team_data['revenue_pending'].sum():,}
        - Average Deal Value Trend: ${team_data['avg_deal_value_30_days'].mean():,.0f}

        Performance Efficiency:
        - Average Tours per Lead: {team_data['tours_per_lead'].mean():.2f}
        - Average Apps per Tour: {team_data['apps_per_tour'].mean():.2f}
        - Team Activity Level: {team_data[['mon_text', 'tue_text', 'wed_text', 'thur_text', 'fri_text', 'sat_text', 'sun_text']].sum().sum()} total texts

        Please provide:
        1. Trend analysis for {time_period} performance
        2. Key performance indicators and their trajectories
        3. Seasonal patterns and insights
        4. Revenue and lead generation forecasts for the next 3 months
        5. Risk factors and opportunities
        6. Recommended actions to improve trends
        7. Pipeline health assessment

        Format your response with clear sections, data-driven insights, and actionable recommendations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating trend analysis: {str(e)}"
    
 