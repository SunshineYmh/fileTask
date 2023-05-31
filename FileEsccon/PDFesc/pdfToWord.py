import json
from django.http import HttpResponse
from django.shortcuts import render
import os
from django.core.cache import cache
from pdf2docx import Converter
from PDFesc.models.fileModels import FileStorage
from .utils import isFIleExists, unique_id, UPLOAD_FILE_PATH, DOWNLOAD_FILE_PATH

# https://dothinking.github.io/pdf2docx/quickstart.convert.html


def PyPDFToWord(pdf_file, fileName):
    print(DOWNLOAD_FILE_PATH, "--333---", pdf_file, fileName)
    fileName = fileName.replace('.pdf', '').replace('.PDF', '') + '.docx'
    isFIleExists(DOWNLOAD_FILE_PATH)
    docx_file = os.path.join(DOWNLOAD_FILE_PATH, fileName)
    # pdf_file = 'E:\\worknew\\python\\FileEsccon\\uploadfile\\pdfToWord\\20230530\\666.pdf'
    # docx_file = 'E:\\worknew\\python\\FileEsccon\\uploadfile\\pdfToWord\\999.docx'
    cv = Converter(pdf_file)
    cv.convert(docx_file, start=0, end=None)
    # cv.convert(docx_file)
    cv.close()
    # parse(pdf_file, docx_file)  方法2
    # docx_file.close()
    file_size = os.stat(docx_file).st_size
    unique_id_d = unique_id()
    FileStorage.objects.create(
        file_id=unique_id_d,
        file_name=fileName,
        file_path=docx_file,
        file_content_type=
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        file_ywfl="pdfToWord",
        file_ywdl="downloadfile",
        file_size=file_size)
    context = {unique_id_d: fileName}
    return context


# 上传文件
def upload_file(request):
    if request.method == "POST":
        # newfile = request.FILES.get('newfile', None)
        newfile = request.FILES.getlist('newfile')  # 获得多个文件上传进来的文件列表。
        if not newfile:
            context = {"succse": False, "msg": '提交无效，没有文件上传！'}
            return HttpResponse(json.dumps(context))
        isFIleExists(UPLOAD_FILE_PATH)
        down_file_list = {}
        for fileds in newfile:
            upload_file_up = os.path.join(UPLOAD_FILE_PATH, fileds.name)
            down_file_list[upload_file_up] = fileds.name
            to_path = open(upload_file_up, 'wb+')
            for chunk in fileds.chunks():
                to_path.write(chunk)

            unique_id_d = unique_id()
            # 设置缓存，设置失效时间为1小时
            cache.set(unique_id_d, fileds.name, timeout=10)
            FileStorage.objects.create(file_id=unique_id_d,
                                       file_name=fileds.name,
                                       file_path=upload_file_up,
                                       file_content_type="application/pdf",
                                       file_ywfl="pdfToWord",
                                       file_ywdl="uploadfile",
                                       file_size=fileds.size)
        to_path.close()

        docx_data_list = []
        # 遍历字典的键值对
        for downfilePath, filee_name in down_file_list.items():
            docx_data = PyPDFToWord(downfilePath, filee_name)
            docx_data_list.append(docx_data)

        context = {"succse": True, "data": docx_data_list}
        return HttpResponse(json.dumps(context))
    else:
        context = {"succse": False, "msg": '非表单提交访问！'}
        return HttpResponse(json.dumps(context))


# 下载文件
def download_file(request, file_path):
    # 获取文件路径
    # file_path = os.path.join(settings.MEDIA_ROOT, 'example.pdf')
    print('.>>>>>', file_path)
    file_path = 'E:\\worknew\\python\\FileEsccon\\downloadfile\\pdfToWord\\20230531\\\u53ef\u4fe1\u8ba4\u8bc1\u670d\u52a1\u533a\u5757\u94fe\u5e73\u53f0-\u5e94\u7528\u65b9\u63a5\u53e3\u6587\u6863V2.1.docx'
    # 打开文件
    with open(file_path, 'rb') as f:
        # 构建 HttpResponse 对象
        response = HttpResponse(
            f.read(),
            content_type=
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        # 设置 Content-Disposition 头部，告诉浏览器下载文件而不是直接打开
        response['Content-Disposition'] = 'attachment; filename=' + f.name
        return response
