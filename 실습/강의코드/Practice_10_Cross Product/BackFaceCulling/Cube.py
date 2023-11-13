from Mesh3D import *
from MathOGL import *


class Cube(Mesh3D):
    def __init__(self, draw_type, back_face_cull = False):
        self.vertices = \
            [(0.5, -0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (0.5, 0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (0.5, -0.5, -0.5),
            (-0.5, -0.5, -0.5),
            (0.5, 0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (0.5, -0.5, -0.5),
            (0.5, -0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (-0.5, -0.5, -0.5),
            (-0.5, -0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (-0.5, 0.5, -0.5),
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (0.5, 0.5, -0.5),
            (0.5, 0.5, 0.5),
            (0.5, -0.5, 0.5)
            ]
        self.triangles = [0, 2, 3,
                          0, 3, 1, 
                          8, 4, 5, 
                          8, 5, 9, 
                          10, 6, 7, 
                          10, 7, 11, 
                          12,13, 14, 
                          12, 14, 15, 
                          16, 17, 18, 
                          16, 18, 19, 
                          20, 21, 22, 
                          20, 22, 23]
        self.uvs = [(0.0, 0.0),
                    (1.0, 0.0),
                    (0.0, 1.0),
                    (1.0, 1.0),
                    (0.0, 1.0),
                    (1.0, 1.0),
                    (0.0, 1.0),
                    (1.0, 1.0),
                    (0.0, 0.0),
                    (1.0, 0.0),
                    (0.0, 0.0),
                    (1.0, 0.0),
                    (0.0, 0.0),
                    (0.0, 1.0),
                    (1.0, 1.0),
                    (1.0, 0.0),
                    (0.0, 0.0),
                    (0.0, 1.0),
                    (1.0, 1.0),
                    (1.0, 0.0),
                    (0.0, 0.0),
                    (0.0, 1.0),
                    (1.0, 1.0),
                    (1.0, 0.0)]
        self.draw_type = draw_type
        self.back_face_cull = back_face_cull
        Mesh3D.draw_type = draw_type
        self.faceNormals = []
        
        for t in range(0, len(self.triangles), 3):
            p1 = self.vertices[self.triangles[t]]
            p2 = self.vertices[self.triangles[t+1]]
            p3 = self.vertices[self.triangles[t+2]]
            
            u = pygame.Vector3(p1[0] - p2[0],
                               p1[1] - p2[1],
                               p1[2] - p2[2])
            
            v = pygame.Vector3(p3[0] - p2[0],
                               p3[1] - p2[1],
                               p3[2] - p2[2])
            
            print(u)
            print(v)

            norm = cross_product(u,v)
            print(norm)
            self.faceNormals.append(norm)
        
    def draw(self, forward):
        for t in range(0, len(self.triangles), 3):
            glBegin(self.draw_type)
            if self.back_face_cull :
                if dot_product(self.faceNormals[t//3], forward) <= 0:
                    glTexCoord2fv(self.uvs[self.triangles[t]])
                    glVertex3fv(self.vertices[self.triangles[t]])
                    
                    glTexCoord2fv(self.uvs[self.triangles[t + 1]])
                    glVertex3fv(self.vertices[self.triangles[t + 1]])

                    glTexCoord2fv(self.uvs[self.triangles[t + 2]]) 
                    glVertex3fv(self.vertices[self.triangles[t + 2]])
            else:
                glTexCoord2fv(self.uvs[self.triangles[t]])
                glVertex3fv(self.vertices[self.triangles[t]])
                    
                glTexCoord2fv(self.uvs[self.triangles[t + 1]])
                glVertex3fv(self.vertices[self.triangles[t + 1]])

                glTexCoord2fv(self.uvs[self.triangles[t + 2]]) 
                glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()
            
            
            


