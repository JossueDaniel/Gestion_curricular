from reportlab.pdfgen import canvas

class Report:
    def __init__(self, objeto):
        self.objeto = objeto

    def generar_pdf(self, response):
        p = canvas.Canvas(response)
        p.drawString(100, 800, f'Código: {self.objeto.asignatura}')
        p.drawString(100, 780, f'Facultad: {self.objeto.facultad}')
        p.drawString(100, 760, f'Carrera: {self.objeto.carrera}')
        p.showPage()
        p.save()