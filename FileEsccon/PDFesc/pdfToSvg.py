from PyPDF2 import PdfReader
import json
from django.http import HttpResponse
import svgwrite
import os
from PDFesc.models.fileModels import FileStorage
from .utils import isFIleExists, unique_id, DOWNLOAD_FILE_SVG_PATH


def upload_file(request, page_index):
    if page_index < 0:
        page_index = 0
    if request.method == "POST":
        # newfile = request.FILES.get('newfile', None)
        newfile = request.FILES.getlist('newfile')  # 获得多个文件上传进来的文件列表。
        if not newfile:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))
        doc_info_list = []
        for fileds in newfile:
            pdf_reader = PdfReader(fileds)
            print('-->>>>>>>aaaaa>', len(pdf_reader.pages))
            isFIleExists(DOWNLOAD_FILE_SVG_PATH)
            file_name = fileds.name.replace('.pdf', '').replace('.PDF', '')
            docx_file = os.path.join(DOWNLOAD_FILE_SVG_PATH,
                                     file_name + ".svg")
            dwg = svgwrite.Drawing(docx_file, profile="tiny")

            # for page in pdf_reader.pages:

            if page_index > len(pdf_reader.pages):
                page_index = len(pdf_reader.pages)

            page = pdf_reader.pages[page_index]

            def visitor_svg_rect(op, args, cm, tm):
                if op == b"re":
                    (x, y, w, h) = (args[i].as_numeric() for i in range(4))
                    dwg.add(
                        dwg.rect((x, y), (w, h),
                                 stroke="red",
                                 fill_opacity=0.05))

            def visitor_svg_text(text, cm, tm, fontDict, fontSize):
                (x, y) = (tm[4], tm[5])
                dwg.add(dwg.text(text, insert=(x, y), fill="blue"))

            page.extract_text(visitor_operand_before=visitor_svg_rect,
                              visitor_text=visitor_svg_text)
            dwg.save()

            file_size = os.stat(docx_file).st_size
            unique_id_d = unique_id()
            fileName = file_name + '.svg'
            FileStorage.objects.create(file_id=unique_id_d,
                                       file_name=fileName,
                                       file_path=docx_file,
                                       file_content_type="image/svg+xml",
                                       file_ywfl="pdfToSvg",
                                       file_ywdl="downloadfile",
                                       file_size=file_size)
            svg_data = {unique_id_d: fileName}
            doc_info_list.append(svg_data)

        context = {"succse": True, "data": doc_info_list}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))
