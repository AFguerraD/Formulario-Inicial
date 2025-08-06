from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = "clave_secreta"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.wjzabbdnwmsydegvwrep:FormAutores2025!@aws-0-us-east-2.pooler.supabase.com:5432/postgres?sslmode=require'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# MODELO
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(100))
    nombre_autor = db.Column(db.String(100))
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
    huella_digital = db.Column(db.String(300))
    obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'))
    capitulo_id = db.Column(db.Integer, db.ForeignKey('capitulo.id'))

class Obra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo_tentativo = db.Column(db.String(200))
    origen = db.Column(db.String(100))
    linea_editorial = db.Column(db.String(100))
    tipologia = db.Column(db.String(100))
    area_conocimiento = db.Column(db.String(100))
    thema = db.Column(db.String(100))
    ods = db.Column(db.String(100))
    resumen = db.Column(db.String(60))
    publico_objetivo = db.Column(db.String(200))
    presupuesto = db.Column(db.String(50))
    tipo = db.Column(db.String(50))  # "Obra Completa" o "Capítulo"

 # Relación con autores
    autores = db.relationship('Autor', backref='obra', lazy=True)

class Capitulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo_capitulo = db.Column(db.String(200))
    obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'))

    # Relación con autores
    autores = db.relationship('Autor', backref='capitulo', lazy=True)

