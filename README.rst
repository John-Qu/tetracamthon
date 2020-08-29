Tetracamthon
============

Project Name
------------

This is a revers engineering project, generating virtual cam profiles
for Tetra Pak's `A3
Flex/CompactFlex <https://www.tetrapak.com/packaging/tetra-pak-a3-compactflex>`__
aseptic filling machine.

Tetracamthon covers three parts: "tetra", "cam", and "(py)thon",
respecting to industry machine, engineering knowledge, and algorithms
tool.

-  "Tetra" indicates Tetra Pak company, and "tetra" means four - four
   side package of milk as its first product.
-  "Cam" is lowercase, meaning mechanical cam that controlling follers
   position, not "CAM" abrevated for computer-aided manufacture.
-  "(Py)thon" points to its family, particularly to sympy and numpy.

Personal Motivation
-------------------

I have been studying and copying Tetra Pak's filling machines for five
years since graduate school in Shanghai Jiaotong University. When I left
Presise Pak in 2012, I have built the models of jaw and drive systems of
Tetra Pak's A3 Flex filling machine, but I failed to calculate its cam
profiles to generate actions for these models. I had been using scilab,
MSC Adams and Solidworks (both without license). Precise was providing
seventy sets of TBA 19 filling machine that year. We have some
experience and the mechanical cam profile of some type of packages. I
was making progress, but I had to leave. Because I must return to
Shanghai to live with my new wife, and because my project is not
supported officially by boss who is struggling with the co-inventing a
different flex filling machine with Shanghai Jiaotong University.

Early this year, I picked up this project and deside to step forward
from here. The motivations are as follows:

1. I need to prove to myself and campanies that I am an engineer of
   level five as in the definition of Prof. Wu Jun. I will solve a
   problem which is valuable to market and technicle community.
2. I want to connect the dots in my life and put a comma to this tunnel
   of life. I have been studying programming with python and translating
   documents of FreeCAD, which means nothing if I have no product.
3. I will go through this entrance to a new world, which might be
   engineering software add-ons, or technical documentation. I cannot
   wait or think. I must participate and build.
4. I feel like the process of digging in this problem. I had been
   thinking on it for half a year without official permission at
   Precise. I have been studying it for another seven months last year.
   I sat still for minutes to think about algorithms and spoke proudly
   to my wife any tiny progress made everyday.

Data and Result
---------------

Objective Chart
~~~~~~~~~~~~~~~

The reference data is derived from MSC Adams 2010 Euro User conference
`showslides <https://www.mscsoftware.com/sites/default/files/metodi-strumenti-calcolo-prototipaz.pdf>`__.
In page 56, Tetra Pak released A3/Flex york and jaw acceleration curves,
as shown below.

.. figure:: ../../static/images/README/006tNbRwgy1gap1ec6d1sj314x0u0h45.jpg
   :alt:

.. figure:: https://tva1.sinaimg.cn/large/006tNbRwgy1g9lt1h7fg2j31960u017z.jpg
   :alt:

Curves of velocity and position can be integrated from the above
acceleration chart. Here is the rough diagram of p v a j data.

.. image:: ./src/tetra_pak_a3_flex_cam/Tetra_Pak_A3_flex_Curves_with_721_points.png
   :width: 600
   :alt: Tetra_Pak_A3_flex_Curves_with_721_points

Ploted Results
~~~~~~~~~~~~~~

Curves for different type of packages can be derived with the python
scripts in `src <src>`__.

`Here <temp_png/plot_of_Cam_Curves_for_TPA_330sq_with_knots.png>`__ is
the cam profile for TPA 330 SQ on A3 Compact Flex machine.

.. figure:: https://tva1.sinaimg.cn/large/006tNbRwly1g9ji1vg98dj31c10u0b16.jpg
   :alt: 

`Here <plot/plot_of_Cam_Curves_for_TBA1000sq.png>`__ is the cam profile
for TBA 1000 SQ on A3 Flex machine.

.. figure:: https://tva1.sinaimg.cn/large/006tNbRwly1g9ji6kzml7j31c00u0qv6.jpg
   :alt: 

Roadmap
-------

-  Search for objective information, March 2019
-  Derive data from chart as a reference object, April 2019
-  Comprehend timing chart of each stage of machine movement, May 2019
-  Analyze the mechanisms of crack-slider, September 2019
-  Synthesis the movement of each stage, October and November 2019
-  Inform the industry that this project have been released publicly.
-  Fetch the opportunity to check and run on real machines.
-  Write a tutorial on how to run these scripts to generate other
   curves.
-  Refactor the codes aiming at the API for customized parameter script.
-  Abstract the algorithm as backend of a cam design add-on for FreeCAD.
-  Gather more applications of various conditions with high-speed cams.

Readme Changelog
----------------

- 2020-01-08 reformat this readme file.
- 2020-08-29 refresh the tetra pak a3 curve with 721 points sample.


