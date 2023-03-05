from flask import Blueprint, render_template

documentation = Blueprint("documentation", __name__, url_prefix="/documentation")

@documentation.route('/', methods=['GET'])
def documentation_page():
    return render_template('documentation/documentation.html')

@documentation.route('/relay', methods=['GET'])
def doc_relay():
    return render_template('documentation/relay.html')

@documentation.route('/nip', methods=['GET'])
def doc_nip():
    return render_template('documentation/nip.html')

@documentation.route('/lnaddr_forwarding', methods=['GET'])
def doc_lnaddr_forwarding():
    return render_template('documentation/lnaddr_forwarding.html')