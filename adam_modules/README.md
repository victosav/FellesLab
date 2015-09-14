
Prettify:
* `python -m markdown README.md > README.html`

The Basics
==========


Changing Configuration to Modbus Protocol
=========================================

The *ADAM-4000* Modbus version modules may come from the factory set for which *ADAM ASCII* protocol are set as the **default** protocol. If the module is connected to a Modbus network, the Modbus network may not recognize the module. This may be caused by the incorrect settings. *ADAM-4000* module should be set-up for Modbus protocol instead of *ADAM ASCII* protocol. Please follow the steps as below for configuring an *ADAM-4000* module to Modbus protocol.  

1. Configure the *ADAM-4000* Module with the *ADAM-4000* utility (latest *ADAM-4000* utility can be found at [www.advantech.com](www.advantech.com) service & support.)
2. Initialize the *ADAM-4000* on a *RS-485* network (the preferred method is one module at a time on the *RS-485* network).
3. With the module powered off, turn the switch in the _"Init"_ position. (For some older Adam models, use an external wire to connect the **INIT*** terminal to the GND terminal)
4. Power up the module
5. Wait 10 seconds for the module to initialize.
6. Using the *ADAM-4000* utility, search (scan) for the module to change the protocol. (Initial *COM* settings: 9600 baud, N-8-1)
7. The utility will identify the module from the search function.
8. The *ADAM-4000* utility will now permit the serial data protocol to be changed to the Modbus protocol.
9. The address and *COM* port settings can also be changed at this time.
10. To access the module, click on the module icon in the utility.
11. Update the settings by pressing the _"Update"_ button.
12. Power off the module.
13. Turn the switch back to **NORMAL*** position. (For the older Adam models, remove the wire between the **INIT*** and *GND* terminals)
14. The module is now ready to be placed in the Modbus network.

Modbus
======

* Every device has a unique **address**
* 

Main Modbus exception codes
---------------------------

+----------------------------------------------------------------------------------------------------------------+
|Code   | Text                                    | Details                                                        |
|:-----:|-----------------------------------------|----------------------------------------------------------------|
|1      | Illegal Function                        | Function code received in the query is not recognized or allowed by slave |
|2      | Illegal Data Address                    | Data address of some or all the required entities are not allowed or do not exist in slave |
|3      | Illegal Data Value                      |  Value is not accepted by slave |
|4      | Slave Device Failure                    | Unrecoverable error occurred while slave was attempting to perform requested action |
|5      | Acknowledge                             | Slave has accepted request and is processing it, but a long duration of time is required. This response is returned to prevent a timeout error from occurring in the master. Master can next issue a Poll Program Complete message to determine if processing is completed |
|6      | Slave Device Busy                       | Slave is engaged in processing a long-duration command. Master should retry later
|7      | Negative Acknowledge                    | Slave cannot perform the programming functions. Master should request diagnostic or error |information from slave |
|8      | Memory Parity Error                     | Slave detected a parity error in memory. Master can retry the request, but service may be required on the slave device |
|10     | Gateway Path Unavailable                | Specialized for Modbus gateways. Indicates a misconfigured gateway |
|11     | Gateway Target Device Failed to Respond | Specialized for Modbus gateways. Sent when slave fails to respond  |
+--------------------------------------------------------------------------------------------------------------------+