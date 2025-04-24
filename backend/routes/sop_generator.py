from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union
import time
from datetime import datetime

# Define Pydantic models for request validation - make fields optional
class DataPoint(BaseModel):
    id: str
    name: str
    table: str
    refreshRate: str
    source: str
    lastRefreshed: Optional[Union[str, datetime]] = None
    
    class Config:
        # Allow extra fields to be more flexible
        extra = "ignore"

class SOPRequest(BaseModel):
    dataPoints: List[DataPoint]
    template: Optional[str] = "default"
    audience: Optional[str] = "technical"
    goals: Optional[str] = ""
    
    class Config:
        # Allow extra fields to be more flexible
        extra = "ignore"

class SOPResponse(BaseModel):
    success: bool
    sopDocument: Optional[Dict[str, Any]] = None
    generatedAt: Optional[str] = None
    error: Optional[str] = None

# Create APIRouter
router = APIRouter(
    prefix="/api",
    tags=["SOP Generator"],
    responses={404: {"description": "Not found"}},
)

@router.post("/generate-sop", response_model=SOPResponse)
async def generate_sop(request: SOPRequest):
    """
    Generate a Standard Operating Procedure document based on the provided data points
    and configuration. This endpoint creates an SOP by analyzing data patterns,
    refresh rates, and relationships between the selected data points.
    """
    try:
        # Extract request data
        data_points = [point.dict(exclude_unset=True) for point in request.dataPoints]
        template_type = request.template
        audience = request.audience
        goals = request.goals
        
        # Validate request
        if not data_points:
            raise HTTPException(
                status_code=400, 
                detail="At least one data point must be provided"
            )
            
        # In a real implementation, this would call an AI service or use templates
        # For demo purposes, we'll generate a structured SOP based on the inputs
        
        # Analyze data points
        sop_content = generate_sop_content(data_points, template_type, audience, goals)
        
        # Return generated SOP
        return {
            'success': True,
            'sopDocument': sop_content,
            'generatedAt': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error generating SOP: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# For debugging purposes
@router.options("/generate-sop")
async def options_sop():
    """
    Handle OPTIONS requests for the generate-sop endpoint
    """
    return {}

def generate_sop_content(data_points, template_type, audience, goals):
    """
    Generate the actual SOP content based on data points and configuration.
    In a production environment, this would likely use an AI service or 
    sophisticated template engine.
    """
    # Simulate processing time
    time.sleep(1)
    
    # Extract data source types
    sources = set(point['source'] for point in data_points)
    source_counts = {source: len([p for p in data_points if p['source'] == source]) for source in sources}
    
    # Analyze refresh patterns
    refresh_patterns = analyze_refresh_patterns(data_points)
    
    # Generate appropriate sections based on template type
    if template_type == 'detailed':
        sections = generate_detailed_template(data_points, refresh_patterns, audience, goals)
    elif template_type == 'quickstart':
        sections = generate_quickstart_template(data_points, refresh_patterns, audience, goals)
    else:  # default template
        sections = generate_default_template(data_points, refresh_patterns, audience, goals)
    
    # Combine into final document
    sop_document = {
        'title': 'Standard Operating Procedure: Data Pipeline Management',
        'summary': f"This SOP covers the management of {len(data_points)} data points across {', '.join(sources)} sources",
        'audience': get_audience_description(audience),
        'sections': sections,
        'dataPointsSummary': {
            'totalPoints': len(data_points),
            'bySource': source_counts
        }
    }
    
    return sop_document


def analyze_refresh_patterns(data_points):
    """Analyze refresh patterns across data points to identify dependencies and recommend monitoring"""
    patterns = {
        'frequent': [],
        'daily': [],
        'weekly': [],
        'other': []
    }
    
    for point in data_points:
        refresh = point.get('refreshRate', '').lower()
        
        if 'hour' in refresh or 'minute' in refresh:
            patterns['frequent'].append(point['id'])
        elif 'daily' in refresh or 'day' in refresh:
            patterns['daily'].append(point['id'])
        elif 'week' in refresh:
            patterns['weekly'].append(point['id'])
        else:
            patterns['other'].append(point['id'])
    
    return patterns


def get_audience_description(audience):
    """Return a description based on the target audience"""
    descriptions = {
        'technical': 'This document is intended for data engineers and technical staff responsible for maintaining data pipelines.',
        'business': 'This document is intended for business users who rely on these data sources for analytics and reporting.',
        'executive': 'This document provides a high-level overview for executive stakeholders on data pipeline operations.',
        'mixed': 'This document is intended for a diverse audience including both technical and business stakeholders.'
    }
    
    return descriptions.get(audience, descriptions['mixed'])


def generate_default_template(data_points, refresh_patterns, audience, goals):
    """Generate a standard template with balanced detail"""
    sections = [
        {
            'title': 'Overview',
            'content': f"This SOP outlines the procedures for monitoring and maintaining data pipelines across {len(data_points)} critical data points. " + 
                      (f"Key business objectives: {goals}" if goals else "")
        },
        {
            'title': 'Data Sources',
            'content': format_data_sources_section(data_points)
        },
        {
            'title': 'Monitoring Procedures',
            'content': generate_monitoring_procedures(data_points, refresh_patterns)
        },
        {
            'title': 'Troubleshooting Guide',
            'content': generate_troubleshooting_guide(data_points, refresh_patterns)
        },
        {
            'title': 'Refresh Schedule',
            'content': generate_refresh_schedule(data_points, refresh_patterns)
        }
    ]
    
    return sections


def generate_detailed_template(data_points, refresh_patterns, audience, goals):
    """Generate a detailed template with comprehensive information"""
    sections = generate_default_template(data_points, refresh_patterns, audience, goals)
    
    # Add additional detailed sections
    sections.extend([
        {
            'title': 'Data Lineage',
            'content': generate_data_lineage(data_points)
        },
        {
            'title': 'Quality Control Measures',
            'content': generate_quality_control(data_points)
        },
        {
            'title': 'Escalation Procedures',
            'content': 'Detailed steps for escalating issues based on severity and impact.'
        },
        {
            'title': 'Compliance and Governance',
            'content': 'Guidelines for ensuring data handling complies with organizational policies and regulatory requirements.'
        }
    ])
    
    return sections


def generate_quickstart_template(data_points, refresh_patterns, audience, goals):
    """Generate a simplified template for quick reference"""
    sections = [
        {
            'title': 'Quick Start',
            'content': f"Essential procedures for managing {len(data_points)} data points. " + 
                      (f"Key objectives: {goals}" if goals else "")
        },
        {
            'title': 'Key Data Points',
            'content': format_key_data_points(data_points)
        },
        {
            'title': 'Common Issues',
            'content': 'Concise troubleshooting steps for frequent issues.'
        }
    ]
    
    return sections


def format_data_sources_section(data_points):
    """Format information about data sources in a structured way"""
    snowflake_points = [p for p in data_points if p['source'] == 'snowflake']
    fabric_points = [p for p in data_points if p['source'] == 'fabric']
    
    content = []
    
    if snowflake_points:
        content.append("## Snowflake\n")
        for point in snowflake_points:
            content.append(f"- **{point['name']}** (`{point['table']}`): {point['refreshRate']}")
    
    if fabric_points:
        content.append("\n## Fabric\n")
        for point in fabric_points:
            content.append(f"- **{point['name']}** (`{point['table']}`): {point['refreshRate']}")
    
    return "\n".join(content)


def format_key_data_points(data_points):
    """Format key information about data points for quick reference"""
    content = []
    
    for point in data_points:
        last_refreshed_desc = get_refresh_description(point.get('lastRefreshed'))
        content.append(f"- **{point['name']}** ({point['source']})\n  - Table: `{point['table']}`\n  - Refresh: {point['refreshRate']}\n  - Last updated: {last_refreshed_desc}")
    
    return "\n".join(content)


def get_refresh_description(timestamp):
    """Generate a human-readable description of when the data was last refreshed"""
    if not timestamp:
        return "Unknown"
    
    try:
        last_refreshed = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else timestamp
        now = datetime.now()
        diff = now - last_refreshed
        
        if diff.days > 7:
            return f"{diff.days} days ago"
        elif diff.days > 0:
            return f"{diff.days} day(s) ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hour(s) ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minute(s) ago"
        else:
            return "Just now"
    except:
        return "Unknown format"


def generate_monitoring_procedures(data_points, refresh_patterns):
    """Generate monitoring procedures based on data refresh patterns"""
    procedures = [
        "## Regular Monitoring Tasks\n",
        "1. **Daily Checks**:",
        "   - Verify completion of overnight batch processes",
        "   - Check data freshness indicators for daily refreshed sources",
        "   - Review any alerts generated in the last 24 hours",
        "",
        "2. **Weekly Checks**:",
        "   - Validate weekly data refreshes were completed successfully",
        "   - Review data quality metrics for all sources",
        "   - Check for any anomalies in data patterns or volumes",
        "",
        "3. **Monthly Checks**:",
        "   - Perform comprehensive audit of all data pipelines",
        "   - Review performance metrics and optimize as needed",
        "   - Update documentation for any changes to data sources or procedures"
    ]
    
    # Add specific monitoring based on refresh patterns
    if refresh_patterns['frequent']:
        procedures.append("\n## High-Frequency Data Points\n")
        procedures.append("These data points update frequently and require more active monitoring:")
        for point_id in refresh_patterns['frequent']:
            point = next((p for p in data_points if p['id'] == point_id), None)
            if point:
                procedures.append(f"- **{point['name']}**: Check every {point['refreshRate'].lower()}")
    
    return "\n".join(procedures)


def generate_troubleshooting_guide(data_points, refresh_patterns):
    """Generate troubleshooting steps based on data sources and refresh patterns"""
    guide = [
        "## Common Issues and Solutions\n",
        
        "### Data Freshness Issues",
        "1. **Stale Data Detected**:",
        "   - Check source system connectivity",
        "   - Verify ETL job execution logs",
        "   - Check for upstream dependencies that may have failed",
        "",
        "### Data Quality Issues",
        "1. **Unexpected Null Values**:",
        "   - Verify source data integrity",
        "   - Check transformation logic for errors",
        "   - Review recent changes to data pipelines",
        "",
        "2. **Volume Anomalies**:",
        "   - Compare with historical patterns",
        "   - Check for changes in source systems",
        "   - Verify all data is being properly extracted"
    ]
    
    # Add source-specific troubleshooting
    if any(p['source'] == 'snowflake' for p in data_points):
        guide.append("\n### Snowflake-Specific Issues")
        guide.append("1. **Connection Issues**:")
        guide.append("   - Check network connectivity to Snowflake")
        guide.append("   - Verify credentials and access permissions")
        guide.append("   - Review warehouse suspension settings")
    
    if any(p['source'] == 'fabric' for p in data_points):
        guide.append("\n### Fabric-Specific Issues")
        guide.append("1. **API Rate Limiting**:")
        guide.append("   - Check for throttling messages in logs")
        guide.append("   - Implement exponential backoff if needed")
        guide.append("   - Review API quota usage")
    
    return "\n".join(guide)


def generate_refresh_schedule(data_points, refresh_patterns):
    """Generate a consolidated refresh schedule for all data points"""
    schedule = ["## Refresh Schedule Summary\n"]
    
    # Group by refresh pattern
    if refresh_patterns['frequent']:
        schedule.append("### Hourly/Sub-hourly")
        for point_id in refresh_patterns['frequent']:
            point = next((p for p in data_points if p['id'] == point_id), None)
            if point:
                schedule.append(f"- **{point['name']}** ({point['source']}): {point['refreshRate']}")
    
    if refresh_patterns['daily']:
        schedule.append("\n### Daily")
        for point_id in refresh_patterns['daily']:
            point = next((p for p in data_points if p['id'] == point_id), None)
            if point:
                schedule.append(f"- **{point['name']}** ({point['source']}): {point['refreshRate']}")
    
    if refresh_patterns['weekly']:
        schedule.append("\n### Weekly")
        for point_id in refresh_patterns['weekly']:
            point = next((p for p in data_points if p['id'] == point_id), None)
            if point:
                schedule.append(f"- **{point['name']}** ({point['source']}): {point['refreshRate']}")
    
    if refresh_patterns['other']:
        schedule.append("\n### Other Frequencies")
        for point_id in refresh_patterns['other']:
            point = next((p for p in data_points if p['id'] == point_id), None)
            if point:
                schedule.append(f"- **{point['name']}** ({point['source']}): {point['refreshRate']}")
    
    return "\n".join(schedule)


def generate_data_lineage(data_points):
    """Generate a description of data lineage across the selected data points"""
    # This would typically use more complex logic to determine actual data dependencies
    # For demo purposes, we'll create a simplified representation
    
    lineage = ["## Data Lineage\n"]
    
    lineage.append("### Source Systems")
    lineage.append("Data flows from these original sources through various transformations:")
    
    snowflake_points = [p for p in data_points if p['source'] == 'snowflake']
    fabric_points = [p for p in data_points if p['source'] == 'fabric']
    
    if snowflake_points:
        lineage.append("\n**Snowflake:**")
        for point in snowflake_points:
            lineage.append(f"- {point['table']}")
    
    if fabric_points:
        lineage.append("\n**Fabric:**")
        for point in fabric_points:
            lineage.append(f"- {point['table']}")
    
    lineage.append("\n### Dependencies")
    lineage.append("These data points have interdependencies that affect refresh scheduling and monitoring:")
    
    # Generate some mock dependencies for demonstration
    if len(data_points) > 1:
        lineage.append("\n```")
        lineage.append("Source Tables → Transformation → Target Tables")
        
        # Create some fictional dependencies
        for i in range(min(3, len(data_points) - 1)):
            source = data_points[i]
            target = data_points[(i + 1) % len(data_points)]
            lineage.append(f"{source['table']} → Transform → {target['table']}")
        
        lineage.append("```")
    
    return "\n".join(lineage)


def generate_quality_control(data_points):
    """Generate quality control measures for the data points"""
    qc = ["## Quality Control Measures\n"]
    
    qc.append("### Automated Checks")
    qc.append("The following automated checks are implemented to ensure data quality:")
    qc.append("1. **Completeness**: Verify all expected records are present")
    qc.append("2. **Validity**: Check that values conform to expected formats and ranges")
    qc.append("3. **Consistency**: Ensure data is consistent across related tables")
    qc.append("4. **Timeliness**: Verify data is updated according to schedule")
    
    qc.append("\n### Data Point Specific Checks")
    
    for point in data_points:
        qc.append(f"\n**{point['name']}**")
        
        # Generate checks based on the data point name/table
        if 'sales' in point['name'].lower() or 'sales' in point['table'].lower():
            qc.append("- Validate sales totals against financial systems")
            qc.append("- Check for negative values in revenue fields")
            qc.append("- Verify no duplicate transaction IDs")
        
        elif 'customer' in point['name'].lower() or 'customer' in point['table'].lower():
            qc.append("- Verify email format is valid where present")
            qc.append("- Check for duplicate customer records")
            qc.append("- Validate demographic data is within expected ranges")
        
        elif 'product' in point['name'].lower() or 'product' in point['table'].lower():
            qc.append("- Verify all products have valid categories")
            qc.append("- Check for negative inventory values")
            qc.append("- Validate pricing data is within expected ranges")
        
        elif 'traffic' in point['name'].lower() or 'traffic' in point['table'].lower():
            qc.append("- Verify page view counts are reasonable")
            qc.append("- Check for unusual traffic spikes")
            qc.append("- Validate referrer information")
        
        else:
            qc.append("- Validate no unexpected null values in key fields")
            qc.append("- Check data volumes against historical averages")
            qc.append("- Verify data format consistency")
    
    return "\n".join(qc) 