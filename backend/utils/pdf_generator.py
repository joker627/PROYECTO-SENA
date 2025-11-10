"""
Generador de reportes PDF para métricas del dashboard
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Circle
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from datetime import datetime
from io import BytesIO
import os


"""
Generador de reportes PDF para métricas del dashboard
"""


def _crear_barra_progreso(valor, max_valor=100, ancho=200, alto=20):
    """Crear una barra de progreso visual"""
    porcentaje = min((valor / max_valor * 100), 100) if max_valor > 0 else 0

    drawing = Drawing(ancho, alto)

    # Fondo de la barra
    drawing.add(Rect(0, 0, ancho, alto, 
                    fillColor=colors.HexColor('#ecf0f1'),
                    strokeColor=colors.HexColor('#bdc3c7'),
                    strokeWidth=1))

    # Barra de progreso (color según porcentaje)
    if porcentaje >= 75:
        color_barra = colors.HexColor('#27ae60')  # Verde
    elif porcentaje >= 50:
        color_barra = colors.HexColor('#f39c12')  # Naranja
    else:
        color_barra = colors.HexColor('#e74c3c')  # Rojo

    ancho_progreso = (ancho * porcentaje) / 100
    drawing.add(Rect(0, 0, ancho_progreso, alto,
                    fillColor=color_barra,
                    strokeColor=None))

    # Texto del porcentaje
    drawing.add(String(ancho/2, alto/2 - 3,
                      f'{int(valor)} / {int(max_valor)}',
                      fontSize=10,
                      fillColor=colors.white if porcentaje > 30 else colors.black,
                      textAnchor='middle',
                      fontName='Helvetica-Bold'))

    return drawing


def _crear_indicador_crecimiento(crecimiento):
    """Crear un indicador visual de crecimiento"""
    drawing = Drawing(80, 30)

    # Determinar color y símbolo
    if crecimiento > 0:
        color = colors.HexColor('#27ae60')
        simbolo = '▲'
        texto = f'+{crecimiento}%'
    elif crecimiento < 0:
        color = colors.HexColor('#e74c3c')
        simbolo = '▼'
        texto = f'{crecimiento}%'
    else:
        color = colors.HexColor('#95a5a6')
        simbolo = '●'
        texto = '0%'

    # Dibujar círculo de fondo
    drawing.add(Circle(15, 15, 12,
                      fillColor=color,
                      strokeColor=None))

    # Símbolo
    drawing.add(String(15, 11,
                      simbolo,
                      fontSize=10,
                      fillColor=colors.white,
                      textAnchor='middle',
                      fontName='Helvetica-Bold'))

    # Texto del porcentaje
    drawing.add(String(40, 11,
                      texto,
                      fontSize=12,
                      fillColor=color,
                      textAnchor='start',
                      fontName='Helvetica-Bold'))

    return drawing


def generar_reporte_metricas(metricas_data):
    """
    Generar PDF con métricas generales del dashboard

    Args:
        metricas_data: Diccionario con las métricas del sistema

    Returns:
        BytesIO: Buffer con el PDF generado
    """
    # Crear buffer en memoria
    buffer = BytesIO()

    # Configurar documento con márgenes
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=30,
    )

    # Contenedor para elementos del PDF
    elements = []

    # ==================== ESTILOS PERSONALIZADOS ====================
    styles = getSampleStyleSheet()

    # Estilo título principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=32
    )

    # Estilo subtítulo
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#5a6c7d'),
        spaceAfter=30,
        alignment=TA_CENTER,
        leading=14
    )

    # Estilo sección
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=15,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderWidth=2,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=8,
        backColor=colors.HexColor('#ecf0f1'),
        leading=22
    )

    # Estilo descripción
    desc_style = ParagraphStyle(
        'Description',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=14
    )

    # ==================== ENCABEZADO ====================
    # Logo o banner (simulado con rectángulo de color)
    banner = Drawing(500, 60)
    banner.add(Rect(0, 0, 500, 60,
                   fillColor=colors.HexColor('#1a5490'),
                   strokeColor=None))
    banner.add(String(250, 35,
                     'SIGN TECHNOLOGY',
                     fontSize=24,
                     fillColor=colors.white,
                     textAnchor='middle',
                     fontName='Helvetica-Bold'))
    banner.add(String(250, 15,
                     'Sistema de Traducción de Lengua de Señas',
                     fontSize=11,
                     fillColor=colors.HexColor('#ecf0f1'),
                     textAnchor='middle',
                     fontName='Helvetica'))
    elements.append(banner)
    elements.append(Spacer(1, 0.3*inch))

    # Título del reporte
    title = Paragraph("📊 Reporte de Métricas del Sistema", title_style)
    elements.append(title)

    # Fecha y hora de generación
    fecha_actual = datetime.now().strftime("%d de %B de %Y - %H:%M:%S")
    meses = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
        'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
        'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
        'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    for eng, esp in meses.items():
        fecha_actual = fecha_actual.replace(eng, esp)

    subtitle = Paragraph(
        f"<b>Fecha de generación:</b> {fecha_actual}<br/>"
        "<i>Este documento contiene información confidencial del sistema</i>",
        subtitle_style
    )
    elements.append(subtitle)

    # ==================== RESUMEN EJECUTIVO ====================
    elements.append(Paragraph("📋 Resumen Ejecutivo", section_style))

    total_usuarios = metricas_data.get('total_users', 0)
    total_traducciones = metricas_data.get('total_translations', 0)
    reportes_pendientes = metricas_data.get('pending_reports', 0)
    usuarios_anonimos = metricas_data.get('total_anonymous_users', 0)

    resumen_texto = f"""
    El sistema Sign Technology presenta las siguientes métricas al {fecha_actual.split(' - ')[0]}:
    <br/><br/>
    <b>• Usuarios Activos:</b> {total_usuarios} usuarios registrados y activos en el sistema<br/>
    <b>• Traducciones Realizadas:</b> {total_traducciones} traducciones completadas exitosamente<br/>
    <b>• Usuarios Anónimos:</b> {usuarios_anonimos} visitantes únicos registrados<br/>
    <b>• Reportes Pendientes:</b> {reportes_pendientes} reportes esperando revisión
    """
    elements.append(Paragraph(resumen_texto, desc_style))
    elements.append(Spacer(1, 0.3*inch))

    # ==================== MÉTRICAS PRINCIPALES CON INDICADORES ====================
    elements.append(Paragraph("📈 Métricas Principales", section_style))

    # Crear tabla con indicadores visuales
    metricas_tabla = []

    # Encabezado
    metricas_tabla.append([
        Paragraph('<b>Métrica</b>', styles['Normal']),
        Paragraph('<b>Valor Actual</b>', styles['Normal']),
        Paragraph('<b>Tendencia</b>', styles['Normal'])
    ])

    # Usuarios
    metricas_tabla.append([
        Paragraph('<b>👥 Usuarios Activos</b><br/><font size=8 color="#7f8c8d">Usuarios registrados en el sistema</font>', styles['Normal']),
        Paragraph(f'<font size=16 color="#2c3e50"><b>{total_usuarios}</b></font>', styles['Normal']),
        _crear_indicador_crecimiento(metricas_data.get('users_growth', 0))
    ])

    # Traducciones
    metricas_tabla.append([
        Paragraph('<b>🔄 Traducciones Totales</b><br/><font size=8 color="#7f8c8d">Traducciones completadas</font>', styles['Normal']),
        Paragraph(f'<font size=16 color="#2c3e50"><b>{total_traducciones}</b></font>', styles['Normal']),
        _crear_indicador_crecimiento(metricas_data.get('translations_growth', 0))
    ])

    # Reportes
    metricas_tabla.append([
        Paragraph('<b>⚠️ Reportes Pendientes</b><br/><font size=8 color="#7f8c8d">Requieren atención</font>', styles['Normal']),
        Paragraph(f'<font size=16 color="#2c3e50"><b>{reportes_pendientes}</b></font>', styles['Normal']),
        _crear_indicador_crecimiento(metricas_data.get('reports_growth', 0))
    ])

    # Usuarios Anónimos
    metricas_tabla.append([
        Paragraph('<b>🔓 Usuarios Anónimos</b><br/><font size=8 color="#7f8c8d">Visitantes únicos</font>', styles['Normal']),
        Paragraph(f'<font size=16 color="#2c3e50"><b>{usuarios_anonimos}</b></font>', styles['Normal']),
        Paragraph('<font size=10 color="#95a5a6">N/A</font>', styles['Normal'])
    ])

    tabla_metricas = Table(metricas_tabla, colWidths=[3.2*inch, 1.5*inch, 1.5*inch])
    tabla_metricas.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Filas alternas
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e8f4f8')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.white),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#e8f4f8')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.white),
        
        # Alineación
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Padding
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        
        # Bordes
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2c3e50')),
    ]))

    elements.append(tabla_metricas)
    elements.append(Spacer(1, 0.4*inch))

    # ==================== ALERTAS Y ESTADO DEL SISTEMA ====================
    elements.append(Paragraph("🔔 Estado del Sistema", section_style))

    alertas_data = []
    alertas_data.append([
        Paragraph('<b>Categoría</b>', styles['Normal']),
        Paragraph('<b>Cantidad</b>', styles['Normal']),
        Paragraph('<b>Estado</b>', styles['Normal'])
    ])

    alertas_sistema = metricas_data.get('system_alerts', 0)
    solicitudes_pend = metricas_data.get('pending_solicitudes', 0)

    # Fila alertas sistema
    estado_alertas = '✅ Normal' if alertas_sistema == 0 else ('⚠️ Atención' if alertas_sistema < 5 else '🚨 Crítico')
    color_alertas = colors.HexColor('#d4edda') if alertas_sistema == 0 else (colors.HexColor('#fff3cd') if alertas_sistema < 5 else colors.HexColor('#f8d7da'))

    alertas_data.append([
        Paragraph('<b>🔴 Alertas del Sistema</b><br/><font size=8>Notificaciones importantes</font>', styles['Normal']),
        Paragraph(f'<font size=14><b>{alertas_sistema}</b></font>', styles['Normal']),
        Paragraph(f'<b>{estado_alertas}</b>', styles['Normal'])
    ])

    # Fila solicitudes
    estado_solic = '✅ Al día' if solicitudes_pend < 5 else ('⚠️ Pendientes' if solicitudes_pend < 10 else '🚨 Acumuladas')
    color_solic = colors.HexColor('#d4edda') if solicitudes_pend < 5 else (colors.HexColor('#fff3cd') if solicitudes_pend < 10 else colors.HexColor('#f8d7da'))

    alertas_data.append([
        Paragraph('<b>📋 Solicitudes Pendientes</b><br/><font size=8>Esperando revisión</font>', styles['Normal']),
        Paragraph(f'<font size=14><b>{solicitudes_pend}</b></font>', styles['Normal']),
        Paragraph(f'<b>{estado_solic}</b>', styles['Normal'])
    ])

    # Fila reportes
    estado_rep = '✅ Bajo' if reportes_pendientes < 3 else ('⚠️ Moderado' if reportes_pendientes < 10 else '🚨 Alto')

    alertas_data.append([
        Paragraph('<b>📊 Reportes sin Resolver</b><br/><font size=8>Requieren atención</font>', styles['Normal']),
        Paragraph(f'<font size=14><b>{reportes_pendientes}</b></font>', styles['Normal']),
        Paragraph(f'<b>{estado_rep}</b>', styles['Normal'])
    ])

    tabla_alertas = Table(alertas_data, colWidths=[3*inch, 1.5*inch, 1.7*inch])
    tabla_alertas.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Cuerpo
        ('BACKGROUND', (0, 1), (-1, 1), color_alertas),
        ('BACKGROUND', (0, 2), (-1, 2), color_solic),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#e8f4f8')),
        
        ('ALIGN', (1, 1), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#c0392b')),
    ]))

    elements.append(tabla_alertas)
    elements.append(Spacer(1, 0.4*inch))

    # ==================== ESTADÍSTICAS ADICIONALES ====================
    if metricas_data.get('average_precision') or metricas_data.get('colaboradores_count'):
        elements.append(Paragraph("💡 Estadísticas Adicionales", section_style))

        stats_data = []
        stats_data.append([
            Paragraph('<b>Indicador</b>', styles['Normal']),
            Paragraph('<b>Valor</b>', styles['Normal']),
            Paragraph('<b>Visualización</b>', styles['Normal'])
        ])

        # Precisión promedio
        precision = metricas_data.get('average_precision', 0)
        stats_data.append([
            Paragraph('<b>🎯 Precisión Promedio</b><br/><font size=8>Exactitud del sistema</font>', styles['Normal']),
            Paragraph(f'<font size=14 color="#27ae60"><b>{precision}%</b></font>', styles['Normal']),
            _crear_barra_progreso(precision, 100, 150, 20)
        ])

        # Colaboradores
        colaboradores = metricas_data.get('colaboradores_count', 0)
        stats_data.append([
            Paragraph('<b>👨‍💼 Colaboradores Activos</b><br/><font size=8>Equipo actual</font>', styles['Normal']),
            Paragraph(f'<font size=14 color="#3498db"><b>{colaboradores}</b></font>', styles['Normal']),
            Paragraph('<font size=10 color="#95a5a6">Gestores del sistema</font>', styles['Normal'])
        ])

        tabla_stats = Table(stats_data, colWidths=[2.5*inch, 1.5*inch, 2.2*inch])
        tabla_stats.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Cuerpo
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
            ('ALIGN', (1, 1), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            ('TOPPADDING', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#229954')),
        ]))

        elements.append(tabla_stats)

    # ==================== PIE DE PÁGINA ====================
    elements.append(Spacer(1, 0.5*inch))

    footer_box = Drawing(500, 80)
    footer_box.add(Rect(0, 0, 500, 80,
                       fillColor=colors.HexColor('#ecf0f1'),
                       strokeColor=colors.HexColor('#bdc3c7'),
                       strokeWidth=1))
    footer_box.add(String(250, 55,
                         '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
                         fontSize=8,
                         fillColor=colors.HexColor('#95a5a6'),
                         textAnchor='middle'))
    footer_box.add(String(250, 40,
                         'Sign Technology - Sistema de Traducción de Lengua de Señas',
                         fontSize=10,
                         fillColor=colors.HexColor('#2c3e50'),
                         textAnchor='middle',
                         fontName='Helvetica-Bold'))
    footer_box.add(String(250, 25,
                         'Documento generado automáticamente',
                         fontSize=9,
                         fillColor=colors.HexColor('#7f8c8d'),
                         textAnchor='middle'))
    footer_box.add(String(250, 10,
                         '⚠️ CONFIDENCIAL - Solo para uso interno',
                         fontSize=8,
                         fillColor=colors.HexColor('#e74c3c'),
                         textAnchor='middle',
                         fontName='Helvetica-Bold'))

    elements.append(footer_box)

    # Construir PDF
    doc.build(elements)

    # Obtener el PDF del buffer
    buffer.seek(0)
    return buffer


# The module now exposes the function `generar_reporte_metricas` directly.

