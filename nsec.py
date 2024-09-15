import sys
import time
import lxml.etree as ET
import os
import argparse
import re
import json
import urllib2
verbose = 0
emitData = False
colorCells = False

gcc = 0

xflags = 0
SpecificTable = 0
SpecificRow = -1
SpecificCol = -1
drawBorders = False
traceit = False

etparser = ET.HTMLParser()

colormap = {"IndianRed": "#CD5C5C", "LightCoral": "#F08080",\
        "Salmon": "#FA8072", "DarkSalmon": "#E9967A",\
        "LightSalmon": "#FFA07A", "Crimson": "#DC143C",\
        "Red": "#FF0000", "FireBrick": "#B22222",\
        "DarkRed": "#8B0000", "Pink": "#FFC0CB",\
        "LightPink": "#FFB6C1", "HotPink": "#FF69B4",\
        "DeepPink": "#FF1493", "MediumVioletRed": "#C71585",\
        "PaleVioletRed": "#DB7093", "LightSalmon": "#FFA07A",\
        "Coral": "#FF7F50", "Tomato": "#FF6347",\
        "OrangeRed": "#FF4500", "DarkOrange": "#FF8C00",\
        "Orange": "#FFA500", "Gold": "#FFD700",\
        "Yellow": "#FFFF00", "LightYellow": "#FFFFE0",\
        "LemonChiffon": "#FFFACD", "LightGoldenrodYellow": "#FAFAD2",\
        "PapayaWhip": "#FFEFD5", "Moccasin": "#FFE4B5",\
        "PeachPuff": "#FFDAB9", "PaleGoldenrod": "#EEE8AA",\
        "Khaki": "#F0E68C", "DarkKhaki": "#BDB76B",\
        "Lavender": "#E6E6FA", "Thistle": "#D8BFD8",\
        "Plum": "#DDA0DD", "Violet": "#EE82EE",\
        "Orchid": "#DA70D6", "Fuchsia": "#FF00FF",\
        "Magenta": "#FF00FF", "MediumOrchid": "#BA55D3",\
        "MediumPurple": "#9370DB", "RebeccaPurple": "#663399",\
        "BlueViolet": "#8A2BE2", "DarkViolet": "#9400D3",\
        "DarkOrchid": "#9932CC", "DarkMagenta": "#8B008B",\
        "Purple": "#800080", "Indigo": "#4B0082",\
        "SlateBlue": "#6A5ACD", "DarkSlateBlue": "#483D8B",\
        "MediumSlateBlue": "#7B68EE", "GreenYellow": "#ADFF2F",\
        "Chartreuse": "#7FFF00", "LawnGreen": "#7CFC00",\
        "Lime": "#00FF00", "LimeGreen": "#32CD32",\
        "PaleGreen": "#98FB98", "LightGreen": "#90EE90",\
        "MediumSpringGreen": "#00FA9A", "SpringGreen": "#00FF7F",\
        "MediumSeaGreen": "#3CB371", "SeaGreen": "#2E8B57",\
        "ForestGreen": "#228B22", "Green": "#008000",\
        "DarkGreen": "#006400", "YellowGreen": "#9ACD32",\
        "OliveDrab": "#6B8E23", "Olive": "#808000",\
        "DarkOliveGreen": "#556B2F", "MediumAquamarine": "#66CDAA",\
        "DarkSeaGreen": "#8FBC8B", "LightSeaGreen": "#20B2AA",\
        "DarkCyan": "#008B8B", "Teal": "#008080",\
        "Aqua": "#00FFFF", "Cyan": "#00FFFF",\
        "LightCyan": "#E0FFFF", "PaleTurquoise": "#AFEEEE",\
        "Aquamarine": "#7FFFD4", "Turquoise": "#40E0D0",\
        "MediumTurquoise": "#48D1CC", "DarkTurquoise": "#00CED1",\
        "CadetBlue": "#5F9EA0", "SteelBlue": "#4682B4",\
        "LightSteelBlue": "#B0C4DE", "PowderBlue": "#B0E0E6",\
        "LightBlue": "#ADD8E6", "SkyBlue": "#87CEEB",\
        "LightSkyBlue": "#87CEFA", "DeepSkyBlue": "#00BFFF",\
        "DodgerBlue": "#1E90FF", "CornflowerBlue": "#6495ED",\
        "MediumSlateBlue": "#7B68EE", "RoyalBlue": "#4169E1",\
        "Blue": "#0000FF", "MediumBlue": "#0000CD",\
        "DarkBlue": "#00008B", "Navy": "#000080",\
        "MidnightBlue": "#191970", "Cornsilk": "#FFF8DC",\
        "BlanchedAlmond": "#FFEBCD", "Bisque": "#FFE4C4",\
        "NavajoWhite": "#FFDEAD", "Wheat": "#F5DEB3",\
        "BurlyWood": "#DEB887", "Tan": "#D2B48C",\
        "RosyBrown": "#BC8F8F", "SandyBrown": "#F4A460",\
        "Goldenrod": "#DAA520", "DarkGoldenrod": "#B8860B",\
        "Peru": "#CD853F", "Chocolate": "#D2691E",\
        "SaddleBrown": "#8B4513", "Sienna": "#A0522D",\
        "Brown": "#A52A2A", "Maroon": "#800000",\
        "White": "#FFFFFF", "Snow": "#FFFAFA",\
        "HoneyDew": "#F0FFF0", "MintCream": "#F5FFFA",\
        "Azure": "#F0FFFF", "AliceBlue": "#F0F8FF",\
        "GhostWhite": "#F8F8FF", "WhiteSmoke": "#F5F5F5",\
        "SeaShell": "#FFF5EE", "Beige": "#F5F5DC",\
        "OldLace": "#FDF5E6", "FloralWhite": "#FFFAF0",\
        "Ivory": "#FFFFF0", "AntiqueWhite": "#FAEBD7",\
        "Linen": "#FAF0E6", "LavenderBlush": "#FFF0F5",\
        "MistyRose": "#FFE4E1", "Gainsboro": "#DCDCDC",\
        "LightGray": "#D3D3D3", "Silver": "#C0C0C0",\
        "DarkGray": "#A9A9A9", "Gray": "#808080",\
        "DimGray": "#696969", "LightSlateGray": "#778899",\
        "SlateGray": "#708090", "DarkSlateGray": "#2F4F4F",\
        "Black": "#000000"}

