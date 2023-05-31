from django.urls import path

# from . import views
from . import pdfToWord
from . import pdfToPpt
from . import pdfToImage
from . import pdInfo
from . import pdfToSvg

urlpatterns = [
    # path("", views.index, name="index"),
    # path("question", views.question, name="question"),
    # path("<int:question_id>", views.detail, name="detail"),
    # path("libjs/<file_name>", views.libjsRoute, name="libjsRoute"),
    path("uploadfile/pdftoword", pdfToWord.upload_file, name="upload_file"),
    path("uploadfile/pdfToPpt", pdfToPpt.upload_file, name="upload_file"),
    path("uploadfile/pdfToImage", pdfToImage.upload_file, name="upload_file"),
    path("uploadfile/pdfToSvg/<int:page_index>",
         pdfToSvg.upload_file,
         name="upload_file"),
    path("pdfInfo/getPdfMetaInfo",
         pdInfo.getPdfMetaInfo,
         name="getPdfMetaInfo"),
    path("pdfInfo/getPdfExtractText",
         pdInfo.getPdfExtractText,
         name="getPdfExtractText"),
    path("pdfInfo/pdfEncrypt/<password>", pdInfo.pdfEncrypt,
         name="pdfEncrypt"),
    path("pdfInfo/pdfDecrypt/<password>", pdInfo.pdfDecrypt,
         name="pdfDecrypt"),
    path("downloadFile/pdftoword/<file_path>",
         pdfToWord.download_file,
         name="download_file"),
]
