from flask import Blueprint, render_template, request, redirect, url_for, flash
from .utils import dogecoin_rpc, get_last_blocks

routes = Blueprint('routes', __name__)

@routes.route("/")
def index():
    block = dogecoin_rpc("getbestblockhash")
    last_blocks = get_last_blocks(5)
    return render_template("index.html", last_blocks=last_blocks)

@routes.route("/block/<block_hash>")
def block_details(block_hash):
    block = dogecoin_rpc("getblock", [block_hash])
    return render_template("block.html", block=block)

@routes.route("/transaction/<txid>")
def transaction_details(txid):
    transaction = dogecoin_rpc("getrawtransaction", [txid, True])
    return render_template("transaction.html", tx=transaction)

@routes.route("/search")
def search():
    txid = request.args.get("txid")
    if not txid:
        flash("Please enter a transaction ID.")
        return redirect(url_for("routes.index"))
    
    transaction = dogecoin_rpc("getrawtransaction", [txid, True])
    if transaction:
        return render_template("transaction.html", tx=transaction)
    else:
        flash("Transaction not found.")
        return redirect(url_for("routes.index"))

