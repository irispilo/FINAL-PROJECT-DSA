from flask import Flask, render_template, request, redirect, url_for, flash
from priority_queue import MaxPriorityQueue, Order

app = Flask(__name__)
app.secret_key = "pizzeria-secret"

pq = MaxPriorityQueue()
history = []
order_counter = 1


def next_id():
    global order_counter
    oid = f"ORD-{order_counter:03d}"
    order_counter += 1
    return oid


# ── seed data ─────────────────────────────────────────────────────────────────
for data in [
    ("Mario López", "Margherita, Coca-Cola", "mesa"),
    ("Ana García", "Pepperoni x2", "express"),
    ("Luis Torres", "Hawaiana, Agua", "para_llevar"),
]:
    pq.insert(Order(next_id(), data[0], data[1], data[2]))


# ── routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    orders = [o.to_dict() for o in pq.get_all()]
    next_order = pq.peek()
    return render_template(
        "index.html",
        orders=orders,
        next_order=next_order.to_dict() if next_order else None,
        history=list(reversed(history)),
        size=pq.size(),
    )


@app.route("/add", methods=["POST"])
def add_order():
    customer = request.form.get("customer", "").strip()
    items = request.form.get("items", "").strip()
    order_type = request.form.get("order_type", "mesa")
    if not customer or not items:
        flash("Completa cliente e ítems.", "error")
        return redirect(url_for("index"))
    order = Order(next_id(), customer, items, order_type)
    pq.insert(order)
    flash(f"{order.order_id} agregada con prioridad {order.priority}.", "success")
    return redirect(url_for("index"))


@app.route("/dispatch", methods=["POST"])
def dispatch():
    try:
        order = pq.extract_max()
        history.append(order.to_dict())
        flash(f"Despachada: {order.order_id} — {order.customer}.", "success")
    except IndexError:
        flash("No hay órdenes en cola.", "error")
    return redirect(url_for("index"))


@app.route("/update_priority", methods=["POST"])
def update_priority():
    order_id = request.form.get("order_id", "").strip()
    try:
        new_priority = int(request.form.get("priority", 0))
        pq.update_priority(order_id, new_priority)
        flash(f"Prioridad de {order_id} actualizada a {new_priority}.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/cancel", methods=["POST"])
def cancel_order():
    order_id = request.form.get("order_id", "").strip()
    try:
        order = pq.delete(order_id)
        flash(f"Cancelada: {order.order_id} — {order.customer}.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/wait", methods=["POST"])
def add_wait():
    try:
        minutes = int(request.form.get("minutes", 5))
        pq.add_wait_time(minutes)
        flash(f"+{minutes} min aplicados a todas las órdenes.", "success")
    except ValueError:
        flash("Ingresa minutos válidos.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
