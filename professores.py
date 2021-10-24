from bs4 import BeautifulSoup
import sys
import unicodedata

asc = lambda x: unicodedata.normalize('NFKD', x).encode('ascii','ignore')

def main():
    alunos = open(sys.argv[1], 'rb').read()
    cod, disciplina = processa(alunos, "Disciplina:")[0].split('-', 1)
    turma = processa(alunos, "Turma:")[0]
    for prof in processa(alunos, "Professores:"):
        nome = disciplina.strip().replace('/', '')
        print(','.join(['"' + x + '"' for x in [nome, turma, prof]]))
                

def processa(html, termo):
    soup = BeautifulSoup(html, 'html.parser')
    for tb in soup.find_all('div', {'class': 'row'}):
        found = False
        for div in tb.find_all('div'):
            if found:
                return div.getText().strip().split('\n')
            if div.getText() == termo:
                found = True
                

if __name__ == "__main__":
    main()
