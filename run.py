# -*- coding: utf-8 -*-

import subprocess

def require_box_name():
    box_name = raw_input('Please input box name: ')
    if box_name == '':
        print('box name needed!')
        require_box_name()
    else:
        check_box(box_name)

def check_box(box_name):
    output = subprocess.check_output(['vagrant', 'box', 'list'])
    boxes = output.split('\r\n')
    del boxes[-1]

    box_collector = []
    for box in boxes:
        box_split = box.split(' ')
        name = box_split[0]
        version = box_split[-1].replace(')', '')
        if name == box_name.strip():
            box_collector.append({'name': name, 'version': version})

    if len(box_collector) == 0:
        print('box name %s is not exists!' % box_name)
        require_box_name()
    elif len(box_collector) == 1:
        print('box name %s is the latest version' % box_name)
        require_box_name()
    else:
        confirm_remove(box_name, box_collector)

def confirm_remove(box_name, box_collector):
    confirmed = raw_input('do you want to remove past %s [y/n]? ' % box_name)
    if confirmed.lower() != 'y':
        exit()

    del box_collector[-1]
    for box in box_collector:
        command = 'vagrant box remove %s --box-version %s' % (box['name'], box['version'])
        print(command)
        result = subprocess.call(command, shell=True)
        if result == 0:
            print('done')

require_box_name()
