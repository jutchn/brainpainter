all:
	export PYTHONPATH="${PYTHONPATH}:E:/Users/spectR/Desktop/%Rutgers/RESEARCH/brainpainter"
	configFile=config.py "/mnt/c/Program Files/Blender Foundation/Blender/blender.exe" --background --python blendCreateSnapshot.py
	configFile=config.py "/mnt/c/Program Files/Blender Foundation/Blender/blender.exe" --background --python blendCreateSnapshot.py
	configFile=config.py "/mnt/c/Program Files/Blender Foundation/Blender/blender.exe" --background --python blendCreateSnapshot.py
	"/mnt/c/Program Files/Blender Foundation/Blender/blender.exe" --background --python imageMerge.py