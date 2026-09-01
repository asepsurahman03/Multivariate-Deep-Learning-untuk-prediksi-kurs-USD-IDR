import sys
sys.stdout.reconfigure(encoding='utf-8')
import zipfile
from lxml import etree

template_path = r'c:\Nusa Putra University\S2 Magister\Semester 2\Business Intellegence\Setelah UTS Cuy\template_IJIMAI_18_12_2025-OTH.docx'

with zipfile.ZipFile(template_path, 'r') as z:
    with z.open('word/styles.xml') as f:
        styles_content = f.read()
    with z.open('word/document.xml') as f:
        doc_content = f.read()

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# Parse styles
styles_tree = etree.fromstring(styles_content)
doc_tree = etree.fromstring(doc_content)

def get_style_props(style_id):
    style = styles_tree.find(f'.//w:style[@w:styleId="{style_id}"]', ns)
    if style is None:
        return f'Style {style_id} NOT FOUND'
    info = {}
    
    # Name
    name_el = style.find('w:name', ns)
    info['name'] = name_el.get(f'{{{ns["w"]}}}val') if name_el is not None else ''
    
    # Based on
    based = style.find('w:basedOn', ns)
    info['basedOn'] = based.get(f'{{{ns["w"]}}}val') if based is not None else ''
    
    # Para props
    pPr = style.find('w:pPr', ns)
    if pPr is not None:
        jc = pPr.find('w:jc', ns)
        info['align'] = jc.get(f'{{{ns["w"]}}}val') if jc is not None else ''
        spacing = pPr.find('w:spacing', ns)
        if spacing is not None:
            info['spaceBefore'] = spacing.get(f'{{{ns["w"]}}}before', '')
            info['spaceAfter'] = spacing.get(f'{{{ns["w"]}}}after', '')
            info['lineRule'] = spacing.get(f'{{{ns["w"]}}}lineRule', '')
            info['line'] = spacing.get(f'{{{ns["w"]}}}line', '')
        ind = pPr.find('w:ind', ns)
        if ind is not None:
            info['indLeft'] = ind.get(f'{{{ns["w"]}}}left', '')
            info['indRight'] = ind.get(f'{{{ns["w"]}}}right', '')
            info['indFirstLine'] = ind.get(f'{{{ns["w"]}}}firstLine', '')
            info['indHanging'] = ind.get(f'{{{ns["w"]}}}hanging', '')
        numPr = pPr.find('w:numPr', ns)
        if numPr is not None:
            info['numbering'] = True
        keepNext = pPr.find('w:keepNext', ns)
        info['keepNext'] = keepNext is not None
        outlineLvl = pPr.find('w:outlineLvl', ns)
        if outlineLvl is not None:
            info['outlineLevel'] = outlineLvl.get(f'{{{ns["w"]}}}val', '')
        
    # Run props
    rPr = style.find('w:rPr', ns)
    if rPr is not None:
        fonts = rPr.find('w:rFonts', ns)
        if fonts is not None:
            info['fontAscii'] = fonts.get(f'{{{ns["w"]}}}ascii', '')
            info['fontHAnsi'] = fonts.get(f'{{{ns["w"]}}}hAnsi', '')
            info['fontCs'] = fonts.get(f'{{{ns["w"]}}}cs', '')
        sz = rPr.find('w:sz', ns)
        if sz is not None:
            val = sz.get(f'{{{ns["w"]}}}val', '')
            info['fontSize'] = str(float(val)/2) + 'pt' if val else ''
        szCs = rPr.find('w:szCs', ns)
        if szCs is not None:
            val2 = szCs.get(f'{{{ns["w"]}}}val', '')
            info['fontSizeCs'] = str(float(val2)/2) + 'pt' if val2 else ''
        bold = rPr.find('w:b', ns)
        info['bold'] = bold is not None
        italic = rPr.find('w:i', ns)
        info['italic'] = italic is not None
        color = rPr.find('w:color', ns)
        info['color'] = color.get(f'{{{ns["w"]}}}val', '') if color is not None else ''
        caps = rPr.find('w:caps', ns)
        info['caps'] = caps is not None
        smallCaps = rPr.find('w:smallCaps', ns)
        info['smallCaps'] = smallCaps is not None
    
    return info

