# Metal Gear OS — Sistema de Inspeção Visual

O **Metal Gear OS** é uma aplicação desktop de controle de qualidade que combina visão computacional, interface operacional, persistência de dados em servidor e preparação para integração com automação industrial.

O sistema analisa dados coloridos em tempo real, identifica a cor e a face visível, aplica regras configuradas pelo operador e registra o resultado como **APROVADO** ou **REJEITADO**.

> **Versão atual:** `v1.3.4`  
> **Estado:** interface e fluxo principal homologados em rede local  
> **Cores atualmente habilitadas:** vermelho, verde e azul

---

## Visão geral

O projeto foi desenvolvido como o primeiro estágio de um ecossistema industrial maior. Nesta fase, o computador executa a visão computacional e a interface gráfica, enquanto o histórico de produção é armazenado em um servidor separado por meio de uma API.

```text
Câmera
  ↓
OpenCV — detecção de cor e face
  ↓
Metal Gear OS — aplicação desktop
  ↓ HTTP/JSON
Metal Gear API — FastAPI
  ↓
MariaDB
  ↓
phpMyAdmin — administração
```

A aplicação desktop **não se conecta diretamente ao MariaDB**. Toda leitura e gravação passa pela API, reduzindo o acoplamento entre o executável e o banco de dados.

---

## Funcionalidades principais

### Visão computacional em tempo real

- Captura contínua da câmera com OpenCV.
- Zona de inspeção definida na imagem.
- Detecção das cores vermelho, verde e azul.
- Contagem dos pontos da face superior do dado.
- Seleção de um único alvo principal.
- Filtro por área, proporção e circularidade.
- Confirmação temporal por múltiplos frames.
- Indicador de progresso e confiança da leitura.
- Bloqueio contra registros duplicados.
- Liberação de um novo ciclo somente após a retirada da peça.

### Interface operacional

- Interface dark responsiva construída com CustomTkinter.
- Painel principal com estado da câmera, API e inspeção.
- Regras configuráveis de cores e faces permitidas.
- Contadores de aprovados e rejeitados.
- Histórico resumido das últimas inspeções.
- Pausa de inspeção.
- Parada de emergência de software.
- Perfis de acesso para administrador e operador.
- Adaptação para janela maximizada ou reduzida.

### Dados e relatórios

- Registro centralizado em MariaDB.
- Comunicação por API REST em JSON.
- Consulta por período.
- Visualização do histórico em tabela.
- Gráfico de aprovados e rejeitados.
- Exportação para PDF.
- Exportação para CSV.
- Logs locais para auditoria e diagnóstico.

---

## Arquitetura do sistema

### Aplicação desktop

Responsável por:

- captura da câmera;
- processamento da imagem;
- aplicação das regras do lote;
- interface com o operador;
- relatórios e exportações;
- comunicação com a API.

### Metal Gear API

API desenvolvida com FastAPI e executada em contêiner Docker no servidor.

Endpoints utilizados:

| Método | Endpoint | Função |
|---|---|---|
| `GET` | `/health` | Verifica API e banco |
| `POST` | `/producao` | Registra uma inspeção |
| `GET` | `/producao` | Consulta o histórico |
| `DELETE` | `/producao` | Limpa o histórico |

A documentação interativa da API fica disponível em:

```text
http://ENDERECO_DO_SERVIDOR:8001/docs
```

### Banco de dados

O histórico é armazenado no MariaDB, em uma estrutura compatível com MySQL.

Tabela principal:

```sql
CREATE TABLE producao (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    cor_dado VARCHAR(20) NOT NULL,
    numero_lido INT NOT NULL,
    status_peca VARCHAR(15) NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```

O arquivo `DATABASE/METAL_GEAR_SCHEMA.sql` documenta a estrutura necessária para recriar o banco.

---

## Tecnologias

| Área | Tecnologias |
|---|---|
| Linguagem | Python 3 |
| Visão computacional | OpenCV, NumPy |
| Interface gráfica | CustomTkinter, Pillow, Tkinter |
| API | FastAPI, Uvicorn |
| Comunicação | HTTP, REST, JSON, Requests |
| Banco de dados | MariaDB / MySQL |
| Administração do banco | phpMyAdmin |
| Infraestrutura | Docker, Docker Compose, Linux |
| Relatórios | FPDF, CSV, Matplotlib |
| Versionamento | Git e GitHub |

---

## Estrutura do projeto

