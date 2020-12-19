import bpy
import bmesh
from bpy_extras import view3d_utils
from bpy.props import BoolProperty

def menu_draw(self, context):
    self.layout.operator("mesh.vertex_rip_merge_keep_normals")

def ray_cast_get_face_index(context, event):
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    mouse_region = event.mouse_region_x, event.mouse_region_y

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse_region)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse_region)

    ray_target = ray_origin + view_vector
    
    result, location, normal, index, object, matrix = scene.ray_cast(context.view_layer, ray_origin, ray_target)
    if result and index > -1:
        return index
    else:
        return -1

def rip(mesh, vert, face, up):
    if len(vert.link_edges) <= 3:
        return None
    
    face_edges, ext_edges = [], []
    for e in vert.link_edges:
        (face_edges, ext_edges)[e in face.link_edges].append(e)
    face_verts = [next(v for v in e.verts if v != vert) for e in face_edges]
    ext_verts = [next(v for v in e.verts if v != vert) for e in ext_edges]
    
    if up:
        new_verts = []
        for e in ext_edges:
            # TODO: check split location, should it be 0.0 or 1.0?
            new_edge, new_vert = bmesh.utils.edge_split(e, vert, 0.0)
            new_verts.append(new_vert)
            
        # pointmerge doesn't return the new vertex (for some reason ?!)
        # so we're instead creating new verts on the ext_edges
        # so that we can return the original vert as the one that is to be moved
        bmesh.ops.pointmerge(new_verts, vert.co)
        
        new_ext_edges = [e for e in vert.link_edges if e not in face_edges]
        if len(new_ext_edges) != 1:
            raise Exception('Rip Up pointmerge has incorrect edge count')
        
        return vert
    else:
        new_verts = []
        for e in ext_edges:
            # TODO: check split location, should it be 0.0 or 1.0?
            new_edge, new_vert = bmesh.utils.edge_split(e, vert, 0.0)
            new_verts.append(new_vert)
            
        # is this return accessed with ['edges']?
        connect_verts = [v for v in new_verts] + face_verts
        # what's the difference between connect_vert_pair and connect_verts?
        # last parameter is so we don't split the target face
        connecting_edges = bmesh.ops.connect_vert_pair(mesh, connect_verts, [], [face])
        dissolve_success = bmesh.utils.vert_dissolve(vert)
        if not dissolve_success:
            raise Exception('Rip Down dissolve of original vertex did not work')
        
        return new_verts


def split(context, event, up):
    mesh = bmesh.from_edit_mesh(context.active_object.data)
    active_vert = mesh.select_history.active
    
    hovered_face_index = ray_cast_get_face_index(context, event)
    hovered_face = mesh.faces[hovered_face_index]
    print(hovered_face_index)
    
    
    """
    selected_verts = [v for v in mesh.verts if v.select]
    # rmf todo: get active vert
    active_vert = selected_verts[0]
    
    if len(active_vert.link_edges) <= 3:
        return False
    
    possible_faces = active_vert.link_faces
    
    for s_v in selected_verts:
        possible_faces = [ f for f in possible_faces if f in s_v.link_faces ]
    
    chosen_face = possible_faces[0]
    
    slide_magnitude = sum([ e.calc_length for e in active_vert.link_edges ])
    slide_magnitude = slide_magnitude / len(active_vert.link_edges) / 4.0
    
    if up:
        
    else:
        

    # adjust uv coordinates
    for face in bm.faces:
        if face.
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            # use xy position of the vertex as a uv coordinate
            loop_uv.uv = loop.vert.co.xy
    """
    bmesh.update_edit_mesh(me)
    return True


class VertexRipForFace(bpy.types.Operator):
    """Vertex Rip to edit one face normal while leaving the others the same"""
    bl_idname = "mesh.vertex_rip_merge_keep_normals"
    bl_label = "Vertex Rip/Merge w/ Keep Normals"
    bl_options = {'REGISTER', 'UNDO'}
    
    # exposed properties 
    # direction_up : BoolProperty(name="To Move Upwards", default=True)

    @classmethod
    def poll(cls, context):
        #if context.area.type != 'VIEW_3D':
        #    return False
        
        #obj = context.active_object
        #return obj and obj.type == 'MESH' and obj.mode == 'EDIT'
        return True

    def invoke(self, context, event):
        result = split(context, event, True)
        if result:
            return {'FINISHED'}
        else:
            return {'CANCELED'}
        
    def execute(self, context):
        print("Testing")
        return {'FINISHED'}
    
    """
    def set_direction(up):
        if self.direction_up == up:
            return
        # can I call undo here?
        bpy.ops.ed.undo()
        self.direction_up = up
        bpy.ops.ed.undo_push()
        split(context, self.direction_up)
    """
        

def register():
    bpy.utils.register_class(VertexRipForFace)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_draw)


def unregister():
    bpy.utils.unregister_class(VertexRipForFace)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_draw)


if __name__ == "__main__":
    register()
