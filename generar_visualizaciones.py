#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from drive_functions import insert_file,insert_folder,check_duplicate_files

def on_draw(event):
    """Auto-wraps all text objects in a figure at draw-time"""
    
    fig = event.canvas.figure

    # Cycle through all artists in all the axes in the figure
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
    
    n = len(data)
    cnt = 1
    for cols in data.columns:
        
        if 'Dirección' in cols:
            # Select all addresses and all the selected work locations, and just map them
            print("Direccion")
            
        elif 'Pendiente' in cols or 'Distancia' in cols:
                fig = plt.figure()
                plt.subplots_adjust(top=0.85) # use a lower number to make more vertical space
                data[cols].plot(kind='box')
                fig.canvas.mpl_connect('draw_event', on_draw)
                plt.title(cols)
                plt.savefig('data_viz/'+str(cnt)+'.png')  
                insert_file(str(cnt)+'.png',' ',folder_id, 'data_viz/'+str(cnt)+'.png',mimetype='image/png') 
                cnt +=1           
        else:
        
            try:
                fig = plt.figure()
                plt.subplots_adjust(top=0.85) # use a lower number to make more vertical space
                data[cols].value_counts().plot(kind='bar')
                fig.canvas.mpl_connect('draw_event', on_draw)
                plt.title(cols)
                plt.savefig('data_viz/'+str(cnt)+'.png')  
                insert_file(str(cnt)+'.png',' ',folder_id, 'data_viz/'+str(cnt)+'.png',mimetype='image/png') 
                cnt +=1 
            except TypeError:
                try: 
                    #plt.figure()
                    fig = plt.figure()
                    plt.subplots_adjust(top=0.85) # use a lower number to make more vertical space
                    data[cols].value_counts().plot(kind='bar')
                    fig.canvas.mpl_connect('draw_event', on_draw)
                    plt.title(cols)
                    plt.savefig('data_viz/'+str(cnt)+'.png')
                    insert_file(str(cnt)+'.png',' ',folder_id, 'data_viz/'+str(cnt)+'.png',mimetype='image/png') 
                    cnt +=1
                except TypeError:
                    # FUCK THIS CASE.
                    if type(data[cols][n-1])==dict:
                        new = True
                        try:
                            for it in data[cols]:
                                try:
                                    dc = dict([a, int(x)] for a, x in it.iteritems())
                                    df = pd.DataFrame([]).from_dict(dc,orient='index')
                                    if new:
                                        D = df
                                    else:
                                        D = D + df
                                        new = False
                                    fig = plt.figure()
                                    plt.subplots_adjust(top=0.85)
                                    D.plot(kind='bar')
                                    fig.canvas.mpl_connect('draw_event', on_draw)
                                    plt.title(cols)
                                    plt.savefig('data_viz/'+str(cnt)+'.png')
                                    insert_file(str(cnt)+'.png',' ',folder_id, 'data_viz/'+str(cnt)+'.png',mimetype='image/png') 
                                    cnt +=1
                                except AttributeError:
                                    pass
                                
                        except ValueError:
                            df = pd.DataFrame([])
                            bl = False
                            for it in data[cols]:
                                try: 
                                    df = df.append(it,ignore_index=True)
                                    bl = True
                                except TypeError:
                                    pass
                            if bl:
                                for cl in df:
                                    new = False
                                    fig = plt.figure()
                                    plt.subplots_adjust(top=0.85)
                                    df[cl].value_counts().plot(kind='bar')
                                    fig.canvas.mpl_connect('draw_event', on_draw)
                                    plt.title(cols)
                                    plt.savefig('data_viz/'+str(cnt)+'.png')
                                    insert_file(str(cnt)+'.png',' ',folder_id, 'data_viz/'+str(cnt)+'.png',mimetype='image/png') 
                                    cnt +=1
                    
                        #print(str(cols))
                        
    #                D = {k:v/n for k,v in D.iteritems()}
