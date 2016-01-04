#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lxml import etree

def transform(xmlPath, xslPath):
  # read xsl file
  xslRoot = etree.fromstring(open(xslPath).read())

  transform = etree.XSLT(xslRoot)

  # read xml
  xmlRoot = etree.fromstring(open(xmlPath).read())

  # transform xml with xslt
  transRoot = transform(xmlRoot)

  # return transformation result
  return etree.tostring(transRoot)

if __name__ == '__main__':
  with open('index.html', 'w') as f:
    f.write(transform('output.xml', 'tohtml.xsl'))

  with open('transformed.xml', 'w') as f:
    f.write(transform('output.xml', 'toXML.xsl'))


