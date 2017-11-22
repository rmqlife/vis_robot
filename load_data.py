#!/usr/bin/env python

"""Convert UnstructuredGrid in .vtk files to STL files."""

import os
import sys
import vtk
import numpy

def computeNormal(vss,iss):
    nss=numpy.zeros(vss.shape)
    for i in xrange(iss.shape[0]):
        a=vss[iss[i][0]]
        b=vss[iss[i][1]]
        c=vss[iss[i][2]]
        n=numpy.cross(numpy.subtract(b,a),numpy.subtract(c,a))
        n=numpy.divide(n,numpy.linalg.norm(n))
        nss[iss[i][0]]=numpy.add(n,nss[iss[i][0]])
        nss[iss[i][1]]=numpy.add(n,nss[iss[i][1]])
        nss[iss[i][2]]=numpy.add(n,nss[iss[i][2]])
    for i in xrange(vss.shape[0]):
        nss[i]=numpy.divide(nss[i],numpy.linalg.norm(nss[i]))
    return nss

def computeNormalHandle(vss,nss,pos):
    minDist=10000
    minId=-1
    for i in xrange(vss.shape[0]):
        dist=numpy.linalg.norm(numpy.subtract(pos,vss[i]))
        if dist < minDist:
            minDist=dist
            minId=i
    if minId >= 0:
        return nss[minId]
    else:
        return numpy.zeros((3))
    
if len(sys.argv) < 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print('Usage: vtk-unstructuredgrid-to-stl.py <input_folder>')
    sys.exit(1)

recreate=True
directory=sys.argv[1]
print directory
handles=numpy.load(directory+"/data.npz")['tt_handles']
normals=numpy.zeros(handles.shape)
for filename in os.listdir(directory):
    if filename.endswith(".vtk"):
        print filename
        filename_output=filename[0:-4]+".stl"
        print filename_output
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(directory+"/"+filename)

        surface_filter = vtk.vtkDataSetSurfaceFilter()
        surface_filter.SetInputConnection(reader.GetOutputPort())

        triangle_filter = vtk.vtkTriangleFilter()
        triangle_filter.SetInputConnection(surface_filter.GetOutputPort())
        
        #write stl
        if (not os.path.exists(directory+"/"+filename_output)) or recreate:
            writer = vtk.vtkSTLWriter()
            writer.SetFileName(directory+"/"+filename_output)
            writer.SetFileTypeToBinary()
            writer.SetInputConnection(triangle_filter.GetOutputPort())
            writer.Write()
            
        reader.Update()
        #read stl:v
        nrP=reader.GetOutput().GetNumberOfPoints()
        vss=numpy.zeros((nrP,3))
        for i in xrange(nrP):
            vss[i]=reader.GetOutput().GetPoint(i)
        #read stl:i
        cells=reader.GetOutput().GetCells()
        nrC=cells.GetNumberOfCells()
        iss=numpy.zeros((nrC,3))
        for i in xrange(nrC):
            cc=reader.GetOutput().GetCell(i)
            iss[i][0]=cc.GetPointId(0)
            iss[i][1]=cc.GetPointId(1)
            iss[i][2]=cc.GetPointId(2)
        #compute normal
        id=int(filename[0:-4])
        nss=computeNormal(vss,iss)
        if id >= 0 and id < normals.shape[0]:
            normals[id,0:3 ]=computeNormalHandle(vss,nss,handles[id,0:3 ])
            normals[id,3:6 ]=computeNormalHandle(vss,nss,handles[id,3:6 ])
            normals[id,6:9 ]=computeNormalHandle(vss,nss,handles[id,6:9 ])
            normals[id,9:12]=computeNormalHandle(vss,nss,handles[id,9:12])
        print("converting %s %ld!"%(filename,normals.shape[0]))
numpy.save(directory+"/normal.npz",normals)
