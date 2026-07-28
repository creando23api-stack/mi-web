from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inicio():
    mensaje_confirmacion = None
    datos_recibidos = None

    if request.method == "POST":
        # Capturamos toda la información principal del cliente desde el formulario
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")
        empresa = request.form.get("empresa")
        notas = request.form.get("notas")

        # Estructuramos los datos
        datos_recibidos = {
            "nombre": nombre,
            "correo": correo,
            "telefono": telefono,
            "empresa": empresa,
            "notas": notas
        }
        
        mensaje_confirmacion = f"¡Cliente '{nombre}' registrado con éxito en el sistema!"

    return render_template("index.html", mensaje=mensaje_confirmacion, cliente=datos_recibidos)

if __name__ == "__main__":
    app.run(debug=True)
