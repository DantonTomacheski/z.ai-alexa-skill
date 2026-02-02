# Referência: Princípios de Engenharia de Contexto do Manus

Esta instrução é baseada em princípios de engenharia de contexto do Manus, a empresa de agentes de IA adquirida pela Meta por US$ 2 bilhões em dezembro de 2025.

## Os 6 Princípios do Manus

### Princípio 1: Projetar ao Redor do KV‑Cache

> "Taxa de acerto de KV‑cache é A métrica mais importante para agentes de IA em produção."

**Estatísticas:**

- ~100:1 proporção de tokens de entrada para saída
- Tokens em cache: US$ 0,30/MTok vs sem cache: US$ 3/MTok
- 10x de diferença de custo!

**Implementação:**

- Mantenha prefixos do prompt ESTÁVEIS (mudança de um token invalida o cache)
- NUNCA use timestamps em prompts de sistema
- Faça o contexto ser SOMENTE ANEXO com serialização determinística

### Princípio 2: Mascarar, Não Remover

Não remova ferramentas dinamicamente (quebra o KV‑cache). Use máscara de logit.

**Boa prática:** Use prefixos de ação consistentes (ex.: `browser_`, `shell_`, `file_`) para facilitar a máscara.

### Princípio 3: Sistema de Arquivos como Memória Externa

> "Markdown é minha 'memória de trabalho' em disco."

**A Fórmula:**

```
Janela de Contexto = RAM (volátil, limitada)
Sistema de Arquivos = Disco (persistente, ilimitado)
```

**A compressão deve ser recuperável:**

- Mantenha URLs mesmo se o conteúdo web for descartado
- Mantenha caminhos de arquivos ao remover conteúdo de documentos
- Nunca perca o ponteiro para os dados completos

### Princípio 4: Manipular a Atenção com Recitação

> "Cria e atualiza todo.md ao longo das tarefas para empurrar o plano global para a atenção recente do modelo."

**Problema:** Após ~50 chamadas de ferramenta, modelos esquecem objetivos originais (efeito “perdido no meio”).

**Solução:** Releia `plano_tarefa.md` antes de cada decisão. Os objetivos entram na janela de atenção.

```
Início do contexto: [Objetivo original — distante, esquecido]
...muitas chamadas de ferramenta...
Fim do contexto: [plano_tarefa.md lido recentemente — ganha ATENÇÃO!]
```

### Princípio 5: Mantenha as Coisas Erradas

> "Deixe os desvios errados no contexto."

**Por quê:**

- Ações que falharam com stack traces permitem atualizar crenças implicitamente
- Reduz repetição de erros
- Recuperação de erro é “um dos sinais mais claros de comportamento agentivo VERDADEIRO”

### Princípio 6: Não Seja Few‑Shotted

> "Uniformidade gera fragilidade."

**Problema:** Pares repetitivos de ação‑observação causam deriva e alucinação.

**Solução:** Introduza variação controlada:

- Varie levemente as frases
- Não copie e cole padrões às cegas
- Recalibre em tarefas repetitivas

---

## As 3 Estratégias de Engenharia de Contexto

Baseado na análise de Lance Martin sobre a arquitetura do Manus.

### Estratégia 1: Redução de Contexto

**Compactação:**

```
Chamadas de ferramenta têm DUAS representações:
├── COMPLETA: Conteúdo bruto da ferramenta (guardado no sistema de arquivos)
└── COMPACTA: Apenas referência/caminho do arquivo

REGRAS:
- Aplique compactação a resultados ANTIGOS
- Mantenha resultados RECENTES COMPLETOS (para guiar a próxima decisão)
```

**Resumo:**

- Aplicado quando a compactação tem retorno decrescente
- Gerado usando resultados completos das ferramentas
- Cria objetos de resumo padronizados

### Estratégia 2: Isolamento de Contexto (Multi‑Agente)

**Arquitetura:**

```
┌─────────────────────────────────┐
│ AGENTE PLANEJADOR │
│  └─ Atribui tarefas a subagentes │
├─────────────────────────────────┤
│ GERENTE DE CONHECIMENTO │
│  └─ Revisa conversas │
│  └─ Define armazenamento em arquivos │
├─────────────────────────────────┤
│ SUBAGENTES EXECUTORES │
│  └─ Executam tarefas atribuídas │
│  └─ Têm suas próprias janelas de contexto │
└─────────────────────────────────┘
```

