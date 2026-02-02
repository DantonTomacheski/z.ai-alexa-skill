# Exemplos: Planejamento com Arquivos em Ação

## Exemplo 1: Tarefa de Pesquisa

**Pedido do usuário:** "Pesquise os benefícios do exercício pela manhã e escreva um resumo"

### Ciclo 1: Criar o Plano

```bash
Escrever plano_tarefa.md
```

```markdown
# Plano de Tarefa: Pesquisa sobre Benefícios do Exercício Matinal

## Objetivo

Criar um resumo de pesquisa sobre os benefícios do exercício pela manhã.

## Fases

- [ ] Fase 1: Criar este plano ✓
- [ ] Fase 2: Buscar e reunir fontes
- [ ] Fase 3: Sintetizar descobertas
- [ ] Fase 4: Entregar resumo

## Perguntas‑chave

1. Quais são os benefícios físicos para a saúde?
2. Quais são os benefícios para a saúde mental?
3. Quais estudos científicos apoiam isso?

## Status

**Atualmente na Fase 1** — Criando plano
```

### Ciclo 2: Pesquisa

```bash
Read plano_tarefa.md # Relembrar objetivos
WebSearch "benefícios exercício matinal"
Write notas.md # Guardar descobertas
Edit plano_tarefa.md # Marcar Fase 2 como concluída
```

### Ciclo 3: Sintetizar

```bash
Read plano_tarefa.md # Relembrar objetivos
Read notas.md # Obter descobertas
Write resumo_exercicio_matinal.md
Edit plano_tarefa.md # Marcar Fase 3 como concluída
```

### Ciclo 4: Entregar

```bash
Read plano_tarefa.md # Verificar conclusão
Deliver resumo_exercicio_matinal.md
```

---

## Exemplo 2: Correção de Bug

**Pedido do usuário:** "Corrija o bug de login no módulo de autenticação"

### plano_tarefa.md

```markdown
# Plano de Tarefa: Corrigir Bug de Login

## Objetivo

Identificar e corrigir o bug que impede o login bem-sucedido.

## Fases

- [x] Fase 1: Entender o relatório do bug ✓
- [x] Fase 2: Localizar o código relevante ✓
- [ ] Fase 3: Identificar a causa raiz (ATUAL)
- [ ] Fase 4: Implementar correção
- [ ] Fase 5: Testar e verificar

## Perguntas‑chave

1. Qual mensagem de erro aparece?
2. Qual arquivo trata autenticação?
3. O que mudou recentemente?

## Decisões Tomadas

- O handler de autenticação está em src/auth/login.ts
- O erro ocorre na função validateToken()

## Erros Encontrados

- [Inicial] TypeError: Cannot read property 'token' of undefined
  → Causa raiz: objeto de usuário não aguardado corretamente

## Status

**Atualmente na Fase 3** — Causa raiz encontrada, preparando correção
```

---

## Exemplo 3: Desenvolvimento de Funcionalidade

**Pedido do usuário:** "Adicione um toggle de modo escuro na página de configurações"

### O Padrão de 3 Arquivos em Ação

**plano_tarefa.md:**

```markdown
# Plano de Tarefa: Toggle de Modo Escuro

## Objetivo

Adicionar um toggle funcional de modo escuro nas configurações.

## Fases

- [x] Fase 1: Pesquisar sistema de tema existente ✓
- [x] Fase 2: Desenhar abordagem de implementação ✓
- [ ] Fase 3: Implementar componente de toggle (ATUAL)
- [ ] Fase 4: Adicionar lógica de troca de tema
- [ ] Fase 5: Testar e polir

## Decisões Tomadas

- Usar propriedades CSS customizadas para tema
- Armazenar preferência no localStorage
- Componente de toggle em SettingsPage.tsx

## Status

**Atualmente na Fase 3** — Construindo componente de toggle
```

**notas.md:**

```markdown
# Notas: Implementação do Modo Escuro

## Sistema de Tema Existente

- Localizado em: src/styles/theme.ts
- Usa: propriedades CSS customizadas
- Temas atuais: apenas claro

## Arquivos para Modificar

1. src/styles/theme.ts - Adicionar cores do tema escuro
2. src/components/SettingsPage.tsx - Adicionar toggle
3. src/hooks/useTheme.ts - Criar novo hook
4. src/App.tsx - Envolver com ThemeProvider

## Decisões de Cores

- Fundo escuro: #1a1a2e
- Superfície escura: #16213e
- Texto escuro: #eaeaea
```

**implementacao_modo_escuro.md:** (entregável)

```markdown
# Implementação do Modo Escuro

## Mudanças Feitas

### 1. Adicionadas cores do tema escuro

Arquivo: src/styles/theme.ts
...

### 2. Criado hook useTheme

Arquivo: src/hooks/useTheme.ts
...
```

---

## Exemplo 4: Padrão de Recuperação de Erros

Quando algo falha, NÃO esconda:

### Antes (Errado)

```
Ação: Ler config.json
Erro: Arquivo não encontrado
Ação: Ler config.json  # Tentativa silenciosa
Ação: Ler config.json  # Outra tentativa
```

### Depois (Correto)

```
Ação: Ler config.json
Erro: Arquivo não encontrado

# Atualizar plano_tarefa.md:
## Erros Encontrados
- config.json não encontrado → Vamos criar config padrão

Ação: Escrever config.json (config padrão)
Ação: Ler config.json
Sucesso!
```

---

## O Padrão de Ler Antes de Decidir

**Sempre leia seu plano antes de decisões importantes:**

```
[Muitas chamadas de ferramenta aconteceram...]
[O contexto está ficando longo...]
[O objetivo original pode ser esquecido...]

→ Read plano_tarefa.md # Isso traz os objetivos de volta para a atenção!
→ Agora tome a decisão # Objetivos frescos no contexto
```

É por isso que o Manus consegue lidar com ~50 chamadas de ferramenta sem se perder. O arquivo de plano funciona como um mecanismo de “atualização de objetivos”.
