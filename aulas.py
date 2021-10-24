import csv
from getpass import getpass
import math

import controle


def _processa_csv(csv_f, delimiter):
    # Formato do arquivo: data, aula, carga_horaria (opcional)
    aulas = []
    with open(csv_f, encoding='utf-8-sig') as csvfile:
        aulas_reader = csv.reader(csvfile, delimiter=delimiter)
        for linha in aulas_reader:
            aulas.append(linha)
    return aulas

def conv(dat):
    if '-' in dat:
        a, m, d = dat.split('-')
        return '/'.join([d, m, a])
    return dat


def processa_csv(codigo, turma, csv_f, delimiter=','):
    data = controle.base(codigo, turma, 'ProfessorTurmaAulasConfirmar')
    aulas = _processa_csv(csv_f, delimiter)
    data["numAulas"] = str(len(aulas))
    n = 0
    for aula in aulas:
        d = aula[0]
        a = aula[1]
        ch = "2" if len(aula) == 2 else aula[2]
        data["d_" + str(n + 1)] = conv(str(d))  # 03/05/2017
        data["h_" + str(n + 1)] = ch
        data["a_" + str(n + 1)] = a.encode('iso8859-15')
        n += 1
    return data


def main():
    # ICC: 1411001
    # LP2: 1411181
    # P2 : 1411168
    # DevWeb: 1411335
    # turma = "01"
    login_ = input("LOGIN: ")
    senha_ = getpass("SENHA: ")
    disc = input("DISCIPLINA: ")
    turma = input("TURMA: ")
    arq = input("ARQUIVO: ")
    jsessionid = controle.login(login_, senha_)
    data = processa_csv(disc, turma, arq)
    res = open("res.html", "wb")
    res.write(controle.chamada(data, jsessionid).read())
    res.close()
    print("PROCESSAMENTO ENCERRADO... VERIFIQUE CONTROLE ACADEMICO OU ARQUIVO res.html POR ERROS")

if __name__ == '__main__':
    main()
