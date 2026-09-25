"""
Generates an authentic multi-page Maharashtra State Board Grade 7 Science sample PDF.
Includes:
- Page 1: Chapter 6: Properties of Substances - Separation of Mixtures (Chromatography procedure - Positive Test)
- Page 2: Chapter 6: General notes & generic suggestions (Negative Test: "Discuss in groups", "Use a chart")
- Page 3: Chapter 19: Properties of a Magnetic Field - Magnetic Lines of Force (Iron filings & pins procedure - Positive Test)
- Page 4: Incomplete activity & resource mentions (Incomplete / Resource tests)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors


def generate_mh_science_pdf(output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a365d')
    )
    heading_style = ParagraphStyle(
        'ChapterHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2b6cb0'),
        spaceAfter=10
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=8
    )
    callout_style = ParagraphStyle(
        'ActivityBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1a202c'),
        backColor=colors.HexColor('#edf2f7'),
        borderPadding=8,
        spaceAfter=10
    )

    story = []

    # --- PAGE 1: CHROMATOGRAPHY (POSITIVE TEST) ---
    story.append(Paragraph("Maharashtra State Board of Secondary and Higher Secondary Education", title_style))
    story.append(Paragraph("General Science — Standard Seven (Grade 7)", heading_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Chapter 6: Measurement and Physical Properties of Substances</b>", heading_style))
    story.append(Paragraph(
        "Many substances around us exist as mixtures of two or more components. In chemical laboratories and industries, "
        "it is often necessary to separate the pure constituents of a mixture. One of the most effective and simple methods "
        "used for this purpose is <b>Chromatography</b>.",
        body_style
    ))
    story.append(Paragraph("<b>Let us try this: Separation of components of ink by Paper Chromatography</b>", heading_style))
    story.append(Paragraph(
        "<b>Apparatus & Materials:</b> A 250 ml glass beaker, a strip of Whatman filter paper (or blotting paper), "
        "blue writing ink, a pencil, a ruler, and water (or chalkstick as an alternative).<br/><br/>"
        "<b>Procedure:</b><br/>"
        "1. Take a rectangular strip of filter paper measuring approximately 15 cm in length and 2 cm in width.<br/>"
        "2. Using a pencil, draw a light horizontal line across the strip about 2 cm above the bottom edge.<br/>"
        "3. Place a small concentrated drop of blue ink in the center of this line using a fine dropper or nib and let it dry.<br/>"
        "4. Pour a small quantity of water into the beaker so that it reaches a depth of about 1 cm.<br/>"
        "5. Suspend the paper strip vertically inside the beaker with the help of a split cork or clip, so that the bottom edge "
        "dips into the water, but the ink spot remains strictly above the water level.<br/>"
        "6. Observe the apparatus quietly as the water begins to rise up the paper strip through capillary action.<br/>"
        "7. As the water solvent moves upward past the ink spot, students will observe that the original blue spot begins to separate "
        "into distinct colored bands (e.g. violet, cyan, or pink) at different heights on the strip.<br/><br/>"
        "<b>Scientific Principle & Learning Connection:</b><br/>"
        "The different dye components of the ink have different solubilities in the solvent (water) and different degrees of adsorption "
        "to the filter paper fibers. The component which is more soluble ascends faster and reaches a greater height, while the less "
        "soluble component lags behind. This concrete experiment proves directly that the blue ink is not a single pure substance, but a "
        "mixture of multiple distinct color pigments.",
        callout_style
    ))
    story.append(PageBreak())

    # --- PAGE 2: GENERIC TEACHING SUGGESTIONS (NEGATIVE TEST) ---
    story.append(Paragraph("<b>Chapter 6: Measurement and Physical Properties (Continued)</b>", heading_style))
    story.append(Paragraph(
        "<b>Classroom Teaching Suggestions for Teachers:</b><br/>"
        "• Teacher should conduct a discussion in the classroom about different mixtures seen in daily life, such as tea, sherbet, and air.<br/>"
        "• Use a diagram from page 45 to show the arrangement of particles in solids, liquids, and gases.<br/>"
        "• Teacher should show students a chart depicting various lab instruments.<br/>"
        "• Ask students to form small groups and discuss why pure water is a compound while salt water is a mixture.<br/>"
        "• Teachers should do an experiment demonstrating melting of ice when convenient.",
        body_style
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Exercises and Questions:</b>", heading_style))
    story.append(Paragraph(
        "1. What is meant by chromatography?<br/>"
        "2. Which property forms the basis for separating components in chromatography?<br/>"
        "3. Give two real-world examples of mixtures separated by physical methods.",
        body_style
    ))
    story.append(PageBreak())

    # --- PAGE 3: MAGNETISM & MAGNETIC LINES OF FORCE (POSITIVE TEST) ---
    story.append(Paragraph("<b>Chapter 19: Properties of a Magnetic Field</b>", heading_style))
    story.append(Paragraph(
        "A magnet attracts magnetic substances towards itself. The region around a magnet where its influence can be detected "
        "is called its magnetic field. Since magnetic forces cannot be seen with naked eyes, we use physical methods to trace "
        "the lines of magnetic force.",
        body_style
    ))
    story.append(Paragraph("<b>Activity: Tracing Magnetic Lines of Force using Iron Filings and Floating Pins</b>", heading_style))
    story.append(Paragraph(
        "<b>Materials:</b> A strong bar magnet, a stiff sheet of white cardboard or glass plate, fine iron filings, "
        "a sifter, small steel pins, a plastic bottle or shallow water bowl.<br/><br/>"
        "<b>Instructional Procedure:</b><br/>"
        "1. Place a strong bar magnet horizontally in the center of a wooden table.<br/>"
        "2. Place a sheet of smooth white cardboard directly over the bar magnet.<br/>"
        "3. Using a fine sifter, sprinkle iron filings evenly and thinly over the entire surface of the cardboard.<br/>"
        "4. Instruct students to gently tap the edge of the cardboard with a fingertip 3 to 4 times.<br/>"
        "5. Alternatively, place small steel pins inserted through small styrofoam discs floating on water in a flat shallow dish, "
        "placed adjacent to the magnet.<br/>"
        "6. Direct student observation: Notice how the scattered iron filings immediately twist and arrange themselves into distinct, "
        "continuous curved curves stretching from one pole of the magnet to the other.<br/>"
        "7. Guide students to observe the concentration of lines at the North and South poles compared to the center of the magnet.<br/><br/>"
        "<b>Learning Connection:</b><br/>"
        "Each iron filing becomes a tiny induced magnetic dipole and aligns along the direction of the magnetic field vector at that point. "
        "The curved paths formed by the filings visualize Michael Faraday's lines of magnetic force. The high density of lines at the poles "
        "demonstrates that magnetic field intensity is strongest near the poles.",
        callout_style
    ))
    story.append(PageBreak())

    # --- PAGE 4: INCOMPLETE ACTIVITY & RESOURCE MENTIONS (INCOMPLETE / RESOURCE TESTS) ---
    story.append(Paragraph("<b>Chapter 19: Magnetic Field (Continued)</b>", heading_style))
    story.append(Paragraph(
        "<b>Observe and Discuss:</b><br/>"
        "Look at the picture of the Earth's magnetic field on the board. Observe how compass needles point north. "
        "Try this at home: Take a needle, stroke it with a magnet, and see if it can attract small paper clips.",
        body_style
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Supplementary Teaching Resources:</b>", heading_style))
    story.append(Paragraph(
        "• Educational Video CD: 'Mysteries of Magnetism' (DIKSHA portal QR Code).<br/>"
        "• Activity Worksheet No. 7: Magnetism Crossword Puzzle.<br/>"
        "• Laboratory apparatus: Magnetic compass, Horseshoe magnet, iron stand.",
        body_style
    ))
    story.append(PageBreak())

    # --- PAGE 5: PLANT IDENTIFICATION (SECTION 18 TEST CASE: REVIEW_REQUIRED) ---
    story.append(Paragraph("<b>Chapter 2: Plants: Structure and Function</b>", heading_style))
    story.append(Paragraph(
        "<b>What helps us to easily identify the plants around us?</b><br/>"
        "Observe the plants around you and discuss their parts with your classmates.<br/>"
        "The root, stem, leaves, flowers, fruits, etc. of different plants are different. "
        "We can identify plants with the help of these different characteristics. "
        "Let us now examine these plant organs in more detail.",
        callout_style
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "In the primary grades, we have learned that plants have various organs that perform specific vital functions. "
        "Each organ is adapted to the environmental conditions in which the plant grows.",
        body_style
    ))
    story.append(PageBreak())

    # --- PAGE 6: MATHEMATICS: ANGLE BISECTOR CONSTRUCTION (MULTI-SUBJECT TEST) ---
    story.append(Paragraph("Maharashtra State Board of Secondary and Higher Secondary Education", title_style))
    story.append(Paragraph("Mathematics — Standard Six (Grade 6)", heading_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Chapter 1: Basic Concepts in Geometry — Angle Bisector</b>", heading_style))
    story.append(Paragraph(
        "A ray which divides an angle into two equal parts is called the <b>bisector</b> of that angle. "
        "We can construct an accurate angle bisector using a ruler and compasses.",
        body_style
    ))
    story.append(Paragraph("<b>Activity: Constructing an Angle Bisector using a Compass and Ruler</b>", heading_style))
    story.append(Paragraph(
        "<b>Materials & Instruments:</b> Compass box containing ruler, pencil, compass with sharp pencil tip, and blank paper.<br/><br/>"
        "<b>Step-by-step Construction Procedure:</b><br/>"
        "1. Draw any angle ∠ABC of measure 70° on the paper using a protractor and ruler.<br/>"
        "2. Place the metallic point of the compass at vertex B. Taking any convenient radius, draw an arc to cut ray BA at point P and ray BC at point Q.<br/>"
        "3. Now, place the point of the compass at point P. Taking a radius more than half the distance between P and Q, draw an arc inside the angle.<br/>"
        "4. Without changing the radius, place the compass point at point Q and draw another arc intersecting the previous arc. Name the point of intersection as O.<br/>"
        "5. Draw a straight ray from vertex B passing through point O using a ruler. Ray BO is the required angle bisector of ∠ABC.<br/>"
        "6. Verification: Measure ∠ABO and ∠CBO using a protractor. Both angles measure exactly 35°, demonstrating that ray BO bisects ∠ABC into two congruent angles.<br/><br/>"
        "<b>Mathematical Principle & Learning Connection:</b><br/>"
        "Points on the angle bisector are equidistant from the two arms of the angle. By maintaining equal radii from points P and Q, point O forms two congruent triangles (ΔBPO ≅ ΔBQO by SSS congruence), ensuring ∠PBO = ∠QBO.",
        callout_style
    ))

    doc.build(story)
    return output_path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "mh_grade7_science_sample.pdf")
    generate_mh_science_pdf(out)
    print(f"Generated sample PDF at: {out}")
