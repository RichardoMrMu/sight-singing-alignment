auto alignment and evaluation system
--------------------------------------
file and folder tree 
 --__pycache__
| 
 --ali_data  # which use to save alignment reuslts files .including 100 csv about real alignment results,sw and DTW results
|
 --data # include data and label ,data are created from Create_datas_auto.py 
| 
 --fig  # plot image 
|
 --308_score.txt # score note 
|
 --alighment.py # sw alignment algorithm
|
 --config.py # ikmport parameters 
|
 --Create_datas_auto.py # create datas that u can choose parameters like lack and deviation
|
 --DTW.py # DTW alignment algorithm 
|
 --get_label.py # read label files in ./data/label
|
 --main_auto.py # run the whole system 
|
 --README.md
|
 --utils.py 