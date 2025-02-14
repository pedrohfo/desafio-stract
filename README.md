# Desafio Stract

Este projeto utiliza Python e Flask para tratar dados que vêm de APIs da Stract e os apresentar no navegador em forma de tabelas.

## Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)
- Git (para clonar o repositório)

## Configuração do Projeto

### 1. Clonar o Repositório

Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/pedrohfo/desafio-stract.git
cd desafio-stract
```

### 2. Criar e Ativar um Ambiente Virtual

No Linux/MacOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Execução

```bash
python app.py
```

### 5. APIs

As plataformas para serem usadas como parâmetro nas APIs são: meta_ads, ga4, tiktok_insights

/
/{{plataforma}}
/{{plataforma}}/resumo
/geral
/geral/resumo
