####### PACKAGES
import numpy as np
import numpy.fft as fft
import sys
from cytosim_analysis import Frames
import pandas as pd

####### FUNCTIONS

def analyze_curvature(fname_in=None,fname_out=None):
	frames = Frames(fiber_points_report=fname_in)
	frames.analyze()
	#frames.networks[10].export_f_analysis()

	ffts = []
	sPhiR = []
	sPhiI = []
	sPhiAppR = []
	sPhiAppI = []
	for network in frames.networks:
		for filament in network.filaments:
			fcs = fft.fft(filament.analysis['curvatures'],axis=0)
			fcapp = fft.fft(filament.curvatures[1:-1])
			sPhiR.append(np.sum(np.square(np.real(fcs)), axis=1))
			sPhiI.append(np.sum(np.square(np.imag(fcs)), axis=1))
			sPhiAppR.append(np.square(np.real(fcapp)))
			sPhiAppI.append(np.square(np.imag(fcapp)))
			ffts.append(fcs)

	sPhiR = np.array(sPhiR)
	sPhiI = np.array(sPhiI)
	sPhiAppR = np.array(sPhiAppR)
	sPhiAppI = np.array(sPhiAppI)

	MsPhiR = fft.fftshift(np.mean(sPhiR, axis=0))
	MsPhiI = fft.fftshift(np.mean(sPhiI, axis=0))
	MsPhiAppR = fft.fftshift(np.mean(sPhiAppR, axis=0))
	MsPhiAppI = fft.fftshift(np.mean(sPhiAppI, axis=0))

	n_pts=MsPhiR.shape[0]
	out_datas = pd.DataFrame(columns=['ix','real','ima','appR','appI'])
	for i in np.arange(n_pts):
		out_datas.loc[i] = [i,MsPhiR[i],MsPhiI[i],MsPhiAppR[i],MsPhiAppI[i]]
	out_datas.to_csv(fname_out)



if __name__=="__main__":
	args = sys.argv[1:]
	nargs=len(args)
	if nargs:
		fname_in=args[0]
	else:
		fname_in='fibers.txt'
	if nargs>1:
		fname_out=args[1]
	else:
		fname_out='results.csv'

	analyze_curvature(fname_in,fname_out)


