import json
from typing import *
from src import fetch
from bs4 import BeautifulSoup

"""
q:str = `python`
n:str = `not in title`
t:str = `in title`
c:str = `Company`
l: str = `Location`
radius:int = 100
r:str = `The number of results to return per page. Default: 10.`
---
div container.stdContentLayout
div card .snippetPadding".
h3 postion .itemTitle
a     href
span company .colorCompany
span location .colorLocation
spann description .jdSnippet
span 	date 	.colorDate
"""

BASE_URL = "https://www.postjobfree.com/jobs?q="

async def search_job(
    q: str,
    n: Optional[str] = None,
    t: Optional[str] = None,
    c: Optional[str] = None,
    l: Optional[str] = None,
    radius: Optional[int] = 100,
    r: Optional[int] = 10,
) -> List[Dict[str, str]]:
    url = f"{BASE_URL}{q}&l={l}&radius={radius}&r={r}"
    print(url)
    html = await fetch(
        "GET",
        url,
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        },
    )
    if isinstance(html, bytes):
        html = html.decode("utf-8")
    elif isinstance(html, dict):
        html = json.dumps(html)
    soup = BeautifulSoup(html, "lxml")
    jobs = soup.find_all("div", {"class": "snippetPadding"})
    results = []
    for job in jobs:
        title = job.find("h3", {"class": "itemTitle"})
        company = job.find("span", {"class": "colorCompany"})
        location = job.find("span", {"class": "colorLocation"})
        description = job.find("span", {"class": "jdSnippet"})
        date = job.find("span", {"class": "colorDate"})
        results.append(
            {
                "title": title.text,
                "company": company.text,
                "location": location.text,
                "description": description.text,
                "date": date.text,
            }
        )
    return results

"""
---
"""

from fastapi import APIRouter, Depends, HTTPException, status


app = APIRouter(prefix="/jobs", tags=["Jobs"])

@app.get("/search")
async def search_job(
    q: str,
    n: Optional[str] = None,
    t: Optional[str] = None,
    c: Optional[str] = None,
    l: Optional[str] = None,
    radius: Optional[int] = None,
    r: Optional[int] = None,
):
    return await search_job(
        q=q,
        n=n,
        t=t,
        c=c,
        l=l,
        radius=radius,
        r=r,
    )