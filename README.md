# Tetracamthon

## Introduction

This is a revers engineering project, generating cam profiles for Tetra Pak's 
[A3 Flex/CompactFlex](https://www.tetrapak.com/packaging/tetra-pak-a3-compactflex) aseptic filling machine.

## Data

The original chart is from a ppt which engineers in Tetra Pak released on 2010
 for a [conference](https://www.mscsoftware.com/sites/default/files/metodi-strumenti-calcolo-prototipaz.pdf).

![](https://tva1.sinaimg.cn/large/006tNbRwly1g9jhmty4rhj311i0u07wj.jpg)

## Result

Curves for different type of packages can be 
derived with the python scripts in [models](models). 

[Here](temp_png/plot_of_Cam_Curves_for_TPA_330sq_with_knots.png) is the cam profile for TPA 330 SQ on A3 Compact Flex machine.

![](https://tva1.sinaimg.cn/large/006tNbRwly1g9ji1vg98dj31c10u0b16.jpg)

[Here](plot/plot_of_Cam_Curves_for_TBA1000sq.png) is the cam profile for TBA 1000 SQ on A3 Flex machine.

![](https://tva1.sinaimg.cn/large/006tNbRwly1g9ji6kzml7j31c00u0qv6.jpg)

## Roadmap

- Inform the industry that this project have been released publicly.
- Fetch the opportunity to check and run on real machines.
- Write a tutorial on how to run these scripts to generate other curves.
- Refactor the codes aiming at the API for customized parameter script.
- Abstract the algorithm as backend of a cam design add-on for FreeCAD.
- Gather more applications of various conditions with high-speed cams.

## Explanation

Tetracamthon - four(**tetra**) coupling **cam**s mechanisms 
with Py**thon** and FreeCAD.

---
by John Qu at 2019-12-03
