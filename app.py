from flask import Flask, request, render_template, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.wjzabbdnwmsydegvwrep:FormAutores2025!@aws-0-us-east-2.pooler.supabase.com:5432/postgres?sslmode=require'
db = SQLAlchemy(app)

# Modelo Autor
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(100))
    nombre_autor = db.Column(db.String(100))
    seudonimo = db.Column(db.String(100))
    sexo = db.Column(db.String(20))
    perfil = db.Column(db.String(100))
    rol_obra = db.Column(db.String(100))
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

# Diccionario de opciones para el formulario
opciones = {
    "sexos": ["-Seleccione-","Masculino", "Femenino"],
    "perfiles_institucionales": [
        "Colaborador","Docente","Docente con encargo administrativo", "Estudiante", "Egresado", "Otro"
    ],
    "nacionalidades": [
        "-Seleccione-","Afganistán","Albania"	,"Alemania"	,"Andorra","Angola","Antigua y Barbuda","Arabia Saudita","Argelia","Argentina","Armenia",
        "Australia","Austria","Azerbaiyán","Bahamas","Bangladés","Barbados","Baréin","Bélgica","Belice","Benín","Bielorrusia",
        "Birmania (Myanmar)","Bolivia","Bosnia y Herzegovina","Botsuana","Brasil","Brunéi","Bulgaria","Burkina Faso","Burundi","Bután",
        "Cabo Verde","Camboya","Camerún","Canadá","Catar","Chad","Chile","China","Chipre","Colombia","Comoras","Corea del Norte","Corea del Sur",
        "Costa de Marfil","Costa Rica","Croacia","Cuba","Dinamarca","Dominica","Ecuador","Egipto","El Salvador","Emiratos Árabes Unidos","Eritrea",
        "Eslovaquia","Eslovenia","España","Estados Unidos","Estonia","Eswatini (Suazilandia)","Etiopía","Filipinas","Finlandia","Fiyi","Francia","Gabón",
        "Gambia","Georgia","Ghana","Granada","Grecia","Guatemala","Guinea","Guinea-Bisáu","Guinea Ecuatorial","Guyana","Haití","Honduras","Hungría","India",
        "Indonesia","Irak","Irán","Irlanda","Islandia","Islas Marshall","Islas Salomón","Israel","Italia","Jamaica","Japón",
        "Jordania","Kazajistán","Kenia","Kirguistán","Kiribati","Kuwait","Laos","Lesoto","Letonia","Líbano","Liberia","Libia","Liechtenstein","Lituania",
        "Luxemburgo","Macedonia del Norte","Madagascar","Malasia","Malaui","Maldivas","Malí","Malta","Marruecos","Mauricio","Mauritania","México","Micronesia",
        "Moldavia","Mónaco","Mongolia","Montenegro","Mozambique","Namibia","Nauru","Nepal","Nicaragua","Níger","Nigeria","Noruega","Nueva Zelanda","Omán",
        "Países Bajos","Pakistán","Palaos","Panamá","Papúa Nueva Guinea","Paraguay","Perú","Polonia","Portugal","Reino Unido","República Centroafricana","República Checa",
        "República Democrática del Congo","República del Congo","República Dominicana","Ruanda","Rumanía","Rusia","Samoa","San Cristóbal y Nieves","San Marino",
        "San Vicente y las Granadinas","Santa Lucía","Santo Tomé y Príncipe","Senegal","Serbia","Seychelles","Sierra Leona","Singapur","Siria","Somalia","Sri Lanka",
        "Sudáfrica","Sudán","Sudán del Sur","Suecia","Suiza","Surinam","Tailandia","Tanzania","Tayikistán","Timor Oriental","Togo","Tonga",
        "Trinidad y Tobago","Túnez","Turkmenistán","Turquía","Tuvalu","Ucrania","Uganda","Uruguay","Uzbekistán","Vanuatu","Venezuela","Vietnam","Yemen","Yibuti","Zambia","Zimbabue","Palestina","Ciudad del Vaticano (Santa Sede)"	
    ],
    "niveles_formacion": [
        "-Seleccione-","Técnico", "Tecnólogo", "Pregrado",
        "Especialización", "Maestría", "Doctorado"
    ],
    "es_investigador": ["-Seleccione-","Sí", "No"],
    "rectorias": [
        "-Seleccione-","Rectoría Bogotá", "Rectoría Medellín", "Rectoría Cali",
        "Rectoría Bucaramanga", "Otra"
    ],
    "facultades": [
        "-Seleccione-","Ingeniería", "Ciencias Sociales", "Educación",
        "Ciencias Económicas", "Ciencias de la Salud", "Otra"
    ],
    "rol_obra": [
        "-Seleccione-","Autor","Editor","Compialdor","Prologuista","Traductor"
    ],
    "pais_filiacion":[
        "-Seleccione-","Afganistán","Albania"	,"Alemania"	,"Andorra","Angola","Antigua y Barbuda","Arabia Saudita","Argelia","Argentina","Armenia",
        "Australia","Austria","Azerbaiyán","Bahamas","Bangladés","Barbados","Baréin","Bélgica","Belice","Benín","Bielorrusia",
        "Birmania (Myanmar)","Bolivia","Bosnia y Herzegovina","Botsuana","Brasil","Brunéi","Bulgaria","Burkina Faso","Burundi","Bután",
        "Cabo Verde","Camboya","Camerún","Canadá","Catar","Chad","Chile","China","Chipre","Colombia","Comoras","Corea del Norte","Corea del Sur",
        "Costa de Marfil","Costa Rica","Croacia","Cuba","Dinamarca","Dominica","Ecuador","Egipto","El Salvador","Emiratos Árabes Unidos","Eritrea",
        "Eslovaquia","Eslovenia","España","Estados Unidos","Estonia","Eswatini (Suazilandia)","Etiopía","Filipinas","Finlandia","Fiyi","Francia","Gabón",
        "Gambia","Georgia","Ghana","Granada","Grecia","Guatemala","Guinea","Guinea-Bisáu","Guinea Ecuatorial","Guyana","Haití","Honduras","Hungría","India",
        "Indonesia","Irak","Irán","Irlanda","Islandia","Islas Marshall","Islas Salomón","Israel","Italia","Jamaica","Japón",
        "Jordania","Kazajistán","Kenia","Kirguistán","Kiribati","Kuwait","Laos","Lesoto","Letonia","Líbano","Liberia","Libia","Liechtenstein","Lituania",
        "Luxemburgo","Macedonia del Norte","Madagascar","Malasia","Malaui","Maldivas","Malí","Malta","Marruecos","Mauricio","Mauritania","México","Micronesia",
        "Moldavia","Mónaco","Mongolia","Montenegro","Mozambique","Namibia","Nauru","Nepal","Nicaragua","Níger","Nigeria","Noruega","Nueva Zelanda","Omán",
        "Países Bajos","Pakistán","Palaos","Panamá","Papúa Nueva Guinea","Paraguay","Perú","Polonia","Portugal","Reino Unido","República Centroafricana","República Checa",
        "República Democrática del Congo","República del Congo","República Dominicana","Ruanda","Rumanía","Rusia","Samoa","San Cristóbal y Nieves","San Marino",
        "San Vicente y las Granadinas","Santa Lucía","Santo Tomé y Príncipe","Senegal","Serbia","Seychelles","Sierra Leona","Singapur","Siria","Somalia","Sri Lanka",
        "Sudáfrica","Sudán","Sudán del Sur","Suecia","Suiza","Surinam","Tailandia","Tanzania","Tayikistán","Timor Oriental","Togo","Tonga",
        "Trinidad y Tobago","Túnez","Turkmenistán","Turquía","Tuvalu","Ucrania","Uganda","Uruguay","Uzbekistán","Vanuatu","Venezuela","Vietnam","Yemen","Yibuti","Zambia","Zimbabue","Palestina","Ciudad del Vaticano (Santa Sede)"	
    ]
}

# Crear tabla automáticamente en Render
with app.app_context():
    db.create_all()

# Ruta principal
@app.route("/")
def index():
    return redirect("/registro")

# Registro de autor
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
            rol_obra=datos.get("rol_obra"),
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

    return render_template("registro_autor.html", opciones=opciones)

# Ver autores
@app.route("/autores")
def ver_autores():
    autores = Autor.query.all()
    return render_template("lista_autores.html", autores=autores)

# Descargar Excel
@app.route("/descargar_excel")
def descargar_excel():
    autores = Autor.query.all()

    datos = [{
        "Documento": a.documento,
        "Nombre autor": a.nombre_autor,
        "Pseudónimo": a.seudonimo,
        "Sexo": a.sexo,
        "Perfil": a.perfil,
        "Rol_obra": a.rol_obra,
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
    } for a in autores]

    df = pd.DataFrame(datos)

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
