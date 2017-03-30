from sanic import Sanic
from sanic.response import json
import tushare as ts
app = Sanic()

@app.middleware('response')
async def access_control(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"

@app.route("/")
async def test(request):
    return json({"hello": "world"})


@app.route("/history/<code>")
async def history(request, code):
    his = ts.get_k_data(code)
    if his is None:
        return json({"error": "stock not found"}, status=404)
    else:
        return json(his.to_json(orient='split'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)