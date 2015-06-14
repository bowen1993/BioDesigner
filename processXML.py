#! /bin/env python

def mainFunc():
    xml_file = open('new.xml', 'r')
    out_file = open('newnew.xml', 'w')
    for i, line in enumerate(xml_file.readlines()):
        print 'processing line %d' % i
        line = line.replace(';', '')
        line = line.replace('&gt', '')
        line = line.replace('&lt', '')
        line = line.replace('&', '')
        out_file.write(line)

if __name__ == '__main__':
    mainFunc()