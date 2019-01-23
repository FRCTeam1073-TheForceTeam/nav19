= visionmanager design

(overarching visual)

                                     protocol					   networktables
 			CAMERA <----------------------->  PI  <------------------------------------------>
							  -visionmanager.py    <------------------
											input
																					

= NetworkTables API   INTERFACE:

	- (N cameras) each cam has set of keys in nt that match this pattern:

		- cam_#_mode       displayed as a string, can be "blob" or "line" and dictates the structure of the array in later bits
        	- cam_#_frame      a coutner that will run constantly
		- cam_#_status	   string, the feedback for the driver station (aka "this camera died, this one caught on fire, and this camera never 	      	       		   	   calls me; one may think of it as the Jewish Mother of the cameras, if you will)
		- cam_#_lineseg    number array   [x1, y1, x2, y2, score]   <-- "n" number of times 
		- cam_#_blobs      number array   [x1, y1, x2, y2, score, color]  <-- "n" number of times
		- cam_#_?(etc.)    number array   [ ~~fill~in~the~blank~~]  <-- "n" number of times

	- inputs: cam_mode
	- outputs: cam_frame, cam_status, cam_lineseg, cam_blobs, cam_etc.
