# sso-box
SSO implementation to personal projects.

## Protótipo

[Protótipo Figma](https://www.figma.com/file/VhpNdQifpvBaNvxGqEYVie/SSO?node-id=1%3A750&t=lNfAo7dvytvZzo8O-1)


## Modelagem


## Funcionalidades

 - [ ] Conectar sistema ao LDAP (multiplos LDAP)
 - [ ] Cadastro de usuários no banco de dados do sistema
 - [ ] Controle de perfis dos usuários (Perfis dinâmicos)
 - [ ] Habilitar e desabiltiar usuário no sistema
 - [ ] Refletir no sistema se o usuário estiver bloqueado no LDAP
 - [ ] Implementar a autenticação
    - [ ] Cadastrar dados da aplicação
        - [ ] cliend_id, redirect_uri, response_type
    - [ ] Vincular usuário com a aplicação
    - [ ] Autenticar usuário com aplicação (Gerar token de acesso vinculando usuário, aplicação e sessão)
    - [ ] Endpoint para retornar os dados pessoais do usuário logado
    - [ ] Endpoint para encessar a sessão e deletar o token


## Development Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres
    volumes:
      - ./data/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_NAME=${POSTGRES_NAME}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"

  web:
    image: pedro180698/sso_box
    command: python manage.py runserver 0.0.0.0:8000 --settings=sso_box.settings.prod
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG}
      # Database
      - POSTGRES_NAME=${POSTGRES_NAME}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - "80:8000"
      - "8080:8000"
    links:
      - db
    depends_on:
      - db
```
