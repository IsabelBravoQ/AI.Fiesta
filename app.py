from flask import request, Flask, jsonify,json
from funciones import bbdd, llm
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['DEBUG'] = True

@app.route("/", methods = ['GET'])
def main():
    return "API de AI.Fiesta, tu organizador de fiestas online"

@app.route("/fiestas", methods = ["POST"])

def fiestas ():
    data = request.get_json(force=True) or {}
    
    required = ["p_tema", "edad_invitados", "numero_invitados", "presupuesto", "lugar"]
    missing = [i for i in required if i not in data]
    if missing:
        return jsonify({"error":"faltan campos"}),400
    
    try:
        p_tema = str(data["p_tema"]).strip()
        edad_invitados = str(data["edad_invitados"]).strip()
        numero_invitados = int(data["numero_invitados"])
        presupuesto = str(data["presupuesto"]).strip()
        lugar = str(data["lugar"]).strip()
    
        fiesta = llm(p_tema, edad_invitados, numero_invitados, presupuesto, lugar)
        if isinstance(fiesta, str):
            fiesta = json.loads(fiesta)

        r_tema       = fiesta.get("tema", p_tema)
        r_musica     = fiesta.get("música", []) or []
        r_decoracion = fiesta.get("decoración", []) or []
        r_juegos     = fiesta.get("juegos", []) or []
        r_comida     = fiesta.get("comida", []) or []
        r_bebidas    = fiesta.get("bebidas", []) or []

        resultado = bbdd(p_tema, edad_invitados, numero_invitados, presupuesto, lugar,
            r_tema, r_musica, r_decoracion, r_juegos, r_comida, r_bebidas)
    

        if resultado == "ok":
    
            return jsonify({
            "input": {
                "p_tema": p_tema,
                "edad_invitados": edad_invitados,
                "numero_invitados": numero_invitados,
                "presupuesto": presupuesto,
                "lugar": lugar
            },
            "fiesta": fiesta
        }), 200
    
    except Exception as e:
        app.logger.exception("Error en /fiestas")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()