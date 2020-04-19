# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

import bpy
from io_mesh_w3d.w3d.structs.mesh_structs.vertex_material import *


class VertexMaterialGroup():
    name = 'VertexMaterial'

    @staticmethod
    def create(node_tree, vert_mat, shader):
        instance = node_tree.nodes.new(type='ShaderNodeGroup')
        instance.location = (0, 300)
        instance.width = 300

        instance.node_tree = bpy.data.node_groups['VertexMaterial']
        instance.label = vert_mat.vm_name

        attributes = {'DEFAULT'}
        if vert_mat.vm_info.attributes & USE_DEPTH_CUE:
            attributes.add('USE_DEPTH_CUE')
        if vert_mat.vm_info.attributes & ARGB_EMISSIVE_ONLY:
            attributes.add('ARGB_EMISSIVE_ONLY')
        if vert_mat.vm_info.attributes & COPY_SPECULAR_TO_DIFFUSE:
            attributes.add('COPY_SPECULAR_TO_DIFFUSE')
        if vert_mat.vm_info.attributes & DEPTH_CUE_TO_ALPHA:
            attributes.add('DEPTH_CUE_TO_ALPHA')

        instance.inputs['Attributes'].default_value = attributes

        # TODO: translate those to shader properties
        # floats: UPerSec, VPerSec, UScale, VScale, FPS, Speed, UCenter, VCenter, UAmp, UFreq, UPhase, VAmp, VFreq, VPhase,
        #        UStep, VStep, StepsPerSecond, Offset, Axis, UOffset, VOffset, ClampFix, UseReflect, Period, VPerScale,
        #        BumpRotation, BumpScale
        # ints: Log1Width, Log2Width, Last(Frame)

        instance.inputs['VM_ARGS_0'].default_value = vert_mat.vm_args_0
        instance.inputs['VM_ARGS_0'].default_value = vert_mat.vm_args_1

        instance.inputs['Diffuse'].default_value = vert_mat.vm_info.diffuse.to_vector_rgba()
        instance.inputs['Ambient'].default_value = vert_mat.vm_info.ambient.to_vector_rgba()
        instance.inputs['Specular'].default_value = vert_mat.vm_info.specular.to_vector_rgba()
        instance.inputs['Emissive'].default_value = vert_mat.vm_info.emissive.to_vector_rgba()
        instance.inputs['Shininess'].default_value = vert_mat.vm_info.shininess
        instance.inputs['Opacity'].default_value = vert_mat.vm_info.shininess
        instance.inputs['Translucency'].default_value = vert_mat.vm_info.shininess

        instance.inputs['DepthCompare'].default_value = shader.depth_compare
        instance.inputs['DepthMask'].default_value = shader.depth_mask
        instance.inputs['ColorMask'].default_value = shader.color_mask
        instance.inputs['DestBlend'].default_value = shader.dest_blend
        instance.inputs['FogFunc'].default_value = shader.fog_func
        instance.inputs['PriGradient'].default_value = shader.pri_gradient
        instance.inputs['SecGradient'].default_value = shader.sec_gradient
        instance.inputs['SrcBlend'].default_value = shader.src_blend
        instance.inputs['DetailColorFunc'].default_value = shader.detail_color_func
        instance.inputs['DetailAlphaFunc'].default_value = shader.detail_alpha_func
        instance.inputs['Preset'].default_value = shader.shader_preset
        instance.inputs['AlphaTest'].default_value = shader.alpha_test
        instance.inputs['PostDetailColorFunc'].default_value = shader.post_detail_color_func
        instance.inputs['PostDetailAlphaFunc'].default_value = shader.post_detail_alpha_func

        return instance

    @staticmethod
    def addInputInt(group, name, default=0, min=0, max=255):
        group.inputs.new('NodeSocketInt', name)
        group.inputs[name].default_value = default
        group.inputs[name].min_value = min
        group.inputs[name].max_value = max

    @staticmethod
    def register(name):
        group = bpy.data.node_groups.new(name, 'ShaderNodeTree')
        node_tree = group
        node_tree.name = name
        links = node_tree.links

        # create group inputs
        group_inputs = group.nodes.new('NodeGroupInput')
        group_inputs.location = (-350,0)

        group.inputs.new('NodeSocketMaterialAttributes', 'Attributes')
        group.inputs.new('NodeSocketString', 'VM_ARGS_0')
        group.inputs.new('NodeSocketString', 'VM_ARGS_1')
        group.inputs.new('NodeSocketColor', 'Diffuse')
        group.inputs['Diffuse'].default_value = (0.8, 0.8, 0.8, 1.0)
        group.inputs.new('NodeSocketTexture', 'DiffuseTexture')
        group.inputs.new('NodeSocketTextureAlpha', 'DiffuseTextureAlpha')
        VertexMaterialGroup.addInputInt(group, 'DestBlend', max=1)
        group.inputs.new('NodeSocketColor', 'Ambient')
        group.inputs['Ambient'].default_value = (0.8, 0.8, 0.8, 1.0)
        group.inputs.new('NodeSocketColor', 'Specular')
        group.inputs['Specular'].default_value = (0.8, 0.8, 0.8, 1.0)
        group.inputs.new('NodeSocketColor', 'Emissive')
        group.inputs['Emissive'].default_value = (0.8, 0.8, 0.8, 1.0)
        group.inputs.new('NodeSocketFloat', 'Shininess')
        group.inputs.new('NodeSocketFloat', 'Opacity')
        group.inputs.new('NodeSocketFloat', 'Translucency')

        VertexMaterialGroup.addInputInt(group, 'DepthCompare')
        VertexMaterialGroup.addInputInt(group, 'DepthMask')
        VertexMaterialGroup.addInputInt(group, 'ColorMask')
        VertexMaterialGroup.addInputInt(group, 'FogFunc')
        VertexMaterialGroup.addInputInt(group, 'PriGradient')
        VertexMaterialGroup.addInputInt(group, 'SecGradient')
        VertexMaterialGroup.addInputInt(group, 'SrcBlend')
        VertexMaterialGroup.addInputInt(group, 'Texturing')
        VertexMaterialGroup.addInputInt(group, 'DetailColorFunc')
        VertexMaterialGroup.addInputInt(group, 'DetailAlphaFunc')
        VertexMaterialGroup.addInputInt(group, 'Preset')
        VertexMaterialGroup.addInputInt(group, 'AlphaTest')
        VertexMaterialGroup.addInputInt(group, 'PostDetailColorFunc')
        VertexMaterialGroup.addInputInt(group, 'PostDetailAlphaFunc')

        # create group outputs
        group_outputs = group.nodes.new('NodeGroupOutput')
        group_outputs.location = (300,0)
        group.outputs.new('NodeSocketShader', 'BSDF')

        # create and link nodes
        alpha_pipeline = node_tree.nodes.new(type='ShaderNodeGroup')
        alpha_pipeline.location = (-100, 0)
        alpha_pipeline.node_tree = bpy.data.node_groups['AlphaPipeline']
        links.new(group_inputs.outputs['DiffuseTexture'], alpha_pipeline.inputs['Diffuse'])
        links.new(group_inputs.outputs['DiffuseTextureAlpha'], alpha_pipeline.inputs['Alpha'])
        links.new(group_inputs.outputs['DestBlend'], alpha_pipeline.inputs['DestBlend'])

        shader = node_tree.nodes.new('ShaderNodeEeveeSpecular')
        shader.label = 'Shader'
        shader.location = (100, 0)
        shader.inputs['Normal'].hide = True

        links.new(group_inputs.outputs['DiffuseTexture'], shader.inputs['Base Color'])
        links.new(group_inputs.outputs['Specular'], shader.inputs['Specular'])
        links.new(group_inputs.outputs['Shininess'], shader.inputs['Roughness'])
        links.new(group_inputs.outputs['Emissive'], shader.inputs['Emissive Color'])
        links.new(alpha_pipeline.outputs['Alpha'], shader.inputs['Transparency'])
        links.new(shader.outputs['BSDF'], group_outputs.inputs['BSDF'])