```text
PROJECT_METAL_GEAR/
├── DATABASE/
│   └── METAL_GEAR_SCHEMA.sql
├── METAL_GEAR/
│   ├── ASSETS/
│   ├── BACK_END/
│   │   ├── BANCO_DE_DADOS.py
│   │   └── VISAO.py
│   ├── FRONT_END/
│   │   ├── INTERFACE.py
│   │   ├── UI_ESTILOS.py
│   │   ├── UI_GRAFICO.py
│   │   ├── UI_LOGIN.py
│   │   └── UI_SOBRE.py
│   ├── INFRA/
│   │   ├── CONFIG.py
│   │   └── LOGS.py
│   ├── RELATORIOS/
│   ├── MAIN.py
│   └── config.json
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Interface

O Metal Gear OS utiliza uma interface dark responsiva desenvolvida com CustomTkinter.

A aplicação possui três áreas principais:

- **Painel:** inspeção em tempo real, regras do lote, estado dos serviços e métricas da sessão.
- **Relatórios:** consulta do histórico armazenado no MariaDB, gráficos e exportação para PDF ou CSV.
- **Configurações:** seleção de câmera, informações do perfil de visão e operações administrativas.

As capturas da interface serão adicionadas novamente quando a versão visual definitiva do projeto estiver concluída.

> Atualize as imagens da pasta `METAL_GEAR/ASSETS` sempre que a interface receber uma alteração visual importante.

---

## Instalação da aplicação desktop

### 1. Clonar o repositório

```bash
git clone https://github.com/crys001001/METAL-GEAR-OS.git
cd METAL-GEAR-OS
```

### 2. Criar um ambiente virtual

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Dependências principais da aplicação desktop:

```text
customtkinter
fpdf
matplotlib
numpy
opencv-python
Pillow
requests
```

O pacote `mysql-connector-python` não é necessário no aplicativo desktop atual, porque a comunicação com o banco ocorre por meio da API.

---

## Configuração da API

Por padrão, a aplicação procura a API em:

```text
http://192.168.0.7:8001
```

O endereço pode ser alterado pela variável de ambiente `METAL_GEAR_API_URL`.

### PowerShell — sessão atual

```powershell
$env:METAL_GEAR_API_URL="http://192.168.0.7:8001"
```

### PowerShell — configuração persistente no Windows

```powershell
setx METAL_GEAR_API_URL "http://192.168.0.7:8001"
```

Depois de usar `setx`, abra um novo terminal.

### Verificar a API

```powershell
Invoke-RestMethod "http://192.168.0.7:8001/health"
```

Resposta esperada:

```json
{
  "api": "online",
  "banco": "online"
}
```

---

## Executar o sistema

Entre na pasta da aplicação:

```bash
cd METAL_GEAR
```

Execute:

```bash
python MAIN.py
```

Antes de iniciar uma inspeção, confirme:

- câmera conectada;
- API online;
- MariaDB disponível;
- objeto dentro da zona de inspeção;
- cores e faces permitidas configuradas.

---

## Regras de funcionamento da inspeção

O ciclo principal funciona desta forma:

```text
AGUARDANDO
    ↓
Peça entra na zona
    ↓
ANALISANDO
    ↓
Leitura estabilizada em múltiplos frames
    ↓
APROVADO ou REJEITADO
    ↓
Registro enviado à API
    ↓
BLOQUEADO até a retirada da peça
    ↓
Novo ciclo
```

O resultado depende da combinação entre:

- cor detectada;
- face detectada;
- cores permitidas;
- faces permitidas;
- confiança mínima da leitura.

---

## Configuração local

O arquivo `METAL_GEAR/config.json` guarda parâmetros específicos da máquina, como:

- câmera ativa;
- regras do lote;
- zona de inspeção;
- quantidade de frames de confirmação;
- confiança mínima;
- limites geométricos da detecção.

Esse arquivo deve permanecer fora do Git. Use um arquivo `config.example.json` para documentar valores padrão sem versionar configurações locais.

---

## Segurança e operação

A arquitetura atual foi homologada para uso em rede local.

Antes de expor o serviço pela internet, devem ser adicionados:

- autenticação na API;
- HTTPS/TLS;
- controle de origem e CORS;
- limitação de requisições;
- firewall e segmentação de rede;
- gestão segura de segredos;
- backups automatizados;
- auditoria de operações administrativas.

O botão de parada de emergência da interface é um controle de software. Na futura integração com esteira e braço robótico, deverá existir também uma **parada física de emergência**, independente do computador.

---

## Limitações atuais

- O dado amarelo está temporariamente desabilitado por sensibilidade à iluminação e exposição automática da câmera.
- A detecção atual utiliza visão computacional clássica, não um modelo treinado de machine learning.
- O sistema ainda não comanda fisicamente a esteira ou o braço robótico.
- A parada de emergência física ainda será implementada na etapa eletromecânica.
- A API atual está preparada para rede local e ainda precisa de autenticação antes de exposição pública.

---

## Roadmap — Saga de 5 Atos

### Ato I — Metal Gear OS

Visão computacional, aplicação desktop, API, banco de dados e futura integração com a esteira e o braço robótico.

### Ato II — Project Mother Base

Infraestrutura em nuvem, Linux, Docker, Docker Compose e serviços hospedados em AWS.

### Ato III — Project Codec

MQTT, TLS, redes privadas, firewall, VPC e análise de tráfego.

### Ato IV — Project iDroid

Dashboards de produção, indicadores operacionais, SQL, Grafana ou Metabase.

### Ato V — Project Kazuhira

Automação de incidentes, n8n, GLPI ou Zammad, webhooks, alertas e conceitos de ITSM.

---

## Próximas etapas técnicas

- Integração serial com Arduino.
- Controle da esteira por motor DC e ponte H.
- Leitura do sensor infravermelho.
- Sincronização entre inspeção, parada da esteira e pick-and-place.
- Comunicação com o braço robótico de 6 graus de liberdade.
- Integração de parada de emergência física.
- Autenticação e criptografia da API.
- Backups automatizados do MariaDB.
- Geração do executável final para Windows.

---

## Autor

**Crystyan Vicente Gomes de Arruda**

Estudante de Análise e Desenvolvimento de Sistemas, com interesse em sistemas ciberfísicos, visão computacional, infraestrutura, automação e robótica.

O objetivo do projeto é estudar e demonstrar, em uma única solução, a integração entre software, dados, redes e hardware industrial.

---

## Licença

Defina uma licença antes de distribuir ou aceitar contribuições externas. Para projetos de portfólio abertos, opções comuns incluem MIT e Apache 2.0.