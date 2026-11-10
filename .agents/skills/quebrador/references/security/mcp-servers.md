# Servidores MCP — Inventário de Referência

> **AVISO**: Nenhum servidor MCP está instalado ou conectado. Nomes de MCP não comprovam existência, autenticidade ou segurança. Antes de qualquer conexão: verificar URI oficial, contrato de ferramentas, mínimo privilégio e autorização explícita de dSanT.

**Total**: 30 servidores listados | **Instalados**: 0 | **Conectados**: 0

---

## Engenharia Reversa

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| ghidra-mcp | RE / Descompilação | Análise de binários, descompilação, grafos de chamadas, renomeação de funções | Ghidra instalado, Java 17+ | inventário, não instalado |
| ida-pro-mcp | RE / Descompilação | Navegação IDB, descompilação Hex-Rays, scripts IDAPython | IDA Pro (licença comercial) | inventário, não instalado |
| radare2-mcp | RE / Análise binária | Desmontagem, análise de fluxo, emulação ESIL, strings | radare2/rizin instalado | inventário, não instalado |

## Depuração

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| kernel-debug-mcp | Kernel / Debug | Breakpoints de kernel, análise de crash dump, inspeção de estruturas | WinDbg ou kd, VM com debug habilitado | inventário, não instalado |
| windbg-mcp | Debug Windows | Depuração user/kernel, análise de dump, extensões | WinDbg Preview ou clássico | inventário, não instalado |
| x64dbg-mcp | Debug Windows | Breakpoints, stepping, patches, scripts | x64dbg instalado (Windows) | inventário, não instalado |

## Rede

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| nmap-mcp | Escaneamento de rede | Port scan, service detection, scripts NSE, OS fingerprint | nmap instalado | inventário, não instalado |
| wireshark-mcp | Captura de pacotes | Análise PCAP, filtros, dissectors, estatísticas | Wireshark/tshark instalado | inventário, não instalado |
| bettercap-mcp | MITM / Rede | Interceptação, spoofing, Wi-Fi, BLE, HTTP proxy | bettercap instalado, root | inventário, não instalado |
| shodan-mcp | OSINT / Rede | Busca de hosts, banners, vulnerabilidades, estatísticas | API key Shodan | inventário, não instalado |

## Pentest

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| metasploit-mcp | Pentest / Exploração | Módulos exploit/payload/auxiliary, sessões, pivoting | msf instalado, PostgreSQL | inventário, não instalado |
| frida-mcp | Instrumentação dinâmica | Hook de funções, trace, interceptação, scripts JS | frida + frida-tools instalados | inventário, não instalado |

## SAST e Qualidade de Código

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| codeql-mcp | Análise semântica | Queries CodeQL, busca de padrões, vulnerabilidades | CodeQL CLI + databases | inventário, não instalado |
| semgrep-mcp | Análise estática | Regras customizáveis, SAST multi-linguagem | semgrep instalado | inventário, não instalado |

## Nuvem

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| aws-mcp | Segurança AWS | Auditoria IAM, S3, EC2, CloudTrail, configuração | AWS CLI + credenciais | inventário, não instalado |
| azure-mcp | Segurança Azure | Auditoria de recursos, RBAC, políticas, logs | Azure CLI + credenciais | inventário, não instalado |
| gcp-mcp | Segurança GCP | Auditoria IAM, buckets, instances, logs | gcloud CLI + credenciais | inventário, não instalado |
| kubernetes-mcp | Segurança K8S | Pods, RBAC, network policies, secrets, namespaces | kubectl + kubeconfig | inventário, não instalado |

## Firmware e Emulação

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| qemu-mcp | Emulação | VMs, emulação de firmware, snapshots, debug GDB | QEMU instalado | inventário, não instalado |
| firmware-mcp | Análise de firmware | Extração, análise de filesystem, busca de vulnerabilidades | binwalk, firmware-mod-kit | inventário, não instalado |

## Segurança de IA

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| garak-mcp | Teste de LLM | Probes de jailbreak, toxicidade, vazamento, robustez | garak instalado, Python 3.10+ | inventário, não instalado |
| prompt-injection-tester-mcp | Teste de prompt | Injeção, exfiltração, bypass de guardrails | Python, API keys de LLM | inventário, não instalado |

## Mobile

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| frida-mcp | Instrumentação mobile | Hook Android/iOS, bypass SSL pinning, trace | frida + dispositivo/emulador | inventário, não instalado |
| jadx-mcp | Decompilação Android | Decompilação APK/DEX, busca de strings, análise | jadx instalado, Java | inventário, não instalado |

## Contratos Inteligentes

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| foundry-mcp | Dev/Teste Solidity | Compilação, testes, deploy local, fuzzing | foundry (forge, cast, anvil) | inventário, não instalado |
| slither-mcp | Análise de contratos | Detecção de vulnerabilidades, grafos, printers | slither instalado, solc | inventário, não instalado |

## Infraestrutura Base

| Nome | Domínio | Ferramentas expostas | Dependências | Status |
|---|---|---|---|---|
| filesystem-mcp | Acesso a arquivos | Leitura, escrita, navegação de diretórios | Nenhuma adicional | inventário, não instalado |
| memory-mcp | Armazenamento persistente | Memória chave-valor para contexto entre sessões | Nenhuma adicional | inventário, não instalado |
| github-mcp | Integração GitHub | Repos, issues, PRs, actions, busca de código | Token GitHub | inventário, não instalado |
| process-mcp | Processos do sistema | Listar, monitorar, gerenciar processos | Permissões de sistema | inventário, não instalado |
| virustotal-mcp | Análise de malware | Scan de arquivos/URLs, relatórios, IOCs | API key VirusTotal | inventário, não instalado |

---

## Guia rápido de instalação (genérico)

A instalação de qualquer MCP requer:
1. Verificar se o servidor existe no registry oficial ou marketplace
2. Auditar o código-fonte e dependências
3. Configurar com mínimo privilégio
4. Obter autorização explícita de dSanT antes de conectar
5. Testar em ambiente isolado antes de uso em produção

Nenhum MCP deve ser instalado automaticamente por esta skill.
