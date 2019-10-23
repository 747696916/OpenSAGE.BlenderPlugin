# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel
# Last Modification 10.2019
import unittest

from mathutils import Vector

from io_mesh_w3d.structs.w3d_rgba import RGBA
from io_mesh_w3d.structs.w3d_material import VertexMaterial, VertexMaterialInfo, \
    MaterialInfo, MaterialPass, TextureStage

from tests.helpers.w3d_rgba import get_rgba, compare_rgbas


def get_vertex_material_info():
    return VertexMaterialInfo(
        attributes=13,
        ambient=get_rgba(), # alpha is only padding in this and below
        diffuse=get_rgba(),
        specular=get_rgba(),
        emissive=get_rgba(),
        shininess=0.5,
        opacity=0.32,
        translucency=0.12)


def compare_vertex_material_infos(self, expected, actual):
    self.assertEqual(expected.attributes, actual.attributes)
    compare_rgbas(self, expected.ambient, actual.ambient)
    compare_rgbas(self, expected.diffuse, actual.diffuse)
    compare_rgbas(self, expected.specular, actual.specular)
    compare_rgbas(self, expected.emissive, actual.emissive)
    self.assertAlmostEqual(expected.shininess, actual.shininess, 5)
    self.assertAlmostEqual(expected.opacity, actual.opacity, 5)
    self.assertAlmostEqual(expected.translucency, actual.translucency, 5)


def get_vertex_material():
    return VertexMaterial(
        vm_name="VM_NAME",
        vm_info=get_vertex_material_info(),
        vm_args_0="VM_ARGS0",
        vm_args_1="VM_ARGS1")


def compare_vertex_materials(self, expected, actual):
    self.assertEqual(expected.vm_name, actual.vm_name)
    self.assertEqual(expected.vm_args_0, actual.vm_args_0)
    self.assertEqual(expected.vm_args_1, actual.vm_args_1)
    compare_vertex_material_infos(self, expected.vm_info, actual.vm_info)


def get_material_info():
    return MaterialInfo(
        pass_count=33,
        vert_matl_count=123,
        shader_count=43,
        texture_count=142)


def compare_material_infos(self, expected, actual):
    self.assertEqual(expected.pass_count, actual.pass_count)
    self.assertEqual(expected.vert_matl_count, actual.vert_matl_count)
    self.assertEqual(expected.shader_count, actual.shader_count)
    self.assertEqual(expected.texture_count, actual.texture_count)


def get_texture_stage(count = 123):
    tx_stage = TextureStage(
        tx_ids=[],
        per_face_tx_coords=[],
        tx_coords=[])

    for i in range(count):
        tx_stage.tx_ids.append(i)
        tx_stage.tx_coords.append((2, 4))
        tx_stage.per_face_tx_coords.append(Vector((33.0, -2.0, 1.0)))
    return tx_stage


def compare_texture_stages(self, expected, actual):
    self.assertEqual(len(expected.tx_ids), len(actual.tx_ids))
    for i in range(len(expected.tx_ids)):
        self.assertEqual(expected.tx_ids[i], actual.tx_ids[i])
    self.assertEqual(len(expected.tx_coords), len(actual.tx_coords))
    for i in range(len(expected.tx_coords)):
        self.assertAlmostEqual(expected.tx_coords[i], actual.tx_coords[i], 5)
    self.assertEqual(len(expected.per_face_tx_coords), len(actual.per_face_tx_coords))
    for i in range(len(expected.per_face_tx_coords)):
        self.assertAlmostEqual(expected.per_face_tx_coords[i], actual.per_face_tx_coords[i], 5)


def get_material_pass(count=33, num_stages=2):
    matpass = MaterialPass(
        vertex_material_ids=[],
        shader_ids=[],
        dcg=[],
        dig=[],
        scg=[],
        shader_material_ids=[],
        tx_stages=[],
        tx_coords=[])

    for i in range(count):
        matpass.vertex_material_ids.append(i)
        matpass.shader_ids.append(i)
        matpass.dcg.append(get_rgba())
        matpass.dig.append(get_rgba())
        matpass.scg.append(get_rgba())
        matpass.shader_material_ids.append(i)
        matpass.tx_coords.append((0.5, 0.7))

    for _ in range(num_stages):
        matpass.tx_stages.append(get_texture_stage())

    return matpass


def compare_material_passes(self, expected, actual):
    self.assertEqual(expected.vertex_material_ids, actual.vertex_material_ids)
    self.assertEqual(expected.shader_ids, actual.shader_ids)

    self.assertEqual(len(expected.dcg), len(actual.dcg))
    for i in range(len(expected.dcg)):
        compare_rgbas(self, expected.dcg[i], actual.dcg[i])

    self.assertEqual(len(expected.dig), len(actual.dig))
    for i in range(len(expected.dig)):
        compare_rgbas(self, expected.dig[i], actual.dig[i])

    self.assertEqual(len(expected.scg), len(actual.scg))
    for i in range(len(expected.scg)):
        compare_rgbas(self, expected.scg[i], actual.scg[i])

    self.assertEqual(expected.shader_material_ids, actual.shader_material_ids)

    self.assertEqual(len(expected.tx_coords), len(actual.tx_coords))
    for i in range(len(expected.tx_coords)):
        self.assertAlmostEqual(expected.tx_coords[i][0], actual.tx_coords[i][0], 5)
        self.assertAlmostEqual(expected.tx_coords[i][1], actual.tx_coords[i][1], 5)

    self.assertEqual(len(expected.tx_stages), len(actual.tx_stages))
    for i in range(len(expected.tx_stages)):
        compare_texture_stages(self, expected.tx_stages[i], actual.tx_stages[i])
