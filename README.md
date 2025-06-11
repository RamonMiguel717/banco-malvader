# 💰 Sistema Bancário Digital

## 🧾 Descrição

Este projeto tem como objetivo o desenvolvimento de um **Sistema Bancário completo** utilizando a linguagem **Python** com persistência de dados em **MySQL**. O sistema contará com:

1. Cadastro, listagem, modificação e remoção de usuários e contas.
2. Operações bancárias: saque, depósito, transferência e emissão de extratos.
3. Criptografia de senhas e validação de dados (CPF, email, senha).
4. Controle de acesso com autenticação e autorização por tipo de usuário.
5. Exportação de dados em diferentes formatos (ex: JSON, CSV, PDF).
6. Interface específica para cada tipo de usuário (cliente, gerente, administrador).
7. Camadas bem definidas: Models, Views, Controllers, DAO (Repositórios) e Services.
8. Aplicação de **Scrum** como metodologia ágil, com acompanhamento visual via **Kanban**.
9. Testes unitários utilizando Pytest;
10. Ambiente virtual para instalação de pacotes.

---

## 👥 Equipe

| Nome                  | Função                    |
|-----------------------|---------------------------|
| Ramon Miguel          | Desenvolvedor             |
| Maria Eduarda Marques | Desenvolvedora            |
| Rafael Canavarro      | Desenvolvedor             |

---

## 🧑‍💻 Tecnologias Utilizadas

- **Linguagem**: Python
- **Banco de Dados**: MySQL
- **Hospedagem**: FreeSQLDatabase.com
- **Metodologia**: Scrum + Kanban
- **Arquitetura**: MVC + DAO + Service Layer
- **Controle de Versão**: Git + GitHub
- **Bibliotecas**: 
  - `hashlib` (criptografia)
  - `mysql-connector` (integração com MySQL)
  - [Demais bibliotecas serão adicionadas conforme o progresso do projeto]

---

## 📂 Estrutura do Projeto

```bash
banco_digital/
├── controllers/         # Controladores (entrada do sistema)
├── models/              # Estruturas de dados (classes)
├── repository/          # Acesso ao banco de dados (DAO)
├── services/            # Regras de negócio (Service Layer)
├── utils/               # Funções auxiliares (ex: segurança)
├── views/               # Interfaces gráficas (em construção)
├── tests/               # Testes unitários 
├── main.py              # Ponto de entrada do sistema
└── README.md            # Documentação do projeto
