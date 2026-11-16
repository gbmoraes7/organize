# Controle Financeiro

Aplicação web para registrar receitas e despesas, acompanhar investimentos e consultar relatórios. O projeto usa Flask e PostgreSQL e segue a arquitetura MVC: `models/` (dados), `views/` (páginas Jinja), `controllers/` (rotas por funcionalidade) e `services/` (regras do relatório). O fluxo completo e a paleta de cores estão em [`docs/arquitetura.md`](docs/arquitetura.md).

## 1. Antes de começar

Este guia considera que você já tem **Git e VS Code**. Para rodar o sistema completo, tenha **Python 3.12** e **PostgreSQL** instalados. Se faltar algum deles, consulte as instruções de instalação para o seu sistema no [site do Python](https://www.python.org/downloads/) ou no [site do PostgreSQL](https://www.postgresql.org/download/).

Clone o repositório pelo GitHub e abra no VS Code a pasta que contém `app.py` e `requirements.txt`. Rode os comandos abaixo no terminal dessa pasta.

## 2. Instale as dependências do projeto

**Windows (PowerShell)**

```powershell
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Linux**

```bash
python3.12 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Se `python3 --version` já mostrar a versão 3.12, você pode usar `python3` no lugar de `python3.12`. O primeiro comando cria a pasta `venv` automaticamente. O `requirements.txt` instala Flask e as demais bibliotecas. Não precisa de Node.js ou Live Server.

## 3. Configure o banco local

Inicie o PostgreSQL. Abra o **SQL Shell (psql)** no Windows e entre como `postgres`. No Linux, rode `sudo -u postgres psql`. No terminal do PostgreSQL, execute uma linha por vez:

```sql
CREATE ROLE financeiro_local LOGIN;
\password financeiro_local
CREATE DATABASE financeiro_local_db OWNER financeiro_local;
\q
```

Quando o `\password` pedir uma senha, escolha uma para o usuário `financeiro_local`. Se o usuário e o banco já existirem, não precisa criá-los de novo.

Crie o arquivo **`.env` ao lado do `app.py`** a partir do exemplo:

**Windows (PowerShell)**

```powershell
Copy-Item .env.example .env
```

**Linux**

```bash
cp .env.example .env
```

Abra o `.env` no VS Code e substitua `SUA_SENHA` pela senha de `financeiro_local`. A linha deve ficar assim:

```dotenv
DATABASE_URL=postgresql://financeiro_local:SUA_SENHA@127.0.0.1:5432/financeiro_local_db
```

Se seu PostgreSQL usar outra porta, troque `5432` pela porta correta. Se a senha tiver símbolos reservados, codifique-os na URL. Por exemplo, `@` vira `%40` e `#` vira `%23`.

## 4. Rode a aplicação

**Windows (PowerShell)**

```powershell
.\venv\Scripts\python.exe app.py
```

**Linux**

```bash
source venv/bin/activate
python app.py
``` 

Abra [http://127.0.0.1:5000](http://127.0.0.1:5000). O Flask cria as tabelas na primeira execução. Para conferir se está funcionando, cadastre um lançamento de teste e veja se aparece na lista. Para parar o Flask, pressione `Ctrl+C`.

Nas próximas vezes, basta verificar se o PostgreSQL está rodando e repetir esta etapa. Não precisa recriar o banco nem o `venv`. Não envie o `.env` nem a pasta `venv` ao GitHub.
