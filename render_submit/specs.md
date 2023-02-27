# Brainstorm

A tool to automatically submit a list of files to the farm.
Could get files to process and options from a .json file
Could store overrides for in/out points, fallback to timeline in/out
Presets for preview and final
Assemble the files into a movie at the end.

# Pieces

- Core submission: Zach already has a bunch of this working, but will cleanup for this.
- Main loop: see old version in `renderShot.py`
- Unfortunately, shot list isn't managed by a pipe, so it will be more complicated to build.
- We can use pdplayer commandline to assemble shots or even nuke standalone. Probably clean this up as a dependent farm job in main submission.

# Steps
1. Build test data @saul
   1. Create 3 maya files that are ready to render
   2. Place paths in a .json file manually
   3. Think about structure, dict of dicts
      1. ID
      2. Filename
      3. Filepath
      4. Outfile
      5. Preview/Final
      6. cut in
      7. cut out
   4. What is the unique key?
2. Work on render loop @Kaleb @Jeremy
   1. Load the json
   2. Submit each using zach's vss
   3. Yield info that can be used in progress window
   4. Allow cancellation
3. File grepper @Nathan
   1. Given a directory, go find all the ma/mb files recursively
      1. path
      2. file
      3. date
      4. size
   2. Allow to filter by recent or keyword @Ella
      1. sort the list
         1. date
         2. size
         3. name
         4. path
      2. filter the list if it contains a particular string
   3. Return a list of files
1. File selector - @Raphiel @Rileigh
   1. Given an existing file dict integrate new info
   2. functions for
      1. adding
      2. removing
      3. skipping
   3. Look up REST API, consider packages to do this
2. UI - @Ada mockup, then build dead forms
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
# Moved movie submission to the farm!

```



