from abaqusGui import getAFXApp, Activator, AFXMode
from abaqusConstants import ALL
import os
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='Tools ME|Connection Builder', 
    object=Activator(os.path.join(thisDir, 'cB_v6DB.py')),
    kernelInitString='import CB_module',
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    applicableModules=['Assembly','Step','Interaction', 'Load'],
    version='1.0',
    author='Matthias Ernst, Dassault Systemes Germany',
    description='This Plug-In allows an easy creation of connections built of coupling+connector+coupling. '\
                'Supported only in CAE v2016 or higher. Selection of geometric surfaces is required. '\
                'Always confirm selection for each region with DONE button or middle mouse button before pressing Apply or OK. '\
                'Create a connector section first, otherwise a section is created on-the-fly.'\
                '\n\nThis is not an official Dassault Systemes product.',
    helpUrl='N/A'
)
