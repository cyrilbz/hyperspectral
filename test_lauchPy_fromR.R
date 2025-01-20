# a test program to launch Python from R
library(reticulate)

graphics.off()

# when running from R you must skip the Python plots
Sys.setenv(SKIP_PLOTS = TRUE)

# run the Python script
py_run_file("C:/Documents/traitement_image/Hyperspectral_Alex/code/main.py")

# Get the results and some informations from Python

result_reflect= py$reflectance_list # get reflectance data
wavelength = py$lambda_vec # get wavelength
my_strings <- list("Hydrated", "Drought")
nplots = length(result_reflect) # get number of plots/data sets

# Iterate and create the graphs
par(mfrow = c(1, nplots))
for (i in 1:nplots) {
  plot(wavelength,result_reflect[[i]],ylab=my_strings[[i]])
}