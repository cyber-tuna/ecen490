# Note

As discussed in our final report, we used a python publisher/subscriber model in our system architecture. The publisher code exists in the vision code. Therefore, the Publisher directory in this folder does not contain any code used in our final robot, but does provide a working example of a python pusblisher and could therefore be valueable. 

hwclient.py and hwserver.py contain experimental code using MessagePack (see [final report](https://docs.google.com/document/d/1zPuirr4RUlu7Rpwbm5eCCrRhRDmRNydvPN5fMtpG1pc/edit)). These two files were not used in our final implementation, but could provide a good starting point for teams wishing to use MessagePack for object serialization.

The Subscriber director contains the main program for our robot. sub.py is the main execution loop, and running "python sub.py" will begin execution of the main program. Kill.py was created as a quick script to kill (stop it's movement) if the robot ever got into an uncontrollable state. reset.py simply instructs the robot to move to it's starting position on the field. 
