from pathlib import Path
from typing import Union, Literal, List
from PyPDF2 import PdfWriter, PdfReader
import json
import os
from django.http import HttpResponse
from .utils import isFIleExists, unique_id, UPLOAD_FILE_STAMP_PATH, DOWNLOAD_FILE_STAMP_PATH
from PDFesc.models.fileModels import FileStorage


def stamp(
    content_pdf: Path,
    stamp_pdf: Path,
    pdf_result: Path,
    page_indices: Union[Literal["ALL"], List[int]] = "ALL",
):
    reader = PdfReader(stamp_pdf)
    image_page = reader.pages[0]

    writer = PdfWriter()

    reader = PdfReader(content_pdf)
    if page_indices == "ALL":
        page_indices = list(range(0, len(reader.pages)))
    for index in page_indices:
        content_page = reader.pages[index]
        mediabox = content_page.mediabox
        content_page.merge_page(image_page)
        content_page.mediabox = mediabox
        writer.add_page(content_page)

    with open(pdf_result, "wb") as fp:
        writer.write(fp)


# pdf 合并
def pdfStamp(request, page_indices):
    if request.method == "POST":
        #  获取content_pdf文件
        content_pdf = request.FILES.get('content_pdf', None)
        if not content_pdf:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))

        isFIleExists(UPLOAD_FILE_STAMP_PATH)
        content_pdf_name = content_pdf.name.replace('.pdf',
                                                    '').replace('.PDF', '')
        content_pdf_path = os.path.join(UPLOAD_FILE_STAMP_PATH,
                                        content_pdf.name)
        to_path = open(content_pdf_path, 'wb+')
        for chunk in content_pdf.chunks():
            to_path.write(chunk)
        to_path.close()
        unique_id_d = unique_id()
        FileStorage.objects.create(file_id=unique_id_d,
                                   file_name=content_pdf.name,
                                   file_path=content_pdf_path,
                                   file_content_type="application/pdf",
                                   file_ywfl="pdfStamp",
                                   file_ywdl="uploadfile",
                                   file_size=content_pdf.size)

        #  获取stamp_pdf文件
        stamp_pdf = request.FILES.get('stamp_pdf', None)
        if not stamp_pdf:
            context = {"succse": False, "msg": '提交无效，没有上传图章文件！'}
            return HttpResponse(json.dumps(context))

        isFIleExists(UPLOAD_FILE_STAMP_PATH)
        stamp_pdf_path = os.path.join(UPLOAD_FILE_STAMP_PATH, stamp_pdf.name)
        stamp_to_path = open(stamp_pdf_path, 'wb+')
        for stamp_chunk in stamp_pdf.chunks():
            stamp_to_path.write(stamp_chunk)
        stamp_to_path.close()
        stamp_unique_id_d = unique_id()
        FileStorage.objects.create(file_id=stamp_unique_id_d,
                                   file_name=stamp_pdf.name,
                                   file_path=content_pdf_path,
                                   file_content_type="application/pdf",
                                   file_ywfl="pdfStamp",
                                   file_ywdl="uploadfile",
                                   file_size=stamp_pdf.size)

        isFIleExists(DOWNLOAD_FILE_STAMP_PATH)
        pdf_result = os.path.join(DOWNLOAD_FILE_STAMP_PATH,
                                  content_pdf_name + "_stamp.pdf")

        stamp(content_pdf_path, stamp_pdf_path, pdf_result, page_indices)

        file_size = os.stat(pdf_result).st_size
        pdf_result_unique_id_d = unique_id()
        FileStorage.objects.create(file_id=pdf_result_unique_id_d,
                                   file_name=content_pdf_name + "_stamp.pdf",
                                   file_path=pdf_result,
                                   file_content_type="application/pdf",
                                   file_ywfl="pdfMerger",
                                   file_ywdl="downloadfile",
                                   file_size=file_size)

        meg_data = {
            'id': pdf_result_unique_id_d,
            'fileName': content_pdf_name + "_stamp.pdf"
        }
        context = {"succse": True, "data": meg_data}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))


# 水印
def watermark(
    content_pdf: Path,
    stamp_pdf: Path,
    pdf_result: Path,
):
    reader = PdfReader(content_pdf)
    writer = PdfWriter()
    # for page in pdf_reader.pages:
    #     content_page = reader.pages[index]
    for content_page in reader.pages:
        mediabox = content_page.mediabox

        # You need to load it again, as the last time it was overwritten
        reader_stamp = PdfReader(stamp_pdf)
        image_page = reader_stamp.pages[0]

        image_page.merge_page(content_page)
        image_page.mediabox = mediabox
        writer.add_page(image_page)

    with open(pdf_result, "wb") as fp:
        writer.write(fp)


# pdf 合并
def pdfWatermark(request, page_indices):
    if request.method == "POST":
        #  获取content_pdf文件
        content_pdf = request.FILES.get('content_pdf', None)
        if not content_pdf:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))

        isFIleExists(UPLOAD_FILE_STAMP_PATH)
        content_pdf_name = content_pdf.name.replace('.pdf',
                                                    '').replace('.PDF', '')
        content_pdf_path = os.path.join(UPLOAD_FILE_STAMP_PATH,
                                        content_pdf.name)
        to_path = open(content_pdf_path, 'wb+')
        for chunk in content_pdf.chunks():
            to_path.write(chunk)
        to_path.close()
        unique_id_d = unique_id()
        FileStorage.objects.create(file_id=unique_id_d,
                                   file_name=content_pdf.name,
                                   file_path=content_pdf_path,
                                   file_content_type="application/pdf",
                                   file_ywfl="pdfWater",
                                   file_ywdl="uploadfile",
                                   file_size=content_pdf.size)

        #  获取stamp_pdf文件
        stamp_pdf = request.FILES.get('stamp_pdf', None)
        if not stamp_pdf:
            context = {"succse": False, "msg": '提交无效，没有上传图章文件！'}
            return HttpResponse(json.dumps(context))

        isFIleExists(UPLOAD_FILE_STAMP_PATH)
        stamp_pdf_path = os.path.join(UPLOAD_FILE_STAMP_PATH, stamp_pdf.name)
        stamp_to_path = open(stamp_pdf_path, 'wb+')
        for stamp_chunk in stamp_pdf.chunks():
            stamp_to_path.write(stamp_chunk)
        stamp_to_path.close()
        stamp_unique_id_d = unique_id()
        FileStorage.objects.create(file_id=stamp_unique_id_d,
                                   file_name=stamp_pdf.name,
                                   file_path=content_pdf_path,
                                   file_content_type="application/pdf",
                                   file_ywfl="pdfWater",
                                   file_ywdl="uploadfile",
                                   file_size=stamp_pdf.size)

        isFIleExists(DOWNLOAD_FILE_STAMP_PATH)
        pdf_result = os.path.join(DOWNLOAD_FILE_STAMP_PATH,
                                  content_pdf_name + "_water.pdf")

        watermark(content_pdf_path, stamp_pdf_path, pdf_result, page_indices)

        file_size = os.stat(pdf_result).st_size
        pdf_result_unique_id_d = unique_id()
        FileStorage.objects.create(file_id=pdf_result_unique_id_d,
                                   file_name=content_pdf_name + "_stamp.pdf",
                                   file_path=pdf_result,
                                   file_content_type="application/pdf",
                                   file_ywfl="pdfMerger",
                                   file_ywdl="downloadfile",
                                   file_size=file_size)

        meg_data = {
            'id': pdf_result_unique_id_d,
            'fileName': content_pdf_name + "_water.pdf"
        }
        context = {"succse": True, "data": meg_data}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))
