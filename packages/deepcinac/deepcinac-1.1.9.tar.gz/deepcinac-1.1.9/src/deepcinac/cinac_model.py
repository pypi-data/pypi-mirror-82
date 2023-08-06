"""
File that contains methods use to fit the data to the model and train it.
"""

import tensorflow as tf

TF_VERSION = tf.__version__
print(f"TF_VERSION {TF_VERSION}")

# depending on the TF version installed
if TF_VERSION[0] == "2":
    # from https://github.com/tensorflow/tensorflow/issues/25138
    from tensorflow.compat.v1 import ConfigProto
    from tensorflow.compat.v1 import InteractiveSession

    config = ConfigProto()
    # config.gpu_options.per_process_gpu_memory_fraction = 0.75
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)

    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Bidirectional, BatchNormalization
    from tensorflow.keras.layers import Input, LSTM, Dense, TimeDistributed, Activation, Lambda, Permute, RepeatVector
    from tensorflow.keras.models import Model, Sequential
    from tensorflow.keras.models import model_from_json
    from tensorflow.keras.optimizers import RMSprop, Adam, SGD
    from tensorflow.keras import layers
    from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
    from tensorflow.keras import backend as K
    from tensorflow.keras.models import load_model
    from tensorflow.keras.utils import get_custom_objects, multi_gpu_model
    from alt_model_checkpoint.tensorflow import AltModelCheckpoint
else:
    import keras
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Bidirectional, BatchNormalization
    from keras.layers import Input, LSTM, Dense, TimeDistributed, Activation, Lambda, Permute, RepeatVector
    from keras.models import Model, Sequential
    from keras.models import model_from_json
    from keras.optimizers import RMSprop, Adam, SGD
    from keras import layers
    from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
    from keras import backend as K
    from keras.models import load_model
    from keras.utils import get_custom_objects, multi_gpu_model
    from alt_model_checkpoint.keras import AltModelCheckpoint

from deepcinac.cinac_movie_patch import MoviePatchGeneratorMaskedVersions, MoviePatchData, \
    DataGenerator, MoviePatchGeneratorForCellType
from deepcinac.cinac_stratification import neuronal_activity_encoding, StratificationCamembert, \
    StratificationDataProcessor, StratificationCellTypeDataProcessor, StratificationCellTypeCamembert
from deepcinac.cinac_structures import CinacRecording, CinacDataMovie, CinacSplitedNpyMovie, CinacFileReaderMovie, \
    CinacSplitedTiffMovie
from deepcinac.utils.cinac_file_utils import CinacFileReader, read_cell_type_categories_yaml_file
from deepcinac.utils.utils import check_one_dir_by_id_exists
import numpy as np
import time
import scipy.signal
import yaml
import random

import os


def attention_3d_block(inputs, time_steps, use_single_attention_vector=False):
    """
    from: https://github.com/philipperemy/keras-attention-mechanism
    :param inputs:
    :param use_single_attention_vector:  if True, the attention vector is shared across
    the input_dimensions where the attention is applied.
    :return:
    """
    # inputs.shape = (batch_size, time_steps, input_dim)
    # print(f"inputs.shape {inputs.shape}")
    input_dim = int(inputs.shape[2])
    a = Permute((2, 1))(inputs)
    # a = Reshape((input_dim, time_steps))(a)  # this line is not useful. It's just to know which dimension is what.
    a = Dense(time_steps, activation='softmax')(a)
    if use_single_attention_vector:
        a = Lambda(lambda x: K.mean(x, axis=1))(a)  # , name='dim_reduction'
        a = RepeatVector(input_dim)(a)
    a_probs = Permute((2, 1))(a)  # , name='attention_vec'
    if TF_VERSION[0] == "2":
        output_attention_mul = tf.keras.layers.multiply([inputs, a_probs])
    else:
        output_attention_mul = keras.layers.multiply([inputs, a_probs])
    return output_attention_mul


