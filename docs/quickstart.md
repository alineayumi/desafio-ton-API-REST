Este é um projeto base para subir APIs escaláveis em python diretamente no Heroku.

# Table of Contents

1. [Dependencias](#1-dependencias)
2. [Instalação](#2-instalação)
3. [Flask Framework](#3-flask-framework)
4. [Estrutura do Projeto](#4-estrutura-do-projeto)
5. [Rodando a Aplicação](#5-rodando-a-aplicação)
6. [Escalando a Aplicação](#6-escalando-a-aplicação)
7. [Subindo no Heroku](#7-subindo-no-heroku)

# 1. Dependencias

Para utilizar esse projeto serão necessários:

- pip (gestor de pacotes)
- [pipenv](https://github.com/pypa/pipenv) (gestor de ambiente virtual)
- vscode (recomendado)

# 2. Instalação

## 2.1 Clonando o projeto

* Crie um arquivo `.env` copiando o `.env.example` para setar as variaveis de ambiente. Os modos de deploy da API estão são as classes `ProductionConfig`, `StagingConfig`, `DevelopmentConfig` e `TestingConfig` do arquivo `config.py`. Para saber mais: https://flask.palletsprojects.com/en/1.1.x/config/


## 2.2 pipenv + vscode

Existem vantagens em utilizar o vscode com a extensãao para python e o pipenv juntos. o pipenv carrega automaticamente variáveis de ambiente setadas em um arquivo `.env`. Sete a seguinte configuracão de seu vscode: `"python.terminal.activateEnvironment": false`.

* Rode `pipenv install` para insalar as dependencias e `pipenv shell` para iniciar um terminal dentro do ambiente virtual.
    * Seu vscode deve estar da seguinte forma:
    ![Exemplo Vscode](img/vscode_env.png)
    * A extensão para python do vscode permite que você selecione o ambiente virtual do python para o intelisense funcionar dentro dele.
    * Você pode verificar se as variáveis de ambiente estão setadas rodando o comando `echo` no terminal.
    * utilize `pipenv --help` para obter ajuda.

## 3 [Flask Framework](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application)

APIs possuem basicamente três responsabilidades:

- Iniciar a aplicação [1]
- Declarar as rotas [2]
- Declarar a operação de cada rota [3]

Um aplicação minima em Flask pode ser feita da seguinte forma minimalista:

```python
from flask import Flask
app = Flask(__name__) #[1]

@app.route('/') #[2]
def hello_world(): #[3]
    return 'Hello, World!'
```

Para projetos maiores, essa forma não é escalável. O que esse projeto sujerir uma arquitetura escalável.

# 4 Estrutura do Projeto

## 4.1 Arquivos de configuração

São responsáveis por [1]. (Não precisam ser editados)

- `config.py` configura a api para os ambientes de produção ou desenvolvimento. Para selecionar o ambiente desejado, basta setar a variavel de ambiente no arquivo .env: `APP_SETTINGS="config.DevelopmentConfig"`

- `manager.py` é o arquivo principal, que cria uma instancia da aplicação local com `python manager.py runserver` e também pode gerar um console local com o contexto da aplicação com `python manager.py shell`

- `Procfile` configura a subida da aplicação no Heroku.

## 4.2 API

### `app/mock_api`

Contém a api em si, cuida das partes [2] e [3]

- [2] `blueprint.py` é responsável por declarar uma rota para cada classe que extende a classe base `Resource` definida no `controller.py`.

- [3] `controller.py` é responsável por declarar os métodos que serão chamados em cada rota declarada em `blueprint.py`.

- `helper.py` é útil para escrever os metodos em si, e nao poluir o controller.

### `app/resources/responses`

Declara formatos de resposta padrão a serem utilizados pela api.


## 4.3 Authentication

Existem dois modelos de autentificacao, por token simples ou por JWT, que estao descritos no proximo item

### Token 

Declara um decorator `@requires_auth` para proteger as rotas desejadas da api. Ele utiliza como comparação a variável de ambiente `APPLICATION_KEY`.

```python
class DoSomething(Resource):

    @requires_auth
    def get(self):
        return {
            "mensagem" : "ola"
        }
```

### JWT

Esse esquema eh responsavel por gerar um token vom validade de 1h para o usuario e senha passados. Cada usuario e senha possui uma lista de scopes definida no banco de dados, que dizem a quais rotas ele tem acesso.

Precisa-se de um banco postgres, com a seguinte tabela:

```sql
create table app_clients
(
	_password text,
	updated_at timestamp,
	created_at timestamp,
	name varchar(255),
	id varchar(36) not null
		constraint app_clients3_pk
			primary key,
	scopes text
);

alter table app_clients owner to rodrigomaluf;
```

#### criando um usuario

Para criar um primeiro usuario, de um `python manager.py shell` e execute:

```python
a = AppClients('<client_name>','<client_password>')
db.session.add(a)
db.session.commit()
```

#### solicitando um token 

Os tokens tem validacao de 1h, e sao obtidos da seguinte forma:

```
POST /auth HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "username": "joe",
    "password": "pass"
}
```

Com a seguinte resposta:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E"
}
```

Para fazer requests, basta passar o header: `Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E
`
#### @check_scopes

Esse decorador aceita uma lista de scopes, necessarios para acessar essa rota. Qualquer usuario que possua pelo menos um desses scopes podera utilizar a rota

```python
class DoSomething(Resource):

    @check_scopes(scopes=["sales", "chat"])
    def get(self):
        return {
            "mensagem" : "ola"
        }
```
### `app/__init__.py`

Esse arquivo declara exporta uma função `create_app` que realiza os passos [1],[2] e [3]. Essa função é chamada no `manager.py`, que é quem de fato roda a aplicaçaão.

### Sobre arquivos `__init__.py`

No python, diferente delinguagens como `Node.js`, quando se coloca arquivos `.py` dentro de pastas, é necessário colocar dentro da mesma pasta um arquivo `__init__.py` que diz quais funções ou variáveis poderão ser importadas por outros arquivos arquivos `.py` que estão fora dessa pasta.

[Referência](https://docs.python.org/3/tutorial/modules.html#packages)

# 5 Rodando a Aplicação

Dentro do ambiente virtual, rode a aplicação com `python manager.py runserver`.

Teste a rota declarada no `blueprint.py` com GET `http://127.0.0.1:5000/sample-api/do-something`


# 6 Escalando a Aplicação

Para criar uma nova api com outro prefixo: 

* Clone a pasta `mock_api` e seus conteúdos com um novo nome, digamos `outra_api`
* Renomeie o prefixo e o nome da `blueprint.py` para `outra-api`:

```python
bp = Blueprint("outra-api", __name__, url_prefix= "/outra-api" )
```

* Em `app/__init__.py` registre as novas blueprints:

```python
def create_app(config):

    from .mock_api import setup_blueprint as mock_api_blueprint
    from .outra_api import setup_blueprint as outra_api_blueprint

    # create application instance
    app = Flask(__name__)

    # config from object
    app.config.from_object(config)

    # repetir isso para outros modulos
    app.register_blueprint(mock_api_blueprint())
    app.register_blueprint(outra_api_blueprint())
    
    return app
```

# 7 Subindo no Heroku

* Instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
* Logue na sua conta do heroku e crie um novo `app` (`sample-api`)
* Dentro dele, em settings, procure a url do git, vai ser algo do tipo:
```
https://git.heroku.com/sample-api.git
```
* No seu repositorio, adicione esse remote com: 
```
git remote add heroku https://git.heroku.com/sample-api.git
```
* De um push `git push heroku master`