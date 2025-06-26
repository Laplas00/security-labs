from flask import request, redirect, url_for, session, flash, render_template, abort 
from app.utils.vulns import get_vuln_flag
from icecream import ic
import lxml.etree as ET

from app.utils.app import app


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    flag = get_vuln_flag()
    if flag != 'xxe_repurpose_local_dtd':
        abort(404)

    if request.method == 'POST':
        xml_file = request.files.get('file')
        if not xml_file:
            flash('No file uploaded')
            return redirect(url_for('contact'))

        xml_data = xml_file.read()
        import lxml.etree as ET
        try:
            parser = ET.XMLParser(load_dtd=True, resolve_entities=True)
            tree = ET.fromstring(xml_data, parser=parser)
            return ET.tostring(tree)
        except Exception as e:
            return str(e), 500

    return render_template('contact.html', vulnerabilities=get_vuln_flag())

