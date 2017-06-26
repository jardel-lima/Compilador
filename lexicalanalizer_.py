#!/usr/bin/python
# -*- coding: utf-8 -*-

from regularexpressions import *
from characterlists import *

class LexicalAnalizer:
	
	# Construtor da classe que recebe o nome do arquivo 
	def __init__(self,file_name):
		self.__symbol_table = [] # Tabela de símbolos.
		self.__comment = 0 # Flag para comentario. 0 comentário não iniciado. 1 comentário iniciado.
		self.__count_line = 0 # Contador de Linhas.
		self.__erro = [] # Vetor com informações de erro.
		self.__file_name = file_name # Nome do arquivo com o código fonte.

	# Faz a análise léxica
	def analyzer(self):
	
		try:
			# Abri o arquivo fonte
			with open(self.__file_name) as infile:
				# Percorre linha por linha
				for line in infile:	
					# Conta linhas		 
					self.__count_line += 1
					# Faz a análise léxica linha por linha
					if not self.__scanner(line):
						# Se algum erro acontecer retorna None
						return None
			# Se o código passou na análise léxica a tabele com os tokens será retornada			
			return self.__symbol_table
			# Se o arquivo com o nome fornecido não foi encontrado é identificado o erro no vetor de erro e None é retornado
		except IOError:
			self.__erro = [0,self.__file_name]
			return None

	# Retorna o vetor de erro
	def getErro(self):
		return self.__erro
	
	# Retorna a tabela de símbolos	
	def getSymbolTable(self):
		return self.__symbol_table
		
	# Função que recebe uma linha do arquivo e faz a análise léxica
	def __scanner(self,line):
		count_column = 0 # Contator de colunas
		token_type = -1 # Flag para tipo de token. -1 sem tipo, 0 pode ser do tipo Operador e 1 pode ser do tipo literal.
		word = '' # Variável onde o lexema será montado
		count_blank_space = 0 # Contador de espaços vazios
		
		# Enquanto o contador de colunas for menor que o comprimento da lihna percorrer caracter por caracter
		while count_column < len(line):
			# Recebe um caracter do linha do arquivo
			char = line[count_column]
			
			if char in('\n','\r'):
				return self.__addWord(word.strip(),token_type,self.__count_line, count_column)
			
			# Se comentário não tiver sido iniciado 
			if self.__comment == 0:
				#Se o caracter de inicio de de comentário for encontrado flag de comentário é setada para iniciada
				if char == comment_start_token:
					self.__comment = 1
					
				# Se o caracter de término de comentario for encontrado retorna None	
				elif char is comment_end_token:
					# Vetor de erro recebe o tipo de erro e informações sobre o mesmo
					self.__erro = [1,char,self.__count_line,count_column]
					return None
					
				# Se o caracter atual não for um caracter que deve ser ignorado( Nulo )
				# Prossegue com o a análise 			
				elif not isBlank(char):

					# Caso a palavra a ser analisada não tiver um tipo de Token
					if token_type == -1:
						
						# Se o character é algum operador o tipo de token será operador
						if isOperator(char):
							token_type = 0
						# Caso Contrário seŕa do tipo literal
						else:
							token_type = 1
							
					# Caso o tipo de token é operador 	
					if token_type == 0:
						
						# Se o caracter atual continua sendo um operadores
						# Adciona o mesmo a palvra que está sendo formada  
						if isOperator(char):
							word += char
							
						# Caso contrário o possível operador será passado para uma função para 
						# Verificar se o mesmo é um operador
						else:
							# Caso não seja realmente um operador None é retornado
							if not self.__canBeAnOperator(word.strip(),self.__count_line,count_column+1-len(word)-count_blank_space):
								return None
							
							if char == '.':
								self.__symbol_table.append((char,'','',self.__count_line,count_column))
								word = ''
								token_type = -1
							else:
							# O caracter atual passara a ser um nova palavara que poderá ser do tipo literal	
								word = char
								count_blank_space = 0
								token_type = 1
							
					# Caso a palavra iniciada seja do tipo literal
					else:
						# Se o caracter atual for um operador a palavra formada será passada para outra função
						# Que verifica se a palavre é um literal válido	
						if isOperator(char):
						
							# Caso a palavra não seja um literal válido o vetor de erro será setado e None será retornado
							if not self.__canBeALiteral(word,self.__count_line,count_column+1-len(word)):
								return None
								
							# Uma nova palavra será formada com o novo caracter, sendo esse do tipo operador
							word = char
							token_type = 0
						# Caso não seja um operador o caracter atual será adicionado à palavra que está sendo formada
						else:
							if char == '.' and not int_re.match(word):
								if not self.__canBeALiteral(word,self.__count_line,count_column+1-len(word)):
									return None
								self.__symbol_table.append((char,'','',self.__count_line,count_column))
								word = ''
								token_type = -1
							else:
								word += char
							
				# Caso um espaço vazio for encontrado e a palavre tinha sido iniciada e a mesma for do tipo literal
				# Ela será passada para a função que verifica se ela é um literal válido.
				# Caso ela seja do tipo operador o espaço será ignorado e o contador de espaços vazios será
				# incrementado para auxiliar posição da coluna onde o operador é encontrado no texto		
				elif len(word)>0:
						if token_type == 1:
							if not self.__canBeALiteral(word,self.__count_line,count_column+1-len(word)):
								return None
							word = ''
							token_type = -1
						if token_type == 0:
							count_blank_space += 1
						
			# Se a flag de comentário estiver ativa e o caracter de fim de comentário for encontrado a flag é desativada
			else:
				if char == comment_end_token:
					self.__comment = 0	

			# Indíce do próximo caracter			
			count_column+=1
		#Final do Loop
			
		#Caso alguma exista alguma palavra a ser analisada a mesma será analisada 
		#com a correspondente função de analíse de acordo com o seu tipo
		return self.__addWord(word,token_type,self.__count_line, count_column)
		
	#Fim da função
	 
	#Caso alguma exista alguma palavra a ser analisada a mesma será analisada 
	#com a correspondente função de analíse de acordo com o seu tipo
	def __addWord(self,word, token_type, count_line, count_column):
		if len(word)>0:
			if token_type==0:
				if not self.__canBeAnOperator(word.strip(),count_line,count_column-len(word)):
					return None
				count_blank_space = 0
			elif token_type == 1:
				if not self.__canBeALiteral(word,count_line,count_column+1-len(word)):
					return None
		return True
	
	# Função que analisa se uma palavra é um operador válido
	def __canBeAnOperator(self,word, count_line, count_column):
		if len(word) == 1:
			if word == attribution_start_token:
				self.__erro = [1,':',count_line,count_column]
				return None
			# Verifica se a palavra passada é um operador relacional válido	
			elif isRelationalOp(word):
				# Adciona na tabela de símbolos informações do tokem (Tipo, lexema, valor, linha, coluna)
				self.__symbol_table.append(('OP_RELACIONAL',word,'',count_line,count_column))
			# Verifica se a palavra passada é um operador aritmético válido	
			elif isAritimeticOp(word):
				self.__symbol_table.append(('OP_ARITMETICO',word,'',count_line,count_column))
			elif word == '(':
				self.__symbol_table.append((word,'','',count_line,count_column))
			elif word == ')':
				self.__symbol_table.append((word,'','',count_line,count_column))
			elif word == ',':
				self.__symbol_table.append((word,'','',count_line,count_column))
			elif word == ';':
				self.__symbol_table.append((word,'','',count_line,count_column))
			else:
				self.__erro = [1,word,count_line,count_column+1]
				return None
		else:
			# Reconhece ':='
			if word[0] == ':':
				if word[1]== '=':
					if len(word) == 2:
						self.__symbol_table.append((word,'','',count_line,count_column))
					else:
						# Caso possua mais de um operador na palavra passada chamar recusivamente a função 
						self.__symbol_table.append((word[:2],'','',count_line,count_column))
						if not self.__canBeAnOperator(word[2:],count_line,count_column+2):
							return None
				else:
					self.__erro = [1,word,count_line,count_column+1]
					return None
			# Reconhece '='
			elif word[0] == '=':
				self.__symbol_table.append(('OP_RELACIONAL','=','',count_line,count_column))
				if not self.__canBeAnOperator(word[1:],count_line,count_column+1):
					return None
						
			# Reconhece '<=' e '<>'
			elif word[0] == '<':
				if word[1]== '=':
					if len(word) == 2:
						self.__symbol_table.append(('OP_RELACIONAL','',word,count_line,count_column))
					else:
						self.__symbol_table.append(('OP_RELACIONAL',word[:2],'',count_line,count_column))
						if not self.__canBeAnOperator(word[2:],count_line,count_column+2):
							return None
		
				elif word[1]== '>':
					if len(word) == 2:
						self.__symbol_table.append(('OP_RELACIONAL','',word,count_line,count_column))
					else:
						self.__symbol_table.append(('OP_RELACIONAL',word[:2],'',count_line,count_column))
						if not self.__canBeAnOperator(word[2:],count_line,count_column+2):
							return None
	
				else:
					self.__symbol_table.append(('OP_RELACIONAL','',word[0],count_line,count_column))
					if not self.__canBeAnOperator(word[1:],count_line,count_column+1):
							return None

			# Reconhece '>='
			elif word[0] == '>':
				if word[1]== '=':
					if len(word) == 2:
						self.__symbol_table.append(('OP_RELACIONAL','',word,count_line,count_column))
					else:
						self.__symbol_table.append(('OP_RELACIONAL',word[:2],'',count_line,count_column))
						if not self.__canBeAnOperator(word[2:],count_line,count_column+2):
							return None
				else:
					self.__symbol_table.append(('OP_RELACIONAL','',word[0],count_line,count_column))
					if not self.__canBeAnOperator(word[1:],count_line,count_column+1):
						return None

			# Reconhece sequência de '('
			elif word[0] == '(':
				self.__symbol_table.append((word[0],'','',count_line,count_column))
				count_aux = 1
				
				if not self.__canBeAnOperator(word[1:],count_line,count_column+1):
						return None
				
			# Reconhece sequência de ')'
			elif word[0] == ')':
				self.__symbol_table.append((word[0],'','',count_line,count_column))
				count_aux = 1
				
				if not self.__canBeAnOperator(word[1:],count_line,count_column+1):
						return None
						
			# Reconhece operadores aritméticos	
			elif isAritimeticOp(word[0]) == 1:
				self.__symbol_table.append(('OP_ARITMETICO',word[0],'',count_line,count_column))
				if not self.__canBeAnOperator(word[1:],count_line,count_column+1):
						return None
			# Reconhece ','			
			elif word[0] == ',':
				self.__symbol_table.append((',','','',count_line,count_column))
				if not self.__canBeAnOperator(word[1:],count_line,count_column+1):
					return None
			
			# Reconhece ';'
			elif word[0] == ';':
				self.__symbol_table.append((';','','',count_line,count_column))
				if not self.__canBeAnOperator(word[1:],count_line,count_column+1):
					return None
					
			# Caso nenhum dos padrões anteriores seja encontrado um erro é gerado
			else:
				self.__erro = [1,word,count_line,count_column+1]
				return None
		
		return True	
	# Fim da Função

	# Função que verifica se a palavra passada é um caracter válido
	def __canBeALiteral(self,word,count_line,count_column):
	
		# Se a palavra passada casar com a expressão regular para Identificadores
		# uma função auxiliar será chamada para verificar se a palavra passada
		# é uma palavra reservada da linguagem ou um simples identificador
		if id_re.match(word):
			self.__wichLiteral(word, count_line, count_column)
		# Se a palavra passada combinar com a expressão regular para números inteiros adcionar na tabela de tokens
		elif int_re.match(word):
			self.__symbol_table.append(('INTEGER_VAR','',int(word),count_line,count_column))
		# Se a palavra passada combinar com a expressão regular para números reais adcionar na tabela de tokens
		elif float_re.match(word):
			self.__symbol_table.append(('REAL_VAR','',float(word),count_line,count_column))
#		elif end_programa_re.match(word):
#			self.__symbol_table.append(('END.','','',count_line,count_column))
		# Caso a palavra passada não combinar com nenhum padrão a mesma não é um literal válido
		else:
			self.__erro = [1,word,count_line,count_column]
			return None

		return True
	# Fim da Função
	
	# Função que verifica se a palavra que casa com a expressão regular para indentificadores é alguma palavra reservada
	def __wichLiteral(self,word, count_line, count_column):

		if and_re.match(word) or or_re.match(word) :
			self.__symbol_table.append(('OP_BOOLEAN',word,'',count_line,count_column))
		elif begin_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif end_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif if_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif then_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif else_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif while_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif do_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif until_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif repeat_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif integer_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif real_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif all_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif string_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		elif programa_re.match(word):
			self.__symbol_table.append((word,'','',count_line,count_column))
		else:
			self.__symbol_table.append(('ID',word,'',count_line,count_column))
		
	#Fim da Função

# Fim da Classe
