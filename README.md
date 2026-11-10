# dSantCreator + SagaZ

Agente modular de criação de conteúdo: copywriting, CTA, estratégia, estudo de vídeos e produção audiovisual. Skills para Codex, Claude Code e OpenCode, com contexto portátil para ChatGPT e Claude web. Ferramentas gratuitas como padrão.

## Instalação na VPS

Requisitos: Git, tar e Python 3.10 ou superior. O código completo desta versão está no pacote `dSantCreator-3.2.0-source.tar.gz`, incluindo as pastas de skills.

```bash
git clone https://github.com/21daTitan/HooLeeSheet.git
cd HooLeeSheet
tar -xzf dSantCreator-3.2.0-source.tar.gz
cd dSantCreator
python3 dsant.py install --target all
python3 dsant.py doctor
python3 dsant.py sagaz --web
```

Interface local: http://127.0.0.1:8080. Para acessar uma VPS pelo celular ou computador, mantenha um túnel SSH com `-L 8080:127.0.0.1:8080`.

## Incluído na versão 3.2.0

- SagaZ com interface azul/Matrix e projetos persistentes.
- Seis skills: dSant Creator, Cartoon, Remotion, Storyboard Analyzer, YouTube Reverse Engineering e Ponytail.
- Referências e 15 estudos parciais da playlist; revisão integral das aulas permanece pendente.
- Templates de animação e licenças de terceiros preservadas.
- Instalador e pacote de contexto para chats web.
- 25 testes locais aprovados antes do upload.

## Skill Quebrador — Foco No Progresso

Fica em `.agents/skills/quebrador/`, fora do pacote `dSantCreator-3.2.0-source.tar.gz`. Reúne catálogos de pesquisa (repositórios, MCPs, skills, sites, YouTube, ferramentas criativas e de áudio) e um CLI sem dependências obrigatórias. Os catálogos são inventário não verificado; qualquer ação que altere estado exige autorização do dono.

```bash
cd .agents/skills/quebrador
python3 scripts/quebrador.py doctor
python3 scripts/quebrador.py catalog web --search exploit
python3 -m unittest discover -s tests
```

Detalhes em `.agents/skills/quebrador/SKILL.md`.

## Uso sem API

O núcleo prepara contratos, referências e contexto. O chat do seu aplicativo executa o briefing com suas ferramentas. Geração pelo SagaZ exige configurar um endpoint; assinatura de chat não implica créditos de API.

```bash
python3 dsant.py pack
python3 dsant.py agent prepare --brief "Campanha RR: painel apagado" --niche automotive --method automotive-pov --out projects/rr-001
```

Leia o README e a pasta `docs/` dentro do pacote para detalhes, limites e ferramentas opcionais.

## Atualizações

Este repositório publica o sistema como pacote completo. `git pull --ff-only` atualiza o pacote, mas não extrai nem substitui sua instalação automaticamente. Para uma versão nova, extraia em uma pasta nova e preserve `projects/`, `state/` e credenciais da instalação anterior. O comando `dsant.py update` exige um clone com os fontes rastreados; não deve ser usado na pasta extraída deste pacote.
