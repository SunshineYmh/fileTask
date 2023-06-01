from PyPDF2 import PdfWriter
import json
import os
from django.http import HttpResponse
from .utils import isFIleExists, unique_id, DOWNLOAD_FILE_MEG_PATH, UPLOAD_FILE_MEG_PATH
from PDFesc.models.fileModels import FileStorage

# https://pypdf2.readthedocs.io/en/3.0.0/user/merging-pdfs.html


# pdf 合并
def getPdfMetaInfo(request):
    if request.method == "POST":
        newfile = request.FILES.getlist('newfile')  # 获得多个文件上传进来的文件列表。
        if not newfile:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))

        merger = PdfWriter()
        for fileds in newfile:
            # pdf_reader = PdfReader(fileds)
            merger.append(fileds)
            isFIleExists(UPLOAD_FILE_MEG_PATH)
            upload_file_up = os.path.join(UPLOAD_FILE_MEG_PATH, fileds.name)
            to_path = open(upload_file_up, 'wb+')
            for chunk in fileds.chunks():
                to_path.write(chunk)

            unique_id_d = unique_id()
            FileStorage.objects.create(file_id=unique_id_d,
                                       file_name=fileds.name,
                                       file_path=upload_file_up,
                                       file_content_type="application/pdf",
                                       file_ywfl="pdfMerger",
                                       file_ywdl="uploadfile",
                                       file_size=fileds.size)
        to_path.close()

        unique_id_d = unique_id()
        isFIleExists(DOWNLOAD_FILE_MEG_PATH)
        doc_file = os.path.join(DOWNLOAD_FILE_MEG_PATH, unique_id_d + ".pdf")
        merger.write(doc_file)
        merger.close()

        file_size = os.stat(doc_file).st_size
        FileStorage.objects.create(file_id=unique_id_d,
                                   file_name=unique_id_d + ".pdf",
                                   file_path=doc_file,
                                   file_content_type="application/pdf",
                                   file_ywfl="pdfMerger",
                                   file_ywdl="downloadfile",
                                   file_size=file_size)

        meg_data = {'id': unique_id_d, 'fileName': unique_id_d + ".pdf"}
        context = {"succse": True, "data": meg_data}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))
