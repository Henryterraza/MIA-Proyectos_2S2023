
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CADENA COMILLA ENTERO FIT IGUAL MENOS PATH RUTA SIZE UNIT\n    param : CADENA parametros\n    parametros : parametros parametro\n                | parametro\n                | empty\n    parametro : MENOS CADENA IGUAL RUTA \n                | MENOS CADENA IGUAL COMILLA RUTA COMILLA\n                | MENOS CADENA IGUAL COMILLA CADENA COMILLA\n                | MENOS CADENA IGUAL CADENA\n                | MENOS CADENA IGUAL ENTERO\n    empty :'
    
_lr_action_items = {'CADENA':([0,6,9,12,],[2,8,10,14,]),'$end':([1,2,3,4,5,7,10,11,13,16,17,],[0,-10,-1,-3,-4,-2,-8,-5,-9,-7,-6,]),'MENOS':([2,3,4,5,7,10,11,13,16,17,],[6,6,-3,-4,-2,-8,-5,-9,-7,-6,]),'IGUAL':([8,],[9,]),'RUTA':([9,12,],[11,15,]),'COMILLA':([9,14,15,],[12,16,17,]),'ENTERO':([9,],[13,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'param':([0,],[1,]),'parametros':([2,],[3,]),'parametro':([2,3,],[4,7,]),'empty':([2,],[5,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> param","S'",1,None,None,None),
  ('param -> CADENA parametros','param',2,'p_param','sintactico.py',16),
  ('parametros -> parametros parametro','parametros',2,'p_parametros','sintactico.py',22),
  ('parametros -> parametro','parametros',1,'p_parametros','sintactico.py',23),
  ('parametros -> empty','parametros',1,'p_parametros','sintactico.py',24),
  ('parametro -> MENOS CADENA IGUAL RUTA','parametro',4,'p_parametro','sintactico.py',32),
  ('parametro -> MENOS CADENA IGUAL COMILLA RUTA COMILLA','parametro',6,'p_parametro','sintactico.py',33),
  ('parametro -> MENOS CADENA IGUAL COMILLA CADENA COMILLA','parametro',6,'p_parametro','sintactico.py',34),
  ('parametro -> MENOS CADENA IGUAL CADENA','parametro',4,'p_parametro','sintactico.py',35),
  ('parametro -> MENOS CADENA IGUAL ENTERO','parametro',4,'p_parametro','sintactico.py',36),
  ('empty -> <empty>','empty',0,'p_empty','sintactico.py',50),
]