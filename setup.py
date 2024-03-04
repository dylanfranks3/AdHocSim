from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A Python package to help simulate and visulaise Ad-Hoc networks'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="AdHocSim", 
        version=VERSION,
        author="Dylan Franks",
        author_email="dylan@dylanfranks.ney",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=['blinker==1.7.0','certifi==2024.2.2','charset-normalizer==3.3.2','click==8.1.7','click-default-group==1.2.4','cloup==2.1.2','Cython==3.0.8','decorator==5.1.1','glcontext==2.5.0','idna==3.6','isosurfaces==0.1.0','itsdangerous==2.1.2','Jinja2==3.1.3','manim==0.18.0','ManimPango==0.5.0','mapbox-earcut==1.0.1','markdown-it-py==3.0.0','MarkupSafe==2.1.5','mdurl==0.1.2','moderngl==5.10.0','moderngl-window==2.4.4','multipledispatch==1.0.0','networkx==3.2.1','numpy==1.26.3','pandas==2.2.0','Pillow==9.5.0','pyarrow==15.0.0','pycairo==1.25.1','pydub==0.25.1','pyglet==2.0.10','Pygments==2.17.2','pyobjc-core==10.1','pyobjc-framework-Cocoa==10.1','pyrr==0.10.3','python-dateutil==2.8.2','pytz==2024.1','requests==2.31.0','rich==13.7.0','scipy==1.12.0','screeninfo==0.8.1','setuptools==69.0.3','six==1.16.0','skia-pathops==0.8.0.post1','srt==3.5.3','svgelements==1.9.6','tqdm==4.66.1','typing_extensions==4.9.0','tzdata==2023.4','urllib3==2.2.0','watchdog==3.0.0','Werkzeug==3.0.1'],
        
        keywords=['python'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS" 

        ]
)