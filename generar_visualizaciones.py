#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib as mpl
from drive_functions import insert_file,insert_folder
import smopy
import re
import unicodedata
from shapely.geometry import Point
import sys

sns.set_style("white")
#sns.set(rc={'axes.facecolor':'white'})
# Turn interactive plotting off
plt.ioff()

def quitar_caracteres_especiales(cols):
    """
    cols_complete = data.columns
    data.columns = data.columns.map(lambda x: ''.join((c for c in unicodedata.normalize('NFD', unicode(x)) if unicodedata.category(c) != 'Mn')))
    data.columns = data.columns.map(lambda x: re.sub(r'[^a-zA-Z\d\s]', '', x))
    cols = data.columns
    data.columns = cols
    return cols_complete,data
    """
    # Removes accents
    cols = ''.join((c for c in unicodedata.normalize('NFD', unicode(cols)) if unicodedata.category(c) != 'Mn'))
    cols = re.sub(r'[^a-zA-Z\d\s]', '', cols)
    return cols

def on_draw(event):
    """Auto-wraps all text objects in a figure at draw-time"""
    
    fig = event.canvas.figure

    # Cycle through all arists in all the axes in the figure
    for ax in fig.axes:
        for artist in ax.get_children():
            # If it's a text artist, wrap it...
            if isinstance(artist, mpl.text.Text):
                autowrap_text(artist, event.renderer)

    # Temporarily disconnect any callbacks to the draw event...
    # (To avoid recursion)
    func_handles = fig.canvas.callbacks.callbacks[event.name]
    fig.canvas.callbacks.callbacks[event.name] = {}
    # Re-draw the figure..
    fig.canvas.draw()
    # Reset the draw event callbacks
    fig.canvas.callbacks.callbacks[event.name] = func_handles