# Diccionario de opciones para el formulario
opciones = {
    "sexos": ["-Seleccione-", "Masculino", "Femenino"],
    "perfiles_institucionales": [
        "Colaborador", "Docente", "Docente con encargo administrativo", "Estudiante", "Egresado", "Otro"
    ],
    "nacionalidades": [
        "-Seleccione-", "Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda",
        "Arabia Saudita", "Argelia", "Argentina", "Armenia", "Australia", "Austria", "Azerbaiyán", "Bahamas",
        "Bangladés", "Barbados", "Baréin", "Bélgica", "Belice", "Benín", "Bielorrusia", "Birmania (Myanmar)",
        "Bolivia", "Bosnia y Herzegovina", "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso",
        "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Catar", "Chad", "Chile", "China",
        "Chipre", "Colombia", "Comoras", "Corea del Norte", "Corea del Sur", "Costa de Marfil", "Costa Rica",
        "Croacia", "Cuba", "Dinamarca", "Dominica", "Ecuador", "Egipto", "El Salvador", "Emiratos Árabes Unidos",
        "Eritrea", "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia", "Eswatini (Suazilandia)",
        "Etiopía", "Filipinas", "Finlandia", "Fiyi", "Francia", "Gabón", "Gambia", "Georgia", "Ghana", "Granada",
        "Grecia", "Guatemala", "Guinea", "Guinea-Bisáu", "Guinea Ecuatorial", "Guyana", "Haití", "Honduras",
        "Hungría", "India", "Indonesia", "Irak", "Irán", "Irlanda", "Islandia", "Islas Marshall",
        "Islas Salomón", "Israel", "Italia", "Jamaica", "Japón", "Jordania", "Kazajistán", "Kenia",
        "Kirguistán", "Kiribati", "Kuwait", "Laos", "Lesoto", "Letonia", "Líbano", "Liberia", "Libia",
        "Liechtenstein", "Lituania", "Luxemburgo", "Macedonia del Norte", "Madagascar", "Malasia", "Malaui",
        "Maldivas", "Malí", "Malta", "Marruecos", "Mauricio", "Mauritania", "México", "Micronesia", "Moldavia",
        "Mónaco", "Mongolia", "Montenegro", "Mozambique", "Namibia", "Nauru", "Nepal", "Nicaragua", "Níger",
        "Nigeria", "Noruega", "Nueva Zelanda", "Omán", "Países Bajos", "Pakistán", "Palaos", "Panamá",
        "Papúa Nueva Guinea", "Paraguay", "Perú", "Polonia", "Portugal", "Reino Unido",
        "República Centroafricana", "República Checa", "República Democrática del Congo", "República del Congo",
        "República Dominicana", "Ruanda", "Rumanía", "Rusia", "Samoa", "San Cristóbal y Nieves", "San Marino",
        "San Vicente y las Granadinas", "Santa Lucía", "Santo Tomé y Príncipe", "Senegal", "Serbia", "Seychelles",
        "Sierra Leona", "Singapur", "Siria", "Somalia", "Sri Lanka", "Sudáfrica", "Sudán", "Sudán del Sur",
        "Suecia", "Suiza", "Surinam", "Tailandia", "Tanzania", "Tayikistán", "Timor Oriental", "Togo", "Tonga",
        "Trinidad y Tobago", "Túnez", "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda", "Uruguay",
        "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yibuti", "Zambia", "Zimbabue", "Palestina",
        "Ciudad del Vaticano (Santa Sede)"
    ],
    "niveles_formacion": ["-Seleccione-", "Técnico", "Tecnólogo", "Pregrado", "Especialización", "Maestría", "Doctorado"],
    "es_investigador": ["-Seleccione-", "Sí", "No"],
    "rectorias": [
        "-Seleccione-", "Antioquia - Chocó", "Bogotá Cundinamarca - Boyacá", "Caribe", "Centro Occidente", "Centro Sur",
        "Oriente", "Parque Científico de Innovación Social (PCIS)", "UNIMINUTO Virtual"
    ],
    "facultades": [
        "-Seleccione-", "Ingeniería", "Ciencias Sociales", "Educación",
        "Ciencias Económicas", "Ciencias de la Salud", "Otra"
    ],
    "rol_obra": ["-Seleccione-", "Autor", "Editor", "Compilador", "Prologuista", "Traductor"],

    "pais_filiacion": ["-Seleccione-", "Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda",
        "Arabia Saudita", "Argelia", "Argentina", "Armenia", "Australia", "Austria", "Azerbaiyán", "Bahamas",
        "Bangladés", "Barbados", "Baréin", "Bélgica", "Belice", "Benín", "Bielorrusia", "Birmania (Myanmar)",
        "Bolivia", "Bosnia y Herzegovina", "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso",
        "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Catar", "Chad", "Chile", "China",
        "Chipre", "Colombia", "Comoras", "Corea del Norte", "Corea del Sur", "Costa de Marfil", "Costa Rica",
        "Croacia", "Cuba", "Dinamarca", "Dominica", "Ecuador", "Egipto", "El Salvador", "Emiratos Árabes Unidos",
        "Eritrea", "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia", "Eswatini (Suazilandia)",
        "Etiopía", "Filipinas", "Finlandia", "Fiyi", "Francia", "Gabón", "Gambia", "Georgia", "Ghana", "Granada",
        "Grecia", "Guatemala", "Guinea", "Guinea-Bisáu", "Guinea Ecuatorial", "Guyana", "Haití", "Honduras",
        "Hungría", "India", "Indonesia", "Irak", "Irán", "Irlanda", "Islandia", "Islas Marshall",
        "Islas Salomón", "Israel", "Italia", "Jamaica", "Japón", "Jordania", "Kazajistán", "Kenia",
        "Kirguistán", "Kiribati", "Kuwait", "Laos", "Lesoto", "Letonia", "Líbano", "Liberia", "Libia",
        "Liechtenstein", "Lituania", "Luxemburgo", "Macedonia del Norte", "Madagascar", "Malasia", "Malaui",
        "Maldivas", "Malí", "Malta", "Marruecos", "Mauricio", "Mauritania", "México", "Micronesia", "Moldavia",
        "Mónaco", "Mongolia", "Montenegro", "Mozambique", "Namibia", "Nauru", "Nepal", "Nicaragua", "Níger",
        "Nigeria", "Noruega", "Nueva Zelanda", "Omán", "Países Bajos", "Pakistán", "Palaos", "Panamá",
        "Papúa Nueva Guinea", "Paraguay", "Perú", "Polonia", "Portugal", "Reino Unido",
        "República Centroafricana", "República Checa", "República Democrática del Congo", "República del Congo",
        "República Dominicana", "Ruanda", "Rumanía", "Rusia", "Samoa", "San Cristóbal y Nieves", "San Marino",
        "San Vicente y las Granadinas", "Santa Lucía", "Santo Tomé y Príncipe", "Senegal", "Serbia", "Seychelles",
        "Sierra Leona", "Singapur", "Siria", "Somalia", "Sri Lanka", "Sudáfrica", "Sudán", "Sudán del Sur",
        "Suecia", "Suiza", "Surinam", "Tailandia", "Tanzania", "Tayikistán", "Timor Oriental", "Togo", "Tonga",
        "Trinidad y Tobago", "Túnez", "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda", "Uruguay",
        "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yibuti", "Zambia", "Zimbabue", "Palestina",
        "Ciudad del Vaticano (Santa Sede)"],
    "centros_por_rectoria": {
        "Antioquia - Chocó": 
        ["Apartadó","Bello","Centro  de Atención Tutorial Caucasia","Centro de Atención Tutorial El Bagre","Centro de Atención Tutorial Quibdó",
        "Centro de Atención Tutorial Rionegro","Centro de Atención Tutorial Zaragoza","Itagüí","Urabá"],

        "Bogotá Cundinamarca - Boyacá": 
        ["Kennedy","Las Cruces - Santa Fe""Minuto de Dios - Engativá","Perdomo - Ciudad Bolívar""San Cristóbal Norte - Usaquén","Centro de Atención Tutorial Facatativá",
        "Centro de Atención Tutorial Funza","Centro de Atención Tutorial Fusagasugá","Centro de Atención Tutorial La Mesa","Centro de Atención Tutorial Ubaté","Centro de Atención Tutorial Villeta",
        "Chiquinquirá","Duitama","Girardot","Madrid","Soacha","Zipaquirá"],

        "Caribe": 
        ["Barranquilla","Cartagena","Centro de Atención Tutorial Magangué","Santa Marta"],

        "Centro Occidente": 
        ["Buenaventura","Buga","Cali","Centro de Atención Tutorial Armenia","Centro de Atención Tutorial Cartago","Centro de Atención Tutorial Ipiales",
        "Centro de Atención Tutorial Miranda","Chinchiná","Pasto","Pereira"],

        "Centro Sur": ["Florencia","Garzón","Ibagué","La Dorada","Lérida","Mocoa","Neiva","Pitalito"],

        "Oriente": ["Barrancabermeja","Bucaramanga","Centro de Atención Tutorial Orocué","Centro de Atención Tutorial Puerto Carreño",
        "Cúcuta","Inírida","Mitú","Ocaña","Tibú","Villavicencio","Yopal"],

        "Parque Científico de Innovación Social (PCIS)": [],
        
        "UNIMINUTO Virtual": ["Virtual"]
    }
}

