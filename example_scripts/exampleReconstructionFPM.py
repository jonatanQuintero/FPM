""" 
FPM data reconstructor 
change data visualization and initialization options manually for now
"""
import matplotlib

try:
    matplotlib.use("tkagg")
except:
    pass
import PtyLab
from PtyLab.io import getExampleDataFolder
from PtyLab import Engines
import logging

logging.basicConfig(level=logging.INFO)

""" 
ptycho data reconstructor 
change data visualization and initialization options manually for now
"""

# download the example file from one of the suggested repositories
#fileName = "/Users/User/Documents/Ptychography/PtyLab.py/datasets/LungCarcinomaFPM.hdf5"  # simu.hdf5 or Lenspaper.hdf5
fileName = "/Users/User/Documents/Ptychography/PtyLab.py/datasets/USAFTargetFPM.hdf5"
filePath = getExampleDataFolder() / fileName

exampleData, reconstruction, params, monitor, engine, calib = PtyLab.easyInitialize(
    filePath, operationMode="FPM"
)

# %% Prepare everything for the reconstruction
# now, all our experimental data is loaded into experimental_data and we don't have to worry about it anymore.
# now create an object to hold everything we're eventually interested in
reconstruction.initialProbe = "circ"
reconstruction.initialObject = "upsampled"

# %% FPM position calibration
calib.plot = False
# calib.fit_mode ='SimilarityTransform'
calib.calibrateRadius = True
calib.fit_mode = "Translation"
calib.runCalibration()

# %% Prepare reconstruction post-calibration
reconstruction.initializeObjectProbe()

# %% Set monitor properties
monitor.figureUpdateFrequency = 1
monitor.objectPlot = "complex"  # complex abs angle
monitor.verboseLevel = "high"  # high: plot two figures, low: plot only one figure
monitor.objectZoom = 0.01  # control object plot FoVW
monitor.probeZoom = 0.01  # control probe plot FoV

# %% Set param
params.gpuSwitch = False
params.positionOrder = "NA"
params.probePowerCorrectionSwitch = False
params.comStabilizationSwitch = False
params.probeBoundary = True
params.adaptiveDenoisingSwitch = True
# Params.positionCorrectionSwitch = True
# Params.backgroundModeSwitch = True

#%% Run the reconstructors
# Run momentum accelerated reconstructor
engine = Engines.mqNewton(reconstruction, exampleData, params, monitor)
engine.numIterations = 50
engine.betaProbe = 1
engine.betaObject = 1
engine.beta1 = 0.5
engine.beta2 = 0.5
engine.betaProbe_m = 0.25
engine.betaObject_m = 0.25
engine.momentum_method = "NADAM"
engine.reconstruct()
