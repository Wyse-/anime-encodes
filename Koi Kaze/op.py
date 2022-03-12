import vapoursynth as vs
from rekt import rektlvls
import havsfunc as haf
from modules import utils

wobbly_matches = 'ccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccccccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnnccccccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnnccccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccbcccccncncncncncncncncncncncncncncncncnncncncncncncncncncncnncncncncncncncncncncncncncncncncncncncncncncncnnncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncnncncncncncncncncncncncncncncncncncncncncncncncncncncncncccncncncncncncbccccnncccnncccnncccnncccnncccnncccnnccncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccbccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccbccccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnbcnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccbccnncccnncccnncccnncccnncccnncccnncccnncccnncccnnccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccbcnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnbccccccncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncncnncccncncncncncncncncncncncncnncncncncncncncncncncncncncncnncncncncncncncncncncncncncncncncncncncncncncnccncncncncncncncncncncncncncncnncncncncncncncncncncncncncncncnncncncncncncncncncncncncncncncncncncncncnccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnnccccnncccnncccnncccnncccnncccnncccnncccbcnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnnccncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnnccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnnccccccccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccbccccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccbcnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnncccnnccccc'

c = vs.core
utils.init(c)

src = c.d2v.Source(r'/home/wyse/vapoursynth-scripts/anime-encodes/Koi Kaze/d2v/R2J_DVD/DVD_01.d2v')
src = c.std.Splice(clips=[src[0:3000],])
src = c.fh.FieldHint(clip=src, tff=1, matches=wobbly_matches)
src_r1 = c.d2v.Source(r'/home/wyse/vapoursynth-scripts/anime-encodes/Koi Kaze/d2v/R1_DVD/DVD_01.d2v')
src_r1 = src_r1.resize.Point(range_in=1, range=0)
src_r1 = c.std.Splice(clips=[src_r1[0:3000],])
src_r1 = c.fh.FieldHint(clip=src_r1, tff=1, matches=wobbly_matches)

section0 = src[0:]
src = c.std.Splice(mismatch=True, clips=[section0,])
section0 = src_r1[0:]
src_r1 = c.std.Splice(mismatch=True, clips=[section0,])

