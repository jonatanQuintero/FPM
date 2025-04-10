import matplotlib
try:
    matplotlib.use("tkagg")
except:
    pass
import PtyLab
from PtyLab import Engines
import logging

logging.basicConfig(level=logging.INFO)


#filePath = "/Users/User/Documents/Ptychography/PtyLab.py/datasets/LungCarcinomaFPM.hdf5"
#filePath = "/bodega/FPM/PtyLab/FPM_generator-master/FPM_generator-master/datasets/my_FPM_dataset_fixed.hdf5"
filePath = "/bodega/FPM/PtyLab/simulated_FPM_data.hdf5"
#filePath = "/bodega/FPM/USAFTargetFPM.hdf5"
#filePath = "/Users/User/Desktop/FPM_INR-main/FPM_INR-main/data/sheepblood/sheepblood_r_2.hdf5"

experimentalData, reconstruction, params, monitor, engine, calib = PtyLab.easyInitialize(
    filePath, operationMode="FPM"
)
#match the indices of the frames to the encoder
#
# # Regular expression pattern to find a 4-digit number
# pattern = r'\d{1,4}.tif'
# numbers = r'\d{1,4}'
# indices = []
# for f in files:
#     match = re.findall(pattern, f)
#     for m in match:
#         number = re.findall(numbers, m)[0]
#         indices.append(int(number))
#
# indices = np.array(indices)-1 #zero-based index
# #
# encoder = encoder[indices]
# experimentalData.magnnification = 4
experimentalData.entrancePupilDiameter = None #entrance pupil diameter, defined in lens-based microscopes as the aperture diameter, reqquired for FPM
experimentalData._setData()
reconstruction.copyAttributesFromExperiment(experimentalData)
reconstruction.computeParameters()
# %% Prepare everything for the reconstruction
# now, all our experimental data is loaded into experimental_data and we don't have to worry about it anymore.
# now create an object to hold everything we're eventually interested in
reconstruction.initialProbe = "circ"
reconstruction.initialObject = "upsampled"

# %% FPM position calibration
calib.plot = True
calib.fit_mode ='SimilarityTransform'
calib.calibrateRadius = True
calib.fit_mode = "Translation"
calib.runCalibration()

# %% Prepare reconstruction post-calibration
reconstruction.initializeObjectProbe()

# %% Set monitor properties
monitor.figureUpdateFrequency = 1
monitor.objectPlot = "complex"  # complex abs angle
monitor.verboseLevel = "low"  # high: plot two figures, low: plot only one figure
monitor.objectZoom = 0.01  # control object plot FoVW
monitor.probeZoom = 0.01  # control probe plot FoV

# %% Set param
params.gpuSwitch = True
params.positionOrder = "NA"
params.probePowerCorrectionSwitch = False
params.comStabilizationSwitch = False
params.probeBoundary = True
params.adaptiveDenoisingSwitch = True
# Params.positionCorrectionSwitch = True
# Params.backgroundModeSwitch = True

#%% Run the reconstructors
# Run momentum accelerated reconstructor
engine = Engines.mqNewton(reconstruction, experimentalData, params, monitor)
engine.numIterations = 50
engine.betaProbe = 1
engine.betaObject = 1
engine.beta1 = 0.5
engine.beta2 = 0.5
engine.betaProbe_m = 0.25
engine.betaObject_m = 0.25
engine.momentum_method = "NADAM"
engine.reconstruct()