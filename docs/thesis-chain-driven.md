# Note of Functional design and kinematic synthesis of a chain driven high-speed packaging machine

## About Authors

### Roberto Borsari

Dr.-Ing. Roberto Borsari received the degree in Nuclear Engineering  (1989) and Ph.D. in Nuclear Engineering (1994) from the University of Bologna. He is presently manager for Forming and Virtual Verification  within Tetra Pak Packaging Solutions. His major area of expertise is computational physics and his activities focus mainly on  the definition and application of model-based systems engineering approaches to the development of complex packaging systems, with special  emphasis on modeling and simulation of package forming and related manufacturing processes.

Tetra Pak Packaging Solutions SpA, Via Delfini 1, 41123 Modena, Italy

From [here](https://www.degruyter.com/view/j/auto.2016.64.issue-3/auto-2015-0071/auto-2015-0071.xml)

His profile pages are:

* [research gate](https://www.researchgate.net/profile/Roberto_Borsari) 
* [Dblp](https://dblp.org/pers/hd/b/Borsari:Roberto)
* [academia](http://independent.academia.edu/RobertoBorsari)

The most relavant ariticle aside from this one is:

[Design and Modeling of a Mechatronic Packaging Machine](https://www.academia.edu/28934458/Design_and_Modeling_of_a_Mechatronic_Packaging_Machine)

### Felix Dunge

Little information found.

## Terminolody

### layout

In this paper we show a design procedure for the **main layout** of a new concept of packaging machine based on a chain drive.

The starting point for the design of the jaw unit is a simple **geometrical layout** like the one shown if fig.9. 

It easily seen from these figures that the curves corresponding to the two sets of links have been strongly modified by imposing the correct motions to the links. This means that we have modified the **initial layout** and we now need to compensate for the chain length variation in order to minimize the polygon effect that can cause unwanted fluctuations and intermittency.

The main results of this procedure are the set of points of the main cams, the folding flaps cam, the volume adjustment cam and the cutting cam, and the definition of the **general layout** of the system.

Finally it is worth to note here that this parametric procedure has drastically reduced the development time needed to **define the layouts** corresponding to new volumes/shapes of packages.

### introduction

The **introduction of this type of drive unit** allows a significant increase of the capacity of the machine, in comparison with the traditional cam driven mechanisms nowadays in use, but involves some additional complex kinematic and dynamic behaviours that must be carefully analyzed and understood in order to obtain the full functionality of the final design and to avoid unexpected effects during operation.

This forces the minimization of the velocity fluctuations during the motion in order to reduce noise and to avoid unexpected behaviours in operative conditions and **the introduction of a specific spring-like chain-tensioning device** to reduce possible problems due to inertial effects.

### capacity

The introduction of this type of drive unit allows a significant increase of the **capacity** of the machine, in comparison with the traditional cam driven mechanisms nowadays in use, but involves some additional complex kinematic and dynamic behaviours that must be carefully analyzed and understood in order to obtain the full functionality of the final design and to avoid unexpected effects during operation.

1.1 The High **Capacity** TBA/22 Filling Machine.
TBA/22 is a new system inside the Tetra Brik Aseptic portfolio and has been designed with the specific purpose of reducing the costs and raising the **productivity** of the producers. It achieves a **capacity** of 20000 packages per hour, which is about three times the **capacity** of a traditional Tetra Brik filling machine.

The length of this process (together with the one of the sterilization process) puts physical limits on the **capacity** of the machine.

The package dimensions and shape, the **capacity** of the machine and the sealing time mainly decide the dimensions defining this configuration.

### chain drive

The elementary mechanics of **chain drives** has been known for many decades. There are however some subtle characteristics that require complex analyses to be fully understood due to the advanced mechanics involved. The conventional **roller chain drive** consists of two sprockets and a chain belt. The chain belt is made up of discrete links. The motion transmission is due to the geometry of the connection and there is no relative sliding. The chain axis, i.e. the line connecting the centers of the axles, is made of a regular polygon inscribed inside the primitive circle of the sprocket. The main consequences of this are:

1. The axles connecting the links of the chain are lifted and lowered subsequently (polygon effect) during the motion.
2. The absolute speed and acceleration of the axles vary during the motion. These fluctuations decrease rapidly as the number of teeth of the sprocket increases.
3. If the two sprockets (drive and driven) have different diameter the transmission ratio varies cyclically. Furthermore the length of the chain span varies discontinuously with time.
4. The teeth of the sprockets and the axles of the links have different velocities (mainly in direction) when they come in contact. This causes impacts and energy losses that are proportional to the square of the angular velocity of the sprocket.

### cam drive

In traditional systems the jaw system is a **cam driven** mechanism made of two moving jaws in alternative motion.

This **cam** drives the motion of the volume box (or volume flaps) carried by each link.

### kinematic

Functional design and **kinematic synthesis** of a chain driven high-speed packaging machine

For this reason, starting from basic geometric and functional parameters easily derived from the main specifications, all the steps involved in the design process are performed, without specific reference to any defined geometry of the bodies, using ADAMS **kinematic parametric models**.

Once a **kinematically satisfactory scheme** has been found, all the relevant information is transferred to the CAD system where the actual parts and assemblies are created using the guidelines defined during the kinematic synthesis.

A parametric Adams **kinematic model** is used to generate the curves that define the basic path of the rollers carrying the links.

The model is **kinematically well defined** and capable to give as result a curve describing the path of the roller of the links.

We proceed in the synthesis process with inverse **kinematic analyses** and since at this stage we have only the knowledge of when and where during the motion a certain phase is completed we are forced to drive the motion backwards.

This is a far too complex problem to be handled at this stage (it involves contacts, nonlinear material behaviours and fluid- structure interactions), so we have developed **a simpler kinematic model** of the forming based on minimizing the deformation (measured as fiber length variations) of the packaging material during the forming process. Despite its simplicity (neglecting most of the real complex physical interactions involved, but trying to keep the essentials), this model has proven to be quite effective and is almost always used during **kinematic cam synthesis**.

Of course this correction should not affect the **already defined kinematics**.

With **a kinematic (this time) forward analysis** is then possible to verify the correct timing of the different phases.

This problem is in reality what is commonly defined a function generation problem in **kinematics**.

Towards a more **exact kinematics** of roller chain drives

### dynamic

It is then possible to estimate the relevant inertia properties that can be transferred in ADAMS to perform **a fully dynamic analysis**, allowing both the calculation of the forces acting on the various parts, which can then be used for finite element analyses, and the verification of the system actual performances.

Since in this case the performance of the system is strongly affected by the interaction between the cams and the fixed pins, **a dynamic analysis** is in order to obtain information about the contact forces, needed to dimension the parts, and the actual motion profile of the blade and the corresponding cutting force.

This estimation, although not very accurate since many **dynamic aspects** are not included, is however enough for dimensioning the parts and in particular the links.

A fully **dynamic model** has created based on the existing kinematic model introducing all the complex contact interaction among parts. 

**Multibody dynamics** with unilateral contacts

### behaviour

The introduction of this type of drive unit allows a significant increase of the capacity of the machine, in comparison with the traditional cam driven mechanisms nowadays in use, but involves some additional **complex kinematic and dynamic behaviours** that must be carefully analyzed and understood in order to obtain the full functionality of the final design and to avoid unexpected effects during operation.

This forces the minimization of the velocity fluctuations during the motion in order to reduce noise and to avoid **unexpected behaviours** in operative conditions and the introduction of a specific spring-like chain- tensioning device to reduce possible problems due to inertial effects.

This is a far too complex problem to be handled at this stage (it involves contacts, **nonlinear material behaviours** and fluid- structure interactions), so we have developed a simpler kinematic model of the forming based on minimizing the deformation (measured as fiber length variations) of the packaging material during the forming process.

### operative

This forces the minimization of the velocity fluctuations during the motion in order to reduce noise and to avoid unexpected behaviours in **operative conditions** and the introduction of a specific spring-like chain- tensioning device to reduce possible problems due to inertial effects.

adjective

1 *this piece of legislation is not yet operative*: in force, in operation, in effect, valid. ANTONYMS  invalid.

2 *most of our antique machinery is operative*. See [operational](x-dictionary:r:t_en_us1009568:com.apple.dictionary.OAWT:operational).

operational adjective 

*the new conveyor belts will be operational by tomorrow*: up and running, running, working, functioning, operative, in operation, in use, in action; in working order, workable, serviceable, functional, usable, ready for action. ANTONYMS  out of order, broken.

3 *when I say ‘perhaps I'll go,’ the operative word is ‘perhaps’*: key, significant, relevant, applicable, pertinent, apposite, germane, crucial, critical, pivotal, central, essential. ANTONYMS  irrelevant.

noun 

1 *the operatives clean the machines*: machinist, (machine) operator, mechanic, engineer, worker, workman, blue-collar worker.

2 *an operative of the CIA*: agent, secret agent, undercover agent, spy, mole, plant, double agent; *informal* spook; *archaic* intelligencer.

3 *we hired our own operatives*: detective, private detective, investigator, private investigator, sleuth; *informal* private eye, bloodhound; *informal* *dated* gumshoe, dick, private dick.

### geometric/geometrical

For this reason, starting from **basic geometric** and functional parameters easily derived from the main specifications, all the steps involved in the design process are performed, without specific reference to any defined geometry of the bodies, using ADAMS kinematic parametric models.

The starting point for the design of the jaw unit is a simple **geometrical layout** like the one shown if fig.9.

This motion is fully determined by **geometric clearances considerations** and depends only on the chosen dimensions of the sprocket, of the rollers pitch, of the jaw pressure stroke (which in turn is defined by the chosen spring stiffness and the sealing pressure), and of course of the package at hand.

The **geometric description** is kept at a minimum level, leaving out any complex manipulation of existing CAD models and reducing to a minimum design constraints (at geometrical level) at this stage.

### functional

**Functional design** and kinematic synthesis of a chain driven high-speed packaging machine

The introduction of this type of drive unit allows a significant increase of the capacity of the machine, in comparison with the traditional cam driven mechanisms nowadays in use, but involves some additional complex kinematic and dynamic behaviours that must be carefully analyzed and understood in order to obtain the **full functionality** of the final design and to avoid unexpected effects during operation.

For this reason, starting from basic geometric and **functional parameters** easily derived from the main specifications, all the steps involved in the design process are performed, without specific reference to any defined geometry of the bodies, using ADAMS kinematic parametric models.

The relevant **machine functions** are described with the help of fig.2.

In the following we will examine the steps involved in the **functional design and synthesis** of all the mechanisms and motions involved in the package-forming phase.

This problem is in reality what is commonly defined a **function generation problem in kinematics**.

In fact, given a certain motion of link1 we want to define a suitable mechanism such that link2 performs a motion that is **a function of** the motion of link1. In this particular case the function is simply **the identity function**.

The model is defined with just starting approximate values for the driving parameters and with all the relationships needed to drive all the dimensions by these free parameters. Then **a goal function** is defined as the maximum absolute error between the vertical positions of the end point of the fingers. The goal function is then minimized with a constraint on angular velocities. (Why?)

The motion should be **a ramp-like function of time**, and we use a standard modified trapezoid motion law to minimize the acceleration peaks.

The volume box has **the function to** form the body of the package and at the same time it should give the package the correct volume content.

### specification

For this reason, starting from basic geometric and functional parameters easily derived from **the main specifications**, all the steps involved in the design process are performed, without specific reference to any defined geometry of the bodies, using ADAMS kinematic parametric models.

The systems include packaging material, **package specifications**, filling machine and distribution equipment for the filling line.

Since the pivot distance is fixed by **package specification** and is given for a given shape/volume, the mechanism is completely defined by the four variables rad1, rad2, ang1 and ang2, the length of the connecting rod being univocally defined by these parameters.

As can be seen from the figure the maximum error between the vertical positions has been reduced from about 0.2 mm to about 0.055 mm using 13 iterations. It should be noted here that the maximum allowed by the **design specifications** is 0.1 mm.

Since there are some overlaps in the motion profiles this phase diagram is fundamental information that allows an early determination of possible forming problems due to inadequate timing. If this is the case then some **design specification** has to be accordingly redefined and the complete procedure should be re- run. 

The total mass of the link is quite easy to estimate from the main dimensions given by the **design specification**, and the motion of the link in this stage should be a pure translational motion, so the inertia properties other than the mass play a little role.

noun 

1 *the clear specification of objectives*: statement, identification, definition, description, setting out, framing, designation, detailing, enumeration; stipulation, prescription.

2 (specifications) *a shelter built to their specifications*: instructions, guidelines, parameters, stipulations, requirements, conditions, provisions, restrictions, order; description, details; *informal* specs.

### inertia

It is then possible to estimate the **relevant inertia properties** that can be transferred in ADAMS to perform a fully dynamic analysis, allowing both the calculation of the forces acting on the various parts, which can then be used for finite element analyses, and the verification of the system actual performances.

Furthermore the chain is not made of simple links but each link is in reality the assembly of a number of sub-systems resulting in **a considerable final mass** with **complex inertia distribution**.

This forces the minimization of the velocity fluctuations during the motion in order to reduce noise and to avoid unexpected behaviours in operative conditions and the introduction of a specific spring-like chain- tensioning device to reduce possible problems due to **inertial effects**.

Once the CAD models have been defined, it is quite easy to transfer back the **inertia properties** to Adams and run new analyses to estimate the forces.

*Physics* a property of matter by which it continues in its existing state of rest or uniform motion in a straight line, unless that state is changed by an external force. See also [moment of inertia](x-dictionary:r:m_en_gbus0654650:com.apple.dictionary.NOAD:moment of inertia).

• *[with modifier]* resistance to change in some other physical property: *the thermal inertia of the oceans will delay the full rise in temperature for a few decades*.

moment of inertia 

noun 

*Physics* a quantity expressing a body's tendency to resist angular acceleration. It is the sum of the products of the mass of each particle in the body with the square of its distance from the axis of rotation.

### stage

This allows a great flexibility and, **during the initial stages of the design process**, gives the possibility to quickly loop several times over different possible solutions simply changing some user defined parameters without any effort spent to change already existing complex CAD models.

**During this stage** the flaps of the semi- finished package are folded and glued on the side panels.

We proceed in the synthesis process with inverse kinematic analyses and since **at this stage** we have only the knowledge of when and where during the motion a certain phase is completed we are forced to drive the motion backwards.

 This is a far too complex problem to be handled **at this stage** (it involves contacts, nonlinear material behaviours and fluid- structure interactions), so we have developed a simpler kinematic model of the forming based on minimizing the deformation (measured as fiber length variations) of the packaging material during the forming process. 

At this stage the kinematic synthesis of the main cams is completed since all the motions needed to form the package are accounted for in the chain path.

At this stage it is quite simple to mount on our model the volume box parts and give them the appropriate motion, since all the other needed reference motion profiles are already well defined.

The total mass of the link is quite easy to estimate from the main dimensions given by the design specification, and the motion of the link in this stage should be a pure translational motion, so the inertia properties other than the mass play a little role.

The geometric description is kept at a minimum level, leaving out any complex manipulation of existing CAD models and reducing to a minimum the design constraints (at geometrical level) at this stage.

1 *this stage of the development*: phase, period, juncture, step, point, time, moment, instant, level.

2 *the last stage of the race*: part, section, portion, stretch, leg, lap, circuit.

### phase 

stage process sequence operation motion

The packages are formed at the top of the jaw system. In fig. 4 the detail of **the forming phase** is shown. It is seen that the packages are formed by the jaws (grey) and by the volume flaps (green).

In fig.8 it is shown the package configuration inside the jaw system during **the phase of** jaw pressure applied.

The sequence of operations in **this phase** is: jaw pressure application, design correction, sealing pulse, and cooling time.

First of all it is not made of two sprockets and the chain but, since we need to strictly follow the motion of the links during **the forming, sealing and cutting phases**, the motion is controlled by a series of cams.

This curve is shown in fig.11 and is used as the basis for successive corrections needed to allow **all the phases involved in the package forming process** to be correctly executed.

We proceed in the synthesis process with inverse kinematic analyses and since at this stage we have only the knowledge of when and
 where during the motion **a certain phase** is completed we are forced to drive the motion backwards.

The main goal of this motion is to introduce into the exiting curves the correction needed to correctly perform the **jaw pressure and in movement** (as we call the motion during the forming of the package from the tube) **phases**.

With a kinematic (this time) forward analysis is then possible to verify the correct timing of the **different phases.**

Having defined all the motions and subsystems involved in the package forming we are now in position to check the synchronization of all the motions involved in order to obtain a suitable **phase diagram**.

Since there are some overlaps in the motion profiles this **phase diagram** is fundamental information that allows an early determination of possible forming problems due to inadequate timing.

It allows an early evaluation of the performances of the final design and in
particular it is possible to have a good estimate of **the actual phase diagram**,
highlighting possible timing/sequence problems during forming.

1 a distinct period or stage in a series of events or a process of change or development: *the final phases of the war* | *[as modifier]* *:  phase two of the development is in progress*. 

• a stage in a person's psychological development, especially a period of temporary unhappiness or difficulty during adolescence or a particular stage during childhood: *you are not obsessed, but you are going through a phase*. 

• each of the separate events in an eventing competition.

5 *Physics* the relationship in time between the successive states or cycles of an oscillating or repeating system (such as an alternating electric current or a light or sound wave) and either a fixed reference point or the states or cycles of another system with which it may or may not be in synchrony.

### configuration

In fig.8 it is shown the package **configuration** inside the jaw system during the phase of jaw pressure applied.

The starting point for the design of the jaw unit is a simple geometrical layout like the one shown if fig.9. The package dimensions and shape, the capacity of the machine and the sealing time mainly decide the dimensions defining this **configuration**.

We show in fig.15 the curves resulting after the correction calculated by this model. The curve and the rollers corresponding to the link set 1 are displayed in green and the ones to set 2 in magenta. The figure shows **the configuration frame 1** that corresponds to the complete jaw pressure application; while in fig. 16 we show the last frame corresponding to the tube hitting (we are once more moving backwards).

The chosen mechanism for this task is a four bar linkage in the **anti-parallelogram configuration**, see fig.6.

Fig.21 shows the position error in the **resulting configuration** that corresponds to a rotation of the driving link1 of 90 degrees (the time on the x-axis is not the absolute physical time but a normalized one).

The skeleton of the resulting mechanism is shown in fig.5 in **four different configurations** along the required trajectory to be followed.

noun *proper configuration of the sound system will improve the acoustics*: arrangement, layout, geography, design, organization, order, grouping, positioning, disposition, alignment; shape, form, appearance, formation, structure, setup, format.

### trajectory

This motion is fully determined by geometric clearances considerations and depends only on the chosen dimensions of the sprocket, of the rollers pitch, of the jaw pressure stroke (which in turn is defined by the chosen spring stiffness and the sealing pressure), and of course of the package at hand. The resulting trajectory of the roller centers is shown in fig. 13.

The resulting trajectory curve of the roller center (see fig.18) is then used to define a suitable cam for the folding flap mechanism.

1 the path followed by a projectile flying or an object moving under the action of given forces: *the missile's trajectory was preset* | *figurative* *:  the rapid upward trajectory of Rich's career*. 

2 *Geometry* a curve or surface cutting a family of curves or surfaces at a constant angle.

## Abstract.

### what

In this paper we show **a design procedure** for the main layout of a new concept of **packaging machine** based on **a chain drive**. 

### Why

The introduction of this type of drive unit allows a significant increase of the **capacity of the machine**, in comparison with the traditional cam driven mechanisms nowadays in use, but involves some **additional complex kinematic and dynamic behaviours** that must be carefully analyzed and understood in order to obtain the full functionality of the final design and to avoid unexpected effects during operation. 

### How

For this reason, starting from basic geometric and functional parameters easily derived from the main specifications, **all the steps involved in the design process** are performed, without specific reference to any defined geometry of the bodies, using ADAMS kinematic parametric models. 

### Advantages

This allows a great flexibility and, during the initial stages of the design process, gives **the possibility to quickly loop several times** over different possible solutions simply changing some user defined parameters without any effort spent to change already existing complex CAD models. 

### Usability

Once a kinematically satisfactory scheme has been found, all the relevant information is transferred to the CAD system where the actual parts and assemblies are created using the guidelines defined during the kinematic synthesis. It is then possible to estimate the relevant inertia properties that can be transferred in ADAMS to perform a fully dynamic analysis, allowing both the calculation of the forces acting on the various parts, which can then be used for finite element analyses, and the verification of the system actual performances.

## Frame

1. Introduction.
   1. The High Capacity TBA/22 Filling Machine.
   2. Description of the jaw system.
2. Kinematic synthesis of the main cams.
   1. Basic curves definition.
   2. Jaw pressure application and in movement correction.
3. Kinematic synthesis of the design correction mechanism.
4. Volume adjustment mechanism and Phase diagram.
5. Cutting mechanism design.
6. Conclusions.
7. References.

## Earned

### Business Unit Tetra Brik

Tetra Pak develops, manufactures and markets systems for processing, packaging and distribution of liquid food. 

Business Unit Tetra Brik is a part of the Carton Division of the Tetra Pak Group and is responsible for the development, production, marketing and support of the Tetra Brik Packaging Systems. 

The systems include packaging material, package specifications, filling machine and distribution equipment for the filling line.

### The fundamental idea behind this type of packaging systems

to form a tube from a roll of plastic-coated paper, fill it with the liquid product and seal it below the liquid level. The entire process is continuous and takes place in a single machine, which both forms and fills the package. This process is schematically shown in fig.1.

It is also possible to see in fig.1 that from the same concept not only different volumes but also different shapes of packages can be obtained.

### The main advantages of this roll/tube concept are:

a. the space savings before and after filling,

b. it is possible to sterilize the whole surface of the packaging material,

c. the resulting simple filling system gives high hygiene,

d. the packages are fully filled ensuring high quality product and good distribution
properties.

### TBA/22 The relevant machine functions

![Fig. 2 The TBA/22 filling machine.](https://ws2.sinaimg.cn/large/006tNc79ly1g2euw1enfej310g0u04qq.jpg)Fig. 2 The TBA/22 filling machine.

1. Packaging material supply. Two reels of packaging material are placed in an integrated section of the machine. The reels are spliced automatically by induction heat. This solution enables the next reel to be spliced before the one currently in use is finished.
2. Longitudinal sealing. Induction heat is used for sealing the longitudinal seam of the packages.
3. Aseptic system. Sterilization of the packaging material is achieved by letting the packaging material pass through a deep bath of hydrogen peroxide. Rollers remove the hydrogen peroxide from the packaging material and residues are evaporated by hot sterile air.
4. Jaw unit. The jaw unit consists of two chains opposite each other driven at constant speed by a servo-motor. Each chain is made of 10 links and these links move against fixed cams. In the jaw system a semi-finished filled package (with a pouch-like shape) is created and cut out from the tube.
5. Single final folder. After the semi-finished package has been created from the tube in the jaw system, it is folded into its final shape in the final folder. This consists of a single chain driven at constant speed by a servo-motor. During this stage the flaps of the semi- finished package are folded and glued on the side panels.
6. Product filling system. The product filling system is equipped with a level probe that senses and controls the liquid level by a regulating valve connected to the electronic control system.
7. Platform
8. Electrical cabinet with air cooler. 
9. Waste conveyor.
10. Integrated closed water cooling system.
11. Service unit.
12. Interactive operator’s panel.

### Description of the jaw system

The main function of the jaw system in every type of Tetra Brik machines is to form a semi finished package from the packaging material tube filled with the product. In traditional systems the jaw system is a cam driven mechanism made of two moving jaws in alternative motion.

Let us now examine the main function achieved by the resulting chain driven mechanism. In fig.3 we present an overview of the final assembly with the two chains carrying the links and the tube of packaging material. The links on one side (left in fig.3) are called sealing links, while the ones on the other side are called pressure links. The reason for these denominations will be clear in a moment. 

![Fig. 3 The TBA/22 jaw system.](https://ws1.sinaimg.cn/large/006tNc79ly1g2evk8shyzj313k0u0qv6.jpg)Fig. 3 The TBA/22 jaw system.

The packages are formed at the top of the jaw system. In fig. 4 the detail of the forming phase is shown. It is seen that the packages are formed by the jaws (grey) and by the volume flaps (green).

![Fig. 4 Semi finished package forming inside the jaw system.](https://ws4.sinaimg.cn/large/006tNc79ly1g2evlizzb5j313s0u0u0y.jpg)Fig. 4 Semi finished package forming inside the jaw system.

After the jaws are closed together a special mechanism folds the flaps in the bottom of the package in order to keep the printed image on the package synchronized with the overall motion (design correction). This is shown in fig.5 where the end fingers of this mechanism are shown in blue. This mechanism is governed by a control system based on optical sensing. This mechanism is responsible for design correction and is called folding flap mechanism.

![Fig. 5 The printed image is kept in position by the folding flaps (blue).](https://ws1.sinaimg.cn/large/006tNc79ly1g2evlk6g56j30y00pmnpd.jpg)Fig. 5 The printed image is kept in position by the folding flaps (blue).

The complete mechanism is shown in fig.6. The stroke of the folding flaps (fingers) is set by a cam (yellow) which is controlled by a servo-motor. The servo-motor affects the cam via a belt (green) and two eccentric shafts (blue, grey).

![Fig.6 The folding flap mechanism.](https://ws4.sinaimg.cn/large/006tNc79ly1g2evlkuqw1j31420u0qv5.jpg)Fig.6 The folding flap mechanism.

After the jaws are closed and before the folding flaps have started to adjust the package relative position, the jaw are pressed together in order to apply the so-called jaw pressure needed to seal transversally the packages. This jaw pressure is applied by two springs (violet in fig.7) in each pressure jaw. This is shown in fig.7.

![Fig. 7 Jaw pressure applied by spring loading.](https://ws4.sinaimg.cn/large/006tNc79ly1g2evll61t0j312o0q81kx.jpg)Fig. 7 Jaw pressure applied by spring loading.

In fig.8 it is shown the package configuration inside the jaw system during the phase of jaw pressure applied. This figure is obtained by virtually opening the jaw system during the motion.

The sequence of operations in this phase is: jaw pressure application, design correction, sealing pulse, and cooling time.

![Fig. 8 Jaw pressure applied.](https://ws4.sinaimg.cn/large/006tNc79ly1g2evlm2xpej31400u0kjn.jpg)Fig. 8 Jaw pressure applied.

Once the jaw pressure is fully applied the sealing pulse starts. To seal transversally the packages we use an induction heating system mounted on each sealing link. This induction system generates an eddy current distribution on an aluminum layer inside the packaging material structure. The aluminum heats up due to Joule effect and transfers heat to the adjacent polyethylene (PE) layers that reach their melting temperature. Due to the applied pressure there is a mixing between the melted PE layers corresponding to the two open opposite sides of the tube pressed together. After the sealing pulse is terminated there is a cooling time that enables the PE to re-solidify as a single layer. This guarantees a strong and tight sealing of the packages and is one of the most advanced and developed technologies in our machines. The jaw must be closed, i.e. the jaw pressure must be kept, during a period long enough to allow a suitable sealing and cooling time, in order to ensure a tight closure of the package. The length of this process (together with the one of the sterilization process) puts physical limits on the capacity of the machine.
After the end of the cooling time a cutting mechanism carried by the pressure link cuts the package in correspondence of the transversal sealing area. The package then falls down in a conveyor to enter the final folder.

### The elementary mechanics plus further sources of complexity

The main consequences of this are:
a. The axles connecting the links of the chain are lifted and lowered subsequently (polygon effect) during the motion.
b. The absolute speed and acceleration of the axles vary during the motion. These fluctuations decrease rapidly as the number of teeth of the sprocket increases.
c. If the two sprockets (drive and driven) have different diameter the transmission ratio varies cyclically. Furthermore the length of the chain span varies discontinuously with time.
d. The teeth of the sprockets and the axles of the links have different velocities (mainly in direction) when they come in contact. This causes impacts and energy losses that are proportional to the square of the angular velocity of the sprocket.

First of all it is not made of two sprockets and the chain but, since we need to strictly follow the motion of the links during the forming, sealing and cutting phases, the motion is controlled by a series of cams. 

The chain drive of TBA/22 shows further sources of complexity. Furthermore the chain is not made of simple links but each link is in reality the assembly of a number of sub-systems resulting in a considerable final mass with complex inertia distribution. This forces the minimization of the velocity fluctuations during the motion in order to reduce noise and to avoid unexpected behaviours in operative conditions and the introduction of a specific spring-like chain- tensioning device to reduce possible problems due to inertial effects.

### Start from a simple geometrical layout

The starting point for the design of the jaw unit is a simple geometrical layout like the one shown in fig.9. 

![Fig.9 Model schematic.](https://ws4.sinaimg.cn/large/006tNc79ly1g2eznmo2amj31410u01ei.jpg)Fig.9 Model schematic.

The package dimensions and shape, the capacity of the machine and the sealing time mainly decide the dimensions defining this configuration. In particular the vertical path has to be long enough to allow a suitable sealing and cooling time under jaw pressure applied. 

External constraints are added by cost, simplicity and size considerations, all being strongly affected by the total number of links that should be minimized. 

Of course the total length of the path should fit with the length of the chain, small differences being absorbed by the tensioning device.

### Different Models on Different Stages

A parametric Adams kinematic model is used to generate the curves that define the basic path of the rollers carrying the links. The Adams model is shown in fig.10 and is made of 6 parts (not including ground), 1 cylindrical,1 revolute, 4 translational joints and 7 motions.

![Fig.10 Adams model for basic curve generation.](https://ws4.sinaimg.cn/large/006tNc79ly1g2ezp1v573j30yb0u0nd5.jpg)Fig.10 Adams model for basic curve generation.

![Fig.11 Basic curve generated by Adams.](https://ws3.sinaimg.cn/large/006tNc79ly1g2ezqgo1l0j31330u01hr.jpg)Fig.11 Basic curve generated by Adams.

A second parametric Adams model is used to correct the basic curve to allow the link to release correctly the jaw pressure. The model is made up of 6 moving parts, 1 cylindrical, 2 revolute, 1 spherical, 3 translational joints and 4 motions. 

![Fig.12 Model for jaw pressure release and out movement.](https://ws3.sinaimg.cn/large/006tNc79ly1g2ezra7ou2j31320u04m8.jpg)Fig.12 Model for jaw pressure release and out movement.

![Fig. 13 Jaw pressure release and out movement curve correction.](https://ws2.sinaimg.cn/large/006tNc79ly1g2ezs66apej31300u01kx.jpg)Fig. 13 Jaw pressure release and out movement curve correction.

A third Adams model is then used to implement the other dimensioning parameters defined by the package and link dimensions. The resulting curves from the previous step are introduced in this model and the corresponding rollers are connected to them by Point to Curve constraints (PTCV). The resulting model is made of 26 moving parts, 22 cylindrical, 1 revolute, 3 spherical and 3 translational joints, 9 motions and 15 PTCV.

![Fig. 14 Chain model.](https://ws1.sinaimg.cn/large/006tNc79ly1g2ezw8yz0ij31350u0e81.jpg)Fig. 14 Chain model.

In fig.18 we show a planar schematic of this mechanism together with the relevant dimensional parameters. The points C and D represent pivot points and link1 and link2 rotate about axes, perpendicular to the plane of the drawing, passing through these points. A cam whose roller center is shown in fig.18 then drives Link1. Points A and B are located in the physical position where the fingers pull down the packaging material during the motion. Since the pivot distance is fixed by package specification and is given for a given shape/volume, the mechanism is completely defined by the four variables rad1, rad2, ang1 and ang2, the length of the connecting rod being univocally defined by these parameters.

![Fig. 18 Schematic of the folding flaps mechanism.](https://ws4.sinaimg.cn/large/006tNc79ly1g2f09cu372j313w0u0h6o.jpg)Fig. 18 Schematic of the folding flaps mechanism.

In this particular case the function is simply the identity function. This requirement will of course be satisfied within a certain tolerance. The problem is easily adapted as an optimization design study. In fig. 19 it is shown the simple Adams model used to solve this problem. The model is defined with just starting approximate values for the driving parameters and with all the relationships needed to drive all the dimensions by these free parameters.

![Fig. 19 Adams model of the folding flaps mechanism.](https://ws1.sinaimg.cn/large/006tNc79ly1g2f0bhau8nj31260u0wv7.jpg)Fig. 19 Adams model of the folding flaps mechanism.

The resulting trajectory curve of the roller center (see fig.18) is then used to define a suitable cam for the folding flap mechanism. This cam is shown in fig. 23 together with the chain and the main cams. It is also shown how the folding flap mechanism looks like once assembled.

![Fig.23 Folding flaps mechanism and cam assembled.](https://ws4.sinaimg.cn/large/006tNc79ly1g2f0ktnapsj31350u07wh.jpg)Fig.23 Folding flaps mechanism and cam assembled.

At this stage it is quite simple to mount on our model the volume box parts and give them the appropriate motion, since all the other needed reference motion profiles are already well defined. In fig.25 it is shown the final assembly.

![Fig. 25 Complete chain assembly.](https://ws3.sinaimg.cn/large/006tNc79ly1g2f0nt3xt6j31340u0hdt.jpg)Fig. 25 Complete chain assembly.

The mass of the cams is a direct consequence of their shape calculated by the inverse kinematic analysis already performed, so a fully dynamic Adams model can be easily constructed. This model is shown in fig.29. We use the data from the previous steps to define a suitable motion profile for the link.

![Fig. 29 Cutting device model.](https://ws4.sinaimg.cn/large/006tNc79ly1g2f0s84wifj31370u0kjl.jpg)Fig. 29 Cutting device model.

### Correction after initial calculation

The resulting curves from the previous step are introduced in this model and the corresponding rollers are connected to them by Point to Curve constraints (PTCV). The resulting model is made of 26 moving parts, 22 cylindrical, 1 revolute, 3 spherical and 3 translational joints, 9 motions and 15 PTCV. The main goal of this motion is to introduce into the exiting curves the correction needed to correctly perform the jaw pressure and in movement (as we call the motion during the forming of the package from the tube) phases. The points on the curves where the jaw pressure release starts have been identified in the previous step of the synthesis. From the needed sealing and cooling time we can calculate the length of the curve vertical path, identifying the points where the jaw pressure must be fully applied (as before we proceed backwards). From this point we disconnect a link from the curves and apply (backwards again) the appropriate motion for the jaw pressure application and the in movement. Simply a smooth polynomial motion on a translational joint gives the jaw pressure application. The in movement is instead a more complex motion to define. It is generated by polynomial interpolation and essentially defines the rotation of the package panels due to the action of the jaw carried by the links on the tube. The actual interaction simulation should include impact between a mechanical system (the jaw) and the filled tube. This is a far too complex problem to be handled at this stage (it involves contacts, nonlinear material behaviours and fluid- structure interactions), so we have developed a simpler kinematic model of the forming based on minimizing the deformation (measured as fiber length variations) of the packaging material during the forming process. Despite its simplicity (neglecting most of the real complex physical interactions involved, but trying to keep the essentials), this model has proven to be quite effective and is almost always used during kinematic cam synthesis. Some finite element simulations have permitted the fine tuning of this model giving suitable values for velocities and accelerations (used as conditions for the polynomial interpolation of the motion) that are not creating damages or tears on the final package.
We show in fig.15 the curves resulting after the correction calculated by this model. The curve and the rollers corresponding to the link set 1 are displayed in green and the ones to set 2 in magenta. The figure shows the configuration frame 1 that corresponds to the complete jaw pressure application; while in fig. 16 we show the last frame corresponding to the tube hitting (we are once more moving backwards).

![Fig. 15 Jaw pressure fully applied.](https://ws3.sinaimg.cn/large/006tNc79ly1g2f011c83qj31370u04qp.jpg)Fig. 15 Jaw pressure fully applied.

![Fig. 16 The jaw hits the tube.](https://ws2.sinaimg.cn/large/006tNc79ly1g2f01svwc4j31370u07wh.jpg)Fig. 16 The jaw hits the tube.

It easily seen from these figures that the curves corresponding to the two sets of links have been strongly modified by imposing the correct motions to the links. This means that we have modified the initial layout and we now need to compensate for the chain length variation in order to minimize the polygon effect that can cause unwanted fluctuations and intermittency.

An additional Adams macro has been created that automatically calculates the chain length variation and minimizes the polygon effect adding a further correction on one of the curves. Of course this correction should not affect the already defined kinematics. Fig.17 shows the calculated correction (cyan curve). This calculated curve is then trimmed and merged into the curve corresponding to link set 1 (green curve).

![Fig.17 Curve correction for polygon effect compensation.](https://ws3.sinaimg.cn/large/006tNc79ly1g2f04jwrk7j313b0u0kik.jpg)Fig.17 Curve correction for polygon effect compensation.

### The usage of phase diagram

Having defined all the motions and subsystems involved in the package forming we are now in position to check the synchronization of all the motions involved in order to obtain a suitable phase diagram. Since there are some overlaps in the motion profiles this phase diagram is fundamental information that allows an early determination of possible forming problems due to inadequate timing. If this is the case then some design specification has to be accordingly redefined and the complete procedure should be re-run. An example of such phase diagram is shown in fig.26.

![Fig. 26 Forming phase diagram.](https://ws3.sinaimg.cn/large/006tNc79ly1g2f0ur18bdj314a0u0dpw.jpg)Fig. 26 Forming phase diagram.

It allows an early evaluation of the performances of the final design and in particular it is possible to have a good estimate of the actual phase diagram, highlighting possible timing/sequence problems during forming.

2019-04-25 17:53:15
