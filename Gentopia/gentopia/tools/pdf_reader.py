import os
from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Optional, Type
import textwrap


class PDFReaderArgs(BaseModel):
    pdf_path: str = Field(..., description="PDF FILE")

class PDFReader(BaseTool):
    name = "pdf_reader"
    description = "A tool that has capability to summarize the pdf file"
    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, pdf_path: str) -> str:
        current_dir = os.path.dirname(__file__)  
        full_path = os.path.join(current_dir, pdf_path)

        if not os.path.isfile(full_path):
            raise ValueError(f"PDFFile not found in the current directory")

        with open(full_path, 'rb') as file:
            pdf = PdfReader(file)
            full_text = ' '.join(page.extract_text().strip() for page in pdf.pages if page.extract_text().strip())

        
        pdf_summary = self.summarize(full_text)
        return pdf_summary

    def summarize(self, text: str, length: int = 500) -> str:
        summary = textwrap.shorten(text, width=length, placeholder="...")
        return summary


    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    pdf_reader = PDFReader()
    pdf_sample = '4502_large_language_model_cascades_.pdf'  

    if not os.path.isfile(pdf_sample):
        raise FileNotFoundError(f"The file {pdf_sample} does not exist.")
    
    text = pdf_reader._run(pdf_sample)
    summary = pdf_reader.summarize(text)
    print(summary)