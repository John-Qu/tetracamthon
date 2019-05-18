# Note of *Design and Modeling of a Mechatronic Packaging Machine*

## Authors

D. Borghi, R.Borsari, M.Poppi, E. Sacchetti 

Tetra Pak Carton Ambient S.p.A., Modena, Italy

L. Bassi

University of Bologna, Department of Electronics, Computer Science and Systems, Bologna, Italy

## Terminology

model-based systems engineering approach

characteristics 

attribute/requirement driven

functional decomposition

the drive unit of the package-forming module of a filling machine for liquid food packaging.

the package forming process typical of Tetra Pak Carton Ambient filling equipments.

Architecture

### Flow functions

In order to manage the extreme complexity of the package forming process, a functional decomposition approach has been taken [8], treating the other concurrent processes (aseptic, filling and sealing) as external processes connected through interfaces. This allows the development of a functional model of the forming process based on two main concepts [9] [10]: function, defined as a performed operation that is expressed as the active verb of a verb-object pair, and flow, defined as the change with respect to time of the object of the verb- object pair. A flow is the recipient of the function operation. Three types of flows are used: material, energy and signal, even if the distinction is purely a matter of convenience since all signals are in fact energy flows.

## Earned

### Challenges

Engineering design of systems is nowadays showing a strong tendency towards the creation of more and more complex products encompassing several different engineering domains. 

Mechatronic systems, integrating together mechanical, electrical/electronic (and possibly hydraulic/pneumatic, etc.) components with information processing and control elements are a typical example of this **class** of products. 

On the other hand we assist also to an increased pressure on shortening development lead times and cutting costs.

### Why Tetra Pak develop roll-fed (in contrast to blank-fed) systems?

Tetra Pak develops, produces and markets food processing and packaging systems, i.e. processing equipments, packaging materials, package specifications, packaging machines and distribution equipments. Tetra Pak Carton Ambient more specifically is mainly involved in aseptic packaging systems and this means that strong focus is on process hygiene and integrity of the packages, in addition to other attributes, common to other types of packaging systems, like package appearance, cost, convenience and so on. In order to fulfill the strong quality/legal requirements typical of aseptic packaging, an architectural choice for the filling machine has been taken: we develop roll-fed (in contrast to blank-fed) systems. The resulting process is schematically shown in fig.1.

