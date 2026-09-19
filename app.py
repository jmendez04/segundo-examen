from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "clave-secreta"


# --- LEER (listado) ---
@app.route("/")
def index():

    conn = get_connection()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cur.execute(
        "SELECT * FROM productos ORDER BY id DESC"
    )

    productos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        productos=productos
    )


# --- CREAR ---
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    if request.method == "POST":

        datos = (
            request.form["codigo"],
            request.form["nombre"],
            request.form["categoria"],
            request.form["precio"],
            request.form["existencia"],
            "activo" in request.form
        )

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO productos
            (codigo, nombre, categoria, precio, existencia, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            datos
        )

        conn.commit()

        cur.close()
        conn.close()

        flash("Producto creado correctamente.")

        return redirect(
            url_for("index")
        )

    return render_template(
        "form.html",
        producto=None
    )


# --- LEER UNO + ACTUALIZAR ---
@app.route(
    "/productos/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar_producto(id):

    conn = get_connection()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    if request.method == "POST":

        datos = (
            request.form["codigo"],
            request.form["nombre"],
            request.form["categoria"],
            request.form["precio"],
            request.form["existencia"],
            "activo" in request.form,
            id
        )

        cur.execute(
            """
            UPDATE productos
            SET codigo=%s,
                nombre=%s,
                categoria=%s,
                precio=%s,
                existencia=%s,
                activo=%s
            WHERE id=%s
            """,
            datos
        )

        conn.commit()

        cur.close()
        conn.close()

        flash("Producto actualizado correctamente.")

        return redirect(
            url_for("index")
        )

    cur.execute(
        "SELECT * FROM productos WHERE id=%s",
        (id,)
    )

    producto = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "form.html",
        producto=producto
    )


# --- ELIMINAR ---
@app.route(
    "/productos/eliminar/<int:id>",
    methods=["POST"]
)
def eliminar_producto(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM productos WHERE id=%s",
        (id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    flash("Producto eliminado.")

    return redirect(
        url_for("index")
    )


if __name__ == "__main__":
    app.run(debug=True)