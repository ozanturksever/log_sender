from src.helpers.config.config_client import ConfigClient
from src.processor.base_processor import BaseProcessor

__author__ = 'ozanturksever'

class ProcessorManager(object):
    def __init__(self):
        self.__config = ConfigClient()
        self.__processors = []

        self.__construct_processors()

    def get_processors(self):
        return self.__processors

    def get_processor(self, name):
        for p in self.__processors:
            if p.get_name() == name:
                return p

    def __construct_processors(self):
        processor_list = self.__config.get('processor')
        for processor in processor_list:
            conf = processor_list[processor]
            class_name = '%sProcessor' % conf['type'].capitalize()
            import_code = 'from src.processor.%s_processor import %s' % (
                conf['type'], class_name)
            construct_code = "instance = %s(processor, conf)" % class_name
            try:
                exec(import_code+'\n'+construct_code)
            except ImportError:
                instance = BaseProcessor(processor, conf)
                pass
            self.__processors.append(instance)
