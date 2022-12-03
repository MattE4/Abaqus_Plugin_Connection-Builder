from abaqus import *
from abaqusConstants import *
import regionToolset
#import time

def CB_function(
kw_name=None,
kw_faces_A=None,
kw_coupling_A=None,
kw_setregion_A=None,
kw_faces_B=None,
kw_coupling_B=None,
kw_setregion_B=None,
kw_rb_section=None,
kw_pd_reuse_section=None,
kw_pd_new_section=None,
kw_create_wireset=None):


    #print '\n\n----control output----'
    #print kw_name
    #print kw_faces_A
    #print kw_coupling_A
    #print kw_setregion_A
    #print kw_faces_B
    #print kw_coupling_B
    #print kw_setregion_B
    #print kw_rb_section
    #print kw_pd_reuse_section
    #print kw_pd_new_section
    #print kw_create_wireset
    #print '---------------------------\n\n'

################################################################################################################
## initial settings

    vpName = session.currentViewportName
    modelName = session.sessionState[vpName]['modelName']
    
    ass = mdb.models[modelName].rootAssembly
    r1 = ass.referencePoints
    
##########################################################################################
    # check if selection is valid
   
    if kw_faces_A == None or kw_faces_B == None:
        #print '\nError: Select face(s) for both regions and confirm each selection before pressing Apply or OK'
        getWarningReply(message='Select face(s) for both regions and confirm each selection before pressing Apply or OK!', buttons=(CANCEL,))
        return

#########################################################################
## Check existing names and define new one
    
    if kw_name[-1] <> '-':
        kw_name = kw_name + '-'    
    
    featurenames = ass.features.keys()
    
    i = 0
    x = 0
    while x==0:
        x = 1
        i = i+1
        currname = kw_name+str(i)
        for name in featurenames:
            if name.find(currname)<>-1:
                x = 0
    
    cntnname = currname    
    
####################################################################
## Region A

    facetuple = kw_faces_A
    rpname_a = cntnname+'_RP-A'
    coupname_a = cntnname+'_Coup-A'
    
    facetemp = ass.instances[facetuple[0].instanceName].faces[0:0]
    for x in facetuple:
        i = x.index
        j = x.instanceName
        facetemp = facetemp + ass.instances[j].faces[i:i+1]
    
    faceregion = regionToolset.Region(faces=facetemp,)
    massprop = ass.getMassProperties(regions=faceregion, relativeAccuracy=MEDIUM, miAboutCenterOfMass=False)
    center = massprop['areaCentroid']
    
    
    rp = ass.ReferencePoint(point=center)
    ass.features.changeKey(fromName=rp.name, toName=rpname_a)
    
    
    rp_a = r1[rp.id]
    refPoints1=(r1[rp.id], )
    
    if kw_setregion_A == True:
        ass.Set(referencePoints=refPoints1, name=rpname_a)
        region1=ass.sets[rpname_a]
        ass.Surface(side1Faces=facetemp, name=cntnname+'_Surf-A')
        region2=ass.surfaces[cntnname+'_Surf-A']
        
    else:    
        region1=regionToolset.Region(referencePoints=refPoints1)
        region2=regionToolset.Region(side1Faces=facetemp)
    
    if kw_coupling_A == 'Distributing':
    
        mdb.models[modelName].Coupling(name=coupname_a, controlPoint=region1, 
            surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=DISTRIBUTING, 
            weightingMethod=UNIFORM, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
            ur2=ON, ur3=ON)

    else:
    
        mdb.models[modelName].Coupling(name=coupname_a, controlPoint=region1,
            surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
            localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

####################################################################
## Region B

    facetuple = kw_faces_B
    rpname_b = cntnname+'_RP-B'
    coupname_b = cntnname+'_Coup-B'
    
    facetemp = ass.instances[facetuple[0].instanceName].faces[0:0]
    for x in facetuple:
        i = x.index
        j = x.instanceName
        facetemp = facetemp + ass.instances[j].faces[i:i+1]
    
    faceregion = regionToolset.Region(faces=facetemp,)
    massprop = ass.getMassProperties(regions=faceregion, relativeAccuracy=MEDIUM, miAboutCenterOfMass=False)
    center = massprop['areaCentroid']
    
    
    rp = ass.ReferencePoint(point=center)
    ass.features.changeKey(fromName=rp.name, 
    toName=rpname_b)
    
    rp_b = r1[rp.id]
    refPoints1=(r1[rp.id], )
    
    
    if kw_setregion_B == True:
        ass.Set(referencePoints=refPoints1, name=rpname_b)
        region1=ass.sets[rpname_b]
        ass.Surface(side1Faces=facetemp, name=cntnname+'_Surf-B')
        region2=ass.surfaces[cntnname+'_Surf-B']    
    
    else:
        region1=regionToolset.Region(referencePoints=refPoints1)
        region2=regionToolset.Region(side1Faces=facetemp)
    
    if kw_coupling_B == 'Distributing':
   
        mdb.models[modelName].Coupling(name=coupname_b, controlPoint=region1, 
            surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=DISTRIBUTING, 
            weightingMethod=UNIFORM, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
            ur2=ON, ur3=ON)
    else:
    
        mdb.models[modelName].Coupling(name=coupname_b, controlPoint=region1,
            surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
            localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

###############################################################################
## Create CSYS

    dtm1 = ass.DatumCsysByThreePoints(origin=rp_a, point1=rp_b, 
        coordSysType=CARTESIAN)
    dtmid1 = ass.datums[dtm1.id]
    
    ass.features.changeKey(fromName=dtm1.name, 
        toName=cntnname+'_CSYS')
    
## Create Wire and Wireset    
    
    wire = ass.WirePolyLine(points=((rp_a, rp_b), ), mergeType=IMPRINT, 
        meshable=False)
    
    ass.features.changeKey(fromName=wire.name, 
        toName=cntnname+'_Wire')
    

##################################################################################
## Check Connector Section

    if (kw_rb_section=='Create new connector section') or (kw_pd_reuse_section=='None. Create new is used'):
        
        if kw_pd_new_section<>'Axial':
            a = kw_pd_new_section.upper()
            secconstante = SymbolicConstant(a)
            secname = kw_pd_new_section+'-ConnSection'
            mdb.models[modelName].ConnectorSection(name=secname, 
                assembledType=secconstante)

        elif kw_pd_new_section=='Axial':
            secname = 'Axial-ConnSection'
            mdb.models[modelName].ConnectorSection(name=secname, 
                translationalType=AXIAL)
    else:
        secname = kw_pd_reuse_section

    
## Assign Connector Section   
    
    for x in ass.edges:
        if x.featureName == cntnname+'_Wire':
            i = x.index
    
    if kw_create_wireset == True:
        ass.Set(edges=ass.edges[i:i+1], name=cntnname+'_Set-Wire')
        region = ass.sets[cntnname+'_Set-Wire']
    
    else:
        edges1 = ass.edges[i:i+1]
        region = regionToolset.Region(edges=edges1)

    
    csa = ass.SectionAssignment(sectionName=secname, region=region)
    ass.ConnectorOrientation(region=csa.getSet(), localCsys1=dtmid1)

    ass.regenerate()
