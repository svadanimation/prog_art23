# Brainstorm

A tool to automatically submit a list of files to the farm.
Could get files to process and options from a .json file
Could store overrides for in/out points
Presets for preview and final
Assemble the files into a movie at the end.

# Pieces

- Core submission: Zach already has a bunch of this working, but will cleanup for this.
- Main loop: see old version in `renderShot.py`
- Unfortunately, shot list isn't managed by a pipe, so it will be more complicated to build.
- We can use pdplayer commandline to assemble shots or even nuke standalone. Probably clean this up as a dependent farm job in main submission.

# Steps
1. Build test data
   1. Create 3 maya files that are ready to render
   2. Place paths in a .json file manually
   3. Think about structure, dict of dicts
   4. What is the unique key?
2. Work on render loop
   1. Load the json
   2. Submit each using zach's vss
   3. Yield info that can be used in progress window
3. File grubber
   1. Given a directory, go find all the ma/mb files recursively
   2. Allow to filter by recent or keyword
   3. Return a list of files
4. File selector
   1. Given an existing file dict integrate new info
   2. functions for
      1. adding
      2. removing
      3. skipping
      4. sorting
5. UI
   1. create a shot data file
   2. load a shot data file
   3. display shot data in a table
   4. select line
      1. set skip state
      2. delete
      3. set preview flag
   5. show new files
      1. option to add




```
#It's important that the machines have the correct codecs installed or the movie conversion will fail
        pdplayercmd = ('%s %s \
--force_sequence \
--alpha=ignore \
--color_space=%s \
--exposure=0 \
--soft_clip=0 \
--saturation=0 \
--transient \
--scale=100 --mask_size=1280,720 --mask_type=crop --fps=24 \
--save_mask_as_image=%s \
--save_mask_as_sequence=%s,mp4v,100 \
--exit'
            % (PDPLAYER,
            #input sequence
            #str(framePath.replace('#','*')),
            str(framePath.replace('#','*')),
            #str(os.path.normpath(LUT)),
            str(colorSpace),
            #thumbnail path
            str(basePath +  'thumb.jpg'),
            #movie path
            str(basePath + 'movie.mov')
            ))        
            ```



