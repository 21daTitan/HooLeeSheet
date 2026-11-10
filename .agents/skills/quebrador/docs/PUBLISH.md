# Publicação privada no GitHub

1. Instale [GitHub CLI](https://cli.github.com/) na máquina/VPS e autentique **interativamente**: `gh auth login` (não cole tokens na conversa).
2. Execute o script `bash scripts/publish_private.sh` **e confirme digitando a frase exibida no terminal**; o script recusa execução não interativa. Não rode antes de revisar arquivos e política de privacidade.
3. Se `git commit` pedir identidade: configure `git config user.name` e `git config user.email` localmente.
4. Acesse Settings > Actions > General no repo, habilite GitHub Actions, `Read and write permissions` para o `GITHUB_TOKEN` se necessário.
5. O workflow `watch.yml` **não possui agendamento automático**. Só pode ser acionado manualmente pelo dono `21daTitan`.

O script executa testes, verifica pré-condições, recusa sobrescrever um repositório existente e cria a origem privada.
