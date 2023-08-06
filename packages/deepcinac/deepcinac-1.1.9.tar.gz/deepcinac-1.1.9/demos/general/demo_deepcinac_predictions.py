from deepcinac.cinac_predictor import *
from deepcinac.cinac_structures import *
from deepcinac.utils.cinac_file_utils import read_cell_type_categories_yaml_file
import tensorflow as tf
import numpy as np

"""
We're going to guide you on how using deepCINAC to either infer the neuronal activity or 
predict the cell type from your calcium imaging data. 

Here is a link to our gitlab page for more information about our package: https://gitlab.com/cossartlab/deepcinac

So far, to run this code, you will need some calcium imaging data to work on (in tiff format) and 
some segmentation data (ROIs) indicating the contours or pixels 
that compose your cells (compatible format are Caiman, suite2p, Fiji or NWB outputs).

The filenames of the data in the code corresponds to the demo data available on our gitlab repository, 
using suite2p ROIs data: https://gitlab.com/cossartlab/deepcinac/tree/master/demos/data

You will also need a model file (.json extension) and a file containing the weights of network (.h5 extensions). 
You can download some there: https://bit.ly/2XyNoF5

"""

"""
You can either choose to use the classifier to infer neuronal activity or to predict the cell type. 
To predict the cell type set the variable cell_type_classifier_mode to False, else True.
"""
if __name__ == '__main__':
    cell_type_classifier_mode = False

    # ------------------------- #
    #     Setting file names
    # ------------------------- #

    # root path, just used to avoid copying the path everywhere
    root_path = '/../demo'

    # path to calcium imaging data
    data_path = os.path.join(root_path, "data")
    movie_file_name = os.path.join(data_path, "demo_deepcinac_1.tif")

    # string used to identify the recording from which you want to predict activity
    identifier = "demo_deepcinac"

    # Path to your model data. It's possible to have more than one model, and use
    # each for different cell of the same recording (for exemple, one
    # network could be specialized for interneurons and the other one for pyramidal
    # cells)
    if cell_type_classifier_mode:
        weights_file_name = os.path.join(root_path,
                                         "model/cell_type_v1_weights.h5")
        json_file_name = os.path.join(root_path,
                                      "model/cell_type_v1_model.json")
    else:
        weights_file_name = os.path.join(root_path, "model/cinac_v1_general_weights.h5")
        json_file_name = os.path.join(root_path, "model/cinac_v1_general_model.json")

    # useful for cell type classifier
    cell_type_yaml_file = os.path.join(data_path, "cell_type_yaml_files",
                                       "pyr_vs_ins_multi_class.yaml")

    # path of the directory where the results will be save
    # a directory will be created each time the prediction is run
    # the directory name will be the date and time at which the analysis has been run
    # the predictions will be in this directory.
    results_path = os.path.join(root_path, "results")

    # not mandatory, just to test if you GPU is accessible
    device_name = tf.test.gpu_device_name()
    if device_name != '/device:GPU:0':
        raise SystemError('GPU device not found')
    print('Found GPU at: {}'.format(device_name))

    evaluate_cell_type_classifier = True

    if evaluate_cell_type_classifier and cell_type_classifier_mode:
        cinac_dir_name = os.path.join(data_path, "cinac_cell_type_ground_truth", "for_testing")

        evaluate_cell_type_predictions(cinac_dir_name, cell_type_yaml_file, results_path,
                                       json_file_name, weights_file_name, save_cell_type_distribution=True)
    else:
        # ############
        # Creating an instance of CinacRecording
        # this class will be use to link the calcium imaging movie and the ROIs.
        # ############

        cinac_recording = CinacRecording(identifier=identifier)

        # Creating and adding to cinac_recording the calcium imaging movie data
        cinac_movie = CinacTiffMovie(tiff_file_name=movie_file_name)

        # if you have the movie already loaded in memory (for exemple in an nwb file,
        # if not using external link), then if you could do instead:

        # cinac_movie = CinacTiffMovie(tiff_movie=tiff_movie)
        # tiff_movie being a 3d numpy array (n_frames*dim_y*dim_x)

        cinac_recording.set_movie(cinac_movie)

        """
        Adding the information regarding the ROIs to the CinacRecording instance.
        There are four options, de-comment the one you need
        """

        # -----------------------------
        # options 1: suite2p data
        # -----------------------------

        """
        Segmenting your data will produce npy files used to build the ROIs
        the file iscell.npy indicated which roi represents a real cell, only those will be used.
        stat.npy will conain the ROIs coordinates. 
        """

        is_cell_suite2p_file_name = os.path.join(data_path, "suite2p", "demo_deepcinac_iscell_1.npy")
        stat_suite2p_file_name = os.path.join(data_path, "suite2p", "demo_deepcinac_stat_1.npy")
        cinac_recording.set_rois_from_suite_2p(is_cell_file_name=is_cell_suite2p_file_name,
                                               stat_file_name=stat_suite2p_file_name)


        # ------------------------------------------------------
        # options 2: contours coordinate (such as CaImAn, Fiji)
        # ------------------------------------------------------

        """
        Args:
            coord: numpy array of 2d, first dimension of length 2 (x and y) and 2nd dimension 
                   of length the number of
                   cells. Could also be a list of lists or tuples of 2 integers
            from_matlab: Indicate if the data has been computed by matlab, 
                         then 1 will be removed to the coordinates so that it starts at zero.
            """

        # coord = None
        # cinac_recording.set_rois_2d_array(coord=coord, from_matlab=False)


        # ------------------------------------------------
        # options 3: NWB (Neurodata Without Borders) data
        # ------------------------------------------------

        """
        Args:
             nwb_data: nwb object instance
                 name_module: Name of the module to find segmentation. 
                 Used this way: nwb_data.modules[name_module]
                 Ex: name_module = 'ophys'
             name_segmentation: Name of the segmentation in which find the plane segmentation.
                 Used this way:get_plane_segmentation(name_segmentation)
                 Ex: name_segmentation = 'segmentation_suite2p'
             name_seg_plane: Name of the segmentation plane in which to find the ROIs data
                 Used this way: mod[name_segmentation]get_plane_segmentation(name_seq_plane)
                 Ex: name_segmentation = 'my_plane_seg'
        
        'pixel_mask' data need to be available in the segmentation plane for it to work
        
        """
        # nwb_data = None
        # name_module = ""
        # name_segmentation = ""
        # name_seg_plane = ""
        # cinac_recording.set_rois_from_nwb(nwb_data=nwb_data, name_module=name_module,
        #                                   name_segmentation=name_segmentation, name_seg_plane=name_seg_plane)


        # -----------------------
        # options 4: Pixel masks
        # -----------------------

        """
        Args:
            pixel_masks: list of list of 2 integers representing 
                         for each cell all the pixels that belongs to the cell
        This method is actually called by set_rois_from_nwb() after extracting the 
        pixel_masks data from the nwb_file
        """

        # pixel_masks = None
        # cinac_recording.set_rois_using_pixel_mask(pixel_masks=pixel_masks)

        """
        Then we decide which network will be used for predicting the cells' activity.
        
        A dictionnary with key a tuple of 3 elements is used.
        
        The 3 elements are:
        
        (string) the model file name (.json extension)
        (string) the weights of the network file name (.h5 extension)
        (string) identifier for this configuration, will be used to name the output file
        The dictionnary will contain as value the cells to be predicted by the key configuration. 
        If the value is set to None, then all the cells will be predicted using this configuration.
        """

        model_files_dict = dict()
        # predicting 10 first cells with this model, weights and string identifying the network
        model_files_dict[(json_file_name, weights_file_name, "demo_cinac")] = np.arange(10)

        # the line below allows to predict the activity of all cells present
        # model_files_dict[(json_file_name, weights_file_name, "demo_cinac")] = None

        """
        We now create an instance of CinacPredictor and add the CinacRecording we have just created.
        
        It's possible to add more than one instance of CinacRecording, they will be predicted on the same run then.
        
        The argument removed_cells_mapping allows to remove cells from the segmentation. 
        This could be useful as the network take in consideration the adjacent cells to predict the activity, 
        thus if a cell was wrongly added to segmentation, this could lower the accuracy of the classifier.
        """

        cinac_predictor = CinacPredictor()

        """
        Args:
        
            removed_cells_mapping: integers array of length the original numbers of 
                cells (such as defined in CinacRecording)
                and as value either of positive int representing the new index of 
                the cell or -1 if the cell has been removed
        """

        cinac_predictor.add_recording(cinac_recording=cinac_recording,
                                      removed_cells_mapping=None,
                                      model_files_dict=model_files_dict)

        """
        Finally, we run the prediction.
        
        The output format could be either a matlab file(.mat) and/or numpy one (.npy).
        
        If matlab is chosen, the predictions will be available under the key "predictions".
        
        The predictions are a 2d float array (n_cells * n_frames) with value between 0 and 1, representing the prediction of our classifier for each frame. 1 means the cell is 100% sure active at that time, 0 is 100% sure not active.
        
        A cell is considered active during the rising time of the calcium transient.
        
        We use a threshold of 0.5 to binarize the predictions array and make it a raster.
        """

        # you could decomment this line to make sure the GPU is used
        #with tf.device('/device:GPU:0'):

        # predictions are saved in the results_path and return as a dict,
        overlap_value = 0 if cell_type_classifier_mode else 0.5
        predictions_dict = cinac_predictor.predict(results_path=results_path,
                                                   output_file_formats="npy",
                                                   overlap_value=overlap_value,
                                                   cell_type_classifier_mode=cell_type_classifier_mode)

        # Do output_file_formats=["npy", "mat"] to get both extensions

        """
        You can then use the .npz produced to visualize the predictions in the GUI, or use them at your ease, b
        elow is the code to binarized the activity predictions. 

        When loading the npz, you can get the predictions by loading the field 'predictions'. 
        The other field is 'cells' and is a 1d array containing the 
        indices of the cells whose activity has been predicted.
        """

        """
        Code to convert the activity predictions as binary raster
        """
        if not cell_type_classifier_mode:
            # dictionary with key identifier of the recording and value a binary 2d array
            binary_predictions_dict = dict()

            for identifier, predictions in predictions_dict.items():
                binary_predictions = np.zeros((len(predictions), len(predictions[0])),
                                              dtype="int8")
                binary_predictions[predictions > 0.5] = 1
                binary_predictions_dict[identifier] = binary_predictions
        else:
            # code to display the cell type predicted
            cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg = \
                read_cell_type_categories_yaml_file(yaml_file=cell_type_yaml_file,
                                                    using_multi_class=2)

            for identifier, cell_type_predictions in predictions_dict.items():
                print(f"identifier: {identifier}")
                for cell in np.arange(len(cell_type_predictions)):
                    if np.sum(cell_type_predictions[cell]) == 0:
                        continue
                        # print(f"No prediction for cell {cell}")
                    else:
                        cell_type_code = np.argmax(cell_type_predictions[cell])
                        print(f"Predictions for cell {cell} are {cell_type_predictions[cell]}")
                        print(f"Predicted type for cell {cell} is {cell_type_from_code_dict[cell_type_code]}")
                        print(" ")
