# Introduction
Use python to find THREADSTACK address in CheatEngine.

# How to use
Just clone it and install pythonforwindows.
```
pip install pythonforwindows
```
More infomation about pythonforwindows: https://github.com/hakril/PythonForWindows and https://pypi.org/project/PythonForWindows/

# Implementation
Before us talk to implementation, we must know what is THREADSTACK mean in CheatEngine. Fortunately In CheatEngine forum, there are many discussions about this, thus I won't go into details here.  
<br>
https://forum.cheatengine.org/viewtopic.php?p=5638945 you can find good answer in user MakeMEK's Reply.  
<br>
https://forum.cheatengine.org/viewtopic.php?p=5487976 site admin Dark Byte described the implementation process.  
<br>
https://forum.cheatengine.org/viewtopic.php?t=570862&sid=dcc003718f32d2a18c46da29ba26f0fb also site admin Dark Byte's answer, recommend that we should avoid to use THREADSTACK, and find other way to get game address.  
<br>
In breif, THREADSTACK is a pointer in Thread, and pointed to a kernel32.dll function Exitthread address. In 32bitness process, it point to BaseThreadInitThunk address.  
<br>
So, If we wanna implement this,  we must invoke windows api, and I done this via third patry named pythonforwindows.

# Question
+ I just test my code in my 64bit windows, running 32bit and 64bit process,  It seems good now, at lease it get THREADSTACK0 address correctly. So there may some problem in other situation.
+ There is a strange place in my code:  
```
if target_process.is_wow_64:
  teb = teb + 0x2000
```
When process run into wow64, I find that teb value get from thirdpary and the real teb value difference of 0x2000, I have issued it: https://github.com/hakril/PythonForWindows/issues/41
