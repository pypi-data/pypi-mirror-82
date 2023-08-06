# Blackout Nexus Node for Python

![Blackout logo](https://www.blackout.ai/wp-content/uploads/2018/08/logo.png)

|||
|---|---|
|Author|Adrian Lubitz|
|Author|Marc Fiedler|
|Email|dev@blackout.ai|
|Required Instance versions| >= 3.0|
|Runs on|Python 2.7+ or Python 3.6+|
|State|`Stable`|

# Prerequisites

* Python installed (either 2.7+ or Python 3.6+)
* Owner of a btNexus instance or a btNexus account

# Install btnexus-node-python
```
pip install btnexus-node-python
```
If you need to install a specific version use
```
pip install btnexus-node-python==[VERSION]
```

# API Documentation
You find an API Documentation our [GitHub Page](https://blackout-technologies.github.io/btnexus-node-python/6.3.233)


# Introduction

The `nexus` by Blackout Technologies is a platform to create Digital Assistants and to connect them via the internet to multiple platforms. Those platforms can be websites, apps or even robots. The `nexus` consists of two major parts, first being the `btNexus` and second the nexusUi. The `btNexus` is the network that connects the A.I. with the nexusUi and the chosen interfaces. The nexusUi is the user interface, that allows the user to create their own A.I.-based Digital Assistant. Those Digital Assistants can be anything, support chatbots or even robot personalities.   
Every user has one or multiple nexusUi instances or short nexus instances, which means, it's their workspace. One nexusUi / nexus instance can host multiple personalities.

Every part of the `btNexus` is a Node. These Nodes can react on messages and send messages through the `btNexus`. To understand how Nodes work the following key concepts need to be clear.

## Nodes
Nodes are essentially little programs. It is not important in which language these programs are implemented.
More important is that they share `Messages` between them in certain `Groups` and `Topics`.
So every node has its very unique purpose. It reacts on `Messages` with a `Callback` which is subscribed to a `Group` and a `Topic`
and also sends `Messages` to the same and/or other `Group` and `Topic` to inform other `Nodes`, what is happening.

## Messages
`Messages` are the media of communication between `Nodes`.
A `Message` contains a name for a `Callback` and the corresponding parameters.
A `Message` is send on a specific `Group` and `Topic`, so only `Callbacks` that subscribed to this `Group` and `Topic` will react.

## Callbacks
`Callbacks` are functions which serves as the reaction to a `Message` on a specific `Topic` in a specific `Group`.
Every `Callback` returns a `Message` to the `btNexus` with the name of the origin `Callback` + `_response`. So a `Node` can also subscribe to the response of the `Message` send out.

## Topics & Groups
`Topics` and `Groups` help to organize `Messages`. A `Callback` can only be mapped to one `Group` and  `Topic`.





# Example Nodes
Following you will see an example of a Node which sends out the current minute
and second every five seconds.

```python
"""Example for a Node that sends out messages"""
# System imports
from threading import Thread
import datetime
import time
import os
# 3rd party imports
from btNode import Node

# local imports

class SendingNode(Node):
    """
    This Node shows how to implement an active Node which sends different Messages
    """
    def onConnected(self):
        """
        This will be executed after a the Node is succesfully connected to the btNexus
        Here you need to subscribe and set everything else up.

        :returns: None
        """
        self.shouldRun = True
        self.subscribe(group="exampleGroup",topic="example", callback=self.fuseTime_response) # Here we subscribe to the response of messages we send out to fuseTime
        self.thread = Thread(target=self.mainLoop)
        self.thread.start() # You want to leave this method so better start everything which is actively doing something in a thread.
    def fuseTime_response(self, orignCall ,originParams, returnValue):
        """
        Reacting to the fused Time with a print in a specific shape.
        responseCallbacks always have the following parameters.

        :param orignCall: The name of the orignCall
        :type orignCall: String
        :param originParams: The parameters given to the orignCall
        :type originParams: List or keywordDict
        :param returnValue: The returned Value from the orignCall
        :type returnValue: any
        :returns: None
        """
        print("[{}]: {}".format(self.__class__.__name__, returnValue))

    def mainLoop(self):
        """
        Sending currenct minute and second to the ListeningNode on the printMsg and fuse callback.

        :returns: Never
        """
        #Make sure the thread terminates, when reconnecting
        #otherwise onConnected will spawn another
        #and you will end up with n threads, where n is the number of connects
        while(self.shouldRun):
            now = datetime.datetime.now()
            self.publish(group="exampleGroup", topic="example", funcName="printTime", params=[now.minute, now.second])
            self.publish(group="exampleGroup", topic="example", funcName="fuseTime", params={"min":now.minute, "sec":now.second})
            time.sleep(5)

    def cleanUp(self):
        """
        Make sure the thread terminates, when reconnecting
        otherwise onConnected will spawn another
        and you will end up with n threads, where n is the number of connects
        """
        super(SendingNode, self).cleanUp()
        self.shouldRun = False
        try:
            self.thread.join()
        except AttributeError:
            pass # This only happens if onConnected was never called before - Node was never connected correctly and therefore closes the connection and calls the cleanUp


if( __name__ == "__main__" ):
    #Here you initialize your Node and run it.
    sendingNode = SendingNode() # CONNECT_HASH needs to be in .btnexusrc or environment variable CONNECT_HASH
    sendingNode.connect() # This call is blocking


```
The ListeningNode and all further examples can be seen in the examples folder.


# Implement your own Node
First you need know the purpose of your Node.
Nodes should be small and serve only one purpose.
To implement your own Node you need to inherit from the Node class,
implement your callbacks and if you are actively doing something implement your
Threads, that for example read in sensor data. See the examples to get started ;)
Keep in mind, that you need to set the `CONNECT_HASH` in your `.btnexusrc` or the environment variable `CONNECT_HASH`. If you are using Anaconda you can integrate those into your virtual environment(https://conda.io/docs/user-guide/tasks/manage-environments.html#saving-environment-variables).


# Changelog
* Since Version 4 the protocol was changed to completely use [socketIO](https://pypi.org/project/python-socketio/) - Therefore it only works with **Dynamic Davinci** *(Instance Version 2.2)*
* Since Version 5, Nodes and all inheriting classes (Hooks, Integrations) use a `CONNECT_HASH` which can be obtained from the Instance and should be given in the file `.btnexusrc` or the environment variable `CONNECT_HASH` *(The latter overwrites the first)*. Additionally a `package.json` file is needed. It should be minimal the following:

    ```json
    {
        "name": "test",
        "title": "Test",
        "description": "This is just a test",
        "type": "integration",
        "keywords": [
            "test",
            "testing"
        ],
        "version": "0.2.3",
        "nexusVersion": "2.2",
        "license": "See attached LICENSE file",
        "author": {
            "name": "Adrian Lubitz",
            "url": "https://blackout.ai/",
            "email": "al@blackout.ai"
        }
    }
    ```
* Since Version 6 all Nodes are able to connect to 3.0 Instances 

