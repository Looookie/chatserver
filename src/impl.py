#!/usr/bin/env python
#coding:utf-8
'''
Created on 2018年3月6日

@author: Luke
'''

from itertools import filterfalse, accumulate
import json



def table_to_dict_list(table):
    return [dict(zip(table[0], d)) for d in table[1:]]

def multiple_of_three(data):
    return filterfalse(lambda x: x % 3, data)

def pick_GlossTerm(data):
    return json.loads(data)['glossary']['GlossDiv']['GlossList']['GlossEntry']['GlossTerm']


def sort_and_distinct(data):
    return list(set(data))


def sort_by_amount(data):
    data.sort(key=lambda x: x.amount, reverse=True)
    return data

def multiply_func(num1, num2):
    return num1 * num2

def divide_func(num1, num2):
    return num1 / num2

def add_func(num1, num2):
    return num1 + num2

def subtract_func(num1, num2):
    return num1 - num2
    
calc_method_dict={
        'multiply': multiply_func,
        'divide': divide_func,
        'add': add_func,
        'subtract': subtract_func
    }
    

def calc(methodName, *args, **kwargs):
    return calc_method_dict[methodName](*args, **kwargs)

def trace_tree_depth(tree, depth):
    depth = depth + 1
    for temp_key in tree.keys():
        temp_value = tree[temp_key]
        yield [temp_key, depth]
        if isinstance(temp_value, dict):
            for j in trace_tree_depth(temp_value, depth):
                yield j

def find_deepest_child(tree):
    treeNodeDict = dict(trace_tree_depth(tree, 0))
    deepestChildDepth = 0
    deepsetChildKey = ''
    for key in treeNodeDict.keys():
        if treeNodeDict[key] > deepestChildDepth:
            deepestChildDepth = treeNodeDict[key]
            deepsetChildKey = key
    return deepsetChildKey

def trace_tree(tree):
    for temp_key in tree.keys():
        temp_value = tree[temp_key]
        if isinstance(temp_value, dict):
            if len(temp_value) >= 3:
                yield temp_key
            for j in trace_tree(temp_value):
                yield j

def find_nodes_that_contains_more_than_three_children(tree):
    return set(trace_tree(tree))

def trace_tree_by_child(tree, child, found):
    for temp_key in tree.keys():
        temp_value = tree[temp_key]
        if isinstance(temp_value, dict):
            if found or child == temp_key:
                yield len(temp_value)
                for j in trace_tree_by_child(temp_value, None, True):
                    yield j
            else:
                for j in trace_tree_by_child(temp_value, child, False):
                    yield j

def count_of_all_distributions_of_linux(tree):
    return sum(list(trace_tree_by_child(tree, 'Linux', False)))

class NociceMsg(object):
    def __init__(self, content):
        self.content = content
    def output(self, current_userid):
        return '<li class="notice">%s</li>' % (self.content)
    
class MessageMsg(NociceMsg):
    def __init__(self, content, userid):
        self.content = content
        self.userid = userid
    def output(self, current_userid):
        currentUserClass = 'left'
        if current_userid == self.userid:
            currentUserClass = 'right'
        return '<li class="%s">\n    <img class="profile" src="${user_image(%d)}">\n    <div class="message-content">%s</div>\n</li>' % (currentUserClass, self.userid, self.content)

def Notice(content):
    return NociceMsg(content)

def Message(content, userid):
    return MessageMsg(content, userid)

def render_messages(messages, current_userid):
    return '\n'.join(map(lambda x: x.output(current_userid), messages))


