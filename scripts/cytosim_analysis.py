# /usr/bin/python3
####### PACKAGES |||||||||----------------
import sio_tools as sio
import sys
import pandas as pd
from filaments import Filament,make_filaments



##### A class containing several filaments
class Network(Filament):
    def __init__(self,*args,**kwargs):
        self.filaments=[]
        self.analysis=None
        self.f_analysis=None
        self.initialize(*args,**kwargs)

    #def initialize(self, *args, fiber_pts_report=None, fiber_pts_lines=None, **kwargs):
    def initialize(self,*args, fiber_points_report=None, fiber_points_lines=None, **kwargs):
        if fiber_points_report is not None:
            [pts,a,b]=sio.getdata(fiber_points_report)
            self.filaments = make_filaments(points=pts)
        elif fiber_points_lines is not None:
            [pts, a, b] = sio.getdata_lines(fiber_points_lines)
            self.filaments = make_filaments(points=pts)

    def analyze(self, *args, **kwargs):
        ids=[]
        f_datas=None
        for fil in self.filaments:
            fil.analyze(*args, **kwargs)
            ids.append(fil.id)
            if f_datas is None:
                f_keys = fil.analysis.keys()
                f_datas = pd.DataFrame(columns=f_keys)
            else:
                f_datas.loc[fil.id] = [fil.analysis[key] for key in f_keys]
        self.f_analysis=f_datas

    def export_f_analysis(self,fname='f_analysis.csv'):
        self.f_analysis.to_csv(fname)

    def export_analysis(self, fname='analysis.csv'):
        return

# A set of frame ; each frame contains a network
class Frames(Network):
    def __init__(self,*args,**kwargs):
        self.networks=[]
        self.analysis={}
        self.n_frames = 0
        self.initialize(*args,**kwargs)


    def initialize(self, *args, fiber_points_report=None, **kwargs):
        if fiber_points_report is not None:
            reports=get_frames_from_report(fiber_points_report)
            for report in reports:
                self.n_frames+=1
                self.networks.append(Network(fiber_points_lines=report))

    def analyze(self,*args,**kwargs):
        for frame in self.networks:
            frame.analyze(*args,**kwargs)

def get_frames_from_report(fname):
    lines = sio.getlines(fname)
    frixes = [i for i, x in enumerate(lines) if x.find("frame") > 0]
    nframes = len(frixes)
    frixes.append(len(lines))
    return  [lines[frixes[i]:frixes[i + 1]] for i in range(nframes)]


# A really simple example for analysis functions
def count_points(pts):
    shape=pts.shape
    return shape[0]


if __name__=="__main__":
    args = sys.argv[1:]
    frames=Frames(fiber_points_report=args[0])
    funcs = {'number': lambda x: count_points(x)}
    frames.analyze(func_dict=funcs)
    frames.networks[10].export_f_analysis()

    #network=Network(fiber_points_report=args[0])
    #funcs={'number': lambda x: count_points(x)}
    #network.analyze(func_dict=funcs)
    #network.export_f_analysis()

