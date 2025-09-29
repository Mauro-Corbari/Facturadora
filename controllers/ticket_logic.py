from flask import render_template, redirect, url_for, Blueprint, request, session
from datetime import datetime, date
from config import db
from models.ticket_model import Ticket
from models.kyaku_model import Okyaku
from models.product_model import Product
from models.detail_model import Detail

ticket_bp = Blueprint("ticket", __name__)

@ticket_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.auth"))

@ticket_bp.route("/ticket/new", methods=["GET", "POST"])
def create_ticket_page():
    clients = Okyaku.query.all()
    products = Product.query.all()

    if request.method == "POST":
        data = request.form
        client_id = int(data["cliente_id"])

        ticket = Ticket(date=date.today(), total=0, kyakuID=client_id)
        db.session.add(ticket)
        db.session.flush()

        total = 0
        prod_ids = data.getlist("prodID[]")
        quantities = data.getlist("quant[]")

        for pid, qty in zip(prod_ids, quantities):
            if not pid or not qty:
                continue

            product = Product.query.get(int(pid))
            quantity = int(qty)
            subtotal = product.price * quantity
            total += subtotal

            product.stock -= quantity

            detail = Detail(
                prodID=product.id,
                ticketID=ticket.ticketID,
                quant=quantity,
                unit_price=product.price,
                subtotal=subtotal
            )
            db.session.add(detail)

        ticket.total = total
        db.session.commit()

        return redirect(url_for("ticket.ticket_list"))

    return render_template("new_ticket.html", clientes=clients, productos=products)

@ticket_bp.route("/ticket", methods=["GET"])
def ticket_list():
    tickets = Ticket.query.all()
    clients = Okyaku.query.all()
    products = Product.query.all()
    return render_template(
        "ticket.html",
        tickets=[
            {
                "ticketID": t.ticketID,
                "date": t.date.strftime("%Y-%m-%d"),
                "total": t.total,
                "cliente": t.cliente.namae if t.cliente else "Desconocido"
            }
            for t in tickets
        ],
        clientes=clients,
        productos=products
    )

@ticket_bp.route("/ticket/details", methods=["GET"])
def ticket_details():
    ticket_id = request.args.get("id", type=int)
    tickets = Ticket.query.all()

    if ticket_id:
        ticket = Ticket.query.get_or_404(ticket_id)
    else:
        ticket = tickets[0] if tickets else None

    return render_template(
        "ticket_details.html",
        factura=ticket,
        tickets=tickets
    )

@ticket_bp.route("/ticket/update/<int:id>", methods=["POST"])
def ticket_update(id):
    ticket = Ticket.query.get_or_404(id)
    data = request.form
    ticket.total = float(data["total"])
    ticket.kyakuID = int(data["cliente_id"])
    db.session.commit()
    return redirect(url_for("ticket.ticket_list"))

@ticket_bp.route("/ticket/delete/<int:id>", methods=["POST"])
def ticket_delete(id):
    ticket = Ticket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for("ticket.ticket_list"))
