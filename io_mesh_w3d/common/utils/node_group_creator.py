# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

import os
import bpy
from io_mesh_w3d.common.io_xml import *


class NodeGroupCreator():
    def process_input_hides(self, xml_node, node):
        for child_node in xml_node:
            if child_node.tag != 'hide':
                continue
            id = child_node.get('id')
            port_type = child_node.get('type')

            if port_type == 'input':
                node.inputs[id].hide = True
            else:
                node.outputs[id].hide = True


    def process_default_value(self, socket, default):
        if default is None:
            return
        if socket.type == 'VALUE':
            default = float(default)
        elif socket.type == 'INT':
            default = int(default)
        elif socket.type == 'BOOLEAN':
            default = int(default)
        elif socket.type == 'RGBA':
            values = default.split(',')
            default = Vector((float(values[0]), float(values[1]), float(values[2]), float(values[3])))
        socket.default_value = default


    def process_min_value(self, socket, min):
        if min is None:
            return
        if socket.type == 'FLOAT':
            min = float(min)
        elif socket.type == 'INT':
            min = int(min)
        socket.min_value = min


    def process_max_value(self, socket, max):
        if max is None:
            return
        if socket.type == 'FLOAT':
            max = float(max)
        elif socket.type == 'INT':
            max = int(max)
        socket.max_value = max


    def process_presets(self, socket, xml_node, name=None):
        if name is None:
            name = xml_node.get('name', xml_node.get('id'))

        self.process_default_value(socket, xml_node.get('default'))
        self.process_min_value(socket, xml_node.get('min'))
        self.process_max_value(socket, xml_node.get('max'))


    def create_input_node(self, node_tree, xml_node, node):
        for child_node in xml_node:
            if child_node.tag != 'input':
                continue
            type = child_node.get('type')
            name = child_node.get('name')

            if type == 'NodeSocketTexture':
                type = 'NodeSocketColor'

            socket = node_tree.inputs.new(type, name)
            self.process_presets(socket, child_node, name)


    def create_output_node(self, node_tree, xml_node, node):
        for child_node in xml_node:
            if child_node.tag != 'output':
                continue
            node_tree.outputs.new(child_node.get('type'), child_node.get('name'))


    def create(self, directory, file, node_tree=None):
        path = os.path.join(directory, file)
        root = find_root(None, path)
        if root is None:
            return

        name = root.get('name')
        if name in bpy.data.node_groups and node_tree is None:
            return

        if node_tree is None:
            node_tree = bpy.data.node_groups.new(name, 'ShaderNodeTree')

        links = node_tree.links
        nodes = {}

        for xml_node in root:
            location = (float(xml_node.get('X', 0.0)), float(xml_node.get('Y', 0.0)))

            if xml_node.tag == 'include':
                file = xml_node.get('file')
                NodeGroupCreator().create(directory, file)

            elif xml_node.tag == 'parent':
                parent = xml_node.get('file')
                nodes = NodeGroupCreator().create(directory, parent, node_tree)

            elif xml_node.tag == 'node':
                type = xml_node.get('type')
                node = node_tree.nodes.new(type)

                node.location = location
                nodes[xml_node.get('name')] = node

                self.process_input_hides(xml_node, node)

                if type == 'NodeGroupInput':
                    self.create_input_node(node_tree, xml_node, node)
                elif type == 'NodeGroupOutput':
                    self.create_output_node(node_tree, xml_node, node)
                elif type == 'ShaderNodeMath':
                    node.operation = xml_node.get('mode').upper()
                    self.process_presets(node_tree, xml_node)
                elif type in ['ShaderNodeEeveeSpecular', 'ShaderNodeNormalMap', 'ShaderNodeSeparateHSV']:
                    continue
                else:
                    print('shader node type: ' + type + ' is not yet supported')

            elif xml_node.tag == 'nodegroup':
                nodegroup = node_tree.nodes.new(type='ShaderNodeGroup')
                nodegroup.location = location
                nodegroup.node_tree = bpy.data.node_groups[xml_node.get('type')]
                nodes[xml_node.get('name')] = nodegroup

            elif xml_node.tag == 'link':
                (from_node, from_port, from_input) = xml_node.get('from').split('.')
                (to_node, to_port, to_input) = xml_node.get('to').split('.')

                if from_input.isdigit():
                    from_input = int(from_input)
                if to_input.isdigit():
                    to_input = int(to_input)

                if from_port == 'inputs':
                    from_ref = nodes[from_node].inputs[from_input]
                else:
                    from_ref = nodes[from_node].outputs[from_input]

                if to_port == 'inputs':
                    to_ref = nodes[to_node].inputs[to_input]
                else:
                    to_ref = nodes[to_node].outputs[to_input]

                links.new(from_ref, to_ref)
            else:
                print('node type: ' + xml_node.tag + ' is not supported')
        return nodes