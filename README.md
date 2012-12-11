# Aery32 Sublime Text 2 plug-in

## Installation

**Via package control (recommended)**

First make sure that you have a [Sublime Text 2 package control plug-in](http://wbond.net/sublime_packages/package_control) installed.

After then:

- Press `CTRL+SHIFT+P`, type install and press enter.
- Select Aery32 from the list and press enter.

**Manual installation**

Download and unzip, or git clone, the plug-in into `Sublime Text 2/Packages/Aery32` folder. To access this folder open ST2 and select *Preferences - Browse packages...*

## Usage

Press `CTRL+SHIFT+P` to bring the command palette into view. Next type *Aery32* and select a command which to run.

- **Create new project**:
  - Prompts the directory where to create a new project. After then downloads the Aery32 Framework in to that directory and sets up the `aery32.sublime-project` file. When done you can open the project file located under the directory where ever you created the project. To do that select *Project - Open projects...*, browse to the project folder and double click `aery32.sublime-project` file. In case you want to disable the code autocomplete, open the project's sublime-project file and set `sublimeclang_enabled` false.

Aery32 plug-in also has hidden commands that are supportive kind and thus not accessable through the command palette. To run a hidden command open Sublime Text 2's Console window and write `window.run_command("cmd")` where `cmd` is the command which to run.

- **aery_fix_hudson**:
  - Painless way to fix the so call Hudson problem. This problem rises from the fact that Atmel failed to strip the .o and .a files when building the AVR libraries with the Hudson CI tool. Note that in Windows you most likely need to start ST2 in administrator mode to have access to change the installed AVR library files. Similarly in Linux or Mac OS X you may need root access.

## Settings

You can edit settings from *Preferences - Package Settings - Aery32*.

- **download_url**:
  - URL where to download Aery32 Framework.
- **strip**:
  - List of files and directories, which are included in the Aery32 framework but you don't care to include in your project.
- **mpart**:
  - MCU part name

## Prerequisites

**!! The plug-in assumes that the AVR 32-bit Toolchain is set in PATH.**

Additionally two other Sublime Text 2 plug-ins are needed: SublimeClang and Nettuts+ Fetch. However, these will be automatically installed by the sublime-aery32 plug-in if needed.

## License

This Aery32 Sublime Text 2 plug-in is licensed under the new BSD license:

> Copyright (c) 2012, Muiku Oy
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