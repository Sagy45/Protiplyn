"""Zobrazenia (views) pre generovanie a výber dokumentov o vybavení."""

import io
import os
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from documents.models import DocumentTemplate
from equipment.models import Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA
from viewer.constants import STATUS_VRIESENI


def templates_list(request):
    """
    Zobrazuje zoznam dostupných dokumentových šablón.

    Args:
        request (HttpRequest): Prichádzajúca požiadavka.

    Returns:
        HttpResponse: Renderovaný HTML zoznam šablón.
    """
    templates = DocumentTemplate.objects.all()
    return render(request, "documents/templates_list.html", {"templates": templates})


def generate_equipment_pdf(template, equipment, user):
    """
    Vytvorí PDF dokument so zoznamom vybraného vybavenia podľa šablóny.

    Args:
        template (DocumentTemplate): Šablóna dokumentu.
        equipment (list): Zoznam vybavenia (objekty modelov).
        user (User): Používateľ, ktorý vytvára dokument.

    Returns:
        bytes: Vygenerovaný PDF dokument ako bajty.
    """
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    # Hlavička dokumentu
    c.setFont("DejaVu", 16)
    c.drawCentredString(width / 2, y, template.name)
    y -= 40

    c.setFont("DejaVu", 12)
    c.drawString(40, y, template.description or "")
    y -= 30

    c.setFont("DejaVu", 12)
    c.drawString(40, y, "Vybrané zariadenia:")
    y -= 20

    # Hlavička tabuľky
    c.setFont("DejaVu", 11)
    c.drawString(40, y, "Typ")
    c.drawString(140, y, "E-číslo")
    c.drawString(220, y, "Sériové číslo")
    c.drawString(340, y, "Stanica")
    y -= 16

    # Záznamy zariadení
    c.setFont("DejaVu", 11)
    for eq in equipment:
        c.drawString(40, y, str(eq.equipment_type))
        c.drawString(140, y, str(eq.e_number))
        c.drawString(220, y, str(eq.serial_number))
        c.drawString(340, y, str(eq.located.name))
        y -= 16

    # Podpisová časť
    y -= 20
    c.setFont("DejaVu", 12)
    c.drawString(40, y, f"Používateľ: {user.first_name} {user.last_name}")
    y -= 16
    station_name = (
        getattr(user.profile.station, "name", "-") if hasattr(user, "profile") else "-"
    )
    c.drawString(40, y, f"Stanica: {station_name}")
    y -= 16
    c.drawString(40, y, "Dátum: ____________")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def equipment_select(request, template_id):
    """
    Zobrazuje zariadenia vhodné na vloženie do dokumentu podľa typu šablóny.

    Ak je šablóna typu „rev“, vyberú sa zariadenia so stavom „V riešení“.
    Ak ide o archívnu šablónu, vyberú sa archivované zariadenia.

    Args:
        request (HttpRequest): Prichádzajúca požiadavka.
        template_id (int): ID šablóny dokumentu.

    Returns:
        HttpResponse: Stránka s výberom zariadení alebo vygenerované PDF.
    """
    template = get_object_or_404(DocumentTemplate, id=template_id)
    equipment_list = []

    # Filtrovanie podľa názvu šablóny
    if "rev" in template.name.lower():
        equipment_list = (
            list(Mask.objects.filter(status=STATUS_VRIESENI, is_archived=False))
            + list(ADPMulti.objects.filter(status=STATUS_VRIESENI, is_archived=False))
            + list(ADPSingle.objects.filter(status=STATUS_VRIESENI, is_archived=False))
            + list(AirTank.objects.filter(status=STATUS_VRIESENI, is_archived=False))
            + list(PCHO.objects.filter(status=STATUS_VRIESENI, is_archived=False))
            + list(PA.objects.filter(status=STATUS_VRIESENI, is_archived=False))
        )
    elif "vyrad" in template.name.lower() or "archiv" in template.name.lower():
        equipment_list = (
            list(Mask.objects.filter(is_archived=True))
            + list(ADPMulti.objects.filter(is_archived=True))
            + list(ADPSingle.objects.filter(is_archived=True))
            + list(AirTank.objects.filter(is_archived=True))
            + list(PCHO.objects.filter(is_archived=True))
            + list(PA.objects.filter(is_archived=True))
        )

    # Pridanie pomocných údajov do objektov zariadení
    enriched_equipment_list = []
    for eq in equipment_list:
        eq.model_name = eq.__class__.__name__
        eq.model_verbose = eq._meta.verbose_name
        enriched_equipment_list.append(eq)

    # Spracovanie odoslaného formulára
    if request.method == "POST":
        selected = request.POST.getlist("equipment_ids")
        selected_equipment = []

        model_map = {
            "Mask": Mask,
            "ADPMulti": ADPMulti,
            "ADPSingle": ADPSingle,
            "AirTank": AirTank,
            "PCHO": PCHO,
            "PA": PA,
        }

        for eq_string in selected:
            eq_id, model_name = eq_string.split("|")
            model = model_map[model_name]
            obj = model.objects.get(id=eq_id)
            selected_equipment.append(obj)

        pdf_buffer = generate_equipment_pdf(
            template=template, equipment=selected_equipment, user=request.user
        )
        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="vyplneny_dokument.pdf"'
        return response

    context = {
        "template": template,
        "equipment_list": enriched_equipment_list,
    }
    return render(request, "documents/equipment_select.html", context)
