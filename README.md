# Keyword Controller for Julius

This script allows the handling of a keyword inside the open source speech recognition engine Julius. That script use I/O redirection to grab the output of Julius.

## Requirements

* Computer (e.g. Ubuntu) with [Julius](http://julius.sourceforge.jp/en/)
* Microphone
* Grammar files:
  * Word Dictionary for N-gram and DFA (dictionary file)
  * HMMlist (Triphone model) to map logical phone to physical
  * Acoustic HMM definition file (ascii or Julius binary)
  * DFA grammar file

## Configuration

### Keyword

The Keyword is placed in `KeyCtrlJulius.json` file and can replaced with your own Keyword.
> **Note:** Dictionary and language model must contain the new Keyword

## Usage

The general syntax with jconf is:
```shell
julius | KeyCtrlJulius.py
```

without jconf configuration file:
```shell
julius -quiet -input mic
       -dfa /devel/acoustic_files/sample.dfa \
       -v /devel/acoustic_files/sample.dict \
       -h /devel/acoustic_model/hmmdefs \
       -hlist /devel/acoustic_model/tiedlist \
| python KeyCtrlJulius.py --debug
```

## License

The MIT License (MIT)

Copyright (c) 2015 Ronny Eisenkolb (@eisenkolb)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.