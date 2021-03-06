# -*- coding:utf-8 -*-
'''
Created on 2016.06.01

@author: davidpower

修正 Reference 的材質球在流程末端無法更新的問題

https://knowledge.autodesk.com/search-result/caas/sfdcarticles/sfdcarticles/Updating-per-face-material-assignment-on-a-referenced-model-with-deformations.html
'''

import maya.cmds as cmds
import maya.mel as mel

def deformerAfterObjectSetMod():
    for i in cmds.ls(sl=1):
        shapes = cmds.listRelatives(i, s=1)
        referenceShapes =  [k for k in shapes if (cmds.referenceQuery(k,inr=1) and cmds.listConnections(k))]
        destShapes = [k for k in shapes if ( not cmds.referenceQuery(k,inr=1))]
        if referenceShapes:
            for destShape in destShapes:
                try:
                    mel.eval('deformerAfterObjectSetMod "%s" "%s";'%(referenceShapes[0],destShape))
                except Exception, e:
                    print e


def fixShaderConflix():
    for i in cmds.ls(sl=1):
        shapesMess = cmds.listRelatives(i, s= 1)
        shapesPure = cmds.listRelatives(i, s= 1, ni= 1)[0]
        shapesMess.remove(shapesPure)
        imObj = shapesMess[0]
        sg = cmds.listConnections(imObj, t= 'shadingEngine')[0]
        sgWrong = cmds.listConnections(shapesPure, t= 'shadingEngine', p= 1, c= 1)
        cmds.disconnectAttr(sgWrong[0], sgWrong[1])
        cmds.connectAttr(shapesPure + '.instObjGroups', sg + '.dagSetMembers', na= 1)




#deformerAfterObjectSetMod()
fixShaderConflix()
