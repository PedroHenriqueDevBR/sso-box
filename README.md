# sso-box
SSO implementation to personal projects.

## Protótipo

[Protótipo Figma](https://www.figma.com/file/VhpNdQifpvBaNvxGqEYVie/SSO?node-id=1%3A750&t=lNfAo7dvytvZzo8O-1)


## Modelagem


## Funcionalidades

 - [X] Conectar sistema ao LDAP (multiplos LDAP)
 - [X] Cadastro de usuários no banco de dados do sistema
 - [X] Controle de perfis dos usuários (Perfis dinâmicos)
 - [X] Habilitar e desabiltiar usuário no sistema
 - [ ] Refletir no sistema se o usuário estiver bloqueado no LDAP
 - [X] Implementar a autenticação
    - [X] Cadastrar dados da aplicação
        - [X] cliend_id, redirect_uri, response_type
    - [ ] Vincular usuário com a aplicação
    - [ ] Autenticar usuário com aplicação (Gerar token de acesso vinculando usuário, aplicação e sessão)
    - [ ] Endpoint para retornar os dados pessoais do usuário logado
    - [ ] Endpoint para encessar a sessão e deletar o token
