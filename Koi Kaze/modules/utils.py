import sys
import vapoursynth as vs
import havsfunc as haf
import lvsfunc as lvf

this = sys.modules[__name__]
this.c = None

def init(vs_core):
	this.c = vs_core

def scenefilter_interlaced_fade(clip, start_frame, end_frame, use_vinverse=False, vinverse_amnt=1.5):
	if use_vinverse:
		fixed_fade_clip = haf.Vinverse(clip, amnt=vinverse_amnt)
	else:
		fixed_fade_clip = lvf.deinterlace.fix_telecined_fades(clip, thr=10)
	return c.std.Trim(clip, 0, start_frame - 1) + c.std.Trim(fixed_fade_clip, start_frame, end_frame) + c.std.Trim(clip, end_frame + 1)

def decomb_clip_mask(clip, mask_file, start_frame, end_frame):
	combmask = c.resize.Point(c.lsmas.LWLibavSource(source='./combmasks/' + mask_file), format=vs.GRAY8, matrix_s="170m").std.Binarize(180, v0=0, v1=255)
	decombed_clip = c.tdm.TDeintMod(clip, order=1, edeint=c.nnedi3.nnedi3(clip, field=1))
	merged_clip = c.std.MaskedMerge(clip, decombed_clip, combmask)
	return c.std.Trim(clip, 0, start_frame - 1) + c.std.Trim(merged_clip, start_frame, end_frame) + c.std.Trim(clip, end_frame + 1)

def merge_clips_mask(clip1, clip2, mask_file, start_frame, end_frame):
	combmask = c.resize.Point(c.lsmas.LWLibavSource(source='./combmasks/' + mask_file), format=vs.GRAY8, matrix_s="170m").std.Binarize(180, v0=0, v1=255)
	merged_clip = c.std.MaskedMerge(clip1, clip2, combmask)
	return c.std.Trim(clip1, 0, start_frame - 1) + c.std.Trim(merged_clip, start_frame, end_frame) + c.std.Trim(clip1, end_frame + 1)