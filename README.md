[English Version](/README-en.md)
# Instalção

## Bibliotecas Python
Esse projeto foi desenvolvido utilizado o gerenciador de pacotes [Poetry](https://python-poetry.org/)

Para instalar as dependências, use o comando:
>poetry install

Dentro do diretório do projeto

O arquivo "requirements.txt" possui uma lista das dependências, mas não é garantido que estará atualizado.

# MongoDB

O arquivo "docker-compose.yml" possui as receitas para instalação do Mongo-DB e Mongo-express


# Configuração
O arquivo ".env" precisa ser criado na raíz do projeto. Um exemplo do conteúdo esperado pode ser encontrado em [".env.sample"](/.env.sample)

A única variável que precisa ser alterada é a "ANTI_CAPTCH_API_KEY", que é a chave para a API do [ANTI-CAPTCHA](https://anti-captcha.com/)

Se o banco de dados vai ficar aberto para acesso via internet, as demais variáveis também devem ser alteradas

# Funcionalidades

- Obtenção da chave das notas fiscais, a partir do link fornecido 
    - ![70%](https://progress-bar.dev/90)
      - Testado apenas para notas de combustível e alguns casos ainda apresentam erros

- Download de notas fiscais a partir das chaves
  - NFe  ![100%](https://progress-bar.dev/100)
  - NFCe ![10%](https://progress-bar.dev/10)

- Processamento
  - Identificar informações (CPF, nome, etc.) nas notas fiscais ![0%](https://progress-bar.dev/0)
  - Obter nomes a partir do CPF ![0%](https://progress-bar.dev/0)

  - Identificar se consumidor é secretário do deputado ![0%](https://progress-bar.dev/0)
