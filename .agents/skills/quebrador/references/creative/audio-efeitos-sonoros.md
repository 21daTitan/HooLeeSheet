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

```bash
# 1. Ambiente isolado
python3 -m venv .venv && source .venv/bin/activate

# 2. Instalar (CPU ou CUDA)
pip install fish-speech   # ou clonar o repo e pip install -e .

# 3. Baixar pesos (uma vez)
# via huggingface-cli download fishaudio/openaudio-s1-mini --local-dir checkpoints/

# 4. Subir servidor de API LOCAL
python -m tools.api_server --listen 0.0.0.0:8080 --llama-checkpoint-path checkpoints/

# 5. Seu app chama a API LOCAL — zero créditos
curl http://localhost:8080/v1/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Olá, teste local","reference_audio":"voz_autorizada.wav"}'
```

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
# Requer chave grátis em https://freesound.org/apiv2/apply/
# A chave fica em variável de ambiente, NUNCA no código:
export FREESOUND_API_KEY="..."   # definido pelo dono, fora do repo

curl -s "https://freesound.org/apiv2/search/text/?query=chuva+trovao&fields=name,previews,license&token=$FREESOUND_API_KEY"
# Baixar o preview MP3 do resultado; respeitar a licença CC de cada som.
```

### Método de geração local via AudioGen (grátis)
```bash
pip install audiocraft
python -c "
from audiocraft.models import AudioGen
import torchaudio
m = AudioGen.get_pretrained('facebook/audiogen-medium')
m.set_generation_params(duration=5)
wav = m.generate(['passos na madeira', 'porta rangendo'])
for i, a in enumerate(wav):
    torchaudio.save(f'sfx_{i}.wav', a.cpu(), m.sample_rate)
"
# Roda local; nenhum crédito; apenas CPU/GPU e tempo.
```

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
