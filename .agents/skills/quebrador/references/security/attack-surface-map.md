# Mapa de Superfície de Ataque — Referência Cruzada

> **AVISO**: Este mapa é referência educacional para pesquisa autorizada, CTF e defesa. Nenhuma ferramenta foi instalada. Cenários descritos são para uso em ambientes autorizados com permissão explícita de dSanT. Não é um playbook operacional.

---

## 1. Engenharia Reversa Windows

| Item | Detalhes |
|---|---|
| **Objetivo** | Análise de binários PE, descompilação, reconstrução de lógica |
| **Repos** | ghidra, radare2, rizin, cutter, x64dbg, pe-sieve, hollows_hunter, Detect-It-Easy, dnSpy, ReClass.NET |
| **MCPs** | ghidra-mcp, x64dbg-mcp, ida-pro-mcp |
| **Skills** | assembly-x64, ghidra, x64dbg, manual-unpacking, detect-it-easy, reclass, scylla |
| **Websites** | Exploit-DB (referência de vulnerabilidades), NVD (CVEs) |

## 2. Análise de Malware

| Item | Detalhes |
|---|---|
| **Objetivo** | Triagem, análise estática/dinâmica, IOCs, relatório de ameaças |
| **Repos** | ghidra, pe-sieve, hollows_hunter, Hunt-Sleeping-Beacons, al-khaser, ScyllaHide, OffensiveNim, DeepSleep, FOLIAGE |
| **MCPs** | ghidra-mcp, virustotal-mcp, x64dbg-mcp, windbg-mcp |
| **Skills** | malware-keygen-triage, antidebug, windows-internals, manual-unpacking, live-debugging |
| **Websites** | VirusTotal, PacketStorm, NVD, CVE Mitre |

## 3. Pentest de Rede

| Item | Detalhes |
|---|---|
| **Objetivo** | Escaneamento, enumeração, interceptação, exploração de serviços |
| **Repos** | metasploit-framework, nmap (via nmap-mcp), wireshark, bettercap, scapy, mitmproxy, zaproxy, Responder, mitm6, hashcat |
| **MCPs** | metasploit-mcp, nmap-mcp, wireshark-mcp, bettercap-mcp, shodan-mcp |
| **Skills** | (contexto de rede não tem skill dedicada; usar docs de repos) |
| **Websites** | Shodan, ZoomEye, FOFA, SecurityTrails, BGP HE, YouGetSignal |

## 4. Segurança Web

| Item | Detalhes |
|---|---|
| **Objetivo** | Teste de aplicações web, XSS, SQLi, SSRF, autenticação |
| **Repos** | zaproxy, mitmproxy, selenium, playwright, puppeteer, beautifulsoup, scrapy |
| **MCPs** | wireshark-mcp, bettercap-mcp |
| **Skills** | python-re (para automação de testes) |
| **Websites** | OWASP, Exploit-DB, CrackStation (para hashes encontrados), NVD |

## 5. Segurança de API e LLM

| Item | Detalhes |
|---|---|
| **Objetivo** | Teste de prompt injection, jailbreak, guardrails, robustez de modelos |
| **Repos** | garak, promptfoo, deepeval, llm-guard, PurpleLlama, NeMo-Guardrails, promptinject, LLMFuzzer, JailbreakBench, HarmBench, adversarial-robustness-toolbox, TextAttack, OpenAttack |
| **MCPs** | garak-mcp, prompt-injection-tester-mcp |
| **Skills** | llm-security |
| **Websites** | OWASP Top 10 para LLM |

## 6. Segurança Kubernetes

| Item | Detalhes |
|---|---|
| **Objetivo** | Auditoria de clusters, RBAC, network policies, supply chain de containers |
| **Repos** | kube-hunter, kube-bench, kubescape, trivy, grype, syft, cosign, falco, tracee, kyverno, gatekeeper, opa, checkov, kics, tfsec, terrascan, prowler |
| **MCPs** | kubernetes-mcp, aws-mcp, gcp-mcp, azure-mcp |
| **Skills** | cloud-security, supply-chain-security |
| **Websites** | NVD (CVEs de containers), Shodan (exposição de APIs K8S) |

## 7. Análise Mobile

| Item | Detalhes |
|---|---|
| **Objetivo** | RE de APKs, análise dinâmica, bypass de proteções, pentesting mobile |
| **Repos** | frida, objection, jadx, Apktool, dex2jar, MobSF, drozer, Xposed, EdXposed, LSPosed, Magisk, ZygiskNext |
| **MCPs** | frida-mcp, jadx-mcp |
| **Skills** | android-reverse, python-re |
| **Websites** | NVD, Exploit-DB |

## 8. Firmware e IoT

| Item | Detalhes |
|---|---|
| **Objetivo** | Extração e análise de firmware, emulação, busca de vulnerabilidades |
| **Repos** | binwalk, chipsec, UEFITool, flashrom, firmware-mod-kit, firmadyne, FACT_core, emba, coreboot, qemu, uefi-firmware-parser |
| **MCPs** | qemu-mcp, firmware-mcp |
| **Skills** | (usar docs dos repos; combinar com assembly-internals para análise de baixo nível) |
| **Websites** | Shodan (dispositivos IoT), NVD, PacketStorm |

## 9. Active Directory

| Item | Detalhes |
|---|---|
| **Objetivo** | Enumeração, escalação de privilégios, movimentação lateral em domínios AD |
| **Repos** | impacket, BloodHound, SharpHound, BloodHound.py, PetitPotam, Coercer, noPac, ShadowCoerce, Certipy, krbrelayx, PyWhisker, mimikatz, Responder |
| **MCPs** | metasploit-mcp, nmap-mcp |
| **Skills** | windows-internals, syscalls |
| **Websites** | CVE Mitre, NVD, Exploit-DB |

## 10. Smart Contracts e Blockchain

| Item | Detalhes |
|---|---|
| **Objetivo** | Auditoria de contratos Solidity, fuzzing, verificação formal, segurança de consenso |
| **Repos** | slither, mythril, echidna, foundry, hardhat, halmos, scribble, solhint, solgraph, surya, openzeppelin-contracts, solmate, mev-boost, lighthouse, teku, prysm, sigstore, fulcio, rekor, in-toto, harden-runner |
| **MCPs** | foundry-mcp, slither-mcp |
| **Skills** | blockchain-security |
| **Websites** | NVD, Exploit-DB (smart contract exploits) |

---

## Legenda de escopos

| Escopo | Significado |
|---|---|
| `read_only` | Leitura de documentação e código-fonte; sem execução |
| `research_only` | Análise para pesquisa defensiva; requer ambiente isolado |
| `manual_review` | Revisão manual obrigatória antes de qualquer uso |

Qualquer execução requer autorização explícita e específica de dSanT.
