from flask import Flask, request, redirect, session, render_template_string
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

DOSYA = "data.json"

ARACLAR = ["TIR1","TIR2","TIR3","TIR4","KAMYONET1","KAMYONET2"]

def load():
    try:
        with open(DOSYA) as f:
            return json.load(f)
    except:
        return []

def save(data):
    with open(DOSYA,"w") as f:
        json.dump(data,f)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["u"] == "admin" and request.form["p"] == "1234":
            session["ok"] = True
            return redirect("/panel")

    return """
    <h2>Giriş</h2>
    <form method="post">
    <input name="u" placeholder="kullanıcı">
    <input name="p" type="password" placeholder="şifre">
    <button>Giriş</button>
    </form>
    """

@app.route("/panel")
def panel():
    if not session.get("ok"):
        return redirect("/")

    data = load()

    arac = {a:0 for a in ARACLAR}

    for d in data:
        if d["tur"]=="gelir":
            arac[d["arac"]] += d["miktar"]
        else:
            arac[d["arac"]] -= d["miktar"]

    return render_template_string("""
    <h2>🚚 Panel</h2>

    <form method="post" action="/add">
    <select name="tur">
    <option value="gelir">Gelir</option>
    <option value="gider">Gider</option>
    </select>

    <select name="arac">
    {% for a in araclar %}
    <option>{{a}}</option>
    {% endfor %}
    </select>

    <input name="miktar" placeholder="miktar">
    <button>Ekle</button>
    </form>

    <h3>Durum</h3>
    {% for a,v in arac.items() %}
    {{a}} : {{v}} <br>
    {% endfor %}
    """, arac=arac, araclar=ARACLAR)

@app.route("/add", methods=["POST"])
def add():
    data = load()

    data.append({
        "tur": request.form["tur"],
        "arac": request.form["arac"],
        "miktar": float(request.form["miktar"]),
        "tarih": datetime.now().strftime("%Y-%m-%d")
    })

    save(data)
    return redirect("/panel")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