def getcolor(tdNode):
  rv = 0xffffff
  while True:
    bg = tdNode.get(bgcolor)
    if bg is None:
      tdNode = tdNode.getparent()
      continue
    if bg in colormap:
      bg = colormap[bg]
    if not (type(bg) is str):
      print "Strange type of background color", bg, type(bg)
    elif (bg.find("rgb(")==0):
      ns = list(map(int(re.findall(r"(\d+)", bg))))
      rv = ns[0]*0xffff + ns[1]*0xff + ns[2]
    elif bg[0] == '#':
      rv = int(bg[1:], 16)
    else:
      print "Strange bgcolor string", bg

#goodcolor = 0xdaf7a6  # light green
#badcolor = 0xffc0cb  # pink
#goodcolorStr = "greenyellow"  # ADFF2F
goodcolorStr = "#DDFF5F"  # ADFF2F
badcolorStr = "pink"  # pink
     
class matchText:
  def __init__(self, text, val = None):
      ''' text is the text to match. val, is going to be appended to make dim value
          missing val implies:  same as text. um0 as val implies : no val'''
      self.text = text
      if (val == None):
        val = text # if None, 
      self.val = val


def isNumber(str, rvn=None):
  ds = " 01234567890%().,-%"  # allowed chars
  dg = "01234567890"         # must have one of these
  num = ""
  sign = 1
  rv = False
  idx = 0
  hasDot = False
  ispercent = False
  for c in str:
    idx = idx + 1
    isPercent = (c == '%')
    if (c == '$') and (idx == 1):
      # $ in first col is OK
      continue
    if not(c in ds):
      return False
    if (c == '(' or c == '-'):
      sign = -1
    if (c in dg):
      rv = True
      num = num + c
    elif c == '.':
      num = num + c
      if hasDot:
        return False
      hasDot = True
  if rvn and rv:
    rvn[1] = isPercent
    if hasDot:
      rvn[0] = float(num) * sign
    else:
      rvn[0] = int(num) *sign
  return rv

def getNumber(str):
  n = str.find('%')
  if (n > 0):
    str = str[:n]
  try:
    n = int(str)
  except:
    n = -1
  return n

class cellRange:
  def __init__(self, start, end):
    self.cellStart = start
    self.cellEnd = end
    self.cellCount = 1
  def incr(self):
    self.cellCount = self.cellCount + 1
  def __repr__(self):
    return str(self.cellCount)

def findPeaks(stats):
  ''' find peaks in a statistics list '''
  res = []
  cur = stats[0]
  goingDown = False
  k = 0
  for i in stats:
    #print "findPeaks ", k, cur, i, goingDown
    if i == cur:
      k = k + 1
      continue
    if i < cur:
      if not goingDown:
        res.append(k-1)
        #print "peak ", k-1
      goingDown = True
    else:
      goingDown = False
    cur = i
    k = k + 1
  return res

def isIn(lst, s, e):
  ri = 0
  for i in lst:
    if (i >= s) and (i <= e):
      return ri
    ri = ri + 1
  return -1

def addThem(a, b):
  if (a == ""):
    return b
  if (b == ""):
    return a
  return a + ' ' + b

class cellElt:
  def isCellElt(self):
    return "isCellElt"
  def __init__(self, tdNode):
    self.tdNode = tdNode
    self.width = None # width in percentage
    self.start = None # start in percentage
    self.isNumber = False
    self.text = None  # if any
    self.number = None  # if any
    self.isPartOfHeader = False
    self.colspan = 1
    self.rowNum = -1
    self.colNum = -1
    self.startColNum = -1
    self.endColNum = -1
    self.isPercent = False
    self.realColIdx = -1 # if >= 0, this is the non-last cell of a colspan>1 cell. 
                         # realColIdx is the idx of last cell 
  def __repr__(self):
    ci = "cell[%d,%d]" % (self.rowNum, self.colNum)
    if self.text is not None:
      ci = ci + '"' + self.text.encode('utf-8') + '"'
    if traceit:
      print "ci type is ", type(ci)
    return ci
def remove160(str):
  if str is None:
    return ""
  yt = ""
  str = str.strip('\n ')
  skpb = False
  for c in str:
    if skpb and c == ' ':
      continue
    skpb = False
    if (ord(c) == 10):
      c = ' '#  space TODO: remove leading blanks
      skpb = True
    if (ord(c) == 160):
      c = ' '#  space
    yt = yt + c
  return yt.strip('\n')

def getTextOfTd(tdn):
  cet = ""
  for y in tdn.iter():
    yt = remove160(y.text)
    cet = addThem(cet, yt)
    yt = remove160(y.tail)
    cet = addThem(cet, yt)
  if cet == ' ':
    cet = ''
  return cet

def findPeakCell(row, num):
  for c in row:
      if (c.width == None):
        continue
      if (c.start <= num and (c.start + c.width) > num):
          return c.colNum
  return -1

def joinCname(s1, s2):
  s1 = s1.strip()
  s2 = s2.strip()
  if (s1 == ''):
    return s2
  if (s2 == ''):
    return s1
  return s1 + ' ' + s2


def setTD(tdn, attr, val):
  try:
    tdn.set(attr, val)
  except:
    print 'FAILED TO SET "{:}", "{:}"'.format(attr, val)
    vl = ""
    vll = []
    for c in val:
      o = ord(c)
      vll.append(o)
      if (c == '"'):
        vl = vl + '&#' + str(o) + ';'
      elif o == 160:
        vl = vl + ' ' # no break space
      elif (o >= 32 and o <= 127):
        vl = vl + c
      else:
        vl = vl + '&#' + str(o) + ';'
      #print 'c =', c, ' ty=', type(c), ' ord=', ord(c)
    print 'FAILED TO SET vl=', vl
    tdn.set(attr, vl)
  gv = tdn.get(attr)