def autowrap_text(textobj, renderer):
    """Wraps the given matplotlib text object so that it exceed the boundaries
    of the axis it is plotted in."""
    import textwrap
    # Get the starting position of the text in pixels...
    x0, y0 = textobj.get_transform().transform(textobj.get_position())
    # Get the extents of the current axis in pixels...
    clip = textobj.get_axes().get_window_extent()
    # Set the text to rotate about the left edge (doesn't make sense otherwise)
    textobj.set_rotation_mode('anchor')

    # Get the amount of space in the direction of rotation to the left and 
    # right of x0, y0 (left and right are relative to the rotation, as well)
    rotation = textobj.get_rotation()
    right_space = min_dist_inside((x0, y0), rotation, clip)
    left_space = min_dist_inside((x0, y0), rotation - 180, clip)

    # Use either the left or right distance depending on the horiz alignment.
    alignment = textobj.get_horizontalalignment()
    if alignment is 'left':
        new_width = right_space 
    elif alignment is 'right':
        new_width = left_space
    else:
        new_width = 2 * min(left_space, right_space)

    # Estimate the width of the new size in characters...
    aspect_ratio = 0.5 # This varies with the font!! 
    fontsize = textobj.get_size()
    pixels_per_char = aspect_ratio * renderer.points_to_pixels(fontsize)

    # If wrap_width is < 1, just make it 1 character
    wrap_width = max(1, new_width // pixels_per_char)
    try:
        wrapped_text = textwrap.fill(textobj.get_text(), wrap_width)
    except TypeError:
        # This appears to be a single word
        wrapped_text = textobj.get_text()
    textobj.set_text(wrapped_text)

def min_dist_inside(point, rotation, box):
    """Gets the space in a given direction from "point" to the boundaries of
    "box" (where box is an object with x0, y0, x1, & y1 attributes, point is a
    tuple of x,y, and rotation is the angle in degrees)"""
    from math import sin, cos, radians
    x0, y0 = point
    rotation = radians(rotation)
    distances = []
    threshold = 0.0001 
    if cos(rotation) > threshold: 
        # Intersects the right axis
        distances.append((box.x1 - x0) / cos(rotation))
    if cos(rotation) < -threshold: 
        # Intersects the left axis
        distances.append((box.x0 - x0) / cos(rotation))
    if sin(rotation) > threshold: 
        # Intersects the top axis
        distances.append((box.y1 - y0) / sin(rotation))
    if sin(rotation) < -threshold: 
        # Intersects the bottom axis
        distances.append((box.y0 - y0) / sin(rotation))
    return min(distances)



def vis_answers(df,parent_id,folder_name):

    folder_id = insert_folder(parent_id,folder_name)
    for cols in df.columns:         
        if len(df[cols].dropna()) > 0:
            cols_n = cols
    
            if len(cols_n):
                cols_n = cols_n[:150]
                
            figure_name = quitar_caracteres_especiales(cols_n)+'.png'
                
            if cols in [u'p12 Edad',u'Pendiente',u'Distancia',u'Emisiones']:
                """
                Plots that I want as boxes.
                """
                try:
                    fig = plt.figure()
                    plt.subplots_adjust(top=0.85) # use a lower number to make more vertical space
                    ax = df[cols].dropna().plot(kind='box')
                    quantile = df[cols].quantile(.95)
                    fig.canvas.mpl_connect('draw_event', on_draw)
                    plt.title(cols)
                    plt.tight_layout()
                    ax.set_ylim(0, (quantile))
                    plt.savefig('data_viz/'+figure_name)  
                    insert_file(figure_name,' ',folder_id, 'data_viz/'+figure_name,mimetype='image/png')        
                    plt.close(fig)
                    
                except TypeError:
                    print ("Unexpected error:"+str(sys.exc_info()[0]))
                    pass
                
            elif 'Dirección' in cols:
                """
                No need to plot this.
                """
                pass
    
            else:    
                """
                Otherwise try a bar plot.
                """
                try:    
                    fig = plt.figure()
                    plt.subplots_adjust(top=0.85) # use a lower number to make more vertical space
                    #df[cols].value_counts().sort_index().plot(kind='bar')
                    pd.value_counts(df[cols].values.flatten()).plot(kind='bar')
                    fig.canvas.mpl_connect('draw_event', on_draw)
                    
                    plt.title(cols)
                    plt.tight_layout()
                    plt.savefig('data_viz/'+figure_name)  
                    insert_file(figure_name,' ',folder_id, 'data_viz/'+figure_name,mimetype='image/png')                     
                except ValueError:
                    try:
                        fig = plt.figure()
                        plt.subplots_adjust(top=0.85) # use a lower number to make more vertical space
                        #df[cols].value_counts().sort_index().plot(kind='bar')
                        pd.value_counts(df[cols].values.flatten()).sort_index().plot(kind='bar')
                        fig.canvas.mpl_connect('draw_event', on_draw)
                        
                        plt.title(cols)
                        plt.tight_layout()
                        plt.savefig('data_viz/'+figure_name)  
                        insert_file(figure_name,' ',folder_id, 'data_viz/'+figure_name,mimetype='image/png') 
                        
                    except ValueError:
                        pass
    plot_map(df,folder_id,'')
    return folder_id

                
def crear_compendios(data,nombre_empresa,folder_id,viz_folder):
    """
    Crear sumarios de agrupaciones que tienen sentido.
    Guardar las tablas.
    Crear graficas.
    * folder_id = ID de carpeta donde se alojan los resumenes en cuestion.
    * data = data frame principal.
    * nombre_empresa.
    """    
    resumen_folder_id = insert_folder(folder_id,'Tablas')
    
    agg_1 = data.groupby([u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'])
    agg_1 = agg_1.mean().dropna(axis=1).apply(pd.to_numeric)
    agg_1.to_csv('Files/Modo_regreso.csv')
    resumen_folder_id_1 = insert_folder(resumen_folder_id, 'Modo de regreso')
    insert_file('Modo_regreso.csv', ' ', resumen_folder_id_1, 'Files/Modo_regreso.csv', mimetype='text/csv') 
    vis_compendios(agg_1, resumen_folder_id_1, 'Modo regreso. ')
    
    agg_2 = data.groupby([u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'])
    agg_2 = agg_2.mean().dropna(axis=1).apply(pd.to_numeric)
    agg_2.to_csv('Files/Modo_ida.csv')
    resumen_folder_id_2 = insert_folder(resumen_folder_id,'Modo de ida')
    insert_file('Modo_ida.csv', ' ', resumen_folder_id_2, 'Files/Modo_ida.csv', mimetype='text/csv') 
    vis_compendios(agg_2,resumen_folder_id_2,'Modo ida. ')
    
    agg_3 = data.groupby( [u'p22 5. \xbfEn qu\xe9 municipio vive?'])
    agg_3 = agg_3.mean().dropna(axis=1).apply(pd.to_numeric)
    agg_3.to_csv('Files/Municipio.csv')
    resumen_folder_id_3 = insert_folder(resumen_folder_id,'Municipio')
    insert_file('Municipio.csv',' ',resumen_folder_id_3, 'Files/Municipio.csv',mimetype='text/csv')     
    vis_compendios(agg_3,resumen_folder_id_3,'Municipio. ')

def vis_compendios(df,resumen_folder_id,aggregation_name):
    """
    Visualizar resumenes de diferentes "agregaciones".
    * DF: Subconjunto del cuerpo de datos [Pandas Data Frame].
    * resumen_folder: carpeta donde se guardan estos compendios [].
    * aggregation_name: agregación en concreto.
    """
    for cols in df:
        if len(cols):
            cols = cols[:150]
        figure_name = aggregation_name + str(quitar_caracteres_especiales(cols))+'.png'
        fig = plt.figure()
        plt.subplots_adjust(top=0.85) # use a lower number to make more vertical space
        df[cols].plot(kind='bar')
        fig.canvas.mpl_connect('draw_event', on_draw)
        
        plt.title(cols)
        plt.tight_layout()
        plt.savefig('data_viz/'+figure_name)  
        insert_file(figure_name, ' ', resumen_folder_id, 'data_viz/'+figure_name, mimetype='image/png') 
        
def plot_map(data,viz_folder,prefijo,columnas=[None]):
    """
    Outputs (and uploads to Google Drive) maps of locations of a given data frame and a 
    subset of columns.
    * Data: entire data frame or subset.
    * viz_folder: destination folder in Google Drive.
    * columnas: subset of columns to plot.
    * prefijo: importante para nomenclatura.
    """
    
    if columnas != [None]:
        columnas += [None]
        
    for columna in columnas:
        if columna == None:
            data_plot = data.dropna(subset=[['Longitude','Latitude']])
        else:
            data_plot = data.dropna(subset=[['Longitude','Latitude',columna]])
            
            
        # Different basemap options
        
        #smopy.TILE_SERVER = "http://tile.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png" 
        #smopy.TILE_SERVER = "http://tile.openstreetmap.org/{z}/{x}/{y}.png"
        #smopy.TILE_SERVER = "http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
        #smopy.TILE_SERVER = "https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png";
        smopy.TILE_SERVER = "https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png"            
            
        # Create basemap with Smopy using the geographical extent of our group
        map = smopy.Map(data_plot.Latitude.min(), data_plot.Longitude.max(), data_plot.Latitude.max(), data_plot.Longitude.min(),z=100);
        #map.show_ipython(); 
        x, y = map.to_pixels(data_plot.Latitude,data_plot.Longitude);
        ax = map.show_mpl(figsize=(40,40));
        if columna == None:
            ax.scatter(x,y,c='#006400',linewidth=0, s=3000)
        else:
            sr = (((data_plot[columna]-data_plot[columna].min())/data_plot[columna].max())*100).astype(int)
            ax.scatter(x,y,c=sr,cmap='Greens',linewidth=0, s=3000)
        #plt.show()
        if columna != None:
            viz_name = quitar_caracteres_especiales(str(columna))
        else:
            viz_name = 'Total' #temporal
        viz_name = prefijo+' '+viz_name+'.'
        plt.title(viz_name,fontsize=80)
        plt.tight_layout()
        plt.savefig('data_viz/'+viz_name+'.png',figsize=(40,40))
        #insert_file(viz_name,' ',viz_folder, 'data_viz/'+viz_name+'.png',mimetype='image/png') 
    
     
    
