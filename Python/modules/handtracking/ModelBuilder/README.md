# HOW TO FEED THE DATASET FOR CART CLASSIFIER
* ### STEP 0 : Change of branch
You'll have to change the branch you are working on.
Open git bash in the project directory on your computer, then copy-paste
the following command :
```
git checkout robinson_gesture_recognition_NN
```

* ### STEP 1 : *datasetBuilder.py* [ModelBuilder]

This program goal is to build the training and testing datasets.
To do so, you will have to do hand sign and press the corresponding key on your keyboard.
These are the signs we are going to recognize with the key you have to press :
```
o  :  Open hand   
c  :  Closed hand  
i  :  index up  
p  :  thumb up  
v  :  index and middle finger up  
k  :  index and thumb joined
```
If you don't remember which key to press, just press `h` or `enter`.
To exit the program, press `ESC`. If you have made a mistake, don't 
save the data !
Press `n` to the question `Save data ? (y/n)`.

* ### STEP 2 : *datasetStatistics.py* [ModelBuilder]

Once you run this program, it displays the statistics, 
i.e. the number of registered hand signs for both hands, as follows:  
```
 On left hand : 
 - Nb: 100 	Open hand
 - Nb: 100 	Closed hand
 - Nb: 100 	index up
 - Nb: 100 	thumb up
 - Nb: 100 	index and middle finger up
 - Nb: 100 	index and thumb joined  
TOTAL : 600

 On right hand : 
 - Nb: 100 	Open hand
 - Nb: 100 	Closed hand
 - Nb: 100 	index up
 - Nb: 100 	thumb up
 - Nb: 100 	index and middle finger up
 - Nb: 100 	index and thumb joined  
TOTAL : 600
```
**Make sure that the number of data for each sign and for each hand is the same.**  
In case you saved too many data and you want to delete some of them, 
use the following CSV files (in `ModelBuilder`): 
* `dataset_left.csv`
* `dataset_right.csv`  

You will just need to select and delete 
the unwanted lines.

* ### STEP 3 : Pull
Try to pull the work online.

When you pull, some conflicts may occur, especially on the dataset files
(`dataset_left.csv` and `dataset_right.csv`) when people work on them
at the same time.  
So you should merge the file using the merging tool provided by PyCharm.
This tool pop-up automatically when you pull and you have conflicts.
When you merge, you need to accept your changes and the changes made by the others 
which are causing the conflict.


* ### STEP 4 : Commit and push your work to the git.
Commit your work with a message containing your name and push your work.