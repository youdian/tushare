from sanic import Sanic
from sanic.response import json
import tushare as ts
from policy import hot
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

@app.route("/policy/<name>")
async def policy(request, name):
    l = []
    if name == "hot":
        l = hot.get()
    elif name == "new":
        l = hot.new()
    if l:
        return json(l)
    else:
        return json({})

@app.route("/realtime/<code>")
async def realtime(request, code):
    real = ts.get_realtime_quotes(code)
    if real is None:
        return json({"error": "no realtime data"}, status=500)
    else:
        return json(real.to_json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)