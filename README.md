# NionSwift-extensions

io_ser: to use this plug-in to import TIA .ser format images into Nion Swift, place this folder in the PlugIns folder of your Nion Swift directory and then run Swift, like any other Nion Swift extension (https://github.com/nion-software/extensions).

If Swift is properly installed, you should be able to import .ser files in the UI with the import dialog under File -> Import...

Tested and works for collections of 2D CCD acquisitions (e.g. a 1D or 2D scan of diffraction images in STEM) and single EELS spectra; untested for collections of EELS spectra, but theoretically works. Warning: loads all data in the .ser file into memory all at once, so be cautious with large datasets.

Please let me know if you find bugs.

(adapted from the folks at the National Center for Electron Microscopy https://bitbucket.org/linoleum13/openncem/src)

For more information on the .ser file format: http://www.er-c.org/cbb/info/TIAformat/
