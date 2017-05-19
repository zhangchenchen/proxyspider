#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author by pekingzcc -*-
# -*- date : 2017-05-19 -*-

from config import (
    QINIU_AUTH, QINIU_BUCKET, OUTPUT_FILE
    )
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config


class uploadToqiniu(object):
    def  __init__(self):
        self.access_key = QINIU_AUTH["AccessKey"]
        self.secret_key = QINIU_AUTH["SecretKey"]
        self.upload_auth = Auth(self.access_key, self.secret_key)
        self.bucket_name = QINIU_BUCKET
        self.key = OUTPUT_FILE


    def upload(self):
        token = self.upload_auth.upload_token(self.bucket_name, self.key, 3600)
        try:
            ret, info = put_file(token, self.key, OUTPUT_FILE )
            print(info)
            print "success get key %s\n" % ret["key"]
        except Exception as e:
            print "something is wrong!!!"
            raise e

if __name__ == '__main__':
    uploadtoqiniu = uploadToqiniu()
    uploadtoqiniu.upload()

