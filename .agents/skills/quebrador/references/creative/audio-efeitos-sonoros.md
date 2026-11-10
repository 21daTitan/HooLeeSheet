# Áudio, Voz e Efeitos Sonoros

> **Aviso**: referências de ferramentas. Preços, licenças e disponibilidade mudam. Verificar ToS e licença de cada peso/som antes de uso comercial. Clonagem de voz exige **consentimento verificável** da pessoa (Princípio 6 do master prompt).

## Conceito central — "API sem descontar créditos"

Há dois modos de usar a maioria dos serviços de áudio por IA:

1. **Site/API hospedada** (ex: `fish.audio`, ElevenLabs): cada chamada **desconta créditos** da sua conta paga.
2. **Modelo open source auto-hospedado**: você baixa os pesos e roda **na sua máquina/VPS**. A "API" passa a ser um servidor local (`localhost`), então **não existe crédito de site para descontar** — o custo é só a sua GPU/CPU e tempo.

O método gratuito **legítimo** é sempre o #2 (auto-hospedar). Não se trata de burlar o faturamento do serviço pago — é usar a versão aberta que foi feita para rodar localmente. Isso alinha com o Princípio 4 (baixo custo) e a política `license_check`.

---

## 1. Fish Speech / OpenAudio (TTS + clonagem de voz)

| Item | Detalhe |
|---|---|
| Repo | https://github.com/fishaudio/fish-speech |
| Pesos | HuggingFace: `fishaudio/fish-speech-1.5`, `fishaudio/openaudio-s1-mini` |
| Licença | Código Apache-2.0; **pesos frequentemente CC-BY-NC-SA (não-comercial)** — checar antes de uso comercial |
| Site pago | https://fish.audio (API por créditos) |
| Capacidade | TTS multilíngue, clonagem de voz com poucos segundos de referência |

### Método auto-hospedado (sem créditos)

**[PENDENTE] Instalação não testada neste ambiente.** Os passos de instalação e os nomes dos pesos mudam entre versões: siga o README oficial do repositório para instalar, baixar os pesos e subir `tools/api_server.py`. Suba o servidor escutando em `127.0.0.1:8080` (não em `0.0.0.0`) para não expor a API na rede.

Com o servidor local no ar, a skill gera a voz:

```bash
# Voz padrão do modelo
python3 scripts/quebrador.py tts "Olá, teste local" --out narracao.wav

# Com amostra de voz própria ou autorizada (exige --consent e a transcrição da amostra)
python3 scripts/quebrador.py tts "Olá" --out narracao.wav \
  --reference-audio minha_voz.wav --reference-text "texto falado na amostra" --consent
```

- O comando recusa qualquer servidor que não seja `localhost` ou rede privada, então não gasta crédito do serviço pago.
- Contrato usado (conferido em `fish_speech/utils/schema.py`, `ServeTTSRequest`): `text`, `format`, `reference_id` e `references: [{audio em base64, text}]`.
- **[PENDENTE]** A rota `/v1/tts` vem da documentação do Fish e ainda não foi exercitada contra um servidor real; conferir no primeiro uso.

- **Nenhuma chamada sai para fish.audio** → nenhum crédito consumido.
- Para clonar voz: usar **apenas** amostra com consentimento comprovado (ou a sua própria voz).
- Hardware: roda em CPU (lento) ou GPU (rápido). VPS com GPU é opcional.

### Alternativas open source de TTS/voz (mesmo princípio: local = grátis)
| Modelo | Repo | Nota |
|---|---|---|
| Coqui XTTS-v2 | https://github.com/coqui-ai/TTS | Clonagem multilíngue, local |
| Piper | https://github.com/rhasspy/piper | Leve, ótimo para Termux/VPS/Raspberry |
| Kokoro | https://huggingface.co/hexgrad/Kokoro-82M | Pequeno, rápido, licença permissiva |

---

## 2. Efeitos Sonoros (SFX)

A skill **pode buscar efeitos sonoros**. Escada de prioridade (grátis primeiro):

### Escada de prioridade
1. **Geração por IA local** (grátis, sem créditos, sem chave):
   | Modelo | Repo | Função |
   |---|---|---|
   | Meta AudioCraft / AudioGen | https://github.com/facebookresearch/audiocraft | Gera SFX a partir de texto, local |
   | Stable Audio Open | https://huggingface.co/stabilityai/stable-audio-open-1.0 | SFX e áudio curto, pesos abertos |

2. **Bibliotecas gratuitas com API/licença aberta**:
   | Fonte | URL | Licença | API |
   |---|---|---|---|
   | Freesound | https://freesound.org/ | CC (varia por som — respeitar atribuição) | Sim (chave grátis) |
   | Pixabay | https://pixabay.com/sound-effects/ | Pixabay License (livre) | Sim |
   | Mixkit | https://mixkit.co/free-sound-effects/ | Mixkit License (livre) | Não |
   | Uppbeat | https://uppbeat.io/sfx | Grátis com atribuição | Não |

3. **Pago (crédito) — último recurso, só com autorização**:
   | Serviço | Nota |
   |---|---|
   | ElevenLabs Sound Effects | API hospedada, desconta créditos |
   | vidIQ (`vidiq_generate_music`) | Plugin, gasta créditos vidIQ |

### Método de busca via Freesound (grátis)
```bash
# Chave gratuita em https://freesound.org/apiv2/apply/ — fica em variável de ambiente, NUNCA no código
export FREESOUND_API_KEY="..."

python3 scripts/quebrador.py sfx "chuva trovão"                 # lista nome, duração, licença, autor e prévia
python3 scripts/quebrador.py sfx "porta rangendo" --download 3  # baixa a prévia MP3 dos 3 primeiros
```
Os resultados ficam em `outputs/sfx-<id>/results.json`. Cada som tem licença própria (CC0, CC-BY, CC-BY-NC): guarde autor e licença para a atribuição. **[PENDENTE]** Testado só com resposta simulada; a primeira busca real depende da chave do dono.

### Método de geração local via AudioGen (grátis)
**[PENDENTE] Não testado neste ambiente** e fora do CLI, porque exige instalar `audiocraft` e `torch`. Seguir o README oficial do AudioCraft; a geração roda local, sem créditos.

---

## Como pedir à skill

- **Voz/TTS**: "gera narração local com Fish" → rota para a seção 1 (auto-hospedado).
- **Efeito sonoro**: "busca SFX de chuva" → rota para a seção 2, começando por geração local / Freesound / Pixabay, só subindo para pago com autorização.
- A skill **nunca** desconta crédito de serviço pago sem permissão explícita (política `billing`).

## Proteções
- Chaves de API (Freesound, ElevenLabs) **só** em variável de ambiente, nunca commitadas.
- Respeitar licença de cada som e de cada peso de modelo (não-comercial vs livre).
- Voz de terceiros = consentimento verificável obrigatório.
- Serviço pago só com autorização específica do dono por ação.
