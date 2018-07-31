#! /usr/bin/env python3

import subprocess
import os
from rest_framework.views import APIView
from django.http import HttpResponse


class RunExtend(APIView):

    def get(self, request, bar):
        eds = ExtencDataSet(bar)
        encode = eds.encode(bar)
        print(encode)
        return HttpResponse(encode)


class ExtencDataSet(object):

    def __init__(self, bar):
        self.barcode = bar
        self.WORK_PATH = '/data6/public/tanghao/10.Script/03.ExtendData/Middle'
        self.SNP_DIR = '/data6/chip/Extend_chip_data'
        self.impute_script = '/data6/public/BioPipline/Impute2/sample_imputation_2.pl'
        self.fetchdownload_script = '/data6/public/BioPipline/Impute2/fetchdownload_sample2.pl'

    def impute_cmd(self):
        os.chdir(self.WORK_PATH)
        cmd_step1 = 'perl {} -B {}'.format(self.impute_script, self.barcode)
        cmd_step2 = 'perl {s} -B {b} > {b}_fd.log 2> {b}_fd.err'.format(s=self.fetchdownload_script, b=self.barcode)
        subprocess.check_call(cmd_step1, shell=True)
        subprocess.check_call(cmd_step2, shell=True)
        with open('upload.sh', 'w') as upout, open('barcode_comparison_table.txt', 'a') as out:
            encode = self.encode(self.barcode)
            out.write(self.barcode + '\t' + encode + '\n')
            cmd_step3 = 'mv -f {} {}'.format(self.barcode + '.download.snp.txt.gz',
                                             os.path.join(self.SNP_DIR, encode + '.download.snp.txt.gz'))
            subprocess.check_call(cmd_step3)
            cmd_upload = 'coscmd upload {} {}'.format(os.path.join(self.SNP_DIR, encode + '.download.snp.txt.gz'),
                                                      os.path.join('/imputation/1200W',
                                                                   encode + '.download.snp.txt.gz'))
            upout.write(cmd_upload + '\n')
            # subprocess.check_call(cmd_upload)

    @staticmethod
    def encode(barcode):
        cmd = '/usr/local/python27/bin/python2.7 /data6/public/yeweijian/20180131mtRawdata/selfdc --encode {bar}'.format(
            bar=barcode)
        try:
            code = str(subprocess.check_output(cmd, shell=True)).strip()
        except subprocess.CalledProcessError:
            code = 'None'
        return code
