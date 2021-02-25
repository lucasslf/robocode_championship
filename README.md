# robocode_championship
This is a side project to practice different concepts. It is a system to manage Robocode tournaments. 

Currently only backend. 


## robot-service

API - Basic CRUD - Relational DB - Kafka - Python

Responsible for the robot catalog.
Sends events after changing robot states

Next steps:

- Add robot states
- Add ELO Rating


## championship-service

API - Event sourcing - Kafka - Python

Responsible for Championships capabilities.
* Set up a Championship
1. robot-service validate robots after championship created event
2. championship is ready to be started after "Championship Validated" event
* Start a Championship

Next steps:

- Add current state projection stored in mongodb
- Trigger championship finished event when last battle finishes
- Add queries for chapionship results and statistics
- Add battle state projection stored in mongodb 

## battle-service

Event driven - Document DB - Kafka - Spring/spring-boot - Java

Responsible for running battles on Robocode. It runs a battle at a time when it detects a battle created event.
It downloads the Robots to store them in the Robocode local storage when it detects a Robot Created event.

Next steps:

- Error handling
- Send robot downloaded event

## robocode-battle-runner

Pure Java - Robocode

Wrapper around Robocode, it is necessary because Robocode needs to run as a stand alone process due to it having its own classloader and it not working well with spring-boot's class loader.

---

General roadmap:

- Ranking Service: general ranking independent of championship with general statistics about the robots
- Possibly add a frontend
- Users and auth?