def changeCol(s, tagName, colVal):
  si = s.lower().find(tagName)
  if si >= 0:
    sheader = s[:si]
    stail = s[si:]
    se = stail.find(';')
    if se >= 0:
      stail = stail[se:]
      return sheader + tagName + colVal + stail
    else:
      return sheader + tagName + colVal
  return s

def hasClass(tdn):
  ''' return True if any node has a 'class=' attribute '''
  for y in tdn.iter():
    if y.get("class"):
      return True
  return  False

def newsetColor(tdn, colVal, isTop = True):
  ''' set color of contents of td.
  1) if the node has a background color, change it
  2) if the node has a 'class' attribute, move its contents 
     below a <span> node with color.
  return True if everything under the node has been changed if needed
  '''
  beforeS = ET.tostring(tdn)

  if isTop:
    setTD(tdn, "bgcolor", colVal)

  needToColor = False
  if tdn.text is not None:
    needToColor = True
  if tdn.tail is not None:
    needToColor = True
  for q in tdn:
    if not newsetColor(q, colVal, False):
      needToColor = True

  if not needToColor:
    return True

  s = tdn.get("style")
  c = tdn.get("class")
  if (s is None) and (c is None) and (not isTop):
    return False # let a higher node handle it

  ss = s
  if s is not None:
    s = changeCol(s, "background-color:", colVal)
    s = changeCol(s, "background:", colVal)
    if (s != ss):
      if (verbose > 4):
        print "Changed Style from ", ss, " to ", s
      tdn.set("style", s)
      return True

  if (c is None) and not isTop:
    t = tdn.text
    if (t is not None) and (t.strip() != ""):
      return False
    t = tdn.tail
    if (t is not None) and (t.strip() != ""):
      return False
    if (len(tdn) > 0):
      return False
    return True # was empty node

  # isTop or (s in not None). Need to insert

  #spnode = ET.fromstring('<span style="background:{:}"></span>'.format(colVal), etparser)
  spnode = ET.Element("span")
  spnode.set("style", "background:{:}".format(colVal))
  spnode.text = tdn.text
  spnode.tail = tdn.tail
  for q in tdn:
    spnode.append(q)
  for q in tdn:
    tdn.remove(q)
  tdn.append(spnode)
  tdn.text = None
  tdn.tail = None
  if (verbose > 4):
    print "Changed TDN'"+ beforeS+ '" to "'+afterS+'"'
  return True

def setColor(tdn, colVal):
  # set color
  if (xflags & 4) == 0:
    tdx = ET.tostring(tdn)
    print tdx
    if tdx.find("38,215") >= 0:
      print "Here"
    newsetColor(tdn, colVal, True)
    return
  s = tdn.get("style")
  ss = s
  if not (s is None):
    s = changeCol(s, "background-color:", colVal)
    s = changeCol(s, "background:", colVal)
    if (s != ss):
      if (verbose > 4):
        print "Changed Style from ", ss, " to ", s
      tdn.set("style", s)
  setTD(tdn, "bgcolor", colVal)

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July'] + \
         ['August', 'Septemper','October', 'November', 'December'] + \
         ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'June', 'Jul'] + \
         ['Aug', 'Sep','Oct', 'Nov', 'Dec', 'Sept']
def endsInAMonth(str):
  sl = len(str)
  for m in months:
    sm = len(m)
    if (sl >= sm and m == str[sl-sm:]):
      return True
  return False


def endsInADate(str):
  ''' Return A triple of <True,s1,n2> if this str ends in a date, such as "Mar 31", 
      where n2 is the numeric tail as an integer and s1 is the string before it '''
  sl = len(str)
  i = sl-1
  while (i >= 0 and str[i] in '0123456789'):
    i = i - 1
  if (i == (sl-1)):
    return False # no date found
  n1 = int(str[i:])
  sp = str[:i] # part before the number
  sp = sp.strip()  # remove blanks
  return endsInAMonth(sp)

def makesAValidDate(str1, str2):
  ''' return True if str2 is an year number and str1 ends in a date, optionally 
      followed by a comma, so that the two will makea date together. This function can 
      be made more smart by adding more rules'''
  if str1 == '':
     return False
  try:
    yn = int(str2)
    if (yn < 1900 or yn > 2999):
      return False
  except:
    return False
  # str2 is a valid year
  sl = len(str1)
  try:
    ssl = str1[sl-1]
  except:
    print "str1='{:}'".format(str1)
  if (str1[sl-1] == ','):
    # str1 ends in a ,. Trim it
    sl = sl - 1
    str1 = str1[:sl]
  if endsInADate(str1):
    return True
  return False

class cheader:
  def __init__(self, text, nRows, tag):
    self.text = text
    self.nRows = nRows
    self.tag = tag
    # nRows is the count od rows that have been consumed by this header. This header
    # if not a valid header for for all rows below that; numbered rRows and higher. It
    # is not a valid header for row (nRows-1) but can be saved for use on cells below.
  def __repr__(self):
    return "HDR('%s',%d,%s)"%(self.text.encode('utf-8'),self.nRows, self.tag)

def nodeHasWidth(tdn):
  w = tdn.get("width")
  if w:
    return w
  # see if it has style="width:20%;"
  s = tdn.get("style")
  if s is None:
    return None
  wi = s.find("width:")
  if (wi < 0):
    # no width in style
    return None
  s = s[wi+6:]
  # remove ; or %
  wi = s.find('%')
  if (wi >= 0):
    s = s[:wi]
  wi = s.find(';')
  if (wi >= 0):
    s = s[:wi]
  try:
    wi = int(s)
    return s
  except:
    # could not find an integer
    return None

