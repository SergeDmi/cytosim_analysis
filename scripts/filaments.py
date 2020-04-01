# /usr/bin/python3
####### PACKAGES
import numpy as np


### This should definitely be in a yaml file
__N_DIM__=3

###### A class to contain a single filament
class Filament:
    def __init__(self, *args, points=np.array(None), id=None,**kwargs):
        self.points=np.array(points[:,0:__N_DIM__])
        self.curvatures=np.array(points[:,-1])
        self.id=int(id)
        self.analysis={}
        shape=points.shape
        self.n_points=shape[0]
        #self.seg_lengths=[]

    def analyze(self,*args,func_dict={},**kwargs):
        # we even provide a nice custom interface to lambda funcs
        for name,func in func_dict.items():
            self.analysis[name]=func(self.points)
        # I guess we should do something else...
        [cs,mp,absc] = self.get_curvatures()
        self.analysis['deformation_energy']=self.deformation_energy(cs,mp,**kwargs)
        self.analysis['curvatures']=cs
        #self.analysis.['curvature_fft']=


    def deformation_energy(self, cs, mp, stiffness=1.0, **kwargs):
        return 0.5*stiffness*np.sum(np.sum(cs * cs, axis=1) * mp)


    def get_curvatures(self):
        pts=self.points
        n_pts=pts.shape[0]
        if self.n_points>2:
            # dp are the segments
            dp=pts[1:,:]-pts[0:-1,:]
            seg_lengths = np.sqrt(np.sum(dp * dp, axis=1))

            # mp are the middle points
            #mp=(pts[1:,:]+pts[0:(n_pts-1),:])/2.0
            #dm=mp[1:,:]-mp[0:(n_pts-2),:]
            #m_lengths=np.sum(dm * dm, axis=1)
            #print(seg_lengths)

            m_lengths=( seg_lengths[1:]+seg_lengths[0:-1] )/2.0
            #print(m_lengths)
            #print(m_lengths.shape)
            #self.seg_lengths=seg_lengths
            n_c=n_pts-2
            curvs=np.zeros((n_c,__N_DIM__))

            for i in range(n_c):
                curvs[i,:] = ( (pts[i+1,:]-pts[i,:])/seg_lengths[i] + (pts[i+1,:]-pts[i+2,:])/seg_lengths[i+1] )/m_lengths[i]

        abscissa=np.zeros((n_c,1))
        for i,ds in enumerate(seg_lengths[1:n_c-2]):
            abscissa[i+1]=abscissa[i]+ds
        return curvs,m_lengths,abscissa


def make_filaments(*args,points=np.array([[]]),**kwargs):
    filaments=[]
    ixes=np.unique(points[:,0])
    #print(points[0:5,:])
    for id in ixes:
        #print(points.shape)
        pts=points[np.where(points[:,0] == id )]
        pts=pts[:,1:]
        #print(pts.shape)
        filaments.append(Filament(*args,id=id,points=pts,**kwargs))
    return filaments