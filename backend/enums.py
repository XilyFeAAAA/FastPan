#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from enum import Enum, unique


class FolderType(Enum):
    FILE = 0
    FOLDER = 1


class DelFlag(Enum):
    # 0 正常 1 删除 2 回收站
    EXIST = 0
    DELETED = 1
    RECYCLE = 2


class FileCategory(Enum):
    VIDEO = 1
    MUSIC = 2
    IMAGE = 3
    DOC = 4
    OTHERS = 5


class Status(Enum):
    TRANSCODING = 1
    TRANSCODE_FAILED = 2
    TRANSCODE_SUCCESS = 3


class ShareValidType(Enum):
    DAY_1 = 1
    DAY_7 = 7
    DAY_30 = 30
    FOREVER = 0


@unique
class FileType(Enum):
    VIDEO = FileCategory.VIDEO, 0, ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.mpg', '.mpeg', '.3gp']
    MUSIC = FileCategory.MUSIC, 1, ['.mp3', '.wav', '.wma', '.flac', '.midi', '.ra', '.ape']
    IMAGE = FileCategory.IMAGE, 2, ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.psd', '.raw', '.webp']
    PDF = FileCategory.DOC, 3, ['.pdf']
    WORD = FileCategory.DOC, 4, ['.docx', '.doc']
    EXCEL = FileCategory.DOC, 5, ['.xlsx', '.xls', '.xlsm', '.xltx', '.xltm']
    TXT = FileCategory.DOC, 6, ['.txt']
    CODE = FileCategory.OTHERS, 7, ['.php', '.html', '.css', '.js', '.java', '.py', '.rb', '.c', '.cpp', '.h', '.m',
                                 '.swift', '.go', '.cs', '.aspx', '.json', '.yml', '.txt', '.md', '.sql', '.pl', '.coffee', '.less', '.scss',
                                 '.sass', '.htaccess', '.inc', '.mustache', '.erb', '.ex', '.ts', '.jsx', '.tsx', '.elm', '.hs',
                                 '.rs', '.vue', '.fs', '.fsharp', '.dart', '.r', '.ipynb', '.sh', '.bat', '.ps1']

    ZIP = FileCategory.OTHERS, 8, ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.pkg', '.dmg', '.xpi', '.cab']
    OTHER = FileCategory.OTHERS, 9, []

    def __init__(self, category, _type, extensions):
        self.category = category
        self.type = _type
        self.extensions = extensions

    @classmethod
    def FileTypeEnums(cls, ext):
        ext = ext.lower()
        for file_type in cls:
            if ext in file_type.extensions:
                return file_type.type
        return FileType.OTHER.type

    @classmethod
    def FileCategoryEnums(cls, ext):
        ext = ext.lower()
        for file_type in cls:
            if ext in file_type.extensions:
                return file_type.category.value
        return FileCategory.OTHERS.value
