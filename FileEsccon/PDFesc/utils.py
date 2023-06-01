import os
import datetime
import uuid
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now = datetime.datetime.now().strftime('%Y%m%d')
UPLOAD_FILE_PATH = BASE_DIR + '\\uploadfile\\pdfToWord\\' + now
DOWNLOAD_FILE_PATH = BASE_DIR + '\\downloadfile\\pdfToWord\\' + now

UPLOAD_FILE_PPTX_PATH = BASE_DIR + '\\uploadfile\\pdfToPptx\\' + now
DOWNLOAD_FILE_PPTX_PATH = BASE_DIR + '\\downloadfile\\pdfToPptx\\' + now

UPLOAD_FILE_IMAGE_PATH = BASE_DIR + '\\uploadfile\\pdfToImage\\' + now
DOWNLOAD_FILE_IMAGE_PATH = BASE_DIR + '\\downloadfile\\pdfToImage\\' + now

UPLOAD_FILE_SVG_PATH = BASE_DIR + '\\uploadfile\\pdfToSvg\\' + now
DOWNLOAD_FILE_SVG_PATH = BASE_DIR + '\\downloadfile\\pdfToSvg\\' + now

DOWNLOAD_FILE_DSC_PATH = BASE_DIR + '\\downloadfile\\pdfDec\\' + now

UPLOAD_FILE_MEG_PATH = BASE_DIR + '\\uploadfile\\pdfMerger\\' + now
DOWNLOAD_FILE_MEG_PATH = BASE_DIR + '\\downloadfile\\pdfMerger\\' + now

UPLOAD_FILE_STAMP_PATH = BASE_DIR + '\\uploadfile\\pdfStamp\\' + now
DOWNLOAD_FILE_STAMP_PATH = BASE_DIR + '\\downloadfile\\pdfStamp\\' + now


def isFIleExists(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def unique_id():
    return "{}{}".format(uuid.uuid4(),
                         time.mktime(time.localtime(time.time()))).replace(
                             "-", "").replace(".", "")