# Crear tabla automáticamente
with app.app_context():
    db.create_all()

# Rutas
@app.route("/")
def index():
    return redirect("/tipo_obra")


@app.route("/tipo_obra", methods=["GET", "POST"])
def tipo_obra():
    if request.method == "POST":
        tipo = request.form.get("tipo")
        session['autores'] = []
        session['tipo_obra'] = tipo

        if tipo == "obra_capitulo":
            return redirect("/obra_info")
        elif tipo == "obra_completa":
            return redirect("/registro")
        else:
            return redirect("/tipo_obra")
    return render_template("tipo_obra.html")


@app.route("/registro", methods=["GET", "POST"])
def registro_autor():
    if request.method == "POST":
        datos = request.form
        nuevo_autor = Autor(
            documento=datos.get("documento"),
            nombre_autor=datos.get("nombre_autor"),
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
            programa=datos.get("programa"),
            huella_digital=datos.get("huella_digital")
        )
        db.session.add(nuevo_autor)
        db.session.commit()

        autor_guardado = {
            "nombre_autor": nuevo_autor.nombre_autor,
            "rol_obra": nuevo_autor.rol_obra
        }
        session['autores'].append(autor_guardado)
        session.modified = True

        if 'registrar_otro' in request.form:
            return redirect("/registro")
        elif 'siguiente' in request.form:
            return redirect("/obra_info")

    return render_template("registro_autor.html", opciones=opciones)

@app.route('/registro-capitulo/<int:obra_id>', methods=['GET', 'POST'])
def registro_capitulo(obra_id):
    if request.method == 'POST':
        titulo_capitulo = request.form['titulo_capitulo']
        
        nuevo_capitulo = Capitulo(
            titulo_capitulo=titulo_capitulo,
            obra_id=obra_id
        )
        db.session.add(nuevo_capitulo)
        db.session.commit()

        # Redirige al formulario de autores para ese capítulo
        return redirect(url_for('registro_autor_capitulo', capitulo_id=nuevo_capitulo.id))
    
    return render_template('registro_capitulo.html', obra_id=obra_id)



