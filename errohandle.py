#!/usr/bin/python
# -*- coding: utf-8 -*-

# Classe que trata os diferentes tipos de erro do código
class ErroHandle:
	
	# Construtor da classe, recebe o vetor com informações do erro
	def __init__(self,erro):
		self.__erro = erro # 
		self.__erro_msg = ''
		
		self.__buildErroMsg()
		
		
	# Função que monta a mensagem de erro baseado no tipo de erro passado
	def __buildErroMsg(self):
		erro_type = self.__erro[0]
		
		if erro_type == 0:
			self.__erro_msg = "\nArquivo '%s' não encontrado!!!\n"%(self.__erro[1])
		elif erro_type == 1:
			self.__erro_msg = "\nErro 01: Identificador ou simbolo invalido '%s'. Linha %d Coluna %d.\n"%(self.__erro[1], self.__erro[2], self.__erro[3])
		elif erro_type == 2: 
			self.__erro_msg = "\nErro 2: Símbolo ‘%s’ inesperado. Esperando: '%s''. Linha %d Coluna %d.\n"%(self.__erro[1], self.__erro[2], self.__erro[3], self.__erro[4])
		elif erro_type == 3:
			self.__erro_msg = "\nErro 3: Tipos Incompatíveis. %s e %s. Linha %d Coluna %d.\n"%(self.__erro[1], self.__erro[2], self.__erro[3], self.__erro[4])
		elif erro_type == 4:
			self.__erro_msg= "\nErro 4: Identificador '%s' não declarado. Linha %d Coluna %d.\n"%(self.__erro[1], self.__erro[2], self.__erro[3])
			
		elif erro_type == 5:
			self.__erro_msg= "\nErro 5: Identificador '%s' já declarado. Linha %d Coluna %d.\n"%(self.__erro[1], self.__erro[2], self.__erro[3])
		
		elif erro_type == 7:
			self.__erro_msg= "\nErro 2:Esperando: 'PROGRAMA'. Linha 1 Coluna 1.\n"
		
		elif erro_type == 6:
			self.__erro_msg = "\nErro 2: Fim Inesperado. Linha %d Coluna %d.\n"%(self.__erro[1], self.__erro[2])
			
	# Retorna a mensagem de erro
	def getErroMsg(self):
		return self.__erro_msg
