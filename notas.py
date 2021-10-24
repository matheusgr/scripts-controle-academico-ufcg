import csv
from getpass import getpass
import math

import controle


def _processa_csv(csv_f):
    # HEADER: matr,n1,n2,n3,f
    # CONTROLE ACADEMICO: n1_matr, n2_matr, .. final = f
    data = {}
    # arredondando 1 casa decimal, usando virgulas no lugar de ponto:
    conv = lambda y: ("%.1f" % (math.ceil(10 * float(y)) / 10)).replace('.', ',')
    with open(csv_f, encoding='utf-8-sig', newline='') as csvfile:
        notas_reader = csv.reader(csvfile)
        header = next(notas_reader)
        for linha in notas_reader:
            matr = linha[0]
            for f, n in zip(header[1:], linha[1:]):
                if n:
                    data[f + "_" + matr] = conv(float(n.replace(',','.')))
    return data


def processa_csv(codigo, turma, pesos, csv_f):
    data = controle.base(codigo, turma, "ProfessorTurmaNotasConfirmar")
    data["notas"] = str(len(pesos))
    data["numNotas"] = str(len(pesos))
    for n, peso in enumerate(pesos):
        data["peso" + str(n + 1)] = str(peso)
    data.update(_processa_csv(csv_f))
    return data


def main():
    login_ = input("LOGIN: ")
    senha_ = getpass("SENHA: ")
    # ICC: 1411001
    # LP2: 1411181
    # P2 : 1411168
    # DevWeb: 1411335
    # Turma: 01
    # Pesos: 10 15 20
    disc = input("DISCIPLINA: ")
    turma = input("TURMA: ")
    arq = input("ARQUIVO: ")
    pesos = input("PESOS (Separado por espaco): ")
    data = processa_csv(disc, turma, [int(x) for x in pesos.split()], arq)
    jsessionid = controle.login(login_, senha_)
    res = open("res.html", "wb")
    res.write(controle.chamada(data, jsessionid).read())
    res.close()
    print("PROCESSAMENTO ENCERRADO... VERIFIQUE CONTROLE ACADEMICO OU ARQUIVO res.html POR ERROS")


if __name__ == "__main__":
    main()
