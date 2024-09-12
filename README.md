# Minha API

Este projeto faz parte do MVP03 da Disciplina **Desenvolvimento Full Stack Avançado** 

---
## Como executar 

# Criar ambiente virtual

python -m venv env

# Ative o ambiente 
# Utilizando o S.O. Linux 

```
$ source <venv>/bin/activate
```

# Utilizando o S.O. Windows
```
usando o cmd.exe C:\> <venv>\Scripts\activate.bat
usando o PS C:\> <venv>\Scripts\Activate.ps1
```

# Segue o link da documentação caso tenha algum problema 
# https://docs.python.org/3/library/venv.html
# https://virtualenv.pypa.io/en/latest/installation.html


# Instale as bibliotecas
```
(env)$ pip install -r requirements.txt
```
Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

# Inicializa o serviço
Para executar a API  basta executar:
```
(env)$ flask run --host 0.0.0.0 --port 5000
```
Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```