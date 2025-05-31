# 💳 E-commerce Microservice - Pagamentos Service

<div align="center">

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-2496ED?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/r/bpsbrunopinheiro/pagamentos-service)
[![Security](https://img.shields.io/badge/Security-Verified-brightgreen?style=flat-square&logo=shield&logoColor=white)](#-segurança-e-vulnerabilidades)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](#licença)

</div>

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Características](#-características)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Uso](#-uso)
- [API Reference](#-api-reference)
- [Segurança e Vulnerabilidades](#-segurança-e-vulnerabilidades)
- [Backup e Recuperação](#-backup-e-recuperação)
- [Monitoramento](#-monitoramento)
- [Troubleshooting](#-troubleshooting)
- [Contribuição](#-contribuição)

## 🎯 Visão Geral

Este projeto implementa um **microserviço containerizado** para gerenciamento de pagamentos de e-commerce, desenvolvido com **Python/Flask** e **MySQL**, seguindo as melhores práticas de DevOps e arquitetura de containers.

### 🚨 Alerta de Segurança

> ⚠️ **Versão Recomendada**: `bpsbrunopinheiro/pagamentos-service:v1.0.1`  
> ✅ **Status**: Vulnerabilidades críticas corrigidas  
> 🔒 **Produção**: Aprovado para uso em produção

## ✨ Características

### 🏗️ Arquitetura e Infraestrutura

- ✅ **Containerização completa** com Docker e Docker Compose
- ✅ **Ambientes isolados** (desenvolvimento/produção)
- ✅ **Multi-stage builds** para otimização de imagens
- ✅ **Redes Docker isoladas** para cada ambiente
- ✅ **Volumes persistentes** com nomenclatura diferenciada

### 🛡️ Segurança

- ✅ **Usuário não-root** nos containers
- ✅ **Imagens Alpine Linux** minimalistas
- ✅ **Análise de vulnerabilidades** com Docker Scout
- ✅ **Variáveis de ambiente** seguras
- ✅ **Health checks** implementados

### 🔧 Funcionalidades

- ✅ **Processamento de pagamentos** (Cartão, PIX, Boleto)
- ✅ **Gestão de formas de pagamento**
- ✅ **Histórico de transações**
- ✅ **Interface web** intuitiva
- ✅ **API RESTful** completa

## 🏗️ Arquitetura

```mermaid
graph TB
    subgraph "Ambiente Desenvolvimento"
        WEB1[Interface Web :8787] --> APP1[pagamentos-service]
        APP1 --> DB1[MySQL :3306]
        APP1 -.-> NET1[dev-network]
        DB1 -.-> NET1
        DB1 --> VOL1[mysql_data_dev]
    end

    subgraph "Ambiente Produção"
        WEB2[Interface Web :8787] --> APP2[pagamentos-service]
        APP2 --> DB2[MySQL :3306]
        APP2 -.-> NET2[prod-network]
        DB2 -.-> NET2
        DB2 --> VOL2[mysql_data_prod]
    end

    subgraph "Docker Hub"
        HUB[bpsbrunopinheiro/pagamentos-service]
    end

    APP2 -.->|pulls from| HUB
```

### 📁 Estrutura do Projeto

```
feature-pagamentos/
├── 📄 README.md                    # Documentação principal
├── 🔧 docker-compose.yml           # Configuração base
├── 🔧 docker-compose.dev.yml       # Override desenvolvimento
├── 🔧 docker-compose.prod.yml      # Override produção
├── 🔐 .env.dev                     # Variáveis desenvolvimento
├── 🔐 .env.prod                    # Variáveis produção
├── 🗄️ init.sql                     # Inicialização banco
└── 📁 pagamentos-service/
    ├── 🐍 app.py                   # Aplicação Flask
    ├── 🐳 dockerfile               # Produção (multistage)
    ├── 🐳 dockerfile.dev           # Desenvolvimento
    ├── 📦 requirements.txt         # Dependências Python
    └── 📁 templates/
        └── 🌐 index.html           # Interface web
```

## 🔧 Pré-requisitos

| Ferramenta         | Versão Mínima | Comando de Verificação     |
| ------------------ | ------------- | -------------------------- |
| **Docker Desktop** | 4.0+          | `docker --version`         |
| **Docker Compose** | 2.0+          | `docker-compose --version` |
| **Git**            | 2.0+          | `git --version`            |

### 📋 Verificação do Ambiente

```bash
# Verificar todas as dependências
echo "🔍 Verificando dependências..."
docker --version && echo "✅ Docker OK" || echo "❌ Docker não encontrado"
docker-compose --version && echo "✅ Docker Compose OK" || echo "❌ Docker Compose não encontrado"
git --version && echo "✅ Git OK" || echo "❌ Git não encontrado"
```

## 🚀 Instalação e Configuração

### 1️⃣ Clone do Repositório

```bash
git clone <repository-url>
cd feature-pagamentos
```

### 2️⃣ Configuração de Ambiente

```bash
# Criar pasta para backups
mkdir -p backups

# Verificar arquivos de configuração
ls -la .env.*
```

### 3️⃣ Build das Imagens

```bash
# Build para desenvolvimento
docker build -f pagamentos-service/dockerfile.dev -t pagamentos-service:dev ./pagamentos-service

# Build para produção
docker build -f pagamentos-service/dockerfile -t bpsbrunopinheiro/pagamentos-service:v1.0.1 ./pagamentos-service
```

## 🎮 Uso

### 🔧 Ambiente de Desenvolvimento

```bash
# 1. Iniciar ambiente
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml up -d

# 2. Verificar status
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml ps

# 3. Acompanhar logs
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml logs -f

# 4. Parar ambiente
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml down
```

### 🏭 Ambiente de Produção

```bash
# 1. Configurar Docker Hub user no .env.prod
# DOCKER_HUB_USER=seuusuario

# 2. Iniciar ambiente
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d

# 3. Verificar status
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml ps

# 4. Verificar logs
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml logs -f
```

### 🌐 Acesso à Aplicação

| Serviço              | URL                                    | Descrição              |
| -------------------- | -------------------------------------- | ---------------------- |
| **Interface Web**    | http://localhost:8787                  | Dashboard principal    |
| **Health Check**     | http://localhost:8787/status           | Status da aplicação    |
| **API Pagamentos**   | http://localhost:8787/                 | Endpoint principal     |
| **Formas Pagamento** | http://localhost:8787/formas_pagamento | Gestão de métodos      |
| **Histórico**        | http://localhost:8787/historico        | Transações realizadas  |
| **MySQL (dev)**      | localhost:3309                         | Acesso direto ao banco |

## 📚 API Reference

### 🔍 Endpoints Disponíveis

| Método   | Endpoint            | Descrição            | Exemplo                                                                                  |
| -------- | ------------------- | -------------------- | ---------------------------------------------------------------------------------------- |
| **GET**  | `/`                 | Interface web        | `curl http://localhost:8787/`                                                            |
| **GET**  | `/status`           | Health check         | `curl http://localhost:8787/status`                                                      |
| **GET**  | `/formas_pagamento` | Listar métodos       | `curl http://localhost:8787/formas_pagamento`                                            |
| **POST** | `/formas_pagamento` | Cadastrar método     | `curl -X POST -d "forma_pagamento=Cartão Débito" http://localhost:8787/formas_pagamento` |
| **POST** | `/`                 | Processar pagamento  | `curl -X POST -d "cartao=4111111111111111" http://localhost:8787/`                       |
| **GET**  | `/historico`        | Histórico transações | `curl http://localhost:8787/historico`                                                   |

### 💳 Tipos de Pagamento Suportados

#### Cartão de Crédito

```bash
curl -X POST http://localhost:8787/ \
  -d "cartao=4111111111111111"
```

#### PIX

```bash
curl -X POST http://localhost:8787/ \
  -d "pix=usuario@exemplo.com"
```

#### Boleto

```bash
curl -X POST http://localhost:8787/ \
  -d "boleto=123456789"
```

### 📊 Responses de Exemplo

```json
// GET /status
{
  "status": "healthy",
  "service": "pagamentos-service",
  "timestamp": "2025-05-31T10:30:00Z"
}

// GET /historico
[
  {
    "id": 1,
    "tipo": "cartao",
    "detalhes": "Pagamento processado via Stripe",
    "data_criacao": "2025-05-31 10:30:00"
  }
]
```

## 🛡️ Segurança e Vulnerabilidades

### 🔒 Status Atual de Segurança

> ✅ **Versão Segura**: `v1.0.1`  
> 🛡️ **Vulnerabilidades Críticas**: 0  
> 📊 **Última Verificação**: 31/05/2025

### 🔍 Verificação de Segurança

```bash
# Análise completa de segurança
docker scout cves bpsbrunopinheiro/pagamentos-service:v1.0.1

# Verificação rápida
docker scout quickview bpsbrunopinheiro/pagamentos-service:v1.0.1

# Análise com Trivy (alternativo)
trivy image bpsbrunopinheiro/pagamentos-service:v1.0.1
```

### 📋 Dependências Seguras (v1.0.1)

| Dependência | Versão | Status    |
| ----------- | ------ | --------- |
| Flask       | 3.1.0  | ✅ Segura |
| Werkzeug    | 3.1.3  | ✅ Segura |
| Jinja2      | 3.1.6  | ✅ Segura |
| click       | 8.1.8  | ✅ Segura |
| PyMySQL     | 1.1.1  | ✅ Segura |

### 🛡️ Medidas de Segurança Implementadas

- **🔐 Usuário não-root**: Containers executam como `appuser`
- **🌐 Redes isoladas**: Comunicação segura entre containers
- **📦 Imagens minimalistas**: Alpine Linux reduz superfície de ataque
- **🔒 Secrets**: Variáveis sensíveis em arquivos `.env`
- **🚨 Health checks**: Monitoramento contínuo da aplicação

## 💾 Backup e Recuperação

### 📋 Comandos de Backup Testados

#### 🔧 Backup de Desenvolvimento

```bash
# Backup completo do volume MySQL (desenvolvimento)
docker run --rm \
  -v ecommerce_dev_mysql_data:/data:ro \
  -v "$(pwd)/backups:/backup" \
  alpine tar czf "/backup/mysql-volume-dev-$(date +%Y%m%d-%H%M%S).tar.gz" -C /data .

echo "✅ Backup de desenvolvimento concluído!"
```

#### 🏭 Backup de Produção

```bash
# Backup completo do volume MySQL (produção)
docker run --rm \
  -v ecommerce_prod_mysql_data:/data:ro \
  -v "$(pwd)/backups:/backup" \
  alpine tar czf "/backup/mysql-volume-prod-$(date +%Y%m%d-%H%M%S).tar.gz" -C /data .

echo "✅ Backup de produção concluído!"
```

### 🔄 Recuperação de Backup

```bash
# ⚠️ ATENÇÃO: Processo destrutivo - remove dados atuais

# 1. Parar ambiente
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml down

# 2. Remover volume existente
docker volume rm ecommerce_dev_mysql_data

# 3. Recriar volume
docker volume create ecommerce_dev_mysql_data

# 4. Restaurar backup (ajustar nome do arquivo)
BACKUP_FILE="mysql-volume-dev-20250531-103000.tar.gz"
docker run --rm \
  -v ecommerce_dev_mysql_data:/data \
  -v "$(pwd)/backups:/backup" \
  alpine tar xzf "/backup/$BACKUP_FILE" -C /data

# 5. Reiniciar ambiente
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### 📊 Verificação de Backups

```bash
# Listar backups disponíveis
ls -la ./backups/*.tar.gz

# Verificar tamanho dos backups
du -h ./backups/

# Verificar último backup criado
ls -t ./backups/*.tar.gz | head -1

# Testar integridade do backup
ULTIMO_BACKUP=$(ls -t ./backups/*.tar.gz | head -1)
docker run --rm -v "$(pwd)/backups:/backup" alpine \
  tar -tzf "/backup/$(basename $ULTIMO_BACKUP)" | head -10
```

## 📊 Monitoramento

### 🔍 Comandos de Monitoramento

```bash
# Status geral dos containers
docker ps --filter "name=ecommerce"

# Uso de recursos
docker stats

# Logs em tempo real
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml logs -f

# Verificar redes criadas
docker network ls | grep ecommerce

# Verificar volumes
docker volume ls | grep ecommerce
```

### 🗄️ Acesso ao Banco de Dados

```bash
# Conexão direta ao MySQL (desenvolvimento)
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml exec mysql-db \
  mysql -u root -proot ecommerce_db

# Verificação rápida de dados
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml exec mysql-db \
  mysql -u root -proot ecommerce_db -e "
    SHOW TABLES;
    SELECT COUNT(*) as total_transacoes FROM transacoes;
    SELECT COUNT(*) as total_formas_pagamento FROM pagamentos;
  "
```

### 📈 Health Checks

```bash
# Status da aplicação
curl -f http://localhost:8787/status || echo "❌ Aplicação não está respondendo"

# Teste de conectividade com banco
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml exec mysql-db \
  mysqladmin ping -u root -proot || echo "❌ MySQL não está respondendo"
```

## 🔧 Troubleshooting

### ❌ Problemas Comuns

#### Container não inicia

```bash
# Verificar logs detalhados
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml logs pagamentos-service

# Verificar configuração
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml config
```

#### Erro de conexão com banco

```bash
# Testar conectividade
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml exec mysql-db \
  mysql -u root -proot -e "SELECT 1"

# Verificar variáveis de ambiente
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml exec pagamentos-service \
  env | grep DB_
```

#### Problemas de permissão

```bash
# Recriar volumes com permissões corretas
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml down -v
docker volume prune -f
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml up -d
```

#### Porta já em uso

```bash
# Verificar processos usando a porta 8787
lsof -i :8787

# Parar containers conflitantes
docker stop $(docker ps -q --filter "publish=8787")
```

### 🧹 Limpeza Geral

```bash
# Parar todos os ambientes
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml down
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml down

# Limpeza completa do sistema
docker system prune -af
docker volume prune -f
```

## 🚀 Comandos Rápidos - Cheat Sheet

### 📋 Desenvolvimento

```bash
# Iniciar
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml up -d

# Logs
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml logs -f

# Parar
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml down
```

### 📋 Produção

```bash
# Iniciar
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d

# Logs
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Parar
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml down
```

### 📋 Build e Deploy

```bash
# Build produção
docker build -f pagamentos-service/dockerfile -t bpsbrunopinheiro/pagamentos-service:v1.0.1 ./pagamentos-service

# Tag latest
docker tag bpsbrunopinheiro/pagamentos-service:v1.0.1 bpsbrunopinheiro/pagamentos-service:latest

# Push
docker push bpsbrunopinheiro/pagamentos-service:v1.0.1
docker push bpsbrunopinheiro/pagamentos-service:latest
```

### 📋 Testes Rápidos

```bash
# Aplicação
curl http://localhost:8787/status

# API
curl http://localhost:8787/formas_pagamento

# Histórico
curl http://localhost:8787/historico
```

## 🤝 Contribuição

### 🔄 Fluxo de Desenvolvimento

1. **Fork** do repositório
2. **Clone** do fork: `git clone <fork-url>`
3. **Branch** para feature: `git checkout -b feature/nova-funcionalidade`
4. **Desenvolvimento** com testes
5. **Commit** com mensagens claras: `git commit -m "feat: adiciona nova funcionalidade"`
6. **Push** para o fork: `git push origin feature/nova-funcionalidade`
7. **Pull Request** com descrição detalhada

### 📝 Padrões de Commit

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Atualização de documentação
- `style:` Formatação de código
- `refactor:` Refatoração
- `test:` Adição de testes
- `chore:` Tarefas de manutenção

### 🧪 Testes

```bash
# Executar testes locais
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml up -d
./run-tests.sh
```

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

- 📧 **Email**: [seu-email@exemplo.com]
- 🐛 **Issues**: [GitHub Issues](link-para-issues)
- 📖 **Documentação**: [Wiki do Projeto](link-para-wiki)
- 🐳 **Docker Hub**: [bpsbrunopinheiro/pagamentos-service](https://hub.docker.com/r/bpsbrunopinheiro/pagamentos-service)

---

<div align="center">

**Desenvolvido para o ecossistema de microserviços**

![Footer](https://img.shields.io/badge/Made%20with-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Footer](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Footer](https://img.shields.io/badge/Made%20with-Flask-000000?style=flat-square&logo=flask&logoColor=white)

</div>
