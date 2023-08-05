#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import yaml
import os
import logging

from . import CicdContextDataSource

from ..utils import get_file_path

class DataSource(CicdContextDataSource):
    filePath = None
    isPrimary = False

    def __init__(self, config=dict):
        self.filePath = config['path']

        if 'isPrimary' in config:
            self.isPrimary = config['isPrimary']

        self.filePath = get_file_path(self.filePath)

        logging.debug("{} -> {} isPrimary:{} isLocal:{}".format(self.get_name(),self.filePath,self.isPrimary,self.is_local()))

    def is_local(self) -> bool:
        return True

    def supports_load(self) -> bool:
        return True

    def get_name(self) -> str:
        return 'yamlfile'

    def is_primary(self) -> bool:
        return self.isPrimary

    def persist(self, cicdContextDataId:str, cicdContextData:object):
        os.makedirs(os.path.dirname(self.filePath),exist_ok=True)
        with open(self.filePath, 'w') as f:
            yamlString = yaml.dump(cicdContextData, default_flow_style=False, sort_keys=False)    
            f.write(yamlString) 

    def load(self, cicdContextDataId:str) -> dict:
        if os.path.isfile(self.filePath):
            with open(self.filePath, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        return None
