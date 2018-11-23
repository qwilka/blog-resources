import glob
import json
import logging
import os
import re
import shlex
import shutil
import subprocess
import tempfile

logger = logging.getLogger(__name__)

import skimage.io


def vid2img(vid_path, ss, img_type='jpg', savefile=False, clobber=False):
    _altname, _ext = os.path.splitext(vid_path)
    if is_number(ss):
        _ss = str(int(ss*1000)) + "ms"
    else:
        _ss = ss
    _altname += "__{}{}".format(_ss, _ext)
    _target = get_target_filepath("dummy."+img_type, "", alt_filename=_altname)
    # print(_target)
    # return None, None
    # _cmd_str = ('ffmpeg -i "' + vid_path + '" ' + 
    # '-vf "' +'select=gte(t\,' + str(ss) + ')*not(gte(n\,1))" ' +
    # '-start_number 0  -vsync vfr -qscale:v 1 "' + _target +'"')
    if clobber or not os.path.isfile(_target):
        _cmd_str = ('ffmpeg -i "' + vid_path + '" ' + 
        '-vf "' +'select=gte(t\,' + str(ss) + ')" ' +
        '-start_number 0 -frames 1 -vsync vfr -qscale:v 1 "' + _target +'"')
        logger.debug("vid2img: system command «%s»" % (_cmd_str, ))
        try: 
            retVal = subprocess.check_output(shlex.split(_cmd_str), stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            logger.error("vid2img: %s; %s" % (err, err.output))
            return False, None
    try:
        _img = skimage.io.imread(_target)
    except FileNotFoundError as err:
        logger.error("vid2img: %s" % (err, ))
        return False, None
    if savefile:
        return _img, _target
    else:
        os.remove(_target)
        return _img, None


def vid2image_files(vid_path, t_start, t_end, img_type='jpg'):
    _altname, _ext = os.path.splitext(vid_path)
    _ss = str(int(t_start*1000)) + "ms"
    _vid_basename = os.path.basename(_altname)
    _glob_patt = _vid_basename + "__{}__???.{}".format(_ss, img_type)
    _altname += "__{}__%03d{}".format(_ss, _ext)
    _target = get_target_filepath("dummy."+str(img_type), "", alt_filename=_altname)
    _cmd_str = ('ffmpeg -i "' + vid_path + '" ' + 
    '-vf "' +'select=between(t\,' + str(t_start) + '\,' + str(t_end) + ')" ' +
    '-start_number 0  -vsync vfr -qscale:v 1 "' + _target +'"')
    logger.debug("vid2img: system command «%s»" % (_cmd_str, ))
    try: 
        retVal = subprocess.check_output(shlex.split(_cmd_str), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        logger.error("vid2img: %s; %s" % (err, err.output))
        return False
    _meta = get_video_meta(vid_path, params=["r_frame_rate_interval"])
    frame_interval = _meta["r_frame_rate_interval"]
    #print(_meta)
    fileslist = glob.glob(_glob_patt)
    # print(_glob_patt)
    # print(_vid_basename)
    # print(fileslist)
    _rgx = re.compile(r"__(\d+)ms__(\d{3})." + img_type + "$")
    target_list = []
    for _file in fileslist:
        _mat = _rgx.search(_file)
        if _mat:
            #print(_mat.groups())
            _starttime = float(_mat.groups()[0])
            _imgno = int(_mat.groups()[1])
            _ss = int(_starttime + frame_interval*_imgno*1000)
            _newname = "{}__{:>08d}ms.{}".format(_vid_basename, _ss, img_type)
            _target_path = shutil.move(_file, _newname)
            target_list.append(_target_path)
    return target_list



# def vid2imgfile(vid_path, ss, img_type='png', save_path="./", clobber=True):
#     _altname, _ext = os.path.splitext(vid_path)
#     if is_number(ss):
#         _ss = str(int(ss*1000)) + "ms"
#     else:
#         _ss = ss
#     _altname += "__{}{}".format(_ss, _ext)
#     _target = get_target_filepath("dummy."+img_type, save_path, alt_filename=_altname)
#     if clobber or not os.path.isfile(_target):
#         _img = vid2img(vid_path, ss, img_type, save=True, save_path=_target)
#     else:
#         logger.debug("vid2imgfile: image «%s» exists, not re-extracting." % (_target, ))
#         _img = skimage.io.imread(_target)
#     return _target, _img


def get_video_meta(vid_path, savefile=False, save_path="./", clobber=False,
            params=None):
    _target = get_target_filepath("dummy.json", save_path, 
                alt_filename=vid_path, orig_ext=True)
    if clobber or not os.path.isfile(_target):
        _cmd_str = ('ffprobe -loglevel quiet -show_format -show_streams -of json "' +
                    vid_path + '"')
        logger.debug("video_meta: system command «%s»" % (_cmd_str, ))
        try: 
            op = subprocess.check_output(shlex.split(_cmd_str), stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            logger.error("video_meta: %s; %s" % (err, err.output))
            return False
        op = op.decode(encoding='UTF-8').strip()
        op = json.loads(op)
        video_stream_idx = audio_stream_idx = None
        count_video_streams = 0
        for _idx, _stream in enumerate(op["streams"]):
            if _stream["codec_type"] == "video":
                if not video_stream_idx: # take 1st video stream
                    video_stream_idx = _idx
                count_video_streams += 1
            if _stream["codec_type"] == "audio":
                audio_stream_idx = _idx
        _meta = {"command": _cmd_str}
        _meta["source"] = {"fs_path": vid_path}
        _meta["video_stream_idx"] = video_stream_idx
        _meta["video_stream_no"] = count_video_streams
        _meta["audio_stream_idx"] = audio_stream_idx
        _meta.update(op)   
        if savefile:
            with open(_target, 'w') as _metaF:
                json.dump(_meta, _metaF)
            logger.debug("video_meta: saving metadata in «%s»" % (_target, ))
    else: 
        with open(_target, 'r') as _metaF:
            _meta = json.load(_metaF)
    if params:
        param_dct = {}
        video_stream_idx = _meta["video_stream_idx"]
        for _parm in params:
            if _parm=="r_frame_rate":
                param_dct["r_frame_rate"] = _meta["streams"][video_stream_idx]["r_frame_rate"]
            elif _parm=="r_frame_rate_interval":
                r_frame_rate = _meta["streams"][video_stream_idx]["r_frame_rate"]
                _num, _denom = r_frame_rate.split("/")
                param_dct["r_frame_rate_interval"] = float(_denom)/float(_num)
            return param_dct
    return _meta


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def fix_filename(filename):
    return re.sub(r'[^\w\d_.]', '_', filename)


def get_target_filepath(source, target, alt_filename=None, 
        orig_ext=False, fix_filename=False):
    if os.path.isdir(target) or target.endswith(os.sep) or target=="":
        if alt_filename:
            if orig_ext:
                _basename = os.path.basename( alt_filename )
            else: # strip off the source filename extension
                _basename = os.path.basename( os.path.splitext(alt_filename)[0])
            _basename += os.path.splitext(source)[1]
            if fix_filename:
                _basename = fix_filename(_basename)
            _target = os.path.join(target, _basename)
        else:
            _target = os.path.join(target, os.path.basename(source) )
    else:
        _target = target
    return _target


def move_file_altname(source, target, alt_filename=None):
    if not os.path.isfile(source):
        logger.error("move_file_altname: «%s» is not a valid file." % (source,))
        return False
    _target = get_target_filepath(source, target, alt_filename)
    os.makedirs(os.path.dirname(_target), mode=0o755, exist_ok=True)
    _target_path = shutil.move(source, _target)
    return _target_path


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    vidfile = "/home/develop/Downloads/data/Skarv_2013/VisualWorks/Projects/18-F-5824_(SKL52)/9821/DATA_201308151543410/201308151543410@Port.mpg"

    # save video file metadata
    # meta = get_video_meta(vidfile, savefile=True)
    # print(meta)

    # extract images
    # img_path, img = vid2imgfile(vidfile, 10.2, img_type='png', 
    #     save_path="", clobber=True)
    # print(img_path)
    # for ss in [0, 0.3, 1.0, 1.1, 83.5, 10.0, 150.08, 151.0]:
    #     img, img_path = vid2img(vidfile, ss, img_type='jpg', savefile=True)
    #     print(img_path)

    # extract series of images
    img_list = vid2image_files(vidfile, 149.0, 151.0)
    print(img_list)
