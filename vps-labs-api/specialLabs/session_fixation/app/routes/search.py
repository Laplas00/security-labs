
from flask import request, render_template, redirect, url_for, session, flash, render_template_string, g
from app.utils.app import app, get_db
from app.utils.vulns import get_vuln_flag
from app.utils.search_vulns import reflected_xss, reflected_xss_angularjs_sandbox_escape

