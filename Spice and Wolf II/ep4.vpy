import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf


clip_part1 = core.lsmas.LWLibavSource(source='/media/wyse/Media III/[BDMV] Spice and Wolf II/Disc 6/00009.m2ts')
clip_part2 = core.lsmas.LWLibavSource(source='/media/wyse/Media III/[BDMV] Spice and Wolf II/Disc 6/00010.m2ts')
clip = clip_part1 + clip_part2
clip = fvf.Depth(clip, 10)
clip.set_output()