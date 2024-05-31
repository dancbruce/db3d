####Author: Dan C Bruce
####Email: dancbruce@gmail.com
####Date: 05/31/2024
####Software: Maya 2022.4
####Script: maya_copyAnim
####Version: 1.0
####Note: Copy animation from one rig to another.  First select the copy rig then the paste rig and run the script.

import maya.cmds as cmds

sel =  cmds.ls(selection=True)

if len(sel) == 2:
    anim_copy_name = cmds.listRelatives(sel[0], allDescendents=True, type='nurbsCurve')    
    anim_copy_path = cmds.listRelatives(sel[0], allDescendents=True, type='nurbsCurve', fullPath=True)
    anim_paste_name = cmds.listRelatives(sel[1], allDescendents=True,  type='nurbsCurve')    
    anim_paste_path = cmds.listRelatives(sel[1], allDescendents=True,  type='nurbsCurve', fullPath=True)
    if len(anim_copy_name) == len(anim_paste_name):
        for i in range(len(anim_paste_name)):
            trans_copy_name = cmds.listRelatives(anim_copy_path[i], parent=True)                                
            trans_copy_path = cmds.listRelatives(anim_copy_path[i], parent=True, fullPath=True)
            trans_paste_name = cmds.listRelatives(anim_paste_path[i], parent=True)
            trans_paste_path = cmds.listRelatives(anim_paste_path[i], parent=True, fullPath=True)
            if anim_copy_name[i].split(":")[-1] == anim_paste_name[i].split(":")[-1]:                      
                try:
                    cmds.copyKey(trans_copy_path, animation='objects', option='keys')
                    cmds.pasteKey(trans_paste_path, animation='objects', option='replaceCompletely')
                    print('Copied Animation : from '+trans_copy_name[0]+" to "+trans_paste_name[0])
                except:
                    attr_list =  cmds.listAttr(trans_copy_path[0], keyable=True)
                    if attr_list == None:
                        continue     
                    for attr in  attr_list:
                        copy_type = cmds.getAttr(trans_copy_path[0]+'.'+attr, type=True)
                        if copy_type not in ['doubleLinear', 'doubleAngle', 'double', 'enum']:
                            continue                      
                        if cmds.getAttr(trans_paste_path[0]+'.'+attr, settable=True):
                            cmds.setAttr(trans_paste_path[0]+'.'+attr, cmds.getAttr(trans_copy_path[0]+'.'+attr))
                    print('No Animation : '+trans_copy_name[0])
            else:
                print('Warning : '+trans_copy_name[0]+" does not match "+ trans_paste_name[0])
    else:
        cmds.warning('Copy rig does not match paste rig.')
else:
    cmds.warning('Select a rig to copy and a rig to paste.')