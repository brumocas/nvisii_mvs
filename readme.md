# NVISII Multi-View Synthetiser 

![renders_example](https://i.imgur.com/O2BrQ2u.jpg)

This repo is the skeleton code used to generate different dataset, [RTMV](https://www.cs.umd.edu/~mmeshry/projects/rtmv/), [watch it move](https://nvlabs.github.io/watch-it-move/), [graspnerf](https://nerfgrasp.github.io/), etc.

## Installation 

From there do the following, 
```
pip install -r requirements.txt
``` 
This code base needs a special version of NViSII, which is  downloaded and installed by the previous step, but you can always download the wheel manually [here](https://www.dropbox.com/s/m85v7ts981xs090/nvisii-1.2.dev47%2Bgf122b5b.72-cp36-cp36m-manylinux2014_x86_64.whl?dl=0).
This updated NViSII mainly add support to render background as an alpha mask when exporting png files. 


# Rendering scenes

The RTMV datasets has 4 types of environment. These can be recreated by using the different configs, e.g., `configs/abc.md`,`configs/abo.md`,`configs/bricks.md`, and `configs/gscanned.md`. 
Please note that this repo does not have any downloadable content (like 3d assets), links a provided for you to download the data below. 
But we do provide some minimal content to run the following examples, these are in the same file format as the original content used. Please download the data, `sh download_sample_content.sh`. 

On top of the RTMV like dataset you can generate, we also offer a config to render a 360 view of a model. You are also welcome to generate your own config file as the scene config driven feel free to mix things up. 

## 360 view of an object or scene
```
python render.py --config configs/three_sixty_view.yaml
```


The script simply forces the renderer to create camera positions that are on a circle, you control the angle through these variables: 
```
# if you do not want a full circle please change that. 
camera_theta_range: [0,360]
# The middle of this interval is what is going to be render. 
camera_elevation_range: [40,90]
# This controls how far the camera is.
camera_fixed_distance_factor: 1
```
You can make a video from this output, [here is an example](https://imgur.com/u2GhoyK). 
```
ffmpeg -framerate 30 -pattern_type glob -i 'output/360_views/*.png' -c:v libx264 -pix_fmt yuv420p three_sixty.mp4
```

## Falling object scene

## Using hdri map





# Citation
If you use this code in your research please cite the following: 
```
@misc{morrical2021nvisii,
      title={NViSII: A Scriptable Tool for Photorealistic Image Generation}, 
      author={Nathan Morrical and Jonathan Tremblay and Yunzhi Lin and Stephen Tyree and Stan Birchfield and Valerio Pascucci and Ingo Wald},
      year={2021},
      eprint={2105.13962},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```