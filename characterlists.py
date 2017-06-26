#!/usr/bin/python
# -*- coding: utf-8 -*-

# Arquivo que contém constantes, listas e funçoes auxíliares

attribution_start_token = ':' # Caracter inicial do token de atribuição
comment_start_token = '{' # Token inicial de comentário
comment_end_token = '}'# Token final do comentário
blank_tokens = (' ','\t','\n','\r') # Lista com caracteres a serem ignorados
rel_op_tokens = ('<','>','=') # Lista com caracteres de operadores relacionais
aritmetics_op_tokens = ('+','-','*','/') # Lista com caracteres de operadores aritméticos 
especial_op_tokens = (':',',',';','(',')') # Lista com caracteres de operadores especiais 

# Função que verifica se o caracter é vazio
def isBlank(char):
	if char in blank_tokens:
		return True
	else:
		return None

# Função que verifica se o caracter é um operador relacional
def isRelationalOp(char):
	if char in rel_op_tokens:
		return True
	else:
		return None

# Função que verifica se o caracter é um operador aritmetico
def isAritimeticOp(char):
	if char in aritmetics_op_tokens:
		return True
	else:
		return None
		
# Função que verifica se o caracter é um operador especial
def isEspecialOp(char):
	if char in especial_op_tokens:
		return True
	else:
		return None
	
# Função que verifica se o caracter é algum tipo de operador
def isOperator(char):
	return isAritimeticOp(char) or isEspecialOp(char) or isRelationalOp(char)
