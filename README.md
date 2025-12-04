# cvtpf
Projeto Final da UC de Computação Visual - UALG | LESTI 

# D&D AR Spells – Aplicação de Realidade Aumentada com OpenCV + MediaPipe + YOLO

Este projeto é uma aplicação de **Interação Humano-Computador (IHC)** e **Realidade Aumentada (RA)** desenvolvida em **Python**, usando **OpenCV**, **MediaPipe**, **YOLO** e objetos 3D criados no **Blender**.  
O objetivo é permitir que o utilizador **conjure magias** inspiradas em Dungeons & Dragons **através de gestos das mãos, dedos e movimentos corporais**, com efeitos 3D sobre a imagem da webcam.

---

## Funcionalidades previstas

###  Detecção de gestos das mãos
- Reconhecimento de gestos para conjurar magias.
- Mínimo de **5 gestos dos dedos/mãos** (ex: pinch, palma aberta, V-sign, etc.).
- Cada gesto aciona um feitiço diferente.

###  Reconhecimento de pose corporal
- Mínimo de **5 poses corporais** usadas para ativar animações 3D.
- Exemplo: levantar braço = conjurar escudo.

### Reconhecimento de objetos reais (YOLO)
- Mínimo de **5 objetos reais detectados**, incluindo:
  - D20  
  - Livro/Spellbook  
  - Varinha  
  - Cajado  
  - Itens mágicos genéricos

### Detecção facial
- Usada para efeitos como **lock-on**, troca de skin ou ativação de UI.

### **🧙 Efeitos e magias 3D**
Integrados via objetos exportados do Blender:
- Mage Hand  
- Fireball (orb)  
- Lightning Bolt  
- Shield  
- Heal Pulse  

Cada feitiço aparece como overlay 3D na imagem da webcam.

---

## Requisitos

- Python 3.10 ou superior  
- Webcam HD  
- Sistema operativo Windows/Linux/macOS  
- Dependências:
  - `opencv-python`
  - `mediapipe`
  - `ultralytics` (YOLO)
  - `numpy`
  - `PyOpenGL` / `PyOpenGL_accelerate`
  - `modern-gl` (opcional)
  - Outros listados no `requirements.txt`

---

## ⚙️ Instalação e Setup

#### 1. Criar ambiente virtual
No diretório do projeto:

```bash
python -m venv venv
```
#### 2. Ativar o ambiente virtual e install de dependências

Windows (PowerShell)

```bash
.\venv\Scripts\activate
```

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

#### 3. Pode fazer um teste inicial correndo esta app

```bash
python test_camera.py
```

pip install opencv-python ultralytics numpy mediapipe pygame moderngl trimesh pyrr pyglet



setup 2 (UV, se nao funcionar):

powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
To add C:\Users\USER\.local\bin to your PATH, either restart your shell or run:

set Path=C:\Users\USER\.local\bin;%Path%   (cmd)
$env:Path = "C:\Users\USER\.local\bin;$env:Path"   (powershell)

uv add numpy --native-tls
uv add opencv-python --native-tls
uv add mediapipe --native-tls
uv add pillow --native-tls
uv add ultralytics --native-tls
uv add matplotlib --native-tls

uv run src/main.py


ou

uv venv
uv sync
