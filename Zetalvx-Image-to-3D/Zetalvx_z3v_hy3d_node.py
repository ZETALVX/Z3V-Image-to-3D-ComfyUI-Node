import os
import uuid
import subprocess
import gc
import torch
import comfy.model_management as mm

from pathlib import Path

import numpy as np
from PIL import Image


class Z3VHy3DFromImage:
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),

                "hy3d_python": ("STRING", {
                    "default": "/home/theboss/hy3d/Hunyuan3D-2.1-main/.venv/bin/python"
                }),

                "script_path": ("STRING", {
                    "default": "/home/theboss/hy3d/Hunyuan3D-2.1-main/z3v_official_v3Comfyui.py"
                }),

                "output_dir": ("STRING", {
                    "default": "/home/theboss/hy3d/Hunyuan3D-2.1-main/comfyui_output"
                }),

                "remove_bg": ("BOOLEAN", {
                    "default": False
                }),

                "delay": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.0,
                    "max": 60.0,
                    "step": 0.5
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("output_folder", "model_path", "job_id", "input_image_path")

    FUNCTION = "run"
    CATEGORY = "ZetaLVX/3D"

    def run(self, image, hy3d_python, script_path, output_dir, remove_bg, delay):
        print("[ZEV HY3D] NODE STARTED")
        output_root = Path(output_dir).expanduser().resolve()
        output_root.mkdir(parents=True, exist_ok=True)

        job_id = f"comfy_{uuid.uuid4().hex[:8]}"
        input_path = output_root / f"{job_id}.png"

        # ComfyUI IMAGE tensor: [batch, height, width, channels], float 0..1
        img = image[0].cpu().numpy()
        img = np.clip(img * 255.0, 0, 255).astype(np.uint8)

        Image.fromarray(img).save(input_path)

        cmd = [
            hy3d_python,
            script_path,
            "--path", str(input_path),
            "--output", str(output_root),
            "--delay", str(delay),
        ]

        if remove_bg:
            cmd.append("--remove-bg")

        print("[ZEV HY3D] Running command:")
        print(" ".join(cmd))

        print("[ZEV HY3D] Unloading ComfyUI models before HY3D...")

        mm.unload_all_models()
        mm.soft_empty_cache()

        gc.collect()

        if torch.cuda.is_available():
            torch.cuda.synchronize()
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

        print("[ZEV HY3D] GPU memory cleanup done")

        result = subprocess.run(
            cmd,
            cwd=str(Path(script_path).resolve().parent),
        )

        if result.returncode != 0:
            raise RuntimeError(f"HY3D failed with exit code {result.returncode}")

        item_output_folder = output_root / job_id

        model_path = ""

        # Prima cerca i textured
        candidates = list(item_output_folder.glob("*textured*.glb"))
        candidates += list(item_output_folder.glob("*textured*.obj"))

        # Poi fallback su qualunque glb/obj
        if not candidates:
            candidates = list(item_output_folder.glob("*.glb"))
            candidates += list(item_output_folder.glob("*.obj"))

        if candidates:
            # prende il file più recente
            candidates = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
            model_path = str(candidates[0])
        else:
            model_path = str(item_output_folder)

        return (str(item_output_folder), model_path, job_id, str(input_path))