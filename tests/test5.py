import os,sys
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(parent,"..","..")))

from Drawlib2.imageRenderer.ImageRenderer_Beta import ImageRenderer

_img = os.path.join(parent,"test2.png")
ImageRenderer(
    image=_img,
    rentype="box",
    mode="foreground",
    char=None,
    pc=False,
    method="lum",
    invert=False,
    monochrome=False,
    width=20,
    height=10,
    resampling="lanczos",
    asTexture=False,
    colorMode="pythonAnsi",
    textureCodec=None,
    delimitChars=False
)