def buildRe(l, s):
  l.append(re.compile(".*("+s+')'))

def initMatcher():
  months = []
  months = months + ["january","february","march","april","june","july","august"]
  months = months + ["september","october","november","december"]
  months = months + ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
  ms = ""
  s = "("
  #print "months = ", months
  for m in months:
    ms = ms + s + m
    s = '|'
  ms = ms+')'

  ds = "([1-9]|[12][0-9]|3[01])"
  ys = "(19|20|21)[0-9][0-9]"

  res = []

  buildRe(res, "%s %s, %s"%(ms, ds, ys))  # mar 31, 2016
  buildRe(res, "quarter %s"%(ys))  # quarter year
  buildRe(res, "[1-4]q[0-9]{2,4}") # 1q2015 or 1q15
  return res  # returns a list of compiled reg expressions

rexs = initMatcher()

def looksLikeHeader(s):
  s = s.lower() # we only match lower case strings
  for r in rexs:
    if r.match(s):
      if (verbose > 2):
        print "looksLikeHeader('{:}') is TRUE".format(s.encode('utf-8'))
      return True
  if (verbose > 2):
    print "looksLikeHeader('{:}') is FALSE".format(s.encode('utf-8'))
  return False

def findRowHeader(row, upto):
    for c in row[:upto]:
      if c.text == None:
        continue
      if c.text == '':
        continue
      return c.text
    return "???"
def selectH(h1, h2):
    if (h1 is None):
      return h2
    if h2 is None:
      return h1
    if len(h2.text) > len(h1.text):
      return h2
    return h1
def isOnlyPercent(s):
  return s.strip() == '%'

