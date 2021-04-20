import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf


clip = core.lsmas.LWLibavSource(source='/media/wyse/Media III/[BDMV] Spice and Wolf II/Disc 7/00001.m2ts')
clip = core.std.Trim(clip, 12, 2170)
clip = fvf.Depth(clip, 10)
clip.set_output()