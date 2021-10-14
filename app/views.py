import io
from datetime import datetime

from PIL import Image
from django.conf import settings
from django.http import HttpResponse, FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

PAGE_WIDTH = 595
PAGE_HEIGHT = 842


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
    p.drawInlineImage(brasao1, x + 20, y + height - 70)

    brasao2 = load_brasao_img()
    p.drawInlineImage(brasao2, width - 60, y + height - 70)


def draw_brasao_second_record(p, x, width, height):
    brasao1 = load_brasao_img()
    p.drawInlineImage(brasao1, x + 20, height - 15)

    brasao2 = load_brasao_img()
    p.drawInlineImage(brasao2, width - 60, height - 15)


def draw_column_registro(canv, label, label_x, label_y, value, value_x, value_y):
    canv.setFont('Helvetica-Bold', 10, leading=None)
    canv.drawString(label_x, label_y, label)
    canv.setFont('Helvetica', 10, leading=None)
    canv.drawString(value_x, value_y, value)


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
    y2 = 55
    width = 555
    height = 365
    y1 = 435

    p.rect(x, y1, width, height)
    p.rect(x, y2, width, height)

    draw_brasao_first_record(p, x, y1, width, height)
    draw_brasao_second_record(p, x, width, height)

    livro_label_x = x + 20
    livro_label_y = PAGE_HEIGHT - 130
    livro_value_x = livro_label_x + 30
    livro_value_y = livro_label_y
    draw_column_registro(p, 'Livro:', livro_label_x, livro_label_y, 'CBA002', livro_value_x, livro_value_y)

    folha_label_x = livro_label_x + 470
    folha_label_y = livro_label_y
    folha_value_x = folha_label_x + 35
    folha_value_y = folha_label_y
    draw_column_registro(p, 'Folha:', folha_label_x, folha_label_y, '001', folha_value_x, folha_value_y)

    processo_label_x = x + 20
    processo_label_y = livro_label_y - 15
    processo_value_x = processo_label_x + 65
    processo_value_y = processo_label_y
    draw_column_registro(p, 'Processo N.:', processo_label_x, processo_label_y, '2011128410201', processo_value_x,
                         processo_value_y)

    registro_label_x = processo_label_x + 385
    registro_label_y = processo_label_y
    registro_value_x = registro_label_x + 65
    registro_value_y = registro_label_y
    draw_column_registro(p, 'Registro N.:', registro_label_x, registro_label_y, '2011128410201', registro_value_x,
                         registro_value_y)

    diplomado_label_x = x + 20
    diplomado_label_y = processo_label_y - 15
    diplomado_value_x = diplomado_label_x + 70
    diplomado_value_y = diplomado_label_y
    draw_column_registro(p, 'Diplomado(a):', diplomado_label_x, diplomado_label_y, 'Aline Souza Montezuma Carvalho',
                         diplomado_value_x, diplomado_value_y)

    rg_label_x = x + 20
    rg_label_y = diplomado_label_y - 15
    rg_value_x = rg_label_x + 20
    rg_value_y = rg_label_y
    draw_column_registro(p, 'RG:', rg_label_x, rg_label_y, '1898964-0', rg_value_x, rg_value_y)

    orgao_expedidor_label_x = rg_label_x + 180
    orgao_expedidor_label_y = rg_label_y
    orgao_expedidor_value_x = orgao_expedidor_label_x + 90
    orgao_expedidor_value_y = orgao_expedidor_label_y
    draw_column_registro(p, 'Órgão Expedidor:', orgao_expedidor_label_x, orgao_expedidor_label_y, 'SSP',
                         orgao_expedidor_value_x, orgao_expedidor_value_y)

    estado_expedidor_label_x = rg_label_x + 385
    estado_expedidor_label_y = rg_label_y
    estado_expedidor_value_x = estado_expedidor_label_x + 90
    estado_expedidor_value_y = estado_expedidor_label_y
    draw_column_registro(p, 'Estado Expedidor:', estado_expedidor_label_x, estado_expedidor_label_y, 'MT',
                         estado_expedidor_value_x, estado_expedidor_value_y)

    cpf_label_x = x + 20
    cpf_label_y = rg_label_y - 15
    cpf_value_x = cpf_label_x + 25
    cpf_value_y = cpf_label_y
    draw_column_registro(p, 'CPF:', cpf_label_x, cpf_label_y, '029.970.861-67', cpf_value_x, cpf_value_y)

    data_nascimento_label_x = x + 20
    data_nascimento_label_y = cpf_label_y - 15
    data_nascimento_value_x = data_nascimento_label_x + 65
    data_nascimento_value_y = data_nascimento_label_y
    draw_column_registro(p, 'Nascimento:', data_nascimento_label_x, data_nascimento_label_y, '12/04/1986',
                         data_nascimento_value_x, data_nascimento_value_y)

    estado_nascimento_label_x = data_nascimento_label_x + 180
    estado_nascimento_label_y = data_nascimento_label_y
    estado_nascimento_value_x = estado_nascimento_label_x + 115
    estado_nascimento_value_y = estado_nascimento_label_y
    draw_column_registro(p, 'Estado de Nascimento:', estado_nascimento_label_x, estado_nascimento_label_y, 'MT',
                         estado_nascimento_value_x, estado_nascimento_value_y)

    estado_expedidor_label_x = data_nascimento_label_x + 385
    estado_expedidor_label_y = data_nascimento_label_y
    estado_expedidor_value_x = estado_expedidor_label_x + 75
    estado_expedidor_value_y = estado_expedidor_label_y
    draw_column_registro(p, 'Nacionalidade:', estado_expedidor_label_x, estado_expedidor_label_y, 'Brasileira',
                         estado_expedidor_value_x, estado_expedidor_value_y)

    curso_label_x = x + 20
    curso_label_y = data_nascimento_label_y - 15
    curso_value_x = curso_label_x + 35
    curso_value_y = curso_label_y
    draw_column_registro(p, 'Curso:', curso_label_x, curso_label_y, 'Tecnologia em Controle de Obras', curso_value_x,
                         curso_value_y)
    titulo_label_x = x + 20
    titulo_label_y = curso_label_y - 15
    titulo_value_x = titulo_label_x + 35
    titulo_value_y = titulo_label_y
    draw_column_registro(p, 'Título:', titulo_label_x, titulo_label_y, 'Tecnólogo', titulo_value_x,
                         titulo_value_y)

    grau_escolaridade_label_x = titulo_label_x + 350
    grau_escolaridade_label_y = titulo_label_y
    grau_escolaridade_value_x = grau_escolaridade_label_x + 110
    grau_escolaridade_value_y = grau_escolaridade_label_y
    draw_column_registro(p, 'Grau de Escolaridade:', grau_escolaridade_label_x, grau_escolaridade_label_y, 'Terceiro',
                         grau_escolaridade_value_x, grau_escolaridade_value_y)

    portaria_label_x = x + 20
    portaria_label_y = titulo_label_y - 15
    portaria_value_x = portaria_label_x + 145
    portaria_value_y = portaria_label_y
    draw_column_registro(p, 'Portaria de Reconhecimento:', portaria_label_x, portaria_label_y,
                         'Portaria do SETEC Nº 245 de 07/03/2007', portaria_value_x, portaria_value_y)

    campus_label_x = x + 20
    campus_label_y = portaria_label_y - 15
    campus_value_x = campus_label_x + 45
    campus_value_y = campus_label_y
    draw_column_registro(p, 'Campus:', campus_label_x, campus_label_y, 'Cuiabá - Octayde Jorge da Silva',
                         campus_value_x, campus_value_y)

    data_colacao_label_x = x + 20
    data_colacao_label_y = campus_label_y - 15
    data_colacao_value_x = data_colacao_label_x + 125
    data_colacao_value_y = data_colacao_label_y
    draw_column_registro(p, 'Data de Colação de Grau:', data_colacao_label_x, data_colacao_label_y, '10/09/2012',
                         data_colacao_value_x, data_colacao_value_y)

    data_expedicao_label_x = x + 20
    data_expedicao_label_y = data_colacao_label_y - 15
    data_expedicao_value_x = data_expedicao_label_x + 155
    data_expedicao_value_y = data_expedicao_label_y
    draw_column_registro(p, 'Data de Expedição do Diploma:', data_expedicao_label_x, data_expedicao_label_y,
                         '10/09/2012', data_expedicao_value_x, data_expedicao_value_y)

    data_registro_label_x = x + 20
    data_registro_label_y = data_expedicao_label_y - 15
    data_registro_value_x = data_registro_label_x + 145
    data_registro_value_y = data_registro_label_y
    draw_column_registro(p, 'Data de Registro do Diploma:', data_registro_label_x, data_registro_label_y,
                         '10/09/2012', data_registro_value_x, data_registro_value_y)

    servidor_responsavel_label_x = x + 20
    servidor_responsavel_label_y = data_registro_label_y - 15
    servidor_responsavel_value_x = servidor_responsavel_label_x + 180
    servidor_responsavel_value_y = servidor_responsavel_label_y
    draw_column_registro(p, 'Servidor Responsável pelo Registro:', servidor_responsavel_label_x,
                         servidor_responsavel_label_y, 'Neuza Ricardo Rodrigues', servidor_responsavel_value_x,
                         servidor_responsavel_value_y)

    siape_label_x = servidor_responsavel_label_x + 425
    siape_label_y = servidor_responsavel_label_y
    siape_value_x = siape_label_x + 35
    siape_value_y = siape_label_y
    draw_column_registro(p, 'SIAPE:', siape_label_x, siape_label_y, '1162995', siape_value_x, siape_value_y)

    visto_superior_label_x = x + 20
    visto_superior_label_y = servidor_responsavel_label_y - 15
    visto_superior_value_x = visto_superior_label_x + 75
    visto_superior_value_y = visto_superior_label_y
    draw_column_registro(p, 'Visto Superior:', visto_superior_label_x, visto_superior_label_y, '_' * 60,
                         visto_superior_value_x, visto_superior_value_y)

    siape_superior_label_x = visto_superior_label_x + 425
    siape_superior_label_y = servidor_responsavel_label_y - 15
    siape_superior_value_x = siape_superior_label_x + 35
    siape_superior_value_y = siape_superior_label_y
    draw_column_registro(p, 'SIAPE:', siape_superior_label_x, siape_superior_label_y, '_' * 10,
                         siape_superior_value_x, siape_superior_value_y)

    observacao_label_x = x + 20
    observacao_label_y = visto_superior_label_y - 15
    observacao_value_x = observacao_label_x + 65
    observacao_value_y = observacao_label_y
    draw_column_registro(p, 'Observação:', observacao_label_x, observacao_label_y,
                         'Reconhecido pela Port. MEC nº 815 de 29/10/2015, publicada no D.O.U. de 30/10/2015.',
                         observacao_value_x, observacao_value_y)
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

    # Stop printing data
    data = {}

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
