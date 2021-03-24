import os
import numpy as np
import PIL
from PIL import Image, ImageDraw, ImageFont
import sys

blendFullPath = os.path.abspath('.')
os.chdir(blendFullPath)
sys.path.append(blendFullPath)
from config import OUTPUT_FOLDER

os.chdir(OUTPUT_FOLDER)

#merge left regions horizontally
#list_im_left = ['cortical-inner_left_area.png', 'cortical-inner_left_grayvol.png', 'cortical-inner_left_thck.png',\
#    'cortical-outer_left_area.png', 'cortical-outer_left_grayvol.png', 'cortical-outer_left_thck.png',\
#    'subcortical_left_area.png']
list_im_left = [ 'cortical-inner_left_thck.png', 'cortical-outer_left_thck.png', 'cortical-inner_left_area.png',\
    'cortical-outer_left_area.png','cortical-inner_left_grayvol.png', 'cortical-outer_left_grayvol.png',\
    'subcortical_left_area.png']

ind_size = Image.open(list_im_left[1]).size

imgs_left = [ PIL.Image.open(i) for i in list_im_left ]

min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs_left])[0][1]
imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs_left ) )

imgs_comb = PIL.Image.fromarray( imgs_comb)
imgs_comb.save( 'left.png' )

#merge right regions horizontally
#list_im_right = ['cortical-inner_right_area.png', 'cortical-inner_right_grayvol.png', 'cortical-inner_right_thck.png',\
#    'cortical-outer_right_area.png', 'cortical-outer_right_grayvol.png', 'cortical-outer_right_thck.png',\
#    'subcortical_right_area.png']
list_im_right = ['cortical-inner_right_thck.png', 'cortical-outer_right_thck.png', 'cortical-inner_right_area.png',\
    'cortical-outer_right_area.png', 'cortical-inner_right_grayvol.png', 'cortical-outer_right_grayvol.png',\
    'subcortical_right_area.png']

imgs_right = [ PIL.Image.open(i) for i in list_im_right ]

min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs_right])[0][1]
imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs_right ) )

imgs_comb = PIL.Image.fromarray( imgs_comb)
imgs_comb.save( 'right.png' )

#merge left and right vertically
left = Image.open('left.png')
right = Image.open('right.png')

left_size = left.size
right_size = right.size

new_im = Image.new('RGB', (left_size[0],right_size[1] + left_size[1]+200), (255,255,255))
new_im.paste(left,(0,100))
new_im.paste(right,(0,left_size[1] + 200))

new_im.save('merge.png')


#add captions
img = Image.open('merge.png')
draw = ImageDraw.Draw(img,'RGB')
font = ImageFont.truetype("arial.ttf", 50)

left_names = ['Thickness', 'Area', 'Gray Matter Volume', 'Subcortical Volume']
for i in range(3):
    draw.text(((int)(ind_size[0] - 30 + i*1.93*ind_size[0]),75), left_names[i], (0, 0, 0),font=font)
draw.text(((int)(ind_size[0] * 6.26),75), left_names[3], (0, 0, 0),font=font)
    #print(left_names[i])
    #print(ind_size[0]/2 + i*ind_size[0])
    #print(left_size[1])

#right_names = ['area', 'right cortical-outer area', 'right cortical-inner thickness',\
#    'right cortical-outer thickness', 'right cortical-inner gray matter volume', 'right cortical-outer gray matter volume',\
#    'right subcortical volume']
#for i in range(7):
#    draw.text(((int)(ind_size[0]/2 + i*ind_size[0]-240),left_size[1]+175), right_names[i], (0, 0, 0),font=font)

img.save('merge.png')

#list_im = ['left.png','right.png']
#imgs    = [ PIL.Image.open(i) for i in list_im ]

#min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
#imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

#imgs_comb = PIL.Image.fromarray( imgs_comb)
#imgs_comb.save( 'merge.png' )


#merge cold and warm color scale horizontally
if os.path.exists("cold.png") and os.path.exists("warm.png"):
    cold = Image.open('cold.png')
    warm = Image.open('warm.png')

    cold_size = cold.size
    warm_size = warm.size
    if cold_size[0] < cold_size[1]:
        cold = cold.transpose(Image.ROTATE_270)
        cold_size = cold.size
    if warm_size[0] < warm_size[1]:
        warm = warm.transpose(Image.ROTATE_270)
        warm_size = warm.size
        
    new_im = Image.new('RGBA', (warm_size[0] + cold_size[0], cold_size[1]), (255,255,255,0))
    new_im.paste(cold, (0,0))
    new_im.paste(warm, (cold_size[0],0))

    new_im.save('cold_warm.png')
    scale = Image.open('cold_warm.png')  
elif os.path.exists("warm.png"):
    scale = Image.open('warm.png')
    if scale.size[0] < scale.size[1]:
        scale = scale.transpose(Image.ROTATE_270)
else:
    raise ValueError('Missing color scale in output folder')


#list_im_colorscale = ['cold3.png','warm3.png']
#imgs_color = [ PIL.Image.open(i) for i in list_im_colorscale ]

#min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs_color])[0][1]
#imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs_color ) )

#imgs_comb = PIL.Image.fromarray( imgs_comb)
#imgs_comb.save( 'coldwarm.png' )


#merge brain regions and color scale vertically
merge = Image.open( 'merge.png' )


maxsize = (2800, 600)
merge.thumbnail(maxsize, PIL.Image.ANTIALIAS)

merge_size = merge.size
scale_size = scale.size
#print(merge_size)
#print(" size ")
#print(scale_size)

new_im_final = Image.new('RGB', (merge_size[0],merge_size[1] + scale_size[1]), (255,255,255))
new_im_final.paste(merge,(0,0))
new_im_final.paste(scale, ((int)((merge_size[0]/2) - (scale_size[0]/2)), merge_size[1]))

new_im_final.save('final.png')

#add border
final = Image.open( 'final.png' )
new_im = Image.new('RGB', (merge_size[0] + 100 , merge_size[1] + scale_size[1]), (255,255,255))

new_im.paste(final, (50,0))

draw = ImageDraw.Draw(new_im,'RGB')
font = ImageFont.truetype("arial.ttf", 16)
left = ['Left']
right = ['Right']
draw.text((10,180), left[0], (0, 0, 0),font=font)

draw.text((10,480), right[0], (0, 0, 0),font=font)

new_im.save('final.png')
os.remove('left.png')
os.remove('right.png')
os.remove('merge.png')


#list_im_final = ['merge.png','cold_warm.png']
#imgs    = [ PIL.Image.open(i) for i in list_im ]

#min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
#imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

#imgs_comb = PIL.Image.fromarray( imgs_comb)
#imgs_comb.save( 'final.png' )


