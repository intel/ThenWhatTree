Copyright (C) 2018 Intel Corporation  
SPDX-License-Identifier: BSD-3-Clause

ThenWhatTree
------------
[Package description](#package-description)  
[Background and motivation](#background-and-motivation)  
[ThenWhatTree methodology](#thenwhattree-methodology)  
[ThenWhatTree analysis algorithm](#thenwhattree-analysis-algorithm)  
[ThenWhatTree class](#thenwhattree-class)  
[Getting started](#getting-started)  
   * [CSV schema and requirements](#csv-schema-and-requirements)
   * [ThenWhatTree reserved name space](#thenwhattree-reserved-name-space)
   
[Example input and output](#example-input-and-output)  
   * [Block diagram](#block-diagram)
   * [CSV file](#csv-file)
   * [Generated XML](#generated-xml)
   * [Example output](#example-output)

Package description
----------------------
ThenWhatTree is a tool to capture, formalize, communicate and execute expert knowledge of complex, poorly documented work flows.  The package facilitates description of work flows as decision trees and automates execution of the decision trees based on observable data.  

ThenWhatTree contains utilities for generating and analyzing decision tree collateral that can be run stand alone or incorporated into another script.  The top-level utilities are:

* **generate.py**:  Standalone function that creates a library of python modules based on the nodes of an XML decision tree.  The XML document can be created from a CSV or text file (format requirements below).  The library will contain one eponymous python module for every node in the XML.  The body of each module will be an extension of the ThenWhatTree class.  Any time the CSV file is changed, 'generate' should be run.

   SWITCHES:
   * --csv \<csv file path> (required)
   * --lib \<full path to directory that will contain the decision tree node modules and XML>  (optional)

   OUTPUT:
   * If only the 'csv' switch is provided, function will generate an XML version of the decision tree
   * If the 'lib' switch is provided, function will generate a library of python modules corresponding to the elements of the decision tree.

* **execute_tree.py**:  Standalone function that performs depth-first evalation of an XML decision tree.  Starting at the root node, the function will analyze each node by executing the 'is_true' method of the eponymous python module.  If the node returns ‘True’, the children of the node will be analyzed.  If the node returns 'False', the branch is aborted.  After the tree has been evaluated, the function will then extract out the state and any messages that were logged during execution and return a formatted string.  See sample output at the bottom of this README.

   SWITCHES:
   * --xml \<path to the xml file in the decision tree node library> (required)
   
   OUTPUT:  string
   
* **evaluate**:  Not standalone; intended for import by other modules.  Module performs depth-first evalation of an XML decision tree.  Starting at the root node, the function will analyze each node by executing the 'is_true' method of the eponymous python module.  If the node returns ‘True’, the children of the node will be analyzed.  If the node returns 'False', the branch is aborted.  The status and output from each node are added as node elements of the XML decision tree.  

   ARGUMENT:  path to the xml file in the decision tree node library  
   RETURN:  ElementTree object

* **extract**:  Not standalone; intended for import by other modules.  The status and output from each node are extracted and returned as a formatted string.  See sample output at the bottom of this README.

   ARGUMENT: ElementTree object  
   RETURN:  string

Background and motivation  
--------------------
Hardware design verification engineers are often required to move to different parts of the design to assist other teams.  Learning to debug by ramping on new design collateral and microarchitectural (uAV) flows is difficult when documentation is stale or missing and most of the uAV knowledge is tribal, passed only by word of mouth or by painstakingly tracing signals.  Much effort is wasted relearning what others have learned but could not teach.

My frequent experience in the ramp process allowed me to study the debug process in many different contexts and notice the behavior patterns that were common to them all.  ThenWhatTree is a methodology that simplifies the process of recording debug knowledge and generating a code base that allows for automated execution of debug knowledge.  

ThenWhatTree was named from countless interviews I’ve done where I stood at a whiteboard asking questions of expert debuggers about how to debug a flow.  As I drew block diagrams and branches describing the process, I was always asking the question, “then what?”.  Capturing and analyzing debug flows in a decision tree format allows the flows to be verified, refactored and communicated just like any other specification.  For integration teams dependent on IP providers in different locations and time zones, this removes roadblocks to forward progress.

ThenWhatTree methodology
---------------------------
ThenWhatTree relies on the insight that debug is an algorithmic activity that can be represented in a decision tree.  There is no magic to debug.  Recognized debug experts have merely collected more algorithms in their heads, know how to judiciously apply those algorithms and where to find the data required to feed those algorithms.  This is hard fought knowledge that is difficult to share, poorly preserved and typically unavailable to others outside the virtual or physical presence of the debug expert.  ThenWhatTree is an expert replication methodology.

Starting a fresh debug session is often a fishing expedition.  Sometimes the output from a failing checker or assertion gives a hint.  For a cycle limit violation or hanging test, we usually are starting from a blank slate.  We look for clues by using a standard set of regular expressions to grep the logs with which we’re familiar.  Or we open an fsdb and check the status of our favorite signals.  At an abstract level, we are trying to detect a nugget of data that we can use to decide which node to traverse to next.  We are mentally populating a node in our decision tree.  Every node of every decision tree can be described like this:
```
+--------+--------+
|        |        |
| Detect | Decide |
|        |        |
+--------+--------+
```
Once we detect a nugget of data that looks promising, we decide where to look next then repeat the process as long as it bears fruit.  If we reach a dead end, we return to the previous node, decide differently, go detect again and repeat.  Eventually a debug flow looks something like this:
```
+--------+--------+       +--------+--------+       +--------+--------+
|        |        |       |        |        |       |        |        |
| Detect | Decide +-------> Detect | Decide +-------> Detect | Decide |
|        |        |       |        |        |       |        |        |
+--------+-----+--+       +--------+--------+       +--------+--------+
               |
               |
               |    +--------+--------+        +--------+--------+
               |    |        |        |        |        |        |
               +----> Detect | Decide +--------> Detect | Decide |
                    |        |        |        |        |        |
                    +-----+--+--------+        +--------+--------+
                          |           |
                          |           |
                          |           |        +--------+--------+
                          |           +-------->        |        |
                       +--v-----+--------+     | Detect | Decide |
                       |        |        |     |        |        |
                       | Detect | Decide |     +--------+--------+
                       |        |        |
                       +--------+--------+
```
This tree represents the hard fought knowledge that represents hours or occasionally days of intense focus and consultation with other engineers to connect the dots.  Represented in this way, the two components of debug knowledge are easy to identify:

  - Identifying relevant data (‘detect’) from many MBs of data in a run directory
  - Understanding how to use that data (‘decide’) to make forward progress

When we distill out the data from the algorithm, the ‘detect’ from the ‘decide’, we begin to understand how we debug.  We get fresh ideas on how to efficiently capture and share this hard fought knowledge.  In practice, the ‘decide’ component of debug knowledge is difficult to capture and communicate.  It’s relatively simple to create a cheatsheet for the ‘detect’ component that defines where various pieces of potentially relevant debug data reside.  The ‘decide’ component is more elusive and comes with caveats and conditional statements.  However, it is also the most valuable for capturing and communicating how to debug.

When constructing a debug decision tree, it is critically important to separate the decisions from the data extraction.
  - The structure of the tree should describe the flow of the debug process and must not depend on the data required to analyze the tree.
  - Tree nodes should be named with sufficient abstraction that they are platform-agnostic.
  - Good debug decision trees read like a specification and serve as communication and teaching tools.

In ThenWhatTree methodology, the debug flow is captured in the CSV or XML tree.  The data extraction for node evaluation is expressed inside each node.  By keeping the debug decisions (tree) and data extraction (nodes) separate, the trees can be leveraged across platforms and the node evaluation can be modified based on the data available on specific platforms.

ThenWhatTree development is empirical and iterative.  Trees are easily reconfigured or extended as additional debug knowledge is discovered.  If tree evaluation data is accumulated, high ROI opportunities for tree extension are easily identified.

ThenWhatTree analysis algorithm
--------------------------------------
The tree walking algorithm is summarized as, "If True, go deeper; if False, abort the branch."

Starting from the root node, the entire tree is analyzed in a depth-first algorith.  If a node returns 'True', all of its children will be evaluated.  If a node returns 'False', that branch will be aborted.  There is no limit to the number of children a node can have.  There is no next step if a node returns 'False'.

There is no loop support in ThenWhatTree.

ThenWhatTreeNode class
-------------------------
Below is an example of the body of a ThenWhatTreeNode module named ‘NODE_A’ that was generated using ‘generate.py’.  (This is poorly named but is irrelevant for this example.)

*is_true(self)*
---
ARGUMENTS: self  
RETURN: True, False  

The ‘is_true’ method is the only element of a ThenWhatTree node that requires user input.  The 'is_true' methods will raise a 'NotImplementedError' by default when the module is generated.  The user is required to replace the ‘raise NotImplementedError’ with code that will determine the state of NODE_A and return ‘True’ or ‘False’.
```
    from ThenWhatTree import ThenWhatTreeNode
    class NODE_A(ThenWhatTreeNode):

        def is_true(self):
            raise NotImplementedError
```
The following property and methods may be accessed in the body of the ‘is_true’ method.

*output*
------
This is a property of the base class and should be assigned with a string and not called.  The ‘output’ property is used to convey anything interesting about the node if it return ‘True’.  If the node returns ‘True’, the string assigned to ‘output’ will be printed in the output of the tree.  If the node returns ‘False’, the string assigned to ‘output’ will be dropped.  If it is not set, the ‘output’ default property is the name of the node appended with "is true".  

USAGE:  self.output = \<my_string>
```
from ThenWhatTree import ThenWhatTreeNode
class NODE_A(ThenWhatTreeNode):

    def is_true(self):
        **Insert user code to evaluate whether NODE_A should return True or False**
        self.output = "Custom string for this node goes here"
        return True
```
*set_branch_element(\<key>, \<value>)*
----------------------------------
Method provided to pass data from a node to its children.  The \<value> can be any data structure.
ARGUMENTS: key, value
RETURN: none
USAGE: self.set_branch_element(\<key>, \<value>)
```
from ThenWhatTree import ThenWhatTreeNode
class NODE_A(ThenWhatTreeNode):

    def is_true(self):
        **Insert user code to evaluate whether NODE_A should return True or False**
        self.set_branch_element('my_key', 'my_value')
        return True
```

*get_branch_element(\<key>)*
-------------------------
Method provided to get a key-value pair passed from an ancestor node.  
ARGUMENT: attribute  
RETURN: value pointed at by key  
USAGE: self.get_branch_element(\<key>)  
```
from ThenWhatTree import ThenWhatTreeNode
class NODE_A(ThenWhatTreeNode):

    def is_true(self):
        my_value = self.get_branch_element('my_key')
        **Insert user code to evaluate whether NODE_A should return True or False**
        return True
```

*set_element(\<attribute>, \<value>)*
---------------------------------
Method provided to set an attribute of the node in the XML.  Attribute must already exist in the XML node or an exception will be raised.  This method will only operate on the node element referenced by 'self'.  
ARGUMENT: attribute, value  
RETURN: none  
USAGE: self.set_element(\<attribute>, \<value>)  
```
from ThenWhatTree import ThenWhatTreeNode
class NODE_A(ThenWhatTreeNode):

    def is_true(self):
        self.set_element('my_xml_attribute', 'my_value')
        **Insert user code to evaluate whether NODE_A should return True or False**
        return True
```

*get_element(\<attribute>)*
------------------------
Method provided to get attributes of the node from the XML.  Attribute must already exist in the XML node or an exception will be raised.  
ARGUMENT: attribute  
RETURN: text of the \<attribute> in the XML  
USAGE: self.get_element(\<attribute>)
```
from ThenWhatTree import ThenWhatTreeNode
class NODE_A(ThenWhatTreeNode):

    def is_true(self):
        my_value = self.get_element('my_xml_attribute')
        **Insert user code to evaluate whether NODE_A should return True or False**
        return True
```


Getting started
------------------
The first step is to create a block diagram of the decision tree.  Experience shows that this step comprises the majority of the work in the ThenWhatTree methodology.  To create a debug decision tree, a team needs to ask itself, 'How do we debug?'  Start with a single node on a whiteboard called 'Test failed' and begin the diagramming processs.  *"After the test failed, then what?"*

Drawing a block diagram is important for the following reasons.

1) When describing how to debug, engineers are generally unaware of the decision trees they have built in their heads.  Even proficient debuggers can struggle to describe how they work.
2) Engineers who believe they know how they work still tend to do a lot of hand waving as if they were conjuring a debug flow out of the air.
3) Drawing block diagrams removes both of these issues.  Putting pen to paper defines a flow that can be tested, followed, amended and extended.

Once the block diagram is created, the recommendation is to translate the diagram into CSV syntax.  Any column names added in the CSV become attribute fields in the XML.  Working with a tree in CSV allows for custom attribute values to be selectively added for each node that can then be accessed by the python node module.  Building decision tree nodes based on elements of a node's XML rather than hard coded values/signals gives a layer of abstraction that creates the opportunity for a macro libraries to be created thus reducing investment costs.

CSV schema and requirements:
----------------------------
1) The first line in a CSV file is required to have a 'name' and 'parent' column.
   -name: Entries in the 'name' column in a CSV file will become the module names in the python library created by 'generate.py’.
   -parent: ThenWhatTree assumes that a line is CSV file follows its parent.  If a node has multiple children, these can be identified by populating the 'parent' field.  Below is an example CSV file and the corresponding XML structure.
3) An entry in the 'name' column cannot have 'test' in its name.
2) All lines in the CSV must have at least as many entries as the first line.  If a line has fewer entries that columns an Exception will be raised.  Entries can be empty.

3) There are no limitations on the number of columns or the names of the columns.

Good:
```
name,parent,other,notes
node1,,,
```
Exception raised: *(node1 only has 3 entries while there are 4 column headers)*
```
name,parent,other,notes
node1,,
```
ThenWhatTree reserved name space
--------------------------------
The following names contain special meaning and are used by methods from ThenWhatTree scripts and plugin utilities.  All entries in one line of the CSV file are added as attributes of the node in the XML. These can be extracted in a ThenWhatTreeNode with the 'self.get_element(<attribute>)' method.

These reserved words should not be used as column headers in a CSV file or as elements in an XML file: *node, branch*


Example
----------
The following example includes:
  - Block diagram of a decision tree when your car won't start
  - The CSV representation of the same tree
  - The XML created using the **‘generate.py’** function
  - The output generated using the **‘execute_tree.py’** function

Block diagram
-------------
Decision tree block diagram that might be created on a whiteboard during a debug interview session when a car won't start.

```
                           +-------------------+       +---------------+
                           |                   |       |               |
                 +---------> engine turns over +-------> car needs gas |
+----------------+         |                   |       |               |
|                |         +-----------------+-+       +---------------+
| car wont start |                           | |
|                |                           | |
+----------------+   +-------------+         | |       +-----------------+        +--------------------+      +----------------+
                 |   |             |         | |       |                 |        |                    |      |                |
                 |   | engine does |         | +-------> battery voltage |        | voltage to starter |      | starter passes |
                 +--->   nothing   |         |         |   meets spec    +-------->     meets spec     +------>  diagnostics   |
                     |             |         |         |                 |        |                    |      |                |
                     ++-+----------+         |         +-----------------+        +--------------------+      +----------------+
                      | |                    |
                      | |                    |
                      | | +----------------+ |        +---------------+
                      | | |                | |        |               |
                      | | | battery is not | +--------> battery needs |
                      | +->   connected    |          |   charging    |
                      |   |                |          |               |
                      |   +----------------+          +---------------+
                      |
                      |       +------------+          +-----------------+       +---------------------+
                      |       |            |          |                 |       |                     |
                      |       | battery is |          | battery voltage |       | battery connections |
                      +-------> connected  +---------->   meets spec    +------->      are good       |
                              |            |          |                 |       |                     |
                              +------------+          +-----------------+       +---------------------+
```
CSV file:
---------
Here is shown the CSV representation of the block diagram shown above.  This content is copied from the ThenWhatTree/examples/car_wont_start/car_wont_start.csv file.
```
name,parent,notes
car wont start,,
engine turns over,,
car needs gas,,add gas if needed
battery voltage meets spec,engine turns over,
voltage to starter meets spec,,
starter passes diagnostics,,may need to remove starter to test this
engine does nothing,car wont start,
battery is not connected,,will need to reconnect battery if this step fails
battery is connected,engine does nothing,
battery voltage meets spec,,
battery connections are good,,may require professional service
battery needs charging,engine turns over,
```
Generated XML:
--------------
This content is copied from the ThenWhatTree/examples/car_wont_start/car_wont_start.xml file.  Below is the generated XML file created from the above CSV file using 'generate.py --csv <path to csv>'.  If the '-lib <full path to lib>' is also added then a python module is created each <node>.
```
<?xml version="1.0" ?>
<node>
    <name>car_wont_start</name>
    <parent/>
    <notes/>
    <node>
        <name>engine_turns_over</name>
        <parent/>
        <notes/>
        <node>
            <name>car_needs_gas</name>
            <parent/>
            <notes>add gas if needed</notes>
        </node>
        <node>
            <name>battery_voltage_meets_spec</name>
            <parent>engine_turns_over</parent>
            <notes/>
            <node>
                <name>voltage_to_starter_meets_spec</name>
                <parent/>
                <notes/>
                <node>
                    <name>starter_passes_diagnostics</name>
                    <parent/>
                    <notes>may need to remove starter to test this</notes>
                </node>
            </node>
        </node>
        <node>
            <name>battery_needs_charging</name>
            <parent>engine_turns_over</parent>
            <notes/>
        </node>
    </node>
    <node>
        <name>engine_does_nothing</name>
        <parent>car_wont_start</parent>
        <notes/>
        <node>
            <name>battery_is_not_connected</name>
            <parent/>
            <notes>will need to reconnect battery if this step fails</notes>
        </node>
        <node>
            <name>battery_is_connected</name>
            <parent>engine_does_nothing</parent>
            <notes/>
            <node>
                <name>battery_voltage_meets_spec</name>
                <parent/>
                <notes/>
                <node>
                    <name>battery_connections_are_good</name>
                    <parent/>
                    <notes>may require professional service</notes>
                </node>
            </node>
        </node>
    </node>
</node>
```
Example output:
---------------
The node library for this XML was created in the ThenWhatTree/examples/car_wont_start directory.  Some of the 'is_true' methods were populated to return 'True', 'False' or an exception.  Below is an example of the 'execute_tree.py --xml <path to XML>' utiliy.  Nodes that return an exception are treated as 'False' for the purpose of the tree walking algorithm.

In a non-contrived example, the 'is_true' method in each node is expected to be python code that discovers the appropriate data sufficient to return 'True' or 'False' for the given node.
```
[0] car_wont_start : true
    [1] engine_turns_over : true
        car_needs_gas : false
        [2] battery_voltage_meets_spec : true
            [3] voltage_to_starter_meets_spec : true
                [4] starter_passes_diagnostics : true
        battery_needs_charging : ZeroDivisionError('division by zero',)
    engine_does_nothing : NotImplementedError

Node output:
------------
[0] car_wont_start is true
[1] engine_turns_over is true
[2] battery_voltage_meets_spec is true
[3] voltage_to_starter_meets_spec is true
[4] may need to remove starter to test this

Exceptions:
-----------
battery_needs_charging: ZeroDivisionError('division by zero',)
engine_does_nothing: NotImplementedError

Exception traceback:
--------------------
battery_needs_charging: ['  File "/nfs/pdx/home/ewberg/.local/lib/python3.6/site-packages/ThenWhatTree-1.0-py3.6.egg/ThenWhatTree/lib/twt_node/ThenWhatTreeNode.py", line 80, in evaluate_node_is_true\n    node_is_true = str(self.is_true()).lower()\n', '  File "/nfs/pdx/disks/ccdo.val.work.341/valid/work/ThenWhatTree/source/ThenWhatTree/examples/car_wont_start/battery_needs_charging.py", line 12, in is_true\n    return 1/0\n']
```
