from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings
from django.http import HttpResponse


def save_pdf(template_src, context={}):
    template = get_template("adminpanel/sales_report.html")
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    file_name = uuid.uuid4()

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None