print('=' * 80)
print('TEMPLATE STYLE ANALYSIS')
print('=' * 80)

key_styles = [
    'Normal', 'Ttulo', 'Author', 'Member', 'Abstract', 'Keywords',
    'Ttulo1', 'Ttulo2', 'Ttulo3',
    'References', 'ReferenceHead',
    'TableTitle', 'FigureCaption0', 'FigureCaption',
    'Equation', 'Tablanormal'
]

for sid in key_styles:
    props = get_style_props(sid)
    print(f'\n--- {sid} ---')
    if isinstance(props, str):
        print(props)
    else:
        for k, v in props.items():
            if v and v != '' and v is not False:
                print(f'  {k}: {v}')

# Also check document body structure / page layout
print('\n\n' + '=' * 80)
print('DOCUMENT PAGE LAYOUT')
print('=' * 80)

body = doc_tree.find('.//w:body', ns)
sectPr = body.find('w:sectPr', ns)
if sectPr is not None:
    pgSz = sectPr.find('w:pgSz', ns)
    if pgSz is not None:
        w = pgSz.get(f'{{{ns["w"]}}}w', '')
        h = pgSz.get(f'{{{ns["w"]}}}h', '')
        orient = pgSz.get(f'{{{ns["w"]}}}orient', 'portrait')
        print(f'Page size: {int(w)/1440*2.54:.2f}cm x {int(h)/1440*2.54:.2f}cm ({orient})')
    
    pgMar = sectPr.find('w:pgMar', ns)
    if pgMar is not None:
        top = int(pgMar.get(f'{{{ns["w"]}}}top', 0))
        bottom = int(pgMar.get(f'{{{ns["w"]}}}bottom', 0))
        left = int(pgMar.get(f'{{{ns["w"]}}}left', 0))
        right = int(pgMar.get(f'{{{ns["w"]}}}right', 0))
        header = int(pgMar.get(f'{{{ns["w"]}}}header', 0))
        footer = int(pgMar.get(f'{{{ns["w"]}}}footer', 0))
        gutter = int(pgMar.get(f'{{{ns["w"]}}}gutter', 0))
        print(f'Margins (cm): top={top/1440*2.54:.2f}, bottom={bottom/1440*2.54:.2f}, left={left/1440*2.54:.2f}, right={right/1440*2.54:.2f}')
        print(f'Header={header/1440*2.54:.2f}cm, Footer={footer/1440*2.54:.2f}cm, Gutter={gutter/1440*2.54:.2f}cm')
    
    cols = sectPr.find('w:cols', ns)
    if cols is not None:
        num = cols.get(f'{{{ns["w"]}}}num', '1')
        space = cols.get(f'{{{ns["w"]}}}space', '720')
        print(f'Columns: {num}, space={int(space)/1440*2.54:.2f}cm')
        col_list = cols.findall('w:col', ns)
        for i, col in enumerate(col_list):
            cw = col.get(f'{{{ns["w"]}}}w', '')
            sp = col.get(f'{{{ns["w"]}}}space', '')
            print(f'  Col {i+1}: width={int(cw)/1440*2.54:.2f}cm, space={int(sp)/1440*2.54:.2f}cm' if cw else f'  Col {i+1}: auto')

# Check table normal style for borders
print('\n\n' + '=' * 80)
print('TABLE NORMAL STYLE - FULL XML')
print('=' * 80)
tbl_normal = styles_tree.find('.//w:style[@w:styleId="Tablanormal"]', ns)
if tbl_normal is not None:
    print(etree.tostring(tbl_normal, pretty_print=True).decode('utf-8'))

# Check Abstract style full XML
print('\n\n' + '=' * 80)
print('ABSTRACT STYLE - FULL XML')
print('=' * 80)
abs_style = styles_tree.find('.//w:style[@w:styleId="Abstract"]', ns)
if abs_style is not None:
    print(etree.tostring(abs_style, pretty_print=True).decode('utf-8'))

print('\nDone.')
