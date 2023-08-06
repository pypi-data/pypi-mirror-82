#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ipywidgets import HTML

# Fixed styles to avoid leaflet maps overlap sepal widgets
STYLES = """
<style>
.leaflet-pane {
    z-index : 6 !important;
}
.leaflet-top, .leaflet-bottom {
    z-index : 6 !important;
}
.v-toolbar {
    z-index: 7 !important;
}
</style>
"""

_ = display(HTML(STYLES))

COMPONENTS = {

    'PROGRESS_BAR':{
        'color':'indigo',
    }
}

ICON_TYPES = {
    # Used for folders
    '':{ 
        'color':'amber',
        'icon':'mdi-folder-outline'
    },
    '.csv':{
        'color':'green accent-4',
        'icon':'mdi-border-all'
    },
    '.txt':{
        'color':'green accent-4',
        'icon':'mdi-border-all'
    },
    '.tif':{
        'color':'deep-purple',
        'icon':'mdi-image-outline'
    },
    '.tiff':{
        'color':'deep-purple',
        'icon':'mdi-image-outline'
    },
    '.shp':{
        'color':'deep-purple',
        'icon':'mdi-vector-polyline'
    },
    'DEFAULT':{
        'color':'light-blue',
        'icon':'mdi-file-outline'
    },
    # Icon for parent folder
    'PARENT':{ 
        'color':'black',
        'icon':'mdi-folder-upload-outline'
    },

}
