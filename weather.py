from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather", log_level="ERROR")

API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app-test/0.1"

async def make_nws_request(url: str) -> dict[str, Any]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """
    Format the alert information into a string.
    """
    props = feature["properties"]
    return f"""
Events: {props.get("event", "N/A")}
Area: {props.get("areaDesc", "N/A")}
Severity: {props.get("severity", "N/A")}
Description: {props.get("description", "N/A")}
Instructions: {props.get("instruction", "N/A")}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a given latitude and longitude.
    """
    url = f"{API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "Failed to retrieve data."
    
    if not data["features"]:
        return "No alerts found."
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n----\n".join(alerts)

@mcp.tool()
async def get_forecast(lat: float, lon: float) -> str:
    """
    Get the weather forecast for a given latitude and longitude.
    """
    points_url = f"{API_BASE}/points/{lat},{lon}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Failed to retrieve data."
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Failed to retrieve forecast data."
    
    # format the forecast data
    periods = forecast_data["properties"]["periods"]
    forecasts = []

    for period in periods[:5]:
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
        """
        forecasts.append(forecast.strip())

    return "\n----\n".join(forecasts)

if __name__ == "__main__":
    mcp.run(transport='stdio')