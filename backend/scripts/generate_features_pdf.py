"""
SatQuery AI - Standalone Master Features PDF Guide Generator
Builds a publication-quality documentation PDF summarizing all project features, architecture, and SIH differentiators.
"""
import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def create_features_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    PRIMARY = colors.HexColor("#0B132B")
    SECONDARY = colors.HexColor("#1C2541")
    ACCENT = colors.HexColor("#00B4D8")
    TEXT_DARK = colors.HexColor("#1E293B")
    TEXT_MUTED = colors.HexColor("#64748B")
    BG_CARD = colors.HexColor("#F1F5F9")
    BORDER = colors.HexColor("#CBD5E1")
    HIGHLIGHT_GREEN = colors.HexColor("#059669")

    # Custom Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        alignment=1, # Center
        spaceAfter=8
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        alignment=1,
        spaceAfter=15
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        leftIndent=12,
        spaceAfter=3
    )

    style_badge = ParagraphStyle(
        'Badge',
        fontName='Helvetica-Bold',
        fontSize=8,
        textColor=colors.whitesmoke,
        alignment=1
    )

    story = []

    # ================= COVER BANNER =================
    banner = Table([[Paragraph("SMART INDIA HACKATHON 2026 • SIH26167 • OFFICIAL MASTER DOCUMENTATION", style_badge)]], colWidths=[523], rowHeights=[20])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(banner)
    story.append(Spacer(1, 15))

    story.append(Paragraph("SATQUERY AI", style_cover_title))
    story.append(Paragraph("Next-Gen Multimodal Vision-Language Earth Observation Copilot", style_cover_sub))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=15))

    # ================= EXECUTIVE SUMMARY =================
    story.append(Paragraph("1. Executive Summary & Vision", style_h1))
    summary_text = (
        "<b>SatQuery AI</b> is an enterprise-grade, agentic geospatial intelligence platform designed for defense, "
        "disaster management, and environmental monitoring. It enables analysts, field commanders, and non-technical "
        "officials to query complex optical and radar satellite imagery using conversational natural language. "
        "The system combines state-of-the-art Vision-Language Models (VLMs), sub-pixel coregistration, open-vocabulary "
        "grounding, bi-temporal Siamese change detection, and Optical-SAR radar fusion into a unified, zero-hallucination workflow."
    )
    story.append(Paragraph(summary_text, style_body))
    story.append(Spacer(1, 10))

    # ================= COMPLETE FEATURES CATALOG =================
    story.append(Paragraph("2. Complete Project Features & Capabilities Catalog", style_h1))

    features = [
        ("🛰️ Feature 1: Single-Image Remote Sensing VQA (RS-VQA)",
         "Answers complex geospatial questions about land cover, infrastructure, vehicle counts, and terrain using fine-tuned Vision-Language Transformers.",
         "• Dynamic image understanding supporting any uploaded GeoTIFF/PNG/JPEG raster.<br/>• Accurate scene interpretation with spectral reflectance context."),

        ("🎯 Feature 2: Open-Vocabulary Visual Grounding & Bounding Box Localization",
         "Localizes specified targets (aircraft, vessels, solar arrays, runways, tanks) and returns precise 2D bounding boxes and pixel overlays.",
         "• Open-vocabulary prompt parsing via Grounding DINO architecture.<br/>• Visual evidence overlays rendered directly onto high-res rasters."),

        ("🔄 Feature 3: Bi-Temporal Sub-Pixel Change Detection (T1 vs T2)",
         "Compares multi-date satellite passes to pinpoint infrastructure development, deforestation, flood progression, or disaster destruction.",
         "• Sub-pixel ECC geometric coregistration aligning multi-temporal rasters.<br/>• Generates difference heatmaps and calculates precise altered surface percentage."),

        ("📡 Feature 4: Optical + Synthetic Aperture Radar (SAR) Multimodal Fusion",
         "Fuses optical albedo with all-weather microwave SAR radar backscatter to defeat cloud cover, smoke, and nighttime blindness.",
         "• SAR speckle filtering and decibel scaling (10*log10).<br/>• Cross-attention alignment detecting hidden metallic structures under cloud cover."),

        ("🗺️ Feature 5: Interactive Geospatial ROI & Map Coordinate Explorer",
         "Interactive map layer allowing users to navigate anywhere on Earth, draw Regions of Interest (ROI), and query strategic presets (Ladakh, Assam, Andaman).",
         "• Base layer toggle with satellite imagery and ISRO Bhuvan integration.<br/>• Coordinate inspector with live Latitude/Longitude and EPSG CRS validation."),

        ("🌿 Feature 6: Spectral Biophysical Indices (NDVI, NDWI, NDBI)",
         "Automated computation of critical remote sensing spectral indices from raster bands.",
         "• <b>NDVI:</b> Crop health & forest canopy density.<br/>• <b>NDWI:</b> Flood extent mapping & water body boundaries.<br/>• <b>NDBI:</b> Urban built-up expansion & concrete encroachment."),

        ("⚔️ Feature 7: Multi-Agent Red Team vs Blue Team Cross-Verification",
         "Multi-agent architecture where Detection Specialist (Agent Alpha) and Geospatial Auditor (Agent Beta) cross-examine evidence before reaching the final verdict.",
         "• Eliminates AI hallucinations in defense and critical missions.<br/>• Generates transparent audit debate logs for commanders."),

        ("🎙️ Feature 8: Voice Query & Regional Multilingual Assistant",
         "Speech-to-text and text-to-speech engine supporting hands-free voice queries in Hindi and English.",
         "• High accessibility for field personnel, NDRF disaster teams, and local agricultural officers.<br/>• Audio response readout with natural cadence."),

        ("📄 Feature 9: 1-Click Defense & Disaster Intelligence Dossier (PDF)",
         "Instant generation of publication-grade official intelligence dossiers formatted for senior government and defense leadership.",
         "• Embeds mission metadata, high-res visual evidence overlays, and calibrated confidence meters.<br/>• Includes actionable tactical field recommendations."),

        ("📊 Feature 10: Calibrated Multi-Factor Confidence Scoring",
         "Calibrates output confidence based on spatial resolution, CRS alignment, cloud obstruction, model agreement, and evidence counts.",
         "• Calibrated percentage gauge (0-100%) and level badge (HIGH, MEDIUM, LOW).<br/>• Full explainability with itemized factor weights."),

        ("⚡ Feature 11: Real-Time Execution Trace Telemetry & Session Audit Trail",
         "End-to-end breakdown of latency spent on Input Validation, Query Planning, Model Execution, and Evidence Synthesis.",
         "• Chronological session history with 1-click restore capability.<br/>• Full OGC and REST API compliance with Swagger documentation.")
    ]

    for title, desc, bullets in features:
        story.append(Paragraph(title, style_h2))
        story.append(Paragraph(desc, style_body))
        story.append(Paragraph(bullets, style_bullet))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # ================= NATIONAL HACKATHON WINNING DIFFERENTIATORS =================
    story.append(Paragraph("3. Why SatQuery AI Wins at National Hackathons (SIH / ISRO)", style_h1))
    
    diff_table_data = [
        [Paragraph("<b>Evaluation Metric</b>", style_h2), Paragraph("<b>Standard Hackathon Submissions</b>", style_h2), Paragraph("<b>SatQuery AI (Winner Level)</b>", style_h2)],
        [
            Paragraph("<b>Image Understanding</b>", style_body),
            Paragraph("Generic pre-trained vision models or hardcoded Q&A", style_body),
            Paragraph("<b>Dynamic Multi-modal VLM + Computer Vision Raster Analytics</b> with actual spectral and spatial reasoning", style_body)
        ],
        [
            Paragraph("<b>Multimodal Depth</b>", style_body),
            Paragraph("Only single RGB optical images", style_body),
            Paragraph("<b>Optical + SAR Radar Fusion</b> penetrating clouds and camouflage with cross-modal agreement scoring", style_body)
        ],
        [
            Paragraph("<b>Geospatial Rigor</b>", style_body),
            Paragraph("Ignored CRS, georeferencing, and sub-pixel alignment", style_body),
            Paragraph("<b>Strict Geospatial Guardrails</b>, EPSG:4326/3857 validation, and ECC sub-pixel coregistration", style_body)
        ],
        [
            Paragraph("<b>Deliverables</b>", style_body),
            Paragraph("Simple text output on screen", style_body),
            Paragraph("<b>1-Click Official Defense & Disaster Intelligence PDF Dossier</b> + GIS GeoJSON export", style_body)
        ],
        [
            Paragraph("<b>Trust & Safety</b>", style_body),
            Paragraph("Black-box AI with hallucinations", style_body),
            Paragraph("<b>Red Team vs Blue Team Multi-Agent Cross-Verification</b> + Calibrated Multi-Factor Confidence", style_body)
        ]
    ]

    diff_table = Table(diff_table_data, colWidths=[120, 190, 213])
    diff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BG_CARD),
        ('BOX', (0, 0), (-1, -1), 1, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(diff_table)
    story.append(Spacer(1, 15))

    # ================= TECHNICAL ARCHITECTURE SUMMARY =================
    story.append(Paragraph("4. Technology Stack & Deployment Architecture", style_h1))
    tech_text = (
        "• <b>Backend Framework:</b> FastAPI (Asynchronous Python 3.11+), SQLAlchemy 2.0, Pydantic V2.<br/>"
        "• <b>Computer Vision & Geospatial Engine:</b> NumPy, Pillow, OpenCV, Shapely, GeoJSON, PyProj.<br/>"
        "• <b>Document & Reporting Engine:</b> ReportLab PDF Generation Suite.<br/>"
        "• <b>Frontend Architecture:</b> Vanilla Glassmorphic Web Architecture, Leaflet GIS Map Engine, Web Speech API.<br/>"
        "• <b>AI Inference:</b> OpenRouter / OpenAI Multimodal Vision Transformer Adapter with local statistical fallback."
    )
    story.append(Paragraph(tech_text, style_body))

    doc.build(story)
    print(f"Features PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent.parent
    pdf_dest = os.path.join(out_dir, "SatQuery_AI_Complete_Features_Guide.pdf")
    create_features_pdf(pdf_dest)
