#!/usr/bin/python
# -*- coding: utf-8 -*-

from syntacticanalyzer_ import *
from errohandle import *

while(True):
	
	file_name = raw_input("\nEntre com o nome do arquivo ou q para sair: ")	
	
	if file_name not in('q','Q'):
		# Passa o nome do arquivo para o analisador Sintático
		syntatic_analyze = SyntacticAnalyzer(file_name.strip()+'.txt')
		# Caso o código passou na analíse 
		if syntatic_analyze.analyzer():
			msg = "\nCompilação efetuada com sucesso!!!."
			while(True):
				input_ = raw_input(msg+'\n\n-Tecle q e Enter pra encerrar.\n-Tecle p e Enter para imprimir a tabela de símbolos.\n-Tecle Enter para inserir um novo arquivo:')
				if len(input_.strip()) == 0:
					break
				elif input_.strip() == 'p':
					syntatic_analyze.printTable()
				elif input_ in('q','Q'):
					exit()
				else:
					msg = '\nEntrada Inválida!!!'
		#Caso ele não passou mostrar a mensagem de erro
		else:
			erro = ErroHandle(syntatic_analyze.getErro())
			print(erro.getErroMsg())
			while(True):
				
				# Se existir uma tabela de símbolo pode-se pedir para que a mesma seja impressa
				if syntatic_analyze.hasSymbolTable():
					input_ = raw_input('-Tecle q e Enter pra encerrar.\n-Tecle p e Enter para impremir a tabela de símbolos.\n-Tecle Enter para inserir um novo arquivo:')
					if len(input_.strip()) == 0:
						break
					elif input_.strip() == 'p':
						syntatic_analyze.printTable()
					elif input_ in('q','Q'):
						exit()	
				else:
					input_ = raw_input('-Tecle q pra encerrar ou Enter para um novo arquivo:')
					if len(input_.strip()) == 0:
						break
					elif input_ in('q','Q'):
						exit()
	else:
		exit()
#	
    

	
	
