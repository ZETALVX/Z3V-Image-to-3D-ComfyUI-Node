# Z3V Image-to-3D ComfyUI Node

ComfyUI custom node bridge for **Z3V Image-to-3D**, a local image-to-3D pipeline based on **Hunyuan3D 2.1**.

This node allows you to generate an image inside ComfyUI and automatically send it to an external Python script that creates a 3D model.

---

# Typical Workflow

```text
Qwen prompt generation
        ↓
Qwen Image generation
        ↓
Z3V Image-to-3D ComfyUI Node
        ↓
HY3D script
        ↓
GLB / OBJ 3D model
```

---

# Important

This repository is only the **ComfyUI bridge node**.

Before using this node, you must install and configure the main **Z3V Image-to-3D** project:

https://github.com/ZETALVX/Z3V-Image-to-3D

The external HY3D script, its Python environment, dependencies, and models must already work from command line before using this ComfyUI node.

---

# Requirements

## Tested Setup

- Ubuntu Linux
- ComfyUI
- Python 3.11
- NVIDIA GPU
- CUDA-compatible PyTorch
- Hunyuan3D 2.1 models
- Z3V Image-to-3D installed and working

## Recommended

- 24GB VRAM or more
- 32GB+ system RAM
- 32GB+ swap for heavy workflows

---

# Installation

## 1. Install the main Z3V Image-to-3D project

First install and test:

https://github.com/ZETALVX/Z3V-Image-to-3D

Make sure this command works before continuing:

```bash
/path/to/hy3d/.venv/bin/python \
/path/to/Z3V-Image-to-3D/z3v_official_v3Comfyui.py \
--path /path/to/test_image.png \
--output /path/to/output
```

If the script does not work from terminal, it will not work inside ComfyUI.

---

## 2. Install this ComfyUI custom node

Copy the folder:

```text
Zetalvx-Image-to-3D
```

into:

```text
ComfyUI/custom_nodes/
```

Final structure:

```text
ComfyUI/
└── custom_nodes/
    └── Zetalvx-Image-to-3D/
        ├── __init__.py
        └── Zetalvx_z3v_hy3d_node.py
```

Restart ComfyUI.

---

# Node

After restarting ComfyUI, search for:

```text
ZetaLvx - Z3V V.1 - Image to 3D
```

The node receives an image from ComfyUI and sends it to the external HY3D script.

---

# Node Inputs

## image

The image generated or loaded inside ComfyUI.

---

## hy3d_python

Path to the Python executable of your Z3V / HY3D virtual environment.

Example:

```text
/home/user/hy3d/Hunyuan3D-2.1-main/.venv/bin/python
```

Do NOT use:

```text
activate
```

Use the actual Python binary inside the virtual environment.

---

## script_path

Path to the external Z3V image-to-3D script.

Example:

```text
/home/user/hy3d/Hunyuan3D-2.1-main/z3v_official_v3Comfyui.py
```

---

## output_dir

Folder where the generated images and 3D models will be saved.

Example:

```text
/home/user/hy3d/Hunyuan3D-2.1-main/comfyui_output
```

---

## remove_bg

If enabled, the script removes the image background before generating the 3D model.

---

## delay

Delay in seconds after generation.

Useful to reduce CUDA / memory pressure between runs.

---

# Node Outputs

## output_folder

The folder generated for the current job.

---

## model_path

Detected path of the generated 3D model.

Usually a `.glb` or `.obj` file.

---

## job_id

Internal generated job name.

Example:

```text
comfy_ab12cd34
```

---

## input_image_path

The temporary image saved by the node and passed to the HY3D script.

---

# Example Output Structure

```text
comfyui_output/
└── comfy_ab12cd34/
    ├── comfy_ab12cd34_bgremoved.png
    ├── comfy_ab12cd34_shape.glb
    └── comfy_ab12cd34_textured.glb
```

---

# Suggested ComfyUI Workflow

```text
Text prompt
    ↓
Qwen Image
    ↓
Z3V Image-to-3D Node
    ↓
Preview model path / output folder
```

If you use a 3D preview node, connect:

```text
model_path
```

NOT:

```text
job_id
```

`job_id` is only the generated folder/name, while `model_path` is the actual 3D file path.

---

# Memory Notes

This workflow can be heavy because ComfyUI and HY3D may both use GPU and system memory.

If you get:

```text
Killed
```

this is usually Linux killing the process because of system RAM / swap pressure.

---

# Recommended Swap Setup

```bash
sudo swapoff /swap.img
sudo rm /swap.img

sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

free -h
```

To make it permanent:

```bash
sudo nano /etc/fstab
```

Replace:

```text
/swap.img none swap sw 0 0
```

with:

```text
/swapfile none swap sw 0 0
```

---

# Troubleshooting

## The node does nothing

Make sure the node is connected to an image output.

The node is an output node, so it should run when the workflow is executed.

---

## No logs appear

Check the ComfyUI terminal.

You should see:

```text
[ZEV HY3D] NODE STARTED
[ZEV HY3D] Running command:
```

---

## HY3D fails with CUDA OOM

Try:

- Lower resolution
- Close other GPU processes
- Use ComfyUI low VRAM mode
- Increase system swap
- Make sure ComfyUI unloads models before starting HY3D

---

## Script works in terminal but not in ComfyUI

Check these paths in the node:

```text
hy3d_python
script_path
output_dir
```

They must match your local installation.

---

# Notes

This node does NOT install Hunyuan3D automatically.

It is a bridge between ComfyUI and an already working Z3V Image-to-3D setup.

The recommended approach is to keep the ComfyUI environment and the HY3D environment separate.

---

# Credits

Based on:

- Z3V Image-to-3D by ZETALVX
- Hunyuan3D 2.1 by Tencent
- ComfyUI custom node system

---

# Disclaimer

This is an experimental local AI workflow.

Generated 3D models may require cleanup depending on the source image, object shape, and HY3D output.
