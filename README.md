# Script para sorteio de amigo secreto
O script tem como entrada um arquivo CSV com uma lista de nomes, emails e sugestões de presente e após randomização envia o resultado do sorteio para cada participante via email.

## Utilização
    pip install -r requirements.txt
    cp .env.TEMPLATE .env

O campo **SENDGRID_API_KEY** deve receber a API Key do Sendgrid. Feito isso:

    python main.py