# Changelog

## 1.2.0 — 2026-11-10
- Subcomando `sfx`: busca efeitos sonoros no Freesound, com licença e autor por resultado
- Subcomando `tts`: voz por servidor Fish Speech local; recusa servidor público e exige `--consent` para amostra de voz
- `references/creative/audio-efeitos-sonoros.md`: método de áudio local e correção do contrato da API do Fish
- Pendente: `sfx` e `tts` validados só por testes simulados, ainda não contra os serviços reais

## 1.1.0 — 2026-11-10
- Integração com estrutura dSantCreator `.agents/skills/quebrador/`
- SKILL.md coordenador com tabela de roteamento por domínio
- Catálogos organizados: security/ (repos, MCPs, skills, mapa de superfície), websites/, creative/, youtube/, external/
- agents/openai.yaml para portabilidade Codex/ChatGPT
- Detecção de ambiente em references/capabilities.md
- Subcomando `validate` adicionado ao CLI
- Subcomandos `refs`, `refs-add`, `record` adicionados
- Escada de prioridade YouTube: yt-dlp > vidIQ > plugins gratuitos > arquivo do usuário
- Testes ampliados: catálogos, JSON, domínios, versão

## 1.0.1 — 2026-11-10
- Consentimento explícito de dSanT exigido antes de qualquer modificação persistente ou externa
- Agenda automática desativada; workflow apenas manual com autorização por execução
- Confirmação humana interativa para publicação privada

## 1.0.0 — 2026-11-10
- Master prompt único, isolamento de projetos, fila de referências multimodal
- Catalogação de identificadores GitHub e de MCP/Skills fornecidos
- CLI de inventário, intake, análise local, saúde de fontes, relatório
- Testes unitários e aprovação obrigatória para mudanças comportamentais
