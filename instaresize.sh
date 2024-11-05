#!/bin/bash
# Uses ImageMagick to convert an image file
# into a JPEG file, 1080 by 1080 pixels and padded
# with black, that can  be easily used on Instagram
#
# Usage:
#    instaresize.sh "file to convert.ext"
#
# Output:
#    resized file called "file to convert_instasize.jpg"

if [ -z "$1" ]
then echo No photo file designated
else
    filename=$1
    basefilename="${filename%.*}"
	convert "$filename" -resize 1080x1080 -gravity center -background "rgb(0,0,0)" -extent 1080x1080 "$basefilename"_instasize.jpg
fi
