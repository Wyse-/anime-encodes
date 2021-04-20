import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf


clip_part1 = core.lsmas.LWLibavSource(source='/media/wyse/Media III/[BDMV] Spice and Wolf II/Disc 5/00004.m2ts')
clip_part2 = core.lsmas.LWLibavSource(source='/media/wyse/Media III/[BDMV] Spice and Wolf II/Disc 5/00005.m2ts')
clip = clip_part1 + clip_part2
clip = fvf.Depth(clip, 10)
clip.set_output()