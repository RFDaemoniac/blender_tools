import bpy
import bmesh
import mathutils


def menu_draw(self, context):
    self.layout.operator("mesh.move_keep_normals")

def main(context):
    '''
    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    selection = 

    uv_layer = bm.loops.layers.uv.verify()

    # adjust uv coordinates
    for face in bm.faces:
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            # use xy position of the vertex as a uv coordinate
            loop_uv.uv = loop.vert.co.xy

    bmesh.update_edit_mesh(me)
    '''
    # need to switch to object mode and back in order to update selection
    # edit mode works on a copy of the mesh that is inaccessible to python
    # this feels like a bug but is apparently just the way it works
    #mode = bpy.context.active_object.mode
    #bpy.ops.object.mode_set(mode='OBJECT')
   
    # back to previous mode
    #bpy.ops.object.mode_set(mode=mode)

"""
TODO:
Initially
    VectorProperty
    Mouse location
    Cast Ray at mouse_offset from vertex screen position
    closest face from ray is modified one
    Face Normal
    Split vertices/edges(/faces?)
    Vertex slide
    Combine vertices
        (also sort requires a split?)
        Pick direction for new edge, with smallest angle to modified face
    Update mesh display during modal
    Highlight chosen face during modal
    Lock in face choice during modal
Eventually
    Multiple Vertices
    Transform Orientation
    Cursor Location
    modes: 
        Move vertex to z=0 plane of cursor
        snap to edge intersections
    undo stack requirements?
"""


class VertexMoveKeepNormalsOperator(bpy.types.Operator):
    """Move a vertex along the direction of one face normal,
    while preserving the normals of the other faces"""
    bl_idname = "mesh.move_keep_normals"
    bl_label = "Move And Keep Face Normals"
    bl_options = {'REGISTER', 'UNDO'}
    
    # exposed properties
    
    
    # internal calculation properties
    # rmf todo: should these be properties?
    selected_verts: CollectionProperty(type=bmesh.types.BMVert)
    vertex_init_pos: FloatVectorProperty()
    mouse_init_x: IntProperty()
    mouse_init_y: IntProperty()
    mouse_x: IntProperty()
    mouse_y: IntProperty()
    locked_face: PointerProperty(type=bmesh.types.BMFace)
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT'
    
    def invoke(self, context, event):
        mesh = bmesh.from_edit_mesh(context.active_object.data)
        self.selected_verts = [v for v in mesh.verts if v.select]
        if not self.selected_verts:
            # todo: error message about requirements?
            return {'CANCELLED'}
        #mathutils.Vector((0.0,0.0,))
        # rmf todo: multiple vertices
        # for s_v in selected_verts:
        s_v = self.selected_verts[0]
        edge_count = len(s_v.link_edges)
        if edge_count < 3:
            return {'CANCELLED'}
        mouse_init_x = event.mouse_x
        mouse_init_y = event.mouse_y
        mouse_x = event.mouse_x
        mouse_y = event.mouse_y
        
        if any(v.select for v in context.active_object.data.vertices) ):
            
            self.first_mouse_x = event.mouse_x
            self.first_value = context.object.location.x

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active vertices, could not finish")
            return {'CANCELLED'}
            
    def modal(self, context, event):
        ''' not allowing navigation for now
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'LEFT_SHIFT', 'RIGHT_SHIFT'}:
            # allow navigation
            return {'PASS_THROUGH'}
        if event.shift and event.type == 'MOUSEMOVE':
            return {'PASS_THROUGH'}
        '''
        lock_face = False
        elif event.type == 'C':
            if self.locked_face:
                self.locked_face = None
            else:
                lock_face = True
            # show/hide face highlight, recalculate vertex position
        elif event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            context.object.location.x = self.first_value + delta * 0.01

        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.location.x = self.first_value
            return {'CANCELLED'}
        
        update_mesh(lock_face)

        return {'RUNNING_MODAL'}
    
    
    def update_mesh(lock_face):
        # for s_v in selected_verts:
        s_v = selected_verts[0]
        chosen_face = self.locked_face
        ray =
        if not chosen_face:
            for f in s_v.link_faces:
                f.median_center
        if lock_face:
            self.locked_face = chosen_face


    def execute(self, context):
        mesh = bmesh.from_edit_mesh(context.active_object.data)
        selected_verts = [v for v in mesh.verts if v.select]
        if not selected_verts:
            # todo: error message about requirements?
            return {'CANCELLED'}
        #mathutils.Vector((0.0,0.0,))
        # rmf todo: multiple vertices
        # for s_v in selected_verts:
        s_v = selected_verts[0]
        chosen_face = None
        
        for f in s_v.link_faces:
            f.median_center
        edge_count = len(s_v.linke_edges)
        if edge_count < 3:
            return {'CANCELLED'}
        elif edge_count == 3:
            # just perform a vertex slide here
        else:
            # need to split vertex
        for e in s_v.link_edges:
            
        for f in mesh.faces:
            for v in f.verts:
                
        
        
        bmesh.update_edit_mesh(mesh)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(UvOperator)


def unregister():
    bpy.utils.unregister_class(UvOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.vertex.move_keep_normals()
