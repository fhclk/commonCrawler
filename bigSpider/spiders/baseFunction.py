#-*- coding:utf-8 -*-

import datetime
import re

class BaseFunctions(object):
    def get_same_xpath(self, selector1, selector2):
        '''
        通过两个xpath选择器，获取他们的共同部分，用于循环列表，通过连续的两个选择器，获取共同选择器
        :param selector1: 第一个选择器的xpath
        :param selector2: 第二个选择器的xpath
        :return: 两个选择器的共同部分
        '''
        selector1_list = selector1.split('/')
        selector2_list = selector2.split('/')
        min_len = len(selector1_list) if len(selector1_list) < len(selector2_list) else len(selector2_list)
        for i in range(0, min_len):
            if selector1_list[i] != selector2_list[i]:
                same_list = selector1_list[0: i]
                different = selector1_list[i]
                if different.find('[') > 0:
                    same = different[0: different.find('[')]
                    same_list.append(same)
                return '/'.join(same_list)
        return selector1


    def get_subitem_xpath(self, xpath, same_xpath):
        '''        
        :param xpath: 
        :param same_xpath: 
        :return: 
        '''
        if same_xpath in xpath:
            str = xpath[len(same_xpath):]
            if str.find('/') >= 0:
                return str[1 + str.find('/') : ]
            return ''
        return xpath


    def enable_open_sub_page(self, condition, content):
        if not condition:
            return True

        type = condition.get('type', '').lower()
        format = condition.get('format', '')
        value = condition.get('value', '')

        if type == 'date':
            base_strs = ["yyyy","MM","dd", "HH", "mm", "ss"]
            python_strs = ['%Y','%m', '%d', '%H', '%M', '%S']
            date_format = format
            for i in range(len(base_strs)):
                if date_format.find(base_strs[i]) >= 0:
                    date_format = date_format.replace(base_strs[i], python_strs[i])
            try:
                clockTime = datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
                contentTime = datetime.datetime.strptime(content, date_format)
                if clockTime > contentTime:
                    return False
            except Exception,e:
                return False

        elif type == 'number':
            try:
                contentValue = float(content)
            except:
                return False
            if format == '>':
                return contentValue > value
            if format == '>=':
                return contentValue >= value
            if format == '<':
                return contentValue < value
            if format == '>=':
                return contentValue <= value
            if format == '==':
                return contentValue == value
            if format == '!=':
                return contentValue != value

        elif type == 'string':
            return True if re.match(format, content) else False
        else:
            pass
        return True