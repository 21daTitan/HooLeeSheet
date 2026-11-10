# Pipeline de engenharia reversa de vídeo e conhecimento

## Níveis de evidência
1. Metadata only: título, duração, descrição; **não** prova técnica audiovisual.
2. Captions: transcrição e timecodes; informa falas mas não enquadramento, transições ou ritmo visual.
3. Video local: FFprobe, cortes, frames representativos; comprova aspectos visuais observáveis.
4. Video+audio: transcrição, análise visual e auditiva; melhor capacidade de associar hook, CTA, cortes e cenas.
5. Expert validation: revisão humana com fontes, comparação e experimento controlado.

## Modelo de estudo
| Tempo | Evidência | Observação | Técnica transferível | Incerteza | Aplicação ORIGINAL | Teste |
|---|---|---|---|---|---|---|

Se houver somente legendas, não inventar cena, cor, som ou expressões faciais. Se um vídeo for indisponível, registrar `blocked` e não presumir conteúdo. Evitar reprodução literal de narrativas, roteiro ou identidade do criador original.

## Ferramentas e custo
- Metadados/legendas: yt-dlp (sujeito às condições de uso, acesso e autorização)
- Local: FFprobe/FFmpeg para codec, duração, thumbnails; PySceneDetect para mudanças de plano
- Áudio: Faster Whisper local CPU int8; modelo e hardware podem ter custo em tempo/RAM
- Código: Repomix para sumarizar repos permitidos
- Plugin opcional: vidIQ plano Free, limitado em créditos. Conectar é ação do usuário
- Plugins gratuitos: TubeAlfred YouTube, YouTube Transcriber, Arcmira, watch-video

## Escada de prioridade para transcrições YouTube
1. yt-dlp (gratuito, sem custo de API, sem chave)
2. vidIQ `vidiq_video_transcript` (5 créditos por chamada, somente com confirmação)
3. Plugins gratuitos do marketplace (TubeAlfred, YouTube Transcriber, Arcmira)
4. Arquivo fornecido pelo usuário (JSON3, VTT, SRT)

## Saídas de aprendizado
Salvar relatório com `{id, url, date, direitos, fontes, evidencias, hipoteses, aplicacao, setor, confianca, lacunas, testes, status}`. Encaminhar para revisão; só unir ao conhecimento confirmado após validação.
