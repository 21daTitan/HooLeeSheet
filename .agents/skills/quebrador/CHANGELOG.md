# Changelog

## 1.3.0 — 2026-11-10
- `check-repos --backend search --all`: verifica o catálogo inteiro pela busca do GitHub (`gh`), em lotes
- Oito estudos de vídeo em `references/youtube/estudos/`, feitos só por legendas (vidIQ, 40 créditos), pendentes de revisão do dono
- Cada estudo separa técnicas transferíveis do que conflita com a política (voz de terceiros, evasão de plataforma, anúncio camuflado, história falsa)
- Playlist e canal seguem não revisados: YouTube bloqueado na rede do ambiente
- Verificação dos 288 repositórios publicada em `references/security/verificacao-repos.md` e `.json`: 261 encontrados, 27 não encontrados, 18 arquivados; catálogo marcado, lista de clonagem inalterada

## 1.2.1 — 2026-11-10
- Subcomando `catalog` para consultar repos, MCPs, skills, sites, criativo, externos e YouTube (o SKILL.md citava comandos que não existiam)
- Histórico encadeado passa a ser gravado (`intake`, `clone-approved`, `sfx --download`, `tts`); `record --verify` acusa adulteração
- Catálogos de sites completados com a lista original do dono; novo `websites/download-ferramentas.md`
- `external/projetos-github.md` usa os rótulos do dono em vez de descrições não conferidas
- Workflows movidos para `.github/workflows/` na raiz do repositório
- Dois repositórios marcados como não encontrados no catálogo

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
