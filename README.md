# Visualizador IFC para GLB

Este é um aplicativo Streamlit que permite enviar um arquivo `.ifc`, convertê-lo automaticamente para `.glb` e visualizá-lo via visualizador 3D online.

## Como usar

1. Faça upload de um arquivo IFC.
2. O sistema tentará convertê-lo para GLB.
3. A visualização 3D será mostrada via [3DViewer.net](https://3dviewer.net).

> ⚠️ Algumas funções de geometria 3D requerem que o `ifcopenshell.geom` esteja corretamente instalado com suporte ao OpenCascade. Se estiver usando Codespaces ou ambiente que não suporta esse backend, você verá uma mensagem de erro amigável.

## Requisitos

Instale os pacotes necessários com:

```bash
pip install -r requirements.txt
```

Execute o app com:

```bash
streamlit run app.py
```