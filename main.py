from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import yfinance as yf
import matplotlib.pyplot as plt
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Stock Price App")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

CHART_PATH = "static/stock_chart.png"

@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "price": None})

@app.post("/", response_class=HTMLResponse)
def form_post(request: Request, symbol: str = Form(...)):
    symbol = symbol.upper()
    stock = yf.Ticker(symbol)
    data = stock.history(period="7d")

    if data.empty:
        price = "Symbol not found"
        return templates.TemplateResponse("index.html", {"request": request, "price": price})

    price = f"${round(data['Close'].iloc[-1], 2)}"

    # Plot trend
    plt.figure(figsize=(6, 3))
    data['Close'].plot(title=f"{symbol} Price Trend (7 days)", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "price": price,
        "symbol": symbol,
        "show_chart": True
    })

@app.get("/test-image")
def test_image():
    return FileResponse("static/stock_chart.png")

