import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import havsfunc as haf

DEBUG_MODE = False
	
def manual_smartfademod(clip, start_frame, end_frame):
	fixed_fade_clip = haf.smartfademod(clip, tff=True, threshold=0)
	return core.std.Trim(clip, 0, start_frame - 1) + core.std.Trim(fixed_fade_clip, start_frame, end_frame) + core.std.Trim(clip, end_frame + 1)
	
def replace_frame_with_previous(clip, frame):
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(clip, frame - 1, frame - 1) + core.std.Trim(clip, frame + 1)
	
def replace_frame_with_next(clip, frame):
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(clip, frame + 1, frame + 1) + core.std.Trim(clip, frame + 1)
	
def ivtc_clip_ovr(clip):
	matched_clip = core.vivtc.VFM(clip, 1)
	if DEBUG_MODE:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_16_vdecimate_override.txt', dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, ovr='./decimate_overrides/ep_16_vdecimate_override.txt', dupthresh=2.0)
		
def ivtc_clip(clip):
	matched_clip = core.vivtc.VFM(clip, 1)
	if DEBUG_MODE:
		return core.vivtc.VDecimate(matched_clip, dupthresh=2.0, dryrun=True)
	else:
		return core.vivtc.VDecimate(matched_clip, dupthresh=2.0)

def filter_clip(clip, is_nced = False):
	filterable_clip = fvf.Depth(clip, 16)
	if is_nced:
		cropped_clip = core.std.Crop(filterable_clip, bottom=2, top=2, left=4, right=2)
	else:	
		cropped_clip = core.std.Crop(filterable_clip, top=4, left=4, right=2)
	filtering_done_clip = fvf.Depth(cropped_clip, 8)				
	return filtering_done_clip;
	
def decomb_clip_whole_frame(clip, frame, order=1):
	deint = core.tdm.TDeintMod(clip, order=order, edeint=core.nnedi3.nnedi3(clip, field=order))
	return core.std.Trim(clip, 0, frame - 1) + core.std.Trim(deint, frame, frame) + core.std.Trim(clip, frame + 1)

source = core.lsmas.LWLibavSource(source='/home/wyse/Videos/NHK_NI_YOUKOSO_01/nhk_ep_16.mkv')
decimated_clip = ivtc_clip_ovr(source)	
filtered_clip = filter_clip(decimated_clip)
filtered_clip = replace_frame_with_next(filtered_clip, 323)
filtered_clip = replace_frame_with_previous(filtered_clip, 2264)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4888)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4890)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4892)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4894)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4896)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4898)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4900)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4902)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4906)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4908)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4911)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4914)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 4916)
filtered_clip = replace_frame_with_next(filtered_clip, 6198)
filtered_clip = replace_frame_with_next(filtered_clip, 6209)
filtered_clip = replace_frame_with_next(filtered_clip, 6221)
filtered_clip = replace_frame_with_previous(filtered_clip, 6257)
filtered_clip = replace_frame_with_previous(filtered_clip, 8028)
filtered_clip = replace_frame_with_previous(filtered_clip, 8867)
filtered_clip = replace_frame_with_previous(filtered_clip, 9743)
filtered_clip = replace_frame_with_previous(filtered_clip, 10501)
filtered_clip = replace_frame_with_next(filtered_clip, 12480)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13320)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13323)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 13326)
filtered_clip = replace_frame_with_previous(filtered_clip, 13765)
filtered_clip = replace_frame_with_previous(filtered_clip, 13777)
filtered_clip = replace_frame_with_next(filtered_clip, 16443)
filtered_clip = replace_frame_with_previous(filtered_clip, 17310)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17920)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17921)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17922)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17924)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17925)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17926)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17928)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17929)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17930)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17934)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 17935)
filtered_clip = replace_frame_with_previous(filtered_clip, 18846)
filtered_clip = replace_frame_with_previous(filtered_clip, 18849)
filtered_clip = replace_frame_with_previous(filtered_clip, 18789)
filtered_clip = replace_frame_with_next(filtered_clip, 18856)
filtered_clip = replace_frame_with_previous(filtered_clip, 19658)
filtered_clip = replace_frame_with_next(filtered_clip, 20138)
filtered_clip = replace_frame_with_previous(filtered_clip, 20209)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 21218)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 21220)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 21222)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 21224)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 21226)
filtered_clip = decomb_clip_whole_frame(filtered_clip, 21227)
filtered_clip = replace_frame_with_previous(filtered_clip, 33806)
filtered_clip = replace_frame_with_next(filtered_clip, 33838)

# Manual Smartfademod Start
fadefixed_clip = manual_smartfademod(filtered_clip, 2701, 2718)
fadefixed_clip = manual_smartfademod(filtered_clip, 4885, 4919)
fadefixed_clip = manual_smartfademod(filtered_clip, 13204, 13239)
fadefixed_clip = manual_smartfademod(filtered_clip, 13305, 13329)
fadefixed_clip = manual_smartfademod(filtered_clip, 14620, 14643)
fadefixed_clip = manual_smartfademod(filtered_clip, 15215, 15246)
fadefixed_clip = manual_smartfademod(filtered_clip, 17925, 17972)
fadefixed_clip = manual_smartfademod(filtered_clip, 22412, 22423)
output_clip = manual_smartfademod(filtered_clip, 26005, 26026)
# Manual Smartfademod End

output_clip = fvf.Depth(output_clip, 10)

if DEBUG_MODE:
	output_clip = core.text.FrameProps(output_clip, props=['VDecimateDrop'])

output_clip.set_output()