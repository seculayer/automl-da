# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
from dataanalyzer.dataloader.DataLoader import DataLoader
from dataanalyzer.info.DAJobInfo import DAJobInfo
from dataanalyzer.common.Constants import Constants
from dataanalyzer.common.Common import Common
from dataanalyzer.manager.SFTPClientManager import SFTPClientManager
from dataanalyzer.util.Singleton import Singleton
from dataanalyzer.util.sftp.PySFTPClient import PySFTPClient


class DataAnalyzerManager(object, metaclass=Singleton):
    # class : DataAnalyzerManager
    def __init__(self):
        self.logger = Common.LOGGER.get_logger()
        self.mrms_sftp_manager: SFTPClientManager = None
        self.storage_sftp_manager: SFTPClientManager = None
        self.job_info: DAJobInfo = None

    def initialize(self, job_id: str, job_idx: str):
        self.mrms_sftp_manager = SFTPClientManager(
            "{}:{}".format(Constants.MRMS_SVC, Constants.MRMS_SFTP_PORT),
            Constants.SSH_USER, Constants.SSH_PASSWD)

        self.storage_sftp_manager = SFTPClientManager(
            "{}:{}".format(Constants.STORAGE_SVC, Constants.STORAGE_SFTP_PORT),
            Constants.SSH_USER, Constants.SSH_PASSWD)

        self.job_info = self.load_job_info(job_id, job_idx)
        self.logger.info(str(self.job_info))

        self.logger.info("DataAnalyzerManager initialized.")

    @staticmethod
    def load_job_info(job_id: str, job_idx: str):
        filename = Constants.DIR_DATA_ANALYZER + "/DA_{}_{}.job".format(job_id, job_idx)
        return DAJobInfo(filename)

    def get_job_info(self):
        return self.job_info

    def get_storage_sftp_client(self) -> PySFTPClient:
        return self.storage_sftp_manager.get_client()

    def data_loader(self):
        loader = DataLoader(self.job_info, self.storage_sftp_manager.get_client())
        loader.load()


if __name__ == '__main__':
    dam = DataAnalyzerManager("ID", "0")
