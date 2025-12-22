from dotenv import load_dotenv

load_dotenv()

from my_trading_prj.graph import app

if __name__ == "__main__":
    print("Hello Advanced RAG")
    print(app.invoke(input={"coin": "BTC-USD","timeframe":1}))