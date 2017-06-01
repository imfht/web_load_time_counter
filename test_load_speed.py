#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/6/1 下午2:32
# @Auth    : fiht
# @File    : load_speed_test.py
# @Purpose : test load speed

import datetime
import logging
import sys
import threading
from Queue import Queue

from selenium import webdriver


def get_time(que, target_file):
    while not que.empty():
        url = que.get()
        w = webdriver.PhantomJS()
        t_start = datetime.datetime.now()
        w.get(url)
        # w.get('http://www.sdu.xxxxxxxxxxxxxxx22xcv.cn')
        if len(w.page_source) < 50:
            logger.info('%s,failed' % url)
        else:
            logger.info('%s,%s' % (url, datetime.datetime.now() - t_start))
        w.close()


def load_file_to_que(file_name, que):
    for i in open(file_name):
        if 'http' not in i:
            i = 'http://' + i
        que.put(i.strip())


def init_log(outfile):
    logger = logging.getLogger('my_logger')
    file_hander = logging.FileHandler(outfile)
    # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # hdlr.setFormatter(formatter)
    stdout_hander = logging.StreamHandler(sys.stdout)
    logger.addHandler(file_hander)
    logger.addHandler(stdout_hander)
    logger.setLevel(logging.INFO)
    return logger


if __name__ == '__main__':

    q = Queue()
    useage = 'python load_speed_test.py [inputfile] [outputfile]'
    if len(sys.argv) < 3:
        print useage
        sys.exit(-1)
    load_file_to_que(sys.argv[1],q)
    target_file = sys.argv[2]
    logger = init_log(target_file)
    t_list = [threading.Thread(target=get_time, args=(q, target_file,)) for i in range(20)]
    for i in t_list:
        i.setDaemon(True)
        i.start()
    for i in t_list:
        i.join()
    import time

    while threading.active_count() > 1:
        print threading.active_count()
        time.sleep(1)

