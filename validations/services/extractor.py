import pdfplumber
import re

def extract_rfc(file_path: str):
    try:
        with pdfplumber.open(file_path) as pdf:
            pages_text = []
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                pages_text.append(page_text)
            
            full_text = "\n".join(pages_text)
        

        print("\n=== TEXTO EXTRAÍDO DEL PDF ===")
        print(full_text[:1500])  
        print("==============================")
        

        pattern = r'(?i)RFC[:\s-]*([A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})'
        match = re.search(pattern, full_text)
        
        if match:
            rfc_value = match.group(1).upper()
            print(f"RFC encontrado: {rfc_value}")
            return "RFC", rfc_value
        
        print("No se encontró coincidencia con el patrón RFC")
        return None, None
    
    except Exception as e:
        print(f"Error al procesar PDF: {str(e)}")
        raise Exception(f"Error procesando PDF: {str(e)}")