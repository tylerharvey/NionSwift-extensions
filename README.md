# NionSwift-extensions

io_ser: to use this tool to import TIA .ser format images into Nion Swift, place this folder in the PlugIns folder of your Nion Swift directory and then run Swift, like any other Nion Swift extension (https://github.com/nion-software/extensions).

If Swift is properly installed, you should be able to import .ser files in the UI with the import dialog under File -> Import...

Tested and works for 1D collections of 2D CCD acquisitions (e.g. a line-scan of diffraction images in STEM) and single EELS spectra; not fully functional for 2D collections of 2D CCD acquisitions and untested for collections of EELS spectra.

(adapted from https://bitbucket.org/linoleum13/openncem/src)


