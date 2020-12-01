'''This plugin is to save POJO files'''

__author__ = 'ThatLousyGuy <thatlousyguy@outlook.com>'
__version__ = '0.6'

from visidata import *

class Cell: 
    def __init__(self, row, col):
        self.row = row
        self.col = col

def _get_rows(sheet, cols):
    for row in Progress(sheet.rows):
        yield [ Cell(row, col) for col in cols ]

def _cells_as_dict(cells):
    ret = {}
    for cell in cells:
        typedValue = cell.col.getTypedValue(cell.row)

        # Empty values are returned as TypedWrappers and their value is None
        if not (isinstance(typedValue, TypedWrapper) and typedValue.val is None):
            ret[cell.col.name] = typedValue
    return ret

def _uppername(name):
    ret = ''
    if len(name) > 0:
        ret = name[0].upper() + name[1:]
    return ret

def _lowername(name):
    ret = ''
    if len(name) > 0:
        ret = name[0].lower() + name[1:]
    return ret

def _singularname(name):
    '''Best-effort attempt at making a name singular or leaving it alone'''
    ret = name

    import re
    if re.compile('hildren$').match(name):
        ret = re.compile('hildren$').sub('hild', name)
    elif re.compile('sses$').match(name):
        ret = re.compile('sses$').sub('ss', name)
    elif re.compile('.+shes$').match(name):
        ret = re.compile('shes$').sub('sh', name)
    elif re.compile('ss$').match(name):
        ret = name
    elif (len(name) > 1) and (name[-1] is 's'):
        ret = name[:-1]
    
    return ret

def _pascalize(name):
    '''Best-effort attempt at making a name PascalCase'''

    import re
    parts = re.compile('[-_.]').split(name)
    ret = ''.join(_uppername(part) for part in parts if len(part) > 0)

    return ret

def _get_type_name_pair(key, value):
    typeStr = 'String'
    name = _lowername(key)

    if isinstance(value, int):
        typeStr = 'Integer'
    elif isinstance(value, float):
        typeStr = 'Double'
    elif isinstance(value, dict):
        typeStr = _uppername(key)
    elif isinstance(value, list):
        singularName = _singularname(key)
        childType = 'String'
        if len(value) > 0:
            childType = _get_type_name_pair(singularName, value[0])[0]
        typeStr = 'List<%s>' % _uppername(childType)

    return (typeStr, name)


@VisiData.api
def save_pojo(vd, path, *sheets):
    indentation = '    '
    with path.open_text(mode='w') as fp:
        for vs in sheets:
            for row in _get_rows(vs, vs.visibleCols):
                sheetName = _uppername(_pascalize(vs.name))
                fp.write('class %s {\n' % _uppername(sheetName))
                rowAsDict = _cells_as_dict(row)
                for (key, value) in rowAsDict.items():
                    typeNamePair = _get_type_name_pair(key, value)
                    fp.write('%sprivate %s %s;\n' % (indentation, typeNamePair[0], typeNamePair[1]))
                fp.write('}\n')
