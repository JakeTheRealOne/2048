# How to create a theme:
1. Each theme is represented by a single file in the ```themes``` subdir
2. The name of the themes is the name of its file:
#
    \<name\>.dmqu
3. Each line of a them file represent a tile colors (in order: line 0 = no tile, line 1 = tile 2 etc.):
#
    <background_color>, <font_color>
4. Please follow the csv format to encode the colors (each color separated by ```, ```)
5. the base theme is available at ```themes/base.dmqu```
6. The limit for the file is 17 lines (see ```themes/ORDER.md``` for the order of tile colors)