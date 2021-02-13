# Python is fucking slow, so let's do some magick
# Oh, well this idea was made by @MissJulia_Robot (so please remember his name)

# simple for loop
for file in $(find ./ -name '*.py'); do 
 cython --embed $file -3 -o $file
 # Now compiling the C files
 gcc `python3-config --cflags --ldflags` $file
done
