import os
import logging

# create logger
def create_log(file:str) -> logging:
    # path = os.path.dirname(os.path.abspath(__file__))
    # path = '{}/{}'.format(path,file)
    # path2 = os.getcwd()
    # print(path2)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file, mode='w')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    logger.findCaller()
    # formatter = logging.Formatter('%(asctime)s %(funcName)s:%(lineno)s %(levelname)-8s '
    #                              '%(message)s')
    # formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(funcName)-25s:%(lineno)-3s  '
    #                               '%(message)s')
    formatter = logging.Formatter('%(asctime)s  %(levelname)-8s %(filename)-14s %(funcName)-25s:%(lineno)-3s  '
                                  '%(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


