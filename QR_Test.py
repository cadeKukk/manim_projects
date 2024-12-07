from manimlib import *
import numpy as np
from PIL import Image

class QRCode(Scene):
    def construct(self):
        # Load the QR code image
        qr_image = ImageMobject("qr_code.png")
        qr_image.set_height(6)
        qr_image.shift(RIGHT * 1.5)
        
        # Create title and position it
        title = Text("SOURCING", font_size=48, weight=BOLD)
        title.next_to(qr_image, RIGHT, buff=1.0)
        title.to_edge(UP, buff=1.0)
        title.set_color(BLACK)
        
        # Create initial root directory
        root = Text("POSC_250_PRES", font_size=24, weight=BOLD)
        root.align_to(qr_image, LEFT).shift(LEFT * 4 + UP * 2)
        
        # Create folder and file texts with consistent spacing
        gov_folder = Text("├── gov_analysis", font_size=24, weight=BOLD)
        manimlib_file = Text("├── manimlib.py", font_size=24, weight=BOLD)
        readme_file = Text("└── README.md", font_size=24, weight=BOLD)
        
        # Create expanded folder contents with more indentation
        manimlib_contents = VGroup(
            Text("       ├── QR_Test.py", font_size=24, weight=BOLD),
            Text("       └── regres1.py", font_size=24, weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        gov_contents = VGroup(
            Text("       ├── regres1.py", font_size=24, weight=BOLD),
            Text("       └── collector1.py", font_size=24, weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        # Position all elements
        for item in [gov_folder, manimlib_file, readme_file]:
            item.align_to(root, LEFT)
        gov_folder.next_to(root, DOWN, buff=0.3)
        manimlib_file.next_to(gov_folder, DOWN, buff=0.3)
        readme_file.next_to(manimlib_file, DOWN, buff=0.3)
        
        # Position contents with more indentation
        manimlib_contents.next_to(manimlib_file, DOWN, buff=0.3)
        manimlib_contents.shift(RIGHT * 0.5)  # Additional indentation
        
        gov_contents.next_to(gov_folder, DOWN, buff=0.3)
        gov_contents.shift(RIGHT * 0.5)  # Additional indentation
        
        # Set white background
        self.camera.background_color = WHITE
        
        # Create cover for QR code
        cover = Rectangle(
            height=qr_image.get_height(),
            width=qr_image.get_width(),
            fill_opacity=1,
            fill_color=WHITE,
            stroke_width=0
        )
        cover.move_to(qr_image)
        
        # Initial setup
        self.add(qr_image)
        self.add(title)
        self.add(cover)
        
        # Reveal QR code first
        self.play(
            cover.animate.set_opacity(0),
            run_time=1.5,
            rate_func=linear
        )
        
        # Wait a moment before starting tree animation
        self.wait(0.5)
        
        # Show initial tree
        self.play(Write(root), run_time=0.5)
        self.play(
            *[Write(item) for item in [gov_folder, manimlib_file, readme_file]],
            run_time=1
        )
        
        # Wait before starting folder animations
        self.wait(0.5)
        
        # Open manimlib.py folder
        self.play(
            readme_file.animate.shift(DOWN * 1.2),
            FadeIn(manimlib_contents, shift=UP * 0.3),
            run_time=0.7
        )
        
        # Close manimlib.py folder
        self.wait(1)
        self.play(
            readme_file.animate.shift(UP * 1.2),
            FadeOut(manimlib_contents),
            run_time=0.7
        )
        
        # Open gov_analysis folder
        self.wait(0.5)
        self.play(
            manimlib_file.animate.shift(DOWN * 1.2),
            readme_file.animate.shift(DOWN * 1.2),
            FadeIn(gov_contents, shift=UP * 0.3),
            run_time=0.7
        )
        
        self.wait(2)
        
        # Fade out tree elements
        self.play(
            *[FadeOut(obj) for obj in [root, gov_folder, manimlib_file, readme_file, gov_contents]],
            run_time=0.7
        )
        
        # Updated sources list focused on accessible data sources
        sources = [
            "World Bank Open Data Repository",
            "UN Statistical Database",
            "OECD iLibrary Data",
            "European Social Survey",
            "Pew Research Center Data",
            "Inter-university Consortium for Political and Social Research (ICPSR)",
            "Harvard Dataverse",
            "Google Public Data Explorer",
            "World Values Survey",
            "International Monetary Fund Data",
            "US Census Bureau Data",
            "Eurostat Database",
            "Global Financial Data",
            "UNESCO Institute for Statistics",
            "WHO Global Health Observatory",
            "International Labor Organization Statistics",
            "UN Comtrade Database",
            "World Trade Organization Statistics",
            "Global Terrorism Database",
            "Correlates of War Project",
            "Polity V Project",
            "Varieties of Democracy (V-Dem) Dataset",
            "Quality of Government Dataset",
            "Armed Conflict Location & Event Data Project",
            "Penn World Table",
            "Manifesto Project Database",
            "Comparative Political Data Set",
            "European Election Database",
            "International Social Survey Programme",
            "Afrobarometer Data",
            "Latinobarometer Data",
            "Asian Barometer",
            "Arab Barometer",
            "European Values Study",
            "Comparative Study of Electoral Systems",
            "Global Peace Index",
            "Freedom House Data",
            "Transparency International Corruption Data",
            "World Bank Governance Indicators",
            "UNHCR Refugee Statistics",
            "International Crisis Behavior Project",
            "Global Innovation Index",
            "ITU Digital Development Dataset",
            "UN E-Government Survey Data",
            "Digital Society Index",
            "Global Cybersecurity Index",
            "Internet World Stats Database",
            "Global Digital Reports (We Are Social)",
            "SIPRI Military Expenditure Database",
            "World Income Inequality Database",
            "Global Education Monitoring Data",
            "World Economic Forum Global Competitiveness Data",
            "Digital Economy and Society Index",
            "Global Open Data Index",
            "Open Data Barometer",
            "Global Financial Centers Index",
            "Environmental Performance Index",
            "Climate Change Performance Index",
            "Global Gender Gap Report Data",
            "Social Progress Index",
            "Worldwide Governance Indicators",
            "Global Entrepreneurship Monitor",
            "Digital Evolution Index",
            "Network Readiness Index",
            "Global Innovation Policy Database",
            "UNCTAD Statistics Database",
            "Global Financial Development Database",
            "Democracy Index Data",
            "Press Freedom Data",
            "Human Development Index Data",
            "Global State of Democracy Indices",
            "International Property Rights Index",
            "Economic Freedom of the World Data",
            "Global Connectivity Index",
            "Digital Intelligence Index",
            "AI Readiness Index",
            "Global Cybersecurity Capacity Portal",
            "Digital Trade Restrictiveness Index",
            "Global Data Innovation Index"
        ]
        
        # Create text objects for sources with left alignment and width limit
        max_width = 5
        source_texts = VGroup()
        
        for source in sources:  # sources list remains the same as before
            text = Text(source, font_size=24, weight=BOLD, color=BLACK)
            if text.get_width() > max_width:
                words = source.split()
                mid = len(words) // 2
                line1 = " ".join(words[:mid])
                line2 = " ".join(words[mid:])
                text = VGroup(
                    Text(line1, font_size=24, weight=BOLD, color=BLACK),
                    Text(line2, font_size=24, weight=BOLD, color=BLACK)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            text.align_to(ORIGIN, LEFT)
            source_texts.add(text)
        
        # Arrange all texts with proper spacing
        source_texts.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        # Position sources further left and adjust starting position
        source_texts.align_to(qr_image, LEFT).shift(LEFT * 5.5)
        source_texts.shift(UP * 15)
        
        # Create constant-speed scrolling animation
        self.play(
            source_texts.animate.shift(DOWN * (len(sources) * 0.8 + 30)),
            run_time=30,
            rate_func=linear
        )
        
        # Brief pause before recentering
        self.wait(0.5)
        
        # Fade out the source texts
        self.play(
            FadeOut(source_texts),
            run_time=0.7
        )
        
        # Recenter QR code with smooth animation
        self.play(
            qr_image.animate.move_to(ORIGIN),
            title.animate.shift(RIGHT * 1.5),  # Move title with QR code
            run_time=1.5,
            rate_func=smooth
        )
        
        self.wait(2)