class ATable:
  def isLeftMostCell(self, pcell):
    if pcell.colNum == 0:
      return True
    cl = self.cells[pcell.rowNum]
    for cell in  cl[:pcell.colNum]:
      if cell.tdNode == None:
        continue  # this is a placeholder cell
      ct = cell.text
      if (not ct is None) and (ct != ''):
        return False
    return True
  def __init__(self, tableNode, name, num):
    self.num = num
    self.tableNode = tableNode
    #tableNode.insert(0, ET.fromstring("<caption>VDVC-TABLE-"+str(num)+"</caption>"))
    tableNode.set("vdvctbl", str(num))
    if drawBorders:
      tableNode.set("border", "1")
    self.name = name
    self.cells = [] # A two dimensional list of cellElt
    self.someHasWidths = False # tentative
    self.allHaveWidths = True  # tentative
    self.stats = [] # an array of size 100 showing how many numbers are in each line
    self.statsb = [] # Similar, but treat each number as filling the whole cell
    self.peaks = []
    self.peaksb = []
    self.rowWithWidths = -1
    #self.jsonDict = {}
    #self.jsonDict["name"] = name
    self.jsonCells = []  # a list of lists, in row major way
    #self.jsonDict["cells"] = self.jsonCells
    self.headerRows = -1 # if >=0 this is the number of rows of headers
                         # it is deduced by looking for empty cells at top left

  def detectHeaderRows(self):
    ''' if the top of the leftmost column has some empty cells, potentially folowed by a cell
        starting with '$ in ' '''
    # first count empty cells in leftmost column
    nempty = -1
    pcell = None
    for row in self.cells:
      pcell = row[0]
      ptext = pcell.text
      if not((ptext is None) or (ptext == '')):
        nempty = pcell.rowNum
        break
    if nempty < 0:
      # all cells in the leftmost row are empty
      return
    self.headerRows = nempty
    ptext = ptext.lower() # lower case tests below
    if '$ in' in ptext:
      self.headerRows = nempty+1
    elif 'dollars in' in ptext:
      self.headerRows = nempty+1
    elif 'in million' in ptext:
      self.headerRows = nempty+1
    elif 'in thousand' in ptext:
      self.headerRows = nempty+1
    elif '(millions' in ptext:
      self.headerRows = nempty+1
      
  def FCH1(self, pcell, useWidth):
    start = pcell.start
    width = pcell.width
    if useWidth:
      return None
    # say self.headerRows is 4. this can not serve as headers of rows 0,1,2 and 3.
    if self.headerRows > pcell.rowNum:
      return None
    txt = ""
    trn = 0 # text in upto this row has been appended to txt
    if verbose > 3:
      print "       fch1({:},{:},{:})".format(start, width, pcell.rowNum)
    for row in self.cells[:self.headerRows]:
      rn = row[0].rowNum
      if not useWidth:
        # find corresponding column by number
        if len(row) <= pcell.colNum:
          continue # this row does not have enough cells
          #print "Blowing up on ", pcell, " rl=", len(row), " row = ", row
        hcell = row[pcell.colNum]
        if hcell.realColIdx >= 0:
          hcell = row[hcell.realColIdx]
        if hcell.start == 0:
          # this cell starts from leftmost. Can not be a column header
          continue
        htext = hcell.text
        if (htext is None) or (htext == ''):
          continue
        #if (hcell.width is None):
        #  continue
        txt = joinCname(txt, htext)
        continue
      for hcell in row:  # TODO break once past the range
        if hcell.start == 0:
          # this cell starts from leftmost. Can not be a column header
          continue
        htext = hcell.text
        if (htext is None) or (htext == ''):
          continue
        if (hcell.width is None):
          continue
        if (hcell.start + hcell.width) <= start :
          continue  # non overlapping
        if (start+width) <= hcell.start:
          continue  # non overlapping
        txt = joinCname(txt, htext)
    return cheader(txt, rn+1, "FCH1")

  def FCH2(self, pcell, useWidth, onlyLLH):
    ''' returns a cheader. This function simply concatenates top cells of the columns
        and checks whether they 'look like a header' 
        useWidth flag tells it to look for header columns via width, as opposed to via 
        column numbers.
        onlyLLH, if false, ignores looksLikeHeader test'''
    start = pcell.start
    width = pcell.width
    rown = pcell.rowNum
    if useWidth:
      return None
    txt = ""
    trn = 0 # text in upto this row has been appended to txt
    if verbose > 3:
      print "       FCH2({:},{:},{:})".format(pcell, useWidth, onlyLLH)
    hr = rown+1   # how many rows to consider for header. Note that we are considering
                  # the current row as header as well. If a header is found using current
                  # row, the current cell is not a data cell, but the header is a valid
                  # header for all cells below it.
    if hr > 20:
      hr = 20      # we will consider at most this many rows
    hasNumber = False
    textAboveNumber = None
    rowForTBN = -1
    candidate = None
    for row in self.cells[:hr]:
      rn = row[0].rowNum
      # first make alist of cells in this row that will participate in this header.
      # with useWidth, these are all cells that overlap the width of the target cell
      # without useWidth, this is the cell of the given column number, considering colspan
      participatingCells = []
      if not useWidth:
        # find corresponding column by number
        if len(row) <= pcell.colNum:
          continue # this row does not have enough cells
        hcell = row[pcell.colNum]
        if (candidate is not None) and hcell.isNumber:
          #after finding a candidate, do not allow numbers
          continue
        if hcell.realColIdx >= 0:
          hcell = row[hcell.realColIdx]
        participatingCells.append(hcell)
      else:
        for hcell in row:
          if (hcell.start + hcell.width) <= start :
            continue  # non overlapping
          if (start+width) <= hcell.start:
            continue  # non overlapping
          if (candidate is not None) and hcell.isNumber:
            #after finding a candidate, do not allow numbers
            continue
          if not (hcell.width is None):
            participatingCells.append(hcell)
      # Now go over these cells
      # given a number in row R
      #   if looksLikeHeader(header-above-R) take it
      #   if looksLikeHeader(header-upto-and-including-R) take it
      if verbose > 3:
          print "          fhc2 R{:} participatingCells ={:}".format(rn, participatingCells)
      for hcell in participatingCells:
        if hcell.startColNum == 0:
          if verbose > 3:
            print "            fhc2 leftmost ", hcell
          continue
        htext = hcell.text
        if (htext is None) or (htext == ''):
          continue
        if hcell.isNumber:
          if textAboveNumber is None:
            textAboveNumber = txt
            rowForTBN = rn
            if verbose > 3:
              print "            fhc2 {:} TBN'{:}'{:}".format(hcell, textAboveNumber.encode('utf-8'), rowForTBN)
        txt = joinCname(txt, htext)
        if verbose > 3:
          print "            fhc2 {:} txt='{:}'".format(hcell, txt.encode('utf-8'))
        if looksLikeHeader(txt):
          if verbose > 3:
            print "            fhc2 {:} LLH txt='{:}'".format(hcell, txt.encode('utf-8'))
          candidate = cheader(txt, rn+1, "FCH2a")
          continue
        if verbose > 3:
          print "            fhc2 {:} !LLH txt='{:}'".format(hcell, txt.encode('utf-8'))
    if candidate is not None:
      return candidate
    if (onlyLLH == False) and not (textAboveNumber is None):
      if verbose > 3:
        print "          fhc2 Returning TBN'{:}'{:}".format(textAboveNumber.encode('utf-8'), rowForTBN)
      return cheader(textAboveNumber, rowForTBN, "FCH2b")
    return None   



  def findColumnHeader(self, pcell):
    ''' returns a cheader. This function uses multiple algorithms to figure out what the
        header could be, and returns the largest. We could enhance this routine to try
        multiple algorithms as needed '''

    # see if the top left cells were empty. If they were, the corresponding cells above
    # coluumns could be header
    if verbose > 3:
      print "---findColumnHeader ",pcell
    h1 = None
    if (self.headerRows > 0) and (self.headerRows <= pcell.rowNum): 
      h1 = self.FCH1(pcell, False)
      if h1 and (verbose > 3):
        #traceit = True
        #print "h1ty = ", h1.isCellElt()
        #print "h1ty = ", type(h1)
        #sh1 = str(h1)
        #traceit = False
        #print "---... FCH1(False) ",type(sh1)
        print "---... FCH1(False) ",h1

    if (self.headerRows > 0) and (self.headerRows <= pcell.rowNum):
      h2 = self.FCH1(pcell, True)
      if h2 and (verbose > 3):
        print "---... FCH1(True) ",h2
      h1 = selectH(h1, h2)

    # The next algorithm concatenates top few cells to see it they look like a header
    for b1 in [False, True]:
      for b2 in [False, True]:
        h2 = self.FCH2(pcell, b1, b2)
        if h2 and (verbose > 3):
          print "---... FCH2({:}, {:}) {:}".format(b1, b2, h2)
        h1 = selectH(h1, h2)

    if (verbose > 3):
      print "---... returning ",h1
    return h1

  def collectJdict(self, tdDict, rowNum, colNum):
    jc = self.jsonCells
    while rowNum >= len(jc): jc.append([])
    rc = jc[rowNum]
    while colNum >= len(rc): rc.append({})
    rc[colNum] = tdDict

  def perCellProcess(self):
    ''' In this algorithm, we ignore the concept of peaks. Instead we loof for colimn names for
        each cell separately. It is more expensive, but more robust. '''
    cheaders = {}
    for row in self.cells:
      if (self.headerRows > 0) and (row[0].rowNum < self.headerRows):
	 continue
      cellidx = -1
      for pcell in row:
	cellidx = cellidx + 1
        if pcell.colNum == 0:
          continue
        if not pcell.isNumber:
          continue
        if (SpecificRow >= 0 and SpecificRow != pcell.rowNum):
          continue
        if (SpecificCol >= 0 and SpecificCol != pcell.colNum):
          continue
        key=str(pcell.start) + ':' + str(pcell.start+pcell.width-1)
        if verbose > 2:
            print "\n    PerCellProcess r{:} c{:} s={:} w={:} key={:} text={:}".format(pcell.rowNum, pcell.colNum, pcell.start, pcell.width, key, pcell.text)
        tdn = pcell.tdNode
        if key in cheaders:
          h = cheaders[key]
        else:
          # this key has not been seen
          h = self.findColumnHeader(pcell)
          if (h is None) or (h.nRows < 0):
            # could not find header. Print that
            print "??? Could not find column header of cell at row{:} col{:} '{:}'".format(pcell.rowNum, pcell.colNum, pcell.text)
            setColor(tdn, badcolorStr)
            continue
          cheaders[key] = h
          if verbose > 2:
              print "    PerCellProcess ='{:}'/{:}".format(h.text.encode('utf-8'), h.nRows)
        if (pcell.rowNum < h.nRows):
          # this number is part of column header. ignore
          setColor(tdn, badcolorStr)
          continue
        # now we have a cell and its headers
        #allTDs.append(tdn)
        #setTD(tdn, "vdvcr", row[0].text)
        if (h.text == '') and self.isLeftMostCell(pcell) :
          continue
        rowHeader = findRowHeader(row, pcell.colNum)
	tdDict = {}
        if (verbose > 0):
	  print("SETTDDTCT 1 -----------------")
        setTD(tdn, "vdvcr", rowHeader)
	tdDict["row"] = rowHeader
        setTD(tdn, "vdvcc", h.text)
	tdDict["col"] = h.text
        ns = str(pcell.number)
        if (pcell.isPercent):
          ns = ns + '%'
        elif (not ('$' in ns)) and (cellidx > 0) and (row[cellidx-1].text == '$'):
          ns = '$' + ns 
        setTD(tdn, "vdvcv", ns)
	tdDict["value"] = ns
	tdDict["rowNum"] = pcell.rowNum
	tdDict["colNum"] = pcell.colNum
        setTD(tdn, "vdvcrn", str(pcell.rowNum))
        setTD(tdn, "vdvccn", str(pcell.colNum))
	self.collectJdict(tdDict, pcell.rowNum, pcell.colNum)
	#self.jsonCells.append(tdDict)
	if h.text == '':
          setColor(tdn, badcolorStr)
        else:
          setColor(tdn, goodcolorStr)
        if h.text == '':
          print '???DATA("{:}","{:}") = "{:}" {:}/{:}'.format(rowHeader.encode('utf-8'), h.text, pcell.text, pcell.rowNum, pcell.colNum)
        elif (emitData or verbose > 0):
          print 'DATA("{:}","{:}") = "{:}"'.format(rowHeader.encode('utf-8'), h.text.encode('utf-8'), pcell.text.encode('utf-8'))

  def parseTable(self):
    rowWithWidths = None
    for j in range(101):
      self.stats.append(0)
      self.statsb.append(0)
    t = self.tableNode
    t0 = t[0]
    if t0.tag == 'tbody':
      t = t0
    allCells = {}
    nl = [0, False]
    for i in range(len(t)):
      rowHasWidths = True
      re = t[i]
      if (re.tag != "tr"):
	print "#### ERROR non-tr under table: "+re.tag
	continue
      cl = [] # cells list
      self.cells.append(cl)
      if (verbose > 0):
        global gcc
        if (verbose > 1):
          print '\nRow ',i, ' (',gcc, ')'
        gcc = gcc + 1
      # first make a list of cellElt, accounting for colspan sttribute
      for j in range(len(re)):
        tdNode = re[j]
        if (tdNode.tag != "td"):
          print "#### ERROR non-td under table"
        cs = tdNode.get("colspan")
        cet = getTextOfTd(tdNode)
        csn = 1

        ce = cellElt(tdNode)
        #print "TYpe ce = ", type(ce)
        ce.startColNum = len(cl)
        ce.endColNum = len(cl)
        ce.colspan = csn
        if cs:
          csn = int(cs)
          rowHasWidths = False
          if csn > 1:
            ce.endColNum = len(cl) + csn - 1
            realColIdx = len(cl) + csn -1
            ce.realColIdx = realColIdx
            for csni in range(csn-1):
              #ce = cellElt(None)
              #ce.rowNum = i
              #ce.colNum = len(cl)
              #ce.text = cet
              cl.append(ce)
	#print "Cell-color = ", tdNode.get("bgcolor")
        ce.text = cet
        ce.rowNum = i
        ce.colNum = len(cl)
        if ce.colNum != ce.endColNum:
          print "############# BAD COLNUMS ", ce, ce.startColNum
          print ce.junk

        #print "cellNode[",ce.rowNum,',',ce.colNum, '] is ', ce, ce.tdNode
        cl.append(ce)

      # now process it
      start = 0
      lastCellNode = None
      cellNode = None
      for xcellNode in cl:
        lastCellNode = cellNode
        cellNode = xcellNode
        tdNode = cellNode.tdNode
        #print "cellNode[",cellNode.rowNum,',',cellNode.colNum, '].tdNode=', tdNode

        #print '@',i,'/',j,': cn=',cellNode, 'ac[][]=:',self.cells[i][j],': cl[j]=:',cl[j],':'
        #cellNode.rowNum = i
        j = cellNode.colNum 
        if cellNode.colspan != 1:
          # start is the start of the first cell of this colspan
          start = cl[j-(cellNode.colspan-1)].start # is colspan=2, cl[j-1]
        cellNode.start = start
        if tdNode == None:
          # this is a placeholder for tc with >1 colspan
          #print "cellNode[",cellNode.rowNum,',',cellNode.colNum, '] is empty'
          if rowWithWidths:
            #cellNode.deducedWidth = rowWithWidths[j].deducedWidth
            cellNode.width = rowWithWidths[j].width
            start = cellNode.width + cellNode.start
          #if verbose > 1:
          #    print '     col    {:2} ->{:}'.format(j,cellNode.realColIdx)
          continue
        #print "TDNODE{:}/{:} ========================= ".format(i,j), tdNode, cellNode
        #print ET.tostring(tdNode)

        cet = cellNode.text
        #w = tdNode.get("width")
        w = nodeHasWidth(tdNode)
        #wi = 0
        badw = ""
        if (w is None):
          # no width attribute.
          self.allHaveWidths = False
          rowHasWidths = False
          if rowWithWidths:
            if j >= len(rowWithWidths):
              print "Row overflow at j=",j,' len=', len(rowWithWidths)
              wn = 10
              badw = "RO"
            else:
              wn = rowWithWidths[j].width
              badw = "IW"
          else:
            wn = 10
            badw = "NW"
        else:
          wn = getNumber(w)
        if not wn:
          if (verbose > 1):
            print "wi= ", badw, ' j=', j
        cellNode.width = wn
        #print "cellNode[",cellNode.rowNum,',',cellNode.colNum, '].width set to', wn
        we = start+wn-1
        while (len(self.statsb) <= we):
          self.statsb.append(0)
        while (len(self.stats) <= we):
          self.stats.append(0)
        dkey = str(start)+":"+str(we)
        isn = 'notN'
        badDK = ""
        cellNode.isNumber = False
        if (isNumber(cet, nl)):
          isn = ' isN'
          cellNode.isNumber = True
          cellNode.number = nl[0]
          if nl[1]:
            cellNode.isPercent = True
          if dkey in allCells:
            allCells[dkey].incr()
          else:
            if rowWithWidths:
              badDK = "#BDK"
            allCells[dkey] = cellRange(start, we)
          for je in range(len(cet)):
            if not (((we-je) < 0 or (we-je)>=len(self.stats))):
              self.stats[we-je] = self.stats[we-je]+1
              # else print "Going to blow we=",we," je=",je," cet=",cet
          for je in xrange(start, start+wn):
            self.statsb[je] = self.statsb[je]+1
        elif (isOnlyPercent(cellNode.text)) and (lastCellNode) and (lastCellNode != cellNode) :
          lastCellNode.isPercent = True
        start = cellNode.start + wn
        if verbose > 1:
          cete = cet.encode('utf-8')
          if cete != "":
            cete = '"' + cete + '"'
          #print '     col  {:1}:{:2} {:4} {:2} {:5} {:20} {:10} {:}'.format(cellNode.colspan,j,w,wn,isn,cete,dkey,badw)
          #print '     col  {:1}:{:2} {:4} {:2} {:5} {:20} {:10} {:}'.format(j-cellNode.colspan+1,j,w,wn,isn,cete,dkey,badw)
          cetep = cete
          if cellNode == lastCellNode:
            cetep = "..... . ."
          print '     col  {:1}:{:2} {:4} {:2} {:5} {:20} {:10} {:}'.format(cellNode.startColNum,j,w,wn,isn,cetep,dkey,badw)
          #print "     col " , j, '/',ej, w, wn, isn, cete, dkey
      if rowHasWidths:
        rowWithWidths = cl
        wl = []
        for cnx in cl:
          wl.append(cnx.width)
        if (verbose > 1):
          print "rowWithWidths found " , len(rowWithWidths), ' widths=', wl

    self.detectHeaderRows()
    if verbose > 1:
      print "headerRows = ",self.headerRows

    if (xflags & 2) == 0:
      self.perCellProcess()
      return
    peaks = findPeaks(self.stats)
    peaksb = findPeaks(self.statsb)
    self.peaks = peaks
    self.peaksb = peaksb
    if verbose > 0:
            print "stats=", self.stats
            print "statsb=", self.statsb
            print "AllCells=", allCells
            print "peaks=", self.peaks
            print "peaksb=", self.peaksb
    #make columNames
    allTDs = []
    columnNames = []
    if (xflags & 1) == 0:
      upeaks = peaksb
    else:
      upeaks = peaks
    for j in upeaks:
      cname = ""
      nRows = len(self.cells)
      firstNumRow = None
      inHeader = True
      for row in self.cells:
        pidx = findPeakCell(row, j)
        if (pidx < 0):
          continue
        pcell = row[pidx]
        if pcell.text == None:
          continue
        ptext = pcell.text.encode('utf-8')
        if inHeader:
          if pcell.isNumber and not makesAValidDate(cname, ptext):
            inHeader = False
            columnNames.append(cname)
          else:
            cname = joinCname(cname ,ptext)
        if not inHeader:
          if pcell.isNumber:
            if (emitData or verbose > 0):
                print 'DATA("{:}","{:}") = "{:}" j={:}'.format(row[0].text.encode('utf-8'), cname, ptext, j)
            tdn = pcell.tdNode
            if tdn != None:
              allTDs.append(tdn)
	      tdDict = {}
              setTD(tdn, "vdvcr", row[0].text)
              if (verbose > 0):
	        print("SETTDDTCT 2 -----------------")
	      tdDict["row"] = row[0].text
              setTD(tdn, "vdvcc", cname)
	      tdDict["column"] = cname
              ns = str(pcell.number)
              if pcell.isPercent:
                ns = ns + '%'
              setTD(tdn, "vdvcv", ns)
	      tdDict["value"] = ns
	      tdDict["rowNum"] = pcell.rowNum
	      tdDict["colNum"] = pcell.colNum
              setTD(tdn, "vdvcrn", str(pcell.rowNum))
              setTD(tdn, "vdvccn", str(pcell.colNum))
	      #self.cellDict.append(tdDict)
	      self.collectJdict(tdDict, pcell.rowNum, pcell.colNum)
              setColor(tdn, goodcolorStr)
              #print "tdn=", ET.tostring(tdn)
              #print "TDNODE AFTER ========================= ", tdn, pcell, ET.tostring(tdn)
      # do the rest
        
