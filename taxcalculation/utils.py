from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
import xhtml2pdf.pisa as pisa
from weasyprint import HTML


class PdfRender:

    @staticmethod
    def getPdf_xhtml2pdf(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return response
        else:
            return None

    @staticmethod
    def getPdf_weasyprint(path: str, params: dict):
        html_string = render_to_string(path,params)
        html = HTML(string=html_string)
        result=html.write_pdf()
        if result:
            return result
        else:
            return None
