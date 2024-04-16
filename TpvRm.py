from Con_DB import DB
from flask import Flask, render_template, send_from_directory, url_for, request, send_file
import codecs
import re
import unicodedata

db = DB()
app = Flask(__name__)
caminhos = set(codecs.open(r"Z:\PCP\Leandro\kaminhos.txt", "r").readlines())


def add_paths(item):
    print('item do path', item)
    for line in caminhos:
        if ("\\" + str(item) + '.ipt') in line or ("\\" + str(item) + '.iam') in line:
            paths = line.rstrip().removeprefix('file://')
            print(paths)
            return paths

    return 'Item não encontrado na rede'


@app.route("/pdf/<filename>")
def serve_pdf(filename):
    pdf_directory = "\\\\10.40.3.5\\engenharia\\Engenharia\\06_Desenhos_PDF\\"
    return send_from_directory(pdf_directory, filename, as_attachment=False)


def url_link(cod_item):
    pdf_filename = str(cod_item) + ".pdf"
    pdf_url = url_for("serve_pdf", filename=pdf_filename)
    return pdf_url


@app.route("/cad/<path:filename>")
def serve_cad(filename):
    return send_file(filename, as_attachment=False)


def url_link_cad(cod_item):
    match = re.search(r'[A-Z]:\\.*?\.ipt', cod_item)
    if match:
        return match.group()
    else:
        return 'Caminho não encontrado'



@app.route('/', methods=['GET', 'POST'])
def index():
    cod_item = request.form.get('cod_item')
    dimencao = request.form.get('dimencao')
    variacao = request.form.get('variacao')
    print('cod_item', cod_item)
    if cod_item:
        if not str(cod_item).isdigit():
            return "O código do item deve ser um número com 5 ou 6 digitos."
        if dimencao != '' and not str(dimencao).isdigit():
            return "A dimensão deve ser um número."
        if variacao != '' and not str(variacao).isdigit():
            return "A variação deve ser um número."

        if dimencao == '':
            dimencao = None
        if variacao == '':
            variacao = None

        cod_item_base = db.item_base(cod_item) if cod_item is not None else None


        if cod_item_base:
            df = db.dim_itens(cod_item, dimencao, variacao)
        else:
            item_base = db.find_item_base(cod_item)
            print('item_base', item_base)
            df = db.dim_itens(item_base, dimencao, variacao)

        df['Arq_CAD'] = df['COD_ITEM'].apply(add_paths)

        #df['Arq_CAD'] = df['Arq_CAD'].apply(lambda x: f'<a href="#" onclick="copyToClipboard(\'{(x).join(c if not unicodedata.combining(c) else "u{:04x}".format(ord(c)) for c in x)}\')">Copiar Path</a>')
        #print(df.to_string())

        df['COD_ITEM'] = df["COD_ITEM"].apply(lambda x: rf'<a href="{url_link(x)}" target="_blank">{x}</a>')

        df = df.sort_values(by=['COD_ITEM']).reset_index(drop=True)
        df.index = df.index + 1

        table_html = df.to_html(classes='table table-striped', justify='left', escape=False, render_links=True)
        return render_template('index.html', table_html=table_html, error="")
    else:
        return render_template('index.html', table_html="", error="")


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8002)
    except Exception as err:
        print(err)
