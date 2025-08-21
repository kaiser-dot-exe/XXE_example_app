from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from defusedxml import ElementTree as DefusedET
from defusedxml.common import DefusedXmlException
import io, re

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # demo amaçlı

# Basit kontroller: DOCTYPE/ENTITY vb. var mı?
DTD_PATTERN = re.compile(rb"<!DOCTYPE|<!ENTITY", re.IGNORECASE)

def parse_xml_safely(data: bytes):
    # Ön kontrol: DTD/ENTITY izi görürsek reddedelim.
    if DTD_PATTERN.search(data):
        raise ValueError("DTD/ENTITY algılandı (potansiyel XXE).")

    # defusedxml ile güvenli parse
    try:
        root = DefusedET.fromstring(data)
        return root
    except DefusedXmlException as e:
        # defusedxml herhangi bir şüpheli yapıda exception fırlatır
        raise ValueError(f"Güvenlik nedeniyle reddedildi: {e}") from e
    except Exception as e:
        raise ValueError(f"XML geçersiz: {e}") from e

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/upload")
def upload():
    file = request.files.get("xmlfile")
    if not file or file.filename == "":
        flash("Bir XML dosyası seçin.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    data = file.read()

    try:
        root = parse_xml_safely(data)
        # Basit bir çıktı: tüm tag'ların listesi ve kök tag adı
        tags = [elem.tag for elem in root.iter()]
        return render_template("result.html", filename=filename, root=root.tag, tags=tags, xml_preview=data.decode("utf-8", errors="replace"))
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
