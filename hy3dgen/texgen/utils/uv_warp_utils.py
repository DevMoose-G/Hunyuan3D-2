# Hunyuan 3D is licensed under the TENCENT HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT
# except for the third-party components listed below.
# Hunyuan 3D does not impose any additional limitations beyond what is outlined
# in the repsective licenses of these third-party components.
# Users must comply with all terms and conditions of original licenses of these third-party
# components and must ensure that the usage of the third party components adheres to
# all relevant laws and regulations.

# For avoidance of doubts, Hunyuan 3D means the large language models and
# their software and algorithms, including trained model weights, parameters (including
# optimizer states), machine-learning model code, inference-enabling code, training-enabling code,
# fine-tuning enabling code and other elements of the foregoing made publicly available
# by Tencent in accordance with TENCENT HUNYUAN COMMUNITY LICENSE AGREEMENT.

import numpy as np
import trimesh
# import xatlas
import open3d as o3d

def mesh_uv_wrap(mesh, atlas_size=1024, gutter=2.0, max_stretch=0.1):
    """
    Compute per-vertex UVs on `mesh` using Open3D’s compute_uvatlas,
    then write them back into the Trimesh object.
    
    Args:
        mesh (trimesh.Scene or trimesh.Trimesh): input mesh.
        atlas_size (int): texture resolution (width=height).
        gutter (float): pixel padding around UV charts.
        max_stretch (float): max allowed UV stretching [0..1].
    
    Returns:
        trimesh.Trimesh: same mesh with updated mesh.visual.uv.
    """
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump(concatenate=True)

    if len(mesh.faces) > 500000000:
        raise ValueError("The mesh has more than 500,000,000 faces, which is not supported.")

    mesh.export("curr_mesh.obj")
    legacy = o3d.io.read_triangle_mesh("curr_mesh.obj")
    tmesh = o3d.t.geometry.TriangleMesh.from_legacy(legacy)
    tmesh.compute_uvatlas(size=atlas_size, gutter=gutter, max_stretch=max_stretch, parallel_partitions=4, nthreads=0)
    legacy_out = tmesh.to_legacy()
    uvs = np.asarray(legacy_out.triangle_uvs).reshape(-1, 2)

    mesh.visual.uv = uvs

    return mesh