@app.route("/obra_info", methods=["GET", "POST"])
def obra_info():
    if request.method == "POST":
        datos = request.form
        tipo = session.get("tipo_obra")

        nueva_obra = Obra(
            titulo_tentativo=datos.get("titulo_tentativo"),
            origen=datos.get("origen"),
            linea_editorial=datos.get("linea_editorial"),
            tipologia=datos.get("tipologia"),
            area_conocimiento=datos.get("area_conocimiento"),
            thema=datos.get("thema"),
            ods=datos.get("ods"),
            resumen=datos.get("resumen"),
            publico_objetivo=datos.get("publico_objetivo"),
            presupuesto=datos.get("presupuesto"),
            tipo=tipo
        )
        db.session.add(nueva_obra)
        db.session.commit()

        # Asociar autores a la obra
        autores = Autor.query.order_by(Autor.id.desc()).limit(len(session.get("autores", []))).all()
        for autor in autores:
            autor.obra_id = nueva_obra.id

        db.session.commit()

        if tipo == "obra_capitulo":
            return redirect(url_for('registro_capitulo', obra_id=nueva_obra.id))
        else:
            return redirect("/confirmacion")
    return render_template("obra_info.html", autores=session.get("autores", []))

@app.route("/confirmacion")
def confirmacion():
    tipo = session.get("tipo_obra")
    autores = session.get("autores", []) + session.get("autores_capitulo", [])
    return render_template("confirmacion.html", tipo=tipo, autores=autores)

@app.route('/registro-autor-capitulo/<int:capitulo_id>', methods=['GET', 'POST'])
def registro_autor_capitulo(capitulo_id):
    if request.method == "POST":
        datos = request.form

        nuevo_autor = Autor(
            documento=datos.get("documento"),
            nombre_autor=datos.get("nombre_autor"),
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
            programa=datos.get("programa"),
            huella_digital=datos.get("huella_digital"),
            capitulo_id=capitulo_id
        )
        db.session.add(nuevo_autor)
        db.session.commit()

        autor_guardado = {
            "nombre_autor": nuevo_autor.nombre_autor,
            "rol_obra": nuevo_autor.rol_obra
        }
        session.setdefault('autores_capitulo', []).append(autor_guardado)
        session.modified = True

        if 'registrar_otro' in request.form:
            return redirect(url_for('registro_autor_capitulo', capitulo_id=capitulo_id))
        elif 'finalizar' in request.form:
            capitulo = Capitulo.query.get_or_404(capitulo_id)
            return redirect(url_for('capitulo_confirmacion', obra_id=capitulo.obra_id))

    return render_template("registro_autor_capitulo.html", opciones=opciones)

@app.route('/capitulo_confirmacion/<int:obra_id>', methods=['GET', 'POST'])
def capitulo_confirmacion(obra_id):
    if request.method == "POST":
        accion = request.form.get("accion")
        if accion == "agregar":
            return redirect(url_for('registro_capitulo', obra_id=obra_id))
        else:
            return redirect("/confirmacion")
    return render_template("capitulo_confirmacion.html", obra_id=obra_id)

@app.route("/confirmacion-capitulo")
def confirmacion_capitulo():
    return render_template("capitulo_confirmacion.html")

@app.route("/descargar_excel")
def descargar_excel():
    autores = Autor.query.outerjoin(Obra).outerjoin(Capitulo).all()  # outerjoin para que no falle si falta alguno

    datos = []
    for a in autores:
        datos.append({
            "Documento": a.documento,
            "Nombre del autor": a.nombre_autor,
            "Rol en la obra": a.rol_obra,
            "Correo": a.correo,
            "Programa": a.programa,
            "Huella Digital": a.huella_digital,
            "Título Tentativo": a.obra.titulo_tentativo if a.obra else "",
            "Origen de la obra": a.obra.origen if a.obra else "",
            "Línea editorial": a.obra.linea_editorial if a.obra else "",
            "Tipología": a.obra.tipologia if a.obra else "",
            "Área de conocimiento": a.obra.area_conocimiento if a.obra else "",
            "Thema": a.obra.thema if a.obra else "",
            "ODS al que aporta": a.obra.ods if a.obra else "",
            "Resumen": a.obra.resumen if a.obra else "",
            "Público objetivo": a.obra.publico_objetivo if a.obra else "",
            "Presupuesto": a.obra.presupuesto if a.obra else "",
            "Tipo de obra": a.obra.tipo if a.obra else "",
            "Título del capítulo": a.capitulo.titulo_capitulo if a.capitulo else ""
        })

    df = pd.DataFrame(datos)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Autores y Obras")

    output.seek(0)
    return send_file(
        output,
        download_name="Autores_y_Obras.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == "__main__":
    app.run(debug=True)