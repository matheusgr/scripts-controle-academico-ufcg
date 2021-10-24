"""
Script para converter nomes/turmas em emails por turma.
"""
import csv
import os
import unicodedata

diretorio='disciplinas'

def acha_email(nome):
    res = []
    primeiro = nome[0]
    for i in range(len(nome) - 1, 0, -1):
        for j in range(i - 1, 0, -1):
            res.append(primeiro + '.' + nome[j] + '.' + nome[i])
    res.append(nome[0] + '.' + nome[-1])
    for i in range(len(nome) - 2, 0, -1):
        res.append(primeiro + '.' + nome[i])
    return res

def procura_email(emails, par_nomes, nome):
    for n, email in par_nomes:
        if nome in n:
            return email
    for email in acha_email(nome.split()) + acha_email(nome[0:40].split()):
        if email in emails:
            return email


emails = set()
par_nomes = []

#proc_uni  = lambda x : unicodedata.normalize('NFKD', unicode(x, 'utf-8')).encode("ascii","ignore").lower()
proc_uni  = lambda x : unicodedata.normalize('NFKD', x.strip()).encode("ascii","ignore").lower().decode('utf-8')

with open('all.csv', 'r') as ficheiro:
    for linha in ficheiro.readlines():
        matr, nome, email = linha.lower().strip().split(';')
        email = email.split('@')[0]
        nome = proc_uni(nome)
        if nome.strip():
            par_nomes.append((nome, email))
        emails.add(email)


# 14102100;112222222;EI BOY TUDO BOM;Em Curso

for arquivo in os.listdir(diretorio):
    if not arquivo.endswith('csv'):
        continue
    print(arquivo)
    data = open(diretorio + os.sep + arquivo, 'r').readlines()
    pessoas_por_turma = {}
    contagem_por_turma = {}
    galera = []
    for dado in data:
        dado = proc_uni(dado)
        dado = dado.split(';')
        nome = dado[2]
        matr = dado[1]
        email = procura_email(emails, par_nomes, nome)
        if email:
            galera.append((email, nome))
        else:
            print(">>>MISSING:", nome)
    if galera:
        saida = open('out' + os.sep + arquivo, 'w')
        disc = proc_uni('.'.join(arquivo.replace('(Bloqueada para Matrícula)', '').split('.')[:-1])).upper().strip()
        turma = disc.split('-')[-1].strip()
        while turma.startswith('0'):
            turma = turma[1:]
        nome_disc = disc[:-3-len(turma)]
        #P2,10,2016.2
        #2291146,matheusgr
        #pedo,bó,pedobo@ccc.ufcg.edu.br
        #maria,mariana macedo, marianana@ccc.ufcg.edu.br
        saida.write(nome_disc + "," + turma + ",2017.2\n2291146,matheusgr\n")
        for pessoa in galera:
            email, nome = pessoa
            nome, sobrenome = nome.split()[0], ' '.join(nome.split()[1:])
            linha = nome + ',' + sobrenome + ',' + email + '@ccc.ufcg.edu.br'
            saida.write(linha + '\n')
        saida.close()
