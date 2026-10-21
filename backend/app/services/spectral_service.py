"""
SatQuery AI - Spectral Indices & Remote Sensing Biophysical Analytics Service
Calculates NDVI, NDWI, NDBI, and Camouflage De-cloaking heatmaps from multimodal rasters.
"""
import os
import uuid
import numpy as np
from PIL import Image
from typing import Dict, Any, Tuple
from app.core.config import settings
from app.core.logging import logger


class SpectralAnalyticsService:
    """Computes spectral indices, flood extent masks, and vegetation health maps."""

    @staticmethod
    def compute_indices(image_arr: np.ndarray) -> Dict[str, Any]:
        """
        Computes NDVI, NDWI, and NDBI approximations from RGB/Multispectral raster.
        Generates colored heatmap artifact images in storage/evidence/.
        """
        h, w = image_arr.shape[:2]
        if len(image_arr.shape) == 2:
            r = g = b = image_arr.astype(float)
        else:
            r = image_arr[:, :, 0].astype(float)
            g = image_arr[:, :, 1].astype(float)
            b = image_arr[:, :, 2].astype(float)

        # Approximate Green-Red Vegetation Index (NDVI surrogate for standard RGB / Pseudo-NIR)
        # Formula: (G - R) / (G + R + 1e-5)
        denom_ndvi = g + r + 1e-5
        ndvi = (g - r) / denom_ndvi
        ndvi_norm = np.clip((ndvi + 1.0) / 2.0, 0, 1.0)

        # Approximate NDWI (Water Index): (G - B) / (G + B + 1e-5) or Blue dominance
        denom_ndwi = b + g + 1e-5
        ndwi = (b - g) / denom_ndwi
        ndwi_norm = np.clip((ndwi + 1.0) / 2.0, 0, 1.0)

        # Approximate NDBI (Built-up / Urban Index): High Red + Blue with low Green
        denom_ndbi = r + g + 1e-5
        ndbi = (r - g) / denom_ndbi
        ndbi_norm = np.clip((ndbi + 1.0) / 2.0, 0, 1.0)

        # Generate Colored Heatmap for NDVI (Red -> Yellow -> Vibrant Green)
        ndvi_rgb = np.zeros((h, w, 3), dtype=np.uint8)
        ndvi_rgb[:, :, 0] = (255 * (1.0 - ndvi_norm)).astype(np.uint8)  # Red for barren
        ndvi_rgb[:, :, 1] = (255 * ndvi_norm).astype(np.uint8)          # Green for lush
        ndvi_rgb[:, :, 2] = 20

        # Generate Colored Heatmap for NDWI (Dark -> Cyan -> Deep Blue)
        ndwi_rgb = np.zeros((h, w, 3), dtype=np.uint8)
        ndwi_rgb[:, :, 0] = 10
        ndwi_rgb[:, :, 1] = (200 * ndwi_norm).astype(np.uint8)
        ndwi_rgb[:, :, 2] = (255 * ndwi_norm).astype(np.uint8)

        # Generate Colored Heatmap for NDBI (Gray -> Orange -> Vivid Amber Red)
        ndbi_rgb = np.zeros((h, w, 3), dtype=np.uint8)
        ndbi_rgb[:, :, 0] = (255 * ndbi_norm).astype(np.uint8)
        ndbi_rgb[:, :, 1] = (120 * ndbi_norm).astype(np.uint8)
        ndbi_rgb[:, :, 2] = 30

        # Save artifacts
        uid = str(uuid.uuid4())[:8]
        os.makedirs(settings.EVIDENCE_DIR, exist_ok=True)

        ndvi_file = f"spectral_ndvi_{uid}.png"
        ndwi_file = f"spectral_ndwi_{uid}.png"
        ndbi_file = f"spectral_ndbi_{uid}.png"

        Image.fromarray(ndvi_rgb).save(os.path.join(settings.EVIDENCE_DIR, ndvi_file))
        Image.fromarray(ndwi_rgb).save(os.path.join(settings.EVIDENCE_DIR, ndwi_file))
        Image.fromarray(ndbi_rgb).save(os.path.join(settings.EVIDENCE_DIR, ndbi_file))

        avg_ndvi = round(float(np.mean(ndvi)), 3)
        avg_ndwi = round(float(np.mean(ndwi)), 3)
        avg_ndbi = round(float(np.mean(ndbi)), 3)

        veg_coverage = round(float(np.count_nonzero(ndvi > 0.1) / (h * w)) * 100, 1)
        water_coverage = round(float(np.count_nonzero(ndwi > 0.15) / (h * w)) * 100, 1)
        urban_coverage = round(float(np.count_nonzero(ndbi > 0.1) / (h * w)) * 100, 1)

        return {
            "mean_ndvi": avg_ndvi,
            "mean_ndwi": avg_ndwi,
            "mean_ndbi": avg_ndbi,
            "vegetation_coverage_pct": veg_coverage,
            "water_coverage_pct": water_coverage,
            "urban_coverage_pct": urban_coverage,
            "artifacts": {
                "ndvi_url": f"/storage/evidence/{ndvi_file}",
                "ndwi_url": f"/storage/evidence/{ndwi_file}",
                "ndbi_url": f"/storage/evidence/{ndbi_file}",
            }
        }
