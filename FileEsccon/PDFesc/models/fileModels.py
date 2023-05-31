from django.db import models


class FileStorage(models.Model):
    file_id = models.CharField('文件唯一id', max_length=200)
    file_date = models.DateTimeField('日期', auto_now=True)
    file_name = models.CharField('文件路径', max_length=200)
    file_path = models.CharField('文件路径', max_length=1000)
    file_content_type = models.CharField('文件类型', max_length=200)
    file_size = models.IntegerField('文件大小', default=0)
    file_ywfl = models.CharField('文件分类', max_length=200)
    file_ywdl = models.CharField('文件大类', max_length=200)
    file_state = models.IntegerField('文件状态，0-正常；1-已失效', default=0)
