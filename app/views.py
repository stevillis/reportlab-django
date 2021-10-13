import io
from datetime import datetime

from PIL import Image
from django.conf import settings
from django.http import HttpResponse, FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def load_brasao_img():
    image_name = 'coat-of-arms-64.jpg'
    file_path = settings.BASE_DIR / 'app/img/' / image_name
    image = Image.open(file_path)

    # new_width = 128
    # new_height = 128
    # resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    return image


def draw_brasao_first_record(p, x, y, width, height):
    brasao1 = load_brasao_img()
    p.drawInlineImage(brasao1, x + 20, y + height - 80)

    brasao2 = load_brasao_img()
    p.drawInlineImage(brasao2, width - 60, y + height - 80)


def draw_brasao_second_record(p, x, width, height):
    brasao1 = load_brasao_img()
    p.drawInlineImage(brasao1, x + 20, height - 60)

    brasao2 = load_brasao_img()
    p.drawInlineImage(brasao2, width - 60, height - 60)


def pdf1(request):
    # return HttpResponse('<h1>Hello, world!</h1>')

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file".
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello, world!")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browser
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def pdf2(request):
    response = HttpResponse(content_type='application/pdf')
    d = datetime.today().strftime('%d-%m-%Y %H-%M-%S')
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Modified
    # A4 - 595 x 842
    x = 20
    y2 = 20
    width = 555
    height = 391
    y1 = 431

    p.rect(x, y1, width, height)
    p.rect(x, y2, width, height)

    draw_brasao_first_record(p, x, y1, width, height)
    draw_brasao_second_record(p, x, width, height)

    # /Modified

    # Data to print
    data = {
        'Posts': [
            {
                'title': 'Python',
                'views': 500
            },
            {
                'title': 'JavaScript',
                'views': 500
            },
        ],
        'Videos': [
            {
                'title': 'Python Programming',
                'likes': 500
            },
        ],
        'Blogs': [
            {
                'name': 'Report  Lab',
                'likes': 500,
                'claps': 500
            },
        ],
    }

    # Start writing the PDF here
    p.setFont('Helvetica', 15, leading=None)
    p.setFillColorRGB(0.29296875, 0.453125, 0.609375)
    p.drawString(260, 800, 'My Website')
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    x1 = 20
    y1 = 750

    # Render data
    for k, v in data.items():
        p.setFont('Helvetica', 15, leading=None)
        p.drawString(x1, y1 - 12, f'{k}')
        for value in v:
            for key, val in value.items():
                p.setFont('Helvetica', 10, leading=None)
                p.drawString(x1, y1 - 20, f'{key} - {val}')
                y1 = y1 - 60

    p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
