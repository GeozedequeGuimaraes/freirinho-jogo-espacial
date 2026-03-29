<div align="center">

# Freirinho – Jogo Espacial Educativo

### Navegue pelo universo coletando letras para formar palavras

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Pygame](https://img.shields.io/badge/Pygame-00979D?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org)

</div>

---

## Sobre o Projeto

**Freirinho** é um jogo 2D educativo com tema espacial desenvolvido em Python com Pygame. O jogador controla uma nave e explora um universo aberto coletando planetas com letras para formar palavras — na ordem correta! Desvie de asteroides, evite letras erradas e complete os 5 níveis.

Projeto desenvolvido para a disciplina de **Introdução à Programação — CIn-UFPE** (Recife, PE, Brasil).

---

## Demo

<div align="center">
  <img src="screenshots/demo.gif" alt="Demo" width="600">
</div>

## Screenshots

### Gameplay
![Gameplay](screenshots/03-gameplay.png)

### Tela de Vitoria
![Vitoria](screenshots/01-vitoria.png)

### Tela de Derrota
![Derrota](screenshots/02-derrota.png)

---

## Funcionalidades

- **Mundo aberto** — mapa 3x maior que a tela com camera que segue a nave
- **5 niveis** com palavras diferentes: MARTE, TEMA, ARTE, TREM, META
- **Coleta em ordem obrigatoria** — precisa pegar as letras na sequencia correta da palavra
- **Seta indicadora** no HUD mostra qual e a proxima letra
- **Letra fora de ordem** — perde vida mas reaparece em outro lugar do mapa
- **Mini-mapa** — mostra posicao da nave, planetas corretos (verde) e errados (vermelho)
- **Dificuldade progressiva** — mais obstaculos a cada nivel
- **Sistema de vidas** com power-up de vida extra
- Animacoes de explosao coloridas ao coletar planetas
- Placar de letras coletadas exibido na tela

---

## Tecnologias

- **Python** — linguagem principal do desenvolvimento
- **Pygame** — engine para renderizacao, sprites, colisoes e animacoes

---

## Como Executar

1. Instale as dependências:
```bash
pip install pygame
```
2. Clone este repositório:
```bash
git clone https://github.com/GeozedequeGuimaraes/freirinho-jogo-espacial.git
```
3. Acesse a pasta do projeto:
```bash
cd freirinho-jogo-espacial
```
4. Execute o jogo:
```bash
python main.py
```

---

## Controles

| Tecla | Ação |
|-------|------|
| ← ↑ → ↓ / WASD | Move a nave |
| Colidir com letra correta | Coleta a letra e avança na palavra |
| Colidir com letra errada | Perde uma vida |
| ENTER | Reinicia / próximo nível |
| ESC | Sair |

---

## Contexto

Projeto desenvolvido para a disciplina de **Introdução à Programação — CIn-UFPE** (Recife, PE, Brasil).

---

## Autor

**Geozedeque Guimarães** — Estudante de Ciência da Computação — CIn-UFPE