**Insight‑chave:** O Manus originalmente usava `todo.md` para planejamento, mas descobriu que ~33% das ações eram gastas atualizando isso. Mudou para um agente planejador dedicado chamando subagentes executores.

### Estratégia 3: Offloading de Contexto

**Desenho de Ferramentas:**

- Use <20 funções atômicas no total
- Armazene resultados completos no sistema de arquivos, não no contexto
- Use `glob` e `grep` para busca
- Divulgação progressiva: carregue informação só quando necessário

---

## O Loop do Agente

O Manus opera em um loop contínuo de 7 etapas:

```
┌─────────────────────────────────────────┐
│  1. ANALISAR CONTEXTO │
│ - Entender a intenção do usuário │
│ - Avaliar o estado atual │
│ - Revisar observações recentes │
├─────────────────────────────────────────┤
│  2. PENSAR │
│ - Devo atualizar o plano? │
│ - Qual é a próxima ação lógica? │
│ - Há bloqueios? │
├─────────────────────────────────────────┤
│  3. SELECIONAR FERRAMENTA │
│ - Escolher UMA ferramenta │
│ - Garantir parâmetros disponíveis │
├─────────────────────────────────────────┤
│  4. EXECUTAR AÇÃO │
│ - Ferramenta roda em sandbox │
├─────────────────────────────────────────┤
│  5. RECEBER OBSERVAÇÃO │
│ - Resultado anexado ao contexto │
├─────────────────────────────────────────┤
│  6. ITERAR │
│ - Voltar ao passo 1 │
│ - Continuar até concluir │
├─────────────────────────────────────────┤
│  7. ENTREGAR RESULTADO │
│ - Enviar resultados ao usuário │
│ - Anexar todos os arquivos relevantes │
└─────────────────────────────────────────┘
```

---

## Tipos de Arquivos que o Manus Cria

| Arquivo            | Finalidade                          | Quando Criado            | Quando Atualizado     |
| ------------------ | ----------------------------------- | ------------------------ | --------------------- |
| `plano_tarefa.md`  | Acompanhamento de fases, progresso  | Início da tarefa         | Após concluir fases   |
| `achados.md`       | Descobertas, decisões               | Após QUALQUER descoberta | Após ver imagens/PDFs |
| `progresso.md`     | Registro da sessão, o que foi feito | Em pontos de parada      | Durante a sessão      |
| Arquivos de código | Implementação                       | Antes da execução        | Após erros            |

---

## Restrições Críticas

- **Execução de Ação Única:** UMA chamada de ferramenta por turno. Sem execução paralela.
- **Plano é Obrigatório:** Agente deve SEMPRE saber: objetivo, fase atual, fases restantes
- **Arquivos são Memória:** Contexto = volátil. Sistema de arquivos = persistente.
- **Nunca Repita Falhas:** Se uma ação falhou, a próxima DEVE ser diferente
- **Comunicação é uma Ferramenta:** Tipos de mensagem: `info` (progresso), `ask` (bloqueio), `result` (terminal)

---

## Estatísticas do Manus

| Métrica                                   | Valor         |
| ----------------------------------------- | ------------- |
| Média de chamadas por tarefa              | ~50           |
| Proporção tokens entrada/saída            | 100:1         |
| Preço de aquisição                        | US$ 2 bilhões |
| Tempo até US$ 100M de receita             | 8 meses       |
| Refactors do framework desde o lançamento | 5 vezes       |

---

## Citações‑chave

> "Janela de contexto = RAM (volátil, limitada). Sistema de arquivos = Disco (persistente, ilimitado). Tudo que é importante vai para o disco."

> "if action_failed: next_action != same_action. Track what you tried. Mutate the approach."

> "A recuperação de erro é um dos sinais mais claros de comportamento agentivo VERDADEIRO."

> "A taxa de acerto de KV‑cache é a métrica mais importante para um agente de IA em produção."

> "Deixe os desvios errados no contexto."

---

## Fonte

Baseado na documentação oficial de engenharia de contexto do Manus:
https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
