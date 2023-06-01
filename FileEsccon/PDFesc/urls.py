from django.urls import path

# from . import views
from . import pdfToWord
from . import pdfToPpt
from . import pdfToImage
from . import pdfInfo
from . import pdfToSvg
from . import pdfMerger
from . import pdfStamp

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
    path("uploadfile/getPdfMetaInfo",
         pdfMerger.getPdfMetaInfo,
         name="getPdfMetaInfo"),
    path("uploadfile/pdfStamp/<page_indices>",
         pdfStamp.pdfStamp,
         name="pdfStamp"),
    path("uploadfile/pdfWatermark", pdfStamp.pdfWatermark,
         name="pdfWatermark"),
    path("pdfInfo/getPdfMetaInfo",
         pdfInfo.getPdfMetaInfo,
         name="getPdfMetaInfo"),
    path("pdfInfo/getPdfExtractText",
         pdfInfo.getPdfExtractText,
         name="getPdfExtractText"),
    path("pdfInfo/pdfEncrypt/<password>",
         pdfInfo.pdfEncrypt,
         name="pdfEncrypt"),
    path("pdfInfo/pdfDecrypt/<password>",
         pdfInfo.pdfDecrypt,
         name="pdfDecrypt"),
    path("downloadFile/pdftoword/<file_path>",
         pdfToWord.download_file,
         name="download_file"),
]