parentDict = {}

def isCentered(x):
  k = 5
  while k > 0:
    if x.get('align') == 'center': return True
    if not (x in parentDict): return False
    x = parentDict[x]
    k = k -1
  return False


def findTables(htmFile):
  tree = htmFile.tree
  rv = []
  tc = 0
  ts = []
  maxts = 4
  for x in iter(tree.iter()):
    for y in x: parentDict[y] = x
    if x.tag == "table":
      tname = ' '.join(ts)
      tc = tc + 1
      at = ATable(x,tname, tc)
      at.htmFile = htmFile
      rv.append(at)
    if x.text:
      if isCentered(x):
	if len(ts) >= maxts : del ts[0]
        ts.append(x.text)
      else:
	ts = []

  return rv;

def isValidNumber(n):
  if n == '':
    return False
  for d in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
    if d in n:
      return True
  return False

class htmlFile:
  def __init__(self, tree):
    self.tree = tree
    self.styleNode = None


def matchTablesNew(htmf):
  ''' tree is a parsed tree. match is a tableMatch object. Match elements'''
  tables = findTables(htmf)
  allJson = []
  # tables is a list of tuples (tbl, tblname)
  #tc = 0
  for tx in tables:
    #tc = tc + 1
    #tx is an ATable
    if (SpecificTable != 0):
      if (tx.num != SpecificTable):
        continue
    if (verbose > 0):
      print "\n\n\nTABLE: ", tx, ' tc=', tx.num, tx.name.encode('utf-8')
    #print "t = ", t, len(t)
    # convert the table to list of lists for easy access
    tx.parseTable()
    if len(tx.jsonCells) > 0: 
	    allJson.append({"name":tx.name, "Cells" : tx.jsonCells})
  return {"Tables":allJson}