![ Fig.1 The package forming process](https://ws3.sinaimg.cn/large/006tNc79ly1g2fumem1e7j30u0172qoh.jpg) Fig.1 The package forming process

![](https://ws2.sinaimg.cn/large/006tNc79ly1g2fwz91n0cj30v50u07wh.jpg)

The roll-tube concept enables space savings before and after filling and high confidence that the whole surface of the packaging material is correctly sterilized, since planar surfaces fulfill the requirements of an aseptic system, in terms of time/temperature exposition to sterilization agents and successive drying, more than complex geometries. Furthermore, the complexity of the filling system is greatly reduced with increased hygienic level and lastly, the resulting packages are totally filled, enabling high product quality and good distribution properties.

### Functional network

The functional network resulting from the analysis is a quite abstract, but very useful description of the process in terms of the elementary functions that are required to achieve its overall purpose. The complete functional network of the forming process is too complex to be shown and described here, but as an example in fig.2 we present a simplified chunk of the network with a single function shown with all its inputs and outputs. The complete network is made of about **forty** functions.

![Fig.2 Functional network – single function example](https://ws1.sinaimg.cn/large/006tNc79ly1g2fumw79zaj31790u0woo.jpg)Fig.2 Functional network – single function example

The approach followed during the development of the functional model has been to take as much as possible a solution independent decomposition, identifying only the functions that are strictly needed to transform the reel of packaging material into fully filled, tight sealed packages, as seen from the packaging material perspective, leaving aside the other functions added by the specific devices used to implement the process (which instead are of course solution dependent).

The availability of the functional network opens several different possibilities: first of all it is easy to follow the main flows of materials, energ y and information along the process, clarifying the relevant changes of state. Secondly the main input/outputs variables of each function can be identified, classified and qualified/quantified according to the specific function description. This is accomplished either by defining empirical relations based on heuristics or experience or using quantitative data coming from standard test methods or simulation models.

### Define the process with input, output and the model

The complete collection of the function descriptions, the functional network and the relationships between the process variables constitute the pillars of our forming process model, which may be used to relate process inputs to outputs, to identify the main attributes and define the relevant functional requirements for the design of forming units. In fig.3 we summarize the relationship among process inputs, outputs and the model.

![Fig.3 The Package Forming Process](https://ws2.sinaimg.cn/large/006tNc79ly1g2fuu17ujij31i00u0gul.jpg)Fig.3 The Package Forming Process

### Stages of design of a package forming unit

**Originating requirements** for a new package forming unit are usually expressed by assigning targets to some established set of attributes such as capacity, operational cost, flexibility, reliability and so on. 

Starting from this point it is necessary to perform a first draft forming process design, in order to clearly determine the **functional requirements** that the unit will have to fulfill.

Using our functional network and related qualitative/quantitative models it is possible at this stage, starting from the assigned originating requirements, to define **process kinematics**, i.e. the temporal sequence of deformation (geometry and motion) steps needed to transform the tube of packaging material into filled, tight
sealed packages fulfilling shape and size requirements.

Process kinematics enables the definition of the trajectory and the shape of the tools that mechanically interacting with the packaging material, translating some of the originating requirements into **system requirements** expressed into more familiar engineering terms.

Indeed the next step in the design process is to synthesize a suitable **mechanical system** that is able to fulfill these requirements set.

Once these system level requirements are defined, they are translated into functions that are in turn mapped into suitable physical architectures (structured collection of elements which realize the specified functions). These architectures are then evaluated based on technical and economic criteria to determine suitable concepts.

We are now ready to start a **preliminary embodiment of the selected solution**. This includes: 

1. the definition of the **assembly structure** and 
2. the preliminary **part shapes**, 
3. a preliminary **materials selection** and 
4. **inertial properties** evaluation. 
5. The characteristics of the **motion profiles** to be generated, and the inertial properties estimation allow also 
6. the definition of the **requirements for the drive unit.**

### Typically common engineering requirements in mechanism synthesis

be classified as follows [11]:

- Topological requirements specifying the nature of the motion and the degrees of freedom;
- Functional requirements specifying the number of independent outputs, the task to be accomplished by each output and the complexity of each task;
- Constraints such as dimensional or inertial constraints.

### Advantages of a catalogue of solutions already available

The resulting kinematic synthesis problem, usually very complex to solve, is simplified in our case since we have a catalogue of solutions already available among which we can select the one that best suites our purposes. 

In our example we develop a system that fulfills flexibility requirements (other architectures exist that fulfill different kind of requirements, such as high capacity [12] or low cost). 

### How to fulfill flexibility requirements?

This means that the resulting solution must 

1. allow change of volume/format/shape of the package 
2. with minimal changes in machine components, 
3. in a short time frame, 
4. without losing sterile settings. 
5. Furthermore, to allow flexibility, the forming unit must allow fast change of the trajectory of the tools interacting with the packaging material tube. 

Among different possibilities, to fulfill these functional characteristics, we select a **“scissors-like” mechanism** made of a slider crank mounted on a translating member. 

Given the mechanism topology and structure, the synthesis problem is reduced to finding the optimal dimensions of the links that enables precise function generation according to the requirements of forming process kinematics. 

This can be easily accomplished by constrained optimization analysis of a simple kinematic multi-body model. The skeleton of the resulting mechanism is shown in fig.5 in four different configurations along the required trajectory to be followed.

![Fig.5 Selected Mechanism and Tools Trajectories](https://ws3.sinaimg.cn/large/006tNc79ly1g2fvw1jvf3j30uu0u0qj5.jpg)Fig.5 Selected Mechanism and Tools Trajectories

In order to fulfill also trajectory flexibility requirements we select a mechatronic servo drive architecture shown in fig.6. 

![Fig. 6 Drive Unit Architecture](https://ws3.sinaimg.cn/large/006tNc79ly1g2fw4xkhi3j31qs0ig43x.jpg)Fig. 6 Drive Unit Architecture

The motion profile generator is executed in the controller and generates the set point for the drive that in turns executes position, speed, torque loops. Finally the power electronics transform the values into physical entities (i.e. Ampere). The feedback system (resolver or encoder for position and velocity, Hall effect sensor for current) closes all the three loops. 

This servo drive architecture allows high kinematics performances in terms of: 

1. strict profile following, 
2. high system bandwidth, 
3. system stiffness and, of course, 
4. possibility to change profiles at will.

The two mechanism degrees of freedom are then driven by two translational axes moved by two AC servomotors with timing belt/pulley couplings. In order to form packages we need two such mechanisms with identical motions shifted in time by half period. 

### Stages of verifying the drive unit solution

To verify that this type of solution fulfills the functional requirements set by the process, we use different models of increasing complexity reflecting **the different confidence level** about the system under development acquired during the design process. 

Initially we have to dimension the belt/pulley drive according to kinematic/dynamic requirements. 

Then we have to investigate that the solution does not introduce unexpected vibrations into the drive due to flexibility of the couplings and 

that the position errors due to the elasticity of the belt is within the limits set by the process model. 

A model of the belt/pulley drive **where the belt elasticity is lumped into variable spring stiffness components** [13], together with variation of the natural frequencies of all the belt drives as a function of machine degrees (non dimensional time scale).

A more detailed model, using a **mixed multibody/finite elements approach** to account for distributed elasticity, is then used to understand how dynamically the elasticity of the belt affects the precision of motion transmission of the motion.

Furthermore, a **model able to reproduce the behavior of the chain composed by the controller, drive, motor and load** is used [14] to analyze the connection between the zeros/poles of the system and the various parameters of the adopted PID control.

The model shown in fig.7 has been realized to understand the transfer function of PID controller, motor and load. This model allows us to understand the connection between the zeros and the poles and the various parameters of the PID control. The simulations on the model reproduce the behavior of the control system during the tuning test. Considering that all the machines will have the same drive, it’s possible to simulate different application changing the motion profile and motor and load parameters.

![Fig. 7 Model of controller, motor and load](https://ws4.sinaimg.cn/large/006tNc79ly1g2fwso5fw9j32500u0du7.jpg)Fig. 7 Model of controller, motor and load

We need also **model reproduces the interpolation that the control system does from the PLC up to the drive.** This model generates a motion profile with a fine interpolation which is the input for the model in fig.7.

The final design of one complete side of the drive unit including the mechanism is shown in fig.8.

![Fig. 8 Complete Drive Unit (one side)](https://ws4.sinaimg.cn/large/006tNc79ly1g2fwy17zqij30u016onpd.jpg)Fig. 8 Complete Drive Unit (one side)