# from: http://www.deepideas.net/unbalanced-classes-machine-learning/
def sensitivity(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    return true_positives / (possible_positives + K.epsilon())


# from: http://www.deepideas.net/unbalanced-classes-machine-learning/
def specificity(y_true, y_pred):
    true_negatives = K.sum(K.round(K.clip((1 - y_true) * (1 - y_pred), 0, 1)))
    possible_negatives = K.sum(K.round(K.clip(1 - y_true, 0, 1)))
    return true_negatives / (possible_negatives + K.epsilon())


def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    return true_positives / (predicted_positives + K.epsilon())


# ------------------------------------------------------------
# needs to be defined as activation class otherwise error
# AttributeError: 'Activation' object has no attribute '__name__'
# From: https://github.com/keras-team/keras/issues/8716
class Swish(Activation):

    def __init__(self, activation, **kwargs):
        super(Swish, self).__init__(activation, **kwargs)
        self.__name__ = 'swish'


def swish(x):
    """
    Implementing a the swish activation function.
    From: https://www.kaggle.com/shahariar/keras-swish-activation-acc-0-996-top-7
    Paper describing swish: https://arxiv.org/abs/1710.05941

    :param x:
    :return:
    """
    return K.sigmoid(x) * x
    # return Lambda(lambda a: K.sigmoid(a) * a)(x)


class CinacModel:
    """
    Model used to train a classifier.
    First add data using add_input_data() method
    Second prepare_model()
    And at last fit()

    Args:
            **kwargs:
            - results_path: (str, mandatory), path where to save the results (such as classifier weigths)
            - n_gpus: (int, default is 1) Maximum number of processes to spin up when using process-based threading
            - workers: (int, default is 10), number of workers used to run the classifier
            - using_multi_class: (int, default is 1) number of classes used to classify the activity. So far only 1 or 3 are valid
            options. 3 means we distinguish active cell, from overlap activity, from neuropil and other. 1 class gives
            better results so far. Don't use it for cell type, the number of classes will be set throught the yaml
            configuration file.
            - n_epochs: (int, default is 30), number of epochs for training the classifier
            - batch_size: (int, default is 8) size of the batch used to train the classifier
            - window_len: (int, default 100) number of frames of the segments given to the classifier
            - max_width: (int, default 25) number of pixels for the width of the frame surrounding the cell. Should be
            big enough so most of the overlaping cell fit in for activity classifier.
            - max_height: (int, default 25) number of pixels for the height of the frame surrounding the cell. Should be
            big enough so most of the overlaping cell fit in for activity classifier.
            - overlap_value: (float, default 0.9), overlap between 2 segments using sliding window of size window_len
            0.9 means contiguous segments will share 90% of their frames.
            - max_n_transformations: (int, default is 6) max number of geometric transformations to apply to each
            segment.
            - pixels_around: (int, default is 0), number of pixels to add around the mask of the cell (for activity
            classifier)
            - with_augmentation_for_training_data: (bool, default is True): is True, then geometric transformations are
            applied to the dataset
            - buffer: (int, default is 1): indicated of how many pixels to inflate the mask of the cell.
            - split_values: (tuple of 3 floats, default is (0.8, 0.2, 0)), tuple of 3 floats, the sum should be equal
            to 1. Give the distribution of the dataset into training, validation and test
            - loss_fct: (str, default is 'binary_crossentropy' is using_multi_class is 1, 'categorical_crossentropy'
            else), loss function used to train the classifier.
            - with_learning_rate_reduction (bool, default is True), if True, means the learning rate will be reduced
            according to the following parameters
            - learning_rate_reduction_patience: (int, default is 2) number of epochs before reducing the learning
            rate if the validation accuracy has not improved, with_learning_rate_reduction needs to be True
            - learning_rate_start: (float, default is 0.001) default learning rate to start with
            - with_early_stopping: (bool, True) if True, then early stopping is activated, if the classifier doesn't
            progress for a given number of epochs indicated through the arg early_stop_patience
            - early_stop_patience: (int, default if 15): number of epochs before the training stops if no progress is
            made (based on validation accuracy values)
            - model_descr  (str, default is ''), sring describing the model, the string will be added to the name of the
            file used to save the model
            - with_shuffling (bool, default True), if True, the segments will be shuffle before added to training or
            validation dataset
            - seed_value (int, default is 42), if not None, used as seed for the shuffling of segments, giving a seed
            means the shuffle will always be the same for a given dataset.
            - main_ratio_balance: (tuple of 3 floats, default is (0.6, 0.2, 0.2)), sequence of 3 float, the sum should
            be equal to 1. Used for activity classifier, precise the proportion in the final training dataset
            between sequence according to real transient, fake transient and "neuropil"
            - crop_non_crop_ratio_balance: (tuple of 2 floats, default is (-1, -1)), use for stratification in activity
            classifier, if values are -1, we don't use it. Otherwise allows to balance segments between segment
            with transient cropped versus not cropped.
            - non_crop_ratio_balance: (tuple of 2 floats, default is (-1, -1)), use for stratification in activity
            classifier, if values are -1, we don't use it. Otherwise allows to balance segments between segment
            with one transient vers more than one transient.
            - with_model_check_point: (bool, default is True) allows to save weights of the classifier at each epoch
            - verbose: (int, default is 2), 0 no verbose, 1 main outputs printed, 2 all outputs printed
            - dropout_value: (float, default 0.5), dropout between CNN layers
            - dropout_value_rnn: (float, default 0.5), dropout between RNN layers
            - dropout_at_the_end: (float, default 0), dropout value at the end of the model
            - with_batch_normalization: (bool, default False), if True use batch normalization
            - optimizer_choice: (str, default is "RMSprop"), optimizer to use, choices "SGD", "RMSprop","Adam"
            - activation_fct: (str, default is "swish") , activation function to use, you can choose any activation
            function available in TensorFlow, swish is also available.
            - without_bidirectional: (bool, default is False), if True, LSTM is not bidirectionnal
            - conv_filters: (tuple of 4 int, default is (64, 64, 128, 128)), the dimensionality of the output space
            (i.e. the number of filters in the convolution) sequence of 4 integers,
            representing the filters of the 4 convolution layers
            - lstm_layers_size (sequence of int, default is (128, 256)), number of LSTM layer and size of each layer.
            - bin_lstm_size (int, default is 256), size of the LSTM layer used in bin et al.
            - use_bin_at_al_version (bool, default is True), using model inspired from the paper from Bin et al.
            - apply_attention: (bool, default is True), if True, attention mechanism is used
            - apply_attention_before_lstm: (bool, default is True), if True it means attention mechanism will be apply
            before LSTM
            - use_single_attention_vector (bool, default is False), if True us single attention vector
            - cell_type_categories_yaml_file: (str, default is None) path and filename of the yaml file used to c
            configure the classifier for cell type (types of cell, number of classes). If None, then
            cell_type_categories_default.yaml will be used with pyramidal cells and interneuron and 2 classes.
            - n_windows_len_to_keep_by_cell: (int, default 2), used only for cell type classifier, indicate how many
            segment of length window_len to keep for training. If too many segment are given then the classifier might
            not be able to generalize well
            - frames_to_avoid_for_cell_type: (sequence of int, default []), list of frame indices. If given, then
            segment than contains one of those indices won't be add to the training. Useful for example if movies are
            concatenated.
    """

    def __init__(self, **kwargs):
        """
        Construct a model. Use arguments to parametrize it.
        Args:
            **kwargs:
        """

        # give the code associated to a cell_type, will be filled by load_cell_type_categories_from_yaml_file()
        self.cell_type_to_code_dict = dict()
        # give the cell_type associated to a code, will be filled by load_cell_type_categories_from_yaml_file()
        self.cell_type_from_code_dict = dict()

        # allows to give a .h5 file representing a partly trained model
        # the training will be resumed from there
        # Caution: the learning rate should be the same as used in the last epoch
        self.partly_trained_model = kwargs.get("partly_trained_model", None)
        # if False, save the full model
        self.save_weigths_only = kwargs.get("save_only_the_weitghs", True)

        self.tiffs_dirname = kwargs.get("tiffs_dirname", None)

        self.n_gpus = kwargs.get("n_gpus", 1)
        self.using_multi_class = kwargs.get("using_multi_class", 1)  # 1 or 3 so far
        if self.using_multi_class not in [1, 3]:
            raise Exception(f"using_multi_class can take only 1 or 3 as value. "
                            f"Value passed being {self.using_multi_class}")

        # indicate if the classifier is made to classify cell_type
        # if False, then we use the classifier to classifier cell activity
        # so far it works just a 1 class classifier, and give the probably that a cell is an interneuron
        self.cell_type_classifier_mode = kwargs.get("cell_type_classifier_mode", False)
        # used for cell_type, add an input with all pixels
        self.with_all_pixels = kwargs.get("with_all_pixels", False)
        if self.cell_type_classifier_mode:
            my_path = os.path.abspath(os.path.dirname(__file__))
            yaml_file = kwargs.get("cell_type_categories_yaml_file",
                                   os.path.join(my_path, "cell_type_categories_default.yaml"))
            self.load_cell_type_categories_from_yaml_file(yaml_file=yaml_file)
            # if cell_type_classifier mode sor no multi class mode available
            # self.using_multi_class = 1
        # used only for cell type classifier
        self.n_windows_len_to_keep_by_cell = kwargs.get("n_windows_len_to_keep_by_cell", 2)

        # used to avoid that a given frame is not added in segments used to learn cell type
        # could be useful if movies are concatenated. Another method is to use doubtful_frames
        # when creating cinac files using the GUI.
        self.frames_to_avoid_for_cell_type = kwargs.get("frames_to_avoid_for_cell_type", [])

        self.n_epochs = kwargs.get("n_epochs", 30)
        # multiplying by the number of gpus used as batches will be distributed to each GPU
        self.batch_size = kwargs.get("batch_size", 8) * self.n_gpus

        self.window_len = kwargs.get("window_len", 100)
        self.max_width = kwargs.get("max_width", 25)
        self.max_height = kwargs.get("max_height", 25)
        self.max_n_transformations = kwargs.get("max_n_transformations", 6)  # TODO: 6
        self.pixels_around = kwargs.get("pixels_around", 0)
        self.with_augmentation_for_training_data = kwargs.get("with_augmentation_for_training_data", True)
        self.buffer = kwargs.get("buffer", 1)
        # between training, validation and test data So far test data is not taking in consideration
        self.split_values = kwargs.get("split_values", (0.8, 0.2, 0))
        if self.using_multi_class > 1:
            self.loss_fct = 'categorical_crossentropy'
        else:
            self.loss_fct = 'binary_crossentropy'

        self.with_learning_rate_reduction = kwargs.get("with_learning_rate_reduction", True)
        self.learning_rate_reduction_patience = kwargs.get("learning_rate_reduction_patience", 2)
        # first learning rate value, could be decreased later if with_learning_rate_reduction is set to True
        self.learning_rate_start = kwargs.get("learning_rate_start", 0.001)
        self.with_model_check_point = kwargs.get("with_model_check_point", True)

        self.verbose = kwargs.get("verbose", 2)

        # ---------------------------
        # Model related (used to build the model)
        # ---------------------------
        self.overlap_value = kwargs.get("overlap_value", 0.9)  # TODO: 0.9
        self.dropout_value = kwargs.get("dropout_value", 0.5)
        self.dropout_value_rnn = kwargs.get("dropout_value_rnn", 0.5)
        self.dropout_at_the_end = kwargs.get("dropout_at_the_end", 0)
        self.with_batch_normalization = kwargs.get("with_batch_normalization", False)
        self.optimizer_choice = kwargs.get("optimizer_choice", "RMSprop")  # "SGD"  used to be "RMSprop"  "Adam", SGD
        self.activation_fct = kwargs.get("activation_fct", "swish")
        self.without_bidirectional = kwargs.get("without_bidirectional", False)
        # the dimensionality of the output space (i.e. the number of filters in the convolution)
        # sequence of 4 integers, representing the filters of the 4 convolution layers
        self.conv_filters = kwargs.get("conv_filters", (64, 64, 128, 128))
        if len(self.conv_filters) != 4:
            raise Exception(f"conv_filters should be of length 4, you gave {self.conv_filters}")
        # TODO: try 256, 256, 256
        self.lstm_layers_size = kwargs.get("lstm_layers_size", (128, 256))  # TODO: 128, 256 # 128, 256, 512
        self.bin_lstm_size = kwargs.get("bin_lstm_size", 256)
        self.use_bin_at_al_version = kwargs.get("use_bin_at_al_version", True)  # TODO: True
        self.apply_attention = kwargs.get("apply_attention", True)  # TODO: True
        self.apply_attention_before_lstm = kwargs.get("apply_attention_before_lstm", True)
        self.use_single_attention_vector = kwargs.get("use_single_attention_vector", False)

        self.with_early_stopping = kwargs.get("with_early_stopping", True)
        self.early_stop_patience = kwargs.get("early_stop_patience", 15)  # 10
        self.model_descr = kwargs.get("model_descr", "")
        self.with_shuffling = kwargs.get("with_shuffling", True)
        self.seed_value = kwargs.get("seed_value", None)  # use None to not use seed, used to be 42
        # main_ratio_balance = (0.6, 0.2, 0.2)
        self.main_ratio_balance = kwargs.get("main_ratio_balance", (0.7, 0.2, 0.1))
        self.crop_non_crop_ratio_balance = kwargs.get("crop_non_crop_ratio_balance", (-1, -1))  # (0.8, 0.2)
        self.non_crop_ratio_balance = kwargs.get("non_crop_ratio_balance", (-1, -1))  # (0.85, 0.15)
        # Maximum number of processes to spin up when using process-based threading
        self.workers = kwargs.get("workers", 10)

        self.results_path = kwargs.get("results_path", None)
        if self.results_path is None:
            raise Exception("You must set a results_path to indicate where to save the network files")

        # will be set in self.prepare_model()
        self.parallel_model = None

        if self.cell_type_classifier_mode:
            self.movie_patch_generator = \
                MoviePatchGeneratorForCellType(window_len=self.window_len, max_width=self.max_width,
                                               max_height=self.max_height,
                                               pixels_around=self.pixels_around,
                                               buffer=self.buffer,
                                               using_multi_class=self.using_multi_class,
                                               with_all_pixels=self.with_all_pixels,
                                               cell_type_classifier_mode=self.cell_type_classifier_mode)
        else:
            self.movie_patch_generator = \
                MoviePatchGeneratorMaskedVersions(window_len=self.window_len, max_width=self.max_width,
                                                  max_height=self.max_height,
                                                  pixels_around=self.pixels_around,
                                                  buffer=self.buffer, with_neuropil_mask=True,
                                                  using_multi_class=self.using_multi_class,
                                                  cell_type_classifier_mode=self.cell_type_classifier_mode)
        # number of inputs that take our model
        self.n_inputs = self.movie_patch_generator.n_inputs

        # data (instances of MoviePatchData) used for training and validating the classifier
        # will be split between training and data according to self.split_values when running the model
        self.inputs_list = []
        # list of tuple containing an instance of cinac_file_reader and a segment (tuple of 3 int)
        # to use to build training and validation data
        # if self.cell_type_classifier_mode:
        #     # TODO: same code as with activity, to create as many h5 files as needed for validation and training
        self.cinac_file_readers_and_segments = []
        # else:
        #     # dict with first key being training, last validation
        #     self.cinac_file_readers_and_segments = {"training": [], "validation": []}
        self.cinac_file_readers_cells_dict = dict()
        # should be the same length of self.cinac_file_readers_and_segments or empty
        # associate to each cinac_file an ID. An ID can be common to several cinac_file
        # will be used to segregate the data, so the ID with less data will be more augmented
        # if self.cell_type_classifier_mode:
        self.session_ids = []
        # contains the index of the segment that should not be put in the validation dataset, but only in the training
        # one. The index should mathc the ones in  self.cinac_file_readers_and_segments
        self.only_for_training_segments = []
        # make sur those segments won't be removed while stratifying the segments.
        # The index should mathc the ones in  self.cinac_file_readers_and_segments
        self.to_keep_absolutely_segments = []
        # indicate if we should keep absolutely segment that are under a certain number of frames
        # put it to zero to keep none based on the frames count.
        # semgents in self.to_keep_absolutely_segments are still kept no matter what
        self.keep_short_segments = kwargs.get("keep_short_segments", 2000)
        self.keep_short_segments_only_for_training = kwargs.get("keep_short_segments_only_for_training", True)
        # means don't you use cinac files to get movie inputs, but individual tiffs (one by frame)
        self.using_splitted_tiff_cinac_movie = kwargs.get("using_splitted_tiff_cinac_movie", True)
        # keep the count of frames in ground truth data
        self.total_frames_as_ground_truth = 0
        # number of frames only used for training
        # will be useful to change the split value between training and validation
        self.total_frames_only_for_training = 0
        self.train_data_list = []
        self.validation_data_list = []
        self.input_shape = None
        self.training_generator = None
        self.validation_generator = None

        # Set a learning rate annealer
        # from: https://www.kaggle.com/shahariar/keras-swish-activation-acc-0-996-top-7
        self.learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc',
                                                         patience=self.learning_rate_reduction_patience,
                                                         verbose=1,
                                                         factor=0.5,
                                                         mode='max',
                                                         min_lr=1e-8)  # used to be: 1e-4 and before 1e-5

        # callbacks to be execute during training
        # A callback is a set of functions to be applied at given stages of the training procedure.
        self.callbacks_list = []

    def load_cell_type_categories_from_yaml_file(self, yaml_file):
        """
        Load cell type names from a yaml file. If more than 2 type cells are given, then a multi-class
        classifier will be used. If 2 type cells are given, then either it could be multi-class or binary classifier,
        then this choice should be given in the parameters of CinacModel.
        If 2 cell-type are given, for binary classifier, it should be precised which cell type should be predicted
        if we get more than 0.5 probability.
        Args:
            yaml_file:

        Returns:

        """

        cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg = \
            read_cell_type_categories_yaml_file(yaml_file=yaml_file, using_multi_class=self.using_multi_class)

        self.cell_type_from_code_dict = cell_type_from_code_dict
        self.cell_type_to_code_dict = cell_type_to_code_dict
        n_cell_categories = len(cell_type_from_code_dict)

        if n_cell_categories < 2:
            raise Exception(f"You need at least 2 cell_type categories, you provided {n_cell_categories}: "
                            f"{list(self.cell_type_from_code_dict.values())}")

        if multi_class_arg is not None:
            if multi_class_arg or (n_cell_categories > 2):
                self.using_multi_class = n_cell_categories
            else:
                self.using_multi_class = 1
        else:
            if n_cell_categories > 2:
                self.using_multi_class = n_cell_categories
            else:
                self.using_multi_class = 1

        # print(f"n_cell_categories {n_cell_categories}")
        # print(f"self.cell_type_from_code_dict {self.cell_type_from_code_dict}")
        # print(f"self.cell_type_to_code_dict {self.cell_type_to_code_dict}")
        # print(f"self.using_multi_class {self.using_multi_class}")

    def add_input_data_from_dir(self, dir_name, verbose=0, display_cells_count=False):
        """
        Add input data loading all .cinac file in dir_name
        If a (UTF-8 encoded) txt file is in the dir, it is parsed in order to give to each cinac_file an id
        the format is for each line:
        cinac_file_name: id
        Args:
            dir_name: str, path + directory from which to load .cinac files
            verbose: 0 no print, 1 informations are printed
            display_cells_count: if True, print the number of cells added in training and the number of sessions associated,
            common field of view are identified using the basename of the ci movie in the cinac file

        Returns:

        """

        cinac_path_w_file_names = []
        cinac_file_names = []
        session_ids_text_file = None
        only_for_training_text_file = None
        to_exclude_text_file = None
        to_keep_absolutely_text_file = None
        # look for filenames in the fisrst directory, if we don't break, it will go through all directories
        for (dirpath, dirnames, local_filenames) in os.walk(dir_name):
            cinac_path_w_file_names = [os.path.join(dirpath, f) for f in local_filenames if f.endswith(".cinac")]
            cinac_file_names = [f for f in local_filenames if f.endswith(".cinac")]
            text_files = [os.path.join(dirpath, f) for f in local_filenames if f.endswith(".txt")]
            for text_file in text_files:
                if "session_ids" in os.path.basename(text_file):
                    session_ids_text_file = text_file
                if "only_for_training" in os.path.basename(text_file):
                    only_for_training_text_file = text_file
                if "to_keep" in os.path.basename(text_file):
                    to_keep_absolutely_text_file = text_file
                if "to_exclude" in os.path.basename(text_file):
                    to_exclude_text_file = text_file
            break

        session_ids = None
        if session_ids_text_file is not None:
            session_ids_dict = dict()
            with open(session_ids_text_file, "r", encoding='UTF-8') as file:
                for line_index, line in enumerate(file):
                    line_list = line.split(':')
                    if len(line_list) < 2:
                        continue
                    session_id = line_list[1].strip()
                    keyword = line_list[0].strip()
                    session_ids_dict[keyword] = session_id

            if len(session_ids_dict) > 0:
                session_ids = []
                for file_name in cinac_file_names:
                    keyword_found = False
                    for keyword in list(session_ids_dict.keys()):
                        if keyword in file_name:
                            session_ids.append(session_ids_dict[keyword])
                            keyword_found = True
                            break
                    if not keyword_found:
                        # by default we could put None, then all the cinac segment with None will have the same id
                        # here we give the name of the file
                        session_ids.append(file_name)

        cinac_files_only_for_training = []
        if only_for_training_text_file is not None:
            with open(only_for_training_text_file, "r", encoding='UTF-8') as file:
                for line_index, line in enumerate(file):
                    if line.endswith(".cinac"):
                        cinac_files_only_for_training.append(line)
                    if line.endswith(".cinac\n"):
                        cinac_files_only_for_training.append(line[:-1])

        cinac_files_to_keep_absolutely = []
        if to_keep_absolutely_text_file is not None:
            with open(to_keep_absolutely_text_file, "r", encoding='UTF-8') as file:
                for line_index, line in enumerate(file):
                    if line.endswith(".cinac"):
                        cinac_files_to_keep_absolutely.append(line)
                    if line.endswith(".cinac\n"):
                        cinac_files_to_keep_absolutely.append(line[:-1])

        cinac_files_to_exclude = []
        if to_exclude_text_file is not None:
            with open(to_exclude_text_file, "r", encoding='UTF-8') as file:
                for line_index, line in enumerate(file):
                    if line.endswith(".cinac"):
                        cinac_files_to_exclude.append(line)
                    if line.endswith(".cinac\n"):
                        cinac_files_to_exclude.append(line[:-1])

        if len(cinac_path_w_file_names) > 0:
            self.add_input_data(cinac_file_names=cinac_path_w_file_names, session_ids=session_ids,
                                verbose=verbose, cinac_files_only_for_training=cinac_files_only_for_training,
                                cinac_files_to_keep_absolutely=cinac_files_to_keep_absolutely,
                                cinac_files_to_exclude=cinac_files_to_exclude, display_cells_count=display_cells_count)

    def add_input_data(self, cinac_file_names, session_ids=None, verbose=0, cinac_files_only_for_training=None,
                       cinac_files_to_keep_absolutely=None, cinac_files_to_exclude=None, display_cells_count=False):
        """
        Add input data.
        Args:
            cinac_file_name: str or list of str, represents the files .cinac
            session_ids: None if no session_id otherwise a tuple, list or just a string (or int) representing the
            id of each cinac_file (one id can be common to several cinac_file)
            verbose: 0 no print, 1 informations are printed
            cinac_files_to_exclude: list of String or None, if the cinac_file_name is in the list, then we don't add it
            display_cells_count: if True, print the number of cells added in training and the number of sessions associated,
            common field of view are identified using the basename of the ci movie in the cinac file

        Returns:

        """
        # keep the count of frames added by session and cell
        # key: session_id, key: cell, value: n_frames
        cinac_files_stat = dict()
        cells_count_sum = 0
        # set of strings representing field of views
        fov_set = set()
        if isinstance(cinac_file_names, str):
            cinac_file_names = [cinac_file_names]
        if session_ids is not None:
            if (not isinstance(session_ids, list)) and (not isinstance(session_ids, tuple)):
                session_ids = [session_ids]
            if len(session_ids) != len(cinac_file_names):
                session_ids = None
        for index_file, cinac_file_name in enumerate(cinac_file_names):
            if verbose > 0:
                print(f"Reading {os.path.basename(cinac_file_name)}")
            if cinac_files_to_exclude is not None:
                if os.path.basename(cinac_file_name) in cinac_files_to_exclude:
                    print(f"{os.path.basename(cinac_file_name)} excluded from inputs")
                    continue
            frames_to_keep = None
            cinac_file_reader = CinacFileReader(file_name=cinac_file_name)
            segments_list = cinac_file_reader.get_all_segments()

            # to count the number of cells in the cinac file
            cells_in_cinac_file_set = set()
            if cinac_file_reader.get_ci_movie_file_name() is None:
                print(f"CAREFUL cinac ci_movie file is None in add_input_data() in CinacModel "
                      f"for {os.path.basename(cinac_file_name)}")
                fov_set.add(os.path.basename(cinac_file_name))
            else:
                fov_set.add(os.path.basename(cinac_file_reader.get_ci_movie_file_name()))

            split_cinac_file = False

            if split_cinac_file:
                # here the idea is to split the cinac file  in multiple cinac files, as many as segments in order
                # to avoid conflict in accessing the file while training the classifier with multiprocesses

                if len(segments_list) > 1:
                    dir_path = os.path.dirname(cinac_file_name)
                    dir_path = os.path.join(dir_path, "individual_cinac_files")
                    # if the path doesn't exist, we create it
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                    # creating individual cinac files, or loading them if they exist
                    cinac_file_readers = cinac_file_reader. \
                        create_cinac_file_for_each_segment(dir_path=dir_path,
                                                           return_file_readers=True)
                    # closing the original file
                    cinac_file_reader.close_file()
                else:
                    cinac_file_readers = [cinac_file_reader]
            else:
                cinac_file_readers = [cinac_file_reader]

            for cinac_file_reader in cinac_file_readers:
                segments_list = cinac_file_reader.get_all_segments()
                # a segment represent a cell and given frames with their corresponding ground truth
                # segment is a tuple of 3 int (cell, first_frame, last_frame)
                for segment in segments_list:
                    if os.path.basename(cinac_file_name) not in cinac_files_stat:
                        cinac_files_stat[os.path.basename(cinac_file_name)] = dict()
                    if segment[0] not in cinac_files_stat[os.path.basename(cinac_file_name)]:
                        cinac_files_stat[os.path.basename(cinac_file_name)][segment[0]] = 0
                    cinac_files_stat[os.path.basename(cinac_file_name)][segment[0]] += (segment[2] - segment[1] + 1)
                    if self.cell_type_classifier_mode:
                        # then we first make sure cell_type is available for the given segment
                        if cinac_file_reader.get_segment_cell_type(segment=segment) is None:
                            continue
                    self.cinac_file_readers_and_segments.append((cinac_file_reader, segment))
                    cells_in_cinac_file_set.add(segment[0])

                    # using file_name + cell to ID every cell, in order to split cell between training and validation
                    # set when cell_type_classifier_mode
                    if cinac_file_name + str(segment[0]) not in self.cinac_file_readers_cells_dict:
                        self.cinac_file_readers_cells_dict[cinac_file_name + str(segment[0])] = []
                    self.cinac_file_readers_cells_dict[cinac_file_name + str(segment[0])].append((cinac_file_reader,
                                                                                                  segment))

                    raster_dur = cinac_file_reader.get_segment_raster_dur(segment=segment)
                    if session_ids is not None:
                        self.session_ids.append(session_ids[index_file])
                    if (cinac_files_only_for_training is not None) and len(cinac_files_only_for_training) > 0:
                        if os.path.basename(cinac_file_name) in cinac_files_only_for_training:
                            self.only_for_training_segments.append(len(self.cinac_file_readers_and_segments)-1)
                            self.total_frames_only_for_training += len(raster_dur)
                    if (cinac_files_to_keep_absolutely is not None) and len(cinac_files_to_keep_absolutely) > 0:
                        if os.path.basename(cinac_file_name) in cinac_files_to_keep_absolutely:
                            self.to_keep_absolutely_segments.append(len(self.cinac_file_readers_and_segments)-1)

                    # keeping the count of the number of frames available,
                    # useful for splitting in training and validation

                    self.total_frames_as_ground_truth += len(raster_dur)
            cells_count_sum += len(cells_in_cinac_file_set)

        if display_cells_count:
            print(" ")
            print(f"Total number of different cells added: {cells_count_sum} from {len(fov_set)} FOV")
            print(" ")

        print("***"*50)
        print("Data added as input:")
        total_frames_all_sessions = 0
        total_n_cells_all_sessions = 0
        for session_id, session_dict in cinac_files_stat.items():
            total_frames = 0
            for cell, n_frames in session_dict.items():
                total_frames += n_frames
                total_n_cells_all_sessions += 1
                print(f"{session_id}: cell {cell}, {n_frames} frames")
            print(f"# {session_id}: {total_frames} frames in total")
            total_frames_all_sessions += total_frames
            print("-"*75)
        print(f"{total_n_cells_all_sessions} cells in total for all sessions")
        print(f"{total_frames_all_sessions} frames in total for all sessions")
        print("***" * 50)


    def __build_model(self):
        """

        Returns:

        """

        """
        Attributes used:
        :param input_shape:
        :param lstm_layers_size:
        :param n_inputs:
        :param using_multi_class:
        :param bin_lstm_size:
        :param activation_fct:
        :param dropout_at_the_end: From Li et al. 2018 to avoid disharmony between batch normalization and dropout,
        if batch is True, then we should add dropout only on the last step before the sigmoid or softmax activation
        :param dropout_value:
        :param dropout_value_rnn:
        :param without_bidirectional:
        :param with_batch_normalization:
        :param apply_attention:
        :param apply_attention_before_lstm:
        :param use_single_attention_vector:
        :param use_bin_at_al_version:
        :param conv_filters
        :return:
        """

        # n_frames represent the time-steps
        n_frames = self.input_shape[0]

        ##########################################################################
        #######################" VISION MODEL ####################################
        ##########################################################################
        # First, let's define a vision model using a Sequential model.
        # This model will encode an image into a vector.
        # TODO: Try dilated CNN
        # VGG-like convnet model
        vision_model = Sequential()
        get_custom_objects().update({'swish': Swish(swish)})
        # to choose between swish and relu

        # TODO: Try dilation_rate=2 argument for Conv2D
        # TODO: Try changing the number of filters like 32 and then 64 (instead of 64 -> 128)
        vision_model.add(Conv2D(self.conv_filters[0], (3, 3), padding='same', input_shape=self.input_shape[1:]))
        if self.activation_fct != "swish":
            vision_model.add(Activation(self.activation_fct))
        else:
            vision_model.add(Lambda(swish))
        if self.with_batch_normalization:
            vision_model.add(BatchNormalization())
        vision_model.add(Conv2D(self.conv_filters[1], (3, 3)))
        if self.activation_fct != "swish":
            vision_model.add(Activation(self.activation_fct))
        else:
            vision_model.add(Lambda(swish))
        if self.with_batch_normalization:
            vision_model.add(BatchNormalization())
        # TODO: trying AveragePooling
        vision_model.add(MaxPooling2D((2, 2)))

        vision_model.add(Conv2D(self.conv_filters[2], (3, 3), padding='same'))
        if self.activation_fct != "swish":
            vision_model.add(Activation(self.activation_fct))
        else:
            vision_model.add(Lambda(swish))
        vision_model.add(Conv2D(self.conv_filters[3], (3, 3)))
        if self.activation_fct != "swish":
            vision_model.add(Activation(self.activation_fct))
        else:
            vision_model.add(Lambda(swish))
        if self.with_batch_normalization:
            vision_model.add(BatchNormalization())
        vision_model.add(MaxPooling2D((2, 2)))

        # vision_model.add(Conv2D(256, (3, 3), activation=activation_fct, padding='same'))
        # vision_model.add(Conv2D(256, (3, 3), activation=activation_fct))
        # vision_model.add(Conv2D(256, (3, 3), activation=activation_fct))
        # vision_model.add(MaxPooling2D((2, 2)))
        # TODO: see to add Dense layer with Activation
        vision_model.add(Flatten())
        # size 2048
        # vision_model.add(Dense(2048))
        # if activation_fct != "swish":
        #     vision_model.add(Activation(activation_fct))
        # else:
        #     vision_model.add(Lambda(swish))
        # vision_model.add(Dense(2048))
        # if activation_fct != "swish":
        #     vision_model.add(Activation(activation_fct))
        # else:
        #     vision_model.add(Lambda(swish))

        if self.dropout_value > 0:
            vision_model.add(layers.Dropout(self.dropout_value))

        ##########################################################################
        # ######################" END VISION MODEL ################################
        ##########################################################################

        ##########################################################################
        # ####################### BiDirectionnal LSTM ############################
        ##########################################################################
        # inputs are the original movie patches
        inputs = []
        # encoded inputs are the outputs of each encoded inputs after BD LSTM
        encoded_inputs = []

        for input_index in np.arange(self.n_inputs):
            video_input = Input(shape=self.input_shape, name=f"input_{input_index}")
            inputs.append(video_input)
            # This is our video encoded via the previously trained vision_model (weights are reused)
            encoded_frame_sequence = TimeDistributed(vision_model)(
                video_input)  # the output will be a sequence of vectors

            if self.apply_attention and self.apply_attention_before_lstm:
                # adding attention mechanism
                encoded_frame_sequence = attention_3d_block(inputs=encoded_frame_sequence, time_steps=n_frames,
                                                            use_single_attention_vector=self.use_single_attention_vector)

            for lstm_index, lstm_size in enumerate(self.lstm_layers_size):
                if lstm_index == 0:
                    rnn_input = encoded_frame_sequence
                else:
                    rnn_input = encoded_video

                return_sequences = True
                # if apply_attention and (not apply_attention_before_lstm):
                #     return_sequences = True
                # elif use_bin_at_al_version:
                #     return_sequences = True
                # elif using_multi_class <= 1:
                #     return_sequences = (lstm_index < (len(lstm_layers_size) - 1))
                # else:
                #     return_sequences = True
                if self.without_bidirectional:
                    encoded_video = LSTM(lstm_size, dropout=self.dropout_value_rnn,
                                         recurrent_dropout=0,
                                         return_sequences=return_sequences)(rnn_input)
                    # From Bin et al. test adding merging LSTM results + CNN representation then attention
                    if self.use_bin_at_al_version:
                        encoded_video = layers.concatenate([encoded_video, encoded_frame_sequence])
                else:
                    # recurrent_dropout used to be self.dropout_value_rnn (june 2020)
                    encoded_video = Bidirectional(LSTM(lstm_size, dropout=self.dropout_value_rnn,
                                                       recurrent_dropout=0,
                                                       return_sequences=return_sequences), merge_mode='concat', )(
                        rnn_input)
                    # TODO: See if this shouldn't be outside of the for loop
                    # From Bin et al. test adding merging LSTM results + CNN represnetation then attention
                    if self.use_bin_at_al_version:
                        encoded_video = layers.concatenate([encoded_video, encoded_frame_sequence])

            # TODO: test if GlobalMaxPool1D +/- dropout is useful here ?
            # encoded_video = GlobalMaxPool1D()(encoded_video)
            # encoded_video = Dropout(0.25)(encoded_video)
            # We can either apply attention a the end of each LSTM, or do it after the concatenation of all of them
            # it's the same if there is only one encoded_input
            # if apply_attention and (not apply_attention_before_lstm):
            #     # adding attention mechanism
            #     encoded_video = attention_3d_block(inputs=encoded_video, time_steps=n_frames,
            #                                        use_single_attention_vector=use_single_attention_vector)
            #     if using_multi_class <= 1:
            #         encoded_video = Flatten()(encoded_video)
            encoded_inputs.append(encoded_video)

        if len(encoded_inputs) == 1:
            merged = encoded_inputs[0]
        else:
            # TODO: try layers.Average instead of concatenate
            merged = layers.concatenate(encoded_inputs)
        # From Bin et al. test adding a LSTM here that will take merged as inputs + CNN represnetation (as attention)
        # Return sequences will have to be True and activate the CNN representation
        if self.use_bin_at_al_version:
            # next lines commented, seems like it didn't help at all
            # if with_batch_normalization:
            #     merged = BatchNormalization()(merged)
            # if dropout_rate > 0:
            #     merged = layers.Dropout(dropout_rate)(merged)

            merged = LSTM(self.bin_lstm_size, dropout=self.dropout_value_rnn,
                          recurrent_dropout=0,
                          return_sequences=True)(merged)
            # print(f"merged.shape {merged.shape}")
            if self.apply_attention and (not self.apply_attention_before_lstm):
                # adding attention mechanism
                merged = attention_3d_block(inputs=merged, time_steps=n_frames,
                                            use_single_attention_vector=self.use_single_attention_vector)
            if self.using_multi_class <= 1 or self.cell_type_classifier_mode:
                merged = Flatten()(merged)

        # TODO: test those 7 lines (https://www.kaggle.com/amansrivastava/exploration-bi-lstm-model)
        # number_dense_units = 1024
        # merged = Dense(number_dense_units)(merged)
        # merged = Activation(activation_fct)(merged)
        if self.with_batch_normalization:
            merged = BatchNormalization()(merged)
        if self.dropout_value > 0:
            merged = (layers.Dropout(self.dropout_value))(merged)
        elif self.dropout_at_the_end > 0:
            merged = (layers.Dropout(self.dropout_at_the_end))(merged)
        # dropout_at_the_end: From Li et al. 2018 to avoid disharmony between batch normalization and dropout,
        # if batch is True, then we should add dropout only on the last step before the sigmoid or softmax activation

        # if we use TimeDistributed then we need to return_sequences during the last LSTM
        if self.using_multi_class <= 1:
            # if use_bin_at_al_version:
            #     outputs = TimeDistributed(Dense(1, activation='sigmoid'))(merged)
            # else:
            if self.cell_type_classifier_mode:
                outputs = Dense(1, activation='sigmoid')(merged)
            else:
                outputs = Dense(n_frames, activation='sigmoid')(merged)
            # outputs = TimeDistributed(Dense(1, activation='sigmoid'))(merged)
        else:
            if self.cell_type_classifier_mode:
                outputs = Dense(self.using_multi_class, activation='softmax')(merged)
            else:
                outputs = TimeDistributed(Dense(self.using_multi_class, activation='softmax'))(merged)
        if len(inputs) == 1:
            print(f"len(inputs) {len(inputs)}")
            inputs = inputs[0]

        # print("Creating Model instance")
        video_model = Model(inputs=inputs, outputs=outputs)
        # print("After Creating Model instance")

        return video_model

    def _split_and_stratify_cell_type_mode_data(self, verbose=0):
        """
        Split (between validation and training) and stratify the data, should be
        used when self.cell_type_classifier_mode is True
        Args:
            verbose:

        Returns:

        """
        # we want don't want a same cell to be both in validation and training
        # also we want an equivalent number of frames of both cell types in each side
        # now we need to split the data between training and validation

        # how many frames to add for each cell, as a multiplier of window_len
        n_windows_len_to_keep_by_cell = self.n_windows_len_to_keep_by_cell

        # key is a string representing the cell type, value is the number of frames
        cell_type_frame_count_dict = dict()
        for key, data_list in self.cinac_file_readers_cells_dict.items():
            for data_cell in data_list:
                cinac_file_reader, segment = data_cell
                cell_type = cinac_file_reader.get_segment_cell_type(segment=segment)
                cell_type = cell_type.lower().strip()
                # raster_dur = cinac_file_reader.get_segment_raster_dur(segment=segment)
                # n_frames_segment = len(raster_dur)
            cell_type_frame_count_dict[cell_type] = cell_type_frame_count_dict.get(cell_type, 0) + \
                                                    (n_windows_len_to_keep_by_cell * self.window_len)

        cell_segments_keys = list(self.cinac_file_readers_cells_dict.keys())
        n_cells = len(cell_segments_keys)
        cells_order = np.arange(n_cells)
        if self.seed_value is not None:
            np.random.seed(self.seed_value)
        # randomising the order in which we put cells in training or validation training
        np.random.shuffle(cells_order)
        # counting how many frames should be added for training
        # key is cell_type, value is an int representing the number of frames for each cell_type
        n_frames_for_training_dict = dict()
        n_frames_added_so_far_dict = dict()
        for cell_type, frame_count in cell_type_frame_count_dict.items():
            n_frames_for_training_dict[cell_type] = int(self.split_values[0] * frame_count)
            n_frames_added_so_far_dict[cell_type] = 0

        cell_types = list(cell_type_frame_count_dict.keys())

        cell_types_code = set()
        for cell_type in cell_types:
            if cell_type.lower().strip() not in self.cell_type_to_code_dict:
                raise Exception(f"'{cell_type}' is not a valid cell type, cell type should be one of those: "
                                f"{list(self.cell_type_to_code_dict.keys())}")
            cell_types_code.add(self.cell_type_to_code_dict[cell_type.lower().strip()])
        # if len(cell_types_code) > 2:
        #     raise Exception(f"The maximum number of different cell types is 2 for now, "
        #                     f"you have {len(cell_types_code)} types, "
        #                     f"which are: {[self.cell_type_from_code_dict[code] for code in cell_types_code]} ")

        using_splitted_tiff_cinac_movie = False

        if using_splitted_tiff_cinac_movie:
            if self.tiffs_dirname is None:
                raise Exception(
                    "You need to pass an argument named 'tiffs_dirname' to CinacModel when instantiating it. "
                    "It represents the path where to save the tiffs as individual tiff for each frame. ")
            # we're having a first loop to make sure the cinac file movie frames have already been
            # created in the hardrive has separeted file in order to save memory
            all_already_loaded = True
            for cell_segments_key in cell_segments_keys:
                for data_cell in self.cinac_file_readers_cells_dict[cell_segments_key]:
                    cinac_file_reader, segment = data_cell
                    identifier = f"{cinac_file_reader.base_name}_{segment[0]}_{segment[1]}_{segment[2]}"
                    cinac_recording = CinacRecording(identifier=identifier)
                    is_created = check_one_dir_by_id_exists(identifiers=[identifier],
                                                            results_path=self.tiffs_dirname)
                    if not is_created:
                        movie_data = cinac_file_reader.get_segment_ci_movie(segment=segment)
                        if movie_data is None:
                            continue
                        cinac_movie = CinacSplitedNpyMovie(identifier=identifier,
                                                           already_normalized=True,
                                                           tiffs_dirname=self.tiffs_dirname, tiff_movie=movie_data)
                        all_already_loaded = False
            if not all_already_loaded:
                raise Exception("All calcium movie in cinac files were not available as single frame tiffs. "
                                "Those have been created, you to relaunch the code now. ")

        for cell_segments_key in cell_segments_keys:
            # we use this variable to make a sure a same cell is added to training or validation but not both
            # the count of total number of frames added is updated only after each cell segments have been added
            n_frames_for_this_cell = 0
            cell_type = None
            for data_cell in self.cinac_file_readers_cells_dict[cell_segments_key]:
                cinac_file_reader, segment = data_cell

                identifier = f"{cinac_file_reader.base_name}_{segment[0]}_{segment[1]}_{segment[2]}"
                cinac_recording = CinacRecording(identifier=identifier)
                # movie_data = cinac_file_reader.get_segment_ci_movie(segment=segment)
                # if movie_data is None:
                #     continue
                # cinac_movie = CinacDataMovie(movie=movie_data, already_normalized=True)
                if using_splitted_tiff_cinac_movie:
                    if self.tiffs_dirname is None:
                        raise Exception(
                            "You need to pass an argument named 'tiffs_dirname' to CinacModel when instantiating it. "
                            "It represents the path where to save the tiffs as individual tiff for each frame. ")
                    cinac_movie = CinacSplitedNpyMovie(identifier=identifier,
                                                       tiffs_dirname=self.tiffs_dirname)
                else:
                    cinac_movie = CinacFileReaderMovie(cinac_file_reader=cinac_file_reader,
                                                       segment=segment)
                cinac_recording.set_movie(cinac_movie)

                coords_data = cinac_file_reader.get_segment_cells_contour(segment=segment)
                coords_data = [np.vstack((coord_data[0], coord_data[1])) for coord_data in coords_data]
                invalid_cells = cinac_file_reader.get_segment_invalid_cells(segment=segment)
                # invalid_cells binary array same length as the number of cell, 1 if the cell is invalid
                # invalid cells allows to remove contours, so the classifier don't take it in consideration
                if np.sum(invalid_cells) > 0:
                    new_coords_data = []
                    for cell_index, cell_coord in enumerate(coords_data):
                        if invalid_cells[cell_index] > 0:
                            continue
                        new_coords_data.append(cell_coord)
                    coords_data = new_coords_data
                cinac_recording.set_rois_2d_array(coord=coords_data, from_matlab=False)

                raster_dur = cinac_file_reader.get_segment_raster_dur(segment=segment)
                doubtful_frames = cinac_file_reader.get_segment_doubtful_frames(segment=segment)
                if len(self.frames_to_avoid_for_cell_type) > 0:
                    # we update doubtful_frames
                    if doubtful_frames is None:
                        doubtful_frames = np.zeros(raster_dur.shape, dtype="int8")
                    for frame_to_avoid in self.frames_to_avoid_for_cell_type:
                        if frame_to_avoid < len(doubtful_frames):
                            doubtful_frames[frame_to_avoid] = 1
                cell_type = cinac_file_reader.get_segment_cell_type(segment=segment)
                smooth_traces = cinac_file_reader.get_segment_smooth_traces(segment=segment)
                # raw_traces = cinac_file_reader.get_segment_raw_traces(segment=segment)
                n_frames = len(raster_dur)
                if n_frames < self.window_len:
                    # making sure the segment has the minimum number of frames
                    continue

                cell_type = cell_type.lower().strip()
                cinac_recording.cell_type = cell_type

                # allow to split the data between training and validation
                if n_frames_added_so_far_dict[cell_type] < n_frames_for_training_dict[cell_type]:
                    # then we add data to training
                    frames_step = int(np.ceil(self.window_len * (1 - self.overlap_value)))
                    data_list_to_use = self.train_data_list
                else:
                    # not temporal overlap for validation data, we don't want to do data augmentation
                    frames_step = self.window_len
                    data_list_to_use = self.validation_data_list

                # temporal overlap for data augmentation
                indices_movies = np.arange(0, n_frames, frames_step)

                # list of  int representing the first_frame possible candidate
                # for moviepatch to add for training or validation. We want to keep for each cell only the most active
                # one
                first_frames_to_filter = []

                for i, index_movie in enumerate(indices_movies):
                    break_it = False
                    first_frame = index_movie
                    if (index_movie + self.window_len) == n_frames:
                        break_it = True
                    elif (index_movie + self.window_len) > n_frames:
                        # in case the number of frames is not divisible by sliding_window_len
                        first_frame = n_frames - self.window_len
                        break_it = True
                    # if some frames have been marked as doubtful, we remove them of the training dataset
                    if doubtful_frames is not None:
                        if np.sum(doubtful_frames[np.arange(first_frame, first_frame + self.window_len)]) > 0:
                            continue
                    first_frames_to_filter.append(first_frame)
                    if break_it:
                        break

                # we want to select at least a first_frame to create a moviePatch
                # the idea is to sort the first_frame and the segment that goes with (adding self.window_len)
                # according to the activity of the cell, we're looking for the segment with the highest amplitude peaks
                first_frames_selected = []
                # will contain a score representing the avg amplitude of the highest peaks
                avg_peaks_amplitudes = []

                peaks, properties = scipy.signal.find_peaks(x=smooth_traces, distance=2)
                peak_nums = np.zeros(n_frames, dtype="int8")
                peak_nums[peaks] = 1
                for first_frame in first_frames_to_filter:
                    peaks = np.where(peak_nums[first_frame:first_frame + self.window_len])[0] + first_frame
                    if len(peaks) == 0:
                        # no peaks found
                        avg_peaks_amplitudes.append(0)
                    amplitudes = smooth_traces[peaks]
                    # print(f"len(amplitudes) {len(amplitudes)}")
                    # print(f"amplitudes {amplitudes}")
                    amplitude_threshold = np.percentile(amplitudes, 90)
                    highest_amplitudes = amplitudes[amplitudes >= amplitude_threshold]
                    # print(f"len(highest_amplitudes) {len(highest_amplitudes)}, "
                    #       f"mean {np.round(np.mean(highest_amplitudes), 2)}")
                    avg_peaks_amplitudes.append(np.mean(highest_amplitudes))
                first_frames_order = np.argsort(avg_peaks_amplitudes)
                # from highest to the smallest
                first_frames_order = first_frames_order[::-1]
                # print(f"avg_peaks_amplitudes ordered {np.array(avg_peaks_amplitudes)[first_frames_order]}")
                n_first_frames_to_peak = min(len(first_frames_order), n_windows_len_to_keep_by_cell)
                for index_first_frame in first_frames_order[:n_first_frames_to_peak]:
                    first_frames_selected.append(first_frames_to_filter[index_first_frame])
                n_frames_added = 0
                for first_frame in first_frames_selected:
                    # the cell of interest in the segment is always the cell 0
                    movie_data = MoviePatchData(cinac_recording=cinac_recording, cell=0, index_movie=first_frame,
                                                window_len=self.window_len, session_id=None,
                                                max_n_transformations=self.max_n_transformations,
                                                with_info=None,
                                                cell_type_classifier_mode=self.cell_type_classifier_mode,
                                                encoded_frames=None, decoding_frame_dict=None,
                                                # TODO: see if we can mark which cinac_file to keep absolutely
                                                to_keep_absolutely=False,
                                                ground_truth=self.cell_type_to_code_dict[cell_type.lower().strip()])

                    # adding the data to the training or validation list
                    data_list_to_use.append(movie_data)
                    n_frames_added += self.window_len

                n_frames_for_this_cell += n_frames_added
            if cell_type is not None:
                n_frames_added_so_far_dict[cell_type] += n_frames_for_this_cell

        # in case self.validation_data_list would be empty, we take from training to fill it
        # if enough data are given for training, this shouldn't happen
        if len(self.validation_data_list) == 0:
            raise Exception("self.validation_data_list is empty, probably not enough data has been added as inputs")

        # just to display stat, doesn't modify the data
        if verbose == 1:
            print(f"VALIDATION DATA")
            StratificationCellTypeCamembert(data_list=self.validation_data_list,
                                            description="VALIDATION DATA",
                                            n_max_transformations=6,
                                            debug_mode=True)

        n_max_transformations = self.train_data_list[0].n_available_augmentation_fct

        print("TRAINING DATA")
        # using StratificationDataProcessor in order to stratify the data, so we balance it
        strat_process = StratificationCellTypeDataProcessor(data_list=self.train_data_list,
                                                            n_max_transformations=n_max_transformations,
                                                            description="TRAINING DATA",
                                                            debug_mode=False)
        self.train_data_list = strat_process.get_new_data_list()

    def _split_and_stratify_data_for_window_len_h5(self, verbose=0):
        """
        Split (between validation and training) and stratify the data


        Returns:

        """
        if self.cell_type_classifier_mode:
            self._split_and_stratify_cell_type_mode_data(verbose=verbose)
            return

        # now we need to split the data between training and validation
        n_segments = len(self.cinac_file_readers_and_segments)
        segments_order = np.arange(n_segments)
        if self.seed_value is not None:
            np.random.seed(self.seed_value)
        np.random.shuffle(segments_order)
        # counting how many frames should be added for training

        # n_frames_for_training = int(self.split_values[0] * self.total_frames_as_ground_truth)
        # useful when we can't split a segment
        last_splits_used = []
        print(f"total_frames_as_ground_truth: {self.total_frames_as_ground_truth}")

        for cinac_file_index in segments_order:
            cinac_file_reader, segment = self.cinac_file_readers_and_segments[cinac_file_index]
            # raster_dur represents the ground truth, a binary 1d array, 1 for each frame during
            # which the cell is active
            if self.session_ids is None or (len(self.session_ids) == 0):
                session_id = None
            else:
                session_id = self.session_ids[cinac_file_index]
            raster_dur = cinac_file_reader.get_segment_raster_dur(segment=segment)
            doubtful_frames = cinac_file_reader.get_segment_doubtful_frames(segment=segment)

            n_frames = len(raster_dur)
            # print(f"cinanc_model.py n_frames {n_frames}")
            if n_frames < self.window_len:
                # making sure the segment has the minimum number of frames
                continue
            # we either start by validation or by the training set to split the current cell
            if n_frames * self.split_values[1] < self.window_len:
                # if we don't have enough frames to split between validation and training, we alternate in oder to
                # to respect the split wanted
                if len(last_splits_used) == 0:
                    last_splits_used.append(0)
                else:
                    if np.sum(last_splits_used) / len(last_splits_used) > self.split_values[1]:
                        last_splits_used.append(0)
                    else:
                        last_splits_used.append(1)
                split_orders = [last_splits_used[-1]]
            else:
                # o is training, 1 is validation
                split_orders = [0, 1]
            np.random.shuffle(split_orders)
            index_so_far = 0
            for split_order in split_orders:
                if split_order == 0:
                    # adding to training, with temporal overlap
                    frames_step = int(np.ceil(self.window_len * (1 - self.overlap_value)))
                    data_list_to_use = self.train_data_list
                else:
                    frames_step = self.window_len
                    data_list_to_use = self.validation_data_list

                first_frame = index_so_far
                if len(split_orders) == 1:
                    last_frame = n_frames
                else:
                    last_frame = min(n_frames, first_frame + int(n_frames * self.split_values[split_order]))
                    index_so_far = last_frame
                # temporal overlap for data augmentation
                indices_movies = np.arange(first_frame, last_frame, frames_step)

                # n_frames_added_so_far += n_frames

                for i, index_movie in enumerate(indices_movies):
                    break_it = False
                    first_frame = index_movie
                    if (index_movie + self.window_len) == n_frames:
                        break_it = True
                    elif (index_movie + self.window_len) > n_frames:
                        # in case the number of frames is not divisible by sliding_window_len
                        first_frame = n_frames - self.window_len
                        break_it = True
                    # if some frames have been marked as doubtful, we remove them of the training dataset
                    # not counted for split between validation and training
                    if doubtful_frames is not None:
                        if np.sum(doubtful_frames[np.arange(first_frame, first_frame + self.window_len)]) > 0:
                            # print(f"doubtful_frames segment not counted split {split_order}")
                            continue

                    dir_path = os.path.dirname(cinac_file_reader.file_name)
                    dir_path = os.path.join(dir_path, "individual_cinac_files")
                    # if the path doesn't exist, we create it
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                    # now we want to create a h5 file with just the window_len frames data
                    new_cinac_file_reader = cinac_file_reader.\
                        create_new_cinac_file_for_segment_chunk(dir_path=dir_path,
                                                                segment=segment, first_frame=first_frame,
                                                                last_frame=first_frame + self.window_len - 1)

                    # identifier is base on file_name, each file_reader contains here only one cell and one segment
                    new_identifier = f"{new_cinac_file_reader.base_name}"

                    cinac_recording = CinacRecording(identifier=new_identifier)
                    new_segment = (segment[0], first_frame+segment[1], first_frame + self.window_len - 1 + segment[1])
                    cinac_movie = CinacFileReaderMovie(cinac_file_reader=new_cinac_file_reader,
                                                       segment=new_segment)
                    cinac_recording.set_movie(cinac_movie)

                    coords_data = new_cinac_file_reader.get_segment_cells_contour(segment=new_segment)
                    coords_data = [np.vstack((coord_data[0], coord_data[1])) for coord_data in coords_data]
                    invalid_cells = new_cinac_file_reader.get_segment_invalid_cells(segment=new_segment)
                    # invalid_cells binary array same length as the number of cell, 1 if the cell is invalid
                    # invalid cells allows to remove contours, so the classifier don't take it in consideration
                    # TODO: Fix later if needed
                    taking_invalid_cells_in_consideration = True
                    if taking_invalid_cells_in_consideration:
                        if np.sum(invalid_cells) > 0:
                            new_coords_data = []
                            for cell_index, cell_coord in enumerate(coords_data):
                                if invalid_cells[cell_index] > 0:
                                    continue
                                new_coords_data.append(cell_coord)
                            coords_data = new_coords_data
                    cinac_recording.set_rois_2d_array(coord=coords_data, from_matlab=False)

                    smooth_traces = new_cinac_file_reader.get_segment_smooth_traces(segment=new_segment)
                    raw_traces = new_cinac_file_reader.get_segment_raw_traces(segment=new_segment)

                    new_raster_dur = new_cinac_file_reader.get_segment_raster_dur(segment=new_segment)

                    # give new raw_traces_smooth_traces etc..
                    encoded_frames, decoding_frame_dict = neuronal_activity_encoding(raw_traces=raw_traces,
                                                                                     smooth_traces=smooth_traces,
                                                                                     raster_dur=new_raster_dur,
                                                                                     identifier=new_identifier)
                    # the cell of interest in the segment is always the cell 0
                    movie_data = MoviePatchData(cinac_recording=cinac_recording, cell=0, index_movie=0,
                                                window_len=self.window_len, session_id=session_id,
                                                max_n_transformations=self.max_n_transformations,
                                                with_info=True, encoded_frames=encoded_frames,
                                                cell_type_classifier_mode=self.cell_type_classifier_mode,
                                                decoding_frame_dict=decoding_frame_dict,
                                                # TODO: see if we can mark which cinac_file to keep absolutely
                                                to_keep_absolutely=False,
                                                ground_truth=new_raster_dur)

                    # adding the data to the training or validation list
                    data_list_to_use.append(movie_data)

                    if break_it:
                        break

        # in case self.validation_data_list would be empty, we take from training to fill it
        # if enough data are given for training, this shouldn't happen
        if len(self.validation_data_list) == 0:
            raise Exception(f"Validation list is empty, you might have not pass any valid data")

        # just to display stat, doesn't modify the data
        if verbose == 1:
            StratificationCamembert(data_list=self.validation_data_list,
                                    description="VALIDATION DATA",
                                    n_max_transformations=6,
                                    debug_mode=True)

        n_max_transformations = self.train_data_list[0].n_available_augmentation_fct

        # using StratificationDataProcessor in order to stratify the data, so we balance it
        strat_process = StratificationDataProcessor(data_list=self.train_data_list,
                                                    n_max_transformations=n_max_transformations,
                                                    description="TRAINING DATA",
                                                    debug_mode=False, main_ratio_balance=self.main_ratio_balance,
                                                    crop_non_crop_ratio_balance=self.crop_non_crop_ratio_balance,
                                                    non_crop_ratio_balance=self.non_crop_ratio_balance)
        self.train_data_list = strat_process.get_new_data_list()
        # TODO: shuffle the list
        random.shuffle(self.train_data_list)
        random.shuffle(self.validation_data_list)

    def _split_and_stratify_data(self, verbose=0):
        """
        Split (between validation and training) and stratify the data


        Returns:

        """
        if self.cell_type_classifier_mode:
            self._split_and_stratify_cell_type_mode_data(verbose=verbose)
            return

        # updating the split_values
        new_split_values = self.split_values

        do_update_split_values = False

        if do_update_split_values:
            if self.total_frames_only_for_training > 0:
                new_split_values = [0.5, 0.5]
                # then we change the ratio between training and validation dataset to take in consideration the frames
                # that will be automatically put into the training dataset
                n_frames_to_split = self.total_frames_as_ground_truth - self.total_frames_only_for_training
                n_frames_in_validation = self.total_frames_as_ground_truth * self.split_values[1]
                if n_frames_in_validation > n_frames_to_split:
                    raise Exception(f"Not enough frames available to build the training dataset, "
                                    f"n_frames_in_validation = {n_frames_in_validation}, "
                                    f"n_frames_to_split = {n_frames_to_split}")
                new_split_values[1] = n_frames_in_validation / n_frames_to_split
                new_split_values[0] = 1 - new_split_values[1]
                print("")
                print(f"## new_split_values after considering data only for training: {np.round(new_split_values, 2)}")
                print("")

        # using_splitted_tiff_cinac_movie = False

        if self.using_splitted_tiff_cinac_movie:
            if self.tiffs_dirname is None:
                raise Exception(
                    "You need to pass an argument named 'tiffs_dirname' to CinacModel when instantiating it. "
                    "It represents the path where to save the tiffs as individual tiff for each frame. ")
            # we're having a first loop to make sure the cinac file movie frames have already been
            # created in the hardrive has separeted file in order to save memory
            all_already_loaded = True
            for cinac_file_index, data in enumerate(self.cinac_file_readers_and_segments):
                cinac_file_reader, segment = data
                identifier = f"{cinac_file_reader.base_name}_{segment[0]}_{segment[1]}_{segment[2]}"
                # cinac_recording = CinacRecording(identifier=identifier)
                is_created = check_one_dir_by_id_exists(identifiers=[identifier],
                                                        results_path=self.tiffs_dirname,
                                                        dir_in_id_name=True)
                if not is_created:
                    # movie_data = cinac_file_reader.get_segment_ci_movie(segment=segment)
                    # if movie_data is None:
                    #     continue
                    # # cinac_movie = CinacSplitedNpyMovie(identifier=identifier,
                    # #                                    already_normalized=True,
                    # #                                    tiffs_dirname=self.tiffs_dirname, tiff_movie=movie_data)
                    # cinac_movie = CinacSplitedTiffMovie(identifier=identifier,
                    #                                    already_normalized=False,
                    #                                    tiffs_dirname=self.tiffs_dirname)
                    # For now tiffs must be created outside of the main code
                    all_already_loaded = False
            if not all_already_loaded:
                raise Exception("All calcium movie in cinac files were not available as single frame."
                                "You have to create them")
            else:
                print("All calcium movie in cinac files were  available as single frame")

        # now we need to split the data between training and validation
        n_segments = len(self.cinac_file_readers_and_segments)
        segments_order = np.arange(n_segments)
        if self.seed_value is not None:
            np.random.seed(self.seed_value)
        np.random.shuffle(segments_order)
        # counting how many frames should be added for training

        # n_frames_for_training = int(new_split_values[0] * self.total_frames_as_ground_truth)
        # useful when we can't split a segment
        last_splits_used = []
        # print(f"total_frames_as_ground_truth: {self.total_frames_as_ground_truth}")

        for cinac_file_index in segments_order:
            cinac_file_reader, segment = self.cinac_file_readers_and_segments[cinac_file_index]
            # raster_dur represents the ground truth, a binary 1d array, 1 for each frame during
            # which the cell is active
            if self.session_ids is None or (len(self.session_ids) == 0):
                session_id = None
            else:
                session_id = self.session_ids[cinac_file_index]
            raster_dur = cinac_file_reader.get_segment_raster_dur(segment=segment)
            smooth_traces = cinac_file_reader.get_segment_smooth_traces(segment=segment)
            raw_traces = cinac_file_reader.get_segment_raw_traces(segment=segment)
            doubtful_frames = cinac_file_reader.get_segment_doubtful_frames(segment=segment)

            # identifier is base on file_name, then cell, first and last frame of the segment
            identifier = f"{cinac_file_reader.base_name}_{segment[0]}_{segment[1]}_{segment[2]}"
            # only valid if using full_movie in case of tiff splitting
            cell_index_in_segment = segment[0]
            cinac_recording = CinacRecording(identifier=identifier)
            if self.using_splitted_tiff_cinac_movie:
                if self.tiffs_dirname is None:
                    raise Exception(
                        "You need to pass an argument named 'tiffs_dirname' to CinacModel when instantiating it. "
                        "It represents the path where to save the tiffs as individual tiff for each frame. ")
                # cinac_movie = CinacSplitedNpyMovie(identifier=identifier,
                #                                    tiffs_dirname=self.tiffs_dirname)
                if verbose > 0:
                    print(f"Using CinacSplitedTiffMovie for {identifier}")
                cinac_movie = CinacSplitedTiffMovie(identifier=identifier,
                                                    tiffs_dirname=self.tiffs_dirname)
            else:
                cinac_movie = CinacFileReaderMovie(cinac_file_reader=cinac_file_reader,
                                                   segment=segment)

            cinac_recording.set_movie(cinac_movie)

            if self.using_splitted_tiff_cinac_movie:
                coords_data = cinac_file_reader.get_coords_full_movie()
            else:
                coords_data = cinac_file_reader.get_segment_cells_contour(segment=segment)
            coords_data = [np.vstack((coord_data[0], coord_data[1])) for coord_data in coords_data]
            if self.using_splitted_tiff_cinac_movie:
                invalid_cells = cinac_file_reader.get_invalid_cells()
            else:
                invalid_cells = cinac_file_reader.get_segment_invalid_cells(segment=segment)
            # invalid_cells binary array same length as the number of cell, 1 if the cell is invalid
            # invalid cells allows to remove contours, so the classifier don't take it in consideration
            # TODO: Fix later if needed
            # TODO: If using splitt tiff version, then we need to change the cell index segment[0]
            taking_invalid_cells_in_consideration = True
            if taking_invalid_cells_in_consideration:
                if np.sum(invalid_cells) > 0:
                    new_coords_data = []
                    for cell_index, cell_coord in enumerate(coords_data):
                        if invalid_cells[cell_index] > 0:
                            if cell_index < segment[0]:
                                cell_index_in_segment -= 1
                            continue
                        new_coords_data.append(cell_coord)
                    coords_data = new_coords_data
            cinac_recording.set_rois_2d_array(coord=coords_data, from_matlab=False)

            n_frames = len(raster_dur)
            # print(f"cinanc_model.py n_frames {n_frames}")
            if n_frames < self.window_len:
                # making sure the segment has the minimum number of frames
                continue

            to_keep_absolutely = (cinac_file_index in self.to_keep_absolutely_segments)
            if not to_keep_absolutely and (self.keep_short_segments > 0):
                if n_frames < self.keep_short_segments:
                    to_keep_absolutely = True
                    if self.keep_short_segments_only_for_training:
                        self.only_for_training_segments.append(cinac_file_index)
            if to_keep_absolutely and (verbose > 0):
                print(f"{identifier} to keep absolutely")
            if cinac_file_index in self.only_for_training_segments:
                split_orders = [0]
                if verbose > 0:
                    print(f"{identifier} only used for training dataset")
            else:
                # we either start by validation or by the training set to split the current cell
                if n_frames * new_split_values[1] < self.window_len:
                    # if we don't have enough frames to split between validation and training, we alternate in order to
                    # to respect the split wanted
                    if len(last_splits_used) == 0:
                        last_splits_used.append(0)
                    else:
                        if np.sum(last_splits_used) / len(last_splits_used) > new_split_values[1]:
                            last_splits_used.append(0)
                        else:
                            last_splits_used.append(1)
                    split_orders = [last_splits_used[-1]]
                else:
                    # o is training, 1 is validation
                    split_orders = [0, 1]
            np.random.shuffle(split_orders)
            index_so_far = 0
            for split_order in split_orders:
                # allow to split the data between training and validation
                # if n_frames_added_so_far < n_frames_for_training:
                #     # then we add data to training
                #     frames_step = int(np.ceil(self.window_len * (1 - self.overlap_value)))
                #     data_list_to_use = self.train_data_list
                # else:
                #     # not temporal overlap for validation data, we don't want to do data augmentation
                #     frames_step = self.window_len
                #     data_list_to_use = self.validation_data_list
                if split_order == 0:
                    # adding to training, with temporal overlap
                    frames_step = int(np.ceil(self.window_len * (1 - self.overlap_value)))
                    data_list_to_use = self.train_data_list
                else:
                    frames_step = self.window_len
                    data_list_to_use = self.validation_data_list

                first_frame = index_so_far
                if len(split_orders) == 1:
                    last_frame = n_frames
                else:
                    last_frame = min(n_frames, first_frame + int(n_frames * new_split_values[split_order]))
                    index_so_far = last_frame
                # if split_order == 0:
                #     print(f"Adding to training {last_frame - first_frame + 1} frames for {identifier}")
                # else:
                #     print(f"Adding to validation {last_frame - first_frame + 1} frames for {identifier}")
                # temporal overlap for data augmentation
                indices_movies = np.arange(first_frame, last_frame, frames_step)

                # n_frames_added_so_far += n_frames

                for i, index_movie in enumerate(indices_movies):
                    break_it = False
                    first_frame = index_movie
                    if (index_movie + self.window_len) == n_frames:
                        break_it = True
                    elif (index_movie + self.window_len) > n_frames:
                        # in case the number of frames is not divisible by sliding_window_len
                        first_frame = n_frames - self.window_len
                        break_it = True
                    # if some frames have been marked as doubtful, we remove them of the training dataset
                    # not counted for split between validation and training
                    if doubtful_frames is not None:
                        if np.sum(doubtful_frames[np.arange(first_frame, first_frame + self.window_len)]) > 0:
                            # print(f"doubtful_frames segment not counted split {split_order}")
                            continue
                    encoded_frames, decoding_frame_dict = neuronal_activity_encoding(raw_traces=raw_traces,
                                                                                     smooth_traces=smooth_traces,
                                                                                     raster_dur=raster_dur)

                    if self.using_splitted_tiff_cinac_movie:
                        cell_to_use = cell_index_in_segment
                    else:
                        # the cell of interest in the segment is always the cell 0
                        cell_to_use = 0
                    movie_data = MoviePatchData(cinac_recording=cinac_recording, cell=cell_to_use,
                                                index_movie=first_frame,
                                                window_len=self.window_len, session_id=session_id,
                                                max_n_transformations=self.max_n_transformations,
                                                with_info=True, encoded_frames=encoded_frames,
                                                cell_type_classifier_mode=self.cell_type_classifier_mode,
                                                decoding_frame_dict=decoding_frame_dict,
                                                # TODO: see if we can mark which cinac_file to keep absolutely
                                                to_keep_absolutely=to_keep_absolutely,
                                                ground_truth=raster_dur[first_frame:first_frame + self.window_len])

                    # adding the data to the training or validation list
                    data_list_to_use.append(movie_data)

                    if break_it:
                        break

        # in case self.validation_data_list would be empty, we take from training to fill it
        # if enough data are given for training, this shouldn't happen
        if len(self.validation_data_list) == 0:
            raise Exception("Validation set is empty")
            # print(f"## cinac_model.py len(self.validation_data_list) == 0")
            # n_patches_in_training = len(self.train_data_list)
            # print(f"cinac_model.py n_patches_in_training {n_patches_in_training}")
            # patches_order = np.arange(n_patches_in_training)
            # if seed_value is not None:
            #     np.random.seed(seed_value)
            # np.random.shuffle(patches_order)
            # n_patches_for_training = int(new_split_values[0] * n_patches_in_training)
            # n_patches_for_validation = n_patches_in_training - n_patches_for_training
            # for index in np.arange(n_patches_for_validation):
            #     self.validation_data_list.append(self.train_data_list[patches_order[index]])
            # new_train_list = []
            # for index in np.arange(n_patches_for_validation, n_patches_in_training):
            #     new_train_list.append(self.train_data_list[patches_order[index]])
            # self.train_data_list = new_train_list

        # just to display stat, doesn't modify the data
        if verbose == 1:
            StratificationCamembert(data_list=self.validation_data_list,
                                    description="VALIDATION DATA",
                                    n_max_transformations=6,
                                    debug_mode=True)

        n_max_transformations = self.train_data_list[0].n_available_augmentation_fct

        # using StratificationDataProcessor in order to stratify the data, so we balance it
        strat_process = StratificationDataProcessor(data_list=self.train_data_list,
                                                    n_max_transformations=n_max_transformations,
                                                    description="TRAINING DATA",
                                                    debug_mode=False, main_ratio_balance=self.main_ratio_balance,
                                                    crop_non_crop_ratio_balance=self.crop_non_crop_ratio_balance,
                                                    non_crop_ratio_balance=self.non_crop_ratio_balance)
        self.train_data_list = strat_process.get_new_data_list()

        random.shuffle(self.train_data_list)
        random.shuffle(self.validation_data_list)

    def prepare_model(self, verbose=0):
        """
        Will build the model that will be use to fit the data.
        Should be called only after the data has been set.
        Returns:

        """

        if len(self.cinac_file_readers_and_segments) == 0:
            print("No input data has been added, use add_input_data() method")
            return

        # splitting the data in train_data_list and validation_data_list and stratifying it
        self._split_and_stratify_data(verbose=verbose)

        # first building the generator that will allow the generate the data for each batch during network iterations
        params_generator = {
            'batch_size': self.batch_size,
            'window_len': self.window_len,
            'max_width': self.max_width,
            'max_height': self.max_height,
            'pixels_around': self.pixels_around,
            'buffer': self.buffer,
            'is_shuffle': True}

        self.training_generator = DataGenerator(self.train_data_list,
                                                with_augmentation=self.with_augmentation_for_training_data,
                                                movie_patch_generator=self.movie_patch_generator,
                                                **params_generator)
        self.validation_generator = DataGenerator(self.validation_data_list, with_augmentation=False,
                                                  movie_patch_generator=self.movie_patch_generator,
                                                  **params_generator)
        self.input_shape = self.training_generator.input_shape

        if self.using_multi_class > 1:
            dependencies = dict()
        else:
            dependencies = {
                'sensitivity': sensitivity,
                'specificity': specificity,
                'precision': precision
            }
            # dependencies = {
            #     'sensitivity': tf.keras.metrics.Recall(),
            #     'specificity': tf.keras.metrics.SpecificityAtSensitivity(sensitivity=0.5),
            #     'precision': tf.keras.metrics.Precision()
            # }
            # tf.keras.metrics.Recall(), tf.keras.metrics.Precision()
        if self.input_shape is None:
            raise Exception("prepare_model() cannot be called before the data has been provided to the model")
        if self.n_gpus == 1:
            print("Building the model on 1 GPU")
            if self.partly_trained_model is not None:
                model = load_model(self.partly_trained_model, custom_objects=dependencies)
            else:
                model = self.__build_model()
        else:
            print(f"Building the model on {self.n_gpus} GPU")
            # We recommend doing this with under a CPU device scope,
            # so that the model's weights are hosted on CPU memory.
            # Otherwise they may end up hosted on a GPU, which would
            # complicate weight sharing.
            # https://www.tensorflow.org/api_docs/python/tf/keras/utils/multi_gpu_model
            with tf.device('/cpu:0'):
                if self.partly_trained_model is not None:
                    model = load_model(self.partly_trained_model, custom_objects=dependencies)
                else:
                    model = self.__build_model()
        print(model.summary())

        if self.n_gpus > 1:
            self.parallel_model = multi_gpu_model(model, gpus=self.n_gpus)
        else:
            self.parallel_model = model

        # Save the model architecture
        classifier_name = "cell_type" if self.cell_type_classifier_mode else "transient"
        with open(f'{self.results_path}/{classifier_name}_classifier_model_architecture_{self.model_descr}.json',
                  'w') as f:
            f.write(model.to_json())

            # Define the optimizer
            # from https://www.kaggle.com/shahariar/keras-swish-activation-acc-0-996-top-7
        if self.optimizer_choice == "Adam":
            optimizer = Adam(lr=self.learning_rate_start, epsilon=1e-08, decay=0.0)
        elif self.optimizer_choice == "SGD":
            # default parameters: lr=0.01, momentum=0.0, decay=0.0, nesterov=False
            optimizer = SGD(lr=self.learning_rate_start, momentum=0.0, decay=0.0, nesterov=False)
        elif self.optimizer_choice == "radam":
            optimizer = RAdam(total_steps=10000, warmup_proportion=0.1, min_lr=1e-5)
        else:
            # default parameters: lr=0.001, rho=0.9, epsilon=None, decay=0.0
            # print("Before RMSprop")
            optimizer = RMSprop(lr=self.learning_rate_start, rho=0.9, epsilon=None, decay=0.0)
            # print("After RMSprop")
            # keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
            # optimizer = 'rmsprop'

            # precision = PPV and recall = sensitiviy but in our case just concerning the active frames
            # the sensitivity and specificity otherwise refers to non-active and active frames classifier
        if self.using_multi_class > 1:
            metrics_to_use = ['acc']
        else:
            metrics_to_use = ['acc', sensitivity, specificity, precision]
            # metrics_to_use = ['acc', tf.keras.metrics.Recall(), tf.keras.metrics.SpecificityAtSensitivity(0.5),
            #                   tf.keras.metrics.Precision()]

        # print(f"Before self.parallel_model.compile")
        self.parallel_model.compile(optimizer=optimizer,
                                    loss=self.loss_fct,
                                    metrics=metrics_to_use)
        # print(f"After self.parallel_model.compile")

        if self.with_learning_rate_reduction:
            self.callbacks_list.append(self.learning_rate_reduction)

        if self.with_early_stopping:
            self.callbacks_list.append(EarlyStopping(monitor="val_acc", min_delta=0,
                                                     patience=self.early_stop_patience, mode="max",
                                                     restore_best_weights=True))

        # not very useful to save best only if we use EarlyStopping
        if self.with_model_check_point:
            # end_file_path = f"_{param.time_str}.h5"
            if self.save_weigths_only:
                if self.cell_type_classifier_mode:
                    # file_path = os.path.join(self.results_path,
                    #                          "cell_type_classifier_weights_{epoch:02d}-{val_accuracy:.4f}.h5")
                    file_path = os.path.join(self.results_path,
                                             "cell_type_classifier_weights_{epoch:02d}.h5")
                else:
                    # file_path = os.path.join(self.results_path,
                    #                      "transient_classifier_weights_{epoch:02d}-{val_accuracy:.4f}.h5")
                    file_path = os.path.join(self.results_path,
                                             "transient_classifier_weights_{epoch:02d}.h5")
            else:
                if self.cell_type_classifier_mode:
                    # file_path = os.path.join(self.results_path,
                    #                          "cell_type_classifier_full_model_{epoch:02d}-{val_accuracy:.4f}.h5")
                    file_path = os.path.join(self.results_path,
                                             "cell_type_classifier_full_model_{epoch:02d}.h5")
                else:
                    # file_path = os.path.join(self.results_path,
                    #                      "transient_classifier_full_model_{epoch:02d}-{val_accuracy:.4f}.h5")
                    file_path = os.path.join(self.results_path,
                                             "transient_classifier_full_model_{epoch:02d}.h5")
            # callbacks_list.append(ModelCheckpoint(filepath=file_path, monitor="val_accuracy", save_best_only=self.save_weigths_only,
            #                                       save_weights_only="True", mode="max"))
            # https://github.com/TextpertAi/alt-model-checkpoint
            # print(f"Before AltModelCheckpoint")
            self.callbacks_list.append(AltModelCheckpoint(file_path, model, save_weights_only=self.save_weigths_only))
            # print(f"After AltModelCheckpoint")
        # print("End prepare_model in cinac_model.py")

    def fit(self):
        if self.training_generator is None:
            print(f"prepare_model() method should be called before fit()")
            return

        # Train model on dataset
        start_time = time.time()

        print(f"self.parallel_model.fit_generator")
        if TF_VERSION[0] != "2":
            history = self.parallel_model.fit_generator(generator=self.training_generator,
                                                        validation_data=self.validation_generator,
                                                        epochs=self.n_epochs,
                                                        use_multiprocessing=False,
                                                        workers=self.workers,
                                                        callbacks=self.callbacks_list, verbose=self.verbose)
        else:
            history = self.parallel_model.fit(x=self.training_generator,
                                              validation_data=self.validation_generator,
                                              epochs=self.n_epochs,
                                              use_multiprocessing=False,
                                              workers=self.workers,
                                              callbacks=self.callbacks_list, verbose=self.verbose)

        # print(f"history.history.keys() {history.history.keys()}")
        stop_time = time.time()
        print(f"Time for fitting the model to the data with {self.n_epochs} epochs: "
              f"{np.round(stop_time - start_time, 3)} s")

        history_dict = history.history
        np.savez(os.path.join(self.results_path, "metrics_history.npz"), **history_dict)
        # TODO: save parameters used + metrics for each epochs
