#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:quincy qiang
@license: Apache Licence
@file: pdfparser_fast.py
@time: 2024/06/06
@contact: yanqiangmiffy@gamil.com
@software: PyCharm
@description: coding..
"""
import re
from io import BytesIO

import fitz
from tqdm import tqdm


class PdfParserUsingPyMuPDF():
    """
    PdfParserUsingPyMuPDF is a parser class for extracting text from PDF files using PyMuPDF library.
    """

    supported_file_extensions = [".pdf"]

    def __init__(self, max_chunk_size: int = 1000, *args, **kwargs):
        """
        Initializes the PdfParserUsingPyMuPDF object.
        """
        self.max_chunk_size = max_chunk_size

    def parse(
            self, fnm: str, *args, **kwargs
    ):
        """
        Asynchronously extracts text from a PDF file and returns it in chunks.
        """
        final_texts = []
        final_tables = []
        # Open the PDF file using pdfplumber
        doc = fitz.open(fnm) if isinstance(
            fnm, str) else fitz.open(
            BytesIO(fnm))
        for page in tqdm(doc, total=len(doc), desc="get pages"):
            table = page.find_tables()
            table = list(table)
            for ix, tab in enumerate(table):
                tab = tab.extract()
                tab = list(map(lambda x: [str(t) for t in x], tab))
                tab = list(map("||".join, tab))
                tab = "\n".join(tab)
                final_tables.append(tab)

            text = page.get_text()
            # print(text)
            # clean up text for any problematic characters
            text = re.sub("\n", " ", text).strip()
            # text = text.encode("ascii", errors="ignore").decode("ascii")
            # text = re.sub(r"([^\w\s])\1{4,}", " ", text)
            # text = re.sub(" +", " ", text).strip()

            final_texts.append(text)

        return final_texts + final_tables


if __name__ == '__main__':
    pdf_parser = PdfParserUsingPyMuPDF()
    contents = pdf_parser.parse('/data/users/searchgpt/yq/GoMate_dev/data/docs/新冠肺炎疫情.pdf')
    print(contents)
