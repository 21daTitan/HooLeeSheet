# Detecção de ambiente e portabilidade

A skill Quebrador funciona em múltiplos ambientes. O agente deve detectar as capacidades reais antes de prometer funcionalidades.

## Matriz de capacidades

| Recurso | Claude Code | Codex/OpenCode | Chat web | Termux/VPS |
|---|---|---|---|---|
| Scripts Python | Sim | Sim | Não | Sim |
| Acesso a terminal | Sim | Sim | Não | Sim |
| MCP servers | Possível | Não | Não | Não |
| yt-dlp | Se instalado | Se instalado | Não | Se instalado |
| FFmpeg/FFprobe | Se instalado | Se instalado | Não | Se instalado |
| faster-whisper | Se instalado | Se instalado | Não | Se instalado |
| GitHub API | Via MCP/gh | Via API | Não | Via gh CLI |
| Leitura de arquivos | Sim | Sim | Como contexto | Sim |
| vidIQ plugin | Se conectado | Não | Não | Não |

## Regras de detecção

1. Verificar `python3 scripts/quebrador.py doctor` para ferramentas disponíveis
2. Não declarar capacidade sem confirmação do ambiente
3. Em chat web, funcionar como contexto de referência carregado (sem scripts)
4. Registrar `tool_missing` quando recurso necessário não estiver instalado
5. Nunca instalar dependências sem autorização explícita

## Modo degradado

Quando um recurso não está disponível:
- Sem yt-dlp: registrar URL na fila, não tentar extrair metadados
- Sem FFmpeg: registrar arquivo como pendente de análise técnica
- Sem MCP: usar catálogos markdown como referência estática
- Sem terminal: fornecer orientação baseada nos catálogos carregados
