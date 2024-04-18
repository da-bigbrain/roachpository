from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, MovieTexture, CardMaker, WindowProperties, FrameBufferProperties, GeomVertexWriter, GeomVertexReader
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
import math
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task
from math import pi, sin, cos


class run(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0,0,0)
        self.roach = self.loader.loadModel("model/roach.bam")
        self.roach.reparentTo(self.render)
        self.roach.setScale(5)
        self.roach.setHpr(90,45,0)
        self.roach.setPos(0,0,3)
        self.disableMouse()
        self.cam.setPos(0, -10, 0)
        self.cam.lookAt(0, 0, 0)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        update_task = self.taskMgr.add(self.update_task, "update_task")


    def spinCameraTask(self, task):
        angleDegrees = task.time * 60.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
       
    def update_task(self, task):
        self.modify_vertices(self.roach, amt=task.time)
        return Task.cont
    
    def modify_vertices(self, model, amt=1):
        # Assuming the model has only one GeomNode
        geomNode = model.find("**/+GeomNode").node()
        geom = geomNode.modifyGeom(0)  # Get the first Geom
        vdata = geom.modifyVertexData()

        # Create a vertex reader and writer for the "vertex" column
        vertex_reader = GeomVertexReader(vdata, 'vertex')
        vertex_writer = GeomVertexWriter(vdata, 'vertex')

        # Iterate over each vertex
        while not vertex_reader.isAtEnd():
            v = vertex_reader.getData3f()  # Read the current vertex position
            print(v[2])
            new_v = (v[0], v[1], v[2] + sin(amt * 3) / 80)  # Modify the vertex position
            vertex_writer.setData3f(new_v)  # Write the new position back


        

if __name__ == "__main__":
    app = run()
    app.run()