from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from datetime import datetime
import io
from typing import Dict, Any

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()
        
    def create_custom_styles(self):
        """Create custom styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3d59'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3f5e7e'),
            spaceBefore=20,
            spaceAfter=10
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceBefore=15,
            spaceAfter=10,
            borderColor=colors.HexColor('#3498db'),
            borderWidth=0,
            borderPadding=5
        ))
        
    def generate_report(self, results: Dict[str, Any], resume_filename: str, 
                       job_description: str) -> io.BytesIO:
        """Generate PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add title
        title = Paragraph("ATS Resume Analysis Report", self.styles['CustomTitle'])
        elements.append(title)
        
        # Add metadata
        metadata_data = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Resume File:', resume_filename],
            ['Overall ATS Score:', f"{results['overall_score']}%"]
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
        ]))
        elements.append(metadata_table)
        elements.append(Spacer(1, 20))
        
        # Score Summary Section
        elements.append(Paragraph("Score Breakdown", self.styles['CustomSubtitle']))
        
        score_data = [
            ['Category', 'Score', 'Status'],
            ['Keyword Match', f"{results['keyword_match_score']}%", self.get_status(results['keyword_match_score'])],
            ['Skills Match', f"{results['skills_score']}%", self.get_status(results['skills_score'])],
            ['Experience', f"{results['experience_score']}%", self.get_status(results['experience_score'])],
            ['Education', f"{results['education_score']}%", self.get_status(results['education_score'])],
            ['Format & Structure', f"{results['format_score']}%", self.get_status(results['format_score'])],
            ['Semantic Similarity', f"{results['semantic_similarity']}%", self.get_status(results['semantic_similarity'])]
        ]
        
        score_table = Table(score_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(score_table)
        elements.append(Spacer(1, 20))
        
        # Issues Found Section
        if results.get('issues'):
            elements.append(Paragraph("Issues Found", self.styles['CustomSubtitle']))
            for i, issue in enumerate(results['issues'], 1):
                issue_text = f"{i}. {issue}"
                elements.append(Paragraph(issue_text, self.styles['Normal']))
            elements.append(Spacer(1, 20))
        
        # Suggestions Section
        if results.get('suggestions'):
            elements.append(Paragraph("Improvement Suggestions", self.styles['CustomSubtitle']))
            for i, suggestion in enumerate(results['suggestions'], 1):
                suggestion_text = f"{i}. {suggestion}"
                elements.append(Paragraph(suggestion_text, self.styles['Normal']))
            elements.append(Spacer(1, 20))
        
        # Missing Keywords Section
        if results.get('missing_keywords'):
            elements.append(Paragraph("Missing Keywords", self.styles['CustomSubtitle']))
            keywords_text = ", ".join(results['missing_keywords'][:20])
            elements.append(Paragraph(f"Consider adding these keywords: {keywords_text}", 
                                     self.styles['Normal']))
            elements.append(Spacer(1, 20))
        
        # Matched Skills Section
        if results.get('matched_skills'):
            elements.append(Paragraph("Matched Skills", self.styles['CustomSubtitle']))
            skills_text = ", ".join(results['matched_skills'])
            elements.append(Paragraph(f"Skills found in your resume: {skills_text}", 
                                     self.styles['Normal']))
            elements.append(Spacer(1, 20))
        
        # Recommendations
        elements.append(PageBreak())
        elements.append(Paragraph("Final Recommendations", self.styles['CustomTitle']))
        
        recommendations = self.generate_recommendations(results)
        for rec in recommendations:
            elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
            elements.append(Spacer(1, 10))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return buffer
    
    def get_status(self, score: float) -> str:
        """Get status based on score"""
        if score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def generate_recommendations(self, results: Dict[str, Any]) -> list:
        """Generate personalized recommendations based on scores"""
        recommendations = []
        
        overall_score = results['overall_score']
        
        if overall_score >= 80:
            recommendations.append("Your resume is well-optimized for ATS. Make sure to tailor it for each specific job application.")
        elif overall_score >= 60:
            recommendations.append("Your resume shows good potential. Focus on the suggested improvements to increase your chances.")
        else:
            recommendations.append("Your resume needs significant improvements to pass ATS screening effectively.")
        
        if results['keyword_match_score'] < 60:
            recommendations.append("Focus on incorporating more relevant keywords from the job description.")
        
        if results['skills_score'] < 60:
            recommendations.append("Enhance your skills section with more relevant technical and soft skills.")
        
        if results['experience_score'] < 60:
            recommendations.append("Improve your experience section with quantifiable achievements and action verbs.")
        
        if results['format_score'] < 70:
            recommendations.append("Ensure your resume follows ATS-friendly formatting guidelines.")
        
        recommendations.append("Remember to save your resume in a compatible format (PDF or DOCX) for ATS systems.")
        recommendations.append("Avoid using images, charts, or complex formatting that ATS might not parse correctly.")
        
        return recommendations