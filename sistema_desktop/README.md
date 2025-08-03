# Sistema de Gerenciamento de Materiais

Sistema desktop desenvolvido em Python com tkinter para gerenciamento de materiais através de uma API REST.

## Funcionalidades

### 📋 Tela 1 - Lista de Materiais
- Exibe todos os materiais cadastrados em uma tabela
- Obtém dados através de consulta à API (JSON)
- Botão para exclusão de materiais
- Botão para incluir novos materiais
- Botão para editar materiais existentes
- Atualização automática da lista

### ➕ Tela 2 - Inclusão de Material
- Formulário para cadastro de novos materiais
- Campos: Nome e Descrição
- Validação de campos obrigatórios
- Envio dos dados para API para inclusão
- Botões: Salvar, Limpar e Voltar

### ✏️ Tela 3 - Edição de Material
- Formulário para alteração de materiais existentes
- Carrega dados do material selecionado
- Campos: ID (somente leitura), Nome e Descrição
- Envio das alterações para API
- Botões: Salvar Alterações e Cancelar

## Estrutura do Projeto

```
sistema_desktop/
├── sistema_materiais.py    # Aplicação principal
├── config.py              # Configurações
├── teste_tkinter.py       # Teste de funcionamento do tkinter
└── requirements.txt       # Dependências (se necessário)
```

## Requisitos

- Python 3.7+
- tkinter (incluído no Python)
- requests (para comunicação com API)

## Instalação

1. Clone ou baixe o projeto
2. Ative o ambiente virtual:
   ```cmd
   venv\Scripts\activate
   ```
3. Instale as dependências:
   ```cmd
   pip install requests
   ```

## Execução

```cmd
python sistema_materiais.py
```

## Configuração da API

Por padrão, o sistema está configurado para conectar com uma API em:
`http://localhost:5000/api`

Para alterar a URL da API, edite o arquivo `config.py` e modifique a variável `API_BASE_URL`.

## Endpoints da API Esperados

O sistema espera que a API tenha os seguintes endpoints:

- `GET /api/materiais` - Lista todos os materiais
- `POST /api/cadastrar-material` - Cria um novo material
- `PUT /api/atualizar/material/{id}` - Atualiza um material existente
- `DELETE /api/excluir-materiail/{id}` - Remove um material

### Formato JSON Esperado

**Material:**
```json
{
  "id": 1,
  "nome": "Nome do Material",
  "descricao": "Descrição detalhada do material"
}
```

**Lista de Materiais:**
```json
[
  {
    "id": 1,
    "nome": "Material 1",
    "descricao": "Descrição do material 1"
  },
  {
    "id": 2,
    "nome": "Material 2",
    "descricao": "Descrição do material 2"
  }
]
```

## Modo Offline

Quando a API não está disponível, o sistema automaticamente utiliza dados mock para demonstração e teste das funcionalidades.

## Funcionalidades Técnicas

- **Comunicação com API**: Classe `APIClient` para todas as operações REST
- **Interface Responsiva**: Layout adaptável com scrollbars quando necessário
- **Validação de Dados**: Validação de campos obrigatórios
- **Tratamento de Erros**: Mensagens de erro amigáveis ao usuário
- **Dados Mock**: Fallback para demonstração quando API não disponível
- **Navegação Entre Telas**: Sistema de navegação simples e intuitivo

## Estrutura das Classes

- `SistemaMateriais`: Classe principal que gerencia a aplicação
- `ListaMateriais`: Tela de listagem e exclusão
- `IncluirMaterial`: Tela de inclusão de novos materiais
- `EditarMaterial`: Tela de edição de materiais existentes
- `APIClient`: Cliente para comunicação com a API REST

## Controles da Interface

### Tela de Lista
- **Incluir Material**: Abre tela de inclusão
- **Atualizar Lista**: Recarrega dados da API
- **Editar Selecionado**: Abre tela de edição do item selecionado
- **Excluir Selecionado**: Remove o item selecionado (com confirmação)

### Tela de Inclusão
- **Salvar**: Envia dados para API e inclui o material
- **Limpar**: Limpa todos os campos do formulário
- **Voltar**: Retorna para a tela de lista

### Tela de Edição
- **Salvar Alterações**: Envia alterações para API
- **Cancelar**: Retorna para a tela de lista sem salvar

## Tratamento de Erros

O sistema trata os seguintes cenários:
- API indisponível (usa dados mock)
- Campos obrigatórios vazios
- Nenhum item selecionado para edição/exclusão
- Erros de conexão com a API
- Respostas de erro da API
