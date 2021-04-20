import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf


clip = core.lsmas.LWLibavSource(source='/media/wyse/Media III/[BDMV] Spice and Wolf Blu-ray BOX Complete Edition R2J/[BDMV][130306] Spice and Wolf Disc1/BDMV/STREAM/00004.m2ts')
clip = core.std.Trim(clip, 34046)
clip = fvf.Depth(clip, 10)
clip.set_output()