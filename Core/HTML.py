#!/usr/bin/python3
# -*-coding:UTF-8 -*

# ==========================================================================
class RootNode:
    """
    The Root Node class
    
    """
    
    # --- Constructor
    def __init__(self):

        self.children = []
        
# ==========================================================================   
class PairedNode:
    """
    The Paired Node class
    
    """
    
    # --- Constructor
    def __init__(self, parent, name, optv, optkv):

        self.parent = parent
        self.name = name
        self.optv = optv
        self.optkv = optkv
        self.children = []
     
# ==========================================================================
class SingleNode:
    """
    The Single Node class
    
    """
    
    # --- Constructor
    def __init__(self, parent, name, optv, optkv):

        self.parent = parent
        self.name = name
        self.optv = optv
        self.optkv = optkv
        
# ==========================================================================        
class TextNode:
    """
    The Text Node class
    
    """
    
    # --- Constructor
    def __init__(self, parent, content, decode=True):

        self.parent = parent
        self.content = content
        self.decode = decode
        
# ==========================================================================     
class HtmlTree:
    """
    The HtmlTree class
    
    """
    
    indent =  '  '
    opener = ('<', '>')
    closer = ('</', '>')
    singler = ('<', ' />')
    compact_build = False
    
    # ----------------------------------------------------------------------
    def __init__(self, spot):
        '''
        [HtmlTree] Constructor
        
        Defines the structure of the HtmlTree object
        
        Inputs:
            spot (Spot) The spot (for language handling)
        '''
        
        self.spot = spot
        self.Nodes = []
        self.Nodes.append(RootNode())
        
        self.text('root', '<!DOCTYPE html>', False)
        self.html = self.paired('root', 'html')
        self.head = self.paired(self.html, 'head')
        self.body = self.paired(self.html, 'body')
        self.ref = self.body
        
    # ----------------------------------------------------------------------
    def par2pos(self, parent):
        '''
        [HtmlTree].par2pos Convert parent to a parent/pos tuple
        
        Inputs:
            parent (int / tuple)  The parent/position identifier. parent can 
            be any positive integer or 'root'. If parent is a negative 
            integer, then it is considered as a relative position with 
            respect to the current reference.
            
        Output:
            A tuple (par, pos) where par is the parent's identifier and pos 
            the position in the parent's children list. If the element is to 
            append at the end of the children list, pos is None.
        '''
        
        if isinstance(parent, tuple):
            par = parent[0]
            pos = parent[1]
        else:
            par = parent
            pos = None
        
        if par=='root':
            par = 0
        elif par<=0:
            tmp = self.ref
            for i in range(-par):
                tmp = self.Nodes[tmp].parent
            par = tmp
            
        if pos=='root':
            pos = 0
            
        return (par, pos)
        
    # ----------------------------------------------------------------------
    def paired(self, parent, name, optv=(), optkv={}):
        '''
        [HtmlTree].paired Append a paired tag node
        
        Inputs:
            parent (int)  The parent identifier
            name (string) The name of the paired tag (div, span, ...)
            optv (tuple) All remaining single-value parameters
            optkv (dict) All remaining key-value parameters
            
        Output:
            The inserted node id (int)
        '''
        
        id = len(self.Nodes)
        P = self.par2pos(parent)
        
        # Append in the Node tree
        self.Nodes.append(PairedNode(P[0], name, optv, optkv))
            
        # Append to parent's children (to define position)
        if P[1] is None:
            self.Nodes[P[0]].children.append(id)
        else:
            self.Nodes[P[0]].children.insert(P[1], id)
            
        return id
    
    # ----------------------------------------------------------------------
    def single(self, parent, name, optv=(), optkv={}):
        '''
        [HtmlTree].single Append a single tag node
        
        Inputs:
            parent (int)  The parent identifier
            name (string) The name of the single tag (div, span, ...)
            optv (tuple) All remaining single-value parameters
            optkv (dict) All remaining key-value parameters
            
        Output:
            The inserted node id (int)
        '''
        
        id = len(self.Nodes)
        P = self.par2pos(parent)
        
        # Append in the Node tree
        self.Nodes.append(SingleNode(P[0], name, optv, optkv))
            
        # Append to parent's children (to define position)
        if P[1] is None:
            self.Nodes[P[0]].children.append(id)
        else:
            self.Nodes[P[0]].children.insert(P[1], id)
            
        return id
    
    # ----------------------------------------------------------------------
    def text(self, parent, content, decode=True):
        '''
        [HtmlTree].text Append a text node
        
        Inputs:
            parent (int)     The parent identifier
            content (string) The content of the text node
            
        Output:
            The inserted node id (int)
        '''
        
        id = len(self.Nodes)
        P = self.par2pos(parent)
        
        # Append in the Node tree
        self.Nodes.append(TextNode(P[0], content, decode))
            
        # Append to parent's children (to define position)
        if P[1] is None:
            self.Nodes[P[0]].children.append(id)
        else:
            self.Nodes[P[0]].children.insert(P[1], id)
  
        return id
    
    # ----------------------------------------------------------------------
    def build(self, id=0, level=0):
        '''
        [HtmlTree].build Builds the html tree
            
        Inputs:
            -
            
        Output:
            A string containing the html code.
            
        '''
        
        # --- Define node
        node =  self.Nodes[id]
        
        # --- Define indentation
        ind = ''
        if not self.compact_build:
            for i in range(level):
                ind += self.indent
        
        # --- Define output
        out = ''
        if node.__class__.__name__ == "RootNode":
            
            # -----------------------------
            #   ROOT
            # -----------------------------
            
            for i in node.children:
                out += self.build(id=i, level=level)
            
            
        elif node.__class__.__name__ == "PairedNode":
        
            # -----------------------------
            #   PAIRED TAG
            # -----------------------------
        
            out += ind + self.opener[0] + node.name
            for k,i in node.optkv.items():
                if k=="cls":
                    out += ' class="' + i + '"'
                else:
                    out += ' ' + k + '="' + i + '"'
            
            for i in node.optv:
                out += ' ' + i
            
            out += self.opener[1]
            
            if not self.compact_build:
                out += '\n'
            
            for i in node.children:
                out += self.build(id=i, level=level+1)
            
            out += ind + self.closer[0] + node.name + self.closer[1]
            
            if not self.compact_build:
                out += '\n'
            
        elif node.__class__.__name__ == "SingleNode":
        
            # -----------------------------
            #   SINGLE TAG
            # -----------------------------
        
            out += ind + self.singler[0] + node.name
            
            for k,i in node.optkv.items():
                if k=="cls":
                    out += ' class="' + i + '"'
                else:
                    out += ' ' + k + '="' + i + '"'
            
            for i in node.optv:
                out += ' ' + i
            
            out += self.singler[1]
            
            if not self.compact_build:
                out += '\n'
            
        elif node.__class__.__name__ == "TextNode":
            
            # -----------------------------
            #   FREE TEXT
            # -----------------------------
            
            out += ind + self.spot.mlt(node.content, node.decode)
            
            if not self.compact_build:
                out += '\n'
            
            
        return out    

