#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from drive_functions import insert_file,insert_folder

import re
import unicodedata
import sys

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



def vis_answers(data,name,parent_id):

    folder_id = insert_folder(parent_id,'Visualizaciones')
    for cols in data.columns:         
        if len(data[cols].dropna()) > 0:
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
                    ax = data[cols].dropna().plot(kind='box')
                    quantile = data[cols].quantile(.95)
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
                fig = plt.figure()
                plt.subplots_adjust(top=0.85) # use a lower number to make more vertical space
                data[cols].value_counts().sort().plot(kind='bar')
                fig.canvas.mpl_connect('draw_event', on_draw)
                
                plt.title(cols)
                plt.tight_layout()
                plt.savefig('data_viz/'+figure_name)  
                insert_file(figure_name,' ',folder_id, 'data_viz/'+figure_name,mimetype='image/png') 
