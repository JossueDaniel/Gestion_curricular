from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Frame, PageTemplate
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.doctemplate import NextPageTemplate

class Report:
    def __init__(self, objeto, pre_requisitos, co_requisitos, user, aportes):
        self.objeto = objeto
        self.styles = getSampleStyleSheet()
        self.doc = None
        self.elements = []
        self.pre_requisitos = pre_requisitos
        self.co_requisitos = co_requisitos
        self.user = user
        self.aportes = aportes
        self.is_horizontal = False
        self.title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Title'],
            fontSize=10,
            leading=10,
            alignment=1,
            textColor=colors.black,
        )

    def generar_pdf(self, response):
        self.doc = SimpleDocTemplate(
            response,
            pagesize=A4,
            leftMargin=20,
            rightMargin=20,
            topMargin=30,
            bottomMargin=30
        )

        # Crear marcos para páginas verticales
        frame_vertical = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            A4[0] - self.doc.leftMargin - self.doc.rightMargin,
            A4[1] - self.doc.topMargin - self.doc.bottomMargin
        )
        # Crear marcos para páginas horizontales
        landscape_width, landscape_height = landscape(A4)
        frame_horizontal = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            landscape_width - self.doc.leftMargin - self.doc.rightMargin,
            landscape_height - self.doc.topMargin - self.doc.bottomMargin
        )

        # Crear plantillas de página
        vertical_template = PageTemplate(id='vertical', frames=frame_vertical, pagesize=A4)
        horizontal_template = PageTemplate(id='horizontal', frames=frame_horizontal, pagesize=landscape(A4))

        # Agregar plantillas al documento
        self.doc.addPageTemplates([vertical_template, horizontal_template])
        self._crear_contenido()
        self.doc.build(self.elements)


    def _agregar_titulo(self):
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Title'],
            fontSize=8,
            leading=10,
            alignment=1,
            textColor=colors.black
        )
        self.elements.append(Paragraph('INFORMACIÓN GENERAL', title_style))
        self.elements.append(Spacer(1, 10))

    def _agregar_header(self):
        centered_style = ParagraphStyle(
            "Centered",
            fontSize=8,
            alignment=1  # 1 = Centrado
        )
        small_text_style = ParagraphStyle(
            "SmallText",
            parent=self.styles["BodyText"],  # Mantiene los estilos base
            fontSize=8,  # Reducimos el tamaño de la fuente
        )
        logo_text = Paragraph('<b>UNIB.E</b>', centered_style)
        gestion_text = Paragraph('<b>GESTIÓN CURRICULAR</B>', centered_style)
        page_width = A4[0]
        margins = 40
        table_width = page_width - margins

        col_widths = [table_width * 0.25, table_width * 0.50, table_width * 0.25]
        page_text = Paragraph('<b>PÁGINA:</b> 1 de 10', small_text_style)
        codigo_text = Paragraph(f'<b>CÓDIGO:</b>\n{self.objeto.codigo}', small_text_style)
        updated_text = Paragraph(f'<b>FECHA DE ACTUALIZACIÓN</b>: {self.objeto.fecha_actualizacion}',
                                 small_text_style)
        data = [
            [logo_text, gestion_text, codigo_text],
            ['', 'FORMULARIO SYLLABUS', page_text],
            [updated_text]
        ]
        table = Table(data, colWidths=col_widths, hAlign='CENTER')
        table.setStyle(TableStyle([
            ('SPAN', (0, 0), (0, 1)),
            ('SPAN', (0, 2), (2, 2)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 20))

    def _seccion_general(self):
        page_width = A4[0]
        margins = 40
        table_width = page_width - margins

        centered_style = ParagraphStyle(
            "Centered",
            fontSize=8,
            leading=14,
            alignment=1  # 1 = Centrado
        )

        col_widths = [table_width * 0.15, table_width * 0.15, table_width * 0.12, table_width * 0.18,
                      table_width * 0.10, table_width * 0.10, table_width * 0.20]

        facultad_text = Paragraph(self.objeto.facultad, centered_style)
        carrera_text = Paragraph(self.objeto.carrera, centered_style)
        eje_text = Paragraph(f'<b>EJE DE FORMACIÓN/NIVEL DE ORGANIZACIÓN CURRICULAR</b>', centered_style)
        nivel_academico_text = Paragraph(f'<b>NIVEL ACADÉMICO</b>', centered_style)
        asignatura_text = Paragraph(self.objeto.asignatura.nombre, centered_style)
        anio_acad_text = Paragraph('<b>AÑO ACADÉMICO</b>', centered_style)
        periodo_acad_text = Paragraph('<b>PERIODO ACADÉMICO</b>', centered_style)
        fecha_inicio_text = Paragraph('<b>FECHA DE INICIO</b>', centered_style)
        pre_requisito_text = Paragraph(self.pre_requisitos, centered_style)
        co_requisito_text = Paragraph(self.co_requisitos, centered_style)

        data = [
            ['FACULTAD:', facultad_text, '', 'CARRERA:', carrera_text],
            ['ASIGNATURA'],
            ['NOMBRE', '', 'CÓDIGO', eje_text, nivel_academico_text, 'CRÉDITOS', 'TOTAL DE HORAS'],
            [
                asignatura_text,
                '',
                self.objeto.asignatura.pk,
                self.objeto.asignatura.eje_formacion,
                self.objeto.asignatura.nivel_academico,
                self.objeto.asignatura.creditos,
                self.objeto.asignatura.total_horas
            ],
            [
                'PRE-REQUISITOS',
                'CO-REQUISITOS',
                anio_acad_text,
                periodo_acad_text,
                fecha_inicio_text,
                'FECHA DE FINALIZACIÓN'
            ],
            [
                pre_requisito_text,
                co_requisito_text,
                self.objeto.anio_academico,
                self.objeto.periodo_academico,
                self.objeto.fecha_inicio,
                self.objeto.fecha_finalizacion,
            ],
            ['HORARIO DE CLASE', '', 'HORAS DE TUTORIAS', '', 'HORARIO DE TUTORIAS'],
            [
                self.objeto.horario_clase,
                '',
                self.objeto.horas_tutorias,
                '',
                self.objeto.horario_tutorias
            ],
            ['INFORMACIÓN DEL DOCENTE'],
            ['APELLIDOS Y NOMBRES', '', 'FORMACIÓN', '', 'EMAIL DOCENTE'],
            [self.user, '', self.user.formacion, '', self.user.email],
        ]

        table = Table(data, colWidths=col_widths, hAlign='CENTER')

        table.setStyle(TableStyle([
            ('SPAN', (1, 0), (2, 0)),
            ('SPAN', (4, 0), (-1, 0)),
            ('SPAN', (0, 1), (-1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (5, 4), (-1, 4)),
            ('SPAN', (5, 5), (-1, 5)),
            ('SPAN', (0, 6), (1, 6)),
            ('SPAN', (2, 6), (3, 6)),
            ('SPAN', (4, 6), (-1, 6)),
            ('SPAN', (0, 7), (1, 7)),
            ('SPAN', (2, 7), (3, 7)),
            ('SPAN', (4, 7), (-1, 7)),
            ('SPAN', (0, 8), (-1, 8)),
            ('SPAN', (0, 9), (1, 9)),
            ('SPAN', (2, 9), (3, 9)),
            ('SPAN', (4, 9), (-1, 9)),
            ('SPAN', (0, 10), (1, 10)),
            ('SPAN', (2, 10), (3, 10)),
            ('SPAN', (4, 10), (-1, 10)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
            ('FONTNAME', (0, 8), (-1, 9), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.elements.append(table)
        self.elements.append(Spacer(1, 15))
        self._seccion_firmas()

    def _seccion_firmas(self):
        page_width = A4[0]
        margins = 40
        table_width = page_width - margins
        col_widths = [table_width * 0.33, table_width * 0.33, table_width * 0.34]

        data = [
            ['Elaborado por', 'Revisado por', 'Aprobado por'],
            ['firma', 'firma', 'firma'],
            [self.user, 'Nombre', 'Nombre'],
        ]

        table = Table(data, colWidths=col_widths, rowHeights=[20, 100, 20])
        table.setStyle((TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
            ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ])))
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def _seccion_detalles(self):
        self.elements.append(PageBreak())
        self._agregar_header()
        self.elements.append(Paragraph('CARACTERIZACIÓN DE LA ASIGNATURA', self.title_style))
        self.elements.append(Paragraph(self.objeto.caracterizacion_asignatura))
        self.elements.append(Spacer(1, 20))
        self.elements.append(Paragraph('OBJETIVOS', self.title_style))
        self.elements.append(Paragraph(self.objeto.objetivos))
        self.elements.append(Spacer(1, 20))
        self.elements.append(Paragraph('COMPETENCIAS TRANSVERSALES O GENÉRICAS', self.title_style))
        self.elements.append(Paragraph(self.objeto.competencias_transversales))
        self.elements.append(Spacer(1, 20))
        self.elements.append(Paragraph('COMPETENCIAS PROFESIONALES', self.title_style))
        self.elements.append(Spacer(1, 20))
        self.elements.append(Paragraph(self.objeto.competencias_profesionales))
        self.elements.append(Spacer(1, 20))
        self.elements.append(Paragraph('METODOLOGÍA', self.title_style))
        self.elements.append(Paragraph(self.objeto.metodologia))
        self.elements.append(Spacer(1, 20))
        self.elements.append(Paragraph('PROCEDIMIENTOS DE EVALUACIÓN', self.title_style))
        self.elements.append(Paragraph(self.objeto.evaluacion))
        self.elements.append(Spacer(1, 20))
        self._tabla_evaluacion()
        self.elements.append(Spacer(1, 20))
        self.elements.append(Paragraph('BIBLIOGRAFÍA', self.title_style))
        self.elements.append(Paragraph(self.objeto.bibliografia))
        self.elements.append(Spacer(1, 20))

    def _tabla_evaluacion(self):
        page_width = A4[0]
        margins = 40
        table_width = page_width - margins
        col_widths = [table_width * 0.30, table_width * 0.18, table_width * 0.18, table_width * 0.18]
        fila_tareas = ['Tareas\nTalleres\nInvestigación\nLecciones\nPruebas\nPresentaciones']
        fila_examen = ['Examen escrito u oral']
        fila_documento = ['Documento final']
        fila_total = ['TOTAL']

        for aporte in self.aportes:
            fila_tareas.append(f'{aporte.actividades}%')
            fila_examen.append(f'{aporte.examen}%')
            fila_documento.append(f'{aporte.proyecto_final}%')
            fila_total.append(f'{aporte.total}%')

        data = [
            ['ACTIVIDADES', '1er. APORTE', '2do. APORTE', '3er. APORTE/FINAL'],
            fila_tareas,
            fila_examen,
            fila_documento,
            fila_total
        ]

        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        self.elements.append(table)

    def _seccion_cronograma(self):
        self.elements.append(PageBreak())
        self.elements.append(Paragraph('CONTENIDO PROGRAMÁTICO', self.title_style))
        self.elements.append(Spacer(1, 12))

        centered_style = ParagraphStyle(
            "Centered",
            fontSize=8,
            leading=14,
            alignment=1  # 1 = Centrado
        )
        landscape_width, landscape_height = landscape(A4)

        # Definimos los márgenes
        margins = 20  # 20 px de margen a cada lado

        # Calculamos el ancho disponible para la tabla
        table_width = landscape_width - (margins * 2)  # Restamos márgenes de ambos lados

        # Por ejemplo, si queremos que la primera columna ocupe el 10% del ancho total
        col_widths = [
            table_width * 0.05,
            table_width * .20,
            table_width * 0.10,
            table_width * 0.05,
            table_width * 0.10,
            table_width * 0.05,
            table_width * 0.10,
            table_width * 0.05,
            table_width * .15,
            table_width * .15,
        ]

        contenido_text = Paragraph('<b>UNIDAD DE APRENDIZAJE TEMAS Y SUBTEMAS</b>', centered_style)
        horas_text = Paragraph('<b>N° HORAS</b>', centered_style)
        resultados_text = Paragraph('<b>RESULTADOS DE APRENDIZAJE</b>', centered_style)
        evidencias_text = Paragraph('<b>EVIDENCIAS DE APRENDIZAJE</b>', centered_style)

        data = [
            ['ACTIVIDADES'],
            [
                'SEMANA',
                'CONTENIDOS',
                'ACTIVIDADES',
                '','', '', '', '',
                resultados_text,
                evidencias_text
            ],
            [
                '',
                contenido_text,
                'CON EL DOCENTE',
                horas_text,
                'PRÁCTICAS',
                horas_text,
                'AUTÓNOMAS',
                horas_text,
                '', ''
            ],
        ]
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('SPAN', (2, 1), (7, 1)),
            ('SPAN', (0, 1), (0, 2)),
            ('SPAN', (-2, 1), (-2, 2)),
            ('SPAN', (-1, 1), (-1, 2)),
            ('ALIGN', (0, 0), (-1, 2), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        self.elements.append(table)
        self.elements.append((Spacer(1, 12)))

    def _agregar_tabla(self):
        data = [
            ['Facultad', self.objeto.facultad],
            ['Carrera', self.objeto.carrera],
            ['Asignatura', self.objeto.asignatura],
        ]
        table = Table(data, colWidths=[120, 400])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E40AF")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F3F4F6")),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def _crear_contenido(self):
        self._agregar_header()
        self._agregar_titulo()
        self._seccion_general()
        self._seccion_detalles()
        self.elements.append(NextPageTemplate('horizontal'))
        self._seccion_cronograma()
        # self._agregar_tabla()