def findKid(tree, tag):
  for x in tree:
    if x.tag == tag:
      return x
  return None

class cssElt:
  ''' A Css element looks like tag[.name] {text}
      such as p{font:11}  or p.p12{font:12}
  '''
  def __init__(self, tag, name, text):
    self.tag = tag
    self.name = name
    self.text = text
  
def parseCss(csstxt):
  start = 0
  rv = []
  while True:
    tag = None
    name = None
    closingBrace = csstxt.find('}', start) # idx of closing brace
    if closingBrace < 0:
      return rv
    openingBrace = csstxt.find('{', start, closingBrace)
    tn = csstxt[start, openingBrace].strip()
    di = tn.find('.')
    if (di < 0):
      tag = tn[:di]
      name = tn[name+1:]
    else:
      tag = tn
      name = None
    rv.append(cssElt(tag, name, csstxt[openingBrace+1:closingBrace]))
    start = closingBrace + 1

def main(inp, pretty=None, outp=None, joutf=None):
  #parser = ET.HTMLParser()

  jtree = None
  jhead = None
  styleNode = None
  try :
    jst = open("outputattr.js", "r").read()
    jtree = ET.fromstring(jst, etparser)
    jhead = jtree.find("head")
    #print "JTREE = ", jtree
  except:
    jst = None

  #fp = open("a16-8475_18k.htm", "r")
  if inp.startswith("http:"):
    fp = urllib2.urlopen(inp)
  else:
    fp = open(inp, "r")
  bv = fp.read()
  fp.close()
  tree = ET.fromstring(bv, etparser)
  htmf = htmlFile(tree)
  hn = findKid(tree, 'head')
  #if not (hn is None):
  #  sn = findKid(hn, "style")
  #  htmf.styleNode = findKid(hn, "style")
  #  if not (sn is None):
  #    htmf.css = parseCss(sn.text)
  #print "tree = ", tree
  #print "tree.items = ", tree.items()
  #print (ET.tostring(tree, pretty_print=True))

  if not outp:
    emitData = True

  if pretty:
    op = open(pretty, "w")
    op.write(ET.tostring(tree,method="html",pretty_print=True))
    op.close()

  jout = matchTablesNew(htmf)
  if joutf is not None: 
    jfp = open(joutf, "w")
    json.dump(jout, jfp, indent=2)
    jfp.close()
  if outp:
    if not (jhead is None):
      he = tree.find("head")
      #print "HE WAS ", he
      if he is None:
	tree.insert(0,ET.fromstring("<head></head>"))
        he = tree.find("head")
	#print "HE is ", he
      if he is not None:
        for hee in jhead:
          he.append(hee)
    newstr = ET.tostring(tree,method="html",pretty_print=True)
    fp = open(outp, "w")
    fp.write(newstr)
    fp.close()

