import xml.sax

class PartXMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentData = ''
        self.isStructure = False
        self.row_name    = ''
        self.type        = ''

    def startElement(self, tag, attributes):
        self.currentData = tag
        if tag == 'table_structure':
            self.isStructure = True
            print '-------Table-------'
            print attributes['name']
            print '---'
        elif tag == 'table_data':
            self.isStructure = False
        elif tag == 'row':
            self.isStructure = False
        elif tag == 'field' and self.isStructure:
            self.row_name = attributes['Field']
            self.type = attributes['Type']

    def endElement(self, tag):
        if self.currentData == 'table_structure':
            self.isStructure = False
        elif self.currentData == 'field' and self.isStructure:
            print self.row_name + '   Type: ' + self.type

if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = PartXMLHandler()
    parser.setContentHandler(handler)
    parser.parse('new.xml')