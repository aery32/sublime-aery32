## Aery32 Sublime Text 2 plug-in

### Prerequisites

The plugin assumes that the AVR 32-bit Toolchain is set in PATH. Additionally few Sublime Text 2 plugins are needed and will be automatically installed if not present: SublimeClang and Nettuts+ Fetch.

### Installation

...

### Supported commands

- __Create new project__: Prompts the directory where to create a new project. Then fetches Aery32 Framework in to that directory and sets up the Aery32.sublime-project file.

### Settings

- __download_url__: Url where to download Aery32 Framework.
- __strip__: List of files and directories which are to be omitted from the Aery32 Framework.

This plugin enables code autocompletion by default. If you don't want to use that, it can be disabled by editing Aery32.sublime-project file. Just set sublimeclang_enabled to false.

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