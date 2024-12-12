# Sistema de Enquetes

Um sistema de enquetes desenvolvido em Python, utilizando Flask, Flask-RESTful, Flask-JWT-Extended e outras bibliotecas. Esta aplicação permite criar e gerenciar enquetes, com autenticação JWT para proteger os endpoints.

## 🚀 Funcionalidades
- Criação e gerenciamento de enquetes.
- Autenticação de usuários via JWT.
- API documentada com Swagger.
- Banco de dados gerenciado com SQLAlchemy.

---

## 📦 Instalação e Configuração

  Siga os passos abaixo para configurar o ambiente local e executar o projeto.

### Pré-requisitos
- **Python** 3.9 ou superior.
- **pip** (gerenciador de pacotes Python).
- **virtualenv** (para criar ambientes virtuais Python).

### Etapas de instalação

1. **Clone o repositório do projeto:**
  ```bash
  git clone <URL_DO_REPOSITORIO>
  cd <PASTA_DO_PROJETO>
  ```
2. **Crie e ative um ambiente virtual (recomendado):**
  ```
  Linux/Mac:
    1. python3 -m venv ambvir
    2. source ambvir/bin/activate
  ```

  ```
  No Windows:
    1. python -m venv ambvir
    2. .\ambvir\Scripts\activate
  ```

3. **Instale as dependências: Com o ambiente virtual ativado, execute:**
  ```bash
  pip install -r requirements.txt
  ```
4. **Inicialização do servidor no ambiente virtual**
  ```bash
  python run.py
  ```
## Documentação com Swagger dos endpoints disponíveis 
  
> Acesse em seu navegador http://localhost:5000/apidocs/