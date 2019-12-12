# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

from io_mesh_w3d.structs_w3x.w3x_struct import Struct
from io_mesh_w3d.io_xml import *


class RenderObject(Struct):
    meshes = []

    @staticmethod
    def parse(xml_render_object):
        render_object = RenderObject(meshes=[])
        xml_meshes = xml_render_object.getElementsByTagName('Mesh')
        for xml_mesh in xml_meshes:
            render_object.meshes.append(xml_mesh.data)
        return render_object

    def create(self, doc):
        render_object = doc.createElement('RenderObject')
        for mesh in self.meshes:
            xml_mesh = doc.createElement('Mesh')
            xml_mesh.data = mesh
            render_object.appendChild(xml_mesh)
        return render_object


class SubObject(Struct):
    id = ""
    bone_index = 0
    render_objects = []

    @staticmethod
    def parse(xml_sub_object):
        sub_object = SubObject(
            id=xml_sub_object.attributes['SubObjectID'].value,
            bone_index=int(xml_sub_object.attributes['BoneIndex'].value))

        xml_render_objects = xml_sub_object.getElementsByTagName('RenderObject')
        for xml_render_object in xml_render_objects:
            sub_object.render_objects.append(RenderObject.parse(xml_render_object)
        return sub_object

    def create(self, doc):
        sub_object = doc.createElement('SubObject')
        sub_object.setAttribute('SubObjectID', self.id)
        sub_object.setAttribute('BoneIndex', self.bone_index)

        for render_object in self.render_objects:
            sub_object.appendChild(render_object.create(doc))
        return sub_object


class Container(Struct):
    id = ""
    hierarchy = ""
    sub_objects = []

    @staticmethod
    def parse(xml_container):
        container = Container(
            id=xml_container.attributes['id'].value,
            hierarchy=xml_container.attributes['Hierarchy'].value)

        xml_sub_objects = xml_container.getElementsByTagName('SubObject')
        for xml_sub_object in xml_sub_objects:
            container.sub_objects.append(SubObject.parse(xml_sub_object))
        return container

    def create(self, doc):
        container = doc.createElement('Container')
        texture.setAttribute('id', self.id)
        texture.setAttribute('Hierarchy', self.hierarchy)

        for sub_object in self.sub_objects:
            sub_object.create(doc)
        return container
