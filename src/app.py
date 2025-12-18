import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv

from api.models import db, User, Cliente, TarifaCliente, Albaran
from docxtpl import DocxTemplate
import tempfile
import subprocess


# ─────────────────────────────────────────────
# Configuración inicial
# ─────────────────────────────────────────────
load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///daeend.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret")

db.init_app(app)
Migrate(app, db)
JWTManager(app)
Bcrypt(app)
CORS(app)



def generar_pdf_albaran(albaran):
    """
    Genera el PDF del albarán y devuelve la ruta al archivo
    """


    context = {
        "nombre_empresa": albaran.cliente.nombre_empresa,
        "persona_contacto": albaran.persona_contacto or "",
        "lugar_de_ensayo": albaran.lugar_de_ensayo or "",
        "fecha": albaran.fecha.strftime("%d/%m/%Y"),
        "hora_inicio": albaran.hora_inicio.strftime("%H:%M") if albaran.hora_inicio else None,
        "hora_fin": albaran.hora_fin.strftime("%H:%M") if albaran.hora_fin else None,

        "linea_trabajo_1": albaran.linea_trabajo_1,
        "linea_trabajo_2": albaran.linea_trabajo_2,
        "linea_trabajo_3": albaran.linea_trabajo_3,

        "descripcion_linea_1": albaran.descripcion_linea_1,
        "descripcion_linea_2": albaran.descripcion_linea_2,
        "descripcion_linea_3": albaran.descripcion_linea_3,
        "descripcion_linea_4": albaran.descripcion_linea_4,

        "total_general": f"{albaran.total_general:.2f} €",
    }

    template_path = os.path.join(
        os.path.dirname(__file__),
        "templates",
        "ALBARAN_BASE_daeEND_rev2.docx"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        docx_path = os.path.join(tmpdir, f"albaran_{albaran.id}.docx")

        doc = DocxTemplate(template_path)
        doc.render(context)
        doc.save(docx_path)

        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                docx_path,
                "--outdir",
                tmpdir,
            ],
            check=True
        )

        pdf_path = docx_path.replace(".docx", ".pdf")
        return pdf_path


# ─────────────────────────────────────────────
# ENDPOINT PREVIEW
# ─────────────────────────────────────────────

@app.route("/api/albaranes/<int:albaran_id>/pdf/preview", methods=["GET"])
@jwt_required()
def preview_albaran_pdf(albaran_id):
    albaran = Albaran.query.get(albaran_id)
    if not albaran:
        return jsonify({"error": "Albarán no encontrado"}), 404

    pdf_path = generar_pdf_albaran(albaran)

    return send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=False,  # 👈 PREVIEW
        download_name=f"albaran_{albaran.id}.pdf"
    )



# ─────────────────────────────────────────────
# ENDPOINT DESCARGA DIRECTA
# ─────────────────────────────────────────────

@app.route("/api/albaranes/<int:albaran_id>/pdf/download", methods=["GET"])
@jwt_required()
def download_albaran_pdf(albaran_id):
    albaran = Albaran.query.get(albaran_id)
    if not albaran:
        return jsonify({"error": "Albarán no encontrado"}), 404

    pdf_path = generar_pdf_albaran(albaran)

    return send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=True,  # 👈 DESCARGA DIRECTA
        download_name=f"albaran_{albaran.id}.pdf"
    )








# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not all([email, password, name]):
        return jsonify({"error": "Datos incompletos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Usuario ya existe"}), 400

    bcrypt = Bcrypt()
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        email=email,
        name=name,
        password_hash=password_hash,
        is_admin=False
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuario creado"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    bcrypt = Bcrypt()
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = create_access_token(identity=user.id)

    return jsonify({
        "token": token,
        "user": user.serialize()
    }), 200


@app.route("/api/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    return jsonify(user.serialize()), 200


# ─────────────────────────────────────────────
# CLIENTES
# ─────────────────────────────────────────────

@app.route("/api/clientes", methods=["GET"])
@jwt_required()
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.serialize() for c in clientes]), 200


