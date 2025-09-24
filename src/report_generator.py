# src/report_generator.py
import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Train Video Processing - Coverage Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(coach_data, config):
    """
    Generates a PDF report with a summary table and annotated frames.
    """
    report_path = config['PDF_REPORT_PATH']
    total_segments = len(coach_data)
    
    # Classify segments as per assignment instructions [cite: 19]
    num_engines = min(2, total_segments)
    num_brakevans = 1 if total_segments > num_engines else 0
    num_wagons = total_segments - num_engines - num_brakevans

    pdf = PDF()
    pdf.add_page()
    
    # --- Summary Page [cite: 27] ---
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Summary Report', 0, 1, 'L')
    
    pdf.set_font('Arial', '', 11)
    # Table Header
    pdf.cell(40, 10, 'Category', 1, 0, 'C')
    pdf.cell(20, 10, 'Count', 1, 0, 'C')
    pdf.cell(120, 10, 'Details', 1, 1, 'C')
    
    # Table Rows
    pdf.cell(40, 10, 'Engines', 1, 0)
    pdf.cell(20, 10, str(num_engines), 1, 0, 'C')
    pdf.cell(120, 10, 'Front locomotives', 1, 1)

    pdf.cell(40, 10, 'Wagon', 1, 0)
    pdf.cell(20, 10, str(num_wagons), 1, 0, 'C')
    pdf.cell(120, 10, 'Passenger or freight cars', 1, 1)

    pdf.cell(40, 10, 'Brakevans', 1, 0)
    pdf.cell(20, 10, str(num_brakevans), 1, 0, 'C')
    pdf.cell(120, 10, 'End of train vehicle', 1, 1)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 10, 'Total Segments', 1, 0)
    pdf.cell(20, 10, str(total_segments), 1, 0, 'C')
    pdf.cell(120, 10, f'{total_segments} units detected', 1, 1)
    
    # --- Detailed Pages ---
    for coach in coach_data:
        pdf.add_page()
        coach_id = coach['id']
        
        # Determine coach type for title
        if coach_id <= num_engines:
            title = f'Engine {coach_id}'
        elif coach_id == total_segments and num_brakevans > 0:
            title = 'Brakevan'
        else:
            wagon_num = coach_id - num_engines
            title = f'Wagon {wagon_num}'
        
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'Coverage for {title}', 0, 1, 'L')
        pdf.ln(5)

        frame_folder = coach.get('frame_folder')
        if frame_folder and os.path.exists(frame_folder):
            image_files = sorted(os.listdir(frame_folder))
            
            x_pos, y_pos = 10, pdf.get_y()
            img_width = 85  # Two images per row
            
            for i, img_name in enumerate(image_files):
                if img_name.endswith('.jpg'):
                    img_path = os.path.join(frame_folder, img_name)
                    if pdf.get_y() + 65 > 280: # Check if space is left on page
                        pdf.add_page()
                        x_pos, y_pos = 10, pdf.get_y()

                    pdf.image(img_path, x=x_pos, y=y_pos, w=img_width)
                    
                    if i % 2 == 0:
                        x_pos += img_width + 10 # Move to the right for next image
                    else:
                        x_pos = 10 # Reset to left margin
                        y_pos += 65 # Move down for next row
        else:
            pdf.set_font('Arial', 'I', 10)
            pdf.cell(0, 10, 'No frames were extracted for this segment.', 0, 1)

    pdf.output(report_path)
    print(f"Successfully generated PDF report at {report_path}")