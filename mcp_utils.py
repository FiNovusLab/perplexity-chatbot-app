import requests
import json

def validate_mcp_server(url):
    """
    MCP 서버 URL이 유효한지 확인합니다.
    """
    try:
        response = requests.get(f"{url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_mcp_server_info(url):
    """
    MCP 서버의 정보를 가져옵니다.
    """
    try:
        response = requests.get(f"{url}/info", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_available_tools(url):
    """
    MCP 서버에서 사용 가능한 도구 목록을 가져옵니다.
    """
    try:
        response = requests.get(f"{url}/tools", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def call_mcp_tool(url, tool_name, parameters):
    """
    MCP 서버의 도구를 호출합니다.
    """
    try:
        response = requests.post(
            f"{url}/tools/{tool_name}",
            json=parameters,
            timeout=30
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}
