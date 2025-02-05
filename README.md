
# Conversor de Imagem para .obj
  
Este projeto é uma aplicação web Flask que permite aos usuários fazer upload de imagens e convertê-las em objetos 3D.
## Pré-requisitos
-   Docker
-   Docker Compose

## Instalação e Execução

## Instalação e Execução

 1. **Clone o repositório**
	

``` 
$  git clone https://github.com/Eduardo-Cezar/img2obj.git
```
``` 
cd img2obj
```
2. **Inicie os containers**

	
``` 
docker-compose up  --build
```
3. **Acesse a aplicação**

- Abra o navegador e acesse: `http://localhost:5000`
   
``` 
.
├── app.py              # Aplicação Flask principal
├── docker-compose.yml  # Configuração dos containers
├── Dockerfile          # Configuração do container da aplicação
├── requirements.txt    # Dependências Python
├── static/             # Arquivos estáticos
│   └── uploads/        # Diretório para uploads de imagens
└── templates/          # Templates HTML
```

## Comandos Úteis

- Iniciar a aplicação
```
docker-compose up
```


 -  Acessar o banco de dados
   ``` 
docker-compose exec  db  psql  -U  postgres  -d  banco_notas
   ```
  - Reconstruir os containers
   ``` 
   docker-compose up  --build
``` 
  - Parar a aplicação
   ``` 
docker-compose down
``` 