@app.route("/api/clientes", methods=["POST"])
@jwt_required()
def create_cliente():
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()
    nombre = data.get("nombre_empresa")

    cliente = Cliente(nombre_empresa=nombre)
    db.session.add(cliente)
    db.session.commit()

    return jsonify(cliente.serialize()), 201


# ─────────────────────────────────────────────
# TARIFAS (SOLO ADMIN)
# ─────────────────────────────────────────────

@app.route("/api/tarifas", methods=["POST"])
@jwt_required()
def create_tarifa():
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()

    tarifa = TarifaCliente(
        cliente_id=data["cliente_id"],
        ensayo=data["ensayo"],
        modalidad=data["modalidad"],  # horas | jornada
        precio_tecnico=data["precio_tecnico"],
        precio_ayudante=data["precio_ayudante"],
        horas_minimas=data.get("horas_minimas", 1)
    )

    db.session.add(tarifa)
    db.session.commit()

    return jsonify({"msg": "Tarifa creada"}), 201


# ─────────────────────────────────────────────
# ALBARANES (CORE)
# ─────────────────────────────────────────────

@app.route("/api/albaranes", methods=["POST"])
@jwt_required()
def create_albaran():
    user_id = get_jwt_identity()
    data = request.get_json()

    cliente = Cliente.query.get(data["cliente_id"])
    tarifa = TarifaCliente.query.filter_by(
        cliente_id=cliente.id,
        ensayo=data["ensayo"],
        modalidad=data["modalidad"],
        activa=True
    ).first()

    if not tarifa:
        return jsonify({"error": "Tarifa no encontrada"}), 400

    total_general = 0
    lineas = []

    # ─── Técnicos ───
    if data.get("num_tecnicos", 0) > 0:
        if tarifa.modalidad == "horas":
            horas = max(data["horas"], tarifa.horas_minimas)
            total = data["num_tecnicos"] * horas * tarifa.precio_tecnico
            texto = (
                f"{data['num_tecnicos']} x Técnico de {tarifa.ensayo} "
                f"x {horas} h = {total} €"
            )
        else:
            total = data["num_tecnicos"] * tarifa.precio_tecnico
            texto = (
                f"{data['num_tecnicos']} x Jornada x Técnico de "
                f"{tarifa.ensayo} = {total} €"
            )
        total_general += total
        lineas.append(texto)

    # ─── Ayudantes ───
    if data.get("num_ayudantes", 0) > 0:
        if tarifa.modalidad == "horas":
            horas = max(data["horas"], tarifa.horas_minimas)
            total = data["num_ayudantes"] * horas * tarifa.precio_ayudante
            texto = (
                f"{data['num_ayudantes']} x Ayudante de {tarifa.ensayo} "
                f"x {horas} h = {total} €"
            )
        else:
            total = data["num_ayudantes"] * tarifa.precio_ayudante
            texto = (
                f"{data['num_ayudantes']} x Jornada x Ayudante de "
                f"{tarifa.ensayo} = {total} €"
            )
        total_general += total
        lineas.append(texto)

    # ─── Fungibles (opcional) ───
    if data.get("fungibles"):
        total = data["fungibles"]["total"]
        texto = f"{data['fungibles']['cantidad']} Fungibles x {data['fungibles']['tipo']} = {total} €"
        total_general += total
        lineas.append(texto)

    albaran = Albaran(
        cliente_id=cliente.id,
        usuario_id=user_id,
        fecha=datetime.strptime(data["fecha"], "%Y-%m-%d").date(),
        hora_inicio=data.get("hora_inicio"),
        hora_fin=data.get("hora_fin"),
        lugar_de_ensayo=data.get("lugar_de_ensayo"),
        persona_contacto=data.get("persona_contacto"),
        linea_trabajo_1=lineas[0],
        linea_trabajo_2=lineas[1] if len(lineas) > 1 else None,
        linea_trabajo_3=lineas[2] if len(lineas) > 2 else None,
        total_general=total_general
    )

    db.session.add(albaran)
    db.session.commit()

    return jsonify({
        "msg": "Albarán creado",
        "total": total_general
    }), 201


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