# ==========================================================================     
class HTML(HtmlTree):
    """
    The HTML class
    
    """
    
    # ----------------------------------------------------------------------
    def __init__(self, spot):
        '''
        [HTMLH] Constructor
        
        Defines the HTML object
        
        Inputs:
            -
        '''
        
        HtmlTree.__init__(self, spot)
        
        # --- Meta tags
        self.meta(charset='UTF-8')
   
    # ==========================
    #   TAGS
    # ==========================
      
    # ----------------------------------------------------------------------
    def a(self, p, href, *optv, **optkv):
        optkv['href'] = href
        self.ref = self.paired(p, 'a', optv, optkv)
        return self.ref
    
    # ----------------------------------------------------------------------
    def br(self, p, num=1):
        for i in range(num):
            self.single(p, 'br')
        return 0
    
    # ----------------------------------------------------------------------
    def center(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'center', optv, optkv)
        return self.ref
    
    # ----------------------------------------------------------------------
    def div(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'div', optv, optkv)
        return self.ref
      
    # ----------------------------------------------------------------------
    def favicon(self, icon):
        optkv = {'rel': 'icon', 'href': icon}
        return self.single(self.head, 'link', (), optkv)
      
    # ----------------------------------------------------------------------
    def _file(self, p, *optv, **optkv):
        optkv['type'] = "file"
        return self.single(p, 'input', optv, optkv)
      
    # ----------------------------------------------------------------------
    def form(self, p, *optv, **optkv):
        optkv['method'] = "POST"
        self.ref = self.paired(p, 'form', optv, optkv)
        return self.ref
       
    # ----------------------------------------------------------------------
    def h1(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'h1', optv, optkv)
        return self.ref
        
    # ----------------------------------------------------------------------
    def h2(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'h2', optv, optkv)
        return self.ref
        
    # ----------------------------------------------------------------------
    def h3(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'h3', optv, optkv)
        return self.ref
        
    # ----------------------------------------------------------------------
    def h4(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'h4', optv, optkv)
        return self.ref
        
    # ----------------------------------------------------------------------
    def h5(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'h5', optv, optkv)
        return self.ref
        
    # ----------------------------------------------------------------------
    def h6(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'h6', optv, optkv)
        return self.ref
        
    # ----------------------------------------------------------------------
    def _hidden(self, p, name, value):
        return self.single(p, 'input', (), {'type': "hidden", 'name': name, 'value': value}) 
     
    # ----------------------------------------------------------------------
    def img(self, p, src, *optv, **optkv):
        optkv['src'] = src
        return self.single(p, 'img', optv, optkv)

    # ----------------------------------------------------------------------
    def javascript(self, script):
        optkv = {'language': "JavaScript"}
        id = self.paired(self.head, 'script', (), optkv)
        self.text(id, script, False)
        return id
    
    # ----------------------------------------------------------------------
    def jsfile(self, fname):
        return self.text(self.head, "<script language='JavaScript' src='{0}'></script>".format(fname), False)

    # ----------------------------------------------------------------------
    def li(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'li', optv, optkv)
        return self.ref

    # ----------------------------------------------------------------------
    def meta(self, *optv, **optkv):
        return self.single(self.head, 'meta', optv, optkv)
      
    # ----------------------------------------------------------------------
    def _option(self, p, val, txt, *optv, **optkv):
        optkv['value'] = val
        self.ref = self.paired(p, 'option', optv, optkv)
        self.text(self.ref, self.spot.mlt(txt))
        return self.ref
      
    # ----------------------------------------------------------------------
    def p(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'p', optv, optkv)
        return self.ref
    
    # ----------------------------------------------------------------------
    def _password(self, p, *optv, **optkv):
        optkv['type'] = "password"
        return self.single(p, 'input', optv, optkv)
    
    # ----------------------------------------------------------------------
    def pre(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'pre', optv, optkv)
        return self.ref
    
    # ----------------------------------------------------------------------
    def _select(self, p, opt=None, select=None, *optv, **optkv):
        ref = self.paired(p, 'select', optv, optkv)
        if isinstance(opt, dict):
            for k, v in opt.items():
                if select is not None and select==k:
                    self._option(ref, k, v, 'selected')
                else:
                    self._option(ref, k, v)
                    
        self.ref = ref;
        return self.ref
    
    # ----------------------------------------------------------------------
    def span(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'span', optv, optkv)
        return self.ref
    
    # ----------------------------------------------------------------------
    def style(self, stag):
        optkv = {'rel': "stylesheet", 'type': "text/css", 'href': "Core/Style/{0}.css".format(stag)}
        return self.single(self.head, 'link', (), optkv)
    
    # ----------------------------------------------------------------------
    def _submit(self, p, value, *optv, **optkv):
        optkv['type'] = "submit"
        optkv['value'] = self.spot.mlt(value)
        return self.single(p, 'input', optv, optkv)
    
    # ----------------------------------------------------------------------
    def table(self, p, *optv, **optkv):
        self.ref_table = self.paired(p, 'table', optv, optkv)
        return self.ref_table
    
    # ----------------------------------------------------------------------
    def td(self, *optv, **optkv):
        self.ref = self.paired(self.ref_row, 'td', optv, optkv)
        return self.ref
    
    # ----------------------------------------------------------------------
    def _text(self, p, *optv, **optkv):
        optkv['type'] = "text"
        return self.single(p, 'input', optv, optkv)
    
    # ----------------------------------------------------------------------
    def th(self, *optv, **optkv):
        self.ref = self.paired(self.ref_row, 'th', optv, optkv)
        return self.ref
    
    # ----------------------------------------------------------------------
    def tr(self, *optv, **optkv):
        self.ref_row = self.paired(self.ref_table, 'tr', optv, optkv)
        return self.ref_row
    
    # ----------------------------------------------------------------------
    def ul(self, p, *optv, **optkv):
        self.ref = self.paired(p, 'ul', optv, optkv)
        return self.ref
    
    # ----------------------------------------------------------------------
    def video(self, p, src, *optv, **optkv):
        optkv['src'] = src
        optkv['controls'] = 'controls'
        id = self.paired(p, 'video', optv, optkv)
        self.text(id, ('Please update your browser.', 'Veuillez mettre à jour votre navigateur.'))
        return id