# 🐳 E-commerce Microservice - Itens Service

Este projeto implementa um microserviço containerizado para gerenciamento de itens de um e-commerce, utilizando **Docker**, **Flask**, **MySQL** e boas práticas de DevOps.

# Docker Hub

Link da imagem no Docker hub - [carmonoca/itens-service](https://hub.docker.com/repository/docker/carmonoca/itens-service/general)

## 🛡️ **ALERTA DE SEGURANÇA**

⚠️ **Use sempre a versão segura**: `carmonoca/itens-service:v1.0.1`  
✅ **Vulnerabilidade crítica CVE-2024-36039 corrigida** (PyMySQL SQL Injection - CVSS 9.8)  
🔒 **Status atual**: 0 Críticas, 0 Altas, 0 Médias, 2 Baixas  
📖 **Detalhes**: [Ver seção de correções de segurança](#-correções-de-segurança-implementadas)

## 📋 Requisitos Atendidos

✅ **Aplicação containerizada** em Python/Flask  
✅ **Banco de dados relacional** MySQL em container  
✅ **Docker Compose** para orquestração  
✅ **Ambientes separados** (dev/prod) com .env  
✅ **Redes isoladas** para cada ambiente  
✅ **Volumes apropriados** com diferenciação  
✅ **Dockerfile otimizado** com multistage build  
✅ **Imagens Alpine** leves e seguras  
✅ **Usuário não-root** para segurança  
✅ **Comunicação segura** entre containers  
✅ **Health checks** implementados  
✅ **Pronto para Docker Hub** com versionamento  

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    AMBIENTE DESENVOLVIMENTO                │
├─────────────────────────────────────────────────────────────┤
│  itens-service:8383  ◄─────────► mysql-db:3306           │
│  (dev-network)                    (dev-network)            │
│  Volume: ./itens-service:/app     Volume: mysql_data_dev    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     AMBIENTE PRODUÇÃO                      │
├─────────────────────────────────────────────────────────────┤
│  itens-service:8383  ◄─────────► mysql-db:3306           │
│  (prod-network)                   (prod-network)           │
│  Image: dockerhub                 Volume: mysql_data_prod   │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Pré-requisitos

- Docker Desktop 4.0+
- Docker Compose 2.0+
- PowerShell (Windows)

## 🚀 Comandos de Execução

### **DESENVOLVIMENTO**

```powershell
# 1. Subir ambiente de desenvolvimento
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d

# 2. Acompanhar logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev logs -f

# 3. Parar ambiente
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev down

# 4. Build (se necessário)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev build --no-cache
```

Renderiza a página inicial com o formulário para cadastro de itens e a lista de itens cadastrados.

### `POST /itens`

Cadastra um novo item com base nos dados fornecidos no formulário.

### `GET /itens`

Retorna a lista de itens cadastrados.

### `GET /itens/<int:item_id>`

Retorna os detalhes de um item específico.

### `PUT /itens/<int:item_id>`

Atualiza os dados de um item específico.

### `DELETE /itens/<int:item_id>`

Remove um item específico.

### `GET /status`

Retorna o status do serviço.

## Exemplos de Requisições e Respostas

### Cadastro de Item

**Requisição:**
```sh
curl -X POST -d "nome=Item1&descricao=Descrição do Item1&preco=10.00" http://0.0.0.0:8383/itens
````

### **PRODUÇÃO**

```powershell
# 1. Configure seu usuário no .env.prod (OBRIGATÓRIO)
# Edite DOCKER_HUB_USER=seuusuario no arquivo .env.prod

# 2. Build da imagem para produção
docker build -t seuusuario/itens-service:v1.0.0 -t seuusuario/itens-service:latest ./itens-service/

# 3. Login no Docker Hub
docker login

# 4. Push da imagem
docker push seuusuario/itens-service:v1.0.0
docker push seuusuario/itens-service:latest

# 5. Subir ambiente de produção
docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d

# 6. Verificar status
docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod ps

# 7. Logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod logs -f
```

### **🔥 PRODUÇÃO - EXECUTADO**

```powershell
# Build realizado
docker build -f itens-service/dockerfile -t carmonoca/itens-service:v1.0.0 ./itens-service

# Tag latest criada
docker tag carmonoca/itens-service:v1.0.0 carmonoca/itens-service:latest

# Push executado com sucesso
docker push carmonoca/itens-service:v1.0.0
docker push carmonoca/itens-service:latest

# ✅ Imagens disponíveis no Docker Hub:
# - carmonoca/itens-service:v1.0.0
# - carmonoca/itens-service:latest

# Subir produção com imagem do Docker Hub
docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod up -d
```

## 🔒 **Análise de Segurança**

### 📋 **Índice de Segurança:**
- [📊 Análise Inicial (v1.0.0)](#-análise-inicial-executada-carmonoca)
- [🛠️ Correções Implementadas (v1.0.1)](#-correções-de-segurança-implementadas)
- [📈 Processo de Correção](#-processo-de-correção-documentado)
- [🎯 Verificação Atual](#-comando-para-verificar-segurança-atual)
- [📋 Próximos Passos](#-próximos-passos-de-segurança)

```powershell
# Docker Scout (recomendado)
docker scout cves seuusuario/itens-service:latest

# Trivy (alternativo)
trivy image seuusuario/itens-service:latest

# Verificação rápida
docker scout quickview seuusuario/itens-service:latest
```

### **🛡️ ANÁLISE INICIAL EXECUTADA**

```powershell
# Comando executado:
docker scout cves carmonoca/itens-service:v1.0.0

# 📊 RESULTADO DA ANÁLISE INICIAL:
# ✅ Imagem analisada: carmonoca/itens-service:v1.0.0
# 📦 74 packages indexados
# ⚠️  7 vulnerabilidades encontradas em 4 packages:

# 🔴 CRITICAL (1):
# - pymysql 1.1.0 → CVE-2024-36039 (SQL Injection)

# 🟠 HIGH (2):  
# - cryptography 41.0.7 → CVE-2023-50782, CVE-2024-26130

# 🟡 MEDIUM (3):
# - cryptography 41.0.7 → CVE-2024-0727, GHSA-h4gh-qq45-vh27
# - requests 2.31.0 → CVE-2024-35195

# 🟢 LOW (1):
# - flask 3.1.0 → CVE-2025-47278

# 💡 Recomendações para próxima versão:
# - Atualizar pymysql para 1.1.1+
# - Atualizar cryptography para 43.0.1+  
# - Atualizar requests para 2.32.0+
# - Atualizar flask para 3.1.1+
```

### **🛠️ CORREÇÕES DE SEGURANÇA IMPLEMENTADAS**

#### **🚨 Vulnerabilidade Crítica Corrigida (v1.0.1)**

**CVE-2024-36039 - PyMySQL SQL Injection**
- **CVSS Score**: 9.8/10.0 (CRÍTICO)
- **Biblioteca**: PyMySQL 1.1.0 → **PyMySQL 1.1.1**
- **Tipo**: SQL Injection vulnerability
- **Status**: ✅ **CORRIGIDO**

```powershell
# ⚡ AÇÃO IMEDIATA EXECUTADA:
# 1. Atualizado requirements.txt: PyMySQL==1.1.1
# 2. Rebuild da imagem: carmonoca/itens-service:v1.0.1
# 3. Verificação de segurança confirmada

# 📋 Comando de correção:
docker build -f itens-service/dockerfile -t carmonoca/itens-service:v1.0.1 ./itens-service

# ✅ RESULTADO DA VERIFICAÇÃO PÓS-CORREÇÃO:
docker scout quickview carmonoca/itens-service:v1.0.1

# 🎯 VULNERABILIDADES APÓS CORREÇÃO:
# ✅ 0 Críticas (era 1)
# ✅ 0 Altas (era 2) 
# ✅ 0 Médias (era 3)
# 🟡 2 Baixas (era 1)
```

#### **📊 Comparativo de Segurança**

| Versão | Críticas | Altas | Médias | Baixas | Status |
|--------|----------|-------|--------|--------|--------|
| v1.0.0 | 🔴 **1** | 🟠 **2** | 🟡 **3** | 🟢 **1** | ❌ Vulnerável |
| v1.0.1 | ✅ **0** | ✅ **0** | ✅ **0** | 🟡 **2** | ✅ Seguro |

#### **🔄 Outras Atualizações de Segurança Aplicadas**

**Dependências Atualizadas no requirements.txt:**

```diff
# Correções críticas e de alta prioridade aplicadas:
- PyMySQL==1.1.0     → PyMySQL==1.1.1     # ✅ CVE-2024-36039 (Critical)
- cryptography==41.0.7 → cryptography==43.0.1 # ✅ CVE-2023-50782, CVE-2024-26130 (High)
- requests==2.31.0   → requests==2.32.0   # ✅ CVE-2024-35195 (Medium)

# Dependências mantidas (baixo risco):
- Flask==3.1.0       # 🟡 CVE-2025-47278 (Low - CVSS 1.8)
```

#### **📈 Processo de Correção Documentado**

```powershell
# 🔍 1. DETECÇÃO DA VULNERABILIDADE
docker scout cves carmonoca/itens-service:v1.0.0

# 🔧 2. ANÁLISE DETALHADA CVE-2024-36039
# Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
# Base Score: 9.8 (Critical)
# Affected: PyMySQL 1.1.0
# Fixed in: PyMySQL 1.1.1+

# ⚡ 3. CORREÇÃO IMEDIATA
# Editado: itens-service/requirements.txt
# Alterado: PyMySQL==1.1.0 → PyMySQL==1.1.1

# 🏗️ 4. REBUILD DA IMAGEM
docker build -f itens-service/dockerfile -t carmonoca/itens-service:v1.0.1 ./itens-service

# ✅ 5. VERIFICAÇÃO DE SEGURANÇA
docker scout quickview carmonoca/itens-service:v1.0.1
# Resultado: ✅ 0 Críticas, 0 Altas, 0 Médias, 2 Baixas

# 📤 6. PUBLICAÇÃO DA VERSÃO SEGURA
docker tag carmonoca/itens-service:v1.0.1 carmonoca/itens-service:latest
docker push carmonoca/itens-service:v1.0.1
docker push carmonoca/itens-service:latest
```

#### **🎯 Comando para Verificar Segurança Atual**

```powershell
# Verificação rápida da versão corrigida
docker scout quickview carmonoca/itens-service:v1.0.1

# Análise detalhada (se necessário)
docker scout cves carmonoca/itens-service:v1.0.1

# Para usar a versão segura em produção
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d
```

#### **📋 Próximos Passos de Segurança**

1. **Monitoramento Contínuo**:
   ```powershell
   # Verificação periódica de novas vulnerabilidades
   docker scout cves carmonoca/itens-service:latest
   ```

2. **Política de Atualizações**:
   - ✅ Vulnerabilidades **CRÍTICAS**: Correção imediata (0-24h)
   - ✅ Vulnerabilidades **ALTAS**: Correção prioritária (1-7 dias)
   - 🟡 Vulnerabilidades **MÉDIAS**: Próximo ciclo de release
   - 🟢 Vulnerabilidades **BAIXAS**: Avaliar necessidade

3. **Automação Futura**:
   - Integrar Docker Scout no CI/CD
   - Alerts automáticos para novas CVEs
   - Scans de segurança em PRs

**🔒 Status Atual de Segurança: ✅ SEGURO (v1.0.1)**

## 📊 **Monitoramento**

```powershell
# Status dos containers
docker ps

# Redes criadas
docker network ls | findstr ecommerce

# Volumes criados  
docker volume ls | findstr ecommerce

# Uso de recursos
docker stats

# Logs específicos
docker logs ecommerce_dev_itens-service_1 -f
```

## 💾 **Backup de Volumes MySQL**

### **📋 Índice de Backup:**
- [🚀 Comandos Testados e Aprovados](#-comandos-de-backup-testados)
- [🔍 Como Funcionam os Comandos](#-explicação-detalhada-dos-comandos) 
- [📁 Verificação de Backups](#-verificar-backups-criados)
- [🔄 Restauração de Backup](#-restaurar-backup)
- [⚙️ Automatização](#-script-de-backup-automatizado)

### **🚀 Comandos de Backup Testados**

Os comandos abaixo foram **testados com sucesso** e são **100% funcionais** no projeto:

#### **💻 Backup de Desenvolvimento:**
```powershell
# BACKUP DESENVOLVIMENTO (TESTADO ✅)
docker run --rm -v ecommerce_dev_mysql_data:/data:ro -v ${PWD}\backups:/backup alpine tar czf /backup/mysql-volume-dev-$(Get-Date -Format "yyyyMMdd-HHmmss").tar.gz -C /data .; if ($LASTEXITCODE -eq 0) { Write-Host "✅ Backup de desenvolvimento concluído!" -ForegroundColor Green }
```

#### **🏭 Backup de Produção:**
```powershell
# BACKUP PRODUÇÃO (TESTADO ✅)
docker run --rm -v ecommerce_prod_mysql_data:/data:ro -v ${PWD}\backups:/backup alpine tar czf /backup/mysql-volume-prod-$(Get-Date -Format "yyyyMMdd-HHmmss").tar.gz -C /data .; if ($LASTEXITCODE -eq 0) { Write-Host "✅ Backup de produção concluído!" -ForegroundColor Green }
```

### **🔍 Explicação Detalhada dos Comandos**

#### **🏗️ Anatomia do Comando de Backup:**

```powershell
docker run --rm -v ecommerce_dev_mysql_data:/data:ro -v ${PWD}\backups:/backup alpine tar czf /backup/mysql-volume-dev-$(Get-Date -Format "yyyyMMdd-HHmmss").tar.gz -C /data .
```

| **Componente** | **Função** | **Explicação Detalhada** |
|----------------|------------|--------------------------|
| `docker run` | Executa container | Cria e executa novo container temporário |
| `--rm` | Auto-limpeza | Remove container automaticamente após execução |
| `-v ecommerce_dev_mysql_data:/data:ro` | Mount volume MySQL | Monta volume do banco em `/data` (somente leitura) |
| `-v ${PWD}\backups:/backup` | Mount pasta local | Monta diretório `./backups` em `/backup` |
| `alpine` | Imagem base | Linux Alpine (~5MB) com ferramentas básicas |
| `tar czf` | Compactação | Cria arquivo `.tar.gz` compactado |
| `/backup/mysql-volume-dev-TIMESTAMP.tar.gz` | Arquivo destino | Nome com timestamp automático |
| `-C /data` | Diretório origem | Muda para `/data` antes de compactar |
| `.` | Conteúdo | Todos os arquivos e pastas |

#### **🎯 Fluxo de Execução:**

```
┌─────────────────────────────────────────────────────────────┐
│                 PROCESSO DE BACKUP                          │
├─────────────────────────────────────────────────────────────┤
│  1. Cria container Alpine temporário                       │
│  2. Monta volume MySQL em /data (read-only)                │
│  3. Monta pasta ./backups em /backup                       │
│  4. Executa tar para compactar /data                       │
│  5. Salva arquivo em ./backups/mysql-volume-TIMESTAMP.tar.gz│
│  6. Remove container automaticamente                        │
│  7. Exibe mensagem de sucesso                              │
└─────────────────────────────────────────────────────────────┘
```

#### **✅ Vantagens desta Abordagem:**

- **🔒 Seguro**: Backup "a quente" sem parar MySQL
- **⚡ Rápido**: Container temporário, sem overhead
- **📦 Compactado**: Arquivo `.tar.gz` economiza espaço
- **🕒 Timestamped**: Nome único com data/hora
- **🧹 Limpo**: Container removido automaticamente
- **🔍 Isolado**: Não afeta sistema host
- **🌐 Portável**: Funciona em qualquer Docker

### **📁 Verificar Backups Criados**

```powershell
# Listar todos os backups
Get-ChildItem .\backups\ | Format-Table Name, @{Name="Tamanho(MB)";Expression={[math]::Round($_.Length/1MB,2)}}, LastWriteTime

# Verificar tamanho do último backup
$UltimoBackup = Get-ChildItem .\backups\*.tar.gz | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Write-Host "📦 Último backup: $($UltimoBackup.Name)" -ForegroundColor Cyan
Write-Host "📊 Tamanho: $([math]::Round($UltimoBackup.Length/1MB,2)) MB" -ForegroundColor Cyan
Write-Host "🕒 Data: $($UltimoBackup.LastWriteTime)" -ForegroundColor Cyan

# Verificar integridade do backup
docker run --rm -v "${PWD}\backups:/backup" alpine tar -tzf "/backup/$($UltimoBackup.Name)" | head -10
```

### **🔄 Restaurar Backup**

#### **⚠️ Restauração Completa (CUIDADO!):**

```powershell
# ATENÇÃO: Este processo APAGA todos os dados atuais!

# 1. Parar ambiente
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev down

# 2. Remover volume existente
docker volume rm ecommerce_dev_mysql_data

# 3. Recriar volume vazio
docker volume create ecommerce_dev_mysql_data

# 4. Restaurar backup (substitua pelo nome do arquivo)
$BackupFile = "mysql-volume-dev-20250531-033348.tar.gz"
docker run --rm -v ecommerce_dev_mysql_data:/data -v "${PWD}\backups:/backup" alpine tar xzf "/backup/$BackupFile" -C /data

# 5. Reiniciar ambiente
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev up -d

Write-Host "✅ Restauração concluída!" -ForegroundColor Green
```




**🔒 Status: TESTADO E FUNCIONANDO ✅**

## 🧹 **Limpeza**

```powershell
# Parar ambientes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env.dev down
docker-compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env.prod down

# Limpeza geral
docker system prune -f
docker volume prune -f
```

## 📁 **Estrutura do Projeto**

```
GS-ITENS/
├── .env.dev                    # Variáveis desenvolvimento
├── .env.prod                   # Variáveis produção  
├── docker-compose.yml          # Arquivo base
├── docker-compose.dev.yml      # Override desenvolvimento
├── docker-compose.prod.yml     # Override produção
├── init.sql                    # Inicialização do banco
├── requirements.txt            # Dependências Python
├── README.md                   # Esta documentação
└── itens-service/              
    ├── app.py                  # Aplicação Flask
    ├── dockerfile              # Produção (multistage)
    ├── dockerfile.dev          # Desenvolvimento
    ├── .dockerignore           # Arquivos ignorados
    └── templates/
        └── index.html          # Interface web
```

## 🛡️ **Segurança Implementada**

### **Dockerfile:**
- ✅ **Multistage build** - reduz tamanho da imagem
- ✅ **Alpine Linux** - imagem base minimalista  
- ✅ **Usuário não-root** - `appuser:appgroup`
- ✅ **Dependências mínimas** - apenas runtime necessárias
- ✅ **Health checks** - monitoramento automático

### **Docker Compose:**
- ✅ **Redes isoladas** - `dev-network` / `prod-network`
- ✅ **Volumes nomeados** - persistência segura
- ✅ **Secrets management** - variáveis de ambiente
- ✅ **Security options** - `no-new-privileges`
- ✅ **Banco protegido** - porta não exposta em produção

### **Comunicação:**
- ✅ **DNS interno** - containers se comunicam por nome
- ✅ **Health checks** - dependências condicionais
- ✅ **Restart policies** - alta disponibilidade

## 🔧 **Otimizações Aplicadas**

### **Performance:**
- Multi-stage build reduz tamanho em ~60%
- Alpine Linux (base ~5MB vs ~180MB)
- Cache de dependências otimizado
- Volume bind para hot reload em dev

### **Produção:**
- Imagem otimizada sem ferramentas de desenvolvimento  
- Usuário não-privilegiado
- Health checks para orquestração
- Restart automático em falhas

## 📖 **Documentação da API**

### **Endpoints Disponíveis:**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Interface web |
| GET | `/status` | Health check |
| GET | `/itens` | Listar itens |
| POST | `/itens` | Criar item |
| GET | `/itens/{id}` | Buscar item |
| PUT | `/itens/{id}` | Atualizar item |
| DELETE | `/itens/{id}` | Remover item |

### **Exemplo de uso:**

```bash
# Criar item
curl -X POST http://localhost:8383/itens \
  -d "nome=Produto Teste" \
  -d "descricao=Descrição do produto" \
  -d "preco=29.99"

# Listar itens  
curl http://localhost:8383/itens

# Status da aplicação
curl http://localhost:8383/status
```

## 🎯 **Acesso à Aplicação**

- **Interface Web**: http://localhost:8383
- **API Health**: http://localhost:8383/status  
- **API Itens**: http://localhost:8383/itens
- **MySQL** (apenas dev): localhost:3306

## ⚠️ **Troubleshooting**

### **Container não inicia:**
```powershell
# Verificar logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs itens-service

# Verificar saúde do banco
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs mysql-db
```

### **Erro de conexão com banco:**
```powershell
# Testar conectividade
docker exec -it ecommerce_dev_mysql-db_1 mysql -u root -p

# Verificar variáveis
docker exec ecommerce_dev_itens-service_1 env | findstr DB_
```

### **Problemas de permissão:**
```powershell
# Recriar volumes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v
docker volume prune -f
```

---

## 🔥 **COMANDOS PRINCIPAIS - COLA RÁPIDA**

### **📋 Para Lembrar Sempre:**

```powershell
# 🔧 DESENVOLVIMENTO
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml up -d
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml logs -f
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml down

# 🚀 PRODUÇÃO  
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml logs -f
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml down

# 🏗️ BUILD & PUSH (carmonoca)
docker build -f itens-service/dockerfile -t carmonoca/itens-service:v1.0.0 ./itens-service
docker tag carmonoca/itens-service:v1.0.0 carmonoca/itens-service:latest
docker push carmonoca/itens-service:v1.0.0
docker push carmonoca/itens-service:latest

# 🛡️ BUILD VERSÃO SEGURA (v1.0.1 - RECOMENDADO)
docker build -f itens-service/dockerfile -t carmonoca/itens-service:v1.0.1 ./itens-service
docker tag carmonoca/itens-service:v1.0.1 carmonoca/itens-service:latest
docker push carmonoca/itens-service:v1.0.1
docker push carmonoca/itens-service:latest

# 🔒 ANÁLISE DE SEGURANÇA
docker scout cves carmonoca/itens-service:v1.0.1
docker scout quickview carmonoca/itens-service:v1.0.1

# 💾 BACKUP DE VOLUMES (TESTADOS ✅)
# Desenvolvimento
docker run --rm -v ecommerce_dev_mysql_data:/data:ro -v ${PWD}\backups:/backup alpine tar czf /backup/mysql-volume-dev-$(Get-Date -Format "yyyyMMdd-HHmmss").tar.gz -C /data .; if ($LASTEXITCODE -eq 0) { Write-Host "✅ Backup de desenvolvimento concluído!" -ForegroundColor Green }

# Produção
docker run --rm -v ecommerce_prod_mysql_data:/data:ro -v ${PWD}\backups:/backup alpine tar czf /backup/mysql-volume-prod-$(Get-Date -Format "yyyyMMdd-HHmmss").tar.gz -C /data .; if ($LASTEXITCODE -eq 0) { Write-Host "✅ Backup de produção concluído!" -ForegroundColor Green }

# Verificar backups
Get-ChildItem .\backups\*.tar.gz | Format-Table Name, @{Name="Tamanho(MB)";Expression={[math]::Round($_.Length/1MB,2)}}, LastWriteTime

# 🧪 TESTE RÁPIDO
curl http://localhost:8383/status
curl http://localhost:8383/itens

# 🗄️ ACESSO MYSQL (DEV)
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml exec mysql-db mysql -u root -proot ecommerce_db
```

### **🌐 URLs de Acesso:**
- **Interface:** http://localhost:8383
- **API Status:** http://localhost:8383/status  
- **API Itens:** http://localhost:8383/itens
- **Docker Hub:** https://hub.docker.com/r/carmonoca/itens-service
- **Versão Segura:** carmonoca/itens-service:v1.0.1 ✅

---

## 📝 **Resumo dos Entregáveis**

✅ **Dockerfile(s)** com multistage build e otimizações  
✅ **docker-compose.yml** base + overrides para dev/prod  
✅ **Aplicação rodando** localmente com banco containerizado  
✅ **Variáveis de ambiente** para troca dev/prod  
✅ **Imagem pronta** para publicação no Docker Hub  
✅ **Documentação completa** com todos os comandos  
✅ **Segurança implementada** conforme boas práticas  
✅ **Redes isoladas** para comunicação segura  
✅ **Volumes adequados** com diferenciação de ambientes  
✅ **Sistema de backup** completo e testado para volumes MySQL  
✅ **Comandos de backup** funcionais para dev/prod  
✅ **Scripts de automação** de backup e recuperação

## 📝 **COMANDOS EXECUTADOS NESTE PROJETO** 

### **🏗️ Build e Push das Imagens (carmonoca)**

```powershell
# Build da imagem de produção
docker build -f itens-service/dockerfile -t carmonoca/itens-service:v1.0.0 ./itens-service

# Criar tag latest
docker tag carmonoca/itens-service:v1.0.0 carmonoca/itens-service:latest

# Login no Docker Hub
docker login

# Push das duas tags
docker push carmonoca/itens-service:v1.0.0
docker push carmonoca/itens-service:latest
```

### **🔒 Análise de Segurança Executada**

```powershell
# Análise completa de vulnerabilidades (v1.0.0)
docker scout cves carmonoca/itens-service:v1.0.0

# Resultado: 7 vulnerabilidades encontradas em 4 packages
# - 1 CRITICAL (pymysql 1.1.0 - CVE-2024-36039)
# - 2 HIGH (cryptography 41.0.7)
# - 3 MEDIUM (requests 2.31.0, cryptography)
# - 1 LOW (flask 3.1.0)

# Verificação pós-correção (v1.0.1)
docker scout quickview carmonoca/itens-service:v1.0.1

# ✅ Resultado: 0 Críticas, 0 Altas, 0 Médias, 2 Baixas
```

### **🛠️ Correção de Vulnerabilidades Executada**

```powershell
# Build da versão segura com dependências atualizadas
docker build -f itens-service/dockerfile -t carmonoca/itens-service:v1.0.1 ./itens-service

# Tag e push da versão segura
docker tag carmonoca/itens-service:v1.0.1 carmonoca/itens-service:latest
docker push carmonoca/itens-service:v1.0.1
docker push carmonoca/itens-service:latest

# Dependências corrigidas no requirements.txt:
# - PyMySQL==1.1.0 → PyMySQL==1.1.1 (CVE-2024-36039 - Critical)
# - cryptography==41.0.7 → cryptography==43.0.1 (High vulnerabilities)
# - requests==2.31.0 → requests==2.32.0 (Medium vulnerability)
```

### **🧪 Comandos de Teste e Validação**

```powershell
# Testar ambiente dev
docker-compose --env-file .env.dev -f docker-compose.yml -f docker-compose.dev.yml up -d
curl http://localhost:8383/status
curl http://localhost:8383/itens

# Testar ambiente prod
docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d
curl http://localhost:8383/status

# Verificar segurança da imagem
docker scout cves carmonoca/itens-service:v1.0.0
docker scout recommendations carmonoca/itens-service:v1.0.0
```