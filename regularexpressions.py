#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

# Arquivo com expressões regulares

id_re = re.compile(r'\A([a-z]|[A-Z])(\d|[a-z]|[A-Z])*\Z') # Expressão regular para reconhecer identificadores
int_re = re.compile(r'\A(\d)+\Z') # Expressão regular para reconhecer números inteiros
float_re = re.compile(r'\A(\d)+\.(\d)+\Z') # Expressão regular para reconhecer números reiais

and_re = re.compile(r'\A(a|A)(n|N)(d|D)\Z') # Expressão regular para reconhecer a palavra reservada AND
or_re = re.compile(r'\A(o|O)(r|R)\Z') # Expressão regular para reconhecer a palavra reservada OR
begin_re = re.compile(r'\A(b|B)(e|E)(g|G)(i|I)(n|N)\Z') # Expressão regular para reconhecer a palavra reservada BEGIN
end_re = re.compile(r'\A(e|E)(n|N)(d|D)\Z') # Expressão regular para reconhecer a palavra reservada END
if_re = re.compile(r'\A(i|I)(f|F)\Z') # Expressão regular para reconhecer a palavra reservada IF
then_re = re.compile(r'\A(t|T)(h|H)(e|E)(n|N)\Z') # Expressão regular para reconhecer a palavra reservada THEN
else_re = re.compile(r'\A(e|E)(l|L)(s|S)(e|E)\Z') # Expressão regular para reconhecer a palavra reservada ELSE
while_re = re.compile(r'\A(w|W)(h|H)(i|I)(l|L)(e|E)\Z') # Expressão regular para reconhecer a palavra reservada WHILE
do_re = re.compile(r'\A(d|D)(o|O)\Z') # Expressão regular para reconhecer a palavra reservada DO
until_re = re.compile(r'\A(u|U)(n|N)(t|T)(i|I)(l|L)\Z') # Expressão regular para reconhecer a palavra reservada UNTIL
repeat_re = re.compile(r'\A(r|R)(e|E)(p|P)(e|E)(a|A)(t|T)\Z') # Expressão regular para reconhecer a palavra reservada REPEAT
integer_re = re.compile(r'\A(i|I)(n|N)(t|T)(e|E)(g|G)(e|E)(r|R)\Z') # Expressão regular para reconhecer a palavra reservada INTEGER
real_re = re.compile(r'\A(r|R)(e|E)(a|A)(l|L)\Z') # Expressão regular para reconhecer a palavra reservada REAL
all_re = re.compile(r'\A(a|A)(l|L)(l|L)\Z') # Expressão regular para reconhecer a palavra reservada ALL
string_re = re.compile(r'\A(s|S)(t|T)(r|R)(i|I)(n|N)(g|G)\Z') # Expressão regular para reconhecer a palavra reservada STRING
programa_re = re.compile(r'\A(p|P)(r|R)(o|O)(g|G)(r|R)(a|A)(m|M)(a|A)?\Z') # Expressão regular para reconhecer a palavra reservada PROGRAMA
end_programa_re = re.compile(r'\A(e|E)(n|N)(d|D)\.\Z') # Expressão regular para reconhecer a palavra reservada END.
