#!/bin/bash
../gcc-linaro-aarch64-linux-gnu-4.9-2014.07_linux/bin/aarch64-linux-gnu-as one.s -o one
python reading_elf.py one
