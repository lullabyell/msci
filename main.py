from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
import httpx
import datetime
import asyncio

app = FastAPI()

class VulnerablePackageResponse(BaseModel):
    name: str
    versions: List[str]
    timestamp: str

@app.get("/versions", response_model=VulnerablePackageResponse)
async def get_vulnerable_versions(name: str = Query(...)):
    try:
        return await fetch_vulnerable_versions(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def fetch_vulnerable_versions(package_name: str) -> VulnerablePackageResponse:
    ecosystems = ['Debian', 'Ubuntu']
    unique_versions = set()
    
    async with httpx.AsyncClient() as client:
        tasks = [client.post("https://api.osv.dev/v1/query", json={
            "package": {
                "name": package_name,
                "ecosystem": ecosystem
            }
        }) for ecosystem in ecosystems]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for response in responses:
            if isinstance(response, Exception):
                raise HTTPException(status_code=500, detail=str(response))
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching data from OSV API")
            data = response.json()
            for vuln in data.get("vulns", []):
                for affected in vuln.get("affected", []):
                    if affected.get("package", {}).get("name") == package_name:
                        unique_versions.update(affected.get("versions", []))
    
    sorted_versions = sorted(unique_versions)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return VulnerablePackageResponse(
        name=package_name,
        versions=sorted_versions,
        timestamp=timestamp
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
