from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
import pandas as pd
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autores.db'
db = SQLAlchemy(app)

# Definición del modelo Autor
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(100))
    nombre_autor = db.Column(db.String(100))
    seudonimo = db.Column(db.String(100))
    sexo = db.Column(db.String(20))
    perfil = db.Column(db.String(100))
    nacionalidad = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    nivel_formacion = db.Column(db.String(100))
    filiacion = db.Column(db.String(100))
    pais_filiacion = db.Column(db.String(100))
    es_investigador = db.Column(db.String(20))
    rectoria = db.Column(db.String(100))
    centro_universitario = db.Column(db.String(100))
    facultad = db.Column(db.String(100))
    programa = db.Column(db.String(100))

@app.route("/registro", methods=["GET", "POST"])
def registro_autor():
    if request.method == "POST":
        datos = request.form

        nuevo_autor = Autor(
            documento=datos.get("documento"),
            nombre_autor=datos.get("nombre_autor"),
            seudonimo=datos.get("seudonimo"),
            sexo=datos.get("sexo"),
            perfil=datos.get("perfil"),
            nacionalidad=datos.get("nacionalidad"),
            correo=datos.get("correo"),
            nivel_formacion=datos.get("nivel_formacion"),
            filiacion=datos.get("filiacion"),
            pais_filiacion=datos.get("pais_filiacion"),
            es_investigador=datos.get("es_investigador"),
            rectoria=datos.get("rectoria"),
            centro_universitario=datos.get("centro_universitario"),
            facultad=datos.get("facultad"),
            programa=datos.get("programa")
        )

        db.session.add(nuevo_autor)
        db.session.commit()

        return "Formulario enviado y guardado en la base de datos ✅"

    return render_template("registro_autor.html")

@app.route("/autores")
def ver_autores():
    autores = Autor.query.all()
    return render_template("lista_autores.html", autores=autores)

@app.route("/descargar_excel")
def descargar_excel():
    autores = Autor.query.all()

    # Convertir a lista de diccionarios
    datos = []
    for a in autores:
        datos.append({
            "Documento": a.documento,
            "Nombre autor": a.nombre_autor,
            "Pseudónimo": a.seudonimo,
            "Sexo": a.sexo,
            "Perfil": a.perfil,
            "Nacionalidad": a.nacionalidad,
            "Correo": a.correo,
            "Nivel de formación": a.nivel_formacion,
            "Filiación": a.filiacion,
            "País filiación": a.pais_filiacion,
            "¿Es investigador?": a.es_investigador,
            "Rectoría": a.rectoria,
            "Centro universitario": a.centro_universitario,
            "Facultad": a.facultad,
            "Programa académico": a.programa
        })

    df = pd.DataFrame(datos)

    # Guardar en memoria y enviar como descarga
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Autores")

    output.seek(0)

    return send_file(output,
                     download_name="Autores_Registrados.xlsx",
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app.run(debug=True)