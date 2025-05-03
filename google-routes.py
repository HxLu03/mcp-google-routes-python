from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("google-routes", log_level="ERROR")

API_BASE = "https://routes.googleapis.com/directions/v2:computeRoutes"
CONTENT_TYPE = "application/json"
# X-Goog-Api-Key
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
# X-Goog-FieldMask
FIELD_MASK = "routes.legs,routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"

@mcp.tool()
async def get_route(
    origin: str,
    destination: str,
    travel_mode: str = "TRANSIT",
    computeAlternativeRoutes: bool = True,
) -> Any:
    """
    Calls Google Directions API to compute routes between origin and destination.
    """
    headers = {
        "Content-Type": CONTENT_TYPE,
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": FIELD_MASK,
    }
    body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": travel_mode,
        "computeAlternativeRoutes": computeAlternativeRoutes,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(API_BASE, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    

if __name__ == "__main__":
    mcp.run(transport='stdio')