dec0 = c.std.SelectEvery(clip=src[0:100], cycle=5, offsets=[0,1,2,4,])
dec100 = c.std.SelectEvery(clip=src[100:105], cycle=5, offsets=[0,2,3,4,])
dec105 = c.std.SelectEvery(clip=src[105:170], cycle=5, offsets=[0,1,3,4,])
dec170 = c.std.SelectEvery(clip=src[170:250], cycle=5, offsets=[1,2,3,4,])
dec250 = c.std.SelectEvery(clip=src[250:505], cycle=5, offsets=[0,1,2,4,])
dec505 = c.std.SelectEvery(clip=src[505:615], cycle=5, offsets=[0,1,2,3,])
dec615 = c.std.SelectEvery(clip=src[615:620], cycle=5, offsets=[0,1,2,4,])
dec880 = c.std.SelectEvery(clip=src[880:885], cycle=5, offsets=[0,2,3,4,])
dec885 = c.std.SelectEvery(clip=src[885:920], cycle=5, offsets=[0,1,3,4,])
dec920 = c.std.SelectEvery(clip=src[920:980], cycle=5, offsets=[1,2,3,4,])
dec980 = c.std.SelectEvery(clip=src[980:1155], cycle=5, offsets=[0,1,2,4,])
dec1155 = c.std.SelectEvery(clip=src[1155:1160], cycle=5, offsets=[0,1,3,4,])
dec1160 = c.std.SelectEvery(clip=src[1160:1220], cycle=5, offsets=[0,1,2,4,])
dec1220 = c.std.SelectEvery(clip=src[1220:1465], cycle=5, offsets=[0,2,3,4,])
dec1465 = c.std.SelectEvery(clip=src[1465:1515], cycle=5, offsets=[0,1,2,3,])
dec1515 = c.std.SelectEvery(clip=src[1515:1665], cycle=5, offsets=[0,1,2,4,])
dec1665 = c.std.SelectEvery(clip=src[1665:1670], cycle=5, offsets=[0,1,3,4,])
dec1670 = c.std.SelectEvery(clip=src[1670:1790], cycle=5, offsets=[1,2,3,4,])
dec2070 = c.std.SelectEvery(clip=src[2070:2220], cycle=5, offsets=[1,2,3,4,])
dec2220 = c.std.SelectEvery(clip=src[2220:2255], cycle=5, offsets=[0,2,3,4,])
dec2255 = c.std.SelectEvery(clip=src[2255:2375], cycle=5, offsets=[0,1,2,4,])
dec2375 = c.std.SelectEvery(clip=src[2375:2380], cycle=5, offsets=[0,2,3,4,])
dec2380 = c.std.SelectEvery(clip=src[2380:2465], cycle=5, offsets=[1,2,3,4,])
dec2465 = c.std.SelectEvery(clip=src[2465:2565], cycle=5, offsets=[0,1,2,4,])
dec2565 = c.std.SelectEvery(clip=src[2565:2715], cycle=5, offsets=[0,1,3,4,])
dec2715 = c.std.SelectEvery(clip=src[2715:2720], cycle=5, offsets=[0,2,3,4,])
dec2720 = c.std.SelectEvery(clip=src[2720:2850], cycle=5, offsets=[0,1,3,4,])
dec2850 = c.std.SelectEvery(clip=src[2850:3000], cycle=5, offsets=[0,1,2,3,])
dec0_r1 = c.std.SelectEvery(clip=src_r1[0:100], cycle=5, offsets=[0,1,2,4,])
dec100_r1 = c.std.SelectEvery(clip=src_r1[100:105], cycle=5, offsets=[0,2,3,4,])
dec105_r1 = c.std.SelectEvery(clip=src_r1[105:170], cycle=5, offsets=[0,1,3,4,])
dec170_r1 = c.std.SelectEvery(clip=src_r1[170:250], cycle=5, offsets=[1,2,3,4,])
dec250_r1 = c.std.SelectEvery(clip=src_r1[250:505], cycle=5, offsets=[0,1,2,4,])
dec505_r1 = c.std.SelectEvery(clip=src_r1[505:615], cycle=5, offsets=[0,1,2,3,])
dec615_r1 = c.std.SelectEvery(clip=src_r1[615:620], cycle=5, offsets=[0,1,2,4,])
dec880_r1 = c.std.SelectEvery(clip=src_r1[880:885], cycle=5, offsets=[0,2,3,4,])
dec885_r1 = c.std.SelectEvery(clip=src_r1[885:920], cycle=5, offsets=[0,1,3,4,])
dec920_r1 = c.std.SelectEvery(clip=src_r1[920:980], cycle=5, offsets=[1,2,3,4,])
dec980_r1 = c.std.SelectEvery(clip=src_r1[980:1155], cycle=5, offsets=[0,1,2,4,])
dec1155_r1 = c.std.SelectEvery(clip=src_r1[1155:1160], cycle=5, offsets=[0,1,3,4,])
dec1160_r1 = c.std.SelectEvery(clip=src_r1[1160:1220], cycle=5, offsets=[0,1,2,4,])
dec1220_r1 = c.std.SelectEvery(clip=src_r1[1220:1465], cycle=5, offsets=[0,2,3,4,])
dec1465_r1 = c.std.SelectEvery(clip=src_r1[1465:1515], cycle=5, offsets=[0,1,2,3,])
dec1515_r1 = c.std.SelectEvery(clip=src_r1[1515:1665], cycle=5, offsets=[0,1,2,4,])
dec1665_r1 = c.std.SelectEvery(clip=src_r1[1665:1670], cycle=5, offsets=[0,1,3,4,])
dec1670_r1 = c.std.SelectEvery(clip=src_r1[1670:1790], cycle=5, offsets=[1,2,3,4,])
dec2070_r1 = c.std.SelectEvery(clip=src_r1[2070:2220], cycle=5, offsets=[1,2,3,4,])
dec2220_r1 = c.std.SelectEvery(clip=src_r1[2220:2255], cycle=5, offsets=[0,2,3,4,])
dec2255_r1 = c.std.SelectEvery(clip=src_r1[2255:2375], cycle=5, offsets=[0,1,2,4,])
dec2375_r1 = c.std.SelectEvery(clip=src_r1[2375:2380], cycle=5, offsets=[0,2,3,4,])
dec2380_r1 = c.std.SelectEvery(clip=src_r1[2380:2465], cycle=5, offsets=[1,2,3,4,])
dec2465_r1 = c.std.SelectEvery(clip=src_r1[2465:2565], cycle=5, offsets=[0,1,2,4,])
dec2565_r1 = c.std.SelectEvery(clip=src_r1[2565:2715], cycle=5, offsets=[0,1,3,4,])
dec2715_r1 = c.std.SelectEvery(clip=src_r1[2715:2720], cycle=5, offsets=[0,2,3,4,])
dec2720_r1 = c.std.SelectEvery(clip=src_r1[2720:2850], cycle=5, offsets=[0,1,3,4,])
dec2850_r1 = c.std.SelectEvery(clip=src_r1[2850:3000], cycle=5, offsets=[0,1,2,3,])

src = c.std.Splice(mismatch=True, clips=[dec0,dec100,dec105,dec170,dec250,dec505,dec615,src[620:880],dec880,dec885,dec920,dec980,dec1155,dec1160,dec1220,dec1465,dec1515,dec1665,dec1670,src[1790:2070],dec2070,dec2220,dec2255,dec2375,dec2380,dec2465,dec2565,dec2715,dec2720,dec2850,])
src_r1 = c.std.Splice(mismatch=True, clips=[dec0_r1,dec100_r1,dec105_r1,dec170_r1,dec250_r1,dec505_r1,dec615_r1,src_r1[620:880],dec880_r1,dec885_r1,dec920_r1,dec980_r1,dec1155_r1,dec1160_r1,dec1220_r1,dec1465_r1,dec1515_r1,dec1665_r1,dec1670_r1,src_r1[1790:2070],dec2070_r1,dec2220_r1,dec2255_r1,dec2375_r1,dec2380_r1,dec2465_r1,dec2565_r1,dec2715_r1,dec2720_r1,dec2850_r1,])

src = utils.scenefilter_interlaced_fade(src, 2462, 2500, True)

src = rektlvls(src, colnum=[715], colval=[-2])

src = c.std.SetFieldBased(src, 0)
src = c.resize.Spline36(clip=src, width=864, height=480, format=c.query_video_format(src.format.color_family, vs.INTEGER, 10, src.format.subsampling_w, src.format.subsampling_h).id)
src = c.std.CropRel(clip=src, left=6, top=2, right=4, bottom=0)
src_r1 = c.std.SetFieldBased(src_r1, 0)
src_r1 = c.resize.Spline36(clip=src_r1, width=864, height=480, format=c.query_video_format(src_r1.format.color_family, vs.INTEGER, 10, src_r1.format.subsampling_w, src_r1.format.subsampling_h).id)
src_r1 = c.std.CropRel(clip=src_r1, left=6, top=0, right=4, bottom=0)
src = haf.Overlay(src_r1, src)

src = rektlvls(src, rownum=[478, 479], rowval=[7, 7])

src.set_output()
