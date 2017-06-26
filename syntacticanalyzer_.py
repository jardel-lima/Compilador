#!/usr/bin/python
# -*- coding: utf-8 -*-

from lexicalanalizer_ import *

class SyntacticAnalyzer:

	def __init__(self,file_name):
		self.__index = 0 # Indíce que percorre a tabela de symbolos
		self.__variables = {} # Vetor de variaveis declaradas
		self.__var_type = '' # Tipo da variável que recebrá uma atribuição ou o resultado de operações 
		self.__erro = [] # Vetor com informações do self.__erro
		self.__file_name = file_name #	Nome do arquivo com o código fonte
		self.__table = [] # Vetor com o vetor de símbolos retornado pelo analisador léxico
		self.__table_size = 0 # Guarda a quantidade de elementos na tabela
		self.__wrong_symbol = '' # Recebe o síbolo errado quando um erro acontece
		
	# Fim do Construtor
		
		
	# Função que faz a analíse sintática
	def analyzer(self):
		# Instancia o analisador léxico
		lexical_analizer = LexicalAnalizer(self.__file_name)
		self.__table = lexical_analizer.analyzer() 
		
		# Se o código passou na analíse léxica a tabela de símbolos será retornada
		# Caso contrário um self.__erro ocorreu
		if self.__table:
			self.__table_size = len(self.__table)
			if self.__syntacticAnalyzer():
				#three_adress = ThreeAdressGenerator(self.__table,'jardel.txt')
				#three_adress.generate()
				return True
			else:
				return None
		else:
			# Caso o arquivo seja vazio
			if self.__table and len(self.__table) == 0:
				self.__erro = [7] 
				return None
			# Caso o arquivo não seja vazio
			else:
				self.__table = lexical_analizer.getSymbolTable()	
				self.__erro = lexical_analizer.getErro()
				return None
	
	# Fim da função
	
	# Retorna o vetor de self.__erro
	def getErro(self):
		return self.__erro
	#Fim da função
	
	# Função que verifica se existe uma tabela de símbolo
	def hasSymbolTable(self):
		if len(self.__table) > 0:
			return True
		return None
		
	# Função que imprime a tabela de símbolos do código fornecido
	def printTable(self):
		print("Tabela de símbolos")
		print("|%15s | %10s | %10s | %10s | %10s|")%('TIPO','LEXEMA','VALOR','LINHA','COLUNA')
		print('---------------------------------------------------------------------')
		for info in self.__table:
			print("|%15s | %10s | %10s | %10d | %10d|")%(info[0],info[1],str(info[2]),info[3],info[4])
			print('---------------------------------------------------------------------')
	
	# Fim da Função
	
	def __getErroSymbol(self):
		
		if self.__table[self.__index][0] in ('REAL_VAR','INTEGER_VAR'):
			self.__wrong_symbol = self.__table[self.__index][2]
		elif self.__table[self.__index][0] in ('ID','OP_ARITMETICO','OP_BOOLEAN','OP_RELACIONAL'):
			self.__wrong_symbol = self.__table[self.__index][1]
		else:
			self.__wrong_symbol = self.__table[self.__index][0]
		
	# Função que verefica se o token atual é o token desejado	
	def __isToken(self,token):
		return self.__table[self.__index][0].upper() == token
	# Fim da Função
	
	# Função que verefica se o indíce da tabela é válido
	def __isIndexValid(self):
			return self.__index < self.__table_size
	# Fim da Função
	
	# Função que incrementa o indície da tabela e verifica se o mesmo é válido
	def __incrementIndex(self):
		self.__index += 1
		if self.__index < self.__table_size:
			return True
		else:
			self.__index -= 1
			self.__erro = [6, self.__table[self.__index][3],self.__table[self.__index][4]+1] 
			return None
	# Fim da Função		
			
	# Faz a analíse sintática da código	
	# Reconhece <Programa> ::= <bloco_principal>
	# Reconhece <bloco_principal> ::= Programa  <id> ; [ <decl_var> ]*  Begin <bloco>  End.
	def __syntacticAnalyzer(self):
	
		if self.__isToken("PROGRAMA") :
			# Chama função que incrementa o índece da tabela de símbolos
			if not self.__incrementIndex():
				return None
		else:
			# Função que determina se dever ser exebido o valor ou o lexema do tokem que está errado
			self.__getErroSymbol()
			# Vetor com informações do erro vai receber- Tipo do erro e informações sobre o erro
			self.__erro = [2,self.__wrong_symbol, 'PROGRAMA', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
			
		if  self.__isToken("ID"):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'Identificador', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None 
	
		if self.__isToken(";"):
			if not self.__incrementIndex():
				return None;
		else :
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ';', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None 

		# Reconhece [ <decl_var> ]*
		while   self.__isToken("INTEGER")  or   self.__isToken("REAL") or self.__isToken("STRING") :
			self.__var_type = self.__table[self.__index][0].upper()
			if not self.__incrementIndex():
				return None	
						
			if self.__decl_var():
				if not self.__incrementIndex():
					return None
			else:
				return None

		# Reconhece 'Begin'
		if self.__isToken("BEGIN"):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'BEGIN', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Reconhece <bloco>
		if not self.__bloco():
			return None
	
		if not self.__incrementIndex():
			return None
		
		# Reconhece 'end.'
		if self.__isToken("END"):
			return True
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'END.', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		if not self.__incrementIndex():
			return None
		
		if self.__isToken("."):
			return True
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'END.', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		
	
	# Fim da Função
	
	# Reconhece <decl_var> ::= 	<tipo>  <id>  [,<id>]*;
	def __decl_var(self):
		#Reconhece <id>
		if  self.__isToken("ID"):
			# Verifica se a variável já foi declarada, caso não colaca na lista de variaveis
			if not self.__variables.has_key(self.__table[self.__index][1].upper()):
				self.__variables[self.__table[self.__index][1].upper()] = self.__var_type
			else:
				self.__erro = [5, self.__table[self.__index][1],self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None
				
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'Identificador', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None	
		
		# Reconhece [,<id>]*
		if  self.__isToken(",") :
			if not self.__incrementIndex():
				return None
			if not self.__decl_var():
				return None
		# Reconhece ;
		elif self.__isToken(";"):
			return True
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, "',' ou ';'", self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		return True
	
	# Fim da função
	
    # Reconhece	<bloco> ::= Begin [<comando>  [ <comando>]*]? End ;
	def __bloco(self):
	
		# Reconhece o 'Begin' do bloco
		if self.__isToken("BEGIN"):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'BEGIN', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Chama função que reconhece <comando>	
#		if not self.__comando():
#			return None
	
#		if not self.__incrementIndex():
#			return None
		
		# Reconhece [<comando>]*
		while self.__table[self.__index][0].upper() in ("ID","BEGIN",'ALL','WHILE','REPEAT','IF'):
			if not self.__comando():
				return None
			if not self.__incrementIndex():
				return None
			
		# Reconhece o 'End' do bloco
		if self.__isToken('END'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'END', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None	
		
		# Reconhece ';' após o 'End'' do bloco
		if self.__isToken(';'):
			return True	
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ';', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None	
	# Final da Função
		
	# Reconhece comando> ::=    <comando_basico> 
	#	| <iteracao> 
	#	|  if (<expr_relacional>) then <comando> [else <comando>]?
	def __comando(self):
		
		# Chama função que reconhece <comando_basico>
		if self.__isIndexValid() and self.__table[self.__index][0].upper() in ("ID","BEGIN",'ALL'):
			return self.__comando_basico()
		# Chama função que reconhece <interacao>
		elif self.__isIndexValid() and self.__table[self.__index][0].upper() in ('WHILE','REPEAT'):
			return self.__interacao()
		# Chama função que reconhece if (<expr_relacional>) then <comando> [else <comando>]?
		elif self.__isToken('IF'):
			if not self.__incrementIndex():
				return None
			return self.__condicional()#
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, " Identificador ou 'BEGIN' ou 'ALL' ou 'WHILE' ou 'REPEAT' ou 'IF'", self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None	
		
	# Fim da função
		
	# Reconhece <comando_basico> ::=  	<atribuicao> 
	#		|   <bloco>
	#		| All ( <id>  [, <id>]* );
	def __comando_basico(self):
		
		# Caso o token for do tipo ID chama a função que reconhece <atribuicao>
		if self.__isToken('ID'):
			if not self.__variables.has_key(self.__table[self.__index][1].upper()):
				self.__erro = [4, self.__table[self.__index][1],self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None	 
			
			# Salva o tipo da variavel para fazer a analíse semântica 
			self.__var_type = self.__variables.get(self.__table[self.__index][1].upper()).upper()
			
			if not self.__incrementIndex():
				return None
			
			return self.__atribuicao()
		
		# Caso o token for 'Begin' chama a função que reconhece <bloco>	
		elif self.__isToken('BEGIN'):
			return self.__bloco()
			
		# Caso o token for 'All' chama a função que reconhece All ( <id>  [, <id>]* );
		elif self.__isToken('ALL'):
			if not self.__incrementIndex():
				return None
			if self.__isToken('('):
				if not self.__incrementIndex():
					return None
				return self.__comandoAll()
			else:
				self.__getErroSymbol()
				self.__erro = [2,self.__wrong_symbol, '(', self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None	
	
	# Fim da Função
	
	# Reconhece <iteracao> ::=  while (<expr_relacional>) do <comando>
	#		|   repeat <comando> until (<expr_relacional>)
	def __interacao(self):
		
		# Caso o token seja 'While' chama a função que reconhece while (<expr_relacional>) do <comando>
		if self.__isToken('WHILE'):
			if not self.__incrementIndex():
				return None
			return self.__comandoWhile()
		
		# Caso o token seja 'Repeat' chama a função que reconhece repeat <comando> until (<expr_relacional>)
		elif self.__isToken('REPEAT'):
			if not self.__incrementIndex():
				return None
			return self.__comandoRepeat()
	
	# Fim da função
	
	# Reconhece if (<expr_relacional>) then <comando> [else <comando>]?
	def __condicional(self):
		
		# Reconhece '('
		if self.__isToken('('):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, '(', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None	
		
		# Chama função que reconhece <expr_relacional>
		if not self.__expr_relacional():
			return None
	
		if not self.__incrementIndex():
			return None
	
		# Reconhece ')'
		if self.__isToken(')'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ')', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None	
		
		# Reconhece 'Then'
		if self.__isToken('THEN'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'THEN', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None	
		
		# Chama função que reconhece <comando>
		if not self.__comando():
			return None
	
		if not self.__incrementIndex():
			return None 
		
		# Reconhece [else <comando>]?
		if self.__isToken('ELSE'):
			if not self.__incrementIndex():
				return None 
			if not self.__comando():
				return None
			if not self.__incrementIndex():
				return None	
		
		self.__index -= 1
		return True

	# Fim da função
	
	# Reconhece <atribuicao> ::= <id> := <expr_arit> ;
	def __atribuicao(self):
		
		# Reconhece ':='
		if self.__isToken(':='):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ':=', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Chama função que reconhece <expr_atr>
		if not self.__expr_aritmetica():
			return None
		
		if not self.__incrementIndex():
			return None
		
		# Reconhece ';'
		if self.__isToken(';'):
			return True
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ';', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
	
	# Fim função
	
	# Reconhece All ( <id>  [, <id>]* );
	def __comandoAll(self):
		
		# Reconhece 'ID'
		if self.__isToken('ID'):
			# Verifica se a variável foi delcarada
			if not self.__variables.has_key(self.__table[self.__index][1].upper()):
				self.__erro = [4,self.__table[self.__index][1],self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None	
			# Verifica se a variável é do tipo string
			if self.__variables.get(self.__table[self.__index][1].upper()).upper() != "STRING":
				self.__erro = [3,'STRING',self.__variables.get(self.__table[self.__index][1].upper()) ,self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None		
		
			if not self.__incrementIndex():
				return None
		# Obrigatóriamente a função All tem que receber um identificador como arguemento
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'Identificador', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Reconhece [, <id>]8
		if	self.__isToken(','):
			if not self.__incrementIndex():
				return None
		
			if not self.__comandoAll():
				return None
		
		# Reconhece ')'	
		elif self.__isToken(')'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ')', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Reconhece ';'
		if self.__isToken(';'):
			return True
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ';', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
	# Fim da função
	
	# Reconhece while (<expr_relacional>) do <comando>
	def __comandoWhile(self):
		
		# Reconhece '('
		if self.__isToken('('):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, '(', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Chama função que reconhece <expr_relacional>
		if not self.__expr_relacional():
			return None
	
		if not self.__incrementIndex():
			return None
		
		# Reconhece ')'
		if self.__isToken(')'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ')', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None	
		
		# Reconhece do <comando>
		if self.__isToken('DO'):
			if not self.__incrementIndex():
				return None
			# Chama a função que reconhece <comando>
			return self.__comando()
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'DO', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
	
	# Fim da função
	
	# Reconhece repeat <comando> until (<expr_relacional>)	
	def __comandoRepeat(self):
		
		# Chama função que reconhece <comando>
		if not self.__comando():
			return None
	
		if not self.__incrementIndex():
			return None
		 
		# Reconhece 'Until'
		if self.__isToken('UNTIL'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, 'UNTIL', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Reconhece '('
		if self.__isToken('('):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, '(', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
			
		# Chama função que reconhece <expr_relacional>
		if not self.__expr_relacional():
			return None
			
		if not self.__incrementIndex():
			return None
			
		# Reconhece ')'	
		if self.__isToken(')'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ')', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Reconhece ';'
		if self.__isToken(';'):
			return True
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, ';', self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
	
	# Fim da função
	
	# Reconhece <expr_relacional> ::= <val> <op_relacionais> <val>
	#		| (<expr_relacional>) [<op_booleanos> (<expr_relacional>)] ?
	def __expr_relacional(self):
		
		# Reconhece: <val> ::= <id>  | <integer> | <real>
		if self.__isIndexValid() and self.__table[self.__index][0] in ('ID','REAL_VAR','INTEGER_VAR'):
			# Caso seja um indentificador verifica se o mesmo foi declarado
			if self.__isToken('ID'):
				
				if not self.__variables.has_key(self.__table[self.__index][1].upper()):
					self.__erro = [4,self.__table[self.__index][1],self.__table[self.__index][3],self.__table[self.__index][4]] 
					return None	
				
				# Quarda o tipo da variável para fazer verificação de tipos				
				if self.__variables.get(self.__table[self.__index][1].upper()).upper() == 'STRING':
					self.__erro = [3,'STRING',"'REAL_VAR' ou'INTEGER_VAR'",self.__table[self.__index][3],self.__table[self.__index][4]] 
					return None
			
			if not self.__incrementIndex():
				return None
				
			# Reconhece: <op_relacionais>
			if self.__isToken('OP_RELACIONAL'):
				if not self.__incrementIndex():
					return None
			else:
				self.__getErroSymbol()
				self.__erro = [2,self.__wrong_symbol, "'<' ou '>' ou '<=' ou '>=' ou '=' ou '<>'", self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None
			
			# Reconhece: <val> ::= <id>  | <integer> | <real>
			if self.__isIndexValid() and self.__table[self.__index][0] in ('ID','REAL_VAR','INTEGER_VAR'):
				# Caso seja um indentificador verifica se o mesmo foi declarado
				if self.__isToken('ID'):
				
					if not self.__variables.has_key(self.__table[self.__index][1].upper()):
						self.__erro = [4,self.__table[self.__index][1],self.__table[self.__index][3],self.__table[self.__index][4]] 
						return None	
				
					# Quarda o tipo da variável para fazer verificação de tipos				
					if self.__variables.get(self.__table[self.__index][1].upper()).upper() == 'STRING':
						self.__erro = [3,'STRING',"'REAL_VAR' ou'INTEGER_VAR'",self.__table[self.__index][3],self.__table[self.__index][4]] 
						return None
				
			else:
				self.__getErroSymbol()
				self.__erro = [2,self.__wrong_symbol, "Identificador, número REAL, número INTEGER ou '('", self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None
				
		# Caso o token for '(' chama a função que reconhece:  (<expr_relacional>) [<op_booleanos> (<expr_relacional>)] ?	
		elif self.__isToken('('):
			
			if not self.__incrementIndex():
				return None
			
			if not self.__expr_relacional():
				return None
			
			if not self.__incrementIndex():
				return None
	
			# Reconhece: ')'
			if self.__isToken(')'):
				if not self.__incrementIndex():
					return None
			else:
				self.__getErroSymbol()
				self.__erro = [2,self.__wrong_symbol,")", self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None
				
			if self.__isToken('OP_BOOLEAN'):
				if not self.__incrementIndex():
					return None 
				
				if self.__isToken('('):
					if not self.__incrementIndex():
						return None
				
				else:
					self.__getErroSymbol()
					self.__erro = [2,self.__wrong_symbol,"(", self.__table[self.__index][3],self.__table[self.__index][4]] 
					return None
				
				if not self.__expr_relacional():
					return None
			
				if not self.__incrementIndex():
					return None
	
				# Reconhece: ')'
				if self.__isToken(')'):
					#if not self.__incrementIndex():
					#	return None
					
					pass
				else:
					self.__getErroSymbol()
					self.__erro = [2,self.__wrong_symbol,")", self.__table[self.__index][3],self.__table[self.__index][4]] 
					return None
			else:
				self.__index -= 1
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, "Identificador, número REAL, número INTEGER ou '('", self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		return True
	
	# Fim da função
		
	# Reconhece: <expr_arit> ::=  <val> 
	#		| <val>  <op_aritmetico> <val> 
	#		| (<expr_arit> ) <op_aritmetico> (<expr_arit>)
	def	__expr_aritmetica(self):
	
		__var_type_local = '' # Quarda o tipo da variável ou constante 
	
		# Caso o token for do tipo 'id'. 'REAL_VAR' ou 'inteiro'
		if self.__isIndexValid() and self.__table[self.__index][0] in ('ID','REAL_VAR','INTEGER_VAR'):
			# Caso o token for um identificador
			if self.__isToken('ID'):
				
				# Verefica se o mesmo foi declarado
				if not self.__variables.has_key(self.__table[self.__index][1].upper()):
					self.__erro = [4,self.__table[self.__index][1],self.__table[self.__index][3],self.__table[self.__index][4]] 
					return None
				
				# Se a variável que recebe a atribuição for inteira ela só pode receber um número inteiro
				if self.__var_type == 'INTEGER' and self.__variables.get(self.__table[self.__index][1].upper()) != 'INTEGER':
					self.__erro = [3, self.__var_type, self.__variables.get(self.__table[self.__index][1].upper()) ,self.__table[self.__index][3],self.__table[self.__index][4]] 
					return None	
				
				#Tirar isso	
				elif self.__var_type == 'STRING' and self.__variables.get(self.__table[self.__index][1].upper()).upper() != 'STRING':
					self.__erro = [3, self.__var_type, self.__variables.get(self.__table[self.__index][1].upper()),self.__table[self.__index][3] ,self.__table[self.__index][4]] 
					return None
				
				# Se a variável que recebe a atribuição for real ela pode receber um número real ou inteiro		
				elif self.__var_type == 'REAL' and self.__variables.get(self.__table[self.__index][1].upper()).upper() == 'STRING':
					self.__erro = [3, self.__var_type, self.__variables.get(self.__table[self.__index][1].upper()), self.__table[self.__index][3], self.__table[self.__index][4]] 
					return None	
			# Caso o token for uma constante
			## Se a variável que recebe a atribuição for inteira ela só pode receber um número inteiro
			elif self.__var_type == 'INTEGER' and self.__isToken('REAL_VAR'):
				self.__erro = [3,self.__var_type, 'REAL' , self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None	
		
			if not self.__incrementIndex():
				return None
				
		# Reconhece: (<expr_arit> ) <op_aritmetico> (<expr_arit>)
		elif self.__isToken('('):
			if not self.__incrementIndex():
				return None
			# Chama função que reconhece: (<expr_arit> ) <op_aritmetico> (<expr_arit>)
			if not self.__expr_aritimetica_parenteses():
				return None

		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, "Identificador, número REAL, número INTEGER ou '('", self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
	
		# Reconhece: <val>  <op_aritmetico> <val> 
		# Reconhece: <op_aritmetico>
		if self.__isToken('OP_ARITMETICO'):		
			
			if self.__var_type == 'INTEGER' and self.__table[self.__index][1]=='/':
				self.__erro = [3,'REAL',self.__var_type,self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None	
			
			if self.__var_type == 'STRING':
				self.__erro= [3,'REAL ou INTEGER','STRING',self.__table[self.__index][3],self.__table[self.__index][4]] 
				return None
			if not self.__incrementIndex():
				return None
	
			# Reconhece <val>
			if self.__table[self.__index][0] in ('ID','REAL_VAR','INTEGER_VAR'):
				if self.__isToken('ID'):
					if not self.__variables.has_key(self.__table[self.__index][1].upper()):
						self.__erro = [4,self.__table[self.__index][1],self.__table[self.__index][3],self.__table[self.__index][4]] 
						return None
					if self.__variables.get(self.__table[self.__index][1].upper()).upper() == 'STRING':
						self.__erro= [3,'REAL ou INTEGER','STRING',self.__table[self.__index][3],self.__table[self.__index][4]] 
						return None
			# Reconhece: (<expr_arit> ) <op_aritmetico> (<expr_arit>)
			elif self.__isToken('('):
				if not self.__incrementIndex():
					return None
				# Chama função que reconhece: (<expr_arit> ) <op_aritmetico> (<expr_arit>)
				if not self.__expr_aritimetica_parenteses():
					return None
				
				self.__index -= 1
		else:
			self.__index -= 1
			
		return True
		
	# Fim da Função
	
	# Reconhece: (<expr_arit> ) <op_aritmetico> (<expr_arit>)
	def __expr_aritimetica_parenteses(self):
		
		# Chama função que reconhece: <expr_arit>
		if not self.__expr_aritmetica():
			return None
	
		if not self.__incrementIndex():
			return None
	
		# Reconhece: ')'
		if self.__isToken(')'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol,")", self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Reconhece: <op_aritmetico>
		if self.__isToken('OP_ARITMETICO'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol, "'+' ou '*' ou '/' ou '*'", self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Reconhece: '('
		if self.__isToken('('):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol,"(", self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		# Chama função que reconhece: <expr_arit>
		if not self.__expr_aritmetica():
			return None
		
		if not self.__incrementIndex():
			return None
	
		# Reconhece: ')'
		if self.__isToken(')'):
			if not self.__incrementIndex():
				return None
		else:
			self.__getErroSymbol()
			self.__erro = [2,self.__wrong_symbol,")", self.__table[self.__index][3],self.__table[self.__index][4]] 
			return None
		
		return True
	
	# Fim da Função

# Fim da Classe
		
	
	
