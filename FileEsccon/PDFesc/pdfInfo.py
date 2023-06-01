from PyPDF2 import PdfReader, PdfWriter
import json
import os
from django.http import HttpResponse
from .utils import isFIleExists, unique_id, DOWNLOAD_FILE_DSC_PATH
from PDFesc.models.fileModels import FileStorage


def getPdfMetaInfo(request):
    if request.method == "POST":
        # newfile = request.FILES.get('newfile', None)
        newfile = request.FILES.getlist('newfile')  # 获得多个文件上传进来的文件列表。
        if not newfile:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))
        doc_info_list = []
        for fileds in newfile:
            reader = PdfReader(fileds)
            meta = reader.metadata
            doc_info = {}
            doc_info["author"] = meta.author
            doc_info["creator"] = meta.creator
            doc_info["producer"] = meta.producer
            doc_info["subject"] = meta.subject
            doc_info["title"] = meta.title
            doc_info["pageSize"] = len(reader.pages)
            doc_info_list.append(doc_info)

        context = {"succse": True, "data": doc_info_list}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))


def getPdfExtractText(request):
    if request.method == "POST":
        # newfile = request.FILES.get('newfile', None)
        newfile = request.FILES.getlist('newfile')  # 获得多个文件上传进来的文件列表。
        if not newfile:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))
        doc_info_list = []
        for fileds in newfile:
            pdf_reader = PdfReader(fileds)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()

            doc_info = {}
            doc_info[fileds.name] = text
            doc_info_list.append(doc_info)

        context = {"succse": True, "data": doc_info_list}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))


def pdfEncrypt(request, password):
    if request.method == "POST":
        newfile = request.FILES.getlist('newfile')  # 获得多个文件上传进来的文件列表。
        if not newfile:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))
        doc_info_list = []
        for fileds in newfile:
            reader = PdfReader(fileds)
            writer = PdfWriter()
            # Add all pages to the writer
            for page in reader.pages:
                writer.add_page(page)

            # Add a password to the new PDF
            writer.encrypt(password)

            # Save the new PDF to a file
            file_name = fileds.name.replace('.pdf', '').replace(
                '.PDF', '') + "_enc.pdf"
            isFIleExists(DOWNLOAD_FILE_DSC_PATH)
            docx_file = os.path.join(DOWNLOAD_FILE_DSC_PATH, file_name)
            with open(docx_file, "wb") as f:
                writer.write(f)

            file_size = os.stat(docx_file).st_size
            unique_id_d = unique_id()
            FileStorage.objects.create(file_id=unique_id_d,
                                       file_name=file_name,
                                       file_path=docx_file,
                                       file_content_type="application/pdf",
                                       file_ywfl="pdfToEnc",
                                       file_ywdl="downloadfile",
                                       file_size=file_size)
            svg_data = {unique_id_d: file_name}
            doc_info_list.append(svg_data)

        context = {"succse": True, "data": doc_info_list}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))


def pdfDecrypt(request, password):
    if request.method == "POST":
        newfile = request.FILES.getlist('newfile')  # 获得多个文件上传进来的文件列表。
        if not newfile:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))
        doc_info_list = []
        for fileds in newfile:
            reader = PdfReader(fileds)
            writer = PdfWriter()

            if reader.is_encrypted:
                reader.decrypt(password)

            # Add all pages to the writer
            for page in reader.pages:
                writer.add_page(page)

            # Save the new PDF to a file
            file_name = fileds.name.replace('.pdf', '').replace(
                '.PDF', '') + "_dec.pdf"
            isFIleExists(DOWNLOAD_FILE_DSC_PATH)
            docx_file = os.path.join(DOWNLOAD_FILE_DSC_PATH, file_name)
            with open(docx_file, "wb") as f:
                writer.write(f)

            file_size = os.stat(docx_file).st_size
            unique_id_d = unique_id()
            FileStorage.objects.create(file_id=unique_id_d,
                                       file_name=file_name,
                                       file_path=docx_file,
                                       file_content_type="application/pdf",
                                       file_ywfl="pdfToDec",
                                       file_ywdl="downloadfile",
                                       file_size=file_size)
            svg_data = {unique_id_d: file_name}
            doc_info_list.append(svg_data)

        context = {"succse": True, "data": doc_info_list}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))