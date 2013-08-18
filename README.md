# Aery32 Sublime Text plug-in

A convenient way to start new projects. Shortcut keys for program uploading (board flashing).
Also supports code complete.

Works on [Sublime Text](https://www.sublimetext.com/) 2 and 3.

## Installation

**Prerequisites**

- Make sure that you have installed [AVR32 Toolchain](http://www.atmel.com/tools/ATMELAVRTOOLCHAINFORWINDOWS.aspx).
  The plug-in assumes that the toolchain is set in PATH.

**Installation via Package Control (recommended)**

First make sure that you have a [Package Control plug-in](https://sublime.wbond.net/installation)
installed. After then ...

- Press `CTRL+SHIFT+P`, type `install` and press enter.
- Select `Aery32` from the list and press enter.
- Done.

**Manual installation**

Download and unzip, or git clone, the plug-in into `Packages/Aery32`
folder. To access `Packages` folder open ST2/3 and select
*Preferences - Browse packages...* Note that Aery32 plug-in can't be
installed in the Sublime Text 3 way to the `Installed Packages` folder.

## Usage

Press `CTRL+SHIFT+P` to bring the command palette into view. Next type
*aery32* and select a command which to run.

- __Create new project__: Prompts the directory where to create a new project.
  After then downloads the Aery32 Framework in to that directory and sets up
  the `aery32.sublime-project` file. When done you can open the project file
  located under the directory where ever you created the project. To do that
  select *Project - Open projects...*, browse to the project folder and double
  click `aery32.sublime-project` file.
- __Setup SublimeClang for current project__: Sets up the SublimeClang
  settings for the current open project. You may like to run this command if
  you had not created a project with the _create new project_ command, or if
  the current SublimeClang settings set in the project file do not work,
  e.g in case when the path to the AVR32 toolchain has been changed.
- __Fix Hudson problem__: Painless way to fix the so call Hudson problem.
  This problem rises from the fact that Atmel failed to strip the .o and .a
  files when building the AVR libraries with the Hudson CI tool. Note that in
  Windows you most likely need to start Sublime Text in administrator mode to
  have access to change the installed AVR library files. Similarly in Linux
  or Mac OS X you may need root access.

## Settings

You can edit settings from *Preferences - Package Settings - Aery32*.

- __mpart__: MCU part name. Change this to uc3a1128 if you are using Rev. 0 boards.
- __download_url__: URL where Aery32 Framework is downloaded from.
- __strip__: Post processing... list of files and directories, which
  you want to remove from the created project. Commonly the files, which
  are included in the Aery32 Framework but which you don't care to include
  in your project.

## Plug-in Dependencies

Aery32 plug-in is dependent of two other Sublime Text plug-ins, which are
needed: SublimeClang and Nettuts+ Fetch, `SublimeClang-18082013.sublime-package`
and `NettutsFetch-2.0.0.sublime-package` files respectively. The package file
name can vary according to the version number.

The dependent plug-ins will be installed automatically by the Aery32 plug-in
if needed. So if you pre-install these plug-ins Aery32 plug-in won't overwrite
or modify your installations.

## License

This Aery32 Sublime Text plug-in is licensed under the new BSD license:

> Copyright (c) 2012-2013, Muiku Oy
> All rights reserved.
>
> Redistribution and use in source and binary forms, with or without modification,
> are permitted provided that the following conditions are met:
>
>    * Redistributions of source code must retain the above copyright notice,
>      this list of conditions and the following disclaimer.
>
>    * Redistributions in binary form must reproduce the above copyright notice,
>      this list of conditions and the following disclaimer in the documentation
>      and/or other materials provided with the distribution.
>
>    * Neither the name of Muiku Oy nor the names of its contributors may be
>      used to endorse or promote products derived from this software without
>      specific prior written permission.
>
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
> ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
> WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
> DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
> ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
> (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
> LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
> ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
> (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
> SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

SublimeClang is licensed under the zlib:

> Copyright (c) 2011-2012 Fredrik Ehnbom
>
> This software is provided 'as-is', without any express or implied
> warranty. In no event will the authors be held liable for any damages
> arising from the use of this software.
>
> Permission is granted to anyone to use this software for any purpose,
> including commercial applications, and to alter it and redistribute it
> freely, subject to the following restrictions:
>
>   1. The origin of this software must not be misrepresented; you must not
>   claim that you wrote the original software. If you use this software
>   in a product, an acknowledgment in the product documentation would be
>   appreciated but is not required.
>
>   2. Altered source versions must be plainly marked as such, and must not be
>   misrepresented as being the original software.
>
>   3. This notice may not be removed or altered from any source
>   distribution.

Nettuts+ Fetch license is unkown:

> ...
