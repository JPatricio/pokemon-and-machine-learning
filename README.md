# Pokemon and Machine Learning

## Table of Contents
  - [Identifying Pokemon using Convulotional NNs (WIP)](#identifying-pokemon-using-convulotional-nns)
    - [Data Set](#data-set)
    - [Method](#method)
    - [Results](#results)
    - [Future Work](#future-work)
  - [Generating new Pokemon with Adversarial NNs](#generating-new-pokemon-with-adversarial-nns)
    - [Data Set](#data-set)
    - [Method](#method)
    - [Results](#results)
    - [Future Work](#future-work)
  - [References](#references)

## Identifying Pokemon using a Convulotional NN

A Convulotional Neural Network, (specifically YOLO's implementation) was used to identify 5 of the most commonly appearing pokemon early in the Pokemon anime series.

### Data Set

Since we're doing supervised learning, we will need a relatively large number of image files which contain the pokemon that the net will be learning to identify. The script [get_dataset.py](get_dataset.py) was used to automatically retrieve image files from a number of different sources (gis, bis and fan-made databases). Annotation was carried out using the [BBox Label Tool](https://github.com/puzzledqs/BBox-Label-Tool).

Approximately 100 images (per class) of varying size were used for training and 10 for validation purposes.

### Method

Convolutional Neural Network is the current go-to model for object detection in images. A typical CNN works by:

1. Find features (partial sections of a given image) that are good representatives of the object we're identifying. These features are windows of NxN pixels where N typically varies between 1-5.
2. Convolution the image, or in other words, perform pattern matching of a feature in every possible subsection of the image to see how well it fits (this step is repeated for each feature)
3. Pooling, in a effective image shrinking step where small windows of pixels are analysed and transformed into a single pixel which depends on the values of the pixels in the window.
4. (optional) Normalization step, where all the negative pixel values of the previous layer are changed to zero or to a scale between 0 and 1

These steps can than be repeated for as many times as needed depending on the desired complexity of the network being built.

In this project the used model for training a pokemon detector was [YOLO](https://pjreddie.com/darknet/yolo/). Yolo is essentially a CNN but changes it's base pipeline in two ways: The convolution step is performed simultaneously for features with different sizes (e.g. 1x1 and 3x3) and the larger features are compressed before being convoluted in order for training not to use as many computational resources.

YOLO uses as input images along with textual information about which classes are present in them and the coordinates of their surrounding bounding boxes. Since the output of BBox label tool's output files are slightly different than the expected YOLO input, the [convertYOLO.py](convertYOLO.py) was used, which was heavily based on [this one](https://github.com/Guanghan/darknet/blob/master/scripts/convert.py) created by Guanghan Ning.

TODO: Develop this section

### Results

To validate the results, the trained model was put to the test with episode 17 of the Pokemon anime season 1.

WIP (TODO:Talk about video's fps, resolution, model speed and accuracy)

### Future Work

One of the most important initial decisions behind this approach was to treat each pokemon as a completely different object/class of detection. But let's consider for instance how face recognition systems are performed nowadays. Typically the first step is to detect that there is a face in a picture. Once the face is detected one can extract its features (in other words the landmarks that are common to every face). Finally, compare those features to already known faces to determine whose face it is. So, rather than training a model for every new face we want to classify, it suffices to be able to extract the features of a face in a way well enough that it's possible to a generic model to tell whether or not such features belong to a given known person.

In theory it therefore follows that if we could find such generic features for pokemon, we would then be able to, rather than train a model to detect each pokemon as a class, one could instead try to find methods that could recognize pokemon in an image and then featurize it so it could be identified by a simpler classifier.

That is of course easier said than done, and would require extensive data and research. But it is true that most pokemon can be considered to share a similar mammal-like anatomy, so it might be something to consider doing in the future!

## Generating new Pokemon with Adversarial NNs

Through the use of generative models there was an attempt at generating a all new pokemon with raw unlabeled data.

### Data Set

In this section, several different sets of data were used for individual trainings with different purposes:

1. A collection of around 20 GIS images of each generation 1 pokemon (3000 images)
2. A collection of one image for each pokemon of the current pokedex up to the 7th generation taken from a fan made database (721 images).
3. A collection of around 20 GIS images of each pokemon in the [Pikachu family](http://pokemon.wikia.com/wiki/Pikachu-family_Pok%C3%A9mon) (200 images).
4. A collection of four images for each electric type pokemon of the current pokedex up to the 7th generation taken from a fan made database (160 images)

All images in each of the 4 sets have the same width and height.

### Method

Another branch of research of Convolutional Neural Networks pertains to unsupervised learning. Specifically, using generative CNN models to virtually fabricate new data from observed one is something that has been gaining some traction in the academic work.
What if we could do the same with Pokemon? With the already long list of 700+ unique existing pokemons, designers must be running out of ideas. Could it be that machines are ready to take over in the creative processes?
In this section [DCGAN](https://arxiv.org/pdf/1511.06434.pdf) was used to attempt at generating new pokemon. DCGAN architecture uses two CNN's a generator and a discriminator. The generator's job is to try and come up with images that look like they could fit the dataset. The discriminator's job is to try to tell them apart. With each training iteration both networks get better and better at their task, up to the point where the generator can hallucinate very interesting imagery.

Training was performed by plugging each of the previously described data sets to Taehoon Kim's [implementation of a DCGAN](https://github.com/carpedm20/DCGAN-tensorflow). Parameters were adjusted differently in accordance to the used data set's size and source.

### Results

All generated samples for each data set's training can be found under the [generated samples](generated_samples/) folder.



### Future Work

This task was started from the assumption that there exists generic features that would define what a pokemon is, and that such features could be learnt from adversarial nns in order to create new pokemon.

It's hard to say if that assumption holds, and even if it does, it'd definitely be a non trivial task to determine what shapes/color make a pokemon, what it is.

In any case, the amount of images used for the sake of these experimentations could be considered a bottleneck both because of the small amount and the poor quality of the extracted imagery.

In the future a better tailored dataset will be used to try to further increase the quality of training.


## References


* [YOLO9000: Better, Faster, Stronger](https://arxiv.org/pdf/1612.08242.pdf)
* [Going deeper with convolutions](https://arxiv.org/pdf/1409.4842.pdf)
* [How to train YOLOv2 to detect custom objects](https://timebutt.github.io/static/how-to-train-yolov2-to-detect-custom-objects/)
* [Abusing Generative Adversarial Networks to Make 8-bit Pixel Art](https://medium.com/@ageitgey/abusing-generative-adversarial-networks-to-make-8-bit-pixel-art-e45d9b96cee7)
* [CAN: Creative Adversarial Networks Generating “Art” by Learning About Styles and Deviating from Style Norms∗](https://arxiv.org/pdf/1706.07068.pdf)
* [Unsupervised Representation Learning With Deep Convolutional Generative Adversarial Networks](https://arxiv.org/pdf/1511.06434.pdf)