# -v verbose
# -i input.htm
# -p pretty-printed
# -o tagged output
# -x experimental flags
# --cs color cells
# -b add borders
# Basically for debugging a specific problem only
#   -sr specific row only
#   -sc specific column only
#   -t only process this table

parser = argparse.ArgumentParser(description = 'extract data from html')
parser.add_argument('-b', '--border', help='Draw Cell borders', action='store_true', default=False)
parser.add_argument('-cs', '--colorcells', help='Color cells', action='store_true', default=False)
parser.add_argument('-x', '--xflag', type=int, help='Internal test flags', default=0)
parser.add_argument('-sr', '--sprow', type=int, help='Choose Specific Row only', default=-1)
parser.add_argument('-sc', '--spcol', type=int, help='Choose Specific Column only', default=-1)
parser.add_argument('-t', '--table', type=int, help='Choose Specific Table', default=0)
parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='count', default=0)
parser.add_argument('input', type = str, help='Input html file or url')
parser.add_argument('-p', '--pretty', type=str, help='Generate pretty-printed input file', action='store')
parser.add_argument('-o', '--output', type=str, help='Tagged output file', action='store')
parser.add_argument('-jo', '--jsonoutput', type=str, help='Json output file', action='store')
args = parser.parse_args()
#print args
verbose = args.verbose
xflags = args.xflag
colorCells = args.colorcells
drawBorders = args.border
SpecificTable = args.table
SpecificRow = args.sprow
SpecificCol = args.spcol
#print "SpecificRow = ", SpecificRow
#print "SpecificCol = ", SpecificCol

# Current assignment of xflags
#   bit 1: if 1, use the old (number of digits) mechanism for detecting peaks
#          if 0: whole cell of the number contributes towards peaks

main(args.input, args.pretty, args.output, args.jsonoutput)

#
