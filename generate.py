#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import os
import shutil
import re
from PIL import Image,ImageOps,ImageDraw,ImageFont
import subprocess
import math
import textwrap


# In[2]:


base_rom_game_path = "/home/pppstudio/RG35XX/SDCARD2/"
base_garlic_rom_path = "/home/pppstudio/RG35XX/ROMS/"

systems = [
    {
        "name":'GB',
    },
    {
        "name":'GBC',
    },
    {
        "name":'SFC',
    },
    {
        "name":'GBA',
    },

]

for i in systems:
    
    i['items'] = []
    
    path_list = {}

    exclude = set(['media'])
    for root, dirs, files in os.walk(base_rom_game_path+i["name"], topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            fullpath = os.path.join(root, file)
            split_tup = os.path.splitext(file)
            game_name = split_tup[0]
            ext = split_tup[1]

            if ext == '.dat':
                continue
            if ext == '.txt':
                continue

            if game_name == 'media':
                continue

            rom_data = {
                "path":fullpath,
                "label":game_name,
                "ext":ext
            }
            i['items'].append(rom_data)

    i['items'].sort(key=lambda element: element['path'])
  


# In[3]:


for s in systems:
    dst_thumbnail = base_garlic_rom_path+'CFW/skin/games/'+s['name']+'/'
    system = s['name']+'/'

    isExist = os.path.exists(dst_thumbnail)
    if not isExist:
        os.makedirs(dst_thumbnail)
    
    dst_cache = base_rom_game_path+system+'media/cache'
    
    isExist = os.path.exists(dst_cache)
    if not isExist:
        os.makedirs(dst_cache)
    
    position = 0
    page = 0
    current_position = 0
    row = 8
    col = 6
    
    for i in range(len(s['items'])):
        current_game_name = game_name = s['items'][i]['label']
        split_tup = os.path.splitext(s['items'][i]['path'])    
        file_extension = split_tup[1]
        cache_path = dst_thumbnail+game_name+file_extension+".png"
        

        png_file_exists = False
        
        art_path = base_rom_game_path+system + "media/box2dfront/"+game_name+".png"
        snap_path = base_rom_game_path+system + "media/screenshot/"+game_name+".png"
        title_path = base_rom_game_path+system + "media/screenshottitle/"+game_name+".png"

        if os.path.exists(cache_path):
            png_file = cache_path
            png_file_exists = True
            
        else:
            new_im = Image.new('RGB', (640, 480))
            found_file = os.path.exists(art_path) or os.path.exists(snap_path) or os.path.exists(title_path)
            if found_file:
                ss_w = 210
                ss_h = 180
                offset = 210
                try:   
                    if(os.path.exists(title_path)):
                        title = Image.open(title_path)
                        title = ImageOps.contain(title,(ss_w,ss_h))
                        offset = title.size[0] + 20
                        new_im.paste(title, (10,50))
                except Exception:
                    pass
                                     
                try:        
                    
                    if(os.path.exists(snap_path)):
                        snap = Image.open(snap_path)
                        snap = ImageOps.contain(snap,(ss_w,ss_h))
                        offset = snap.size[0] + 20
                        new_im.paste(snap, (10,50+min(ss_h,title.size[1])+10))
                except Exception:
                    pass
          
            space = 4
            start_x = 240
            start_y = space+50
            x=start_x
            y=start_y
            
           
            ss_w = math.floor((640-start_x - space * (col-0))/col)
            ss_h = math.floor((480-start_y - space * (row-0))/row)
            last_size = [ss_w,ss_h]
            
            drw = ImageDraw.Draw(new_im, 'RGB')
            
            for j in range(page*row*col,min(len(s['items']),(page+1)*row*col)):    
               
                game_name = s['items'][j]['label']
                split_tup = os.path.splitext(s['items'][j]['path'])
                file_extension = split_tup[1]
                art_path = base_rom_game_path+system + "media/box2dfront/"+game_name+".png"
                snap_path = base_rom_game_path+system + "media/screenshot/"+game_name+".png"
                title_path = base_rom_game_path+system + "media/screenshottitle/"+game_name+".png"
            
            
            
                found_file = False
                
                if os.path.exists(title_path):
                    thumbnail_image = title_path
                    found_file = True
                elif os.path.exists(snap_path):
                    thumbnail_image = snap_path
                    found_file = True
                elif os.path.exists(art_path):
                    thumbnail_image = art_path
                    found_file = True
                
                
                if found_file:
                    try:   
                        if(os.path.exists(thumbnail_image)):
                            title = Image.open(thumbnail_image)
                            title = ImageOps.contain(title,(ss_w,ss_h))
                            if j == current_position:
                                new_im.paste( (255,0,0), [x-space,y-space,x+title.size[0]+space,y+title.size[1]+space])
                            last_size = title.size
                            
                            new_im.paste(title, (x,y))
                    except Exception:
                        pass
                else:
                    if j == current_position:
                        new_im.paste( (255,0,0), [x-space,y-space,x+last_size[0]+space,y+last_size[1]+space])
                    new_im.paste( (0,0,0), [x,y,x+last_size[0],y+last_size[1]])
                    
                    font = ImageFont.truetype(base_garlic_rom_path +"CFW/skin/font.ttf",12)
                    text_offset=0
                    for line in textwrap.wrap(game_name,width=10):
                        drw.text((x+space,y+space+text_offset),line,font=font,align="left")
                        text_offset+=12+1
                        if text_offset+12 > last_size[1]:
                            break
                    
                    
                y+=ss_h+space

                if(y > 480 - ss_h - space):
                    x+=ss_w+space
                    y=start_y

                    
            
            font = ImageFont.truetype(base_garlic_rom_path +"CFW/skin/font.ttf",32)
            text = current_game_name
            drw.text((110,4),text,font=font,align="left")
            
            font = ImageFont.truetype(base_garlic_rom_path +"CFW/skin/font.ttf",12)
            drw.text((4,464),str(current_position+1)+" / "+str(len(s['items'])),font=font,align="left")
            del drw        
                    
            print('Generate thumbnail '+cache_path)
            new_im.save(cache_path)
            
            png_file = cache_path
            png_file_exists = True

            
        position += 1
        current_position += 1
        if position>=row*col:
            page += 1
            position=0
           
  


# In[4]:


"""

SDCARD2

rsync -av --ignore-existing --exclude=PS --exclude=media --exclude=Saves /home/pppstudio/RG35XX/SDCARD2/ /media/pppstudio/ROMS/
rsync -av --ignore-existing --exclude=PS --exclude=media --exclude=Saves /media/pppstudio/ROMS/ /home/pppstudio/RG35XX/SDCARD2/



SDCARD1

rsync -avc --exclude=Saves /home/pppstudio/RG35XX/ROMS/CFW/skin/games/GB/ /media/pppstudio/06D0-83C0/CFW/skin/games/GB/
rsync -avc --exclude=Saves /home/pppstudio/RG35XX/ROMS/CFW/skin/games/GBC/ /media/pppstudio/06D0-83C0/CFW/skin/games/GBC/
rsync -avc --exclude=Saves /home/pppstudio/RG35XX/ROMS/CFW/skin/games/GBA/ /media/pppstudio/06D0-83C0/CFW/skin/games/GBA/
rsync -avc --exclude=Saves /home/pppstudio/RG35XX/ROMS/CFW/skin/games/SFC/ /media/pppstudio/06D0-83C0/CFW/skin/games/SFC/


"""





# In[ ]:




