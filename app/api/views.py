from flask import Blueprint, redirect, request

from ..models import Lnaddr, Nip

api = Blueprint("api", __name__)

@api.route("/.well-known/nostr.json", methods=["GET"])
def nostr():
    args = request.args
    nostr_json = {}
    nostr_json["names"] = {}
    if "name" in args:
        nip = Nip.query.filter_by(username=args["name"]).first()
        nostr_json["names"][nip.username] = nip.hex
    else:
        nips = Nip.query.all()
        for nip in nips:
            nostr_json["names"][nip.username] = nip.hex
    return nostr_json

@api.route("/.well-known/lnurlp/<string:username>", methods=["GET"])
def lnurlp(username):
    lnaddr = Lnaddr.query.filter_by(username=username).first()
    lnurl_out = lnaddr.lnaddr_out.split("@")
    url = "https://"+lnurl_out[1]+"/.well-known/lnurlp/"+lnurl_out[0]
    return redirect(url)